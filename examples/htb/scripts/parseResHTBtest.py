import pandas
import csv
import statistics
# from termcolor import colored
import sys
import os
import matplotlib
import matplotlib.pyplot as plt

maxSimTime = 15
DEBUG = 0

font = {'weight' : 'normal',
        'size'   : 40}

matplotlib.rc('font', **font)
matplotlib.rc('lines', linewidth=2.0)
matplotlib.rc('lines', markersize=8)

downlink = ['Downlink', 'rxPkOk:vector(packetBytes)']
uplink = ['Uplink', 'txPk:vector(packetBytes)']

def makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit):
    scenName = str(testName) + '_' + str(numCLI)
    for nodeType,numNodesType in zip(nodeTypes, nodeSplit):
        scenName += '_' + nodeType.replace('host','') + str(numNodesType)
    return scenName
    # return str(testName) + '_' + str(numCLI) + '_VID' + str(nodeSplit[0]) + '_FDO' + str(nodeSplit[1]) + '_SSH' + str(nodeSplit[2]) + '_VIP' + str(nodeSplit[3])

def makeNodeIdentifier(nodeType, nodeNum):
    if nodeNum < 0:
        return nodeType
    else:
        return nodeType + str(nodeNum)

# Function that imports node information into a dataframe
#   - testName - name of the test
#   - numCLI - total number of clients in the test
#   - nodeSplit - number of nodes running certain applications in the test
#       [numVID, numFDO, numSSH, numVIP]
#   - nodeType - type of the node to import (String), curr. used
#       hostVID, hostFDO, hostSSH, hostVIP, links, serverSSH
#   - nodeNum - number of the node to import, omitted if -1
def importDF(testName, numCLI, nodeTypes, nodeSplit, nodeType, nodeNum):
    # File that will be read
    fullScenarioExportName = makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)
    fileToRead = '../results/' + str(testName) + '/' + fullScenarioExportName + '/vectors/' + fullScenarioExportName + '_' + makeNodeIdentifier(nodeType, nodeNum) + '_vec.csv'
    # '../' + ^^^
    print("Importing: " + fileToRead)
    # Read the CSV
    tabledf = pandas.read_csv(fileToRead)
    #print(tabledf)
    return tabledf

def filterDFType(df, filterType):
    return df.filter(like=filterType)

def getFilteredDFtypeAndTS(df, filterType):
    filteredDF = filterDFType(df, filterType)
    if len(filteredDF.columns):
        print("*****")
        #colNoTS = df.columns.get_loc(df.filter(filteredDF).columns[0])
        colNoTS = df.columns.get_loc(filteredDF.columns[0])
        #print(df.iloc[:,[colNoTS,colNoTS+1]].dropna())
        return df.iloc[:,[colNoTS,colNoTS+1]].dropna()
    else:
        return pandas.DataFrame(columns=['ts', 'tp'])

def calculateThrougputPerSecondDirection(dirDF, nodeIdent, appIndent):
    # dirDF = getFilteredDFtypeAndTS(df, direction[1])
    # dirDf = df
    dirDF = dirDF.rename(columns={str(dirDF.columns[0]) : "ts", str(dirDF.columns[1]) : "bytes"})
    print(max(dirDF["bytes"].tolist()), statistics.mean(dirDF["bytes"].tolist()), min(dirDF["bytes"].tolist()))
    tB = [0,0.1] # time bounds for calculation
    colName = 'Throughput ' + nodeIdent + appIndent
    tpDirDF = pandas.DataFrame(columns=[colName])
    print(tB)
    while tB[1] <= maxSimTime:
        if DEBUG: print(tB, end =" -> Throughput: ")
        #throughput = dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].sum()
        # throughput = sum([x + 47 for x in dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].tolist()])
        throughput = sum([x + 33 for x in dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].tolist()])
        tpDirDF = pandas.concat([tpDirDF, pandas.DataFrame.from_records([{colName : throughput*8/100000}])])
        #tpDirDF = tpDirDF.append({colName : throughput*8/100000}, ignore_index=True)

        if DEBUG: print(throughput*8/100000, end=" mbps\n")
        tB = [x+0.1 for x in tB]
    return tpDirDF

def calculateThrougputMADirection(dirDF, nodeIdent):
    # dirDF = getFilteredDFtypeAndTS(df, direction[1])
    # dirDf = df
    dirDF = dirDF.rename(columns={str(dirDF.columns[0]) : "ts", str(dirDF.columns[1]) : "bytes"})
    tB = [0,1] # time bounds for calculation
    colName = 'Throughput ' + nodeIdent 
    tpDirDF = pandas.DataFrame(columns=[colName])
    while tB[1] <= maxSimTime:
        if DEBUG: print(tB, end =" -> Throughput: ")
        throughput = dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].sum()
        tpDirDF = tpDirDF.append({colName : throughput*8/1000}, ignore_index=True)
        if DEBUG: print(throughput*8/1000, end=" kbps\n")
        tB = [x+0.01 for x in tB]
    return tpDirDF

