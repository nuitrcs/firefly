from signac import *
import Navigator

sig = Signac.getInstance()

prog = sig.addProgram('points')
prog.setVertexShader('shaders/point.vert')
prog.setGeometryShader('shaders/point.geom')
prog.setFragmentShader('shaders/point.frag')
prog.setColormapShader('shaders/colormaps.frag')

prog.define('colormap', 'colormap_default');

l = BinaryLoader()
l.open('C:/Users/Larry/data_0.xyzb')

ds = Dataset.create('darkMatter')
ds.setDoublePrecision(False)
ds.setLoader(l)

x = ds.addDimension('X', DimensionType.Float)
y = ds.addDimension('Y', DimensionType.Float)
z = ds.addDimension('Z', DimensionType.Float)
variableDict = {}
smoothingLength = ds.addDimension('SmoothingLength', DimensionType.Float)
variableDict["Smoothing Length"] = smoothingLength
density = ds.addDimension('Density', DimensionType.Float)
variableDict["Density"] = density
energy = ds.addDimension('InternalEnergy', DimensionType.Float)
variableDict["Internal Energy"] = energy
sfr = ds.addDimension('StarFormationRate', DimensionType.Float)
variableDict["Formation Rate"] = sfr

pc = PointCloud()
pc.setOptions('100000 0:100000:10')
pc.setDimensions(x, y, z)
pc.setData(0, smoothingLength)
pc.setProgram(prog)


sn = SceneNode.create('galaxy')
sn.addComponent(pc)

scale = 0.1
sn.setScale(scale, scale, scale)
#sn.setPosition(-5, 1, -10)

p = prog.getParams()
p.pointScale = 0.05

# set camera near / far z to some reasonable value
# this is needed to make slicing work.
getDefaultCamera().setNearFarZ(1, 100000)

# Hardcoded initial pivot.
Navigator.pivotPosition = Vector3(47, 17, 62)
Navigator.focus()

filterStart = 0.0
filterEnd = 1.0
colormap = 'colormap_default'

def onEvent():
    global colormap
    
    e = getEvent()
    if(e.isKeyDown(ord('p'))): prog.reload()
    if(e.isKeyDown(ord('c'))): 
        if(colormap == 'colormap_default'): colormap = 'colormap_div'
        else: colormap = 'colormap_default'
        print('colormap set to ' + colormap)
        prog.define('colormap', colormap)
    if(e.isKeyDown(ord('l'))): 
        if(e.isFlagSet(EventFlags.Shift)): p.pointScale /= 1.5
        else: p.pointScale *= 1.5
    if(e.isKeyDown(ord('l'))): 
        if(e.isFlagSet(EventFlags.Shift)): p.pointScale /= 1.5
        else: p.pointScale *= 1.5
setEventFunction(onEvent)

#-------------------------------------------------------------------------------
# UI
from omium import *
import porthole
from omegaToolkit import *

o = Omium.getInstance()
ui = UiModule.createAndInitialize().getUi()

porthole.initialize(4080, './fireflyUi.html')
ps = porthole.getService()
ps.setServerStartedCommand('loadUi()')
ps.setConnectedCommand('onClientConnected()')

def loadUi():
    global img
    global p
    img = Image.create(ui)
    p = o.getPixels()
    img.setData(p)
    o.setZoom(3)
    o.open('http://localhost:4080')
    onResize()

getDisplayConfig().canvasChangedCommand = 'onResize()'

def onResize():
    r = getDisplayConfig().getCanvasRect()
    o.resize(r[2], r[3])
    img.setSize(Vector2(r[2], r[3]))
    # flip image Y
    img.setSourceRect(0, r[3], r[2], -r[3])

def onClientConnected():
    print "Client has connected"
    colorMapArray = ["colormap_default","colormap_div","colormap_div2","colormap_div3"]
    colorMapLabels = ["Single Color","Division 1","Division 2","Division 3"]
    # ps.broadcastjs('printSomething()', '')
    # ps.broadcastjs('setColorMap(' + str() + ')', '')
    ps.broadcastjs('setColorMapArrays(' + str(colorMapArray) + ',' + str(colorMapLabels) + ')','')
    ps.broadcastjs('addStarPanel(\'Gases\')', '')
    ps.broadcastjs('addStarPanel(\'Dark Matter\')', '')
    ps.broadcastjs('addStarPanel(\'Star Cluster\')', '')
    # ps.broadcastjs('addStarPanel()', '')
    print "finished broadcasting some commands"

def updateStars():
    return False

def setColorMap(colorName, setName):
    global colormap
    colormap = colorName
    prog.define('colormap', colormap)

def setColorVariable(variable, setName):
    pc.setData(0, variableDict[variable])

def setPointSize(size, setName):
    return False

def setFilter(min, max, filterName,setName):
    return False

def setColorRange(min, max, setName):
    return False

def setLog(isLog, setName):
    return False

def setFilter(isOn, variable, setName):
    return False