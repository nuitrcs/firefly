import numpy as np
import math
from euclid import *

def setCenterOfMassView(pos, mass, distanceRatio):
    # global cameraPosition
    #global pivotPoint, cameraPosition, cameraOrientation
    center = np.average(pos,0,np.ravel(mass))
    pivPoint = Vector3(center[0],center[1],center[2])
    std = np.std(pos,0)
    zZoom = std[2] * distanceRatio
    print "Dist ratio: " + str(distanceRatio) + " :zZoom: " + str(zZoom)
    #print zZoom
    camPos = Vector3(center[0] + zZoom,center[1] + zZoom ,center[2] + zZoom)
    print camPos
    camOrientation = Quaternion()
    #print cameraOrientation
    return camPos, pivPoint, camOrientation

def setDefaultRanges(val,logflag=1):
    if logflag:
	try:
	    assert (val > 0).all()
	    val=np.log10(val)
	except AssertionError:
	    print 'Log scale colorbounds but some values are 0, excising them'
	    val=np.log10(val[val>0])
    center = np.mean(val)
    std = np.std(val)

    minB,maxB = center-5*std,center+5*std
    if logflag:
	minB,maxB=10**minB,10**maxB
    colormapMin,colormapMax = max(minB,1e-8),min(maxB,100)
    return colormapMin,colormapMax

def setDefaultDec(val):
    pass

def setDefaultPointScale(sizeNPArray):
    global pointScale
    pointScale = 1.0
    average = np.average(np.ravel(sizeNPArray))
    print "Average point size: " + str(average)