def extractQueueTPperSecond(testName, numCLI, nodeTypes, nodeSplit, queueNum):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, 'resAllocLink', 0)
    df1 = getFilteredDFtypeAndTS(df, 'packetPopped:vector(packetBytes) htbTest1.router1.ppp[0].ppp.queue.queue['+ str(queueNum) +']')
    return calculateThrougputPerSecondDirection(df1, 'Leaf ' + str(queueNum + 1))

# extractQueueTPperSecond("htbTest1", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 0)
# extractQueueTPperSecond("htbTest1", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 1)

def extractNodeTPperSecond(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum, numApps):
    fig, ax1 = plt.subplots(1, figsize=(26,16))
    print(nodeNum)
    sumTP = []
    sumTP1 = []
    # sumTP2 = []
    sumTP2 = []

    times = [x/10 for x in range(0, maxSimTime*10)]
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum)
    for i in range(0, numApps):
        print('packetReceived:vector(packetBytes) htbEvaluation.hostFDO[0].app['+ str(i) +']')
        df1 = getFilteredDFtypeAndTS(df, 'packetReceived:vector(packetBytes) htbEvaluation.hostFDO[0].app['+ str(i) +']')
        tempTPs=calculateThrougputPerSecondDirection(df1, nodeName + ' ' + str(nodeNum) , ' Flow: ' + str(i))['Throughput ' + nodeName + ' ' + str(0) + ' Flow: ' + str(i)].tolist()
        print(tempTPs)
        mrkr = 'o'
        if i == 0:
        	labl = ' Flow ' + str(i)
        	sumTP = tempTPs
        else:
            labl = ' Flow ' + str(i)
            sumTP = [x+y for x,y in zip(sumTP, tempTPs)]
            if i == 2 and 'scenario2' in testName:
                sumTP1 = sumTP
            if i == 3 and 'scenario2' in testName:
                sumTP2 = tempTPs
                mrkr='s'
            if i > 3 and 'scenario2' in testName:
                sumTP2 = [x+y for x,y in zip(sumTP2, tempTPs)]
                mrkr='s'
        ax1.plot(times, tempTPs, marker=mrkr, linestyle='-', label=labl, alpha=0.8, zorder=100)
    if 'scenario2' in testName:
        ax1.plot(times, sumTP1, marker='o', linestyle='dashed', label='Inner 1', color='grey', alpha=0.9, zorder=80, markersize=14)
        ax1.plot(times, sumTP2, marker='s', linestyle='dashed', label='Inner 2', color='darkgrey', alpha=0.9, zorder=85, markersize=14)
    ax1.plot(times, sumTP, 'X--', label='Sum', alpha=1, zorder=10, markersize=18, color='k')
    if "scenario1" in testName:
        plt.legend(loc="center", bbox_to_anchor=(0.5,0.65)).set_zorder(150)
    elif "scenario2" in testName:
        plt.legend(loc="center", bbox_to_anchor=(0.5,0.775), ncol=2).set_zorder(150)
    else:
        plt.legend(loc="upper right").set_zorder(150)
    plt.grid()
    ax1.set_ylabel('Throughput [Mbit/s]')
    ax1.set_xlabel('Simulation Time [s]')
    ax1.set_xlim(0,20)
    fig.savefig( '../results/'+str(testName)+'/'+str(testName)+'_tps1s.png', dpi=100, bbox_inches='tight')
    fig.savefig( '../results/'+str(testName)+'/'+str(testName)+'_tps1s.pdf', dpi=100, bbox_inches='tight')
    plt.close('all')
    # df1 = getFilteredDFtypeAndTS(df, 'rxPkOk')
    # df1 = getFilteredDFtypeAndTS(df, 'txPk')
    
