#-----------------Loading and Saving Presets -----------------------

file = False
reader = False
fileName = "presetViews.txt"
presets = []
nameList = []
currentIndex = 0

# file.close()

def initializePresetViews():
    global reader, presets, file, reader, nameList
    if not os.path.isfile(fileName):
        print "No file: " , fileName , " creating new file"
        file = open(fileName, "w")
        file.close()
    else:
        print "File: ", fileName, " found, loaded saved data"
    file = open(fileName, 'rU')
    reader = csv.reader(file, delimiter='\t')
    skip = True
    nameList = []
    for row in reader:
        if skip: 
            skip = False
        elif not row:
            pass
        else: 
            # print "reading row: "
            # print row
            slEnabled = (row[9] == 'True')
            cmEnabled = (row[10] == 'True')
            lgEnabled = (row[20] == 'True')
            # print "smoothing length: " , slEnabled
            # print "Color mapper: " , cmEnabled
            v = [row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),int(row[8]),slEnabled,cmEnabled,int(row[11]),float(row[12]),float(row[13]),int(row[14]),int(row[15]),float(row[16]),float(row[17]),float(row[18]),float(row[19]),lgEnabled]
            presets.append(v)
            nameList.append(row[0])
    ps.broadcastjs('settingPresets(' + str(nameList) + ')', '')

def setPresetView( viewArrayIndex ):
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax
    global presets, cameraOrientation
    presetData = presets[viewArrayIndex]
    print "Setting current View to :", presetData[0]
    setCamPos(presetData[1],presetData[2],presetData[3])
    setPivotPoint(presetData[4],presetData[5],presetData[6])
    setPointScale(presetData[7])
    setDataMode(presetData[8])
    enableSmoothingLength(presetData[9])
    enableColormapper(presetData[10])
    setColormap(presetData[11])
    updateColormapBounds(presetData[12], presetData[13])
    setKernelMode(presetData[14])
    setRenderMode(presetData[15])
    newQuat = Quaternion.new_rotate_axis(presetData[16],Vector3(presetData[17],presetData[18],presetData[19]))
    enableLogScale(presetData[20])
    # print "Setting New Camera Orientation" ,newQuat
    cameraOrientation = newQuat
    camera.setOrientation(cameraOrientation)
    updatePythonInterface()
    redraw()
    
def updatePythonInterface():
    print "Updating Python Interface"
    global dataMode,useSmoothingLength,isLogScale,pointScale,colormapperEnabled,currentColorMapIndex
    global colormapMin,colormapMax,cameraPosition,pivotPosition, renderModeInd, kernelModeInd
    ps.broadcastjs("postLoadUpdate({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15})"
        .format(dataMode, boolToJs(useSmoothingLength), boolToJs(isLogScale), pointScale,boolToJs(colormapperEnabled),currentColorMapIndex,colormapMin,colormapMax,cameraPosition[0],cameraPosition[1],cameraPosition[2],pivotPosition[0],pivotPosition[1],pivotPosition[2],renderModeInd,kernelModeInd), '')

def boolToJs(pythonBool):
    if pythonBool == False:
        return "false"
    else:
        return "true"
def saveCurrentView(name):
    global presets
    global file, nameList
    name = name.replace(' ', '_')
    nameList.append(name)
    # print "Name: " , name
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength, cameraOrientation
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax, isLogScale

    # print "Current Camera setOrientation: "
    # print cameraOrientation
    angAxis = cameraOrientation.get_angle_axis()

    newEntry = [name, cameraPosition[0],cameraPosition[1],cameraPosition[2],pivotPosition[0],pivotPosition[1],pivotPosition[2],pointScale,dataMode,useSmoothingLength,colormapperEnabled,currentColorMapIndex,colormapMin,colormapMax,kernelModeInd,renderModeInd,angAxis[0],angAxis[1][0],angAxis[1][1],angAxis[1][2],isLogScale]
    # print "Table: ",newEntry
    presets.append(newEntry)
    saveViews()

def saveViews():
    global presets, file
    file = open(fileName,'w')
    writer = csv.writer(file, delimiter='\t')
    s = ['name','camX','camY','camZ','pivotX','pivotY','pivotZ','pointScale','dataMode','useSmoothingLength','colormapEnabled, colorMapIndex, colormapMin, colormapMax','KernelModeInd','RenderModeInd',"rotDegree","rotAxisX","rotAxisY","rotAxisZ","logScale"]
    writer.writerow(s)
    for row in presets:
        # print "writing row: " , row
        writer.writerow(row)
    file.close()

def eraseView(number):
    global presets
    # print "Erasing element from array: number " , number
    # print presets
    presets.pop(number)
    # print "After delete"
    # print presets 
    saveViews()
    pass
