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

function plot_histogram_jupyter(currentNode){
    require(["d3"], function(d3) {
        // ヒストグラムがすでに描画されていれば、削除する。
        d3.select("#tree").selectAll("#describe")
            .remove();
        d3.select("#tree").selectAll("#histogram")
            .remove();
        // ヒストグラム描画用のデータの読み込み
        data = currentNode.data.data.hist_data
        // 描画する画面のサイズ設定
        var margin = {top: 10, right: 30, bottom: 30, left: 70};

        var width = 1000 - margin.left - margin.right;
        var height = 500 - margin.top - margin.bottom;
        var padding = margin.left;

        
        // tooltip用div要素を追加
        var tooltip = d3.select("#tree").append("div").attr("class", "tooltip")
        // 描画する画面をtree要素の下にsvg要素として追加
        var svg = d3.select("#tree")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("id", "histogram");
        var xScale = d3.scaleBand()
            .rangeRound([padding, width - padding])
            .padding(0.1)
            .domain(data.map(function(d){ return d.x0; }));
        var yScale = d3.scaleLinear()
            .domain([0, d3.max(data, function(d){ return d.n_num; })])
            .range([height - padding, padding]);

        svg.append("g")
            .attr("transform", "translate(" + 0 + "," + (height-padding) + ")")
            .call(d3.axisBottom(xScale)
                    .tickValues(xScale.domain().filter(function(d,i){ 
                        return !(i % 3); }))
                );
            
        svg.append("g")
            .attr("transform", "translate(" + padding + "," + 0 + ")")
            .call(d3.axisLeft(yScale))
            .append("text")
            .attr("x", -50)
            .attr("y", 200)
            .style("text-anchor", "middle")
            .style("fill", "black")
            .style("writing-mode", "tb")
            .style("glyph-orientation-vertical", 90)
            .text("num_sample");

        svg.append("g")
            .selectAll("rect")
            .data(data)
            .enter()
            .append("rect")

            .attr("x", function(d){ return xScale(d.x0) - 1; })

            .attr("y", function(d){ return yScale(d.n_num); })
            .attr("width", xScale.bandwidth())
            .attr("height", function(d){ return height - padding - yScale(d.n_num); })
            .attr("fill", "steelblue")
            .on("mouseover", function(d){
                tooltip
                    .style("visibility", "visible")
                    .html("length:" + d.n_num + "<br>range[" + d.x0 + ", " + d.x1 + "]");
            })
            .on("mousemove", function(d){
                var element = document.getElementById( "tree" )
                tooltip
                    .style("top", (d3.mouse(element)[1] - 10) + "px")
                    .style("left", (d3.mouse(element)[0] + 20) + "px");
            })
            .on("mouseout", function(d){
                tooltip.style("visibility", "hidden");
            })
            .attr("fill", "steelblue")
            .attr("class", "bar")


        var hist_describe = currentNode.data.data.hist_describe
        hist_describe["　"] = "ヒストグラム"
        var outlier_describe = currentNode.data.data.outlier_describe
        outlier_describe["　"] = "外れ値"
        
        // キー順序のリスト
        var order = ["　", "count", "mean", "std", "min", "max", "25%", "50%", "75%"];
        var tmp = {}, tmp2 = {}
        // キーを並べ替え
        for (var key in order){
            tmp[order[key]] = hist_describe[order[key]];
            tmp2[order[key]] = outlier_describe[order[key]];
        }
        var test_dict = [tmp, tmp2]
        var names = d3.keys(test_dict[0])
        /* 基本統計量を描画 */
        var table = d3.select("#tree")
            .append("div").attr("id", "describe").attr("align", "center")
            .append("table")
            .attr("class", "table")
            .attr("border", "0")
            .attr("cellspacing", "0")
            .attr("cellpadding", "5");
            
        table.append("thead")
            .append("tr")
            .selectAll("th")
            .data(names)
            .enter()
            .append("th")
            .text(function(d) { return d; });
        
        table.append("tbody")
            .selectAll("tr")
            .data(test_dict)
            .enter()
            .append("tr")
            .selectAll("td")
            .data(function(row){  
                return d3.entries(row);})
            .enter()
            .append("td")
            .text(function(d) {
                return d.value; });   
    });
}
