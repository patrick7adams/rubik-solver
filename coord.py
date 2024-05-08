from facelet import FaceletCube
import facelet
from const import Moves, ExtendedMoves
import movetable, os
import numpy as np
import queue

def createStageOnePruningTable():
    ''' The big one. Creates a 140,000,000 entry lookup table, where each index is a combination
    of the FlipUDSlice symcoordinate (specifically the representant value) and a symmetry conjugation of 
    the Corner Orientation raw coordinate.'''
    if os.path.exists('.\\lookups\\StageOnePruningTable.npy'):
        return np.load('.\\lookups\\StageOnePruningTable.npy')
    pruningTable = np.full(64430*2187, 255, dtype=np.uint8)
    filled_nodes = 1
    
    depth = 0
    pass_backwards = False
    pruningTable[0] = 0 # initial state
    # defining variables outside of the loop to try to save time
    flipUDSlice, cornerOrientation, newFlipUDSlice, newCornerOrientation, index, depth, sym = 0, 0, 0, 0, 0, 0, 0
    oldFilledNodes = -1
    while filled_nodes < 64430 * 2187 and not (oldFilledNodes == filled_nodes):
        oldFilledNodes = filled_nodes
        print(f'-------------------DEPTH OF {depth}------------------------')
        if depth >= 8: pass_backwards = True
        for i in range(0, 64430 * 2187):
            if i%100000==0: 
                print(f"{filled_nodes / (64430*2187)*100}% done, index {i} of {64430*2187}, nodes={filled_nodes}")
            # behold, the mother of all for loops
            if not pass_backwards and pruningTable[i] == depth or pass_backwards and pruningTable[i] == 255:
                flipUDSlice = i // 2187
                cornerOrientation = i % 2187
                for move in range(18): # all moves
                    # 98.77744060840655% done, index 2600000 of 140908410, nodes=139185721
                    # 98.77744060840655% done, index 2700000 of 140908410, nodes=139185721
                    # 98.77744060840655% done, index 2800000 of 140908410, nodes=139185721
                    # cannot reach the rest of the nodes, check symmetry conjugation and symmult / the previous bug
                    # that I thought wasn't a big enough issue to look into anymore
                    newCornerOrientation = movetable.cornerOrientationMoveTable[cornerOrientation, move]
                    newFlipUDSlice = movetable.FlipUDSliceMoveTable[flipUDSlice, move]
                    newFlipUDSliceSym = newFlipUDSlice % 16
                    newFlipUDSlice //= 16
                    index = newFlipUDSlice * 2187 + movetable.cornerOrientationSymmetryTable[newCornerOrientation, newFlipUDSliceSym]
                    if not pass_backwards:
                        if (pruningTable[index] == 255):
                            pruningTable[index] = depth+1
                            filled_nodes += 1
                            # print(f"Starting at index {index}, with FlipUDSlice {newFlipUDSlice} and CornerOrientation {newCornerOrientation}\n")
                            # symmetry table state code is likely wrong
                            # TODO: if another error, check against distribution table values
                            symmetryTableState = movetable.FlipUDSliceSymmetryTable[newFlipUDSlice]
                            if symmetryTableState != 1:
                                for k in range(1, 16):
                                    symmetryTableState //= 2
                                    if symmetryTableState == 1:
                                        symCornerOrientation = movetable.cornerOrientationSymmetryTable[newCornerOrientation, k]
                                        index = newFlipUDSlice * 2187 + symCornerOrientation
                                        if pruningTable[index] == 255: 
                                            pruningTable[index] = depth+1
                                            filled_nodes += 1
                    else:
                        if pruningTable[i] == 255 and pruningTable[index] == depth:
                            pruningTable[i] = depth+1 # storing symmetry information in pruning table too
                            filled_nodes += 1
        depth += 1
    print(pruningTable)
    np.save('.\\lookups\\StageOnePruningTable', pruningTable)
    return pruningTable

pruningTable = createStageOnePruningTable()

