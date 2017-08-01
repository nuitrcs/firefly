import os, sys
from readsnap import readsnap
import np_tools
import numpy as np

global colormapMin,colormapMax

########################################################################
# Load the Data from the Data Files
########################################################################

# Load the snapshot data. datasetBase and snapshotNumber are defined in the config file!
res = readsnap(datasetBase, snapshotNumber, 0)

# Calculate what the radius and weight should be when shown, as an approximation to what it really is.
radius = np.power(((res['m'] / res['rho'])/(2 * np.pi) ),(1.0/3.0))
weight = 2 * radius * res['rho']

########################################################################
# Orient the Camera
########################################################################

if orientOnCoM:
    cameraPosition, pivotPoint, cameraOrientation = np_tools.setCenterOfMassView( res['p'], res['m'], 4. )

########################################################################
# Put the Data in a Firefly-Recognizable Format
########################################################################

# Make a loader to keep the dataset around
numpy_loader = NumpyLoader()

# Add dimensions to the Numpy Loader
numpy_loader.addDimension( 'Coordinates', res['p'] )
numpy_loader.addDimension( 'Velocities', res['v'] )
numpy_loader.addDimension( 'Surface Density', weight )
numpy_loader.addDimension( 'Particle Radius', radius )

# Get the colormap default range, based on an array
colormapMin, colormapMax = np_tools.setDefaultRanges( weight )

# How large should each particle be? Note that this sets everything to 1 right now, and the function actually isn't finished to do anything with the argument.
np_tools.setDefaultPointScale( radius )

########################################################################
# Make an individual dataset
########################################################################

# String might be an arbitrary label at this point in time
ds0 = Dataset.create( 'PartType0' )
# How the dataset knows where to find the data
ds0.setLoader( numpy_loader )

# Add dimensions
# Arguments: 1: Array to get, 2: Data type for array, 3: Index of the array, if the array has multiple dimensions (0 if single dimensional), 4: Label of some sort
x0 = ds0.addDimension( 'Coordinates', DimensionType.Float, 0, 'x' )
y0 = ds0.addDimension( 'Coordinates', DimensionType.Float, 1, 'y' )
z0 = ds0.addDimension( 'Coordinates', DimensionType.Float, 2, 'z' )
sd0 = ds0.addDimension( 'Surface Density', DimensionType.Float, 0, 'sd' )
vx0 = ds0.addDimension( 'Velocities', DimensionType.Float, 0, 'vx' )
vy0 = ds0.addDimension( 'Velocities', DimensionType.Float, 1, 'vy' )
vz0 = ds0.addDimension( 'Velocities', DimensionType.Float, 2, 'vz' )
r0 = ds0.addDimension( 'Particle Radius', DimensionType.Float, 0, 'radius' )

########################################################################
# Setup Point CLoud
########################################################################
# This is what we actually look at.

# Setup the point cloud object
# The 'pc0' string is probably an arbitrary label
pc0 = PointCloud.create('pc0')

# Use the variable set in the config file to set up information for the point cloud
pc0.setOptions( pointCloudLoadOptions )

# What are the x-, y-, and z-axes? By default they're literally x, y, and z, but they could be temperature, density, and metallicity, for example.
pc0.setDimensions( x0, y0, z0 )

# Default color with no colormap
pc0.setColor( Color('red') )

# What it says.
pc0.setPointScale( pointScale )

# If we want to have multiple point cloud objects
parts = [pc0]

# These theoretically should no longer be used.
defaultMinScale = 1e-8
defaultMaxScale = 1e2

########################################################################
# Setup the Modes Available For Display
########################################################################

# Default is whatever comes up first in the list
dataModes = [
  'Surface Density',
  'Point',
]

# Firefly looks for this specific function later on. It must exist.
def setDataMode( mode ):

    # Setup some required details
    global dataMode
    dataMode = mode
    dm = dataModes[mode]

    if ( dm == 'Surface Density' ):

        # This is what will determine the color, i.e. this should be the weight
        pc0.setData( sd0 )        

        # This is what determines the size
        pc0.setSize( r0 )

        # Make sure it's visible!
        pc0.setVisible( True )

        # Sets the shader program you're using.
        # Typically only use prog_channel (colormapping) or
        # prog_fixedColor (when you only want to display the default colors).
        pc0.setProgram( prog_channel )

        # Update the colormap bounds to work.
        updateColormapBounds( colormapMin, colormapMax )

        # Other options. More options available in the wiki, fireflyUI.py
        enableSmoothingLength( False ) # MUST be False currently.
        enableColormapper( True )
        enableLogScale( True )

    ########################################################################

    if ( dm == 'Point' ):
      
        # No chosen color
        pc0.setData( None )

        # No chosen size
        pc0.setSize( None )

        # Make sure it's visible
        pc0.setVisible( True )

        # Make the shader a single color
        pc0.setProgram( prog_fixedColor )

        enableSmoothingLength( False )
        enableColormapper( False )
        enableLogScale( False )

    redraw()

print 'Finished loader\n'

