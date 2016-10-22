from readsnap import *
import numpy as np

# Read data from the hdf5 file using the readnsap script,
# then register the loaded numpy arrays with their right dimension
# names, so the Dataset class can access them.
l = NumpyLoader()
res = readsnap(datasetPath, snapshotNumber, 0)
print res
l.addDimension('Coordinates', res['p'])
l.addDimension('Velocities', res['v'])
l.addDimension('Mass', res['m'])

########################################################################
# DEBUG
# Get galaxy sizes and mass
# DEBUG
#r = (res['m']/(2*np.pi*res['rho']))**(1./3.)
r = 1.
# DEBUG
#w = 2*res['rho']*r
w = 2.
l.addDimension('Radius', r)
l.addDimension('Weight', w)
########################################################################

# # PartType0
ds0 = Dataset.create('PartType0')
ds0.setLoader(l)

x0 = ds0.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
m0 = ds0.addDimension('Mass', DimensionType.Float, 0, 'm')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')
r0 = ds0.addDimension('Radius', DimensionType.Float, 0, 'r')

#m0 = ds0.addDimension('Masses', DimensionType.Float,0, 'm')
#e0 = ds0.addDimension('InternalEnergy',DimensionType.Float,0,'e')

pc0 = PointCloud.create('pc0')
pc0.setOptions(pointCloudLoadOptions)
pc0.setDimensions(x0, y0, z0)
pc0.setColor(Color('blue'))
pc0.setPointScale(0.01)
parts = [pc0]

dataModes = [
    'DataType', 
   # 'Masses',
   # 'Accurate',
    ]
    
def setDataMode(mode):
    global dataMode
    dataMode = mode
    dm = dataModes[mode]
    if(dm == 'DataType'):
        pc0.setData(None)
        pc0.setVisible(True)
        pc0.setProgram(prog_fixedColor)
        pc0.setColor(Color(0.2, 0.2, 1, 0.1))

    elif(dm == 'Masses'):
        pc0.setVisible(True)
        pc0.setProgram(prog_vector)
        pc0.setData(m0)
    elif(dm == 'Accurate'):
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        pc0.setData(r0)
    redraw()
    
setDataMode(0)

# Announce completion.
print 'loader done.'
print ''
