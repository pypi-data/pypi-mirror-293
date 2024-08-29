import numpy as np
import pandas as pd


class TreeData:

    def __init__(
        self, tree_type, feature_names, target_names, data_feature, data_target
    ):
        self.feature_names = feature_names
        self.target_names = None
        if  isinstance(self.target_names,str):
            self.target_names = [target_names]
        else:
            self.target_names = target_names
        self.data_feature = self.extract_values_if_dataframe(data_feature)
        self.data_target = self.extract_values_if_dataframe(data_target)
        self.data_target = self.convert_target_strings(data_target)
        self.feature_names_size = len(feature_names)
        self.tree_type = tree_type

    def to_dict(self):
        def convert(value):
            if isinstance(
                value,
                (
                    np.int8,
                    np.int16,
                    np.int32,
                    np.int64,
                    np.uint8,
                    np.uint16,
                    np.uint32,
                    np.uint64,
                ),
            ):
                return int(value)
            if isinstance(value, (np.float16, np.float32, np.float64, np.float128)):
                return float(value)
            if isinstance(value, np.ndarray):
                return [convert(item) for item in value.tolist()]
            if isinstance(value, list):
                return [convert(item) for item in value]
            if isinstance(value, pd.Series):
                return [convert(item) for item in value.tolist()]
            if isinstance(value, dict):
                return {key: convert(val) for key, val in value.items()}

            return value

        tree_data_dict = {
            "tree_type": self.tree_type,
            "feature_names": self.feature_names,
            "target_names": convert(self.target_names),
            "data_feature": convert(self.data_feature),
            "data_target": convert(self.data_target),
        }

        return tree_data_dict

    def extract_values_if_dataframe(self, data):
        """
        Conver dataframe.
        """
        if isinstance(data, pd.DataFrame):
            return data.values
        return data
        

    def convert_target_strings(self, data_target):
        """
        convert_strings
        """
        if isinstance(data_target[0], str):
            target_map = {name: idx for idx, name in enumerate(self.target_names)}
            data_target = [target_map[val] for val in data_target]
        if all(1 <= val <= len(self.target_names) for val in data_target):
            data_target = [val - 1 for val in data_target]

        return data_target
