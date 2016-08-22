from overlay import *
from signac import *
import os, csv
from omium import *
import porthole
import datetime

# # Initialize the signac point cloud rendering module. Whenever new data is loaded
# # call the redraw function to refresh the screen.
sig = Signac.getInstance()
sig.setFieldLoadedCommand('redraw()')

# setup the camera
camera = getDefaultCamera()
camera.setBackgroundColor(Color('black'))
camera.setNearFarZ(1, 100000)

# #-------------------------------------------------------------------------------
# # Load firefly components
orun('config.py')
orun('colormapConfig.py')
orun('render.py')
orun('loader.py')
orun('flyControl.py')

#-------------------------------------------------------------------------------
# Application state

# default scale applied to points
pointScale = scale                 

# data mode. see loader.py
dataMode = None                     

# filter mode. Used to exclude a data range from rendering
filterMode = None                   
filterMin = 0
filterMax = 1

# colormapper flag, and bounds of the color map
colormapperEnabled = False
colormapMin = 0
colormapMax = 1

# True when we are choosing a center of rotation. see flyControl.py
pivotSelectionMode = False

filterStart = 0.0
filterEnd = 1.0
currentColorMapIndex = 0
# Initialize an array with false
isLogArray = [False] * 10
# rendering options. kernelMode controls how every single point is rendered.
# renderMode controls how the full image is rendered on screen.
kernelMode = 0
renderMode = 0

#-------------------------------------------------------------------------------
# Scene Setup

# create a point cloud view. This object takes care of rendering and generates
# an image we can place on screen or save to disk. 
pcw = PointCloudView()
pcw.setColormapper(prog_mapper)

# we assume parts is a list containing all the point clouds we want to render
# (parts is populated by loader.py)
for p in parts: pcw.addPointCloud(p)

# create a 2D overlay to display the image rendered by the point cloud view
mainView = Overlay()
mainView.setAutosize(True)
mainView.setTexture(pcw.getOutput())

# create a scene node to handle the 3D scene, attach all the point cloud objects
# to it. 
sn = SceneNode.create('galaxy')
sn.setScale(scale, scale, scale)
for p in parts: 
    sn.addComponent(p)
    p.setPointScale(scale)

#-------------------------------------------------------------------------------
# UI
filterModes = [
    'None',
    'Density',
    'SmoothingLength'
]

kernelModes = [
    'Uniform',
    'Smooth'
]

renderModes = [
    'Standard',
    'Faded',
    'Band5'    
]

# Omium is the web renderer. we use it to render the user interface
o = Omium.getInstance()

# start up the web server that will serve the user interface.
porthole.initialize(4080, './fireflyUi.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')
ps.setConnectedCommand('onClientConnected()')

# used for passing boleans from the js interface
useSmoothingLength = False
true = True
false = False

# called when the user interface is ready. Create an overlay to display it.
def loadUi():
    global gui
    global p
    gui = Overlay()
    p = o.getPixels()
    guifx = OverlayEffect()
    guifx.setShaders('overlay/overlay.vert', 'overlay/overlay-flipy.frag')
    gui.setTexture(p)
    gui.setAutosize(True)
    gui.setEffect(guifx)
    o.setFocusChangedCommand('onUiFocusChanged()')
    o.open('http://localhost:4080')
    onResize()
    onUiFocusChanged()

def onUiFocusChanged():
    if(o.isFocused()):
        gui.setAlpha(1)
    else:
        gui.setAlpha(0.8)

# called when a user interface client connects.
def onClientConnected():
    ps.broadcastjs('initializePresetPanels()', '')
    initializePresetViews()
    
    ps.broadcastjs('initializeControls({0}, {1}, {2}, {3}, {4}, {5})'
        .format(dataModes, colorMapLabels, colorMapNames, filterModes, kernelModes, renderModes), '')
    o.setZoom(-1)

