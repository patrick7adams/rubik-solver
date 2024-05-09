from facelet import FaceletCube
from const import Moves, ExtendedMoves
import coord, pruning, movetable
import numpy, sys, random
# U is blue
# R is orange
# F is yellow
# D is green
# L is red
# B is white

if __name__ == "__main__":
    numpy.printoptions(threshold=sys.maxsize)
    string = "RRBUULUUBLDRBRRUDRFBDUFLDFFLDRRDBLFBDFLULLUBFDFFDBRULB"
    cube = FaceletCube(string)
    cube2 = FaceletCube()
    
    # pruning.printCornerOrientationPruningIndex(cube.getCornerOrientationCoordinate())
    # pruning.printEdgeOrientationPruningIndex(cube.getEdgeOrientationCoordinate())
    # pruning.printUDSlicePruningIndex(cube.getUDSliceCoordinate())
    import time
    
    # initial_time = time.time()
    # print(coord.solve(cube))
    # print(time.time() - initial_time)
    
    # cube.printCoords()
    solve_moves = [9, 15, 1, 14, 10, 2, 3, 2, 15]
    for move in solve_moves:
        for i in range(move % 3+1):
            cube.move(move//3)
            
            
    print(cube.edgePositions)
    cube.printCoords()
    pruning.printCornerPermutationPruningIndex(cube.getCornerPermutationCoordinate())
    pruning.printEdgePermutationPruningIndex(cube.getEdgePermutationCoordinate())
    pruning.printUDPermutationPruningIndex(cube.getUDPermutationCoordinate())
    
        
    # print(' '.join(ExtendedMoves(move).name for move in solve_moves))
    
        # print('----------------')
    #     # print(movetable.cornerOrientationMoveTable[cube.getCornerOrientationCoordinate(), move])
    #     # print(movetable.edgeOrientationMoveTable[cube.getEdgeOrientationCoordinate(), move])
    #     # print(movetable.UDSliceMoveTable[cube.getUDSliceCoordinate(), move])
    #     print(pruning.cornerOrientationPruningTable[cube.getCornerOrientationCoordinate()])
    #     print(pruning.edgeOrientationPruningTable[cube.getEdgeOrientationCoordinate()])
    #     print(pruning.UDSlicePruningTable[cube.getUDSliceCoordinate()])