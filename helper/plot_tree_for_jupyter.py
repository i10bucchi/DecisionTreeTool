from helper import tree_to_json, tree, get_script
def plot_tree(x, y, clf, obj_val, bins_num=25):
    """
    abst:
        決定木の分析結果をjupyter上にプロットするメソッド
    input:
        x : 従属変数
        y : 目的変数
        clf : scikit-learn の決定木の構造
        obj_val : 目的変数の列名
        bins_num : ヒストグラムのbin数
    output:
        string : IPython.display.HTML で描画させるスクリプト
    """
    # 決定木構造をjsonにダンプ
    tree_to_json.tree_dump(clf, obj_val, bins_num, x, y)
    # 分析結果を表示するためのスクリプト取得
    src = get_script.get_html_for_jupyter()
    
    return src
