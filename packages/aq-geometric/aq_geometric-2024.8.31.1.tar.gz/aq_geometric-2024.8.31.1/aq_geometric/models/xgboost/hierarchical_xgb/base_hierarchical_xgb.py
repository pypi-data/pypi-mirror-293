import os
from datetime import datetime
from typing import Dict, List, Tuple, Union, Callable

import uuid
import h3
import torch  # already required, used for serialization
import xgboost as xgb
import numpy as np
import pandas as pd
from torch_geometric.data import Data

from aq_geometric.models.base_model import BaseModel


class BaseAqGeometricXGBModel(BaseModel):
    """
    Train and run inference using data reformed to long format (each row is a single observation for a single station)
    * forecast iteratively for a given station
    * train using X as the values from connected h3 indices
    * inference by forecasting the root node value and then going down from there
    * for each row (h3 index) we take as input the values from the prior timestamp of all connected rows from the graph (same edge index data as the AqHeirEdgeConvModel)
    * we also take as input the forecast values of each row (h3 index) connected to the node but at a coarser resolution
    * these shapes should be the same throughout time as we can handle missing values in the input
    * if the target is missing we can just skip the row!
    Args:
        name (str): the name of the model
        guid (str): the guid of the model
        stations (Union[List, None]): the stations
        features (List[str]): the features
        targets (List[str]): the targets
        num_samples_in_node_feature (int): the number of samples in the node feature
        num_samples_in_node_target (int): the number of samples in the node target
        sample_graph (Data): the sample graph
        finest_resolution (int): the finest resolution
        coarsest_resolution (int): the coarsest resolution
        xgb_kwargs (Dict): the XGBoost kwargs
        verbose (bool): whether to print out information about the model
    """
    def __init__(
        self,
        name: str = "BaseAqGeometricXGBModel",
        guid: str = str(uuid.uuid4()),
        stations: Union[List, None] = None,
        features: List[str] = ["OZONE", "PM2.5", "NO2"],
        targets: List[str] = ["OZONE", "PM2.5", "NO2"],
        num_samples_in_node_feature: int = 48,
        num_samples_in_node_target: int = 12,
        is_iterative: bool = False,
        include_masks_in_features: bool = False,
        include_masks_in_targets: bool = False,
        sample_graph: "Data" = None,
        node_id_to_h3_index_map: Union[dict, None] = None,
        h3_index_to_node_id_map: Union[dict, None] = None,
        finest_resolution: int = 6,
        coarsest_resolution: int = -1,
        reshape_order: str = "F",
        xgb_max_depth: int = 5,
        xgb_n_estimators: int = 256,
        xbg_tree_method: str = "hist",
        xgb_early_stopping_rounds: int = 10,
        xgb_num_boost_round: int = 100,
        xgb_learning_rate: float = 0.08,
        xgb_objective: Union[str, Callable] = "reg:squarederror",
        xgb_model_filename:
        str = "xgb_model.ubj",  # the filename to save the model
        xgb_kwargs: Dict = {},  # additional kwargs for the XGBoost model
        xgb_strategy: str = "multi_output_tree",  # use multi-output model
        verbose: bool = False,
    ):
        assert reshape_order in ["C", "F",
                                 "A"], "reshape_order must be 'C', 'F', or 'A'"
        assert sample_graph is not None or (
            h3_index_to_node_id_map is not None
            and node_id_to_h3_index_map is not None
        ), "either `sample_graph` or `h3_index_to_node_id_map` and `node_id_to_h3_index_map` must be provided"
        if verbose is False:
            # set xgb verbosity to 0
            xgb.set_config(verbosity=0)
        else:
            # use info verbosity
            xgb.set_config(verbosity=2)

        super().__init__(
            name=name,
            guid=guid,
            stations=stations,
            features=features,
            targets=targets,
            num_samples_in_node_feature=num_samples_in_node_feature,
            num_samples_in_node_target=num_samples_in_node_target,
            is_iterative=is_iterative,
        )
        self.finest_resolution = finest_resolution
        self.coarsest_resolution = coarsest_resolution
        self.num_features_in_node_feature = len(features)
        self.num_features_in_node_target = len(targets)
        self.num_edges_for_each_node = 1 + 6 + 1 + 7  # 1 self, 6 same resolution, 1 coarser resolution, 7 finer resolution
        self.reshape_order = reshape_order
        self.include_masks_in_features = include_masks_in_features
        self.include_masks_in_targets = include_masks_in_targets
        self.verbose = verbose

        # process the sample graph to determine structure
        if sample_graph is not None:
            self.node_id_to_h3_index_map = {
                i: v
                for i, v in enumerate(sample_graph.h3_index)
            }  # map node id to h3 index
            self.h3_index_to_node_id_map = {
                v: i
                for i, v in enumerate(sample_graph.h3_index)
            }  # map h3 index to node id
        else:
            self.node_id_to_h3_index_map = node_id_to_h3_index_map
            self.h3_index_to_node_id_map = h3_index_to_node_id_map
        if self.include_masks_in_features:
            self.feature_vector_shape = (-1, 2 * self.num_edges_for_each_node *
                                         self.num_samples_in_node_feature *
                                         self.num_features_in_node_feature
                                         )  # account for mask
        else:
            self.feature_vector_shape = (-1, self.num_edges_for_each_node *
                                         self.num_samples_in_node_feature *
                                         self.num_features_in_node_feature)
        if self.include_masks_in_targets:
            self.target_vector_shape = (-1,
                                        2 * self.num_samples_in_node_target *
                                        self.num_features_in_node_target)
        else:
            self.target_vector_shape = (-1, self.num_samples_in_node_target *
                                        self.num_features_in_node_target)

        # populate the xgb_kawrgs
        xgb_kwargs["max_depth"] = xgb_max_depth
        xgb_kwargs["num_boost_round"] = xgb_num_boost_round
        xgb_kwargs["learning_rate"] = xgb_learning_rate
        xgb_kwargs["objective"] = xgb_objective
        xgb_kwargs["n_estimators"] = xgb_n_estimators
        xgb_kwargs["tree_method"] = xbg_tree_method

        if len(self.features) > 1:
            xgb_kwargs["strategy"] = xgb_strategy

        self.xgb_kwargs = xgb_kwargs
        self.xgb_model = None
        self.xgb_model_filename = xgb_model_filename
        self.xgb_early_stopping_rounds = xgb_early_stopping_rounds

    def fit(self, g: "Data", val_data: Tuple[np.ndarray, np.ndarray]):
        # obtain the training data from `g`
        _, X, y = self.load_from_graph(
            graph=g,
            include_target=True,
            verbose=self.verbose,
            include_masks_in_targets=self.include_masks_in_targets,
            include_masks_in_features=self.include_masks_in_features,
            reshape_order=self.reshape_order,
            num_samples_in_node_feature=self.num_samples_in_node_feature,
            num_features_in_node_feature=self.num_features_in_node_feature,
            num_samples_in_node_target=self.num_samples_in_node_target,
            num_features_in_node_target=self.num_features_in_node_target,
            num_edges_for_each_node=self.num_edges_for_each_node,
        )

        if self.verbose:
            print(
                f"X_samples shape: {np.shape(X)}, y_samples shape: {np.shape(y)}"
            )

        # train the booster using this new data
        if self.xgb_model is None:
            # we need to perform the first fit
            dtrain = xgb.DMatrix(X, y)
            xgb_model = xgb.train(
                params=self.xgb_kwargs,
                dtrain=dtrain,
                evals=[(dtrain, "train"),
                       (xgb.DMatrix(val_data[0], val_data[1]), "validation")],
                early_stopping_rounds=self.xgb_early_stopping_rounds,
            )
            self.xgb_model = xgb_model
        else:
            # we already have a model fit
            self.xgb_model.fit(
                X, y, eval_set=[val_data],
                early_stopping_rounds=self.xgb_early_stopping_rounds,
                xgb_model=self.xgb_model)

    def fit_from_Xy(self, X: np.ndarray, y: np.ndarray,
                    val_data: Tuple[np.ndarray, np.ndarray]):
        if self.verbose:
            print(
                f"X_samples shape: {np.shape(X)}, y_samples shape: {np.shape(y)}"
            )
        # train the booster using this new data
        dtrain = xgb.DMatrix(X, y)
        xgb_model = xgb.train(
            xgb_model=self.xgb_model,
            params=self.xgb_kwargs,
            dtrain=dtrain,
            evals=[(dtrain, "train"),
                   (xgb.DMatrix(val_data[0], val_data[1]), "validation")],
            early_stopping_rounds=self.xgb_early_stopping_rounds,
        )
        self.xgb_model = xgb_model

    def predict(self, g: "Data") -> Tuple[np.ndarray, np.ndarray]:
        """Use the trained boosters to predict the target values for each feature in `g`."""
        assert self.xgb_model is not None, "model must be trained before predicting"
        # obtain the inference data from `g`
        h3_indices, X = self.load_from_graph(
            graph=g,
            include_target=False,
            verbose=self.verbose,
            include_masks_in_targets=self.include_masks_in_targets,
            include_masks_in_features=self.include_masks_in_features,
            reshape_order=self.reshape_order,
            num_samples_in_node_feature=self.num_samples_in_node_feature,
            num_features_in_node_feature=self.num_features_in_node_feature,
            num_samples_in_node_target=self.num_samples_in_node_target,
            num_features_in_node_target=self.num_features_in_node_target,
            num_edges_for_each_node=self.num_edges_for_each_node,
        )

        if self.verbose:
            print(f"final X shape: {np.shape(X)}")

        prediction = self.xgb_model.inplace_predict(X)

        # we need to reshape this prediction to n_h3_index, n_timestamps, n_targets
        prediction = np.reshape(prediction,
                                (-1, self.num_samples_in_node_target,
                                 self.num_features_in_node_target),
                                self.reshape_order)

        return h3_indices, prediction

    def predict_from_X(self, X: np.ndarray) -> np.ndarray:
        """Use the trained boosters to predict the target values for array X."""
        assert self.xgb_model is not None, "model must be trained before predicting"
        # obtain the inference data from `g`
        if self.verbose:
            print(f"final X shape: {np.shape(X)}")

        prediction = self.xgb_model.inplace_predict(X)

        # we need to reshape this prediction to n_h3_index, n_timestamps, n_targets
        prediction = np.reshape(prediction,
                                (-1, self.num_samples_in_node_target,
                                 self.num_features_in_node_target),
                                self.reshape_order)

        return prediction

    def xgb_save(self, path: Union[str, None] = None):
        """Save the model to disk by its booster components."""
        assert self.xgb_model is not None, "model must be trained before saving"
        self.xgb_model.save_model(
            self.xgb_model_filename
        ) if path is None else self.xgb_model.save_model(path)

    def xgb_load(self, path: Union[str, None] = None):
        """Load the model from disk using a path to the top-level where booster components are located."""
        xgb_model = xgb.XGBRegressor()
        xgb_model.load_model(self.xgb_model_filename
                             ) if path is None else xgb_model.load_model(path)
        self.xgb_model = xgb_model

    def eval(self):
        """We match the interface of other models."""
        pass

    def cpu(self):
        """We match the interface of other models."""
        pass

    def save(self, path: str):
        """Save the model to a file."""
        assert self.xgb_model is not None, "model must be trained before saving"

        # ensure the path exists
        # check if the path has a directory
        if os.path.dirname(path):
            # create the directory if it does not exist
            os.makedirs(os.path.dirname(path), exist_ok=True)

        # gather the model data
        model_data = {
            "name": self.name,
            "guid": self.guid,
            "stations": self.stations,
            "features": self.features,
            "targets": self.targets,
            "num_samples_in_node_feature": self.num_samples_in_node_feature,
            "num_samples_in_node_target": self.num_samples_in_node_target,
            "is_iterative": self.is_iterative,
            "finest_resolution": self.finest_resolution,
            "coarsest_resolution": self.coarsest_resolution,
            "reshape_order": self.reshape_order,
            "state_dict": self.xgb_model,
            "node_id_to_h3_index_map": self.node_id_to_h3_index_map,
            "h3_index_to_node_id_map": self.h3_index_to_node_id_map,
            "include_masks_in_features": self.include_masks_in_features,
            "include_masks_in_targets": self.include_masks_in_targets,
            **self.kwargs
        }
        # save the model data
        torch.save(model_data, path)

    def load(self, path: str):
        """Load the model from a file."""
        # load the model data
        model_data = torch.load(path)

        # set the model data
        self.name = model_data["name"]
        self.guid = model_data["guid"]
        self.stations = model_data["stations"]
        self.features = model_data["features"]
        self.targets = model_data["targets"]
        self.num_samples_in_node_feature = model_data[
            "num_samples_in_node_feature"]
        self.num_samples_in_node_target = model_data[
            "num_samples_in_node_target"]
        self.num_features_in_node_feature = len(self.features)
        self.num_features_in_node_target = len(self.targets)
        self.is_iterative = model_data.get(
            "is_iterative", False)  # for backwards compatability
        self.finest_resolution = model_data.get("finest_resolution", 6)
        self.ncoarsest_resolution = model_data.get("coarsest_resolution", -1)
        self.reshape_order = model_data.get("reshape_order", "F")
        self.load_state_dict(model_data["state_dict"])

        # set the kwargs
        for key, value in model_data.items():
            if key not in [
                    "name", "guid", "stations", "features", "targets",
                    "num_samples_in_node_feature",
                    "num_samples_in_node_target",
                    "num_features_in_node_feature",
                    "num_features_in_node_target", "is_iterative", "state_dict"
            ]:
                setattr(self, key, value)

    def load_state_dict(self, state_dict: Dict):
        """We match the interface of other models."""
        self.xgb_model = state_dict

    def _generate_forecasts_iterative(
        self,
        graph: "Data",
        targets: Union[List[str], None] = None,
        include_history: bool = False,
        num_iterations: Union[
            int, None] = None,  # number of iterative forecasting rounds
        sample_freq: str = "1H",
        verbose: Union[List[str], None] = None,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, List[np.ndarray]]:
        """
        Generate forecasts iteratively using the model provided
        """
        raise NotImplementedError

    def _generate_forecasts_direct(
        self,
        graph: "Data",
        targets: Union[List[str], None] = None,
        include_history: bool = False,
        verbose: Union[List[str], None] = None,
    ) -> Tuple[Dict[str, pd.DataFrame], np.ndarray, List[np.ndarray]]:
        """
        Generate forecasts directly using the model provided
        """
        raise NotImplementedError

    @staticmethod
    def load_from_graph(
        graph: "Data",
        include_target: bool = True,
        verbose: bool = False,
        include_masks_in_targets: bool = False,
        include_masks_in_features: bool = False,
        reshape_order: str = "F",
        num_samples_in_node_feature: int = 48,
        num_features_in_node_feature: int = 3,
        num_samples_in_node_target: int = 24,
        num_features_in_node_target: int = 3,
        num_edges_for_each_node: int = 1 + 6 + 7 + 1,
    ) -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray,
                                                    np.ndarray]]:
        """Load the data from the graph and return the X and y components for training or inference.
        
        This method will read the data in the graph and process it for training or inference.
        The first return value is the h3 indices for each sample. The second return value is the X values.
        If `include_target` is True, the third return value is the y values.
        The only values included in the returned data are those whose targets are not NaN. We can handle
        missing values in the X data, but include masks as features which the model can learn to ignore.
        The returned shape is:
        * h3 indices: (n_samples,)
        * X: (n_samples, (n_features * n_samples_per_feature * 2) * (1 + 1 + 6 + 7))  # self, parent, neighbors, children padded with NaNs
        * y: (n_samples, n_targets * n_samples_per_target)

        Args:
            graph (Data): the graph data
            include_target (bool): whether to include the target values
        
        Returns:
            Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, np.ndarray]]: the X and y components with h3 indices
        """
        if include_masks_in_features:
            feature_vector_shape = (-1, 2 * num_edges_for_each_node *
                                    num_samples_in_node_feature *
                                    num_features_in_node_feature)
        else:
            feature_vector_shape = (-1, num_edges_for_each_node *
                                    num_samples_in_node_feature *
                                    num_features_in_node_feature)
        if include_masks_in_targets:
            target_vector_shape = (-1, 2 * num_samples_in_node_target *
                                   num_features_in_node_target)
        else:
            target_vector_shape = (-1, num_samples_in_node_target *
                                   num_features_in_node_target)

        graph_data = graph.x.numpy()
        graph_data_masks = graph.x_mask.numpy()
        graph_target = graph.y.numpy(
        )  # this will exist whether or not we return targets
        graph_target_masks = graph.y_mask.numpy()

        h3_index_to_node_id_map = {v: i for i, v in enumerate(graph.h3_index)}

        # each "row" in our data represents a (single?) observation of a single station
        # we have structure imposed by our graph such that each "row" has:
        # * a value for each training feature (may be missing) (1, n_train_features)
        # * a mask for whether each above feature was missing (1, n_train_features)
        # * a value for each target feature (may be missing) (1, n_target_features)
        # * a mask for whether each above feature was missing (1, n_target_features)
        # * a value for each connected node at the same resolution (1, n_same_connected_nodes, n_train_features)
        # * a mask for whether each above feature was missing (1, n_same_connected_nodes, n_train_features)
        # * a value for each connected node at a coarser resolution (1, n_coarse_connected_nodes, n_target_features)
        # * a mask for whether each above feature was missing (1, n_coarse_connected_nodes, n_target_features)
        # * a value for each connected node at a finer resolution (1, n_fine_connected_nodes, n_target_features)
        # * a mask for whether each above feature was missing (1, n_fine_connected_nodes, n_target_features)
        # given the fact that we can handle missing values, we can enforce structure that:
        # * there are 6 nodes connected at the same resolution
        # * there is one node (the parent) at a coarser resolution
        # * there are 7 nodes (the children) at a finer resolution
        # we can enforce this structure by reshaping the data
        # get the x and y components of the data

        # collect X samples and y samples
        X_samples = []
        y_samples = [
        ]  # if include_target is False, we do not collect y samples
        sample_h3_indices = []  # we can collect the h3 indices for each sample

        # iterate through each h3 index
        for h3_index in graph.h3_index:
            # the first values in `X` are the values of the feature and the masks for the feature, respectively
            # for a feature with n_samples samples, this is the first 2*n_samples values (value, ..., value, mask, ..., mask)
            # we can get the index of the h3 index in the graph data
            node_id = h3_index_to_node_id_map[h3_index]

            # this is the target (y) data
            # before proceeding we can check that the target is not NaN
            node_data_target = graph_target[
                node_id, :, :]  # we capture the target value
            node_data_target_mask = graph_target_masks[
                node_id, :, :]  # we capture the target mask
            # check if any values in the node_data_target_mask are 1
            if (any(node_data_target_mask.reshape(-1) == 0)
                    or any(graph_data_masks[node_id, -1, :].reshape(-1) == 0)
                ) and include_target:
                if verbose:
                    print(
                        f"skipping {h3_index} (node id {node_id}) due to NaN values in target (`include_target` is True)"
                    )
                continue

            # we start with two (1, D) vectors of the correct shape
            # for the target this is simple (1, num_samples_in_node_target * num_features_in_node_target)
            if include_masks_in_targets:
                y = np.concatenate([
                    np.reshape(node_data_target, (1, -1), order=reshape_order),
                    np.reshape(node_data_target_mask,
                               (1, -1), order=reshape_order)
                ], axis=1)
            else:
                y = np.reshape(node_data_target, (1, -1), order=reshape_order)

            # this is the feature (X) data
            node_data = graph_data[
                node_id, :, :]  # we capture ALL feature values
            node_data_masks = graph_data_masks[
                node_id, :, :]  # we capture ALL feature masks

            # update the X values
            if include_masks_in_features:
                X = np.concatenate([
                    np.reshape(node_data, (1, -1), reshape_order),
                    np.reshape(node_data_masks, (1, -1), reshape_order)
                ], axis=1)
            else:
                X = np.reshape(node_data, (1, -1), reshape_order)

            if verbose:
                print(f"after obtaining node values, X shape: {np.shape(X)}")

            # we need to handle the special case "root" h3 index
            # when h3_index is root we do not have any neighbors or parents
            if h3_index != "root":
                # handle child nodes, if any (otherwise we assign missing values)
                child_h3_indices = h3.h3_to_children(h3_index)
                for child_h3_index in child_h3_indices:
                    # get the node id
                    if child_h3_index in h3_index_to_node_id_map:
                        child_node_id = h3_index_to_node_id_map[child_h3_index]
                        # get the data
                        child_node_data = graph_data[child_node_id, :, :]
                        child_node_data_masks = graph_data_masks[
                            child_node_id, :, :]
                    else:
                        # make NaNs of the appropriate shape
                        child_node_data = np.full(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature), np.nan)
                        child_node_data_masks = np.zeros(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature))

                    # update the X values
                    if include_masks_in_features:
                        X = np.concatenate([
                            X,
                            np.reshape(child_node_data,
                                       (1, -1), reshape_order),
                            np.reshape(child_node_data_masks,
                                       (1, -1), reshape_order)
                        ], axis=1)
                    else:
                        X = np.concatenate([
                            X,
                            np.reshape(child_node_data, (1, -1), reshape_order)
                        ], axis=1)

                if verbose:
                    print(
                        f"after obtaining child values, X shape: {np.shape(X)}"
                    )

                # handle neighbors
                neighbor_h3_indices = [
                    h3_id for h3_id in h3.k_ring(h3_index, 1)
                    if h3_id != h3_index
                ]
                for neighbor_h3_index in neighbor_h3_indices:
                    # get the node id
                    if neighbor_h3_index in h3_index_to_node_id_map:
                        neighbor_node_id = h3_index_to_node_id_map[
                            neighbor_h3_index]
                        # get the data
                        neighbor_node_data = graph_data[neighbor_node_id, :, :]
                        neighbor_node_data_masks = graph_data_masks[
                            neighbor_node_id, :, :]
                    else:
                        # make NaNs of the appropriate shape
                        neighbor_node_data = np.full(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature), np.nan)
                        neighbor_node_data_masks = np.zeros(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature))
                    # update the X values
                    if include_masks_in_features:
                        X = np.concatenate([
                            X,
                            np.reshape(neighbor_node_data,
                                       (1, -1), reshape_order),
                            np.reshape(neighbor_node_data_masks,
                                       (1, -1), reshape_order)
                        ], axis=1)
                    else:
                        X = np.concatenate([
                            X,
                            np.reshape(neighbor_node_data,
                                       (1, -1), reshape_order)
                        ], axis=1)

                if verbose:
                    print(
                        f"after obtaining neighbor values, X shape: {np.shape(X)}"
                    )

                # handle parent if possible
                if h3.h3_get_resolution(h3_index) > 0:
                    parent_h3_index = h3.h3_to_parent(h3_index)
                    # get the node id
                    if parent_h3_index in h3_index_to_node_id_map:
                        parent_node_id = h3_index_to_node_id_map[
                            parent_h3_index]
                        # get the data
                        parent_node_data = graph_data[parent_node_id, :, :]
                        parent_node_data_masks = graph_data_masks[
                            parent_node_id, :, :]
                    else:
                        # make NaNs of the appropriate shape
                        parent_node_data = np.full(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature), np.nan)
                        parent_node_data_masks = np.zeros(
                            (1, num_samples_in_node_feature,
                             num_features_in_node_feature))
                else:
                    # the parent is the root node
                    parent_node_data = graph_data[-1, :, :]
                    parent_node_data_masks = graph_data_masks[-1, :, :]
                # update the X values
                if include_masks_in_features:
                    X = np.concatenate([
                        X,
                        np.reshape(parent_node_data, (1, -1), reshape_order),
                        np.reshape(parent_node_data_masks,
                                   (1, -1), reshape_order)
                    ], axis=1)
                else:
                    X = np.concatenate([
                        X,
                        np.reshape(parent_node_data, (1, -1), reshape_order)
                    ], axis=1)
            else:
                # make NaNs of the appropriate shape
                parent_node_data = np.full(
                    (num_edges_for_each_node, num_samples_in_node_feature,
                     num_features_in_node_feature), np.nan)
                parent_node_data_masks = np.zeros(
                    (num_edges_for_each_node, num_samples_in_node_feature,
                     num_features_in_node_feature))
                # update the X values
                if include_masks_in_features:
                    X = np.concatenate([
                        X,
                        np.reshape(parent_node_data, (1, -1), reshape_order),
                        np.reshape(parent_node_data_masks,
                                   (1, -1), reshape_order)
                    ], axis=1)
                else:
                    X = np.concatenate([
                        X,
                        np.reshape(parent_node_data, (1, -1), reshape_order)
                    ], axis=1)

                if verbose: print(f"root node: X shape: {np.shape(X)}")

            if verbose:
                print(f"after obtaining parent values, X shape: {np.shape(X)}")

            if verbose:
                print(
                    f"final X shape: {np.shape(X)}, final y shape: {np.shape(y)}"
                )

            if X.shape[1] != feature_vector_shape[1]:
                # this is the case for the 12 pentagons in the graph
                # we can check that the shape is correct and pad, otherwise skip
                x_shape = X.shape
                # check that X has 2 items in the shape
                if len(x_shape) != 2:
                    if verbose:
                        print(
                            f"skipping {h3_index} (node id {node_id}) due to incorrect shape {x_shape}"
                        )
                    continue

                if include_masks_in_features and x_shape[1] + (
                        2 * num_features_in_node_feature *
                        num_samples_in_node_feature
                ) == feature_vector_shape[1]:
                    # pad with NaNs
                    # make NaNs of the appropriate shape
                    pad_node_data = np.full(
                        (num_edges_for_each_node, num_samples_in_node_feature,
                         num_features_in_node_feature), np.nan)
                    pad_node_data_masks = np.zeros(
                        (num_edges_for_each_node, num_samples_in_node_feature,
                         num_features_in_node_feature))
                    # update the X values
                    X = np.concatenate([
                        X,
                        np.reshape(pad_node_data, (1, -1), reshape_order),
                        np.reshape(pad_node_data_masks, (1, -1), reshape_order)
                    ], axis=1)
                elif include_masks_in_features is False and x_shape[1] + (
                        num_features_in_node_feature *
                        num_samples_in_node_feature
                ) == feature_vector_shape[1]:
                    X = np.concatenate(
                        [X,
                         np.reshape(pad_node_data,
                                    (1, -1), reshape_order)], axis=1)
                else:
                    if verbose:
                        print(
                            f"skipping {h3_index} (node id {node_id}) due to incorrect shape {x_shape}"
                        )
                    continue

            # update the model for this example
            X_samples.append(X)
            y_samples.append(y)
            sample_h3_indices.append(h3_index)

        # transform the samples to numpy arrays
        X_samples = np.reshape(np.array(X_samples), feature_vector_shape,
                               reshape_order)
        y_samples = np.reshape(np.array(y_samples), target_vector_shape,
                               reshape_order)
        sample_h3_indices = np.array(sample_h3_indices)

        if include_target:
            return sample_h3_indices, X_samples, y_samples
        else:
            return sample_h3_indices, X_samples
