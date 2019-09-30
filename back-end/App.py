
from flask import *
from flask import request
# Generalised Imports
import os
import json
import datetime
import threading
import time

# Our custom Module imports
import readingbusesapi as busWrapper
import cords

busWrapper = busWrapper.ReadingBusesAPI("OHYrhd9WoJ")

readingDepot = {
    "longitude": -0.981368,
    "latitude":  51.459180,
}

# We create the BusUpdate class which we will run on another thread so
#that it does not interacts with the flask server
class BusUpdater(object):

    def __init__(self, interval=30):

        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            buses = {}
            aBuses = busWrapper.Call("Buses", {})

            for data in aBuses:
                buses[data["vehicle"]] = data
            for files in os.listdir( os.getcwd() + "/buses"):
                if files.endswith(".json"):
                    filename = os.getcwd() + "/buses/" + files
                    jsonFile = open(filename, 'r')
                    jsonData = json.load(jsonFile)

                    vehicle = jsonData["vehicle"]
                    if vehicle in buses:
                        busData = buses[vehicle]
                        if busData == None:
                            continue
                        if busData["service"] == "":
                            if jsonData["service"] != "":
                                jsonData["lastService"] = jsonData["service"]
                        jsonData["service"] = busData["service"]
                        jsonData["observed"] = busData["observed"]
                        jsonData["isRunning"] = "1"
                        jsonData["latitude"] = busData["latitude"]
                        jsonData["longitude"] = busData["longitude"]
                        jsonData["distance"] = cords.LatLongToDistance(readingDepot["latitude"], readingDepot["longitude"], float(busData["latitude"]), float(busData["longitude"]))
                        buses[vehicle] = None
                    else:
                        jsonData["isRunning"] = "0"
                        buses[vehicle] = None

                    jsonFile.close()
                    jsonFile = open(filename, "w")
                    jsonFile.write(json.dumps(jsonData))
                    jsonFile.close()
            for da in buses:
                data = buses[da]
                if data != None:
                    jsonData = {}
                    jsonData["observed"] = data["observed"]
                    jsonData["vehicle"] = data["vehicle"]
                    jsonData["isRunning"] = "1"
                    jsonData["service"] = data["service"]
                    jsonData["returnTime"] = "2019-08-22 19:46:13"
                    jsonData["latitude"] = busData["latitude"]
                    jsonData["longitude"] = busData["longitude"]
                    jsonData["distance"] = cords.LatLongToDistance(readingDepot["latitude"], readingDepot["latitude"], float(busData["latitude"]), float(busData["longitude"]))

                    with open(os.getcwd() + "/buses/" + data["vehicle"] + ".json", 'w') as f:
                        f.write(json.dumps(jsonData))
            time.sleep(self.interval)

example = BusUpdater()

app = Flask(__name__)

def GetBusJson():
    dict = {
        "running" : [],
        "notRunning" : [],
        "oldService" : [],
    }
    time = datetime.datetime.now()

    for files in os.listdir( os.getcwd() + "/buses"):
        if files.endswith(".json"):
            jsonFile = open(os.getcwd() + "/buses/" + files)
            jsonData = json.load(jsonFile)
            if jsonData["isRunning"] == "1":
                dict["running"].append(jsonData)
            else:
                if (time - datetime.datetime.fromisoformat(jsonData["observed"])).days > 30:
                    dict["oldService"].append(jsonData)
                else:
                    dict["notRunning"].append(jsonData)
    return dict

@app.route("/init", methods=["GET"])
def init():
    dict  = GetBusJson()
    response = jsonify(dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route("/track/<vehicleID>", methods=["GET"])
def track(vehicleID):
    dict = busWrapper.RequestBusPosition(vehicleID)
    response = jsonify(dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
def serve_index():
    return redirect("/static/index.html")

@app.route("/<html_file>", methods=["GET"])
def serve_html(html_file):
    return render_template(html_file)

@app.route("/<css_file>")
def serve_css(css_file):
    return render_template(css_file)

@app.route("/<image>")
def serve_image(image):
    return send_from_directory(image)

@app.route("/<js_file>")
def serve_javascript(js_file):
    return send_from_directory(js_file)

@app.route("/getAllBus")
def getAllBus():
    Dict = []
    for files in os.listdir( os.getcwd() + "/buses"):
        if files.endswith(".json"):
            jsonFile = open(os.getcwd() + "/buses/" + files)
            jsonData = json.load(jsonFile)
            Dict.Append(jsonData["vehicle"])
    with open() as f:
        for a in Dict:
            f.write(a + ",\n")

customBus = {}
@app.route('/addBus', methods=["POST"])
def addBus():
    form = request.get_json()
    dict = {}
    dict["service"] = form["service"]
    dict["vehicle"] = form["vehicle"]
    dict["isRunning"] = form["isRunning"]
    dict["latitude"] = form["latitude"]
    dict["longitude"] = form["longitude"]
    dict["customBus"] = "1"
    dict["observed"] = datetime.date.today()
    customBus[form["service"]] = dict

@app.route("/fetchCBus/<busID>")
def fetchBus(busID):
    if (busID in customBus):
        response = jsonify(dict)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        dict = busWrapper.RequestBusPosition(busID)
        response = jsonify(dict)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify({})

if __name__ == "__main__":
    app.debug = True
    app.run(host= "0.0.0.0", port=os.environ["PORT"])
