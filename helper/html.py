from helper import const

def get_html():
    '''
    abst:
        分析結果を表示するHTMLを作成
    input:
    output:
        html: 分析結果を表示するhtml
    '''
    f = open(const.JSON_PATH, "r")
    json = f.read()
    f.close()
    f = open(const.CSS_PATH, "r")
    style = f.read()
    f.close()
    f = open(const.TREE_JS_PATH, "r")
    tree_plot_js = f.read()
    f.close()
    f = open(const.FIT_JS_PATH, "r")
    poisson_js = f.read()
    f.close()
    f = open(const.HIST_JS_PATH, "r")
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
    html += '    <!-- jsファイルの読み込み -->\n'
    html += '    <script>var jsonData = {}</script>'.format(json)
    html += '    <script>{}</script>\n'.format(tree_plot_js)
    html += '    <script>{}</script>\n'.format(poisson_js)
    html += '    <script>{}</script>\n'.format(histogram_plot_js)
    html += '</body>\n'
    
    return html