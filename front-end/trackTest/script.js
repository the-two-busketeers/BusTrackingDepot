
const busInput = document.getElementById("busInput");
const start = document.getElementById("start");
const last = document.getElementById("last");
const middle = document.getElementById("middle");

const myRange = document.getElementById("myRange");

var oldBus = L.marker([0, 0], {icon: busIcon} ).addTo(mymap);
var newBus = L.marker([0, 0.0005], {icon: busIcon2} ).addTo(mymap);
var startTime;
var lastTime;

var middleTime;
var date;


function loadBus() {
	// Fetch all the bus data
	// wait until times are valid

	// load valid times
}


function setStartTime(event) {
	startTime =Math.round(Date.parse(event.target.value));
	start.textContent = startTime;
}

function setLastTime(event) {
	lastTime = Math.round(Date.parse(event.target.value));
	last.textContent = lastTime;
}

function calcBusPosition(id) {
}

function calcBusTime() {

	middleTime = startTime + (lastTime-startTime)*(myRange.value/1000)
	date = new Date(middleTime);

	middle.textContent = middleTime + " "+ date.getDate() +"/"+ (date.getMonth()+1) + "/" + date.getFullYear()
}

function doConvert(event){
  unix.textContent=Math.round(Date.parse(event.target.value)/1000);
}
