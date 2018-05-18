'use strict';

let Ant = require('ant-plus');
let stick = new Ant.GarminStick3();
let bicyclePowerSensor = new Ant.BicyclePowerSensor(stick);

var previous_ms = 0;
var time_count = 0;
var total_time = 0;
// Attach power data event 
bicyclePowerSensor.on('powerData', data => {
    let date = new Date();
    let current_ms = date.getTime();
    if (previous_ms == 0){
        previous_ms = current_ms;
    } else {
        let time_difference = current_ms - previous_ms;
        time_count++;
        total_time += time_difference;
        let average_time = total_time/time_count;
        console.log(`Time since last packet: ${time_difference}, Average Time: ${average_time}`);
        previous_ms = current_ms;
    }
    console.log(`ID: ${data.DeviceID}, Cadence: ${data.Cadence}, Power: ${data.Power}`);
    console.log();
});


stick.on('startup', function () {
    console.log('Starting up');
    // Connect to the first device found
	bicyclePowerSensor.attach(0, 0);
});

if (!stick.open()) {
	console.log('Stick not found!');
}