import json, os, sys


sampleDict = {
    "id": "sample",
    "parentId": "NULL",
    "rate": 0,
    "ceil": 0,
    "burst": 2000,
    "cburst": 2000,
    "level": 1,
    "quantum": 1500,
    "mbuffer": 60
}
def fillJSON(numVID, numLVD, numFDO, numSSH, numVIP):
    data = []

    fh = open(str(name) + ".json", "a+")

    root = sampleDict.copy()
    root["id"] = "root"
    root["rate"] = 50000
    root["ceil"] = 50000
    data.append(root)


    for FD in range(numFDO):
        tempDict = sampleDict.copy()
        tempDict["id"] = "leafhostFDO" + str(FD)
        tempDict["parentId"] = "root"
        tempDict["rate"] = 5000
        tempDict["ceil"] = 10000
        tempDict["burst"] = 2000
        tempDict["cburst"] = 2000
        tempDict["level"] = 0
        tempDict["priority"] = 0
        tempDict["queueNum"] = FD
        
        data.append(tempDict)

    fh.write(json.dumps(data))
    fh.close

name = sys.argv[1]
slices = sys.argv[2]

print(name)
if os.path.isfile("./" + str(name) + ".json"):
    print("Config already exists with this name!")

else:
    numVID = int(name.split('VID')[1].split('_LVD')[0])
    numLVD = int(name.split('LVD')[1].split('_FDO')[0])
    numFDO = int(name.split('FDO')[1].split('_SSH')[0])
    numSSH = int(name.split('SSH')[1].split('_VIP')[0])
    numVIP = int(name.split('VIP')[1].split('/')[0])

    fillJSON(numVID, numLVD, numFDO, numSSH, numVIP)