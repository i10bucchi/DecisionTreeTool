import pandas as pd

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
    ldf = int(len(df.index) * 0.2)
    df_train = df[ldf:]
    df_test = df[:ldf]

    # 説明変数と目的変数へ分割
    x = df_train.drop(obj_var, axis=1)
    y = df_train[obj_var]
    X = df_test.drop(obj_var, axis=1)
    Y = df_test[obj_var]

    # 表示
    return x, y, X, Y