import facelet # to initialize symmetry tables
from facelet import FaceletCube
from const import Moves, P2Moves
import numpy as np
import pickle
import os

def createCornerOrientationMoveTable():
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

def createEdgeOrientationMoveTable():
    if os.path.exists('.\\lookups\\EdgeOrientationMoveTable.npy'):
        return np.load('.\\lookups\\EdgeOrientationMoveTable.npy')
    moveTable = np.empty((2048, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(2048):
        tmpCube.setEdgeOrientationCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                moveTable[i, move*3+k] = tmpCube.getEdgeOrientationCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\EdgeOrientationMoveTable', moveTable)
    return moveTable

def createUDSliceMoveTable():
    if os.path.exists('.\\lookups\\UDSliceMoveTable.npy'):
        return np.load('.\\lookups\\UDSliceMoveTable.npy')
    moveTable = np.empty((495, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(495):
        tmpCube.setUDSliceCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                moveTable[i, move*3+k] = tmpCube.getUDSliceCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\UDSliceMoveTable', moveTable)
    return moveTable

def createCornerPermutationMoveTable():
    if os.path.exists('.\\lookups\\CornerPermutationMoveTable.npy'):
        return np.load('.\\lookups\\CornerPermutationMoveTable.npy')
    moveTable = np.empty((40320, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(40320):
        tmpCube.setCornerPermutationCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                if move*3+k in P2Moves:
                    moveTable[i, move*3+k] = tmpCube.getCornerPermutationCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\CornerPermutationMoveTable', moveTable)
    return moveTable

def createEdgePermutationMoveTable():
    if os.path.exists('.\\lookups\\EdgePermutationMoveTable.npy'):
        return np.load('.\\lookups\\EdgePermutationMoveTable.npy')
    moveTable = np.empty((40320, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(40320):
        tmpCube.setEdgePermutationCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                if move*3+k in P2Moves:
                    # if any(i in tuple(tmpCube.edgePositions[:8]) for i in range(8, 12)):
                    #     print('hi')
                    moveTable[i, move*3+k] = tmpCube.getEdgePermutationCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\EdgePermutationMoveTable', moveTable)
    return moveTable

def createUDPermutationMoveTable():
    if os.path.exists('.\\lookups\\UDPermutationMoveTable.npy'):
        return np.load('.\\lookups\\UDPermutationMoveTable.npy')
    moveTable = np.empty((24, 18), dtype=np.uint32)
    tmpCube = FaceletCube()
    for i in range(24):
        tmpCube.setUDPermutationCoordinate(i)
        for move in Moves:
            for k in range(3):
                tmpCube.move(move)
                if move*3+k in P2Moves:
                    moveTable[i, move*3+k] = tmpCube.getUDPermutationCoordinate()
            tmpCube.move(move)
    np.save('.\\lookups\\UDPermutationMoveTable', moveTable)
    return moveTable
                

cornerOrientationMoveTable = createCornerOrientationMoveTable()
edgeOrientationMoveTable = createEdgeOrientationMoveTable()
UDSliceMoveTable = createUDSliceMoveTable()
cornerPermutationMoveTable = createCornerPermutationMoveTable()
edgePermutationMoveTable = createEdgePermutationMoveTable()
UDPermutationMoveTable = createUDPermutationMoveTable()