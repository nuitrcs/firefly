from signac import *
import Navigator

sig = Signac.getInstance()

#-------------------------------------------------------------------------------
# GPU Program Setup
prog = sig.addProgram('points')
prog.setVertexShader('shaders/point.vert')
prog.setGeometryShader('shaders/point.geom')
prog.setFragmentShader('shaders/point.frag')
prog.setColormapShader('shaders/colormaps.frag')

colormaps = [
    loadImage('colormaps/bu-og.png'),
    loadImage('colormaps/bu-wh-og.png'),
    loadImage('colormaps/bk-gr.png'),
    loadImage('colormaps/bu-gr-wh-yl-rd.png')
]

#-------------------------------------------------------------------------------
# Data Setup
l = FireLoader()
l.open('snapshot_140.hdf5')

ds = Dataset.create('PartType0')
ds.setLoader(l)

x = ds.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y = ds.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z = ds.addDimension('Coordinates', DimensionType.Float, 2, 'z')
smoothingLength = ds.addDimension('SmoothingLength', DimensionType.Float, 0, 'SmoothingLength')
density = ds.addDimension('Density', DimensionType.Float, 0, 'Density')
variableDict = {}
variableDict["Smoothing Length"] = smoothingLength
variableDict["Density"] = density
variables = ["Smoothing Length","Density","Internal Energy","Formation Rate"]

pc = PointCloud()
pc.setOptions('100000 0:100000:10')

pc.setDimensions(x, y, z)
pc.setData(smoothingLength)
pc.setSize(smoothingLength)
pc.setProgram(prog)
pc.setFilter(smoothingLength)
pc.normalizeFilterBounds(True)
pc.setFilterBounds(0, 1.0)
pc.setColormap(colormaps[0])
#-------------------------------------------------------------------------------
# Scene Setup
sn = SceneNode.create('galaxy')
sn.addComponent(pc)

scale = 0.01
sn.setScale(scale, scale, scale)
#sn.setPosition(-5, 1, -10)

pc.setPointScale(scale)

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
# UI
from omium import *
import porthole
from overlay import *

o = Omium.getInstance()

porthole.initialize(4080, './fireflyUi.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')
ps.setConnectedCommand('onClientConnected()')

print "KEYMAP: " ,Keyboard.KEY_A
def loadUi():
    global gui
    global p
    gui = Overlay()
    p = o.getPixels()
    gui.setTexture(p)
    gui.setAutosize(True)
    o.setZoom(3)
    o.open('http://localhost:4080')
    onResize()

getDisplayConfig().canvasChangedCommand = 'onResize()'

def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])

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
    pc.setFilter(variableDict[variables[int(filterName)]])
    pc.setFilterBounds(minRange/100.0, maxRange/100.0)
    return False

def setColorBounds(minRange, maxRange, setName):
    return False

def setLogColor(isLog, setName):
    # return False
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

def setFilter(isOn, variable, setName):
    return False