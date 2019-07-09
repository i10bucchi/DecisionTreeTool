import json
import getopt
import sys
import os
import numpy as np
import pandas as pd
from sklearn import tree
import subprocess

# ----- ヒストグラムのデータを取得する自作メソッド ----- #
from make_histdata import get_histdata

def usage():
    print("Decision Tree Tool")
    print("")
    print("Usage: python3 tree.py -i ./user_scan.csv -o scan_num -c a02,a04 -d 7 > result.html")
    print("-i --input_csv                       - path of csv file")
    print("-o --objective_variable              - the column name that you want to predict")
    print("-c --categolical_variable            - column names that you want to use as one hot vector")
    print("-d --depth                           - the depth as tree parameter. default is 5.")
    sys.exit(0)

def tree_dump(clf, obj_var, x, y):
    '''
    abst:
        学習した決定木の構造をJsonで出力
    input:
        clf: scikit-learnの決定木の構造
        obj_var: 
        x: 学習データ(特徴量)
        y: 学習データ(目的変数)
    output:
        
    '''
    def n_sample_div(node):
        '''
        abst:
            引数で与えられたノード内のデータをそのノード条件で分割した時のデータ数を返す
        input:
            node: ノードインデックス
        output:
            [左子ノードのデータ数, 右子ノードのデータ数]
        '''
        if child_l_list[node] == -1:
            n_sample_l = -1
        else:
            n_sample_l = n_sample_list[child_l_list[node]]
        if child_r_list[node] == -1:
            n_sample_r = -1
        else:
            n_sample_r = n_sample_list[child_r_list[node]]

        return [int(n_sample_l), int(n_sample_r)]
    
    def get_parent_id(node):
        '''
        abst: 
            引数で与えられたノードの親ノードのインデックスを取得
            親なし(ルート)の場合はNoneを返す
        input:
            node: ノードインデックス
        output:
            親ノードのインデックス
        '''
        p = np.where(child_l_list == node)
        if p[0].size == 0:
            p = np.where(child_r_list == node)
        
        if p[0].size == 0:
            return None
        else:
            return int(p[0])
    
    def get_leaf_by_node(node, leafs):
        '''
        abst:
            引数で与えられたノードに属する葉のインデックスを取得
        input:
            node: ノードインデックス
            leafs: nodeに属する葉部分のノードインデックス
        output:
            leafs: nodeに属する葉部分のノードインデックス
        '''
        if child_l_list[node] != -1:
            leafs = get_leaf_by_node(child_l_list[node], leafs)
        else:
            leafs.append(node)
            return leafs

        if child_r_list[node] != -1:
            leafs = get_leaf_by_node(child_r_list[node], leafs)
        else:
            leafs.append(node)
            return leafs
        
        return leafs
    
    def get_node_mu(node):
        '''
        abst:
            引数で与えられたノードに属するデータの平均値を取得
        input:
            node: ノードインデックス
        output:
            平均値
        '''
        target_leafs = []
        target_leafs = get_leaf_by_node(node, target_leafs)
        data_indexes = np.array([])
        for leaf in target_leafs:
            data_indexes = np.append(data_indexes, np.where(reaching_leafs == leaf))
        
        return y[data_indexes].mean()
    
    def get_node_sigma(node):
        '''
        abst:
            引数で与えられたノードに属するデータの平均値を取得
        input:
            node: ノードインデックス
        output:
            分散値
        '''
        target_leafs = get_leaf_by_node(node, [])
        data_indexes = np.array([])
        for leaf in target_leafs:
            data_indexes = np.append(data_indexes, np.where(reaching_leafs == leaf))
        
        return y[data_indexes].std(ddof=0)
    
    # 木の構造取得
    feature_list = clf.tree_.feature
    threshold_list = clf.tree_.threshold
    n_sample_list = clf.tree_.n_node_samples
    child_l_list = clf.tree_.children_left
    child_r_list = clf.tree_.children_right
    values_list = clf.tree_.value
    reaching_leafs = clf.tree_.apply(x.values.astype(np.float32))
    
    y = y.reset_index()[obj_var]

    # 辞書化
    n_node = clf.tree_.node_count
    tree_structure_dict = [
        {
            'node_number':int(node),
            'feature':x.columns[feature_list[node]],
            'threshold':float(threshold_list[node]),
            'parent':get_parent_id(node),
            'child_l':int(child_l_list[node]),
            'child_r':int(child_r_list[node]),
            'n_sample':int(n_sample_list[node]),
            'n_sample_div':n_sample_div(node),
            'mu': get_node_mu(node),
            'sigma': get_node_sigma(node)
        }
        for node in range(n_node)
    ]
    # --- ヒストグラムを描画するためのデータを取得してjsonに追記するメソッド --- #
    get_histdata(tree_structure_dict, x, y, obj_var)

    f = open("./data/tree_structure.json", "w")
    json.dump(tree_structure_dict, f, indent=4, allow_nan=True)
    f.close()

