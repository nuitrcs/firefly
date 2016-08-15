from overlay import *
from signac import *
import datetime

sig = Signac.getInstance()

#-------------------------------------------------------------------------------
# GPU Program Setup
prog_default = sig.addProgram('default')
prog_default.setVertexShader('shaders/point.vert')
prog_default.setGeometryShader('shaders/point.geom')
prog_default.setFragmentShader('shaders/point.frag')

prog_vector = sig.addProgram('vector')
prog_vector.setVertexShader('shaders/vector.vert')
prog_vector.setGeometryShader('shaders/vector.geom')
prog_vector.setFragmentShader('shaders/vector.frag')

prog_fixedColor = sig.addProgram('fixedColor')
prog_fixedColor.setVertexShader('shaders/point.vert')
prog_fixedColor.setGeometryShader('shaders/point.geom')
prog_fixedColor.setFragmentShader('shaders/point-fixedColor.frag')

prog_df = sig.addProgram('depthFilter')
prog_df.setVertexShader('shaders/point-depthFilter.vert')
prog_df.setGeometryShader('shaders/point-depthFilter.geom')
prog_df.setFragmentShader('shaders/point-depthFilter.frag')

prog_channel = sig.addProgram('channel')
prog_channel.setVertexShader('shaders/point.vert')
prog_channel.setGeometryShader('shaders/point.geom')
prog_channel.setFragmentShader('shaders/point-channel.frag')

prog_mapper = sig.addProgram('colormapper')
prog_mapper.setVertexShader('shaders/colormapper.vert')
prog_mapper.setFragmentShader('shaders/colormapper.frag')

colorMapLabels = ["Black-Green","Full Spectrum","Blue-Orange","Blue-White-Orange"]
colorMapNames = ["colormaps/bk-gr.png","colormaps/bu-gr-wh-yl-rd.png","colormaps/bu-og.png","colormaps/bu-wh-og.png"]
colormaps = []
for cn in colorMapNames:
    colormaps.append(loadImage(cn))

for i in colormaps: i.setTextureFlags(TextureFlags.WrapClamp)

#-------------------------------------------------------------------------------
# Data Setup
l = FireLoader()
l.open('C:/dev/omegalib/apps/firefly/snapshot_140.hdf5')

# PartType0
ds0 = Dataset.create('PartType0')
ds0.setLoader(l)

x0 = ds0.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
sl0 = ds0.addDimension('SmoothingLength', DimensionType.Float, 0, 'SmoothingLength')
d0 = ds0.addDimension('Density', DimensionType.Float, 0, 'Density')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')

pc0 = PointCloud.create('pc0')
pc0.setOptions('50000 0:100000:1')
pc0.setDimensions(x0, y0, z0)
pc0.setData(sl0)
pc0.setVectorData(vx0, vy0, vz0)
pc0.setSize(sl0)
pc0.setProgram(prog_vector)
pc0.normalizeFilterBounds(True)
pc0.setFilterBounds(0, 1)
pc0.setColormap(colormaps[2])
pc0.setColor(Color('red'))

# PartType1
ds1 = Dataset.create('PartType2')
ds1.setLoader(l)

x1 = ds1.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y1 = ds1.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z1 = ds1.addDimension('Coordinates', DimensionType.Float, 2, 'z')

pc1 = PointCloud.create('pc1')
pc1.setOptions('50000 0:100000:1')
pc1.setDimensions(x1, y1, z1)
pc1.setProgram(prog_fixedColor)
pc1.normalizeFilterBounds(True)
pc1.setFilterBounds(0, 1)
pc1.setColormap(colormaps[0])
pc1.setColor(Color('blue'))

pcw = PointCloudView()
pcw.addPointCloud(pc0)
pcw.addPointCloud(pc1)
pcw.setColormapper(prog_mapper)
pcw.setColormap(colormaps[2])
#pcw.enableColormapper(True)
mainView = Overlay()
mainView.setAutosize(True)
mainView.setTexture(pcw.getOutput())

