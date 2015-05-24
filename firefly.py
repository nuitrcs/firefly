from cyclops import *
from pointCloud import *
from omegaToolkit import *
from math import *
import sys
import PointSet
import Manipulator

#--------------------------------------------------------------------------------
# Dataset
galaxy = [
          PointSet.PointSet('data_0.xyzb', Color(0.05, 0.05, 0.05, 1), 0.2),
          PointSet.PointSet('data_1.xyzb', Color(1, 0.1, 0.1, 1), 0.2),
          PointSet.PointSet('data_2.xyzb', Color(0.5, 0.5, 0.0, 1), 2),
          PointSet.PointSet('data_4.xyzb', Color(0, 0, 0.2, 1), 2)
          ]

# Point set 0 is rendered with a 'gas' renderer, but right now this is the same
# as the star renderer. Also use a different texture for the points
galaxy[0].material.setProgram(PointSet.gasProgram.name)
galaxy[0].material.setDiffuseTexture('gas.png')

#--------------------------------------------------------------------------------
# Scene setup
scene = getSceneManager()
SceneNodeHitPointsFlag = 1 << 16;
# This uniform stores the window size. Needed for the star rendering shader.
windowSize = Uniform.create('windowSize', UniformType.Vector2f, 1)

# Add the window size unform to the point set materials
# and all all of them to the pivot node
pivot = SceneNode.create('pivot')
for ps in galaxy:
    ps.material.attachUniform(windowSize)
    pivot.addChild(ps.object)
    ps.object.setFlag(SceneNodeHitPointsFlag)

pivot.setScale(0.4,0.4,0.4)
Manipulator.root = pivot

# Set the camera background and default movement speed.
c = getDefaultCamera()
c.setBackgroundColor(Color('black'))
c.getController().setSpeed(50)


#--------------------------------------------------------------------------------
# User interface
uim = UiModule.createAndInitialize()
panel = Container.create(ContainerLayout.LayoutVertical, uim.getUi())
panel.setStyle('fill: #303030a0')
headerRow = Container.create(ContainerLayout.LayoutHorizontal, panel)
l1 = Label.create(headerRow)
l1.setText('Dataset Name')
l1.setAutosize(False)
l1.setWidth(120)
l2 = Label.create(headerRow)
l2.setText('Visible')
l2.setStyle('align: middle-left')
l2.setAutosize(False)
l2.setWidth(100)
l3 = Label.create(headerRow)
l3.setText('Intensity')
i = 0
for ps in galaxy:
    psRow = Container.create(ContainerLayout.LayoutHorizontal, panel)
    psl = Label.create(psRow)
    psl.setText(ps.model.name)
    psl.setWidth(150)
    psl.setAutosize(False)
    vb = Button.create(psRow)
    vb.setCheckable(True)
    vb.setChecked(True)
    vb.getLabel().setVisible(False)
    sld = Slider.create(psRow)
    # Remove horizontal navigation so we can use left/right arrow to set
    # the slider value
    sld.setHorizontalPrevWidget(None)
    
    # Hook events
    vb.setUIEventCommand('toggle({0})'.format(i))
    sld.setUIEventCommand('setPointSize({0}, %value%)'.format(i))
    i = i + 1

def setPointSize(id, i):
    galaxy[id].pointScale.setFloat(float(i) / 100 )

def toggle(id):
    galaxy[id].object.setVisible(not galaxy[id].object.isVisible())
    print(galaxy[id].object.isVisible())

#--------------------------------------------------------------------------------
# Add a window resized callback (and call it once when the program starts)
def windowResized():
    dc = getDisplayConfig()
    cr = dc.getCanvasRect()
    windowSize.setVector2f(Vector2(cr[2], cr[3]))
    #print('[windowResized] <{0}>x<{1}>'.format(cr[2], cr[3]))
getDisplayConfig().canvasChangedCommand = 'windowResized()'
windowResized()


#--------------------------------------------------------------------------------
# Utility functions and program start

# Center the datasets on a common pivot node, to ease rotation around the dataset
def center():
    global s, zf, k
    for ps in galaxy:
        ps.object.setPosition(-437, -148, -579)
    getDefaultCamera().setPosition(0,0,200)

# Utility shortcut function to recompile shaders
def rs():
    scene.reloadAndRecompileShaders()

# Utility shortcut function to resize all points
def ps(v):
    for ps in galaxy:
        ps.pointScale.setFloat(v)

center()
queueCommand(':autonearfar on')
ps(0.1)