def get_data(csv_path, obj_var, dummy_vars):
    '''
    abst:
        決定木分析のためのデータ取得とデータ整形
        データ整形
        - dummy_varsで指定されたカラムをOneHot化
        - nanを-1で埋める
        - 説明変数と目的変数に分割
        - 学習データとテストデータに分割
    input:
        csv_path: 対象データであるcsvファイルへのパス
        obj_var: 目的変数名
        dummy_vars: OneHot化する説明変数名のリスト
    output:
        x: 学習データ説明変数
        y: 学習データ目的変数
        X: テストデータ説明変数
        Y: テストデータ目的変数
    '''
    # データのロード
    df = pd.read_csv(csv_path, index_col=0)
    # データ整形
    if dummy_vars != None:
        df = pd.get_dummies(df, dummy_na=True, columns=dummy_vars)
    else:
        df = pd.get_dummies(df, dummy_na=True)
    
    df = df.fillna(-1)

    # 学習データとテストデータに分ける
    ldf = int(len(df.index) * 0.1)
    df_train = df[ldf+1:]
    df_test = df[:ldf]

    # 説明変数と目的変数へ分割
    x = df_train.drop(obj_var, axis=1)
    y = df_train[obj_var]
    X = df_test.drop(obj_var, axis=1)
    Y = df_test[obj_var]

    # 表示
    return x, y, X, Y

def tree_calc(x, y, X, Y, opts):
    '''
    abst:
        決定木分析を行う
    input:
        x: 学習データ説明変数
        y: 学習データ目的変数
        X: テストデータ説明変数
        Y: テストデータ目的変数
        opts: sklearnの決定木に対するオプション
    output:
        clf: scikit-learnの決定木の構造
    '''

    clf = tree.DecisionTreeRegressor(
        criterion=opts["criterion"],
        splitter=opts["splitter"],
        max_depth=opts["max_depth"],
        min_samples_split=opts["min_samples_split"],
        min_samples_leaf=opts["min_samples_leaf"],
        min_weight_fraction_leaf=opts["min_weight_fraction_leaf"],
        max_features=opts["max_features"],
        random_state=opts["random_state"],
        max_leaf_nodes=opts["max_leaf_nodes"],
        min_impurity_decrease=opts["min_impurity_decrease"],
        min_impurity_split=opts["min_impurity_split"],
        presort=opts["presort"]
    )
    clf = clf.fit(x, y)
    y_ = clf.predict(x)
    y_pred = clf.predict(X)

    # print("Result:")
    # print('\t train: LSM={:>10.2f}'.format(((y_ - y) * (y_ - y)).sum() / len(y) / 2))
    # print('\t test:  LSM={:>10.2f}'.format(((y_pred - Y) * (y_pred - Y)).sum() / len(Y) / 2))

    return clf

