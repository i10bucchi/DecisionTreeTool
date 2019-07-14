import sys

from helper import tool_option, data_manager, tree_to_json, tree, html

def main():
    # オプションの取得
    tool_opts_dict, skltree_opts_dict = tool_option.get_command_opts(sys.argv[1:])
    # データ整形
    x, y, X, Y = data_manager.get_data(tool_opts_dict["csv_path"], tool_opts_dict["obj_var"], tool_opts_dict["dummy_vars"])
    # 決定木分析
    clf = tree.tree_calc(x, y, X, Y, skltree_opts_dict)
    # 決定木構造をjsonにダンプ
    tree_to_json.tree_dump(clf, tool_opts_dict["obj_var"], tool_opts_dict["num_of_bins"], x, y)
    # 分析結果を表示するためのhtml取得
    src = html.get_html()
    print(src)

main()