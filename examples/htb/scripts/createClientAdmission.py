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

    times = numpy.unique(numpy.concatenate((startTime, endTime), axis=None))

    print(times)
    
    return configString

print(clientAdmission(5))

# liteCbaselineTestTokenQoS_base:
#*.hostFDO[*].app[0].startTime = uniform(0.01s,1s) # time first session begins
#*.hostFDO[*].app[0].stopTime = -1s # time of finishing sending, negative values mean forever
