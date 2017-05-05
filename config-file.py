# use this code to load multipart files
# datasetBase = 'C:/Users/defaultuser0/omegalib/firefly/modules/firefly'
datasetBase = 'C:/Users/defaultuser0/omegalib/snapshots'
# snapshotNumber = 600
snapshotNumber = 50
# snapshotNumber = 440
# Initial pivot point when rotating the galaxy
# pivotPosition = Vector3(0,0,0)
# cameraPosition = Vector3(0,0,0)
# cameraOrientation = Quaternion()

orientOnCoM = True

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
#scale = 1.0

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:20"

#pointCloudLoadOptions = "1 0:1:1"

# This sets the dynamic quality rendering mode. Higher number = faster rendering but
# lower quality
dqDec = 4

# This is the name of the script we want to use to load the file. Different simulation
# snapshots might be outputting different DataParts / columns. You can have a different
# loader script for each simulation output config.
loaderScript = 'C:/Users/defaultuser0/omegalib/loader_readsnap.py' #'firefly/loader_readsnap.py'

#Specifies where images will be saved when a screenshot is created through the user interface.
# imagePath = 'C:/Users/defaultuser0/'
# presetPath = 'C:/Users/defaultuser0/'