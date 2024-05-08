from facelet import FaceletCube
from const import Moves
import movetable, pruning, facelet
import numpy as np
import queue, os

        
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