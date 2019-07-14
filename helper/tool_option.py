import sys
import getopt

def usage():
    print("Decision Tree Tool")
    print("")
    print("Usage: python3 tree.py -i ./user_scan.csv -o scan_num -c a02,a04 -d 7 > result.html")
    print("-i --input_csv                       - path of csv file")
    print("-o --objective_variable              - the column name that you want to predict")
    print("-c --categolical_variable            - column names that you want to use as one hot vector")
    print("-d --depth                           - the depth as tree parameter. default is 5.")
    print("-b --num_of_bins                     - the value of bins when plot histogram")
    sys.exit(0)

def get_command_opts(c_args):
    # パラメータが指定されていない場合は使い方を表示
    if not len(c_args):
        usage()

    # Decision Tree Tool Option
    tool_opts_dict = {
        "csv_path": None,
        "obj_var": None,
        "dummy_vars": None,
        "num_of_bins": 25,
    }
    # sklearn.tree.DesisionTreeRegressor Options
    skltree_opts_dict = {
        "criterion": "mse",
        "splitter": "best",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.,
        "max_features": None,
        "random_state": None,
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.,
        "presort": False
    }
    
    # パラメータ定義
    try:
        opts, args = getopt.getopt(
            c_args,
            "hi:o:c:b:",
            [
                # Decision Tree Tool Options
                "help",
                "input_csv=",
                "objective_variable=",
                "categolical_variable=",
                "bins_num="
                # sklearn.tree.DesisionTreeRegressor Options
                "criterion=",
                "splitter=",
                "max_depth=",
                "min_samples_split=",
                "min_samples_leaf=",
                "min_weight_fraction_leaf=",
                "max_features=",
                "random_state=",
                "max_leaf_nodes=",
                "min_impurity_decrease=",
                "presort="
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    # 各パラメータの値を取得
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input_csv"): 
            tool_opts_dict["csv_path"] = a
        elif o in ("-o", "--objective_variable"):
            tool_opts_dict["obj_var"] = a
        elif o in ("-c", "--categolical_variable"):
            tool_opts_dict["dummy_vars"] = a.split(',')
        elif o in ("-b", "--bins_num"):
            tool_opts_dict["num_of_bins"] = int(a)
        elif o in ("--criterion"):
            skltree_opts_dict["criterion"] = a
        elif o in ("--splitter"):
            skltree_opts_dict["splitter"] = a
        elif o in ("--max_depth"):
            skltree_opts_dict["max_depth"] = int(a)
        elif o in ("--min_samples_split"):
            skltree_opts_dict["min_samples_split"] = int(a)
        elif o in ("--min_samples_leaf"):
            skltree_opts_dict["min_samples_leaf"] = int(a) # floatも取り得る
        elif o in ("--min_weight_fraction_leaf"):
            skltree_opts_dict["min_weight_fraction_leaf"] = float(a)
        elif o in ("--max_features"):
            skltree_opts_dict["max_features"] = a # int, float, stringを取り得る
        elif o in ("--random_state"):
            skltree_opts_dict["random_state"] = int(a)
        elif o in ("--max_leaf_nodes"):
            skltree_opts_dict["max_leaf_nodes"] = int(a)
        elif o in ("--min_impurity_decrease"):
            skltree_opts_dict["min_impurity_decrease"] = float(a)
        elif o in ("--presort"):
            skltree_opts_dict["presort"] = bool(a)
        else:
            assert False, "Unhandled Option"
    
    # 最低限のパラメータが指定されていない場合は使い方を表示
    if (tool_opts_dict["csv_path"] == None) or (tool_opts_dict["obj_var"] == None):
        print("Error: -i and -o are specified always.")
        usage()
    
    return tool_opts_dict, skltree_opts_dict