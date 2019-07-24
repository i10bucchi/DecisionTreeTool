function make_destribution(tree_structure) {
    require(["d3"], function(d3) {
        var datas = [];
        var data;
        var i;

        // 条件に該当するノード情報から分布に該当する座標点取得する
        function getTargetNode(i, datas) {
            if (tree_structure[i].sigma < (0.6 * tree_structure[0].sigma)) {
                data = tree_structure[i].hist_data
                datas.push(
                    {
                        'node_number': tree_structure[i].node_number,
                        'mu': tree_structure[i].mu,
                        'sigma': tree_structure[i].sigma,
                        'min_q': d3.min(data, function(d) { return d.x0 }),
                        'max_q': d3.max(data, function(d) { return d.x1 }),
                        'max_p': d3.max(data, function(d) { return d.prob }),
                        'hist_data': data
                    }
                );
                return datas;
            }
            else {
                if (tree_structure[i].child_l != -1) {
                    datas = getTargetNode(tree_structure[i].child_l, datas);
                }
                if (tree_structure[i].child_r != -1) {
                    datas = getTargetNode(tree_structure[i].child_r, datas);
                }
                return datas;
            }
        }

        // 対象ノードの情報を配列で取得
        datas = getTargetNode(0, datas);

        // グラフを描画するキャンバス情報
        var margin = { top: 20, right: 20, bottom: 30, left: 50 };
        var width = 960 - margin.left - margin.right;
        var height = 500 - margin.top - margin.bottom;

        // x座標スケール作成
        // - .domainはメモリを決定する[min, max]
        // - .rangeはメモリをキャンバスに収めるにように設定する
        var x = d3.scaleLinear()
            .domain([d3.min(datas, function(d) { return d.min_q }), d3.max(datas, function(d) { return d.max_q })])
            .range([0, width]);

        // y座標スケール作成
        var y = d3.scaleLinear()
            .domain([0, d3.max(datas, function(d) { return d.max_p })])
            .range([height, 0]);

        // x座標設定
        var xAxis = d3.axisBottom(x);

        // y座標設定
        var yAxis = d3.axisLeft(y);
        
        // マウスオーバーで表示する情報のクラスを作成
        var tooltip = d3.select("#tree").append("div").attr("class", "tooltip");

        // キャンバスの作成
        var svg = d3.select("#tree").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        
        // キャンバスへx座標軸を作成
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // キャンバスへy軸座標を作成
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

        // ヒストグラムを滑らかに繋いでぐ
        var histline = d3.line()
            .curve(d3.curveMonotoneX)
            .x(function(d) { return x( (d.x0 + d.x1) / 2 ) })
            .y(function(d) { return y(d.prob) });

        // ルートノードのガウス分布最優推定モデルを作成
        svg.append("path")
            .datum(tree_structure[0].hist_data)
            .attr("class", "line_root")
            .attr("d", histline)
            .style('fill', 'none')
            .style('stroke-width', '2.0px')
            .style('stroke', '#ff0000');

        // 収束しているノードのガウス分布最優推定モデルを作成
        for (i = 0; i < datas.length; i++) {
            svg.append("path")
                .datum(datas[i])
                .attr("class", "line_" + datas[i].node_number)
                .attr("d", histline(datas[i].hist_data))
                .style('fill', 'none')
                .style('stroke-width', '2.0px')
                .style('stroke', 'steelblue')
                // .on("click", function(d) {
                //     d3.select(".circle_" = d.node_number)
                //         .style('')
                // })
                .on("mouseover", function(d){
                    svg.select(".line_" + d.node_number).style("stroke", "#ffff00");
                    tooltip
                        .style("visibility", "visible")
                        .html(
                            "node_number : " + d.node_number + "<br>"
                            + "mean : " + d.mu.toFixed(2) + "<br>"
                            + "variance : " + d.sigma.toFixed(2) + "<br>"
                        );
                })
                .on("mousemove", function(d){
                    tooltip
                        .style("top", (d3.event.pageY - 20) + "px")
                        .style("left", (d3.event.pageX + 10) + "px");
                })
                .on("mouseout", function(d) { 
                    svg.select(".line_" + d.node_number).style("stroke", "steelblue"); 
                    tooltip.style("visibility", "hidden");
                });
        }
    });
}
