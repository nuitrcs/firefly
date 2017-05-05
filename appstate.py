# default scale applied to points
try:
	scale
	pointScale = scale 
except NameError:
	pointScale = 1.0
	scale = 1.0

try:
	orientOnCoM
except NameError:
	orientOnCoM = False

isLogScale = True                

# data mode. see loader.py
dataMode = 0                     

# filter mode. Used to exclude a data range from rendering
filterMode = None                   
filterMin = 0
filterMax = 1

# colormapper flag, and bounds of the color map
colormapperEnabled = False
colormapMin = 0
colormapMax = 1
currentColorMapIndex = 0

# True when we are choosing a center of rotation. see flyControl.py
pivotSelectionMode = False


# Initialize an array with false
# rendering options. kernelMode controls how every single point is rendered.
# renderMode controls how the full image is rendered on screen.

kernelModes = [
    'Uniform',
    'Smooth'
]

renderModes = [
    'Standard',
    'Faded',
    'Band5'    
]
kernelModeInd = 0
renderModeInd = 0
