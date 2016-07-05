#load h5py, numpy libraries
import h5py
import math
import numpy as np
import struct
import sys
import csv

#-------------------------------------------------------------------------------
def extractPart(h5file, partName, outfile, useSmoothing, useDensity = False, saveCSV = False):
    part = h5file[partName]
    out = open(outfile, 'wb')
    if(saveCSV):
        outw = csv.writer(out)
        
    # extraction hack
    IE = part['InternalEnergy']
    ieArray = np.array(IE)
    ieArray = ieArray.astype(float)

    SFR = part['StarFormationRate']
    sfrArray = np.array(SFR)
    sfrArray = sfrArray.astype(float)

    C = part['Coordinates']
    coordArray = np.array(C)
    coordArray = coordArray.astype(float)
    if(useSmoothing):
        S = part['SmoothingLength']
        smoothingArray = np.array(S)
        smoothingArray = smoothingArray.astype(float)
    if(useDensity):
        D = part['Density']
        densityArray = np.array(D)
        densityArray = densityArray.astype(float)
            

    print("Extracting {0} points from {1} to {2}".format(coordArray.shape[0], partName, outfile))
    for i in range(0, coordArray.shape[0]):
        sl = 1 * scale
        ds = 1
        if(useSmoothing):
            sl = smoothingArray[i] * scale
        if(useDensity):
            ds = densityArray[i] * densityScale
        
        if(saveCSV):
            outw.writerow([
                coordArray[i][0] * scale,
                coordArray[i][1] * scale,
                coordArray[i][2] * scale,
                sl,
                ds,
                1,
                1,
                1,
                1])
        else:
            out.write(struct.pack('ddddddd',
                                  coordArray[i][0] * scale,
                                  coordArray[i][1] * scale,
                                  coordArray[i][2] * scale,
                                  sl,
                                  ds,
                                  ieArray[i],
                                  sfrArray[i]))
        # Progress logging stuff
        if i % 400000 == 0:
            perc = 100 * i / coordArray.shape[0]
            print("{0}%".format(perc))
    out.close()


#open the file
f = h5py.File('snapshot_140.hdf5','r')

# scale factor for coordinates and smoothing length
scale = 0.1
densityScale = 1
saveCSV = False

# Extract parts data to binary point cloud files
extractPart(f, 'PartType0', 'data_0.xyzb', True, True, saveCSV)
#extractPart(f, 'PartType1', 'data_1.csv', False, False, saveCSV)
#extractPart(f, 'PartType2', 'data_2.csv', False, False, saveCSV)
#extractPart(f, 'PartType4', 'data_4.csv', False, False, saveCSV)

print("Done!")