class CoordCube():
    def __init__(self, cornerOrientation, flipUDSlice):
        self.cornerOrientation = cornerOrientation
        self.FlipUDSlice = flipUDSlice
        self.FlipUDSliceIndex = flipUDSlice // 16
        self.FlipUDSliceSym = flipUDSlice % 16
        
    @staticmethod
    def from_cube(cube):
        return CoordCube(cube.getCornerOrientationCoordinate(), cube.getFlipUDSliceCoordinate())
        
    def getIndex(self):
        return self.FlipUDSliceIndex * 2187 + movetable.cornerOrientationSymmetryTable[self.cornerOrientation, self.FlipUDSliceSym]
        
    def move(self, move):
        ''' Applies a move to the coordinate cube. '''
        self.cornerOrientation = movetable.cornerOrientationMoveTable[self.cornerOrientation, move]
        flipUDSlice = movetable.FlipUDSliceMoveTable[self.FlipUDSliceIndex, FaceletCube.SymMove[self.FlipUDSliceSym, move]]
        self.FlipUDSliceSym = FaceletCube.SymMult[flipUDSlice % 16, self.FlipUDSliceSym]
        self.FlipUDSliceIndex = flipUDSlice // 16
        self.FlipUDSlice = self.FlipUDSliceIndex * 16 + self.FlipUDSliceSym
        
    def applySolution(self):
        solveMoves = self.solve()
        printPruning(pruningTable, self.getIndex())
        for move in solveMoves:
            self.move(move)
            printPruning(pruningTable, self.getIndex())
        
    def solve(self):
        ''' F score is the number of moves deep + the depth of the position described by the pruning table
        Starts at the start index described by flipUDSlice * 2187 + cornerOrientation, then recursively
        explores the full tree given by the current f score. Then, it will increment the f score by one
        and search the entire tree again.
        
        Pretty much, for each iteration:
        - Set the distance threshold equal to the depth of the root node.
        - Start at the root node, and explore all connected nodes by move indexing
        - Check for every node:
        - if the node is the goal, return the moves reached to get to that goal state. 
        - if the node has a distance (depth + cur_depth) higher than the threshold, prune it (don't explore it)
        - Otherwise, explore the node and continue checking from it and onwards.
        - If the goal node is not found by the end of the search, increase the distance threshold by one.
        - solver works; it goes from any start index to the goal index of 0 and returns the proper moves to reach
        the goal index. However, the indices don't seem to align with the actual moves in this case.
        '''
        start_index = self.getIndex()
        threshold = pruningTable[start_index]
        while threshold <= 12:
            visited_indices = queue.LifoQueue()
            visited_indices.put(start_index)
            visited_index_distances = queue.LifoQueue()
            visited_index_distances.put(0)
            visited_nodes = 1
            visited_paths = queue.LifoQueue()
            visited_paths.put([])
            # conjugate paths into a natural number for faster processing?
            min_depth = 100
            min_index = -1
            min_path = []
            while not visited_indices.empty():
                if visited_nodes % 100000 <= 18: 
                    print(f"Visited {visited_nodes} nodes in threshold {threshold}")
                index = visited_indices.get()
                distance = visited_index_distances.get()
                cornerOrientation, flipUDSlice = index % 2187, index // 2187
                flipUDSliceIndex, flipUDSliceSym = flipUDSlice // 16, flipUDSlice % 16
                path = visited_paths.get()
                for move in range(18):
                    newCornerOrientation = movetable.cornerOrientationMoveTable[cornerOrientation, move]
                    newFlipUDSlice = movetable.FlipUDSliceMoveTable[flipUDSliceIndex, FaceletCube.SymMove[flipUDSliceSym, move]]
                    newFlipUDSliceSym = FaceletCube.SymMult[flipUDSliceSym, newFlipUDSlice % 16] # change order back if things break
                    newFlipUDSliceIndex = newFlipUDSlice // 16
                    moved_index = newFlipUDSliceIndex * 2187 + movetable.cornerOrientationSymmetryTable[newCornerOrientation, newFlipUDSliceSym]
                    depth = pruningTable[moved_index]
                    f_score = depth + distance
                    visited_nodes += 1
                    new_path = path + [move]
                    if depth < min_depth:
                        min_depth = depth
                        min_index = moved_index
                        min_path = new_path
                    if moved_index == 0:
                        # print(f"Index: {index}, path: {path}, move: {move}")
                        return new_path
                    if f_score <= threshold:
                        visited_indices.put(moved_index)
                        visited_index_distances.put(distance+1)
                        visited_paths.put(new_path)
            threshold += 1
            print(f"Final visited nodes: {visited_nodes}")
            print(f"Min depth for this iteration: {min_depth}")
            print(f"Index at min iteration depth: {min_index}")
            print(f"Path to minimum depth: {min_path}")
        
        
    def print(self):
        print("------------Coordinate Cube---------------")
        print(f"CornerOrientation: {self.cornerOrientation}")
        print(f"FlipUDSlice: {self.FlipUDSliceIndex*16+self.FlipUDSliceSym}\n")



