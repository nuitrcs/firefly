from overlay import *
from signac import *
import Navigator

sig = Signac.getInstance()

#-------------------------------------------------------------------------------
# GPU Program Setup
prog_default = sig.addProgram('default')
prog_default.setVertexShader('shaders/point.vert')
prog_default.setGeometryShader('shaders/point.geom')
prog_default.setFragmentShader('shaders/point.frag')

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


colormaps = [
    loadImage('colormaps/bu-og.png'),
    loadImage('colormaps/bu-wh-og.png'),
    loadImage('colormaps/bk-gr.png'),
    loadImage('colormaps/bu-gr-wh-yl-rd.png')
]

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

pc0 = PointCloud()
pc0.setOptions('100000 0:100000:10')
pc0.setDimensions(x0, y0, z0)
pc0.setData(sl0)
pc0.setSize(sl0)
pc0.setProgram(prog_fixedColor)
pc0.normalizeFilterBounds(True)
pc0.setFilterBounds(0, 1)
pc0.setColormap(colormaps[0])
pc0.setColor(Color('red'))

# PartType1
ds1 = Dataset.create('PartType2')
ds1.setLoader(l)

x1 = ds1.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y1 = ds1.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z1 = ds1.addDimension('Coordinates', DimensionType.Float, 2, 'z')

pc1 = PointCloud()
pc1.setOptions('100000 0:100000:10')
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
pcw.setColormap(colormaps[1])
#pcw.enableColormapper(True)
mainView = Overlay()
mainView.setAutosize(True)
mainView.setTexture(pcw.getOutput())

#-------------------------------------------------------------------------------
# Scene Setup
sn = SceneNode.create('galaxy')
sn.addComponent(pc0)
sn.addComponent(pc1)

scale = 0.01
sn.setScale(scale, scale, scale)
#sn.setPosition(-5, 1, -10)

pc0.setPointScale(scale)
pc1.setPointScale(scale)

# set camera near / far z to some reasonable value
# this is needed to make slicing work.
getDefaultCamera().setNearFarZ(1, 100000)

# Hardcoded initial pivot.
Navigator.pivotPosition = Vector3(47, 17, 62)
Navigator.focus()

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
    elif(e.getType() == EventType.Up and not e.isFlagSet(EventFlags.Shift)) : enablePivotSelectorMode(False)

    if(e.isKeyDown(Keyboard.KEY_M)): ps.broadcastjs('toggleColorMap()','')
    if(e.isKeyDown(Keyboard.KEY_H)): ps.broadcastjs('toggleHelp()','')
    if(e.isKeyDown(Keyboard.KEY_V)): ps.broadcastjs('clearConsole()','')
    if(e.isKeyDown(Keyboard.KEY_C)): ps.broadcastjs('toggleConsole()','')
    
def onUpdate(frame, time, dt):
    pc0.setFocusPosition(Navigator.pivotPosition)
    pc1.setFocusPosition(Navigator.pivotPosition)

setUpdateFunction(onUpdate)
setEventFunction(onEvent)

#-------------------------------------------------------------------------------
# Misc
def enablePivotSelectorMode(enabled):
    if(enabled):
        pc0.setProgram(prog_df)
        pc1.setProgram(prog_df)
    else:
        pc0.setProgram(prog_fixedColor)
        pc1.setProgram(prog_fixedColor)


#-------------------------------------------------------------------------------
# UI
from omium import *
import porthole

variableDict = {}
variableDict["Smoothing Length"] = sl0
variableDict["Density"] = d0
variables = ["Smoothing Length","Density","Internal Energy","Formation Rate"]

o = Omium.getInstance()

porthole.initialize(4080, './fireflyUi.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')
ps.setConnectedCommand('onClientConnected()')


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

def onClientConnected():
    print "Client has connected"
    colorMapArray = [0,1,2,3]
    colorMapLabels = ["Black-Green","Full Spectrum","Blue-Orange","Blue-White-Orange"]
    colorMapNames = ["colormaps/bk-gr.png","colormaps/bu-gr-wh-yl-rd.png","colormaps/bu-og.png","colormaps/bu-wh-og.png"]

    filterRanges = [[0.0,100.0],[0.0,100.0],[0.0,100.0],[0.0,100.0]]
    variableRanges = [[0.0,10.0],[2.0,4.0],[10.0,100.0],[0.5,2.0]]
    # ps.broadcastjs('printSomething()', '')
    # ps.broadcastjs('setColorMap(' + str() + ')', '')
    ps.broadcastjs('setVariables(' + str(variables) + ',' + str(filterRanges) + ')','')
    ps.broadcastjs('setColorMapArrays(' + str(colorMapArray) + ',' + str(colorMapLabels) + ',' + str(colorMapNames) + ')','')
    ps.broadcastjs('addStarPanel(\'View Settings\',' + str(variables) + ',' + str(filterRanges) + ')', '')
    o.setZoom(2)
    # ps.broadcastjs('addStarPanel()', '')
    print "finished broadcasting some commands"

def updateStars():
    return Falsed

def setColorMap(colorName, setName):
    global colormap
    print "Setting a new Color Map: " , colorName, " For Set: ", setName
    colormap = colorName
    print setName
    print colorName
    print colormaps[int(colorName)]
    pc.setColormap(colormaps[int(colorName)])

def setColorVariable(variable, setName):
    pc.setData(variableDict[variable])

def setPointSize(size, setName): 
    return False

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

def setColorBounds(minRange, maxRange, setName):
    return False

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

def playAnimation(file):
    playing = True
    animateCamera()


def onAnimate():
    if playing:
        return False

def isAtPoint():
    return False

def nextPoint():
    return False

def resetAnimation():
    return False

def loadAnimation():
    return False

