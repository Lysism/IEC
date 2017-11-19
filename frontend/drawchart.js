var DATA_COUNT = 16;
var MIN_XY = -150;
var MAX_XY = 100;

var presets = window.chartColors;
var utils = Samples.utils;

utils.srand(110);

function colorize(opaque, context) {
    var value = context.dataset.data[context.dataIndex];
    var x = value.x / 100;
    var y = value.y / 100;
    var r = x < 0 && y < 0 ? 250 : x < 0 ? 150 : y < 0 ? 50 : 0;
    var g = x < 0 && y < 0 ? 0 : x < 0 ? 50 : y < 0 ? 150 : 250;
    var b = x < 0 && y < 0 ? 0 : x > 0 && y > 0 ? 250 : 150;
    var a = opaque ? 1 : 0.5 * value.v / 1000;

    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
}

function generateData() {
    var data = [];
    var i;

    for (i = 0; i < DATA_COUNT; ++i) {
        data.push({
            x: utils.rand(MIN_XY, MAX_XY),
            y: utils.rand(MIN_XY, MAX_XY),
            v: utils.rand(100, 1000)
        });
    }

    return data;
}

data = JSON.parse(`
    {
        "plane": [
            {
                "x": 100,
                "y": 200,
                "v": 100
            }
        ],
        "sats": [
            {
                "x": 100,
                "y": 200,
                "v": 800
            },
            {
                "x": -100,
                "y": 300,
                "v": 540
            },
            {
                "x": 500,
                "y": 80,
                "v": 500
            }
        ],
        "intersections": [
            {
                "x": 80,
                "y": 20,
                "v": 100
            },
            {
                "x": -100,
                "y": 320,
                "v": 100
            },
            {
                "x": 500,
                "y": 80,
                "v": 100
            }
        ]
    }

    `)

var data = {
    datasets: [{
        data: data.plane
    }, {
        data: data.sats
    }, {
        data: data.intersections
    }]
};


var options = {
    aspectRatio: 1,
    legend: false,
    tooltips: false,

    elements: {
        point: {
            backgroundColor: function(context) {
                context.datasetIndex == 0 ? '#FFFFFF' : '#ABCABC'
            },

            borderColor: function(context) {
                context.datasetIndex == 0 ? '#FFFFFF' : '#ABCABC'
            },

            borderWidth: function(context) {
                return Math.min(Math.max(1, context.datasetIndex + 1), 8);
            },

            hoverBackgroundColor: 'transparent',

            hoverBorderColor: function(context) {
                return utils.color(context.datasetIndex);
            },

            hoverBorderWidth: function(context) {
                var value = context.dataset.data[context.dataIndex];
                return Math.round(8 * value.v / 1000);
            },

            radius: function(context) {
                var value = context.dataset.data[context.dataIndex];
                var size = context.chart.width;
                var base = Math.abs(value.v) / 1000;
                return (size / 24) * base;
            }
        }
    },
    // Container for pan options
    pan: {
        // Boolean to enable panning
        enabled: false,

        // Panning directions. Remove the appropriate direction to disable 
        // Eg. 'y' would only allow panning in the y direction
        mode: 'xy',
        rangeMin: {
            // Format of min pan range depends on scale type
            x: null,
            y: null
        },
        rangeMax: {
            // Format of max pan range depends on scale type
            x: null,
            y: null
        }
    },

    // Container for zoom options
    zoom: {
        // Boolean to enable zooming
        enabled: false,

        // Enable drag-to-zoom behavior
        drag: false,

        // Zooming directions. Remove the appropriate direction to disable 
        // Eg. 'y' would only allow zooming in the y direction
        mode: 'xy',
        rangeMin: {
            // Format of min zoom range depends on scale type
            x: null,
            y: null
        },
        rangeMax: {
            // Format of max zoom range depends on scale type
            x: null,
            y: null
        }
    }
};

var chart = new Chart('canvas', {
    type: 'bubble',
    data: data,
    options: options
});

function randomize() {
    chart.data.datasets.forEach(function(dataset) {
        dataset.data = generateData()
    });
    chart.update();
}

function addDataset() {
    chart.data.datasets.push({
        data: generateData()
    });
    chart.update();
}

function removeDataset() {
    chart.data.datasets.shift();
    chart.update();
}