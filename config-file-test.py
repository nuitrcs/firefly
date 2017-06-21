# use this code to load multipart files
# datasetBase = 'C:/Users/defaultuser0/omegalib/firefly/modules/firefly'

datasetBase =''
snapshotNumber = 0

# Initial pivot point when rotating the galaxy
# pivotPosition = Vector3(0,0,0)
# cameraPosition = Vector3(0,0,0)
# cameraOrientation = Quaternion()

# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
#scale = 1.0

# change the last number to choose a different decimation level for data loading
pointCloudLoadOptions = "50000 0:100000:1"

#pointCloudLoadOptions = "1 0:1:1"

# This sets the dynamic quality rendering mode. Higher number = faster rendering but
# lower quality
dqDec = 4

# This is the name of the script we want to use to load the file. Different simulation
# snapshots might be outputting different DataParts / columns. You can have a different
# loader script for each simulation output config.


loaderScript = 'firefly/loader_test.py'




#Specifies where images will be saved when a screenshot is created through the user interface.
# imagePath = 'C:/Users/defaultuser0/'
# presetPath = 'C:/Users/defaultuser0/'

#============================Optional Variables===================


# --- Camera Options ---

# Sets the initial pivot point that the galaxy model will rotate around upon starting the application
# pivotPosition = Vector3(0,0,0)

# Sets the initial camera position upon starting the application.
# cameraPosition = Vector3(0,0,0)

#Determines the initial camera orientation when starting the application. Output must be in the form of
# a Quaternion.
# cameraOrientation = Quaternion.new_rotate_axis(1, 0,0,0)

# OrientOnCoM: boolean. If set to true, will start with the camera pointed at the center of mass by default. 
# If set to true, this OVERRIDES the default cameraOrientation and cameraPosition Variables.
orientOnCoM = True
#distanceFromCoM: float, only used if OrientToCoM is true. Specifies the distance between the initial camera and
# the center of mass as a ratio of standard deviations. Defaults to 2.0
distanceFromCoM = 2.0


#PivotAtCom: boolean: The initial pivotPoint will also be set to the centerOfMass.
pivotAtCoM = True
#--- Display Variables ---


# Scale to apply to the entire 3D dataset. Useful if the dataset is too large,
# to simplify navigation
#scale = 1.0

#kernelModeInd: integer. Specifies the kernel mode from a few options. 
# 0:    Uniform
# 1:    Smooth
kernelModeInd = 1

#RenderModeInd: integer. Specifies the render mode from a few options. 
# 0:    Standard
# 1:    Faded
# 2:    Band5    
renderModeInd = 0

# --- Variable Paths ---

#Specifies where images will be saved when a screenshot is created through the user interface.
# imagePath = 'C:/Users/defaultuser0/'

#Specifies where the preset views options in the "preset panel" will be saved.
# presetPath = 'C:/Users/defaultuser0/'
