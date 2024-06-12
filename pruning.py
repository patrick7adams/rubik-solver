
import movetable
from const import P2Moves
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

def getPhaseOneIndex(CO, EO, UD):
    return UD * 4478976 + EO * 2187 + CO

def getPhaseTwoIndex(CP, EP):
    return CP * 40320 + EP

def createPhaseOnePruningTable():
    ''' Pruning table that combines all of the phase one elements, for faster indexing. Swaps memory for speed. '''
    if os.path.exists('.\\lookups\\PhaseOnePruningTable.npy'):
        return np.load('.\\lookups\\PhaseOnePruningTable.npy')
    numNodes = 2187*2048*495
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating PhaseOne pruning table...')
    while filled_nodes != numNodes and depth < 11:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if i%1000000 == 0: print(f"{filled_nodes/numNodes*100}%: {filled_nodes} filled of {numNodes}, {i/numNodes*100}% done with current iteration.")
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                CO = i%2187
                EO = (i // 2187) % 2048
                UD = (i // 4478976)
                for move in range(18):
                    newCornerOrientation = movetable.cornerOrientationMoveTable[CO, move]
                    newEdgeOrientation = movetable.edgeOrientationMoveTable[EO, move]
                    newUDSlice = movetable.UDSliceMoveTable[UD, move]
                    index = newUDSlice * (4478976) + newEdgeOrientation * (2187) + newCornerOrientation
                    if not pass_backwards:
                        if pruningTable[index] == 255:
                            pruningTable[index] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[index] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating PhaseOne pruning table.')
    np.save('.\\lookups\\PhaseOnePruningTable.npy', pruningTable)
    return pruningTable

def createPhaseTwoPruningTable():
    ''' Pruning table that combines corner and edge permutations, for faster indexing. Swaps memory for speed. (1.6 GB)'''
    if os.path.exists('.\\lookups\\PhaseTwoPruningTable.npy'):
        return np.load('.\\lookups\\PhaseTwoPruningTable.npy')
    numNodes = 40320*40320
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating PhaseTwo pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if i%1000000 == 0: print(f"{filled_nodes/numNodes*100}%: {filled_nodes} filled of {numNodes}, {i/numNodes*100}% done with current iteration.")
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in range(18):
                    newCornerPermutation = movetable.cornerPermutationMoveTable[i // 40320, move]
                    newEdgePermutation = movetable.edgePermutationMoveTable[i % 40320, move]
                    index = newCornerPermutation * (40320) + newEdgePermutation
                    if not pass_backwards:
                        if pruningTable[index] == 255:
                            pruningTable[index] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[index] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating PhaseTwo pruning table.')
    np.save('.\\lookups\\PhaseTwoPruningTable.npy', pruningTable)
    return pruningTable

def createCornerPermutationPruningTable():
    if os.path.exists('.\\lookups\\CornerPermutationPruningTable.npy'):
        return np.load('.\\lookups\\CornerPermutationPruningTable.npy')
    numNodes = 40320
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating CornerPermutation pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in P2Moves:
                    newCornerPermutation = movetable.cornerPermutationMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newCornerPermutation] == 255:
                            pruningTable[newCornerPermutation] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newCornerPermutation] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating CornerPermutation pruning table.')
    np.save('.\\lookups\\CornerPermutationPruningTable.npy', pruningTable)
    return pruningTable

def createEdgePermutationPruningTable():
    if os.path.exists('.\\lookups\\EdgePermutationPruningTable.npy'):
        return np.load('.\\lookups\\EdgePermutationPruningTable.npy')
    numNodes = 40320
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating EdgePermutation pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in P2Moves:
                    newEdgePermutation = movetable.edgePermutationMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newEdgePermutation] == 255:
                            pruningTable[newEdgePermutation] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newEdgePermutation] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating EdgePermutation pruning table.')
    np.save('.\\lookups\\EdgePermutationPruningTable.npy', pruningTable)
    return pruningTable

def createUDPermutationPruningTable():
    if os.path.exists('.\\lookups\\UDPermutationPruningTable.npy'):
        return np.load('.\\lookups\\UDPermutationPruningTable.npy')
    numNodes = 24
    pruningTable = np.full(numNodes, 255, dtype=np.uint8)
    filled_nodes = 1
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0
    print('Generating UDPermutation pruning table...')
    while filled_nodes != numNodes:
        print(f'Depth of {depth}: {filled_nodes} / {numNodes} nodes generated.')
        if filled_nodes > (numNodes/2): pass_backwards = True
        for i in range(numNodes):
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                for move in P2Moves:
                    newUDPermutation = movetable.UDPermutationMoveTable[i, move]
                    if not pass_backwards:
                        if pruningTable[newUDPermutation] == 255:
                            pruningTable[newUDPermutation] = depth+1
                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[newUDPermutation] == depth:
                            pruningTable[i] = depth+1
                            filled_nodes += 1
        depth += 1
    print('Done generating UDPermutation pruning table.')
    np.save('.\\lookups\\UDPermutationPruningTable.npy', pruningTable)
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
    
def printCornerPermutationPruningIndex(cornerPermutation):
    print(f"Depth of {cornerPermutationPruningTable[cornerPermutation]} at cornerPermutation {cornerPermutation}")
    print('-------------------------')   
    for move in P2Moves:
        newCornerPermutation = movetable.cornerPermutationMoveTable[cornerPermutation, move]
        print(f"Move {move}: Depth of {cornerPermutationPruningTable[newCornerPermutation]} at cornerPermutation {newCornerPermutation}")  
    print('-------------------------')   
    
def printEdgePermutationPruningIndex(edgePermutation):
    print(f"Depth of {edgePermutationPruningTable[edgePermutation]} at edgePermutation {edgePermutation}")
    print('-------------------------')   
    for move in P2Moves:
        newEdgePermutation = movetable.edgePermutationMoveTable[edgePermutation, move]
        print(f"Move {move}: Depth of {edgePermutationPruningTable[newEdgePermutation]} at edgePermutation {newEdgePermutation}")  
    print('-------------------------')   
    
def printUDPermutationPruningIndex(UDPermutation):
    print(f"Depth of {UDPermutationPruningTable[UDPermutation]} at UDPermutation {UDPermutation}")
    print('-------------------------')   
    for move in P2Moves:
        newUDPermutation = movetable.UDPermutationMoveTable[UDPermutation, move]
        print(f"Move {move}: Depth of {UDPermutationPruningTable[newUDPermutation]} at UDPermutation {newUDPermutation}")  
    print('-------------------------')   
    
     
                        

cornerOrientationPruningTable = createCornerOrientationPruningTable()
edgeOrientationPruningTable = createEdgeOrientationPruningTable()
UDSlicePruningTable = createUDSlicePruningTable()
cornerPermutationPruningTable = createCornerPermutationPruningTable()
edgePermutationPruningTable = createEdgePermutationPruningTable()
UDPermutationPruningTable = createUDPermutationPruningTable()
PhaseOnePruningTable = createPhaseOnePruningTable()
PhaseTwoPruningTable = createPhaseTwoPruningTable()