# handle input events
def onEvent():
    e = getEvent()
    if(e.isFlagSet(EventFlags.Ctrl)): enablePivotSelectorMode(True)
    elif(e.getType() == EventType.Up and not e.isFlagSet(EventFlags.Ctrl) and pivotSelectionMode) : enablePivotSelectorMode(False)

    if(e.isKeyDown(Keyboard.KEY_M)): ps.broadcastjs('toggleColorMap()','')
    if(e.isKeyDown(Keyboard.KEY_H)): ps.broadcastjs('toggleHelp()','')
    if(e.isKeyDown(Keyboard.KEY_V)): ps.broadcastjs('clearConsole()','')
    if(e.isKeyDown(Keyboard.KEY_C)): ps.broadcastjs('toggleConsole()','')
    
setEventFunction(onEvent)

def setKernelMode(mode):
    # pass the kernel mode index to the shaders and redraw
    for p in programs: p.define('KERNEL_MODE', str(mode))
    redraw()

def setRenderMode(mode):
    # pass the render mode index to the shaders and redraw
    global renderMode
    renderMode = renderModes[mode]
    for p in programs: p.define('RENDER_MODE', str(mode))
    redraw()
    
def enableColormapper(enabled):
    global colormapperEnabled
    colormapperEnabled = enabled
    pcw.enableColormapper(enabled)
    redraw()

def enableSmoothingLength(enabled):
    global useSmoothingLength
    useSmoothingLength = enabled
    print(enabled)
    if(enabled):
        pc0.setSize(sl0)
    else:
        pc0.setSize(None)
    redraw()
    
def setPointScale(sc):
    global pointScale
    pointScale = sc
    for p in parts: p.setPointScale(sc)
    print('point scale: ' + str(sc))
    redraw()
  
def setColormap(index):
    global currentColorMapIndex
    currentColorMapIndex = index
    for p in parts: p.setColormap(colormaps[index])
    pcw.setColormap(colormaps[index])
    redraw()

def updateColormapBounds(cmin, cmax):
    print('bounds now are {0}    {1}'.format(cmin, cmax))
    global colormapMin
    global colormapMax
    colormapMin = cmin
    colormapMax = cmax
    pcw.setChannelBounds(colormapMin, colormapMax)
    redraw()

def resetColormapBounds():
    pcw.updateChannelBounds(True)
    queueCommand('sendColormapBounds()')

def sendColormapBounds():
    global colormapMin
    global colormapMax
    colormapMin = pcw.getChannelMin()
    colormapMax = pcw.getChannelMax()
    ps.broadcastjs("updateColormapBounds({0}, {1})".format(colormapMin, colormapMax), '')

def setFilterMode(mode):
    global filterMode
    filterMode = mode
    dm = filterModes[mode]
    if(dm == 'None'): 
        for p in parts: p.setFilter(None)
    elif(dm == 'Density'): 
        pc0.setFilter(d0)
    redraw()

def updateFilterBounds(cmin, cmax):
    print('bounds now are {0}    {1}'.format(cmin, cmax))
    for p in parts: p.setFilterBounds(cmin, cmax)
    redraw()

def resetFilterBounds():
    print('resetting bounds')
    
    
def enableLogScale(enable):
    if(enable):
        for p in programs: p.define('LOG_MODE', '1')
    else:
        for p in programs: p.define('LOG_MODE', '0')
    redraw()
    
def saveViewImage():
    filename = '{:%Y%m%d-%H%M%S}.png'.format(datetime.datetime.now())
    saveImage(pcw.getOutput(), filename, ImageFormat.FormatPng)
    #ps.broadcastjs("setScreenView('{0}')".format(filename), '')
        
def echo(msg):
    ps.broadcastjs("setConsole('" + msg + "')", '')

def cls():
    ps.broadcastjs('clearConsole()', '')

#-----------------Loading and Saving Presets -----------------------

file = False
reader = False
fileName = "presetViews.txt"
presets = []
nameList = []
currentIndex = 0

# file.close()

