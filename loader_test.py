import os,sys

from readsnap import readsnap
import np_tools

import numpy as np 
global colormapMin,colormapMax

def read_test_snap():
    import h5py
    pathh="test_snap.hdf5"
    res = {}
    with h5py.File(pathh,'r') as snap:
	coords0 = np.array(snap['PartType0/Coordinates'])
	coords4 = np.array(snap['PartType4/Coordinates'])
    res['P0Coords']=coords0
    res['P4Coords']=coords4
    return res
    
#read in snapshot data
print "Loading test snapshot..."
res = read_test_snap()

#l = HDF5Loader() <--- deprecated
l = NumpyLoader()

#first argument can be anything but you will reference it later
l.addDimension('P0Coordinates',res['P0Coords'])
l.addDimension('P4Coordinates',res['P4Coords'])

#that's legacy from HDF5 loader
ds0 = Dataset.create('PartType0')
ds4 = Dataset.create('PartType4')

#tell dataset where to get its info from
ds0.setLoader(l)
ds4.setLoader(l)

# 1-> array to get, 2-> should almost always be float, 
# 3-> index for vector variables (0 if single dimensional)
# 4->potentially another arbitrary label that is legacy
x0 = ds0.addDimension('P0Coordinates', DimensionType.Float,0,'x')
y0 = ds0.addDimension('P0Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('P0Coordinates', DimensionType.Float, 2, 'z')


x4 = ds0.addDimension('P4Coordinates', DimensionType.Float,0,'x')
y4 = ds0.addDimension('P4Coordinates', DimensionType.Float, 1, 'y')
z4 = ds0.addDimension('P4Coordinates', DimensionType.Float, 2, 'z')

pc0 = PointCloud.create('pc0')
pc0.setOptions(pointCloudLoadOptions)


pc4 = PointCloud.create('pc4')
pc4.setOptions(pointCloudLoadOptions)

#this is very different usage of dimension from above, this
#sets x,y,z coordinates in sim
pc0.setDimensions(x0,y0,z0)
pc4.setDimensions(x4,y4,z4)

#can also take an RGBA string, used if no adv cmap
pc0.setColor(Color('red'))
pc0.setPointScale(pointScale)


pc4.setColor(Color('blue'))
pc4.setPointScale(pointScale)
#for easy iteration
#parts = [pc0,pc4]
pc0=pc4
parts = [pc0]

#default will be the first that appears in the list
dataModes = ['Point']

#firefly looks for this specific function, it *must* exist
#otherwise will crash
def setDataMode(mode):
    """mode is an index and is exported to the 
	global variable dataMode, then used to pick 
	out from list above"""
    global dataMode 
    dataMode = mode
    dm = dataModes[mode]
	
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
	#enableSmoothingLength(False)
    redraw()
