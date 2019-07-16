import numpy as np
import pandas as pd
import json

def n_sample_div(child_l_list, child_r_list, n_sample_list, node):
    '''
    abst:
        引数で与えられたノード内のデータをそのノード条件で分割した時のデータ数を返す
    input:
        child_l_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には左子ノードのノードidが入っている
        child_r_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には右子ノードのノードidが入っている
        n_sample_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中にはノードのサンプル数が入っている
        node (int): ノードインデックス
    output:
        [左子ノードのデータ数 (int), 右子ノードのデータ数 (int)]
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

def get_parent_id(child_l_list, child_r_list, node):
    '''
    abst: 
        引数で与えられたノードの親ノードのインデックスを取得
        親なし(ルート)の場合はNoneを返す
    input:
        child_l_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には左子ノードのノードidが入っている
        child_r_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には右子ノードのノードidが入っている
        node (int): ノードインデックス
    output:
        親ノードのインデックス (int)
    '''
    p = np.where(child_l_list == node)
    if p[0].size == 0:
        p = np.where(child_r_list == node)
    
    if p[0].size == 0:
        return None
    else:
        return int(p[0])

def get_leaf_by_node(child_l_list, child_r_list, node, leafs):
    '''
    abst:
        引数で与えられたノードに属する葉のインデックスを取得
    input:
        child_l_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には左子ノードのノードidが入っている
        child_r_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には右子ノードのノードidが入っている
        node (int): ノードインデックス
        leafs (list): nodeに属する葉部分のノードインデックス
    output:
        leafs (list): nodeに属する葉部分のノードインデックス
    '''
    if child_l_list[node] != -1:
        leafs = get_leaf_by_node(child_l_list, child_r_list, child_l_list[node], leafs)
    else:
        leafs.append(node)
        return leafs

    if child_r_list[node] != -1:
        leafs = get_leaf_by_node(child_l_list, child_r_list, child_r_list[node], leafs)
    else:
        leafs.append(node)
        return leafs
    
    return leafs

def get_node_mu(child_l_list, child_r_list, reaching_leafs, y, node):
    '''
    abst:
        引数で与えられたノードに属するデータの平均値を取得
    input:
        child_l_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には左子ノードのノードidが入っている
        child_r_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には右子ノードのノードidが入っている
        reaching_leaf (numpy.array): データが到達したノードid
        y (pandas.Series): 学習データ目的変数
        node (int): ノードインデックス
    output:
        平均値 (float)
    '''
    target_leafs = get_leaf_by_node(child_l_list, child_r_list, node, [])
    data_indexes = np.array([])
    for leaf in target_leafs:
        data_indexes = np.append(data_indexes, np.where(reaching_leafs == leaf))
    
    return y[data_indexes].mean()

def get_node_sigma(child_l_list, child_r_list, reaching_leafs, y, node):
    '''
    abst:
        引数で与えられたノードに属するデータの平均値を取得
    input:
        child_l_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には左子ノードのノードidが入っている
        child_r_list (numpy.array): 要素番号がノードidとなっており, 対応する要素番号の中には右子ノードのノードidが入っている
        reaching_leaf (numpy.array): データが到達した葉のノードid
        y (pandas.Series): 学習データ目的変数
        node (int): ノードインデックス
    output:
        分散値 (float)
    '''
    target_leafs = get_leaf_by_node(child_l_list, child_r_list, node, [])
    data_indexes = np.array([])
    for leaf in target_leafs:
        data_indexes = np.append(data_indexes, np.where(reaching_leafs == leaf))
    
    return y[data_indexes].std(ddof=0)

def get_histdata(tree_structure_dict, x, y, obj_var, num_bins):

    """
    abst:
        ヒストグラムを描画するためのデータを出力
    input:
        tree_structure_dict: 決定木の構造が格納された辞書のリストが格納された変数
    output:
    """
    def get_left_and_right(node_number):
        """
        abst:  
            与えられたnode_numberの親を見に行き、
            node_numberの位置が兄弟ノードと比較して右か左かを返すメソッド
        input:
            node_number: 位置を知りたいノードの番号
        output:
            False: 親がいなかった場合
            "LEFT": 左だった場合
            "RIGHT": 右だった場合    
        """
        if (tree_structure_dict[node_number]["parent"] == None):
            return False

        parent_num = tree_structure_dict[node_number]["parent"]
        parent_left_child = tree_structure_dict[parent_num]["child_l"]
        parent_right_child = tree_structure_dict[parent_num]["child_r"]
        
        if (node_number == parent_left_child):
            return "LEFT"
        elif (node_number == parent_right_child):
            return "RIGHT"

        return False

    def get_feat_to_root(node_number):
        """
        abst:
            与えられたnode_numberからrootまでの特徴と条件を返す関数
            ##### 再帰的なメソッドです ######
        input:
            node_number: ノードの番号
        output:
            []: node_numberの親がいないとき
            辞書のリスト: それ以外
        """
        if (tree_structure_dict[node_number]["parent"] == None):
            return []

        # 辞書のリストを返す
        return [
            {
                "node_num": tree_structure_dict[node_number]["parent"],
                "feature": tree_structure_dict[tree_structure_dict[node_number]["parent"]]["feature"],
                "threshold": tree_structure_dict[tree_structure_dict[node_number]["parent"]]["threshold"],
                "LorR": get_left_and_right(node_number)
            }
        ] + get_feat_to_root(tree_structure_dict[node_number]["parent"])
    
    def replace_outlier(series, bias=1.5):
        """
        abst:
            外れ値(最大値)を除くメソッド
        input:
            series: 各データの目的変数の値が格納されたpandas.Series
        outpu:
            replaced_series: 外れ値が取り除かれたSeries
        """
        # seriesのデータ数が5未満の場合は外れ値を取り除いてしまうとデータ数が少なくなりすぎてしまうため
        # 外れ値を除く処理を行わない
        if (series.shape[0] < 5):
            return series

        # 四分位数
        q1 = series.quantile(.25)
        q3 = series.quantile(.75)
        iqr = q3 - q1
        # 外れ値の基準点
        min_outlier = q1 - (iqr * bias)
        max_outlier = q3 + (iqr * bias)
        
        # 外れ値の除去
        replaced_series = series[(min_outlier <= series) & (series <= max_outlier)]
        outlier = series[~((min_outlier <= series) & (series <= max_outlier))]
        
        return replaced_series, outlier

    def get_describe(series):
        """
        abst:
            シリーズの基本統計量を返す関数
        input:
            series: pandasシリーズ
        output:
            シリーズの基本統計量(辞書型)
        """
        desc = series.describe()
        return_dict = {
            "count": round(desc["count"], 2),
            "mean": round(desc["mean"], 2),
            "std": round(desc["std"], 2),
            "min": round(desc["min"], 2),
            "max": round(desc["max"], 2),
            "25%": round(desc["25%"], 2),
            "50%": round(desc["50%"], 2),
            "75%": round(desc["75%"], 2)
        }
        return return_dict
        

    df = pd.concat([x.reset_index(drop=True), y.reset_index(drop=True)], axis=1)


    # BIN数の設定
    NUM_BINS = num_bins
    for node_info in tree_structure_dict:
        # 各ノードのヒストグラムを書くための条件を取得
        feats = get_feat_to_root(node_info["node_number"])
        # 大元のスキャンデータを読み込み
        tmp = df.copy()
        for feat in reversed(feats):
            # もし、ノードが左側だった場合、条件に当てはまるものを抽出
            if (feat["LorR"] == "LEFT"):
                tmp = tmp[tmp[feat["feature"]] <= feat["threshold"]]
            # もし、ノードが右側だった場合、条件に当てはまるもの以外を抽出
            elif (feat["LorR"] == "RIGHT"):
                tmp = tmp[~(tmp[feat["feature"]] <= feat["threshold"])]

        # mapメソッドで使う関数
        def get_left(x):
            return x.left
        def get_right(x):
            return x.right
        # cutメソッドを適用する前に外れ値がある場合は除く。
        series, outlier = replace_outlier(tmp[obj_var])
        # cutメソッドで指定のBIN数にデータを分割、その後列名の設定等々の処理を行う。
        # cutting_bins = pd.cut(tmp[obj_var].values, NUM_BINS).value_counts().reset_index()

        if (series.unique().max() <= NUM_BINS and y.dtype == np.int64):
            series = series.astype(np.int64)
            # NUM_BISの長さを持つ空のデータフレーム作成
            cutting_bins = pd.DataFrame(index=range(NUM_BINS))
            # x0を基準にする
            cutting_bins["x0"] = cutting_bins.index
            # x1は+1した値にする -> [0, 1), [1, 2)に対応するようにする
            cutting_bins["x1"] = cutting_bins["x0"] + 1
            # x0とx1の範囲に収まるデータ数をカウントする
            cutting_bins["n_num"] = np.bincount(series.values, minlength=NUM_BINS)
        else:
            cutting_bins = pd.cut(series.values, NUM_BINS).value_counts().reset_index()
            cutting_bins["x0"] = cutting_bins["index"].map(get_left)
            cutting_bins["x1"] = cutting_bins["index"].map(get_right)
            cutting_bins = cutting_bins.drop(columns=["index"]).rename(columns={0:"n_num"}).reset_index(drop=False).rename(columns={"index":"hist_num"})

        cutting_bins["prob"] = cutting_bins["n_num"] / cutting_bins["n_num"].sum() * NUM_BINS / (cutting_bins["x1"].max() - cutting_bins["x0"].min())



        # 整形したDataFrameを辞書型に変換
        add_dict = cutting_bins.to_dict(orient="records")

        node_info["hist_data"] = add_dict
        node_info["hist_describe"] = get_describe(series)
        node_info["outlier_describe"] = get_describe(outlier)
        
    return add_dict

def tree_dump(clf, obj_var, num_bins, x, y):
    '''
    abst:
        学習した決定木の構造をJsonで出力
    input:
        clf: scikit-learnの決定木の構造
        obj_var: 
        num_bins: ヒストグラムのBin数
        x: 学習データ(特徴量)
        y: 学習データ(目的変数)
    output:
        
    '''
    
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
            'parent':get_parent_id(child_l_list, child_r_list, node),
            'child_l':int(child_l_list[node]),
            'child_r':int(child_r_list[node]),
            'n_sample':int(n_sample_list[node]),
            'n_sample_div':n_sample_div(child_l_list, child_r_list, n_sample_list, node),
            'mu': get_node_mu(child_l_list, child_r_list, reaching_leafs, y, node),
            'sigma': get_node_sigma(child_l_list, child_r_list, reaching_leafs, y, node)
        }
        for node in range(n_node)
    ]

    get_histdata(tree_structure_dict, x, y, obj_var, num_bins)

    f = open("./data/tree_structure.json", "w")
    json.dump(tree_structure_dict, f, indent=4, allow_nan=True)
    f.close()