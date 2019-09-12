
from flask import *
import os
import json
import readingbusesapi as busWrapper
import datetime
import threading
import time


class BusUpdater(object):

    def __init__(self, interval=30):

        self.interval = interval

        self.busWrapper = busWrapper.ReadingBusesAPI("OHYrhd9WoJ")

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            buses = {}
            aBuses = self.busWrapper.Call("Buses", {})

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
                        jsonData["service"] = busData["service"]
                        jsonData["observed"] = busData["observed"]
                        jsonData["isRunning"] = "1"

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
                # Do a check to see if the observed date is over a month old
                # if it is move it to the oldService json
                dict["notRunning"].append(jsonData)
    return dict

@app.route("/init", methods=["GET"])
def init():
    dict  = GetBusJson()
    response = jsonify(dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.debug = True
    app.run(host= "0.0.0.0", port = 5000)
