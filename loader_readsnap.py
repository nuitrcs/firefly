import os,sys

from readsnap import readsnap
import np_tools

import numpy as np 
global colormapMin,colormapMax

#read in snapshot data
print "loading base: " + str(datasetBase) + " number: " + str(snapshotNumber)
res = readsnap(datasetBase,snapshotNumber,0)

#distribute mass throughout a cylinder 
radius = np.power(((res['m'] / res['rho'])/(2 * np.pi) ),(1.0/3.0))
weight = 2 * radius * res['rho']

#orient camera pivot and position on center of mass
if orientOnCoM:
    cameraPosition,pivotPoint,cameraOrientation =np_tools.setCenterOfMassView(res['p'],res['m'],distanceFromCoM) 

#l = HDF5Loader() <--- deprecated
l = NumpyLoader()

#first argument can be anything but you will reference it later
l.addDimension('Coordinates',res['p'])
l.addDimension('Velocities',res['v'])

l.addDimension('SurfaceDensity',weight)
l.addDimension("ParticleRadius",radius)

#2 sigma of the log of the array 
colormapMin,colormapMax = np_tools.setDefaultRanges(weight)

#sets global variable PointScale -> 1
#but could in principle be some function of the radii
np_tools.setDefaultPointScale(radius)

#Make our datasets

#this string might be arbitrary, maybe just an internal label 
#that's legacy from HDF5 loader
ds0 = Dataset.create('PartType0')

#tell dataset where to get its info from
ds0.setLoader(l)

# 1-> array to get, 2-> should almost always be float, 
# 3-> index for vector variables (0 if single dimensional)
# 4->potentially another arbitrary label that is legacy
x0 = ds0.addDimension('Coordinates', DimensionType.Float,0,'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
sd0 = ds0.addDimension('SurfaceDensity', DimensionType.Float, 0, 'sfcden')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')
r0 = ds0.addDimension('ParticleRadius', DimensionType.Float, 0, 'radius')

#setting up point cloud object now

#Probably also arbitrary but we should definitely check this

pc0 = PointCloud.create('pc0')

#set in the config file, basically decimation level
pc0.setOptions(pointCloudLoadOptions)

#this is very different usage of dimension from above, this
#sets x,y,z coordinates in sim
pc0.setDimensions(x0,y0,z0)

#can also take an RGBA string, used if no adv cmap
pc0.setColor(Color('red'))
pc0.setPointScale(pointScale)

#for easy iteration
parts = [pc0]

#consider deleting this now that cololrmapMin/Max exist
#defaultMinScale= 1e-8
#defaultMaxScale= 1e2

#default will be the first that appears in the list
dataModes = ['Surface Density',
    'Point']

#firefly looks for this specific function, it *must* exist
#otherwise will crash
def setDataMode(mode):
    """mode is an index and is exported to the 
	global variable dataMode, then used to pick 
	out from list above"""
    global dataMode 
    dataMode = mode
    dm = dataModes[mode]

    #go through each possible 
    if dm =='Surface Density':
	#this specifies will determine the
	#color, it should be the weight
	pc0.setData(sd0)

	pc0.setSize(r0)
	pc0.setVisible(True)
	#what determines the point cloud will 
	#appear as, prog_channel is filtered through
	#colormap according to its weight
	#prog_fixedColor is whatever you set with setColor
	pc0.setProgram(prog_channel)
	#colormapMin,colormapMax=1e-8,1e2
	updateColormapBounds(colormapMin,colormapMax)	
	
	#can change control panel options for convenience
	#more options available on wiki fireflyUi.py
	enableLogScale(True)
	enableColormapper(True)
	
	#potential legacy option
	enableSmoothingLength(False)
	
    if dm =='Point':
	#removes the capability to use a colormap
	pc0.setData(None)	
	#what does this do?
	pc0.setSize(None)
	pc0.setVisible(True)
	pc0.setProgram(prog_fixedColor)
	
	enableColormapper(False)
	enableLogScale(False)
	
	
	#potential legacy option
	enableSmoothingLength(False)
    redraw()
