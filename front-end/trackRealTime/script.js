
const busInput = document.getElementById("busInput");

var oldBus = L.marker([0, 0], {icon: busIcon} ).addTo(mymap);
var newBus = L.marker([0, 0.0005], {icon: busIcon2} ).addTo(mymap);
var busService;
var lastTime;

function loadBus() {
	// Fetch all the bus data
	// wait until times are valid

	// load valid times
	busService = busInput.value;
}


const api_url = 'https://bus-tracker-reading-buses.herokuapp.com/track/';
//const api_url = "http://192.168.152.155:5000/track/"+ vehicleID;
async function getBus() {
	const response = await fetch(api_url + busService);
	const data = await response.json();

	var latitude = data["latitude"];
	var longitude = data["longitude"];
	console.log(data);
	mymap.setView([latitude, longitude], mymap.getZoom());
	marker.setLatLng([latitude, longitude]);
	busIconE = document.getElementsByClassName("busIcon")[0]

	//marker.setHeading(data["bearing"])

	bearing = data["bearing"];
	busIconE.style.transform = busIconE.style.transform + "rotate( " + (bearing-45).toString() + "deg)"
	//busIconE.style.transform = busIconE.style.transform + "rotate( " + (data["bearing"]).toString() + "deg)"
	//busIconE.innerHTML = "<div style ='background: #FF;'> <p> | </p></div>"
}
getBus();
setInterval(getBus, 1000*10);
