import os,sys

from readsnap import readsnap
import np_tools

import numpy as np 

def verifyLoader(loader):
    try:
	loader.importParticleData
	loader.getPointcloud
	loader.setDataMode
    except NameError:
	raise Exception("Invalid Loader")

class Loader(object):
    """Loader class that organizes required parts of loader script 
	for verification. Standardizes class format for any additional loader classes."""
    def __init__(self,snapdir,snapnum):
	"""
	Saves the arguments to the structure. 
	Input: 
	    datasetBase - path to the dataset
	    snapshotNumber - which snapshot we want
	"""
	self.snapdir=snapdir

	self.snapnum=snapnum

    def importParticleData(self,ptype):
	"""
	Reads data in from whatever format you'd like.
	Input:
	    ptype - The numerical index of the particle type you want
	Output:
	    res - A dictionary that contains information for a *single* pointcloud!
	"""
	#we have a function of exactly this format, how convenient (/sarcasm)!
	return readsnap(self.snapdir,self.snapnum,ptype)

    def getPointcloud(self,res,keys,color):
	"""
	Creates a pointcloud object out of a particle dictionary, res. 
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
	l.addDimension('Velocities',res['v'])

	if 'rho' in keys:
	    radius = np.power(((res['m'] / res['rho'])/(2 * np.pi) ),(1.0/3.0))
	    weight = 2 * radius * res['rho']
	    self.orientCamera(res,weight,radius)
	    l.addDimension('SurfaceDensity',weight)
	    l.addDimension("ParticleRadius",radius)
	    

	ds = Dataset.create('PartType%s'%color)
	#tell dataset where to get its info from
	ds.setLoader(l)


	# 1-> array to get, 2-> should almost always be float, 
	# 3-> index for vector variables (0 if single dimensional)
	# 4->potentially another arbitrary label that is legacy
	x = ds.addDimension('Coordinates', DimensionType.Float,0,'x')
	y = ds.addDimension('Coordinates', DimensionType.Float, 1, 'y')
	z = ds.addDimension('Coordinates', DimensionType.Float, 2, 'z')
	vx = ds.addDimension('Velocities', DimensionType.Float, 0, 'vx')
	vy = ds.addDimension('Velocities', DimensionType.Float, 1, 'vy')
	vz = ds.addDimension('Velocities', DimensionType.Float, 2, 'vz')


	if 'rho' in keys:	
	    self.gas_sd = ds.addDimension('SurfaceDensity', DimensionType.Float, 0, 'sfcden')
	    self.gas_r = ds.addDimension('ParticleRadius', DimensionType.Float, 0, 'radius')

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
	#default will be the first that appears in the list
	dataModes = ['Surface Density','Point']
	
	#why are these lines here?
	## stores index in global variable
	dataMode = mode
	## extracts index once for lines below...
	dm = dataModes[mode]

	#go through each possible 
	## should consider replacing dataModes with a list of functions
	## that takes parts as an argument...
	if dm =='Surface Density':
	    for pci,pc in enumerate(parts):
		#assumes gas particles are at 0th index
		#ideally this is changed later to refer 
		#to an attribute or something...
		if pci == 0:
		    #this specifies will determine the
		    #color, it should be the weight
		    pc.setData(self.gas_sd)

		    pc.setSize(self.gas_r)
		    pc.setVisible(True)
		    #what determines the point cloud will 
		    #appear as, prog_channel is filtered through
		    #colormap according to its weight
		    #prog_fixedColor is whatever you set with setColor
		    pc.setProgram(prog_channel)
		    #colormapMin,colormapMax=1e-8,1e2
		else:
		    ## not sure what this needs to not crash
		    pc.setData(None)	
		    #what does this do?
		    pc.setSize(None)
		    pc.setVisible(False)
		    pc.setProgram(prog_fixedColor)

	    updateColormapBounds(colormapMin,colormapMax)	
	    
	    #can change control panel options for convenience
	    #more options available on wiki fireflyUi.py
	    enableLogScale(True)
	    enableColormapper(True)
	    
	elif dm =='Point':
	    # Loop over each point cloud object
	    # If we don't loop over every object, and do something with it, we crash.
	    for pci,pc in enumerate(parts):

	      #removes the capability to use a colormap
	      pc.setData(None)	
	      #what does this do?
	      pc.setSize(None)
	      pc.setVisible(True)
	      pc.setProgram(prog_fixedColor)

	    enableColormapper(False)
	    enableLogScale(False)
	    
	redraw()

    def orientCamera(self,res,weight,radius):
	""" 
	Initializes the camera pointing towards the center of mass of the given
	    particle dictionary, res. Additionally (included here for brevity) 
	    sets the colormap bounds and point scale according to the density 
	    of the gas particles (here weight/radius is assumed to be taken 
	    from the gas particles but in principle could be anything). 
	Input:
	    res - 
	    weight - 
	    radius - 
	Modifies:
	    cameraPosition - 
	    pivotPoint -
	    cameraOrientation - 
	    colormapMin - 
	    colormapMax - 
	    PointScale - 
	"""
	global colormapMin,colormapMax
	#orient camera pivot and position on center of mass
	if orientOnCoM:
	    cameraPosition,pivotPoint,cameraOrientation=np_tools.setCenterOfMassView(res['p'],res['m'],distanceFromCoM) 

	#2 sigma of the log of the array 
	colormapMin,colormapMax = np_tools.setDefaultRanges(weight)

	#sets global variable PointScale -> 1
	#but could in principle be some function of the radii
	np_tools.setDefaultPointScale(radius)



#### Ideally this is moved inside another class as well... 
#   impossible until we create a class that can hold parts and
#   has a loader attribute to keep track of the loader that was used. 

print "loading base: " + str(datasetBase) + " number: " + str(snapshotNumber)
loader = Loader(datasetBase,snapshotNumber)

#read in snapshot data
parts=[]
colors = ['red','yellow','blue']


for i,ptype in enumerate([0,1,4][:1]):
    res = loader.importParticleData(ptype)
    ## strictly this should be a list *only* of the keys that we care about
    #	that way we can loop over them to be a bit more general in the future. 
    keys=res.keys()
    pc = loader.getPointcloud(res,keys,colors[i])


    #for easy iteration
    parts+=[pc]

#hacky way to pass setDataMode wherever it needs to be... 
global setDataMode
setDataMode=loader.setDataMode


