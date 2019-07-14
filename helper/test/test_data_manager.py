import unittest
import pandas as pd
import numpy as np
import sys
import pathlib

# 一階層上のディレクトリからインポートするにはpathに追加する必要があるので/decision_treeまでの絶対パスを追加する
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( '/'.join(str(current_dir).split('/')[:-2]) )

from helper import data_manager

class TestDataManager(unittest.TestCase):
    def test_get_data(self):
        arg1 = "./test.csv"
        arg2 = "obj_var"
        categorical_samples_string = ["a", "b", "c", "d", "e", "f", "g", "h", "i", np.nan]
        pattern = [
            {
                "description": "Funciton should convert to dummy variable including nan automatically if arg3 is None.",
                "arg3": None,
                "csv": pd.DataFrame(
                    {
                        "obj_var": range(10),
                        "f1": range(10),
                        "f2": categorical_samples_string
                    },
                    index=range(10)
                ),
                "expected": {
                    "ret1": {
                        "columns": ["f1", "f2_a", "f2_b", "f2_c", "f2_d", "f2_e", "f2_f", "f2_g", "f2_h", "f2_i", "f2_nan"],
                        "values": [
                            [i for i in range(2, 10)],
                            [0 for i in range(2, 10)],
                            [0 for i in range(2, 10)],
                            [0 if i != 2 else 1 for i in range(2, 10)],
                            [0 if i != 3 else 1 for i in range(2, 10)],
                            [0 if i != 4 else 1 for i in range(2, 10)],
                            [0 if i != 5 else 1 for i in range(2, 10)],
                            [0 if i != 6 else 1 for i in range(2, 10)],
                            [0 if i != 7 else 1 for i in range(2, 10)],
                            [0 if i != 8 else 1 for i in range(2, 10)],
                            [0 if i != 9 else 1 for i in range(2, 10)]
                        ]
                    },
                    "ret2": {
                        "values": [i for i in range(2, 10)]
                    },
                    "ret3": {
                        "columns": ["f1", "f2_a", "f2_b", "f2_c", "f2_d", "f2_e", "f2_f", "f2_g", "f2_h", "f2_i", "f2_nan"],
                        "values": [
                            [i for i in range(0, 2)],
                            [0 if i != 0 else 1 for i in range(0, 2)],
                            [0 if i != 1 else 1 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)]
                        ]
                    },
                    "ret4": {
                        "values": [i for i in range(0, 2)]
                    }
                },
            },
            {
                "description": "Funciton should convert to dummy variable including nan accoding to dummy_vars if arg3 is given.",
                "arg3": ["f1", "f2"],
                "csv": pd.DataFrame(
                    {
                        "obj_var": range(10),
                        "f1": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        "f2": categorical_samples_string
                    },
                    index=range(10)
                ),
                "expected": {
                    "ret1": {
                        "columns": ["f1_0.0", "f1_1.0", "f1_nan", "f2_a", "f2_b", "f2_c", "f2_d", "f2_e", "f2_f", "f2_g", "f2_h", "f2_i", "f2_nan"],
                        "values": [
                            [1, 1, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0 for i in range(2, 10)],
                            [0 for i in range(2, 10)],
                            [0 if i != 2 else 1 for i in range(2, 10)],
                            [0 if i != 3 else 1 for i in range(2, 10)],
                            [0 if i != 4 else 1 for i in range(2, 10)],
                            [0 if i != 5 else 1 for i in range(2, 10)],
                            [0 if i != 6 else 1 for i in range(2, 10)],
                            [0 if i != 7 else 1 for i in range(2, 10)],
                            [0 if i != 8 else 1 for i in range(2, 10)],
                            [0 if i != 9 else 1 for i in range(2, 10)]
                        ]
                    },
                    "ret2": {
                        "values": [i for i in range(2, 10)]
                    },
                    "ret3": {
                        "columns": ["f1_0.0", "f1_1.0", "f1_nan", "f2_a", "f2_b", "f2_c", "f2_d", "f2_e", "f2_f", "f2_g", "f2_h", "f2_i", "f2_nan"],
                        "values": [
                            [1, 1],
                            [0, 0],
                            [0, 0],
                            [0 if i != 0 else 1 for i in range(0, 2)],
                            [0 if i != 1 else 1 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)],
                            [0 for i in range(0, 2)]
                        ]
                    },
                    "ret4": {
                        "values": [i for i in range(0, 2)]
                    }
                },
            },
            {
                "description": "Funciton should convert from nan to -1 automatically if variable is included nan.",
                "arg3": None,
                "csv": pd.DataFrame(
                    {
                        "obj_var": range(10),
                        "f1": [np.nan for i in range(10)],
                        "f2": [np.nan for i in range(10)]
                    },
                    index=range(10)
                ),
                "expected": {
                    "ret1": {
                        "columns": ["f1", "f2"],
                        "values": [
                            [-1 for i in range(2, 10)],
                            [-1 for i in range(2, 10)]
                        ]
                    },
                    "ret2": {
                        "values": [i for i in range(2, 10)]
                    },
                    "ret3": {
                        "columns": ["f1", "f2"],
                        "values": [
                            [-1 for i in range(0, 2)],
                            [-1 for i in range(0, 2)]
                        ]
                    },
                    "ret4": {
                        "values": [i for i in range(0, 2)]
                    }
                },
            },
        ]

        for i, p in enumerate(pattern):
            p["csv"].to_csv(arg1)
            ret_act1, ret_act2, ret_act3, ret_act4 = data_manager.get_data(arg1, arg2, p["arg3"])
            
            self.assertListEqual(ret_act1.columns.tolist(), p["expected"]["ret1"]["columns"])
            self.assertListEqual(ret_act1.values.T.tolist(), p["expected"]["ret1"]["values"])
            self.assertListEqual(ret_act2.values.tolist(), p["expected"]["ret2"]["values"])
            self.assertListEqual(ret_act3.columns.tolist(), p["expected"]["ret3"]["columns"])
            self.assertListEqual(ret_act3.values.T.tolist(), p["expected"]["ret3"]["values"])
            self.assertListEqual(ret_act4.values.tolist(), p["expected"]["ret4"]["values"])

if __name__ == "__main__":
    unittest.main()