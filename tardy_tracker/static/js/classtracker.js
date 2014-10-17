/**
 * Created by Adam on 10/14/14.
 */

$(document).ready(function () {

    $('#checkIn').on('click', function () {

        var currentUser = $('#currentUser').data('username');
        var currentCourse = $('#currentCourse').data('course');
        var thisCourse = currentCourse
        var datas = {
            student: currentUser,
            course: currentCourse
        };
        datas = JSON.stringify(datas);
        $.ajax({
            url: '/checkin/',
            type: 'POST',
            dataType: 'json',
            data: datas,
            success: function (response) {
                console.log(response);
                var total = 'Total Checkins for ' + currentCourse + '=' + response['checkin_total'];
                var chartData = response['chart_data'];
                console.log(chartData, 'total');
                $('#checkInButton').html("Checked In!");
                $('#totalCheckin').append(total);
                //D3 data

                var bardata = [];

                for (var i = 0; i < chartData.length; i++) {
                    bardata.push(chartData[i]['dcount'])
                }

                var height = 400,
                    width = 600,
                    barWidth = 50,
                    barOffset = 5;

                var tempColor;

                var colors = d3.scale.linear()
                    .domain([0, bardata.length * .33, bardata.length * .66, bardata.length])
                    .range(['#B58929', '#C61C6F', '#268BD2', '#85992C'])

                var yScale = d3.scale.linear()
                    .domain([0, d3.max(bardata)])
                    .range([0, height]);

                var xScale = d3.scale.ordinal()
                    .domain(d3.range(0, bardata.length))
                    .rangeBands([0, width])

                var tooltip = d3.select('body').append('div')
                    .style('position', 'absolute')
                    .style('padding', '0 10px')
                    .style('background', 'white')
                    .style('opacity', 0)

                var myChart = d3.select('#chart').append('svg')
                    .attr('width', width)
                    .attr('height', height)
                    .selectAll('rect').data(bardata)
                    .enter().append('rect')
                    .style('fill', function (d, i) {
                        return colors(i);
                    })
                    .attr('width', xScale.rangeBand())
                    .attr('x', function (d, i) {
                        return xScale(i);
                    })
                    .attr('height', 0)
                    .attr('y', height)

                    .on('mouseover', function (d) {

                        tooltip.transition()
                            .style('opacity', .9)

                        tooltip.html(d)
                            .style('left', (d3.event.pageX - 35) + 'px')
                            .style('top', (d3.event.pageY - 30) + 'px')


                        tempColor = this.style.fill;
                        d3.select(this)
                            .style('opacity', .5)
                            .style('fill', 'yellow')
                    })

                    .on('mouseout', function (d) {
                        d3.select(this)
                            .style('opacity', 1)
                            .style('fill', tempColor)
                    })

                myChart.transition()
                    .attr('height', function (d) {
                        return yScale(d);
                    })
                    .attr('y', function (d) {
                        return height - yScale(d);
                    })
                    .delay(function (d, i) {
                        return i * 20;
                    })
                    .duration(1000)
                    .ease('elastic')


            },
            error: function (response) {
                console.log(response);
            }
        });
    });
});