def get_html():
    '''
    abst:
        分析結果を表示するHTMLを作成
    input:
    output:
        html: 分析結果を表示するhtml
    '''
    f = open(JSON_PATH, "r")
    json = f.read()
    f.close()
    f = open(CSS_PATH, "r")
    style = f.read()
    f.close()
    f = open(TREE_JS_PATH, "r")
    tree_plot_js = f.read()
    f.close()
    f = open(FIT_JS_PATH, "r")
    poisson_js = f.read()
    f.close()
    f = open(HIST_JS_PATH, "r")
    histogram_plot_js = f.read()
    f.close()

    html = '<!DOCTYPE html>\n'
    html += '<head>\n'
    html += '    <meta charset="utf-8">\n'
    html += '    <script src="http://d3js.org/d3.v4.min.js"></script>\n'
    html += '    <script src="https://cdn.jsdelivr.net/jstat/latest/jstat.min.js"></script>\n'
    html += '    <!-- <link rel="stylesheet" type="text/css" href="d3_4.css"> -->\n'
    html += '    <style>{}</style>'.format(style)
    html += '</head>\n'
    html += '\n'
    html += '<body>\n'
    html += '    <!-- ポップアップを配置させて、隠しておく -->\n'
    html += '    <div class="popup" id="js-popup">\n'
    html += '            <div class="popup-inner" id="popup-inner">\n'
    html += '                <div class="close-btn" id="js-close-btn"></div>\n'
    html += '            </div>\n'
    html += '            <div class="black-background" id="js-black-bg"></div>\n'
    html += '    </div>\n'
    html += '    <!-- bin数設定のスライダーの描画 -->\n'
    html += '    <input id="bin_num" type="range" min="0" max="100" value="25" step="1" onmousemove="OnChangeValue();">\n'
    html += '    bin_num: <span id="bin_num_text">25</span>\n'
    html += '    <!-- jsファイルの読み込み -->\n'
    html += '    <script>var jsonData = {}</script>'.format(json)
    html += '    <script>{}</script>\n'.format(tree_plot_js)
    html += '    <script>{}</script>\n'.format(poisson_js)
    html += '    <script>{}</script>\n'.format(histogram_plot_js)
    html += '</body>\n'
    
    return html

def main():
    # Decision Tree Tool Option
    tool_opts_dict = {
        "csv_path": None,
        "obj_var": None,
        "dummy_vars": None,
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
        "min_impurity_split": 1e-7,
        "presort": False
    }

    # パラメータが指定されていない場合は使い方を表示
    if not len(sys.argv[1:]):
        usage()
    
    # パラメータ定義
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:o:c:",
            [
                # Decision Tree Tool Options
                "help",
                "input_csv=",
                "objective_variable=",
                "dategolical_variable=",
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
                "min_impurity_split=",
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
        elif o in ("--min_impurity_split"):
            skltree_opts_dict["min_impurity_split"] = float(a)
        elif o in ("--presort"):
            skltree_opts_dict["presort"] = bool(a)
        else:
            assert False, "Unhandled Option"
    
    # 最低限のパラメータが指定されていない場合は使い方を表示
    if (tool_opts_dict["csv_path"] == None) or (tool_opts_dict["obj_var"] == None):
        print("Error: -i and -o are specified always.")
        usage()

    # データ整形して決定木分析
    x, y, X, Y = get_data(tool_opts_dict["csv_path"], tool_opts_dict["obj_var"], tool_opts_dict["dummy_vars"])
    clf = tree_calc(x, y, X, Y, skltree_opts_dict)
    tree_dump(clf, tool_opts_dict["obj_var"], x, y)
    html = get_html()
    print(html)

CSS_PATH        = './style.css'
JSON_PATH       = './data/tree_structure.json'
TREE_JS_PATH    = './tree.js'
HIST_JS_PATH    = './histgram.js'
FIT_JS_PATH     = './cov_fit.js'

main()