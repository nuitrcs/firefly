import os,sys

from readsnap import readsnap
import np_tools

import numpy as np 
global colormapMin,colormapMax

def verifyLoader(loader):
    try:
	loader.importData
	loader.getPointcloud
	loader.setDataMode
    except NameError:
	raise Exception("Invalid Loader")

class Loader(object):
    """Loader class that organizes required parts of loader script 
	for verification. Standardizes class format for any additional loader classes."""
    def __init__(self,snapdir,snapnum):
	self.snapdir=snapdir
	self.snapnum=snapnum

    def importData(self,parttype=0):
	"""
	Input:
	    parttype - The numerical index of the particle type you want
	Output:
	    res - A dictionary that contains information for a *single* pointcloud!
	"""
	import h5py
	pathh="test_snap.hdf5"
	res = {}
	with h5py.File(pathh,'r') as snap:
	    coords = np.array(snap['PartType%d/Coordinates'%parttype])

	res['p']=coords
	return res

    def getPointcloud(self,res,keys,color):
	"""
	Input:
	    res - the dictionary containing information for the pointcloud you're creating
	    keys - the keys that are relevant for your res dictionary that you want to load
		into a dataset object for future use. This *shouldn't* be all the keys in res, 
		in general, just the ones you anticipate needing. 
	    color - the color of the points when no advanced colormap is used. This is also 
		used to indentify the pointclouds, so they should *not* overlap (if you think
		they should they shouldn't-- you should merge your data to be a single point
		cloud instead of having two representing subsets of data that should be the same
		color). 
	Output:
	    pc - a pointcloud object
	"""

	l = NumpyLoader()

	#assert that whatever you're loading has spatial coordinates 
	try:
	    assert 'p' in keys
	except AssertionError:
	    raise Exception("You need to specify the 3d positions using the 'p' key")

	l.addDimension('Coordinates',res['p'])
	for key in keys:
	    if key =='p':
		continue
	    #add each key into the loader
	    l.addDimension(key+color,res[key])

	ds = Dataset.create('PartType%s'%color)
	#tell dataset where to get its info from
	ds.setLoader(l)


	# 1-> array to get, 2-> should almost always be float, 
	# 3-> index for vector variables (0 if single dimensional)
	# 4->potentially another arbitrary label that is legacy
	x = ds.addDimension('Coordinates', DimensionType.Float,0,'x')
	y = ds.addDimension('Coordinates', DimensionType.Float, 1, 'y')
	z = ds.addDimension('Coordinates', DimensionType.Float, 2, 'z')

	for key in keys:
	    if key =='p':
		continue
	    #add each key into the dataset
	    ds.addDimension(key+color,DimensionType.Float,0,key)

	pc = PointCloud.create('pc%s'%color)
	pc.setOptions(pointCloudLoadOptions)

	#this is very different usage of dimension from above, this
	#sets x,y,z coordinates in sim
	pc.setDimensions(x,y,z)
	
	#can also take an RGBA string, used if no adv cmap
	pc.setColor(Color(color))
	pc.setPointScale(pointScale)

	return pc

    
    def setDataMode(self,mode):
	"""mode is an index and is exported to the 
	    global variable dataMode, then used to pick 
	    out from list above"""
	global dataMode,dataModes
	dataMode = mode
	dataModes=['Point']
	self.dataModes=dataModes
	dm = dataModes[mode]

	if dm =='Point':

	    # Loop over each point cloud object
	    # If we don't loop over every object, and do something with it, we crash.
	    for pci in parts:

	      #removes the capability to use a colormap
	      pci.setData(None)	
	      #what does this do?
	      pci.setSize(None)
	      pci.setVisible(True)
	      pci.setProgram(prog_fixedColor)

	    enableColormapper(False)
	    enableLogScale(False)
	    
	    #potential legacy option
	    #enableSmoothingLength(False)
	redraw()

#### Ideally this is moved inside the Loader class as well... 
#   impossible until we create a class that can hold parts and
#   has a loader attribute to keep track of the loader that was used. 

print "Loading test snapshot..."
loader = Loader(datasetBase,snapshotNumber)

#read in snapshot data
parts=[]
colors = ['red','yellow','blue']
keys = ['p']


for i,ptype in enumerate([0,1,4]):
    res = loader.importData(ptype)
    pc = loader.getPointcloud(res,keys,colors[i])

    #for easy iteration
    parts+=[pc]

print "Loaded",len(parts),"pointclouds..."

#hacky way to pass setDataMode wherever it needs to be... 
global setDataMode
setDataMode=loader.setDataMode
