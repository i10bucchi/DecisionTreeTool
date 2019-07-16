import sys

from helper import tool_option, data_manager, tree_to_json, tree, html

def main():
    # オプションの取得
    opts_dict = tool_option.parse_commandline_opts()
    # データ整形
    x, y, X, Y = data_manager.get_data(opts_dict["input_csv"], opts_dict["objective_variable"], opts_dict["categolical_variable"])
    # 決定木分析
    clf = tree.tree_calc(x, y, X, Y, opts_dict)
    # 決定木構造をjsonにダンプ
    tree_to_json.tree_dump(clf, opts_dict["objective_variable"], opts_dict["bins_num"], x, y)
    # 分析結果を表示するためのhtml取得
    src = html.get_html()
    print(src)

main()