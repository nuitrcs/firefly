# use this code to load multipart files
snapshotNumber = 440
#datasetBase = '/Users/zhafen/FIRE_Research/Data/m11.9a_2.0_June20_2016/snapdir_{:0>3}/'.format(snum)
datasetPath = '/Users/zhafen/FIRE_Research/Data/m12d_hr_Sept13_2015/snapdir_{:0>3}/'.format(snapshotNumber)

#files = []
#for i in range(0, 4):
#    files.append('{}snapshot_{:0>3}.{}.hdf5'.format(datasetBase, snum, i))
#datasetPath = ';'.join(files)

# Initial pivot point when rotating the galaxy
pivotPosition = Vector3(508, 512, 513)
cameraPosition = Vector3(506, 511, 514)
cameraOrientation = Quaternion()

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
scale = 0.01

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:100"

# This sets the dynamic quality rendering mode. Higher number = faster rendering but
# lower quality
dqDec = 4

# This is the name of the script we want to use to load the file. Different simulation
# snapshots might be outputting different DataParts / columns. You can have a different
# loader script for each simulation output config.
#loaderScript = 'firefly/loader.py'
#loaderScript = '/Users/zhafen/FIRE_Research/Visuals/firefly/loader_readsnap.py'
loaderScript = './loader_readsnap.py'
#loaderScript = './loader.py'

#Specifies where images will be saved when a screenshot is created through the user interface.
imagePath = 'C:/Users/defaultuser0/'
presetPath = 'C:/Users/defaultuser0/'

########################################################################
# DEBUG
import os
print ''
print ''
print 'config-file.py Dir', os.getcwd()
print ''
print ''
print ''
########################################################################

