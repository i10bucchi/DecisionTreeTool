from helper import const

def get_html_for_jupyter():
    '''
    abst:
        分析結果をjupyterで表示するscriptを作成
    input:
    output:
        script: 分析結果を表示するscript
    '''
    f = open(const.JSON_PATH, "r")
    json = f.read()

    script  = '<script type="text/javascript" src="./js/require.js"></script>\n'
    script += '<script>\n'
    script += 'require.config({\n'
    script += '  baseUrl: "js",'
    script += '  paths:{\n'
    script += '    "d3": "d3"\n'
    script += '  }\n'
    script += '});\n'
    script += '</script>\n'
    script += '<link rel="stylesheet" type="text/css" href="./css/style.css">\n'
    script += '<g id="tree"></g>\n'
    script += '<script type="text/javascript" src="{}"></script>\n'.format(const.TREE_JS_FOR_JUPYTER_PATH)
    script += '<script type="text/javascript" src="{}"></script>\n'.format(const.FIT_JS_FOR_JUPYTER_PATH)
    script += '<script type="text/javascript" src="{}"></script>\n'.format(const.HIST_JS_FOR_JUPYTER_PATH)
    script += '<script> var jsonData = {}</script>\n'.format(json)
    script += '<script>\n'
    script += 'make_tree(jsonData);\n'
    script += 'make_destribution(jsonData);\n'
    script += '</script>'
    
    return script