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
    string2 = "UUDUUUUDUFRBRRRRRLBFLBFFLLFDDDUDDUDDLFRLLLFBBRLBBBFFBR"
    cube = FaceletCube(string2)
    cube2 = FaceletCube()
    
    # pruning.printCornerOrientationPruningIndex(cube.getCornerOrientationCoordinate())
    # pruning.printEdgeOrientationPruningIndex(cube.getEdgeOrientationCoordinate())
    # pruning.printUDSlicePruningIndex(cube.getUDSliceCoordinate())
    import time
    
    # initial_time = time.time()
    # print(time.time() - initial_time)
    
    # cube.printCoords()
    solve_moves = coord.solve(cube)
    # solve_moves = [17, 8, 14, 10, 12, 16, 12, 16, 2, 6, 10, 16, 13, 11, 13, 11, 7, 11, 13, 4, 11, 7, 9, 4]
    for move in solve_moves:
        for i in range(move % 3+1):
            cube.move(move//3)
    cube.printCoords()
    print(' '.join(ExtendedMoves(move).name.replace('3', "'") for move in solve_moves))
    # pruning.printCornerPermutationPruningIndex(cube.getCornerPermutationCoordinate())
    # pruning.printEdgePermutationPruningIndex(cube.getEdgePermutationCoordinate())
    # pruning.printUDPermutationPruningIndex(cube.getUDPermutationCoordinate())
    
        
    
    
        # print('----------------')
    #     # print(movetable.cornerOrientationMoveTable[cube.getCornerOrientationCoordinate(), move])
    #     # print(movetable.edgeOrientationMoveTable[cube.getEdgeOrientationCoordinate(), move])
    #     # print(movetable.UDSliceMoveTable[cube.getUDSliceCoordinate(), move])
    #     print(pruning.cornerOrientationPruningTable[cube.getCornerOrientationCoordinate()])
    #     print(pruning.edgeOrientationPruningTable[cube.getEdgeOrientationCoordinate()])
    #     print(pruning.UDSlicePruningTable[cube.getUDSliceCoordinate()])