let sortType = "none"

const pSBC=(p,c0,c1,l)=>{
	let r,g,b,P,f,t,h,i=parseInt,m=Math.round,a=typeof(c1)=="string";
	if(typeof(p)!="number"||p<-1||p>1||typeof(c0)!="string"||(c0[0]!='r'&&c0[0]!='#')||(c1&&!a))return null;
	if(!this.pSBCr)this.pSBCr=(d)=>{
		let n=d.length,x={};
		if(n>9){
			[r,g,b,a]=d=d.split(","),n=d.length;
			if(n<3||n>4)return null;
			x.r=i(r[3]=="a"?r.slice(5):r.slice(4)),x.g=i(g),x.b=i(b),x.a=a?parseFloat(a):-1
		}else{
			if(n==8||n==6||n<4)return null;
			if(n<6)d="#"+d[1]+d[1]+d[2]+d[2]+d[3]+d[3]+(n>4?d[4]+d[4]:"");
			d=i(d.slice(1),16);
			if(n==9||n==5)x.r=d>>24&255,x.g=d>>16&255,x.b=d>>8&255,x.a=m((d&255)/0.255)/1000;
			else x.r=d>>16,x.g=d>>8&255,x.b=d&255,x.a=-1
		}return x};
	h=c0.length>9,h=a?c1.length>9?true:c1=="c"?!h:false:h,f=pSBCr(c0),P=p<0,t=c1&&c1!="c"?pSBCr(c1):P?{r:0,g:0,b:0,a:-1}:{r:255,g:255,b:255,a:-1},p=P?p*-1:p,P=1-p;
	if(!f||!t)return null;
	if(l)r=m(P*f.r+p*t.r),g=m(P*f.g+p*t.g),b=m(P*f.b+p*t.b);
	else r=m((P*f.r**2+p*t.r**2)**0.5),g=m((P*f.g**2+p*t.g**2)**0.5),b=m((P*f.b**2+p*t.b**2)**0.5);
	a=f.a,t=t.a,f=a>=0||t>=0,a=f?a<0?t:t<0?a:a*P+t*p:0;
	if(h)return"rgb"+(f?"a(":"(")+r+","+g+","+b+(f?","+m(a*1000)/1000:"")+")";
	else return"#"+(4294967296+r*16777216+g*65536+b*256+(f?m(a*255):0)).toString(16).slice(1,f?undefined:-2)
}

var busJson = {}
function syncBusData(bool, noSort) {
	$.ajax({
		url: "https://bus-tracker-reading-buses.herokuapp.com/init",
		//url: "http://192.168.152.155:5000/init",
		type: "GET",
		dataType: "json",
		crossDomain: true,
		success: function (json) {
				busesJson = json;
				if (bool === true) {

                  var removeDivs = document.querySelectorAll("#removeDiv")
                  for (let i = 0; i < removeDivs.length; i++) {
                      let div = removeDivs.item(i);

                      div.parentNode.removeChild(div)
                  }


					for (var key in json) {
						var element = document.getElementById(key)
						var dict = json[key]
						for(let i = 0; i < dict.length; i++){
							var bus = dict[i]
							busJson[bus.vehicle] = bus;
							busJson[bus.vehicle].element = CreateBusAccordion(bus, element)
						}
					}
				}
				else {
					for (var key in json) {
							var element = document.getElementById(key)
							var dict = json[key]
							for(let i = 0; i < dict.length; i++){
								var bus = dict[i]
								if (bus.vehicle in busJson) {
									var ele = busJson[bus.vehicle].element
									busJson[bus.vehicle] = bus;
									busJson[bus.vehicle].element = ele
									UpdateBusAccordion(bus, element)
								}
								else {
									busJson[bus.vehicle] = bus;
									busJson[bus.vehicle].element = CreateBusAccordion(busJson, element)
								}
							}
						}

				}
				if (noSort !== true) {
					busSort(sortType)
				}
			},
			error: function (res) { console.log(res); }
		}
	)
}

function SetBusData(acc, panel, json) {

	var service = "noService"

	if (json.service in busColors) {
		service = json.service
	}
	else {
		if (json.lastService && json.lastService in busColors) {
			service = json.lastService
		}
	}
	acc.innerHTML = json.vehicle;
	acc.style.backgroundImage = "linear-gradient(90deg," + busColors[service] + "," + busColors[service] + "," + busColors[service] + "," + busColors[service] + "," + pSBC ( -0.4, busColors[service] ) + ")"
	panel.innerHTML = "<br>Service: " + json.service + "<br>" + "Last Recorded Service: " + ( (json.lastService !== "undefined" && json.lastService) || "");
	panel.innerHTML = panel.innerHTML + "<br>Last Seen: " + json.observed
	if (json["isRunning"] === "1") {
	  var distance = parseInt(json.distance[0]);
	  if (distance >= 1000) {
	    panel.innerHTML = panel.innerHTML + "<br>Distance: " + distance/1000 + "km";
	  }
	  else {
	    panel.innerHTML = panel.innerHTML + "<br>Distance: " + distance + "m";
	  }
		panel.innerHTML = panel.innerHTML + "<br><br>"
		if (json.distance[0] <= 200) {
			acc.innerHTML = acc.innerHTML + " Leaving/Entering"
		}
	}
	else{
		panel.innerHTML = panel.innerHTML + "<br><br>"
	}
	if (json["isRunning"] === "1") {
		var button = document.createElement("button");
		button.innerText = "Track Me!";
		button.setAttribute("onclick", "window.location.href='track.html?vehicleID=" + json.vehicle +"'");
		panel.appendChild(button);
		panel.innerHTML = panel.innerHTML + "<br><br>"
	}
}

