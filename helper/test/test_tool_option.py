import unittest
import sys
import os
import pathlib

# 一階層上のディレクトリからインポートするにはpathに追加する必要があるので/decision_treeまでの絶対パスを追加する
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( '/'.join(str(current_dir).split('/')[:-2]) )

# コマンドライン引数を擬似的に与えるために必要
sys.path.append(os.getcwd())

from helper import tool_option

class TestToolOption(unittest.TestCase):
    def test_parse_commandline_opts(self):
        assert_pattern = [
            {
                "description": "Function should return default value when non-requirement options are not given.",
                "cmd_args": "-i ../abc/def.csv -o obj_var".split(" "),
                "expected": {
                    "input_csv": "../abc/def.csv",
                    "objective_variable": "obj_var",
                    "categolical_variable": None,
                    "bins_num": 25,
                    "criterion": "mse",
                    "splitter": "best",
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "min_weight_fraction_leaf": 0,
                    "max_features": None,
                    "random_state": None,
                    "max_leaf_nodes": None,
                    "min_impurity_decrease": 0,
                    "presort": False
                }
            },
            {
                "description": "Function should return value that options are reflected when options are given.",
                "cmd_args": "-i ../abc/def.csv -o obj_var -b 11 --criterion aaa --splitter bbb --max_depth 22 --min_samples_split 33 --min_samples_leaf 44 --min_weight_fraction_leaf 55 --max_features 66 --random_state 77 --max_leaf_nodes 88 --min_impurity_decrease 99 --presort True".split(" "),
                "expected": {
                    "input_csv": "../abc/def.csv",
                    "objective_variable": "obj_var",
                    "categolical_variable": None,
                    "bins_num": 11,
                    "criterion": "aaa",
                    "splitter": "bbb",
                    "max_depth": 22,
                    "min_samples_split": 33,
                    "min_samples_leaf": 44,
                    "min_weight_fraction_leaf": 55,
                    "max_features": "66",
                    "random_state": 77,
                    "max_leaf_nodes": 88,
                    "min_impurity_decrease": 99,
                    "presort": True
                }
            },
            {
                "description": "Categolical_variable is returned type list when categolical_variable are given from commandline.",
                "cmd_args": "-i ../abc/def.csv -o obj_var -c c1,c2".split(" "),
                "expected": {
                    "input_csv": "../abc/def.csv",
                    "objective_variable": "obj_var",
                    "categolical_variable": ["c1", "c2"],
                    "bins_num": 25,
                    "criterion": "mse",
                    "splitter": "best",
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "min_weight_fraction_leaf": 0,
                    "max_features": None,
                    "random_state": None,
                    "max_leaf_nodes": None,
                    "min_impurity_decrease": 0,
                    "presort": False
                }
            },
        ]
        exit_pattern = [
            {
                "description": "Program should exit when requirement options are not given.",
                "cmd_args": "-i ../abc/def.csv".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when requirement options are not given",
                "cmd_args": "-o obj_var".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when max_depth options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --max_depth abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when max_depth options are given as type float",
                "cmd_args": "-i ../abc/def.csv -o obj_var --max_depth 1.1".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when min_samples_split options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --min_samples_split abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when min_samples_leaf options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --min_samples_leaf abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when min_weight_fraction_leaf options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --min_samples_leaf abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when random_state options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --random_state abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when max_leaf_nodes options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --max_leaf_nodes abcde".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when max_leaf_nodes options are given as type float",
                "cmd_args": "-i ../abc/def.csv -o obj_var --max_leaf_nodes 1.1".split(" "),
                "expected": 2
            },
            {
                "description": "Program should exit when min_impurity_decrease options are given as type string",
                "cmd_args": "-i ../abc/def.csv -o obj_var --min_impurity_decrease abcde".split(" "),
                "expected": 2
            },
        ]

        for i, p in enumerate(assert_pattern):
            for arg in p["cmd_args"]:
                sys.argv.append(arg)
            
            actual = tool_option.parse_commandline_opts()

            for (k,v) in actual.items():
                print(k, v)
                self.assertTrue( (k, v) in p["expected"].items(), str((k, v)) + str(p['expected'].items()))
        
            del sys.argv[1:]

        for i, p in enumerate(exit_pattern):
            for arg in p["cmd_args"]:
                sys.argv.append(arg)

            try:
                actual = tool_option.parse_commandline_opts()
            except SystemExit as e:
                self.assertEqual(e.code, p["expected"])
            else:
                self.fail(p["description"])
    
            del sys.argv[1:]

if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main()