from sklearn import tree

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
        presort=opts["presort"]
    )
    clf = clf.fit(x, y)
    y_ = clf.predict(x)
    y_pred = clf.predict(X)

    # print("Result:")
    # print('\t train: LSM={:>10.2f}'.format(((y_ - y) * (y_ - y)).sum() / len(y) / 2))
    # print('\t test:  LSM={:>10.2f}'.format(((y_pred - Y) * (y_pred - Y)).sum() / len(Y) / 2))

    return clf