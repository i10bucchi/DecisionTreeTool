import unittest
import numpy as np
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

if __name__ == "__main__":
    unittest.main()