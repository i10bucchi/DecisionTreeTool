function make_destribution(tree_structure) {
    var datas = [];
    var data;
    var i;

    // 条件に該当するノード情報から分布に該当する座標点取得する
    function getTargetNode(i, datas) {
        if (tree_structure[i].sigma < (0.6 * tree_structure[0].sigma) && tree_structure[i].n_sample > 0.1 * tree_structure[0].n_sample) {
            data = getGaussianData(tree_structure[i].mu, tree_structure[i].sigma);
            datas.push(
                {
                    'node_number': tree_structure[i].node_number,
                    'mu': tree_structure[i].mu,
                    'sigma': tree_structure[i].sigma,
                    'min_q': d3.min(data, function(d) { return d.q }),
                    'max_q': d3.max(data, function(d) { return d.q }),
                    'max_p': d3.max(data, function(d) { return d.p }),
                    "data": data
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

    // 条件に該当するノード情報から分布に該当する座標点取得する
    // for (i = 0; i < tree_structure.length; i++) {
    //     if (tree_structure[i].sigma < (0.6 * tree_structure[0].sigma) && tree_structure[i].n_sample > 0.1 * tree_structure[0].n_sample) {
    //         data = getGaussianData(tree_structure[i].mu, tree_structure[i].sigma);
    //         datas.push(
    //             {
    //                 'node_number': tree_structure[i].node_number,
    //                 'mu': tree_structure[i].mu,
    //                 'sigma': tree_structure[i].sigma,
    //                 'min_q': d3.min(data, function(d) { return d.q }),
    //                 'max_q': d3.max(data, function(d) { return d.q }),
    //                 'max_p': d3.max(data, function(d) { return d.p }),
    //                 "data": data
    //             }
    //         );
    //     }
    // }

    datas = getTargetNode(0, datas);

    var margin = { top: 20, right: 20, bottom: 30, left: 50 };
    var width = 960 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;

    // x座標スケール作成
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

    // グラフのカーブを定義
    var line = d3.line()
        .x(function(d) { return x(d.q); })
        .y(function(d) { return y(d.p); });
    
    var tooltip = d3.select("body").append("div").attr("class", "tooltip");

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    rootdata = getGaussianData(tree_structure[0].mu, tree_structure[0].sigma);
    svg.append("path")
        .datum(rootdata)
        .attr("class", "line_root")
        .attr("d", line)
        .style('fill', 'none')
        .style('stroke-width', '2.0px')
        .style('stroke', '#ff0000');

    for (i = 0; i < datas.length; i++) {
        svg.append("path")
            .datum(datas[i])
            .attr("class", "line_" + datas[i].node_number)
            .attr("d", line(datas[i].data))
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
}

function getGaussianData(mu, sigma) {
    var data = []
    var inc = sigma * 3 / 100;
    var range_min = mu - (sigma * 3);
    var range_max = mu + (sigma * 3);
    for (var q = range_min; q < range_max; q += inc) {
        el = { "q": q, "p": jStat.normal.pdf( q, mu, sigma ) };
        data.push(el);
    }
    return data;
}

// function getJson(url) {
//     var request = new XMLHttpRequest();
//     request.open('GET', url);
//     request.responseText = 'json';
//     request.addEventListener('load', (event) => make_destribution(JSON.parse(request.response)));
//     request.send();
// }

// var JSON_FILE_PATH = 'data/tree_structure.json'

// getJson(JSON_FILE_PATH)

make_destribution(jsonData);