import threading
import time

class BusTracker(object):
    def __init__(self, service, interval=30):
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
