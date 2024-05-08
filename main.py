from facelet import FaceletCube
from const import Moves
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
    
    pruning.printCornerOrientationPruningIndex(cube.getCornerOrientationCoordinate())
    pruning.printEdgeOrientationPruningIndex(cube.getEdgeOrientationCoordinate())
    pruning.printUDSlicePruningIndex(cube.getUDSliceCoordinate())