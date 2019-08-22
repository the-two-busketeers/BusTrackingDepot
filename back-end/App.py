
from flask import *
import modules.readingbusesapi as busWrapper



app = Flask(__name__)

@app.route("/init", methods=["GET"])
def init():
    return "hi"

print(__name__)
if __name__ == "__main__":
    # Making the app run on local host
    app.debug = True
    app.run(host= "0.0.0.0", port = 5000)
