l = FireLoader()
l.open(datasetPath)

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:10"

dataSets = {}
dataSetVars = {}
dataModes = []
pointClouds = {}
defaultColors = {}
parts = []

def addNewDataSet(name):
    global dataSets, dataSetVars
    dataSets[name] = Dataset.create('PartType0')
    dataSets[name].setLoader(l)
    dataSetVars[name] = {}
    return dataSets[name]

def addDimension(dataSetName, variableField , offset, variableName,varType=DimensionType.Float):
    global dataSets, dataSetVars
    var = dataSets[dataSetName].addDimension(variableField,varType,offset, variableName)
    if variableField == "Coordinates":
        if not "DataType" in dataModes:
            dataModes.append("DataType")
    else:
        if not variableField in dataModes:
            dataModes.append(variableField)
    if not variableField in dataSetVars[dataSetName]:
        dataSetVars[dataSetName][variableField] = {}
    dataSetVars[dataSetName][variableField][offset] = var
    return var

def addPointCloud(name,color, dimensionVal):
    newPointCloud = PointCloud.create(name)
    newPointCloud.setOptions(pointCloudLoadOptions)
    pointClouds[name] = newPointCloud
    parts.append(newPointCloud)
    dataSetVars[name][dimensionVal]
    varList = []
    for key,value in dataSetVars[name][dimensionVal].iteritems():
        varList.append(value)
    newPointCloud.setDimensions(*varList)
    newPointCloud.setColor(color)
    defaultColors[name] = color
    return newPointCloud

def setDataMode(mode):
    print "=====---------------------======="
    print "Starting to Set Data mode with mode: " , mode
    global dataModes, dataSetVars
    dataMode = mode
    dm = dataModes[mode]
    print "DM is : " , dm
    for key, values in pointClouds.iteritems():
        print "Key is: " , key
        if (dm == 'DataType'):
            values.setData(None)
            values.setVisible(True)
            values.setProgram(prog_fixedColor)
            values.setColor(defaultColors[key])
        else:
            if dm in dataSetVars[key].keys():
                values.setVisible(True)
                if len(dataSetVars[key][dm]) == 1:
                    values.setProgram(prog_channel)
                    values.setData(dataSetVars[key][dm][0])
                else:
                    values.setProgram(prog_vector)
                    varList = []
                    for key,value in dataSetVars[key][dm].iteritems():
                        varList.append(value)
                    values.setVectorData(*varList)
            else:
                values.setVisible(False)
    redraw()

addNewDataSet('PartType0')
addDimension('PartType0','Coordinates',0,'x')
addDimension('PartType0','Coordinates',1,'x')
addDimension('PartType0','Coordinates',2,'x')
addDimension('PartType0','SmoothingLength',0,'SmoothingLength')
addDimension('PartType0','Density',0,'Density')
addDimension('PartType0','Velocities',0,'vx')
addDimension('PartType0','Velocities',1,'vy')
addDimension('PartType0','Velocities',2,'vz')

addPointCloud('PartType0',Color('red'), 'Coordinates')