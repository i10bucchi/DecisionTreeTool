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
    d3.select("#popup-inner").selectAll("#hist_describe")
        .remove();
    d3.select("#popup-inner").selectAll("#outlier_describe")
        .remove();
    d3.select("body").selectAll("#histogram")
        .remove();


    // ヒストグラム描画用のデータの読み込み
    data = currentNode.data.data.hist_data
    // 描画する画面のサイズ設定
    var margin = {top: 10, right: 30, bottom: 30, left: 70},
        svgwidth = (screen.width / 2) - margin.left - margin.right;
        svgheight = (screen.height / 2) - margin.top - margin.bottom;
    
    var width = screen.width / 1.7;
    var height = screen.height / 2;
    var padding = margin.left;

    
    // tooltip用div要素を追加
    var tooltip = d3.select("#popup-inner").append("div").attr("class", "tooltip")
    // 描画する画面をpopup-inner要素の下にsvg要素として追加
    var svg = d3.select("#popup-inner")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "60%")
        .attr("id", "histogram");
    var xScale = d3.scaleBand()
        .rangeRound([padding, width - padding])
        .padding(0.1)
        .domain(data.map(function(d){ return d.x0; }));
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(data, function(d){ return d.n_num; })])
        .range([height - padding, padding]);

    // console.log(screen.width)
    // console.log(document.getElementById("histogram").clientWidth)

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


    var hist_describe = currentNode.data.data.hist_describe
    var outlier_describe = currentNode.data.data.outlier_describe

    var hist_names = d3.keys(hist_describe)
    var outlier_names = d3.keys(outlier_describe)
    var hist_val = [d3.values(hist_describe)]
    var outlier_val = [d3.values(outlier_describe)]
    /* ヒストグラムの基本統計量を描画 */
    var table_left = d3.select("#popup-inner")
        .append("div").attr("class", "blocka").attr("id", "hist_describe").attr("align", "center")
        .append("text").text("ヒストグラムの基本統計量")
        .append("table").attr("class", "table");
        
    table_left.append("thead")
        .append("tr")
        .selectAll("th")
        .data(hist_names)
        .enter()
        .append("th")
        .text(function(d) { return d; });
    
    table_left.append("tbody")
        .selectAll("tr")
        .data(hist_val)
        .enter()
        .append("tr")
        .selectAll("td")
        .data(function(row){ return row;})
        .enter()
        .append("td")
        .text(function(d) { return d; });
        
    /* 外れ値の基本統計量を描画 */
    var table_right = d3.select("#popup-inner")
        .append("div").attr("class", "blockb").attr("id", "outlier_describe").attr("align", "center")
        .append("text").text("外れ値の基本統計量")
        .append("table").attr("class", "table");
        
    table_right.append("thead")
        .append("tr")
        .selectAll("th")
        .data(outlier_names)
        .enter()
        .append("th")
        .text(function(d) { return d; });
    table_right.append("tbody")
        .selectAll("tr")
        .data(outlier_val)
        .enter()
        .append("tr")
        .selectAll("td")
        .data(function(row) { return row; })
        .enter()
        .append("td")
        .text(function(d) { return d; });
    
}
