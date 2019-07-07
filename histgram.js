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

    var dataset = [
        { "name": "A", "value": 5 },
        { "name": "B", "value": 6 },
        { "name": "C", "value": 8 },
        { "name": "D", "value": 1 },
        { "name": "E", "value": 2 },
        { "name": "F", "value": 6 },
        { "name": "G", "value": 8 },
        { "name": "H", "value": 6 },
        { "name": "I", "value": 10 },
        { "name": "J", "value": 9 }
    ];    
    // ヒストグラム描画用のデータの読み込み
    data = currentNode.data.data.hist_data
    // 描画する画面のサイズ設定
    var margin = {top: 10, right: 30, bottom: 30, left: 50},
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
        .domain(data.map(function(d){ return d.x1; }));
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(data, function(d){ return d.n_num; })])
        .range([height - padding, padding]);

    svg.append("g")
        .attr("transform", "translate(" + 0 + "," + (height-padding) + ")")
        .call(d3.axisBottom(xScale));
    svg.append("g")
        .attr("transform", "translate(" + padding + "," + 0 + ")")
        .call(d3.axisLeft(yScale))

    svg.append("g")
        .selectAll("rect")
        .data(data)
        .enter()
        .append("rect")
        .attr("x", function(d){ return xScale(d.x1) - 1; })
        .attr("y", function(d){ return yScale(d.n_num); })
        .attr("width", xScale.bandwidth())
        .attr("height", function(d){ return height - padding - yScale(d.n_num); })
        .attr("fill", "steelblue");


    // /***** CSVファイルを読み込んでヒストグラムを描画 *****/
    // d3.csv(CSV_FILE_PATH, function(error, data) {
    //     var NUM_BINS = document.getElementById("bin_num").value;
    //     var X_DOMAIN = [1, 50]
    //     var filltered_data = data
    //     // 条件抽出
    //     for(var i = 0; i < feats.length; i++){
    //         // var feat = feats[i].split(".")[0];
    //         var feat = feats[i];
    //         var th = Number(threshes[i]);
    //         var upAndDown = bool[i];
    //         filltered_data = filltered_data.filter(function(e){
    //             if (upAndDown == "UP"){
    //                 return (e[feat] <= th);
    //             }
    //             else if (upAndDown == "DOWN"){
    //                 return (e[feat] > th);
    //             }
    //         })
    //     }

    //     // 条件をクリアしたデータ(スキャン数の配列)
    //     map = filltered_data.map(function(d,i){ return parseFloat(d.scan_num); })
    //     console.log(map)
    //     // 描画する画面のサイズ設定
    //     var margin = {top: 10, right: 30, bottom: 30, left: 50},
    //         width = (screen.width / 2) - margin.left - margin.right;
    //         height = (screen.height / 2) - margin.top - margin.bottom;
        
    //     // tooltip用div要素を追加
    //     var tooltip = d3.select("#popup-inner").append("div").attr("class", "tooltip")
    //     // 描画する画面をpopup-inner要素の下にsvg要素として追加
    //     var svg = d3.select("#popup-inner")
    //         .append("svg")
    //         .attr("width", "100%")
    //         .attr("height", "100%")
    //         .attr("id", "histogram"),
    //         g = svg.append("g")
    //                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
    //     // x軸の設定
    //     var x = d3.scaleLinear()
    //         .rangeRound([0, width])
    //         .domain(X_DOMAIN);

    //     var bins = d3.histogram()
    //                 .domain(x.domain())
    //                 .thresholds(x.ticks(NUM_BINS))(map);        
    //     // y軸の設定
    //     var y = d3.scaleLinear()
    //         .domain([0, d3.max(bins, function(d) { return d.length; })])
    //         //.domain([0, 200000])
    //         .range([height, 0]);

    //     // それぞれのbinの要素を計算
    //     var bar = g.selectAll(".bar")
    //         .data(bins)
    //         .enter().append("g")
    //         .attr("class", "bar")
    //         .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; });
        
    //     // 棒を描画
    //     bar.append("rect")
    //         .attr("x", 1)
    //         .attr("width", x(bins[0].x1) - x(bins[0].x0) - 1)
    //         // .attr("height", function(d) { return height - y(d.length); });
    //         .attr("height", function(d) { return height - y(d.length); })
    //         .on("click", function(d){
    //             var max = d.reduce((a,b)=>a>b?a:b)
    //             var min = d.reduce((a,b)=>a<b?a:b)
    //         })
    //         .on("mouseover", function(d){
    //             var max = d.reduce((a,b)=>a>b?a:b)
    //             var min = d.reduce((a,b)=>a<b?a:b)
    //             tooltip
    //                 .style("visibility", "visible")
    //                 .html("length:" + d.length + "<br>range[" + min + ", " + max + "]");
    //         })
    //         .on("mousemove", function(d){
    //             var element = document.getElementById( "popup-inner" )
    //             tooltip
    //                 .style("top", (d3.mouse(element)[1] - 10) + "px")
    //                 .style("left", (d3.mouse(element)[0] + 20) + "px");
    //         })
    //         .on("mouseout", function(d){
    //             tooltip.style("visibility", "hidden");
    //         })
    //         .attr("fill", "steelblue")
    //         .attr("class", "bar")

    //     g.append("g")
    //         .attr("class", "axis axis--x")
    //         .attr("transform", "translate(0," + height + ")")
    //         .call(d3.axisBottom(x));
    //     g.append('g')
	// 	    .attr('class', 'axis axis--y')
    //         .call(d3.axisLeft(y));  
        
    // })
}
