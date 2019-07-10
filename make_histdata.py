import pandas as pd
import numpy as np
def get_histdata(tree_structure_dict, x, y, obj_var):
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
        # print("bef:{}, aft:{}".format(series.shape[0], replaced_series.shape[0]))
        # print(series.describe())
        # print(replaced_series.describe())
        return replaced_series
        

    df = pd.concat([x.reset_index(drop=True), y.reset_index(drop=True)], axis=1)


    sigma = tree_structure_dict[0]["sigma"]
    #df = df[df[obj_var] < (sigma * 4)]
    # BIN数の設定
    NUM_BINS = 25
    
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
        series = replace_outlier(tmp[obj_var])
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
        # もともとのtree_structure_dictに追記
        node_info["hist_data"] = add_dict
