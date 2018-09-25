'use strict';
var path = require('path');

// Set up ant+ 
let Ant = require('ant-plus');
let stick = new Ant.GarminStick3();
let bicyclePowerSensor = new Ant.BicyclePowerSensor(stick);

// Set up python shell
var python_script_path = path.join(__dirname, "MHP_Modelling", "Python", "rider_sim_ford_ant_plus.py");
var spawn = require('child_process').spawn;

var is_initial = true;
var prev_estimated_speed = null, prev_estimated_distance = null;

var data_count = 0;
var average_power_total = 0;

// Runs a python script which estimates the final speed and distance given power data
function calculate_estimated_speed_and_distance(){
    var average_power = average_power_total/data_count;
    data_count = 0;
    average_power_total = 0;
    var output_arguments = [python_script_path, average_power];

    if ((prev_estimated_speed != null) || (prev_estimated_distance != null)) {
        output_arguments.push(prev_estimated_speed);
        output_arguments.push(prev_estimated_distance);
    }
    var python_process = spawn('python', output_arguments);

    python_process.stdout.on('data', (data) => {
        var script_output = JSON.parse(data);
        prev_estimated_speed = script_output["estimated_speed"];
        prev_estimated_distance = script_output["estimated_distance"];
        console.log("Power: " + average_power + " W\tEstimated Speed: " + prev_estimated_speed*3.6 + " kmh\t\tEstimated Distance: " +  prev_estimated_distance + " m");
    });

    python_process.stderr.on('data', (data) => {
        console.log(data.toString());
    });
}

// Attach power data event 
bicyclePowerSensor.on('powerData', data => {
    data_count += 1;
    var bicycle_power = data.Power;
    average_power_total += bicycle_power;

    if (is_initial) {
        is_initial = false;
        setInterval(calculate_estimated_speed_and_distance, 1000);
    }
});


stick.on('startup', function () {
    // Connect to the first device found
	bicyclePowerSensor.attach(0, 0);
});

console.log('Opening ant+ USB...');
if (!stick.open()) {
	console.log('Stick not found!');
}