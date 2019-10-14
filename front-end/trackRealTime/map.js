
var lat = 51.459180
var lng = -0.981368

// Making a map and tiles
// Setting a higher initial zoom to make effect more obvious
const mymap = L.map('busMap').setView([0, 0], 17);
const attribution ='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const tiles = L.tileLayer(tileUrl, { attribution });
tiles.addTo(mymap);

const busIcon = L.divIcon({
	//iconUrl: 'images/busIcon.png',
	iconSize: [16, 16],
	iconAnchor: [8, 8],
	className: "busIcon"
});

const busIcon2 = L.divIcon({
	//iconUrl: 'images/busIcon.png',
	iconSize: [16, 16],
	iconAnchor: [8, 8],
	className: "busIcon2"
});