parts = [pc0, pc1]

#-------------------------------------------------------------------------------
# Load firefly components
orun('dynamicQuality.py')
orun('flyControl.py')

#-------------------------------------------------------------------------------
# Scene Setup
camera = getDefaultCamera()
camera.setBackgroundColor(Color('black'))
sn = SceneNode.create('galaxy')
sn.addComponent(pc0)
sn.addComponent(pc1)

scale = 0.01
pointScale = scale
dataMode = None
colormapperEnabled = False
colormapMin = 0
colormapMax = 1
pivotSelectionMode = False

sn.setScale(scale, scale, scale)
#sn.setPosition(-5, 1, -10)

pc0.setPointScale(scale)
pc1.setPointScale(scale)

# set camera near / far z to some reasonable value
# this is needed to make slicing work.
getDefaultCamera().setNearFarZ(1, 100000)

# Hardcoded initial pivot.
pivotPosition = Vector3(47, 17, 62)
focus()

filterStart = 0.0
filterEnd = 1.0
# Initialize an array with false
isLogArray = [False] * 10

#-------------------------------------------------------------------------------
# Input
def onEvent():
    global startPos
    global rotating
    global pivotPosition
    global pivotRayOrigin
    global pivotRayDirection
    global pivotDistance
    global cameraPosition
    global cameraOrientation
    global snapbackCameraPosition
    global snapbackCameraOrientation
    global snapback
    global panVector
    global panSpeed
    
    e = getEvent()
    if(e.isFlagSet(EventFlags.Shift)): enablePivotSelectorMode(True)
    elif(e.getType() == EventType.Up and not e.isFlagSet(EventFlags.Shift) and pivotSelectionMode) : enablePivotSelectorMode(False)

    if(e.isKeyDown(Keyboard.KEY_M)): ps.broadcastjs('toggleColorMap()','')
    if(e.isKeyDown(Keyboard.KEY_H)): ps.broadcastjs('toggleHelp()','')
    if(e.isKeyDown(Keyboard.KEY_V)): ps.broadcastjs('clearConsole()','')
    if(e.isKeyDown(Keyboard.KEY_C)): ps.broadcastjs('toggleConsole()','')
    
def onUpdate(frame, time, dt):
    pc0.setFocusPosition(pivotPosition)
    pc1.setFocusPosition(pivotPosition)

setUpdateFunction(onUpdate)
setEventFunction(onEvent)

def redraw():
    dqon()
    
#-------------------------------------------------------------------------------
# Misc
def enablePivotSelectorMode(enabled):
    global pivotSelectionMode
    pivotSelectionMode = enabled
    if(enabled):
        pc0.setProgram(prog_df)
        pc1.setProgram(prog_df)
        pc0.setPointScale(scale)
        pc1.setPointScale(scale)
        pcw.enableColormapper(False)
        for p in parts: p.setDecimation(dqDec)
        camera.setSceneEnabled(True)
    else:
        # Reset previous view mode
        setDataMode(dataMode)
        setPointScale(pointScale)


#-------------------------------------------------------------------------------
# UI
from omium import *
import porthole

o = Omium.getInstance()

porthole.initialize(4080, './fireflyUi.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')
ps.setConnectedCommand('onClientConnected()')

# used for passing boleans from the js interface
true = True
false = False


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
    o.open('http://localhost:4080')
    onResize()

getDisplayConfig().canvasChangedCommand = 'onResize()'

def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])
    pcw.resize(r[2], r[3])

dataModes = [
    'DataType', 
    'Density',
    'SmoothingLength',
    'Pivot',
    'VelocityVectors']