def initializePresetViews():
    print "initializing presets"
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
            print "skipping first, but by the way, it is: "
            print row
        elif not row:
            print "found empty array, moving onwards"
        else: 
            print "reading row: "
            print row
            v = [row[0],float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),int(row[8]),bool(row[9]),bool(row[10]),int(row[11]),float(row[12]),float(row[13])]
            presets.append(v)
            nameList.append(row[0])
    ps.broadcastjs('settingPresets(' + str(nameList) + ')', '')

def setPresetView( viewArrayIndex ):
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax
    global presets
    presetData = presets[viewArrayIndex]
    print "Setting current View to :", presetData[0]
    setCamPos(presetData[1],presetData[2],presetData[3])
    setPivotPoint(presetData[4],presetData[5],presetData[6])
    setPointScale(presetData[7])
    # setDataMode(presetData[8])
    # enableSmoothingLength(presetData[9])
    # enableColormapper(presetData[10])
    # setColormap(presetData[11])
    # updateColormapBounds(presetData[12], presetData[13])
    redraw()
    
def saveCurrentView(name):
    global presets
    global file, nameList
    nameList.append(name)
    print "Name: " , name
    global cameraPosition,pivotPosition,pointScale, dataMode, useSmoothingLength
    global colormapperEnabled, currentColorMapIndex, colormapMin, colormapMax

    newEntry = [name, cameraPosition[0],cameraPosition[1],cameraPosition[2],pivotPosition[0],pivotPosition[1],pivotPosition[2],pointScale,dataMode,useSmoothingLength,colormapperEnabled,currentColorMapIndex,colormapMin,colormapMax]
    # print "Table: ",newEntry
    print "Before: "
    print presets
    presets.append(newEntry)
    print "After: "
    print presets

    saveViews()

def saveViews():
    global presets, file
    file = open(fileName,'w')
    writer = csv.writer(file, delimiter='\t')
    s = ['name','camX','camY','camZ','pivotX','pivotY','pivotZ','pointScale','dataMode','useSmoothingLength','colormapEnabled, colorMapIndex, colormapMin, colormapMax']
    writer.writerow(s)
    for row in presets:
        print "writing row: " , row
        writer.writerow(row)
    file.close()

def eraseView(number):
    global presets
    print "Erasing element from array"
    # print presets
    presets = presets.pop(number)
    # print "After delete"
    # print presets 
    saveViews()
    pass

#-------------------
    
def enablePivotSelectorMode(enabled):
    global pivotSelectionMode
    pivotSelectionMode = enabled
    if(enabled):
        for p in parts:
            p.setData(None)
            p.setProgram(prog_df)
            p.setPointScale(scale)
        pcw.enableColormapper(False)
        for p in parts: p.setDecimation(dqDec)
        camera.setSceneEnabled(True)
    else:
        # Reset previous view mode
        setDataMode(dataMode)
        setPointScale(pointScale)
        enableColormapper(colormapperEnabled)
        updateColormapBounds(colormapMin, colormapMax)
        redraw()

def resetPivot():
    global pivotPosition
    pivotPosition = sn.getBoundCenter()
    print("Pivot position: " + str(pivotPosition))
 
def setCamPos(x,y,z):
    global camera, cameraPosition
    oldPos = camera.getPosition()
    print "old camera position to: " , cameraPosition
    cameraPosition = Vector3(float(x),float(y),float(z))
    print "new camera position to:" , cameraPosition
    camera.setPosition(cameraPosition)
    redraw()
    #camera.setPosition(Vector3(float(x),float(y),float(z)))

def setPivotPoint(x,y,z):
    global pivotPosition
    print "setting pivit point to to x:" , x ," y: ", y , " z: ", z
    pivotPosition = Vector3(float(x),float(y),float(z))

def lookAtPivot():
    print "looking at pivot point"
    global camera, pivotPosition
    camera.lookAt(pivotPosition,Vector3(0,1,0))
    redraw()

def requestUpdatePos():
    global cameraPosition
    ps.broadcastjs('updateCameraPos('+str(cameraPosition[0])+','+str(cameraPosition[1])+','+str(cameraPosition[2])+')','')
 
setDataMode(0)
setPointScale(pointScale)
focus()
