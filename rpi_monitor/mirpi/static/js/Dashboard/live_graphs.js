Highcharts.setOptions({
    plotOptions: {
        series: {
            animation: false
        }
    }
});

var chart_1;
var chart_2;
var chart_3;
var chart_4;

var graph_ping = 10000;
var graph_interval = 60000;

var getData = $.get('/data/live');
getData.done(function(result) {

    var dataset_1 = [];
    var dataset_2 = [];
    var dataset_3 = [];
    var dataset_4 = [];
    for (var i = 0; i < (result.length - 1); i++) {
        dataset_1.push(result[i][1])
        dataset_2.push(result[i][2])
        dataset_3.push(result[i][3])
        dataset_4.push(result[i][0])
    }
    chart_1 = new Highcharts.chart('current', {
        chart: {
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: 'Hub Current Draw [A]'
        },
        credits: { enabled: false },
        boost: {
            useGPUTranslations: true,
            usePreAllocated: true
        },
        time: {
            useUTC: false
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: null
            }
        },
        tooltip: {
            crosshairs: true,
            shared: true,
            valueSuffix: 'A'
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        },
        series: dataset_1,
    });

    chart_2 = new Highcharts.chart('voltage', {
        chart: {
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: 'Hub Voltage Supply [V]'
        },
        credits: { enabled: false },
        boost: {
            useGPUTranslations: true,
            usePreAllocated: true
        },
        time: {
            useUTC: false
        },
        yAxis: {
            title: {
                text: null
            }
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        exporting: {
            enabled: false
        },
        tooltip: {
            crosshairs: true,
            shared: true,
            valueSuffix: 'V'
        },
        legend: {
            enabled: false
        },
        series: dataset_2,
    });

    chart_3 = new Highcharts.stockChart({
        chart: {
            renderTo: 'container3',
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: 'Hub Power Consumption [W]'
        },
        credits: { enabled: false },
        boost: {
            useGPUTranslations: true,
            usePreAllocated: true
        },
        time: {
            useUTC: false
        },
        rangeSelector: {
            buttons: [{
                count: 10,
                type: 'minute',
                text: '10M'
            }, {
                count: 30,
                type: 'minute',
                text: '30M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        exporting: {
            enabled: false
        },

        series: dataset_3,
    });


    chart_4 = new Highcharts.stockChart({
        chart: {
            renderTo: 'container4',
            type: 'line',
            zoomType: 'x',
        },
        title: {
            text: 'Hub Temperature [C]'
        },
        credits: { enabled: false },
        boost: {
            useGPUTranslations: true,
            usePreAllocated: true
        },
        time: {
            useUTC: false
        },
        rangeSelector: {
            buttons: [{
                count: 10,
                type: 'minute',
                text: '10M'
            }, {
                count: 30,
                type: 'minute',
                text: '30M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        exporting: {
            enabled: false
        },

        series: dataset_4,
    });


    setInterval(function() {
        updateData()
    }, graph_ping);
});

function updateData() {
    var DataUpdate = $.get('/data/update');
    DataUpdate.done(function(result) {
        for (var i = 0; i < result.length - 1; i++) {
            var shift_1 = chart_1.series[i].data.length > 100;
            var shift_2 = chart_2.series[i].data.length > 100;
            var shift_3 = chart_3.series[i].data.length > 2400;
            var shift_4 = chart_3.series[i].data.length > 500;
            for (var j = 0; j < result[i][1].length; j++) {
                chart_1.series[i].addPoint(result[i][1][j], true, shift_1);
                chart_2.series[i].addPoint(result[i][2][j], true, shift_2);
                chart_3.series[i].addPoint(result[i][3][j], true, shift_3);
                chart_4.series[i].addPoint(result[i][0][j], true, shift_4);
            }
        }
    });
}