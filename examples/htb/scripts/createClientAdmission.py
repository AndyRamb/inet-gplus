import numpy

def clientAdmission(clients):
    startTime=numpy.random.randint(1,8,clients)
    length=numpy.random.poisson(2,clients)
    endTime=startTime+length+1
    app = numpy.arange(clients)

    configString = ""
    for a in app:
        configString += '*.hostFDO[*].app['+ str(a) +'].startTime = ' + str(startTime[a]) + 's\n' 
        configString += '*.hostFDO[*].app['+ str(a) +'].stopTime = ' + str(endTime[a]) + 's\n'

    changeTimes = numpy.unique(numpy.concatenate((startTime, endTime), axis=None))
    #print ', '.join(changeTimes)
    configString += ".hostFDO[0].ppp[0].queue.scheduler.changeTimes = [" + ', '.join(str(c) for c in changeTimes) + "]\n"

    for t in changeTimes:
        present = []
        for a in app:
            if startTime[a] > t:
                print(str(a) + "a starts after time t")
            elif startTime[a] <= t and t < endTime[a]:
                print(str(a) + "a is running at time t, adjust resources")
            else:
                print(str(a) + "a is not running at time t")
    
    return configString

print(clientAdmission(5))

# liteCbaselineTestTokenQoS_base:
#*.hostFDO[*].app[0].startTime = uniform(0.01s,1s) # time first session begins
#*.hostFDO[*].app[0].stopTime = -1s # time of finishing sending, negative values mean forever