def printPruning(table, index):
    ''' Prints the adjacent moves to a given index in the pruning table.'''
    flipUDSlice = index // 2187
    cornerOrientation = index % 2187
    print(f"Depth of {table[index]} at index {index} ({flipUDSlice}, {cornerOrientation})")
    print('-------------------------')
    for move in ExtendedMoves:
        newCornerOrientation = movetable.cornerOrientationMoveTable[cornerOrientation, move]
        newFlipUDSlice = movetable.FlipUDSliceMoveTable[flipUDSlice, move]
        sym = newFlipUDSlice % 16
        newFlipUDSliceIndex = newFlipUDSlice // 16
        index = newFlipUDSliceIndex * 2187 + movetable.cornerOrientationSymmetryTable[newCornerOrientation, sym]
        print(f"Move {move}: Depth of {table[index]} at index {index}")  
    print('-------------------------')    
    
# printPruning(pruningTable, 0)
# printPruning(pruningTable, 41163851)
# printPruning(pruningTable, 41164286)
# printPruning(pruningTable, 41164515)
# printPruning(pruningTable, 41164950)
# print(solverPhaseOne(116365301))
# debug()




# print(getFinalIndex(116364977, [3, 9, 13, 17, 4, 6, 6, 14, 10, 6]))
    
# def debug():
#     i = 41165208
#     flipUDSlice = i // 2187
#     cornerOrientation = i % 2187
#     print(f"UD: {flipUDSlice}, CO: {cornerOrientation}")
#     for move in range(18): # all moves
#         print(f"--------Move {move}-------")
#         newFlipUDSlice = getFlipUDSliceMove(flipUDSlice, move)
#         # print(f"FlipUDSlice is {newFlipUDSlice}")
#         symmetry = newFlipUDSlice % 16
#         newFlipUDSlice = newFlipUDSlice // 16
#         newCornerOrientation = movetable.cornerOrientationSymmetryTable\
#         [movetable.cornerOrientationMoveTable[cornerOrientation, move], symmetry]
#         # compute index
#         # index = getPruningIndex(newFlipUDSlice, newCornerOrientation)
#         index = newFlipUDSlice * 2187 + newCornerOrientation
#         print(f"Index: {index}")
#         symmetryTableState = movetable.FlipUDSliceSymmetryTable[flipUDSlice]
#         if symmetryTableState != 1:
#             symCornerOrientation = movetable.cornerOrientationSymmetryTable[newCornerOrientation, symmetryTableState]
#             if move == 2:
#                 for i in range(16):
#                     print(f"SymCorner{i}: {movetable.cornerOrientationSymmetryTable[newCornerOrientation, i]}")
#             index = newFlipUDSlice * 2187 + symCornerOrientation
#             print(f"Symmetrical index: {index}")
                # print(f"Adding symmetry at index {index}")


# print('------------')
# UDcoord = getFlipUDSliceMove(0, 3)
# cornCoord = movetable.cornerOrientationMoveTable[0, 3]
# sym = UDcoord % 16
# newFlipUDSlice = UDcoord // 16
# newCornerOrientation = movetable.cornerOrientationSymmetryTable[cornCoord, sym]
# # compute index
# index = newFlipUDSlice * 2187 + newCornerOrientation
# print(UDcoord)
# print(cornCoord)
# print(index)
# print('------------------------------------')
# the problem is that these are run with the wrong coordinates. They should be run with the unmodified UDcoord
# and corner orientation, but they aren't. How to do this?
# index = 41163851
# UDcoord = index // 2187
# cornCoord = index % 2187

# UDcoord2 = getFlipUDSliceMove(UDcoord, 5)
# cornCoord2 = movetable.cornerOrientationMoveTable[cornCoord, 5]
# sym = UDcoord2 % 16
# newFlipUDSlice = UDcoord2 // 16
# newCornerOrientation = movetable.cornerOrientationSymmetryTable[cornCoord2, sym]
# # compute index
# # index = getPruningIndex(newFlipUDSlice, newCornerOrientation)
# index = newFlipUDSlice * 2187 + newCornerOrientation
# print(UDcoord2)
# print(cornCoord2)
# print(index)

# # print('--------------------------')
# # for i in range(0, 64430 * 2187):
# #     if i%100000 == 0: print(f"{i} out of {64430 * 2187}")
# #     if pruningTable[i] <= 3:
# #         for move in range(18):
# #             UDcoord = movetable.FlipUDSliceMoveTable[0, 3]
# #             cornCoord = movetable.cornerOrientationMoveTable[0, 3]
# #             sym = UDcoord % 16
# #             newFlipUDSlice = UDcoord // 16
# #             newCornerOrientation = movetable.cornerOrientationSymmetryTable[cornCoord, sym]
# #             index = newFlipUDSlice * 2187 + newCornerOrientation
# #             if pruningTable[index] == 0:
# #                 print(f"Index {i} Connects to 0 with move {move}")

# # -----------Move 5-----------------
# # FlipUDSlice: 18822
# # NewFlipUDSlice: 22968
# # New Corner Orientation: 875
# # Sym Corner Orientation: 1749
# # Index: 50232765