def onClientConnected():
    filterRanges = [[0.0,100.0],[0.0,100.0],[0.0,100.0],[0.0,100.0]]
    variableRanges = [[0.0,10.0],[2.0,4.0],[10.0,100.0],[0.5,2.0]]
    # ps.broadcastjs('printSomething()', '')
    # ps.broadcastjs('setColorMap(' + str() + ')', '')
    #ps.broadcastjs('setVariables(' + str(variables) + ',' + str(filterRanges) + ')','')
    #ps.broadcastjs('setColorMapArrays(' + str(colorMapArray) + ',' + str(colorMapLabels) + ',' + str(colorMapNames) + ')','')
    #ps.broadcastjs('addStarPanel(\'View Settings\',' + str(variables) + ',' + str(filterRanges) + ')', '')
       
    ps.broadcastjs('initializeControls({0}, {1}, {2})'
        .format(dataModes, colorMapLabels, colorMapNames), '')
    o.setZoom(2)
    # ps.broadcastjs('addStarPanel()', '')
    print "finished broadcasting some commands"

def setDataMode(mode):
    global dataMode
    dataMode = mode
    dm = dataModes[mode]
    if(dm == 'DataType'):
        pc0.setVisible(True)
        pc0.setProgram(prog_fixedColor)
        pc0.setColor(Color(0.2, 0.2, 1, 0.1))
        pc1.setVisible(True)
        pc1.setProgram(prog_fixedColor)
        pc1.setColor(Color(1, 1, 0.2, 0.1))
    elif(dm == 'Density'):
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        pc0.setData(d0)
        pc1.setVisible(False)
    elif(dm == 'SmoothingLength'):
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        pc0.setData(sl0)
        pc1.setVisible(False)
    elif(dm == 'VelocityVectors'):
        pc0.setVisible(True)
        pc0.setProgram(prog_vector)
        pc1.setVisible(False)
    redraw()

def enableColormapper(enabled):
    global colormapperEnabled
    colormapperEnabled = enabled
    pcw.enableColormapper(enabled)
    pcw.updateChannelBounds(True)
    redraw()

def enableSmoothingLength(enabled):
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
    for p in parts: p.setColormap(colormaps[index])
    pcw.setColormap(colormaps[index])
    redraw()

def setFilterBounds(minRange, maxRange, filterName,setName):
    #print "filterrangemin: " , minRange
    #print "filterrangemax: " , maxRange
    #print "filterName: " , filterName
    #print "setName: " , setName 
    #print filterName
    #print variableDict[variables[int(filterName)]]
    #pc.setFilter(variableDict[variables[int(filterName)]])
    #pc.setFilterBounds(minRange/100.0, maxRange/100.0)
    return False

def updateColormapBounds(cmin, cmax):
    print('bounds now are {0}    {1}'.format(cmin, cmax))
    global colormapMin
    global colormapMax
    colormapMin = cmin
    colormapMax = cmax
    pcw.setChannelBounds(colormapMin, colormapMax)
    redraw()

def resetColormapBounds():
    print('resetting bounds')
    pcw.updateChannelBounds(True)
    queueCommand('sendColormapBounds()')

def sendColormapBounds():
    print('sending bounds')
    global colormapMin
    global colormapMax
    colormapMin = pcw.getChannelMin()
    colormapMax = pcw.getChannelMax()
    ps.broadcastjs("updateColormapBounds({0}, {1})".format(colormapMin, colormapMax), '')
    
    
def setLogColor(isLog, setName):
    return False
    p = prog.getParams()
    if isLog != isLogArray[1] and setName == 'Gases':
        print "SetName: " , setName
        #print "before: " , p.isLog
        if isLog == True:
            p.isLog = 1
            print 'setting scale to log'
        else:
            p.isLog = 0
            print 'setting scale to linear'
        isLogArray[1] = isLog
        print "after: " , p.isLog

setDataMode(0)
setPointScale(pointScale)

def saveViewImage():
    filename = '{:%Y%m%d-%H%M%S}.png'.format(datetime.datetime.now())
    saveImage(pcw.getOutput(), filename, ImageFormat.FormatPng)
    #ps.broadcastjs("setScreenView('{0}')".format(filename), '')
        
def echo(msg):
    ps.broadcastjs("setConsole('" + msg + "')", '')

def cls():
    ps.broadcastjs('clearConsole()', '')