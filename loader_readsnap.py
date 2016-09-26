from readsnap import *

# Read data from the hdf5 file using the readnsap script,
# then register the loaded numpy arrays with their right dimension
# names, so the Dataset class can access them.
l = NumpyLoader()
res = readsnap(datasetPath, snapshotNumber, 0)
print res
l.addDimension('Coordinates', res['p'])
l.addDimension('Velocities', res['v'])
l.addDimension('Mass', res['m'])

# # PartType0
ds0 = Dataset.create('PartType0')
ds0.setLoader(l)

x0 = ds0.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
m0 = ds0.addDimension('Masses', DimensionType.Float, 0, 'm')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')

#m0 = ds0.addDimension('Masses', DimensionType.Float,0, 'm')
#e0 = ds0.addDimension('InternalEnergy',DimensionType.Float,0,'e')

pc0 = PointCloud.create('pc0')
pc0.setOptions(pointCloudLoadOptions)
pc0.setDimensions(x0, y0, z0)
pc0.setColor(Color('red'))
pc0.setPointScale(0.01)
parts = [pc0]

dataModes = [
    'DataType', 
    'Masses']
    
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
    redraw()
    
setDataMode(0)