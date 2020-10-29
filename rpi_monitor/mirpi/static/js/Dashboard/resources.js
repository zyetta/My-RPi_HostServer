Highcharts.setOptions({
    plotOptions: {
        series: {
            animation: false
        }
    }
});
plot_resource()
var chart_12
var graph_ping4 = 60000

function plot_resource() {
    var getData = $.get('/data/device/resources');
    getData.done(function(result) {
        dataset_1 = []
        dataset_2 = []
        dataset_3 = []

        for (var i = 0; i < result.length - 1; i++) {
            dataset_1.push(result[i][0]) //CPU
            dataset_2.push(result[i][1]) //RAM
            dataset_3.push(result[i][2]) //NAME
        }

        chart_12 = new Highcharts.chart('resource_usage', {
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: 'Device Resource Usage',
                align: 'left'
            },
            xAxis: [{
                categories: dataset_3,
                crosshair: true,
                labels: {
                    enabled: false
                }
            }],
            yAxis: [{
                labels: {
                    format: '{value}',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                title: {
                    text: 'CPU Usage',
                    style: {
                        color: Highcharts.getOptions().colors[1]
                    }
                },
                opposite: true

            }, {
                gridLineWidth: 0,
                title: {
                    text: 'Memory Usage',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                },
                labels: {
                    format: '{value} MB',
                    style: {
                        color: Highcharts.getOptions().colors[0]
                    }
                }

            }],
            credits: { enabled: false },
            boost: {
                useGPUTranslations: true,
                usePreAllocated: true
            },
            tooltip: {
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 35,
                floating: true,
                backgroundColor: Highcharts.defaultOptions.legend.backgroundColor || // theme
                    'rgba(255,255,255,0.25)'
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Memory Usage',
                type: 'column',
                yAxis: 1,
                data: dataset_2,
                tooltip: {
                    valueSuffix: ' MB'
                }

            }, {
                name: 'CPU Usage',
                type: 'column',
                data: dataset_1,
                tooltip: {
                    valueSuffix: '%'
                }
            }],

            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 500
                    },
                    chartOptions: {
                        legend: {
                            floating: false,
                            layout: 'horizontal',
                            align: 'center',
                            verticalAlign: 'bottom',
                            x: 0,
                            y: 0
                        },
                        yAxis: [{
                            labels: {
                                align: 'right',

                            },
                            showLastLabel: false
                        }, {
                            labels: {
                                align: 'left',

                            },
                            showLastLabel: false
                        }, {
                            visible: false
                        }]
                    }
                }]
            }
        });
        setInterval(function() {
            plot_resource()
        }, graph_ping4);
    });
}