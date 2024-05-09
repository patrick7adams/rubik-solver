from facelet import FaceletCube
from const import Moves
import movetable, pruning, facelet
from movetable import cornerOrientationMoveTable, edgeOrientationMoveTable, UDSliceMoveTable
from pruning import cornerOrientationPruningTable, edgeOrientationPruningTable, UDSlicePruningTable
import numpy as np
import queue, os

def getDepthPhaseOne(indices):
    return max(cornerOrientationPruningTable[indices[0]], edgeOrientationPruningTable[indices[1]], UDSlicePruningTable[indices[2]])

def getMovesPhaseOne(indices, move):
    return (cornerOrientationMoveTable[indices[0], move], edgeOrientationMoveTable[indices[1], move], UDSliceMoveTable[indices[2], move])
        
def solve(cube):
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
    startCoords = (cube.getCornerOrientationCoordinate(), cube.getEdgeOrientationCoordinate(), cube.getUDSliceCoordinate())
    threshold = getDepthPhaseOne(startCoords)
    while threshold <= 12:
        visited_indices = queue.LifoQueue()
        visited_indices.put(startCoords)
        visited_index_distances = queue.LifoQueue()
        visited_index_distances.put(0)
        visited_nodes = 1
        visited_paths = queue.LifoQueue()
        visited_paths.put([])
        past_indices = queue.LifoQueue()
        past_indices.put([])
        # conjugate paths into a natural number for faster processing?
        import time
        average_times, average_start_times, average_end_times = [], [], []
        while not visited_indices.empty():
            # if visited_nodes % 100000 <= 18: 
            #     print(f"Visited {visited_nodes} nodes in threshold {threshold}")
            indices = visited_indices.get()
            distance = visited_index_distances.get()
            path = visited_paths.get()
            past_index = past_indices.get()
            for move in range(18):
                # start_time = time.time()
                # these two functions take around 1e-06 seconds, six table lookups + max
                moved_indices = getMovesPhaseOne(indices, move)
                max_moved_depth = getDepthPhaseOne(moved_indices)
                f_score = max_moved_depth + distance
                visited_nodes += 1
                # takes around 1.8e-07 seconds, may change soon to make more efficient
                new_path = path + [move]
                new_past_index = past_index + [moved_indices]
                # time_at_mid = time.time()
                # mid_time = time_at_mid - start_time
                # if statements take around 2.8e-07 seconds
                if not (moved_indices[0] + moved_indices[1] + moved_indices[2]):
                    # print(sum(average_times) / len(average_times))
                    # print(sum(average_start_times) / len(average_start_times))
                    # print(sum(average_end_times) / len(average_end_times))
                    return new_path
                if f_score <= threshold:
                    visited_indices.put(moved_indices)
                    visited_index_distances.put(distance+1)
                    visited_paths.put(new_path)
                    past_indices.put(new_past_index)
                # end_time = time.time() - time_at_mid
                # total_time = time.time() - start_time
                # average_start_times.append(mid_time)
                # average_end_times.append(end_time)
                # average_times.append(total_time)
        threshold += 1
        print(f"Final visited nodes: {visited_nodes}")