
from flask import *
from flask import request
# Generalised Imports
import os
import json
import datetime
import threading
import time


class BusTracker(object):
    def __init__(self, interval=30):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    def run(self):
        while True:
            for a in customBus:
                with open(os.getcwd() + "/trackBus/" + a["vehicle"] + ".json", "w") as f:
                    b = RequestBusPosition( a["vehicle"][2] )
                    jsonTime = json.load(f)
                    jsonData = {}
                    jsonData["T"] = a
                    if b:
                        jsonData["N"] = b

                    jsonTime[datetime.datetime.now()] = jsonData

                    f.write(json.dumps(jsonTime))
            time.sleep(self.interval)


# Our custom Module imports
import readingbusesapi as bus_Wrapper
import busupdater as busUpdater
import cords

busWrapper = bus_Wrapper.ReadingBusesAPI("OHYrhd9WoJ")

readingDepot = {
    "longitude": -0.981368,
    "latitude":  51.459180,
}
customBus = {}




# We create the BusUpdate class which we will run on another thread so
#that it does not interacts with the flask server

example = busUpdater.BusUpdater()
busTracker = BusTracker()

app = Flask(__name__)

@app.route("/init", methods=["GET"])
def init():
    dict  = bus_Wrapper.GetBusJson()
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
    dict["observed"] = datetime.datetime.now()
    customBus[form["vehicle"]] = dict
    return ""

@app.route("/fetchCBus/<busID>")
def fetchBus(busID):
    if (busID in customBus):
        response = jsonify(customBus[busID])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        dict = busWrapper.RequestBusPosition(busID)
        response = jsonify(dict)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify({})

@app.route("/fetchC/<busID>")
def fetchC(busID):
    if ("T" + busID) in customBus:
        a = customBus["T" + busID]
        b = busWrapper.RequestBusPosition( busID )
        jsonData = {}
        jsonData["T"] = a
        if b:
            jsonData["N"] = b
        response = jsonify(jsonData)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify({})

if __name__ == "__main__":
    app.debug = True
    app.run(host= "0.0.0.0", port=os.environ["PORT"])
