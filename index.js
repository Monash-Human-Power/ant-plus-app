'use strict';

let Ant = require('ant-plus');
let stick = new Ant.GarminStick3();
let bicyclePowerSensor = new Ant.BicyclePowerSensor(stick);

// Attach power data event 
bicyclePowerSensor.on('powerData', data => {
  console.log(`ID: ${data.DeviceID}, Cadence: ${data.Cadence}, Power: ${data.Power}`);
});


stick.on('startup', function () {
    console.log('Starting up');
    // Connect to the first device found
	bicyclePowerSensor.attach(0, 0);
});

if (!stick.open()) {
	console.log('Stick not found!');
}