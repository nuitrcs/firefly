# use this code to load multipart files
datasetBase = '/Volumes/Windows/dev/snapdir_440/'
files = []
for i in range(0, 4):
    files.append(datasetBase + 'snapshot_440.' + str(i) + '.hdf5')
datasetPath = ';'.join(files)

datasetPath = os.path.abspath('snapshot_600.hdf5')

# Initial pivot.
pivotPosition = Vector3(47, 17, 62)

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
scale = 0.01

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:1"

# This sets the dynamic quality rendering mode. Higher number = faster rendering but
# lower quality
dqDec = 4

# This is the name of the script we want to use to load the file. Different simulation
# snapshots might be outputting different DataParts / columns. You can have a different
# loader script for each simulation output config.
loaderScript = 'firefly/loader.py'