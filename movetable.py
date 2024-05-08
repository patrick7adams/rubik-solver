import facelet # to initialize symmetry tables
from facelet import FaceletCube, FlipUDSliceToRawFlipUDSlice
from const import Moves
import numpy as np
import pickle
import os

def createCornerOrientationMoveTable():
    ''' TODO: Output move table to file, and then read from file if it exists; if it doesn't, create the file too. '''
    if os.path.exists('.\\lookups\\CornerOrientationMoveTable.npy'):
        return np.load('.\\lookups\\CornerOrientationMoveTable.npy')
    moveTable = np.empty((2187, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(2187):
        tmpCube.setCornerOrientationCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                moveTable[i, move*3+k] = tmpCube.getCornerOrientationCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\CornerOrientationMoveTable', moveTable)
    return moveTable

def createCornerOrientationSymmetryTable():
    if os.path.exists('.\\lookups\\CornerOrientationSymmetryTable.npy'):
        return np.load('.\\lookups\\CornerOrientationSymmetryTable.npy')
    symmetryTable = np.empty((2187, 16), dtype=np.uint32)
    tmpCube = FaceletCube()
    tmpCube2 = FaceletCube()
    for i in range(2187):
        tmpCube.setCornerOrientationCoordinate(i)
        for k in range(16): # symmetries
            tmpCube2.applyInvSymmetryCorner(tmpCube, k)
            coord = tmpCube2.getCornerOrientationCoordinate()
            symmetryTable[i, k] = coord
    np.save('.\\lookups\\CornerOrientationSymmetryTable', symmetryTable)
    return symmetryTable

def createInvCornerOrientationSymmetryTable():
    if os.path.exists('.\\lookups\\InvCornerOrientationSymmetryTable.npy'):
        return np.load('.\\lookups\\InvCornerOrientationSymmetryTable.npy')
    symmetryTable = np.empty((2187, 16), dtype=np.uint32)
    tmpCube = FaceletCube()
    tmpCube2 = FaceletCube()
    for i in range(2187):
        tmpCube.setCornerOrientationCoordinate(i)
        for k in range(16): # symmetries
            tmpCube2.applySymmetryCorner(tmpCube, k)
            coord = tmpCube2.getCornerOrientationCoordinate()
            symmetryTable[i, k] = coord
    np.save('.\\lookups\\InvCornerOrientationSymmetryTable', symmetryTable)
    return symmetryTable

def createFlipUDSliceMoveTable():
    if os.path.exists('.\\lookups\\FlipUDSliceMoveTable.npy'):
        return np.load('.\\lookups\\FlipUDSliceMoveTable.npy')
    moveTable = np.empty((64430, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    print("Creating FlipUDSliceMoveTable...")
    for i in range(64430):
        if i%1000==0: print(f"{i/64430*100}% complete")
        rawCoord = FlipUDSliceToRawFlipUDSlice[i]
        tmpCube.setUDSliceCoordinate(rawCoord // 2048)
        tmpCube.setEdgeOrientationCoordinate(rawCoord % 2048)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                coord = tmpCube.getFlipUDSliceCoordinate()
                moveTable[i, move*3+k] = coord
            tmpCube.move(move)
    
    print("Completed FlipUDSliceMoveTable generation.")
    np.save('.\\lookups\\FlipUDSliceMoveTable', moveTable)
    return moveTable

def createFlipUDSliceSymmetryTable():
    ''' This table contains information on the symmetries contained in FlipUDSliceIndexToRepresentants.'''
    if os.path.exists('.\\lookups\\FlipUDSliceSymmetryTable'):
        with open('.\\lookups\\FlipUDSliceSymmetryTable', 'rb') as f:   
            return pickle.load(f)
    symmetryTable = {}
    tmpCube = FaceletCube()
    tmpCube2 = FaceletCube()
    for i in range(64430):
        flipSliceCoord = FlipUDSliceToRawFlipUDSlice[i]
        UDSliceCoord = flipSliceCoord // 2048
        edgeOriCoord = flipSliceCoord % 2048
        tmpCube.setUDSliceCoordinate(UDSliceCoord)
        tmpCube.setEdgeOrientationCoordinate(edgeOriCoord)
        symmetryTable[i] = 0
        for symmetry in range(16):
            tmpCube2.applySymmetryEdge(tmpCube, symmetry)
            coord = tmpCube2.getRawFlipUDSliceCoordinate()
            if FaceletCube.FlipUDSliceLookup(coord) != -1:
                symmetryTable[i] += 2**symmetry
    with open('.\\lookups\\FlipUDSliceSymmetryTable', 'wb') as f:
        pickle.dump(symmetryTable, f, protocol=pickle.HIGHEST_PROTOCOL)
    return symmetryTable

def createCornerPermutationMoveTable():
    if os.path.exists('.\\lookups\\CornerPermutationMoveTable.npy'):
        return np.load('.\\lookups\\CornerPermutationMoveTable.npy')
    moveTable = np.empty((40320, 12), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(40320):
        # coord = CornerPermToRawCornerPerm[i]
        tmpCube.setCornerPermutationCoordinate(i)
        
def debug():
    tmpCube = FaceletCube()
    i = 28473
    rawCoord = FlipUDSliceToRawFlipUDSlice[i]
    tmpCube.setUDSliceCoordinate(rawCoord // 2048)
    tmpCube.setEdgeOrientationCoordinate(rawCoord % 2048)
    tmpCube.move(1) # 3 instead of 5 because 3 is the sym move
    coord = tmpCube.getFlipUDSliceCoordinate()
    print(coord)
    print(coord % 16)
    

cornerOrientationMoveTable = createCornerOrientationMoveTable()
invCornerOrientationSymmetryTable = createInvCornerOrientationSymmetryTable()
FlipUDSliceMoveTable = createFlipUDSliceMoveTable()
cornerOrientationSymmetryTable = createCornerOrientationSymmetryTable()
FlipUDSliceSymmetryTable = createFlipUDSliceSymmetryTable()
debug()