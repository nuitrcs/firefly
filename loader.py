l = FireLoader()
l.open(datasetPath)

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:1"

# PartType0
ds0 = Dataset.create('PartType0')
ds0.setLoader(l)

x0 = ds0.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y0 = ds0.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z0 = ds0.addDimension('Coordinates', DimensionType.Float, 2, 'z')
sl0 = ds0.addDimension('SmoothingLength', DimensionType.Float, 0, 'SmoothingLength')
d0 = ds0.addDimension('Density', DimensionType.Float, 0, 'Density')
vx0 = ds0.addDimension('Velocities', DimensionType.Float, 0, 'vx')
vy0 = ds0.addDimension('Velocities', DimensionType.Float, 1, 'vy')
vz0 = ds0.addDimension('Velocities', DimensionType.Float, 2, 'vz')

pc0 = PointCloud.create('pc0')
pc0.setOptions(pointCloudLoadOptions)
pc0.setDimensions(x0, y0, z0)
pc0.setColor(Color('red'))

# PartType1
ds1 = Dataset.create('PartType2')
ds1.setLoader(l)

x1 = ds1.addDimension('Coordinates', DimensionType.Float, 0, 'x')
y1 = ds1.addDimension('Coordinates', DimensionType.Float, 1, 'y')
z1 = ds1.addDimension('Coordinates', DimensionType.Float, 2, 'z')

pc1 = PointCloud.create('pc1')
pc1.setOptions(pointCloudLoadOptions)
pc1.setDimensions(x1, y1, z1)
pc1.setColor(Color('blue'))

parts = [pc0, pc1]

def setDataMode(mode):
    global dataMode
    dataMode = mode
    dm = dataModes[mode]
    if(dm == 'DataType'):
        pc0.setVisible(True)
        pc0.setProgram(prog_fixedColor)
        pc0.setColor(Color(0.2, 0.2, 1, 0.1))
        pc1.setVisible(True)
        pc1.setProgram(prog_fixedColor)
        pc1.setColor(Color(1, 1, 0.2, 0.1))
    elif(dm == 'Density'):
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        pc0.setData(d0)
        pc1.setVisible(False)
    elif(dm == 'SmoothingLength'):
        pc0.setVisible(True)
        pc0.setProgram(prog_channel)
        pc0.setData(sl0)
        pc1.setVisible(False)
    elif(dm == 'VelocityVectors'):
        pc0.setVisible(True)
        pc0.setProgram(prog_vector)
        pc1.setVisible(False)
    redraw()