def extractNodeE2ED(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum, numApps):
    fig, ax1 = plt.subplots(1, figsize=(26,16))
    print(nodeNum)
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum)
    for i in range(0, numApps):
        print('endToEndDelay:vector htbEvaluation.hostFDO[0].app['+ str(i) +']')
        df1 = getFilteredDFtypeAndTS(df, 'endToEndDelay:vector htbEvaluation.hostFDO[0].app['+ str(i) +']')
        dirDF = df1.rename(columns={str(df1.columns[0]) : "ts", str(df1.columns[1]) : "delay"})
        labl = ' Flow ' + str(i)
        tB = [0,1] # time bounds for calculation
        print('Flow', i, end=': ')
        while tB[1] <= maxSimTime:
            #throughput = dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].sum()
            # throughput = sum([x + 47 for x in dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["bytes"].tolist()])
            delays = [x for x in dirDF.loc[(dirDF['ts'] > tB[0]) & (dirDF['ts'] <= tB[1])]["delay"].tolist()]
            if len(delays) > 0:
                print(round(statistics.mean(delays)*1000,2), end=', ')
            else:
                print(0.00, end=', ')
            tB = [x+1 for x in tB]
        print('\n')
        # tempTPs=calculateThrougputPerSecondDirection(df1, nodeName + ' ' + str(nodeNum) , ' Flow: ' + str(i))['Throughput ' + nodeName + ' ' + str(0) + ' Flow: ' + str(i)].tolist()
        # print(tempTPs)
        # if i == 0:
        # 	labl = ' Flow ' + str(i)
        # 	sumTP = tempTPs
        # else:
        #     labl = ' Flow ' + str(i)
        #     sumTP = [x+y for x,y in zip(sumTP, tempTPs)]
        #     if i == 2 and 'scenario2' in testName:
        #         sumTP1 = sumTP
        #     if i == 3 and 'scenario2' in testName:
        #         sumTP2 = tempTPs
        #     if i > 3 and 'scenario2' in testName:
        #         sumTP2 = [x+y for x,y in zip(sumTP2, tempTPs)]
        
        ax1.plot(dirDF['ts'].dropna().tolist(), dirDF['delay'].dropna().tolist(), 'o-', label=labl, alpha=0.8, zorder=100)
    # if 'scenario2' in testName:
    #     ax1.plot(times, sumTP1, marker='^', linestyle='dashed', label='Inner 1', alpha=0.7, zorder=80, markersize=14)
    #     ax1.plot(times, sumTP2, marker='v', linestyle='dashed', label='Inner 2', alpha=0.7, zorder=85, markersize=14)
    # ax1.plot(times, sumTP, 'X--', label='Sum', alpha=1, zorder=10, markersize=14, color='k')
    # if "scenario1" in testName:
    #     plt.legend(loc="center", bbox_to_anchor=(0.5,0.65)).set_zorder(150)
    # elif "scenario2" in testName:
    #     plt.legend(loc="center", bbox_to_anchor=(0.5,0.775), ncol=2).set_zorder(150)
    # else:
    plt.legend(loc="upper right").set_zorder(150)
    plt.grid()
    ax1.set_ylabel('End-To-End Delay [s]')
    ax1.set_xlabel('Simulation Time [s]')
    fig.savefig( '../results/' +str(testName)+'/'+str(testName)+'_delay.png', dpi=100, bbox_inches='tight')
    fig.savefig( '../results/' +str(testName)+'/'+str(testName)+'_delay.pdf', dpi=100, bbox_inches='tight')
    plt.close('all')

# extractNodeTPperSecond("htbTest1", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 1)

def extractNodeTPma(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum)
    df1 = getFilteredDFtypeAndTS(df, 'rxPkOk')
    return calculateThrougputMADirection(df1, nodeName + ' ' + str(nodeNum))

def plotNodesMA(testName, numCLI, nodeTypes, nodeSplit, nodeName, numNodes):
    fig, ax1 = plt.subplots(1, figsize=(26,16))
    times = [x/100 for x in range(0, maxSimTime*100-100)]
    for i in range(0, numNodes):
        tempTPs = extractNodeTPma(testName, numCLI, nodeTypes, nodeSplit, nodeName, i)['Throughput ' + nodeName + ' ' + str(i)].tolist()
        if i == 0:
            labl = 'Client ' + str(i) + '(QoS)'
        else:
            labl = 'Client ' + str(i)
        ax1.plot(times, tempTPs, label=labl)
    plt.legend()
    plt.grid()
    ax1.set_ylabel('Throughput [kbps]')
    ax1.set_xlabel('Simulation Time [s]')
    fig.savefig( '../results/' +str(testName)+'/'+str(testName)+'_tpsMA.pdf', dpi=100, bbox_inches='tight')
    plt.close('all')

def plotNodes1s(testName, numCLI, nodeTypes, nodeSplit, nodeName, numNodes,numApps):
	extractNodeTPperSecond(testName, numCLI, nodeTypes, nodeSplit, nodeName, 0,numApps)
      
    # plt.show()

# throughput:vector htbEvaluation.hostFDO[0].app[0]

# def plotFlowTP(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum, numApps):
# 	fig, ax1 = plt.subplots(1, figsize=(26,16))

# 	sumTP = []

