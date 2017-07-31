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

def addDimensionToPC(self,key,value):
    self.dataset.l.addDimension(key,value)
    dim = self.dataset.addDimension(key,DimensionType.Float,0,key.lower()+'_dsdim')
    try:
	self.dims+=[dim]
    except AttributeError:
	self.dims=[dim]
	dim.__class__.__repr__=lambda self: self.label
    return dim


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

    def getPointcloud(self,res,keys,color,lowres=0):
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

	#every dataset is called parttype0
	ds = Dataset.create('PartType0')
	#tell dataset where to get its info from
	ds.setLoader(l)
	
	ds.l = l

	#wrapper point cloud that adds a method above
	pc = PointCloud.create('pc%s'%color)

	pc.res = res
	pc.loader = self
    	pc.dataset = ds


	#make it a bound method...
	pc.addDimensionToPC=addDimensionToPC.__get__(pc,pc.__class__)

	#assert that whatever you're loading has spatial coordinates 
	#and spatial velocities?
	try:
	    assert 'p' in keys
	    assert 'v' in keys
	except AssertionError:
	    print keys
	    raise Exception("You need to specify the 3d positions using the 'p' key")

	l.addDimension('Coordinates',res['p'])
	l.addDimension('Velocities',res['v'])   

	# 1-> array to get, 2-> should almost always be float, 
	# 3-> index for vector variables (0 if single dimensional)
	# 4->potentially another arbitrary label that is legacy
	pc.x_dim = ds.addDimension('Coordinates', DimensionType.Float,0,'x')
	pc.y_dim = ds.addDimension('Coordinates', DimensionType.Float, 1, 'y')
	pc.z_dim = ds.addDimension('Coordinates', DimensionType.Float, 2, 'z')
	pc.vx_dim = ds.addDimension('Velocities', DimensionType.Float, 0, 'vx')
	pc.vy_dim = ds.addDimension('Velocities', DimensionType.Float, 1, 'vy')
	pc.vz_dim = ds.addDimension('Velocities', DimensionType.Float, 2, 'vz')
	

	if 'rho' in keys:	
	    radius = np.power(((res['m'] / res['rho'])/(2 * np.pi) ),(1.0/3.0))
	    pc.gas_sd = 2 * radius * res['rho']
	    self.orientCamera(res,pc.gas_sd,radius)
	    pc.gas_sd_dim = pc.addDimensionToPC('SurfaceDensity',pc.gas_sd)
	    pc.gas_r_dim = pc.addDimensionToPC('ParticleRadius',radius)
	
	    #metal surface density 
	    pc.gas_met_sd = 2 * radius * res['rho']*res['z'][:,0]
	    pc.gas_met_sd_dim = pc.addDimensionToPC('MetalSurfaceDensity',pc.gas_met_sd)
	    
	    #sfr
	    pc.gas_sfr = res['sfr']
	    pc.gas_sfr_dim = pc.addDimensionToPC('GasSFR',pc.gas_sfr)
	    
	    pc.is_gas_particles = True
    
	else:
	    shape = res['m'].shape

	    #track dummy arrays just in case
	    pc.gas_sd_dim = pc.addDimensionToPC('SurfaceDensityDummy',np.zeros(shape=shape))
	    pc.gas_r_dim = pc.addDimensionToPC('ParticleRadiusDummy',np.ones(shape=shape))
	    pc.is_gas_particles = False

	if lowres:
	    pointCloudLoadOptions = "50000 0:100000:100"
	else:
	    pointCloudLoadOptions = "50000 0:100000:20"
	    
	pc.setOptions(pointCloudLoadOptions)

	#this is very different usage of dimension from above, this
	#sets x,y,z coordinates in sim
	pc.setDimensions(pc.x_dim,pc.y_dim,pc.z_dim)
	
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
	dataModes = ['Point','Surface Density','Metal Surface Density','SFR','Velocities']
	
	#why are these lines here?
	## stores index in global variable
	dataMode = mode
	## extracts index once for lines below...
	dm = dataModes[mode]

	#go through each possible 
	## should consider replacing dataModes with a list of functions
	## that takes parts as an argument...

	if dm not in ['SFR']:  
	    # certain datamodes look better if you change the decimation
	    #SFR is one of them, want to reset it in case you were just in 
	    #one of them. 
	    setDecimationValue(10)
	    pass
	    

	if dm =='Surface Density':
	    for pci,pc in enumerate(parts):
		if pc.is_gas_particles:
		    pc.setProgram(prog_channel)
		    pc.setSize(None)
		    pc.setVisible(True)
		    pc.setData(pc.gas_sd_dim)
		    #update colormap bounds to 5 sigma in either logspace or not
		    updateColormapBounds(*np_tools.setDefaultRanges(pc.gas_sd))
		else:
		    #pc.setData(None)
		    #pc.setSize(None)
		    #pc.setProgram(prog_channel)
		    pc.setVisible(False)

	    enableLogScale(True)
	    enableColormapper(True)
	    
	elif dm =='Point':
	    for pci,pc in enumerate(parts):
	      pc.setProgram(prog_fixedColor)
	      pc.setData(None)	
	      pc.setSize(None)
	      pc.setVisible(True)

	    enableColormapper(False)
	    enableLogScale(False)
	elif dm =='Metal Surface Density':
	    for pci,pc in enumerate(parts):
		if pc.is_gas_particles:
		    pc.setProgram(prog_channel)
		    pc.setSize(None)
		    pc.setVisible(True)
		    pc.setData(pc.gas_met_sd_dim)

		    #update colormap bounds to 5 sigma in either logspace or not
		    updateColormapBounds(*np_tools.setDefaultRanges(pc.gas_met_sd))

		else:
		    #pc.setData(None)
		    #pc.setSize(None)
		    #pc.setProgram(prog_channel)
		    pc.setVisible(False)

	    enableLogScale(True)
	    enableColormapper(True)
	elif dm =='SFR':
	    for pci,pc in enumerate(parts):
		if pc.is_gas_particles:
		    pc.setProgram(prog_channel)
		    pc.setSize(None)
		    pc.setVisible(True)
		    pc.setData(pc.gas_sfr_dim)


		    #update colormap bounds to 5 sigma in either logspace or not
		    updateColormapBounds(*np_tools.setDefaultRanges(pc.gas_sfr))
		else:
		    #pc.setData(None)
		    #pc.setSize(None)
		    #pc.setProgram(prog_channel)
		    pc.setVisible(False)
	    enableLogScale(True)
	    enableColormapper(True)
	    setDecimationValue(1)
	elif dm =='Gas Velocities':
	    for pci,pc in enumerate(parts):
		if pc.is_gas_particles:
		    pc.setVisible(True)
		    pc.setProgram(prog_vector)
		    pc.setVectorData(pc.vx_dim,pc.vy_dim,pc.vz_dim)
		else:
		    pc.setVisible(False)
	    
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
	global cameraPosition,pivotPoint,cameraOrientation
	#orient camera pivot and position on center of mass
	if orientOnCoM:
	    cameraPosition,pivotPoint,cameraOrientation=np_tools.setCenterOfMassView(res['p'],res['m'],distanceFromCoM) 

	#2 sigma of the log of the array 


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

for i,ptype in enumerate([0,1,4][:3]):
    res = loader.importParticleData(ptype)
    ## strictly this should be a list *only* of the keys that we care about
    #	that way we can loop over them to be a bit more general in the future. 
    keys=['p','v']
    keys=res.keys()
    pc = loader.getPointcloud(res,keys,colors[i],lowres=ptype==1)


    #for easy iteration
    parts+=[pc]

#hacky way to pass setDataMode wherever it needs to be... 
global setDataMode
setDataMode=loader.setDataMode

