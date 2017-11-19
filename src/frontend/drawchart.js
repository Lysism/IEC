var DATA_COUNT = 16;
var MIN_XY = -150;
var MAX_XY = 100;

// var presets = window.chartColors;
var utils = Samples.utils;

utils.srand(110);

function requestData(inputdata) {
    fetch('/', {
        data: inputdata
    }).then(res => {
        chart.data = loadData(res.body);
        chart.update();
    });
}

function loadData(json) {
    var data = JSON.parse(`
    {
        "plane": [
            {
                "x": 100,
                "y": 10,
                "v": 100
            }
        ],
        "sats": [
            {
                "x": 400,
                "y": 100,
                "v": 100
            },
            {
                "x": 800,
                "y": 100,
                "v": 100
            },
            {
                "x": 1200,
                "y": 100,
                "v": 100
            }
        ],
        "all_intersections": [
            {
                "x": 0,
                "y": 200,
                "v": 30
            },
            {
                "x": 100,
                "y": 200,
                "v": 100
            },
            {
                "x": 200,
                "y": 200,
                "v": 100
            }
        ],
        "good_intersections": [
            {
                "x": 0,
                "y": 300,
                "v": 100
            },
            {
                "x": 100,
                "y": 300,
                "v": 100
            },
            {
                "x": 200,
                "y": 300,
                "v": 100
            }
        ]
    }
    `);

    // Load JSON from

    return {
        datasets: [
            {
                data: data.plane
            },
            {
                data: data.sats
            },
            {
                data: data.all_intersections
            },
            {
                data: data.good_intersections
            }
        ]
    };
}

Chart.defaults.derivedBubble = Chart.defaults.bubble;
Chart.controllers.GPS = Chart.controllers.bubble.extend({
    name: "GPS",
    draw: function () {
        Chart.controllers.bubble.prototype.draw.call(this, ease);
        var line = [0, 0, 100, 100];
        this.chart.ctx.beginPath();
        this.chart.ctx.moveTo(line[0], line[1])
        this.strokeStyle = '#000';
        this.chart.ctx.lineTo(line[2], line[3]);
        this.chart.ctx.stroke();
    }
})

var options = {
    aspectRatio: 1,
    legend: false,
    tooltips: false,

    elements: {
        point: {
            backgroundColor: function(context) {
                return utils.color(context.datasetIndex);
            },

            borderColor: function(context) {
                return utils.color(context.datasetIndex);
            },

            borderWidth: function(context) {
                return Math.min(Math.max(1, context.datasetIndex + 1), 8);
            },

            hoverBackgroundColor: "transparent",

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
                return size / 24 * base;
            }
        }
    },
    // Container for pan options
    pan: {
        // Boolean to enable panning
        enabled: false,

        // Panning directions. Remove the appropriate direction to disable
        // Eg. 'y' would only allow panning in the y direction
        mode: "xy",
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
        mode: "xy",
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

var chart = new Chart("canvas", {
    type: "bubble",
    data: loadData(),
    options: options
    });

chart.data = loadData();
chart.update();



