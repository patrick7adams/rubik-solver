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
    faceString = "UUDUUUUDUFRBRRRRRLBFLBFFLLFDDDUDDUDDLFRLLLFBBRLBBBFFBR"
    cube = FaceletCube(faceString)
    solve_moves = coord.solve(cube)
    import serial
    serial_conn = serial.Serial('/dev/ttyACM0', 9600)
    serial_conn.flush()
    serial_conn.write((str(len(solve_moves)+'\n')).encode())
    for move in solve_moves:
        string = str(move) + '\n'
        serial_conn.write(string.encode())
    # for move in solve_moves:
    #     for i in range(move % 3+1):
    #         cube.move(move//3)
    # cube.printCoords()
    # print(' '.join(ExtendedMoves(move).name.replace('3', "'") for move in solve_moves))
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