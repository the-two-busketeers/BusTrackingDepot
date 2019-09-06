import json

with open("bus_fleetID_list.txt", "r") as file:
	fleetIDs = file.readlines()
	fleetIDs = [x.strip() for x in fleetIDs]
	print(fleetIDs)


for ID in fleetIDs:
	dictionary = {
		"observed": "2019-08-22 18:46:13",
		"vehicle": "1104",
		"isRunning": "0",
		"service": str(ID),
		"returnTime": "2019-08-22 19:46:13"
	}
	file = open(str(ID) + ".json", "w")
	file.write(json.dumps(dictionary))
	file.close()