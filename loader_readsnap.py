import os, sys
from readsnap import *
#from readsnap_test import *
from np_tools import *
import numpy as np
global colormapMin,colormapMax
# Read data from the hdf5 file using the readnsap script,
# then register the loaded numpy arrays with their right dimension
# names, so the Dataset class can access them.


print "loading base: " + str(datasetBase) + " number: " + str(snapshotNumber)

#Loading the hdf5 file using the "readsnap" function, which returns a numpy array.
res = readsnap(datasetBase, snapshotNumber, 0)
#res = testReadSnap()

#--- Calculate the relevant numpy arrays here!-------#

radius = np.power(((res['m'] / res['rho'])/(2 * np.pi) ),(1.0/3.0))
weight = 2 * radius * res['rho']

#-----------------------------------------------------

comPos, comPivot, comOrientation = setCenterOfMassView(res['p'],res['m'],distanceFromCoM)

if orientOnCoM:
    cameraPosition = comPos
    cameraOrientation = comOrientation
if pivotAtCoM:
    pivotPoint = comPivot

l = NumpyLoader()

l.addDimension('Coordinates', res['p'])
l.addDimension('Velocities', res['v'])
l.addDimension("Size", radius)
setDefaultPointScale(radius)

#------------------------ Add the dimension to the loader here---------------------#
l.addDimension('Mass', weight)
# To set this as a default colormap variable, copy this line and replace with the new dimension
colormapMin, colormapMax = setDefaultRanges(weight) 

#----------------------------------------------------------------------------------#

ds0 = Dataset.create('PartType0')
ds0.setLoader(l)

x0 = ds0.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')
s0 = ds0.addDimension('Size', DimensionType.Float, 0, 'size')

#------------------------- Add new Dimensions to dataset here -------------------#

m0 = ds0.addDimension('Mass', DimensionType.Float, 0, 'm')
#--------------------------------------------------------------------------------#

#m0 = ds0.addDimension('Masses', DimensionType.Float,0, 'm')


pc0 = PointCloud.create('pc0')
pc0.setOptions(pointCloudLoadOptions)
pc0.setDimensions(x0, y0, z0)
pc0.setColor(Color('red'))
pc0.setPointScale(0.01)
parts = [pc0]

defaultMinScale = 1e-8
defaultMaxScale = 1e2

#----------To add a new option in the UI, add a new string here-----------
dataModes = [
    'Masses', 
    'DataType', 
    'oldDataType',
    'MassesNoS']
#---------------------------------

def setDataMode(mode):
    global dataMode
    dataMode = mode
    dm = dataModes[mode]
    if(dm == 'DataType'):
        pc0.setData(None)
        pc0.setSize(s0)
        pc0.setVisible(True)
        # pc0.setProgram(prog_channel)
        pc0.setProgram(prog_fixedColor)
        pc0.setColor(Color(0.2, 0.2, 1, 0.1))
    elif (dm == 'oldDataType'):
        pc0.setData(None)
        pc0.setSize(None)
        pc0.setVisible(True)
        pc0.setProgram(prog_fixedColor)
        pc0.setColor(Color(0.2, 0.2, 1, 0.1))
    elif(dm == 'Masses'):
        pc0.setData(m0)        
        # pc0.setData(None)
        pc0.setSize(s0)
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        updateColormapBounds(colormapMin, colormapMax )
        enableSmoothingLength(False)
        enableColormapper(True)
        enableLogScale(True)
    elif(dm == 'MassesNoS'):
        pc0.setData(m0)        
        # pc0.setData(None)
        pc0.setSize(None)
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        updateColormapBounds(setDefaultRanges(weight) )

        enableSmoothingLength(False)
        enableColormapper(True)
    redraw()
# setDataMode(0)