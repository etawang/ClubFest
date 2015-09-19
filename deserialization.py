import json

def deserialize_json (inputfile):
	with open(inputfile) as f:
		data=json.load(f)
		mapMatrix=[[0 for x in range(data["width"])] for x in range(data["height"])]
		for i in range(0, len(data["tables"])):
			x=data["tables"][i]["x"]
			y=data["tables"][i]["y"]
			mapMatrix[x][y]=data["tables"][i]["id"] 	#table number 
	return mapMatrix
	

