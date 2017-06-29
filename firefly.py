from overlay import *
from signac import * 
import os, csv
from omium import *
import porthole
import datetime
import os

# # Initialize the signac point cloud rendering module. Whenever new data is loaded
# # call the redraw function to refresh the screen.
sig = Signac.getInstance()
sig.setFieldLoadedCommand('redraw()')

# setup the camera
camera = getDefaultCamera()
camera.setBackgroundColor(Color('black'))
camera.setNearFarZ(1, 100000)

#-------------------------------------------------------------------------------
# Load the configuration file and loader script
# If we don't have a config file, just open the firefly splash screen.
if(datasetBase == None and datasetPath == None):
    orun('splash.py')
else:
    # Load firefly components
    try:
        orun('colormapConfig.py')
    except:
        print "error detected"
        
    orun('render.py')
    orun('flyControl.py')
    orun('appstate.py')
    orun(loaderScript)

    orun('scene.py')
    orun('fireflyUi.py')
    orun('preset.py')


    setDataMode(dataMode)
    print 'set data mode'
    setColormap(currentColorMapIndex)
    print 'set color map'
    setKernelMode(kernelModeInd)
    print 'set kernel mode'
    setRenderMode(renderModeInd)
    print 'set render mode'
    setCamPos(cameraPosition.x,cameraPosition.y,cameraPosition.z)
    print 'set cam pos'
    setPivotPoint(pivotPoint.x,pivotPoint.y,pivotPoint.z)
    print 'set pivot point'
    setPointScale(pointScale)
    print 'set point scale'
    focus()
    print 'focused'
