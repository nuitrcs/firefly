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
if(datasetBase == None):
    orun('splash.py')
else:
    # Load firefly components
    orun('colormapConfig.py')
    orun('render.py')
    orun('flyControl.py')
    orun('appstate.py')
    orun(loaderScript)
    # orun('loader.py')
    orun('scene.py')
    orun('fireflyUi.py')
    orun('preset.py')

    setDataMode(0)
    setColormap(0)
    setKernelMode(1)
    setCamPos(cameraPosition.x,cameraPosition.y,cameraPosition.z)
    setPivotPoint(pivotPoint.x,pivotPoint.y,pivotPoint.z)
    
    setPointScale(pointScale)
    focus()