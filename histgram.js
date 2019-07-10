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
        .attr("height", "100%")
        .attr("id", "histogram");
    var xScale = d3.scaleBand()
        .rangeRound([padding, width - padding])
        .padding(0.1)
        .domain(data.map(function(d){ return d.x0; }));
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(data, function(d){ return d.n_num; })])
        .range([height - padding, padding]);

    console.log(screen.width)
    console.log(document.getElementById("histogram").width)

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

}
