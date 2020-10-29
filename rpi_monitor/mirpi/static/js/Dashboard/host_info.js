Highcharts.setOptions({
	plotOptions: {
		series: {
			animation: false
		}
	}
});
var chart_1221
var graph_ping2 = 10000

var getData = $.get('/data/stats');
getData.done(function(result) {
    chart_1221 = new Highcharts.chart('client_state', {
        chart: {           
            type: 'column'
        },
        title: {
            text: 'Device States'
        },
        legend: {
            enabled: false
        },
        credits: { enabled: false },
        boost: {
            useGPUTranslations: true,
            usePreAllocated: true
        }, 
        xAxis: {
            type: 'category',
            categories: [
                'Active',
                'Idle',
                'Powered Off'                
            ],
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Amount of Devices'
            }
        },
        exporting: {
            enabled: false
        },
        series: [
            {
                colorByPoint: true,
                data: [
                    {
                        name: 'Active',
                        y: result[0][0]['Active'],
                        color: 'rgba(60,179,113, 0.6)',
                    },
                    {
                        name: 'Idle',
                        y: result[0][0]['Idle'],
                        color: 'rgba(255,99,71,0.6)',
                    },
                    {
                        name: 'Powered Off',
                        y: result[0][0]['Off'],
                        color: 'rgba(220,20,60, 0.6)',
                    }
                ]
            }
        ]
    });

    setInterval(function () {
        update_host()
    }, graph_ping2); 
});


function update_host() {
    var DataUpdate = $.get('/data/stats');
    DataUpdate.done(function(result) {
        chart_1221.series[0].update({
        data : [
            {
                y: result[0][0]['Active'],
            },
            {
                y: result[0][0]['Idle'],
            },
            {
                y: result[0][0]['Off'],
            }
        ]
        }, true)   
    });
}