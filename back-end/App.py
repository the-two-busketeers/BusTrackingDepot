
from flask import *
import os
import json
import readingbusesapi as busWrapper
import datetime
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
            print(jsonData)
            if jsonData["isRunning"] == "1":
                dict["running"].append(jsonData)
            else:
                dict["notRunning"].append(jsonData)
    return json.dumps(dict)

@app.route("/init", methods=["GET"])
def init():

    return GetBusJson()

if __name__ == "__main__":
    app.debug = True
    app.run(host= "0.0.0.0", port = 5000)
