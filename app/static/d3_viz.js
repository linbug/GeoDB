
        data = JSON.parse(data)
        var rainfall = [];
        var parseDate = d3.time.format("%Y-%m-%d").parse;
        var dateFormat = d3.time.format("%e %b %Y");
        var offset = 15;

        for(var o in data){
            rainfall.push(Math.round(data[o]))
        }

        var dates= [];
        for ( var p in data){

            dates.push(parseDate(p));
        };

        var margin = {top: 50, right: 30, bottom: 70, left: 40},
            width = 500 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        var x = d3.scale.ordinal()
                .domain(dates)
                .rangeBands([0,width], 0.1) //calculates spacing of x axis; adds padding between bars

        var y = d3.scale.linear()
                .domain([0, d3.max(rainfall)])
                .range([height, 0]);

        var xAxis = d3.svg.axis()
                    .scale(x)
                    .tickValues(x.domain().filter(function(d, i) {
                        if(rainfall.length>60)
                            {return !(i%30)}
                        else
                            { return !(i % 7)}
                    }))
                    .tickFormat(dateFormat)
                    .orient("bottom")

        var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left");

        // Define the div for the tooltip
        var tooltip = d3.select("#tooltip_div").append("div")
                    .attr("class", "tooltip")
                    // .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                    // .style("left", d3.select(".axis").attr("x") + "px")

                    // .style("left", 20)
                    .style("opacity", 0);

        var chart = d3.select(".chart")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var result_text = d3.select("#result_text")
                            .html("Rainfall at " + ((latitude>=0)?(latitude + "° N") : (Math.abs(latitude))+ "° S") + ", "+((longitude>=0)?(longitude + "° W") : (Math.abs(longitude))+ "° E") + '<br>' + dateFormat(dates[0]) + ' to ' + dateFormat(dates[1]))

        chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(" + offset + "," + height + ")")
        .call(xAxis)
        .selectAll("text") //rotates x axis lables
        .attr("y", 9)
        .attr("x", 6)
        .attr("dy", ".35em")
        .attr("transform", "rotate(45)")
        .style("text-anchor", "start");

        chart.append("g")
        .attr("class", "y axis")
        .call(yAxis)

        .append("text")
        .attr("transform", "rotate(90)")
        .attr("dy", "-.5em")
        .text("Rainfall (mm)");

        chart.selectAll(".bar")
            .data(rainfall)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("y", height)
            .attr("rainfall", function(d){return d})
            .attr("height", 0)
            .attr("width", x.rangeBand())
            .transition()
            .attr("y", function(d){return y(d)})
            .attr("height",function(d){return height - y(d);})
            .duration(900)

        chart.selectAll("rect")
            .data(dates)
            .attr("x", function(d){return x(d) + offset})

            .on("mouseover", function(d){
                tooltip.html(dateFormat(d) +  ": " + d3.select(this).attr("rainfall") + "mm")
                // .attr("x", width/2  +"px")
                tooltip.transition()
                    .style("opacity",1)
            })
            .on("mouseout", function(d){

                tooltip.transition()
                    .style("opacity", 0)
                    .transition()
                    .text()

            });

        var chart2 = d3.select(".total_rainfall")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height/3 )
                .append("g")
                .attr("transform", "translate(" + (margin.left ) +  "," + margin.top/2 + ")")

        var rainfall_stats = [d3.sum(rainfall), d3.max(rainfall), d3.mean(rainfall)]

        var total_x = d3.scale.linear()
                    .domain([0, 30*rainfall.length])
                    .range([0, width]);

        var total_y = d3.scale.linear()
                        .domain([0,3])
                        .range([0,100])

        var total_xAxis = d3.svg.axis()
        .scale(total_x)
        .orient("top");

        chart2.append("g")
                .attr("class", "x axis")

                .call(total_xAxis)

        var total_rainfall = d3.sum(rainfall);
        var rainfall_bar = chart2.append("rect")
                                    .attr("width", 0)
                                    .attr("height", 25)
                                    .attr("class", "rainfall_bar")
                                    .attr("transform", "translate(0,5)")
                                    .transition()
                                    .attr("width", total_x(total_rainfall))
                                    .duration(5000)

        chart2.append("text")
                .text(0)
                .attr("class", "text")
                .attr("x", 5)
                .attr("y", d3.select(".rainfall_bar").attr("height")/2 + 5)
                .transition()
                .duration(5000)
                .attr("x", total_x(total_rainfall)+ 5)
                .tween("text", function(){

                    var i = d3.interpolateRound(0,total_rainfall);
                    return function(t){

                        this.textContent = "Total rainfall: " + i(t) + " mm"
                    }
                })

