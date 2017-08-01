#-----------------Loading and Saving Presets -----------------------
try:
    presetPath
except NameError:
    presetPath = "./"

file = False
reader = False

try:
    fileName
except NameError:
    fileName = "fireflyPresets.txt"
presets = []
nameList = []

# file.close()

def initializePresetViews():
    global reader, presets, file, reader, nameList
    if not os.path.isfile(presetPath + fileName):
        print "No file: " , presetPath + fileName , " creating new file"
        file = open(presetPath + fileName, "w")
        file.close()
    else:
        print "File: ", presetPath + fileName, " found, loaded saved data"
    file = open(presetPath + fileName, 'rU')
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
            progEnabled = (row[21] == 'True')
            # print "smoothing length: " , slEnabled
            # print "Color mapper: " , cmEnabled
            print "Loading row: "
            print "Prog Enabled: ", progEnabled
            print "Decimation value ", row[22]
            v = [row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),int(row[8]),slEnabled,cmEnabled,int(row[11]),float(row[12]),float(row[13]),int(row[14]),int(row[15]),float(row[16]),float(row[17]),float(row[18]),float(row[19]),lgEnabled,progEnabled,int(float(row[22]))]
            presets.append(v)
            nameList.append(row[0])
    ps.broadcastjs('settingPresets(' + str(nameList) + ')', '')

def setPresetView( viewArrayIndex ):
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax
    global presets, cameraOrientation, progressiveRender, dqDec
    print "-----------"
    print presets
    print "index: " , viewArrayIndex
    print "Length of array: ", len(presets)
    if len(presets) == 0:
        print "No presets currently set"
        return
    presetData = presets[viewArrayIndex]
    # print "Setting current View to :", presetData[0]
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

    # print "setting preset view: ", presetData[21]
    # print  "Decimation value : ", presetData[22]
    enableProgressive(presetData[21])
    setDecimationValue(presetData[22])

    # print "Setting New Camera Orientation" ,newQuat
    cameraOrientation = newQuat
    camera.setOrientation(cameraOrientation)
    updateJavaScriptInterface()
    redraw()

def saveCurrentView(name):
    global presets
    global file, nameList
    name = name.replace(' ', '_')
    nameList.append(name)
    # print "Name: " , name
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength, cameraOrientation
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax, isLogScale
    global progressiveRender, dqDec
    angAxis = cameraOrientation.get_angle_axis()
    print "---->", angAxis
    # print "Set Progressive Render: " , progressiveRender
    # print "Set Decimation to " , dqDec
    newEntry = [name, cameraPosition[0],cameraPosition[1],cameraPosition[2],pivotPosition[0],pivotPosition[1],pivotPosition[2],pointScale,dataMode,useSmoothingLength,colormapperEnabled,currentColorMapIndex,colormapMin,colormapMax,kernelModeInd,renderModeInd,angAxis[0],angAxis[1][0],angAxis[1][1],angAxis[1][2],isLogScale,progressiveRender,dqDec]
    # print "Table: ",newEntry
    presets.append(newEntry)
    print("saving current View")

    global presets, file
    file = open(presetPath + fileName,'w')
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
    nameList.pop(number)
    # print "After delete"
    # print presets 
    saveViews()
    pass
