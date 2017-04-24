import numpy as np
import os.path
import scipy.interpolate as interpolate
import scipy.optimize as optimize
import math
from euclid import *

# res = readsnap(datasetPath, snapshotNumber, 0)

def testReadSnap():
	# sdir,snum,ptype,
 #    snapshot_name='snapshot',
 #    extension='.hdf5',
 #    h0=0,cosmological=0,skip_bh=0,four_char=0,
 #    header_only=0,loud=0):

	# if (ptype<0): return {'k':-1};
 #    if (ptype>5): return {'k':-1};

    testTotal = 10
    # initialize variables to be read
    pos=np.zeros(testTotal,dtype=float)
    vel=np.copy(pos)
    ids=np.zeros(testTotal,dtype=long)
    mass=np.zeros(testTotal,dtype=float)

    pos = np.array([[0., 0., -30.],[-5., 0., -30.],[-10., 0., -30.],[5., 0., -30.],[10., 0., -30.],
    	[0., 0., 0.],[0., 0., 5.],[0., 0., 10.],[0., 0., 15.],[0., 0., -5.]])
    vel = np.array([[0., 0., 0.],[0., 0., 0.],[0., 0., 0.],[0., 0., 0.],[0., 0., 0.],
    	[0., 0., 0.],[0., 0., 0.],[0., 0., 0.],[0., 0., 0.],[0., 0., 0.]])
    ids = np.array([1,2,3,4,5,6,7,8,9,10])
    mass = np.array([[1.],[2.],[3.],[2.],[3.],[1.],[2.],[3.],[4.],[5.]])
    smoothingLength = np.array([[1.],[2.],[3.],[2.],[3.],[1.],[1.],[1.],[1.],[1.]])

    return {'s':smoothingLength,'p':pos,'v':vel,'m':mass,'id':ids}