function UpdateBusAccordion(busD, par) {
	var acc = busD.element.children[0]
	var panel = busD.element.children[1]
	SetBusData(acc, panel, busD);
	par.appendChild(busD.element);
}

function CreateBusAccordion(json, element) {
	var mainDiv = document.createElement("div");
	element.appendChild(mainDiv);
	var acc = document.createElement("button");
	var panel = document.createElement("div");


	SetBusData(acc, panel, json);


	panel.classList.add("panel");

	acc.classList.add("accordion");
	mainDiv.appendChild(acc);
	mainDiv.appendChild(panel);
	acc.addEventListener("click", function() {
		this.classList.toggle("active");
		var panel = this.nextElementSibling;
		if (panel.style.maxHeight){
			panel.style.maxHeight = null;
		} else {
			panel.style.maxHeight = panel.scrollHeight + "px";
		}
	});
	return mainDiv;
}

function busSearch(match, key) {
	for (var vehicle in busJson) {
		var bus = busJson[vehicle]
		if (match == "") {
			bus.element.style.display = "";
			continue;
		}
		if ( key in bus && (bus[key].toUpperCase().includes(match.toUpperCase()) || bus[key].includes(match.toLowerCase()))) {
			bus.element.style.display = "";
		}
		else {
			bus.element.style.display = "none";
		}
	}
}
var sorting = {
	"none": function() {
		syncBusData(false, true)
	},
	"service": function() {
		var busLists = document.getElementsByClassName("buslist");

		// for (var i = 0; i < busLists.length; i++) {
		//     var buses = []
		//     for (var j = 0; j < busLists[i].children.length; j++) {
		//         buses.push(busLists[i][j])
		//     }
		// }
		for (let i = 0; i < busLists.length; i++) {
			let busList = Array.prototype.slice.call(busLists[i].children).sort(function(a, b) {
				if (a == "" || a == "asd") a = "0";
				a = parseInt(a.children[1].innerText.split(" ")[1].split("\n")[0].replace(/[A-Za-z]/g, ""));

        if (b == "" || b == "asd") b = "0"
				b = parseInt(b.children[1].innerText.split(" ")[1].split("\n")[0].replace(/[A-Za-z]/g, ""))

				return a > b;
			})

			for (let j = 0; j < busList.length; j++) {
				let parent = busList[j].parentNode
				let detachedItem = parent.removeChild(busList[j])
				parent.append(detachedItem)
			}
		}
	},
	"numerical": function() {
		var busLists = document.getElementsByClassName("buslist");

		// for (var i = 0; i < busLists.length; i++) {
		//     var buses = []
		//     for (var j = 0; j < busLists[i].children.length; j++) {
		//         buses.push(busLists[i][j])
		//     }
		// }
		for (let i = 0; i < busLists.length; i++) {
			let busList = Array.prototype.slice.call(busLists[i].children).sort(function(a, b) {
				a = parseInt(a.textContent.replace(/[A-Za-z:]/g, "").split(" ")[0]);
				b = parseInt(b.textContent.replace(/[A-Za-z:]/g, "").split(" ")[0]);

				return a > b;
			})

			for (let j = 0; j < busList.length; j++) {
				let parent = busList[j].parentNode
				let detachedItem = parent.removeChild(busList[j])

				parent.append(detachedItem)
			}
		}
	},
	"distance" : function() {
		var busLists = document.getElementsByClassName("buslist");

		// for (var i = 0; i < busLists.length; i++) {
		//     var buses = []
		//     for (var j = 0; j < busLists[i].children.length; j++) {
		//         buses.push(busLists[i][j])
		//     }
		// }
			let busList = Array.prototype.slice.call(busLists[0].children).sort(function(a, b) {
				a = parseInt( busJson[a.children[0].innerText.split(" ")[0]].distance[0])
				b = parseInt(busJson[b.children[0].innerText.split(" ")[0]].distance[0])

				return a - b
			})

			for (let j = 0; j < busList.length; j++) {
				let parent = busList[j].parentNode
				let detachedItem = parent.removeChild(busList[j])

				parent.append(detachedItem)
			}
	}
};

function busSort(value) {
	if (value in sorting) {
		sortType = value
		sorting[value]();
	}
}

setInterval(syncBusData, 1000 * 30);
syncBusData(true, true);

// add selecting from the service
// searching in the search box
//includes(substring))
var search = document.getElementById("search")
var searchBox = document.getElementById("select-box")
search.addEventListener("keyup", function(e) {
	busSearch(search.value, searchBox.options[searchBox.selectedIndex].value);
})

searchBox.addEventListener("click", function(e) {
	busSearch(search.value, searchBox.options[searchBox.selectedIndex].value);
} )

var grid_container = document.getElementsByClassName("grid-container")[0]

if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
    $(".mobile-load").attr("style", "padding-right: 10%; display:;");
    $(".desktop-load").attr("style", "padding-top: 15%; display: none");
    $("body").attr("style", "background-repeat: repeat-y; height: 100%; width: 100%; overflow-y: hidden; overflow-x: hidden")
    $(".grid-container").attr("style", "display: block; width: 50vw; transform: translateX(24vw)")
    var headers = $(".grid-container #header");
    for (let i = 0; i < headers.length; i++) {
    $(".grid-container .buslist").attr("style", "display: none")
    headers[i].setAttribute("style", "border-bottom-left-radius: 15px; border-bottom-right-radius: 15px")
    headers[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display == ""){
            panel.setAttribute("style", "display: none")
            headers[i].setAttribute("style", "border-bottom-left-radius: 15px; border-bottom-right-radius: 15px")
          } else {
            panel.setAttribute("style", "display: ; height: 50vh; max-height: 50vh;")
            headers[i].setAttribute("style", "border-bottom-left-radius: 0; border-bottom-right-radius: 0")
        }
    });
  }
}