# 	times = [x for x in range(0, maxSimTime)]
# 	df = importDF(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum)
# 	for i in range(0, numApps):
#         print('throughput:vector htbEvaluation.hostFDO[0].app['+ str(i) +']')
#         df1 = getFilteredDFtypeAndTS(df, 'throughput:vector htbEvaluation.hostFDO[0].app['+ str(i) +']')
#         # tempTPs=calculateThrougputPerSecondDirection(df1, nodeName + ' ' + str(nodeNum) , ' Flow: ' + str(i))['Throughput ' + nodeName + ' ' + str(0) + ' Flow: ' + str(i)].tolist()
#         # print(tempTPs)
#         if i == 0:
#         	labl = ' Flow ' + str(i)
#         	sumTP = tempTPs
#         else:
#         	labl = ' Flow ' + str(i)
#         	sumTP = [x+y for x,y in zip(sumTP, tempTPs)]
#         ax1.plot(times, tempTPs, label=labl, alpha=0.95)
# 	ax1.plot(times, sumTP, label='Sum', alpha=0.8)
# 	plt.legend(loc="upper right")
# 	plt.grid()
# 	ax1.set_ylabel('Throughput [kbps]')
# 	ax1.set_xlabel('Simulation Time [s]')
# 	fig.savefig( '../exports/plots/htbTests/'+str(testName)+'_tps1s.png', dpi=100, bbox_inches='tight')
# 	plt.close('all')

# def plotQueueLevel(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum, numApps):
# 	fig, ax1 = plt.subplots(1, figsize=(26,16))

# 	sumTP = []

# 	times = [x for x in range(0, maxSimTime)]
# 	df = importDF(testName, numCLI, nodeTypes, nodeSplit, nodeName, nodeNum)
# 	for i in range(0, numApps):
#         print('packetReceived:vector(packetBytes) htbEvaluation.hostFDO[0].app['+ str(i) +']')
#         df1 = getFilteredDFtypeAndTS(df, 'packetReceived:vector(packetBytes) htbEvaluation.hostFDO[0].app['+ str(i) +']')
#         tempTPs=calculateThrougputPerSecondDirection(df1, nodeName + ' ' + str(nodeNum) , ' Flow: ' + str(i))['Throughput ' + nodeName + ' ' + str(0) + ' Flow: ' + str(i)].tolist()
#         print(tempTPs)
#         if i == 0:
#         	labl = ' Flow ' + str(i)
#         	sumTP = tempTPs
#         else:
#         	labl = ' Flow ' + str(i)
#         	sumTP = [x+y for x,y in zip(sumTP, tempTPs)]
#         ax1.plot(times, tempTPs, label=labl, alpha=0.95)
# 	ax1.plot(times, sumTP, label='Sum', alpha=0.8)
# 	plt.legend(loc="upper right")
# 	plt.grid()
# 	ax1.set_ylabel('Throughput [kbps]')
# 	ax1.set_xlabel('Simulation Time [s]')
# 	fig.savefig( '../exports/plots/htbTests/'+str(testName)+'_tps1s.png', dpi=100, bbox_inches='tight')
# 	plt.close('all')


# queueLength:vector htbEvaluation.serverFDO.ppp[0].ppp.queue.queue[1]
# plotNodes1s("htbTest2c", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'resAllocLink', 1)

# plotNodes("htbTest1", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 15)
# plotNodes1s("htbTest2d", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 15)
# plotNodes1s("noHtbTest2c", 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 15)

# for name in ['htbTest2', 'htbTest3', 'htbTest4', 'htbTest5', 'noHtbTest2', 'noHtbTest3', 'noHtbTest4', 'noHtbTest5']:
#     plotNodes1s(name, 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 15)
    # plotNodesMA(name, 15, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,15,0,0], 'hostFDO', 15)


# plotNodes1s('marcinTest3', 2, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,2,0,0], 'hostFDO', 2)
# plotNodes1s('stasTest3', 2, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,2,0,0], 'hostFDO', 2)
# plotNodes1s('stasTest9', 2, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,2,0,0], 'hostFDO', 2)
# plotNodes1s('udp2clients', 1, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [0,0,1,0,0], 'hostFDO', 1,2)

if __name__ == "__main__":
    name = sys.argv[3]
    print(name)
    numVID = int(name.split('VID')[1].split('_LVD')[0])
    numLVD = int(name.split('LVD')[1].split('_FDO')[0])
    numFDO = int(name.split('FDO')[1].split('_SSH')[0])
    numSSH = int(name.split('SSH')[1].split('_VIP')[0])
    numVIP = int(name.split('VIP')[1].split('/')[0])
    numCLI = numVID + numLVD + numFDO + numSSH + numVIP
    print(numFDO)
    plotNodes1s(sys.argv[1], numCLI, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [numVID, numLVD, numFDO, numSSH, numVIP], 'hostFDO', 0, int(sys.argv[4]))
    print(numFDO)
    extractNodeE2ED(sys.argv[1], numCLI, ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [numVID, numLVD, numFDO, numSSH, numVIP], 'hostFDO', 0, int(sys.argv[4]))