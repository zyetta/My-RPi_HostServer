Highcharts.setOptions({
	plotOptions: {
		series: {
			animation: false
		}
	}
});
plot_totals_update()
var chart_234;
var totals_refresh = 1000*3600

function plot_totals_update() {
    var getData = $.get('/data/device/');
    getData.done(function(result) {
        var dataset_2 = [];
        for(var i = 1; i < result.length; i++)
        {
            dataset_2.push(result[i][0])
        }
        
        chart_234 = new Highcharts.chart({
            chart: {
                renderTo: 'totals',
                type: 'column',
                zoomType: 'xy'
            },
            credits: { enabled: false },
            boost: {
                useGPUTranslations: true,
                usePreAllocated: true
            },
            time: {
                useUTC: false
            },
            scrollbar: {
                enabled: false
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            scrollbar: {
                liveRedraw: false
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Power Consumed [W]'
                }
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                day: '%b %Y'    //ex- 01 Jan 2016
                }
            },   
            title: {
                text: 'Monthly Power Usage'
            },
            exporting: {
                enabled: false
            },
            rangeSelector: {
                selected: 1
            },
            series: dataset_2,
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 800
                    },
                    chartOptions: {
                        rangeSelector: {
                            inputEnabled: false
                        }
                    }
                }]
            },
        });
        setInterval(function () {
            plot_totals_update()
        }, totals_refresh); 

    });
}


