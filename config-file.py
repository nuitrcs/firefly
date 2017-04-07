# use this code to load multipart files
#datasetBase = '/Volumes/Windows/dev/snapdir_440/'
print "Loading config-file.py"
datasetBase = 'C:/Users/defaultuser0/omegalib/firefly/modules/firefly'
files = []
for i in range(0, 4):
    files.append(datasetBase + 'snapshot_440.' + str(i) + '.hdf5')
datasetPath = ';'.join(files)

snapshotNumber = 440
# Initial pivot point when rotating the galaxy
pivotPosition = Vector3(0,0,0)
cameraPosition = Vector3(0,0,0)
cameraOrientation = Quaternion()

orientOnCoM = True

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
scale = 1.0

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "40000 0:100000:80"
#pointCloudLoadOptions = "1 0:1:1"

# This sets the dynamic quality rendering mode. Higher number = faster rendering but
# lower quality
dqDec = 4

# This is the name of the script we want to use to load the file. Different simulation
# snapshots might be outputting different DataParts / columns. You can have a different
# loader script for each simulation output config.
loaderScript = 'firefly/loader_readsnap.py'

#Specifies where images will be saved when a screenshot is created through the user interface.
imagePath = 'C:/Users/defaultuser0/'
presetPath = 'C:/Users/defaultuser0/'