
from flask import *
import os
import json
import readingbusesapi as busWrapper

app = Flask(__name__)

def GetBusJson():
    dict = []
    for files in os.listdir( os.getcwd() + /"/buses"):
        if files.endswith(".json"):
            jsonFile = open(files)
            jsonData = json.load(jsonFile)
            dict.Append(jsonData)
    return dict


@app.route("/init", methods=["GET"])
def init():

    return GetBusJson()
print(__name__)
if __name__ == "__main__":
    # Making the app run on local host
    app.debug = True
    app.run(host= "0.0.0.0", port = 5000)
