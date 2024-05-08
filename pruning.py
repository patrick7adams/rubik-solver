
import movetable

import numpy as np
import os


def createCornerOrientationPruningTable():
    if os.path.exists('.\\lookups\\CornerOrientationPruningTable.npy'):
        return np.load('.\\lookups\\CornerOrientationPruningTable.npy')
    numNodes = 2187
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating CornerOrientation pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in range(18):
                    newCornerOrientation = movetable.cornerOrientationMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newCornerOrientation] == 255:
                            pruningTable[newCornerOrientation] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newCornerOrientation] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating CornerOrientation pruning table.')
    np.save('.\\lookups\\CornerOrientationPruningTable.npy', pruningTable)
    return pruningTable

def createEdgeOrientationPruningTable():
    if os.path.exists('.\\lookups\\EdgeOrientationPruningTable.npy'):
        return np.load('.\\lookups\\EdgeOrientationPruningTable.npy')
    numNodes = 2048
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating EdgeOrientation pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in range(18):
                    newEdgeOrientation = movetable.edgeOrientationMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newEdgeOrientation] == 255:
                            pruningTable[newEdgeOrientation] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newEdgeOrientation] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating EdgeOrientation pruning table.')
    np.save('.\\lookups\\EdgeOrientationPruningTable.npy', pruningTable)
    return pruningTable

def createUDSlicePruningTable():
    if os.path.exists('.\\lookups\\UDSlicePruningTable.npy'):
        return np.load('.\\lookups\\UDSlicePruningTable.npy')
    numNodes = 495
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating UDSlice pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in range(18):
                    newUDSlice = movetable.UDSliceMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newUDSlice] == 255:
                            pruningTable[newUDSlice] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newUDSlice] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating UDSlice pruning table.')
    np.save('.\\lookups\\UDSlicePruningTable.npy', pruningTable)
    return pruningTable

def printCornerOrientationPruningIndex(cornerOrientation):
    print(f"Depth of {cornerOrientationPruningTable[cornerOrientation]} at cornerOrientation {cornerOrientation}")
    print('-------------------------')   
    for move in range(18):
        newCornerOrientation = movetable.cornerOrientationMoveTable[cornerOrientation, move]
        print(f"Move {move}: Depth of {cornerOrientationPruningTable[newCornerOrientation]} at cornerOrientation {newCornerOrientation}")  
    print('-------------------------')   
    
def printEdgeOrientationPruningIndex(edgeOrientation):
    print(f"Depth of {edgeOrientationPruningTable[edgeOrientation]} at edgeOrientation {edgeOrientation}")
    print('-------------------------')   
    for move in range(18):
        newEdgeOrientation = movetable.edgeOrientationMoveTable[edgeOrientation, move]
        print(f"Move {move}: Depth of {edgeOrientationPruningTable[newEdgeOrientation]} at edgeOrientation {newEdgeOrientation}")  
    print('-------------------------')   
    
def printUDSlicePruningIndex(UDSlice):
    print(f"Depth of {UDSlicePruningTable[UDSlice]} at UDSlice {UDSlice}")
    print('-------------------------')   
    for move in range(18):
        newUDSlice = movetable.UDSliceMoveTable[UDSlice, move]
        print(f"Move {move}: Depth of {UDSlicePruningTable[newUDSlice]} at UDSlice {newUDSlice}")  
    print('-------------------------')   
    
     
                        

cornerOrientationPruningTable = createCornerOrientationPruningTable()
edgeOrientationPruningTable = createEdgeOrientationPruningTable()
UDSlicePruningTable = createUDSlicePruningTable()