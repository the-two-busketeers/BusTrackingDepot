import threading
import time

import cords
import datetime
import os
import json

import readingbusesapi as bus_Wrapper
busWrapper = bus_Wrapper.ReadingBusesAPI("OHYrhd9WoJ")

readingDepot = {
    "longitude": -0.981368,
    "latitude":  51.459180,
}

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
