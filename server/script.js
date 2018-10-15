var socket = io();
var power_chart_element = document.getElementById("powerChart");
var power_chart = new Chart(power_chart_element, {
    type: 'line',
    data: {
        labels: ["Power (W)"],
        datasets: [{
            data: [],
            borderWidth: 1
        }]
    },
    options: {
        title: {
          display: true,
          text: 'Power vs Estimated Distance'
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'Estimated Distance (m)'
            }
          }]
        },
        elements: {
          point: {
            radius: 0
          }
        },
        legend: {
          display:false
        }
    }
});

var speed_distance_chart_element = document.getElementById("speedDistanceChart");
var speed_distance_chart = new Chart(speed_distance_chart_element, {
    type: 'line',
    data: {
        labels: ["Speed (km/h)"],
        datasets: [{
            data: [],
            borderWidth: 1
        }]
    },
    options: {
        title: {
          display: true,
          text: 'Estimated Speed vs Estimated Distance'
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'Estimated Distance (m)'
            }
          }]
        },
        elements: {
          point: {
            radius: 0
          }
        },
        legend: {
          display:false
        }
    }
});

socket.on('data', (data) => {
    // Add incoming data to the appropriate graphs
    addData(power_chart, data["estimated_distance"].toFixed(2), data["power"]);
    addData(speed_distance_chart, data["estimated_distance"].toFixed(2), data["estimated_speed"]*3.6);
});

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}