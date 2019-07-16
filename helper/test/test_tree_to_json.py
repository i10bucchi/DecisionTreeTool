import unittest
import numpy as np
import pandas as pd
import sys
import pathlib

# 一階層上のディレクトリからインポートするにはpathに追加する必要があるので/decision_treeまでの絶対パスを追加する
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( '/'.join(str(current_dir).split('/')[:-2]) )

from helper import tree_to_json

class TestTreeToJson(unittest.TestCase):
    def test_n_sample_div(self):
        # pattern[1]で想定している木のイメージ
        # node_id(sample_num)と表している
        #
        #         / 6(2)
        #    4(5)
        #  /      \ 5(3)
        # 0(10)      
        #  \      / 3(4)
        #    1(5)
        #         \ 2(1)
        #
        pattern = [
            {
                "description": "Function should return collectry values when it is given typical arguments.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([10, 5, 1, 4, 5, 3, 2]),
                "arg4": 1,
                "expected": [1, 4]
            },
            {
                "description": "Function should return -1 if given node do not have right child_node.",
                "arg1": np.array([1, 2, -1, 4, 5, -1]),
                "arg2": np.array([3, -1, -1, 5, -1, -1]),
                "arg3": np.array([10, 5, 5, 5, 3, 2]),
                "arg4": 1,
                "expected": [5, -1]
            },
            {
                "description": "Function should return -1 if given node do not have left child_node.",
                "arg1": np.array([1, -1, -1, 4, 5, -1]),
                "arg2": np.array([3, 2, -1, 5, -1, -1]),
                "arg3": np.array([10, 5, 5, 5, 3, 2]),
                "arg4": 1,
                "expected": [-1, 5]
            },
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.n_sample_div(p["arg1"], p["arg2"], p["arg3"], p["arg4"])

            self.assertListEqual(actual, p["expected"])

    def test_get_parent_id(self):
        # pattern[1]で想定している木のイメージ
        # node_id(sample_num)と表している
        #
        #         / 6(2)
        #    4(5)
        #  /      \ 5(3)
        # 0(10)      
        #  \      / 3(4)
        #    1(5)
        #         \ 2(1)
        #
        pattern = [
            {
                "description": "Function should return collectry values when it is given typical arguments.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": 6,
                "expected": 4
            },
            {
                "description": "Function should return None when root node is given as argument",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": 0,
                "expected": None
            },
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_parent_id(p["arg1"], p["arg2"], p["arg3"])

            self.assertEqual(actual, p["expected"])

    def test_get_leaf_by_node(self):
        # pattern[0]で想定している木のイメージ
        # node_id(sample_num)と表している
        #
        #         / 6(2)
        #    4(5)
        #  /      \ 5(3)
        # 0(10)      
        #  \      / 3(4)
        #    1(5)
        #         \ 2(1)
        #
        # pattern[1]で想定している木のイメージ
        #
        #         / 8(2)
        #    6(5)
        #  /      \ 7(3)
        # 0(10)          / 5(1)
        #  \      / 3(4)  
        #    1(5)        \ 4(3)
        #         \ 2(1)
        #
        pattern = [
            {
                "description": "Function should return collectry values when it is given typical arguments.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": 4,
                "arg4": [],
                "expected": [5, 6]
            },
            {
                "description": "Function should also return collectry values when given tree structure lacked.",
                "arg1": np.array([1, 2, -1, 4, -1, -1, 7, -1, -1]),
                "arg2": np.array([6, 3, -1, 5, -1, -1, 8, -1, -1]),
                "arg3": 1,
                "arg4": [],
                "expected": [2, 4, 5]
            }
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_leaf_by_node(p["arg1"], p["arg2"], p["arg3"], p["arg4"])

            self.assertEqual(actual, p["expected"])

    def test_get_node_mu(self):
        # pattern[0]で想定している木のイメージ
        # node_id(sample_num)と表している
        #
        #         / 6(2)
        #    4(5)
        #  /      \ 5(3)
        # 0(10)      
        #  \      / 3(4)
        #    1(5)
        #         \ 2(1)
        #
        pattern = [
            {
                "description": "Function should return collectry values when node that is leaf posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 3,
                "expected": (1 + 2 + 3 + 4) / 4
            },
            {
                "description": "Function should return collectry values when node that is node posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 4,
                "expected": (5 + 6 + 7 + 8 + 9) / 5
            },
            {
                "description": "Function should return collectry values when node that is root posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 0,
                "expected": (1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9) / 10
            },
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_node_mu(p["arg1"], p["arg2"], p["arg3"], p["arg4"], p["arg5"])

            self.assertEqual(actual, p["expected"])

    def test_get_node_sigma(self):
        # pattern[0]で想定している木のイメージ
        # node_id(sample_num)と表している
        #
        #         / 6(2)
        #    4(5)
        #  /      \ 5(3)
        # 0(10)      
        #  \      / 3(4)
        #    1(5)
        #         \ 2(1)
        #
        pattern = [
            {
                "description": "Function should return collectry values when node that is leaf posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 3,
                "expected": np.std(np.array([1, 2, 3, 4]))
            },
            {
                "description": "Function should return collectry values when node that is node posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 4,
                "expected": np.std(np.array([5, 6, 7, 8, 9]))
            },
            {
                "description": "Function should return collectry values when node that is root posision is given.",
                "arg1": np.array([1, 2, -1, -1, 5, -1, -1]),
                "arg2": np.array([4, 3, -1, -1, 6, -1, -1]),
                "arg3": np.array([2, 3, 3, 3, 3, 5, 5, 5, 6, 6]),
                "arg4": pd.Series(range(10)),
                "arg5": 0,
                "expected": np.std(np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
            },
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_node_sigma(p["arg1"], p["arg2"], p["arg3"], p["arg4"], p["arg5"])

            self.assertEqual(actual, p["expected"], p['description'])

    def test_get_left_and_right(self):
        # tree_dictで渡している木のイメージ
        # 数字はnode_idを表している
        #
        #       / 6
        #    4
        #  /    \ 5
        # 0      
        #  \    / 3
        #    1
        #       \ 2
        #
        tree_dict = [
            {
                "node_number": 0,
                "feature": "a04",
                "threshold": 2.5,
                "parent": None,
                "child_l": 1,
                "child_r": 4
            },
            {
                "node_number": 1,
                "feature": "a02",
                "threshold": 1.5,
                "parent": 0,
                "child_l": 2,
                "child_r": 3
            },
            {
                "node_number": 2,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 1,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 3,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 1,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 4,
                "feature": "a04",
                "threshold": 7.5,
                "parent": 0,
                "child_l": 5,
                "child_r": 6
            },
            {
                "node_number": 5,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 4,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 6,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 4,
                "child_l": -1,
                "child_r": -1
            },
        ]
        pattern = [
            {
                "description": "Function should return False when there is no parent of the given node.",
                "arg1": 0,
                "arg2": tree_dict,
                "expected": False
            },
            {
                "description": "Function should return False when a nonexistent node number is specified",
                "arg1": 100,
                "arg2": tree_dict,
                "expected": False
            },
            {
                "description": "Function shoud return 'LEFT' when I was the left child.",
                "arg1": 1,
                "arg2": tree_dict,
                "expected": "LEFT"
            },
            {
                "description": "Function should return 'LEFT' when I was the left child.",
                "arg1": 5,
                "arg2": tree_dict,
                "expected": "LEFT"
            },
            {
                "description": "Function should return 'LEFT' when I was the left child.",
                "arg1": 2,
                "arg2": tree_dict,
                "expected": "LEFT"
            },
            {
                "description": "Function should return 'RIGHT' when I was the right child.",
                "arg1": 4,
                "arg2": tree_dict,
                "expected": "RIGHT"
            },
            {
                "description": "Function should return 'RIGHT' when I was the right child.",
                "arg1": 3,
                "arg2": tree_dict,
                "expected": "RIGHT"
            },
            {
                "description": "Function should return 'RIGHT' when I was the right child.",
                "arg1": 6,
                "arg2": tree_dict,
                "expected": "RIGHT"
            }
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_left_and_right(p["arg1"], p["arg2"])

            self.assertEqual(actual, p["expected"], p["description"])
        
    def test_get_feat_to_root(self):
        # tree_dictで渡している木のイメージ
        # 数字はnode_idを表している
        #
        #       / 6
        #    4
        #  /    \ 5
        # 0      
        #  \    / 3
        #    1
        #       \ 2
        #
        tree_dict = [
            {
                "node_number": 0,
                "feature": "a04",
                "threshold": 2.5,
                "parent": None,
                "child_l": 1,
                "child_r": 4
            },
            {
                "node_number": 1,
                "feature": "a02",
                "threshold": 1.5,
                "parent": 0,
                "child_l": 2,
                "child_r": 3
            },
            {
                "node_number": 2,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 1,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 3,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 1,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 4,
                "feature": "a04",
                "threshold": 7.5,
                "parent": 0,
                "child_l": 5,
                "child_r": 6
            },
            {
                "node_number": 5,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 4,
                "child_l": -1,
                "child_r": -1
            },
            {
                "node_number": 6,
                "feature": "a03",
                "threshold": -2.0,
                "parent": 4,
                "child_l": -1,
                "child_r": -1
            },
        ]
        pattern = [
            {
                "description": "Function should return empty array when there is no parent of given node.",
                "arg1": 0,
                "arg2": tree_dict,
                "expected": []
            },
            {
                "description": "Function should return empty array when a nonexistent node number is specified.",
                "arg1": 100,
                "arg2": tree_dict,
                "expected": []
            },
            {
                "description": "Function should return array containing codinations and thresholds when there is parent of given node.",
                "arg1": 1,
                "arg2": tree_dict,
                "expected": [
                    {
                        "node_num":0,
                        "feature": "a04",
                        "threshold": 2.5,
                        "LorR": "LEFT"
                    }
                ]
            },
            {
                "description": "Function should return array containing codinations and thresholds when there is parent of given node.",
                "arg1": 2,
                "arg2": tree_dict,
                "expected": [
                    {
                        "node_num": 1,
                        "feature": "a02",
                        "threshold": 1.5,
                        "LorR": "LEFT"
                    },
                    {
                        "node_num": 0,
                        "feature": "a04",
                        "threshold": 2.5,
                        "LorR": "LEFT"
                    }
                ]
            },
            {
                "description": "Function should return array containing codinations and thresholds when there is parent of given node.",
                "arg1": 6,
                "arg2": tree_dict,
                "expected": [
                    {
                        "node_num": 4,
                        "feature": "a04",
                        "threshold": 7.5,
                        "LorR": "RIGHT"
                    },
                    {
                        "node_num": 0,
                        "feature": "a04",
                        "threshold": 2.5,
                        "LorR": "RIGHT"
                    }
                ]
            }
        ]
        for i, p in enumerate(pattern):
            actual = tree_to_json.get_feat_to_root(p["arg1"], p["arg2"])

            self.assertEqual(actual, p["expected"], p["description"])
    
    def test_get_describe(self):
        pattern = [
            {
                "description": "Function should return empty dictionary when pd.Series is not given.",
                "arg1": 0,
                "expected":{}
            },
            {
                "description": "Function should return pd.Series when pd.Series is given.",
                "arg1": pd.Series(range(10)),
                "expected": {
                    "count": 10.0,
                    "mean": 4.5,
                    "std": 3.03,
                    "min": 0.0,
                    "max": 9.0,
                    "25%": 2.25,
                    "50%": 4.5,
                    "75%": 6.75
                }
            },
            {
                "description": "Function should return pd.Series when pd.Series is geven.",
                "arg1": pd.Series(range(20)),
                "expected": {
                    "count": 20.0,
                    "mean": 9.5,
                    "std": 5.92,
                    "min": 0.0,
                    "max": 19.0,
                    "25%": 4.75,
                    "50%": 9.5,
                    "75%": 14.25
                }
            }
        ]

        for i, p in enumerate(pattern):
            actual = tree_to_json.get_describe(p["arg1"])

            self.assertEqual(actual, p["expected"], p["description"])




if __name__ == "__main__":
    unittest.main()