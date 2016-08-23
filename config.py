# use this code to load multipart files
datasetBase = '/Volumes/Windows/dev/snapdir_440/'
files = []
for i in range(0, 4):
    files.append(datasetBase + 'snapshot_440.' + str(i) + '.hdf5')
datasetPath = ';'.join(files)

# use this to load a single file.
# <<<<<<< Updated upstream
# datasetPath = '/Volumes/Windows/dev/omegalib/apps/firefly/snapshot_140.hdf5'
# =======
datasetPath = 'C:/Users/defaultuser0/snapshot_140.hdf5'
# >>>>>>> Stashed changes


# Initial pivot.
pivotPosition = Vector3(47, 17, 62)

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
scale = 0.01
