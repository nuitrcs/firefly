# default scale applied to points
pointScale = scale 
isLogScale = False                

# data mode. see loader.py
dataMode = None                     

# filter mode. Used to exclude a data range from rendering
filterMode = None                   
filterMin = 0
filterMax = 1

# colormapper flag, and bounds of the color map
colormapperEnabled = False
colormapMin = 0
colormapMax = 1

# True when we are choosing a center of rotation. see flyControl.py
pivotSelectionMode = False

filterStart = 0.0
filterEnd = 1.0
currentColorMapIndex = 0
# Initialize an array with false
isLogArray = [False] * 10
# rendering options. kernelMode controls how every single point is rendered.
# renderMode controls how the full image is rendered on screen.
kernelMode = 0
renderMode = 0
kernelModeInd = 0
renderModeInd = 0
