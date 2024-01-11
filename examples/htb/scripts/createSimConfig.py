import json, os

FDusers = 3

sampleDict = {
    "id": "sample",
    "parentId": "NULL",
    "rate": 0,
    "ceil": 0,
    "burst": 2000,
    "cburst": 2000,
    "level": 0,
    "quantum": 1500,
    "mbuffer": 60
}

data = []


fh = open("my_json.json", "a+")

for user in range(FDusers):
    userDict = sampleDict.copy()
    userDict["id"] = "leafhostFDO" + str(user)
    data.append(userDict)
    print(data)

fh.write(json.dumps(data))
fh.close