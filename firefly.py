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
l.open('C:/dev/omegalib/apps/firefly/snapshot_140.hdf5')

ds = Dataset.create('PartType0')
ds.setLoader(l)

x = ds.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y = ds.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z = ds.addDimension('Coordinates', DimensionType.Float, 2, 'z')
smoothingLength = ds.addDimension('SmoothingLength', DimensionType.Float, 0, 'SmoothingLength')
density = ds.addDimension('Density', DimensionType.Float, 0, 'Density')

pc = PointCloud()
pc.setOptions('100000 0:100000:10')
pc.setDimensions(x, y, z)
pc.setData(smoothingLength)
pc.setSize(smoothingLength)
pc.setProgram(prog)
pc.normalizeFilterBounds(True)
pc.setFilterBounds(0, 1)
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