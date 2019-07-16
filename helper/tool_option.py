import argparse

def int_or_float(string):
    if '.' in string:
        return float(string)
    else:
        return int(string)

def parse_commandline_opts():
    parser = argparse.ArgumentParser(description="Decision Tree Tool")
    parser.add_argument("-i", "--input_csv", required=True, help="path of csv file")
    parser.add_argument("-o", "--objective_variable", required=True, help="the column name that you want to predict")
    parser.add_argument("-c", "--categolical_variable", default=None, nargs='?', help="column names that you want to use as one hot vector")
    parser.add_argument("-b", "--bins_num", default=25, type=int, help="the value of bins when plot histogram")
    parser.add_argument("--criterion", default="mse", help="the function to measure the quality of a split")
    parser.add_argument("--splitter", default="best", help="the strategy used to choose the split at each node")
    parser.add_argument("--max_depth", default=None, type=int, help="the maximum depth of the tree")
    parser.add_argument("--min_samples_split", default=2, type=int_or_float, help="the minimum number of samples required to split an internal node")
    parser.add_argument("--min_samples_leaf", default=1, type=int_or_float, help="the minimum number of samples required to be at a leaf node")
    parser.add_argument("--min_weight_fraction_leaf", default=0., type=float, help="the minimum weighted fraction of the sum total of weights (of all the input samples) required to be at a leaf node")
    parser.add_argument("--max_features", default=None, help="the number of features to consider when looking for the best split")
    parser.add_argument("--random_state", default=None, type=int, help="the seed used by the random number generator")
    parser.add_argument("--max_leaf_nodes", default=None, type=int, help="grow a tree with max_leaf_nodes in best-first fashion")
    parser.add_argument("--min_impurity_decrease", default=0, type=float, help="a node will be split if this split induces a decrease of the impurity greater than or equal to this value")
    parser.add_argument("--presort", default=False, type=bool, help="Whether to presort the data to speed up the finding of best splits in fitting")

    opts = vars(parser.parse_args())

    if opts["categolical_variable"] != None:
        opts["categolical_variable"] = opts["categolical_variable"].split(',')

    return opts