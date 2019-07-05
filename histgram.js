//クリックされたノードの位置が、兄弟ノードと比較して上か下かを判定する関数
// データ抽出の際に使用
function get_up_or_down(node) {
    if (node.parent == null) return false;
    var this_node_x = node.x
    var bro_node_x_one = node.parent.children[0].x
    if (this_node_x == bro_node_x_one){
        return "UP";
    } else {
        return "DOWN";
    }
}

// クリックされたノードの親ノードの条件を取得する関数
// データ抽出の際に使用
function get_parent_feature(node){
    if (node.parent == null) return false;
    var parent_feat = node.parent.data.data.feature
    return parent_feat
}
// クリックされたノードの親ノードの閾値を取得する関数
// データ抽出の際に使用
function get_parent_thresh(node){
    if (node.parent == null) return false;
    var parent_thresh = node.parent.data.data.threshold
    return parent_thresh
}

// 予め配置されていたpopup要素等を表示させる関数
function popup_func() {
    var popup = document.getElementById('js-popup');
    if(!popup) return;
    popup.classList.add('is-show');
  
    var blackBg = document.getElementById('js-black-bg');
    var closeBtn = document.getElementById('js-close-btn');
  
    closePopUp(blackBg);
    closePopUp(closeBtn);
  
    function closePopUp(elem) {
      if(!elem) return;
      elem.addEventListener('click', function() {
        popup.classList.remove('is-show');
      })
    }
}

// ヒストグラム描画用関数
function plot_histogram(currentNode) {
    // ヒストグラムがすでに描画されていれば、削除する。
    d3.select("body").selectAll("#histogram")
        .remove();


    /***** クリックされたノードの一つ親のノードからルートまでの条件と閾値を取得。 *****/
    // クリックされたノードの一つ親のノードからルートのキーを取得
    var feats = [], threshes = [], bool = [];

    // 条件と閾値を取得
    currentNode.forEach(function(node) {
        if ((get_parent_feature(node) != false) &&
            (get_parent_thresh(node) != false) &&
            (get_up_or_down(node) != false)){
                feats.push(get_parent_feature(node))
                threshes.push(get_parent_thresh(node))
                bool.push(get_up_or_down(node))
            }
    })
    

    /***** CSVファイルを読み込んでヒストグラムを描画 *****/
    d3.csv(CSV_FILE_PATH, function(error, data) {
        var NUM_BINS = document.getElementById("bin_num").value;
        var X_DOMAIN = [1, 50]
        var filltered_data = data
        // 条件抽出
        for(var i = 0; i < feats.length; i++){
            // var feat = feats[i].split(".")[0];
            var feat = feats[i];
            var th = Number(threshes[i]);
            var upAndDown = bool[i];
            filltered_data = filltered_data.filter(function(e){
                if (upAndDown == "UP"){
                    return (e[feat] <= th);
                }
                else if (upAndDown == "DOWN"){
                    return (e[feat] > th);
                }
            })
        }

        // 条件をクリアしたデータ(スキャン数の配列)
        map = filltered_data.map(function(d,i){ return parseFloat(d.scan_num); })
        console.log(map)
        // 描画する画面のサイズ設定
        var margin = {top: 10, right: 30, bottom: 30, left: 50},
            width = (screen.width / 2) - margin.left - margin.right;
            height = (screen.height / 2) - margin.top - margin.bottom;
        
        // tooltip用div要素を追加
        var tooltip = d3.select("#popup-inner").append("div").attr("class", "tooltip")
        // 描画する画面をpopup-inner要素の下にsvg要素として追加
        var svg = d3.select("#popup-inner")
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("id", "histogram"),
            g = svg.append("g")
                   .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        // x軸の設定
        var x = d3.scaleLinear()
            .rangeRound([0, width])
            .domain(X_DOMAIN);

        var bins = d3.histogram()
                    .domain(x.domain())
                    .thresholds(x.ticks(NUM_BINS))(map);        
        // y軸の設定
        var y = d3.scaleLinear()
            .domain([0, d3.max(bins, function(d) { return d.length; })])
            //.domain([0, 200000])
            .range([height, 0]);

        // それぞれのbinの要素を計算
        var bar = g.selectAll(".bar")
            .data(bins)
            .enter().append("g")
            .attr("class", "bar")
            .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; });
        
        // 棒を描画
        bar.append("rect")
            .attr("x", 1)
            .attr("width", x(bins[0].x1) - x(bins[0].x0) - 1)
            // .attr("height", function(d) { return height - y(d.length); });
            .attr("height", function(d) { return height - y(d.length); })
            .on("click", function(d){
                var max = d.reduce((a,b)=>a>b?a:b)
                var min = d.reduce((a,b)=>a<b?a:b)
            })
            .on("mouseover", function(d){
                var max = d.reduce((a,b)=>a>b?a:b)
                var min = d.reduce((a,b)=>a<b?a:b)
                tooltip
                    .style("visibility", "visible")
                    .html("length:" + d.length + "<br>range[" + min + ", " + max + "]");
            })
            .on("mousemove", function(d){
                var element = document.getElementById( "popup-inner" )
                tooltip
                    .style("top", (d3.mouse(element)[1] - 10) + "px")
                    .style("left", (d3.mouse(element)[0] + 20) + "px");
            })
            .on("mouseout", function(d){
                tooltip.style("visibility", "hidden");
            })
            .attr("fill", "steelblue")
            .attr("class", "bar")

        g.append("g")
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        g.append('g')
		    .attr('class', 'axis axis--y')
            .call(d3.axisLeft(y));  
        
    })
}
// スライダーで設定されているbin数をリアルタイムに更新する関数
function OnChangeValue(){
    var binvalue = document.getElementById("bin_num").value;
    d3.select("#bin_num_text").text(binvalue);  //スライダーの横にある表示を更新
}
