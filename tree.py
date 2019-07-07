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
    get_histdata(tree_structure_dict)

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

    # user_id 列がfloatに変換できないというエラーが出た
    # 応急処置としてuser_id列を削除している
    x = x.drop(columns=["user_id"])
    X = X.drop(columns=["user_id"])


    # 表示
    return x, y, X, Y

def tree_calc(x, y, X, Y, depth):
    '''
    abst:
        決定木分析を行う
    input:
        x: 学習データ説明変数
        y: 学習データ目的変数
        X: テストデータ説明変数
        Y: テストデータ目的変数
        depth: 決定木の深さ
    output:
        clf: scikit-learnの決定木の構造
    '''

    clf = tree.DecisionTreeRegressor(random_state=0, max_depth=depth)
    clf = clf.fit(x, y)
    y_ = clf.predict(x)
    y_pred = clf.predict(X)

    # print("Result:")
    # print('\t train: LSM={:>10.2f}'.format(((y_ - y) * (y_ - y)).sum() / len(y) / 2))
    # print('\t test:  LSM={:>10.2f}'.format(((y_pred - Y) * (y_pred - Y)).sum() / len(Y) / 2))

    return clf

def make_html():
    '''
    abst:
        分析結果を表示するHTMLをプリント
    input:
    output:
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

    print('<!DOCTYPE html>')
    print('<head>')
    print('    <meta charset="utf-8">')
    print('    <script src="http://d3js.org/d3.v4.min.js"></script>')
    print('    <script src="https://cdn.jsdelivr.net/jstat/latest/jstat.min.js"></script>')
    print('    <!-- <link rel="stylesheet" type="text/css" href="d3_4.css"> -->')
    print('    <style>{}</style>'.format(style))
    print('</head>')
    print('')
    print('<body>')
    print('    <!-- ポップアップを配置させて、隠しておく -->')
    print('    <div class="popup" id="js-popup">')
    print('            <div class="popup-inner" id="popup-inner">')
    print('                <div class="close-btn" id="js-close-btn"></div>')
    print('            </div>')
    print('            <div class="black-background" id="js-black-bg"></div>')
    print('    </div>')
    print('    <!-- bin数設定のスライダーの描画 -->')
    print('    <input id="bin_num" type="range" min="0" max="100" value="25" step="1" onmousemove="OnChangeValue();">')
    print('    bin_num: <span id="bin_num_text">25</span>')
    print('    <!-- jsファイルの読み込み -->')
    print('    <script>var jsonData = {}</script>'.format(json))
    print('    <script>{}</script>'.format(tree_plot_js))
    print('    <script>{}</script>'.format(poisson_js))
    print('    <script>{}</script>'.format(histogram_plot_js))
    print('</body>')

def main():
    csv_path = None
    obj_var = None
    dummy_vars = None
    depth = 5

    # パラメータが指定されていない場合は使い方を表示
    if not len(sys.argv[1:]):
        usage()
    
    # パラメータ定義
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:o:c:d:",
            ["help", "input_csv=", "objective_variable=", "dategolical_variable=", "depth="],
        )
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    # 各パラメータの値を取得
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input_csv"): 
            csv_path = a
        elif o in ("-o", "--objective_variable"):
            obj_var = a
        elif o in ("-c", "--categolical_variable"):
            dummy_vars = a.split(',')
        elif o in ("-d", "--depth"):
            depth = int(a)
        else:
            assert False, "Unhandled Option"
    
    # 最低限のパラメータが指定されていない場合は使い方を表示
    if (csv_path == None) or (obj_var == None):
        print("Error: -i and -o are specified always.")
        usage()

    # データ整形して決定木分析
    x, y, X, Y = get_data(csv_path, obj_var, dummy_vars)
    clf = tree_calc(x, y, X, Y, depth)
    tree_dump(clf, obj_var, x, y)
    make_html()


CSS_PATH        = './style.css'
JSON_PATH       = './data/tree_structure.json'
TREE_JS_PATH    = './tree.js'
HIST_JS_PATH    = './histgram.js'
FIT_JS_PATH     = './cov_fit.js'

main()