
// 決定木描画用関数
function make_tree(tree_structure) {
    // フラットデータをヒエラルキーデータへ変換
    var stratify = d3.stratify()
        .id(function(d) { return d.node_number; })
        .parentId(function(d) { return d.parent; });
    
    var tree_structure_stratifed = stratify(tree_structure);
    
    // 各要素のnameにidを代入
    tree_structure_stratifed.each(function(d) { d.name = d.id; });

    // 図のマージンと縦横
    var margin = {top: 100, right: 150, bottom: 100, left: 150};
    var width = screen.width - margin.left - margin.right;
    var height = screen.height * 1 - margin.top - margin.bottom;

    // tooltip用div要素追加
    var tooltip = d3.select("body").append("div").attr("class", "tooltip");

    // 決定木レイアウトの作成
    var treemap = d3.tree()
        .size([height, width]);

    //  データの適用
    var root = d3.hierarchy(tree_structure_stratifed, function(d) { return d.children; });

    // 決定木のレイアウトにデータをマッピング
    var treeData = treemap(root);

    // 
    var nodes = treeData.descendants();
    var links = treeData.descendants().slice(1);

    // bodyへsvg要素(id=tree)を追加
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id", "tree");
    
    // svg要素へg要素を追加しmarginの分ずらす
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // adds the links between the nodes
    var link = g.selectAll(".link")
        .data( links )
        .enter().append("path")
        .attr("class", function(d) {
            if (d.data.data.sigma < (0.6 * tree_structure[0].sigma)) {
                // 信頼性のある収束済みリンク
                return "link_conv";
            }
            else {
                // 収束していないリンク
                return "link";
            }
        })
        .attr("d", function(d) {
            return "M" + d.y + "," + d.x
                + "C" + (d.y + d.parent.y) / 2 + "," + d.x
                + " " + (d.y + d.parent.y) / 2 + "," + d.parent.x
                + " " + d.parent.y + "," + d.parent.x;
        });
    
    // adds each node as a group
    var node = g.selectAll(".node")
        .data( nodes )
        .enter().append("g")
        .attr("class", function(d) { return "node" + (d.children ? " node--internal" : " node--leaf"); })
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    // adds the circle to the node
    var mu_max = d3.max(nodes, function(d) { return d.data.data.mu } );
    var mu_min = d3.min(nodes, function(d) { return d.data.data.mu } );
    node.append("circle")
        .attr("r", 10)
        .attr("class", function(d) { return "circle_" + d.data.data.node_number })
        .style("fill", function(d) {return "#" + ("000000" + Math.round(255 - ((d.data.data.mu - mu_min) * 255 / (mu_max - mu_min))).toString(16)).slice(-6); }) // ノードの色設定
        .on("click", function(d) {
            // 背景を描画
            popup_func()
            // ヒストグラム描画用関数の呼び出し
            plot_histogram(d)
        }) //以下マウスオーバーのイベント設定
        .on("mouseover", function(d){
            var data = d.data.data
            tooltip
                .style("visibility", "visible")
                .html("sample : " + data.n_sample + "<br>sample_l : " + data.n_sample_div[0]+
                "<br>sample_r : " + data.n_sample_div[1]+
                "<br>mu : " + data.mu +
                "<br>var :" + data.sigma);
        })
        .on("mousemove", function(d){
            tooltip
                .style("top", (d3.event.pageY - 20) + "px")
                .style("left", (d3.event.pageX + 10) + "px");
        })
        .on("mouseout", function(d){
            tooltip.style("visibility", "hidden");
        })

    // adds the text to the node
    node.append("text")
        .attr("dy", ".35em")
        .attr("y", function(d) { return d.children ? -35 : -20 })
        .style("text-anchor", "end")
        .text(function(d) { return 'node_number: ' + d.data.data.node_number });

    node.append("text")
        .attr("dy", ".35em")
        .attr("y", function(d) { return d.children ? -20 : 0; })
        .style("text-anchor", "end" )
        .text(function(d) { return d.children ? d.data.data.feature + ' <= ' + d.data.data.threshold : d.name; });
}


// function getJson(url) {
//     var request = new XMLHttpRequest();
//     request.open('GET', url);
//     request.responseText = 'json';
//     request.addEventListener('load', (event) => make_tree(JSON.parse(request.response)));
//     request.send();
// }


// var JSON_FILE_PATH = 'data/tree_structure.json'
var CSV_FILE_PATH = 'data/user_scan.csv'

// getJson(JSON_FILE_PATH)

make_tree(jsonData)

