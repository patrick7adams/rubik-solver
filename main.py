from facelet import FaceletCube, binomial, FlipUDSliceToRawFlipUDSlice
from const import Moves, ExtendedMoves
import coord
from coord import CoordCube
import movetable, symmetry, numpy, sys, random
# U is blue
# R is orange
# F is yellow
# D is green
# L is red
# B is white

def testFlipUDSliceToRaw():
    tmpCube = FaceletCube()
    flipUDSlice = 1008088
    sym = flipUDSlice % 16
    raw = FlipUDSliceToRawFlipUDSlice[flipUDSlice//16]
    tmpCube.setRawFlipUDSliceCoordinate(raw)
    tmpCube.applySymmetry(tmpCube, sym)
    assert tmpCube.getEdgeOrientationCoordinate() == 1173
    assert tmpCube.getUDSliceCoordinate() == 436
    
def testMoveOnCubie():
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(1237)
    tmpCube.setCornerOrientationCoordinate(1592)
    tmpCube.setUDSliceCoordinate(371)
    tmpCube.move(1) # right turn
    assert tmpCube.getEdgeOrientationCoordinate() == 1173
    assert tmpCube.getCornerOrientationCoordinate() == 818
    assert tmpCube.getUDSliceCoordinate() == 436
    
def testMoveOnCoordinate():
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(1237)
    tmpCube.setCornerOrientationCoordinate(1592)
    tmpCube.setUDSliceCoordinate(371)
    coordCube = CoordCube.from_cube(tmpCube)
    coordCube.move(3) # right turn
    assert coordCube.cornerOrientation == 818
    assert coordCube.FlipUDSliceIndex == 63005
    assert coordCube.FlipUDSliceSym == 8
    
def testMovesOnCoordCube(EO, CO, UD):
    # print(f"Testing with EO {EO}, CO {CO}, and UD {UD}")
    for move in range(18):
        tmpCube = FaceletCube()
        tmpCube.setEdgeOrientationCoordinate(EO)
        tmpCube.setCornerOrientationCoordinate(CO)
        tmpCube.setUDSliceCoordinate(UD)
        coordCube = CoordCube.from_cube(tmpCube)
        for i in range(move%3+1):
            tmpCube.move(move//3)
        coordCube.move(move)
        # print(move)
        assert coordCube.cornerOrientation == tmpCube.getCornerOrientationCoordinate()
        assert coordCube.FlipUDSliceIndex == tmpCube.getFlipUDSliceCoordinate() // 16
        # try:
        assert coordCube.FlipUDSliceSym == tmpCube.getFlipUDSliceCoordinate() % 16
        # except:
        #     print(f"FlipUDSliceSym failed on move {move}, printing coordCube and cubieCube below: ")
        #     tmpCube.printCoords()
        #     coordCube.print()
        
def testInvertMoves(EO, CO, UD):
    for move in range(18):
        tmpCube = FaceletCube()
        tmpCube.setEdgeOrientationCoordinate(EO)
        tmpCube.setCornerOrientationCoordinate(CO)
        tmpCube.setUDSliceCoordinate(UD)
        coordCube = CoordCube.from_cube(tmpCube)
        initialIndex = coordCube.FlipUDSlice
        invMove = move if (move-1)%3 == 0 else (2-move%3)+(move//3*3) # gets the move required to take the inverse
        coordCube.move(move)
        tmpIndex = coordCube.FlipUDSlice
        coordCube.move(invMove)
        try:
            assert coordCube.FlipUDSlice == initialIndex
        except:
            print(f"ERROR: Move {move} and move {invMove} do not lead back to the same index!")
            print(f"Initial Index: {initialIndex}")
            print(f"Index after move {move}: {tmpIndex}")
            print(f"Index after reversing with move {invMove}: {coordCube.FlipUDSlice}")
            # raise AssertionError()
        
def testInvertMove():
    print('----------')
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(2047)
    tmpCube.setCornerOrientationCoordinate(2186)
    tmpCube.setUDSliceCoordinate(494)
    coordCube = CoordCube.from_cube(tmpCube)
    initialIndex = coordCube.FlipUDSlice
    coordCube.move(3)
    # FaceletCube.SymMove[9, 5] = 9 # 9 or 10 to work
    tmpIndex = coordCube.FlipUDSlice
    coordCube.move(5)
    # The problem at hand here: Sometime along, during the transformation, the symmetry is changed
    # from 10 to 15, which results in a wildly different index. The symmetry should stay the same 
    # going back and forth, though. This bug is the cause of basically all the remaining issues in
    # the program, and it's imperative that I figure it out. 
    finalIndex = coordCube.FlipUDSlice
    # finalIndex should equal initialIndex
    print(initialIndex)
    print(tmpIndex)
    print(finalIndex)
    
def testMoveSymmetryThings():
    FUDS = 455568
    sym = 9
    symMove = 3
    newFUDS = movetable.FlipUDSliceMoveTable[FUDS // 16, symMove] # THIS IS THE PROBLEM CHILD!
    oldSym = sym
    sym = FaceletCube.SymMult[newFUDS % 16, sym] # not at fault here tho I've checked rigorously enough
    
    print(f"SymMult[{newFUDS%16}, {oldSym}] = {sym}")
    assert sym == 10
    
def testInvertMove2():
    print('----------')
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(0)
    tmpCube.setCornerOrientationCoordinate(0)
    tmpCube.setUDSliceCoordinate(0)
    coordCube = CoordCube.from_cube(tmpCube)
    initialIndex = coordCube.getIndex()
    coordCube.move(12)
    tmpIndex = coordCube.getIndex()
    coordCube.FlipUDSliceSym = 6
    coordCube.move(14)
    finalIndex = coordCube.getIndex()
    # SymMult is not wrong here. the symmetries that it provides are correct, but the original cube is now
    # finalIndex should equal initialIndex
    print(initialIndex)
    print(tmpIndex)
    print(finalIndex)
    
def testGetUDSlice():
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(2047)
    tmpCube.setCornerOrientationCoordinate(1403)
    tmpCube.setUDSliceCoordinate(161)
    coord = tmpCube.getFlipUDSliceCoordinate()
    coordCube = CoordCube.from_cube(tmpCube)
    print(f"TmpCube coord: {coord}")
    print(f"TmpCube sym index: {coord%16}")
    print('---------')
    print(f"CoordCube coord: {coordCube.FlipUDSlice}")
    print(f"CoordCube sym index: {coordCube.FlipUDSliceSym}")
    print('-----------------------')
    tmpCube.move(1)
    tmpCube.move(1)
    tmpCube.move(1)
    coord = tmpCube.getFlipUDSliceCoordinate()
    coordCube.move(5)
    print(f"TmpCube coord: {coord}")
    print(f"TmpCube sym index: {coord%16}")
    print('---------')
    print(f"CoordCube coord: {coordCube.FlipUDSlice}")
    print(f"CoordCube sym index: {coordCube.FlipUDSliceSym}")
    
def testGetUDSlice2():
    tmpCube = FaceletCube()
    tmpCube.setEdgeOrientationCoordinate(0)
    tmpCube.setCornerOrientationCoordinate(0)
    tmpCube.setUDSliceCoordinate(0)
    coord = tmpCube.getFlipUDSliceCoordinate()
    print(f"Raw coord: {coord}")
    print(f"Equivalence index: {coord//16}")
    print(f"Sym index: {coord%16}")
    tmpCube.move(4)
    coord = tmpCube.getFlipUDSliceCoordinate()
    print(f"Raw coord: {coord}")
    print(f"Equivalence index: {coord//16}")
    print(f"Sym index: {coord%16}")
    tmpCube.move(4)
    tmpCube.move(4)
    tmpCube.move(4)
    coord = tmpCube.getFlipUDSliceCoordinate()
    print(f"Raw coord: {coord}")
    print(f"Equivalence index: {coord//16}")
    print(f"Sym index: {coord%16}")
    
        
def testInitialCubieCubeState():
    tmpCube = FaceletCube()
    assert tmpCube.getCornerOrientationCoordinate() == 0
    assert tmpCube.getFlipUDSliceCoordinate() == 0
    
def runTests():
    ''' Simple CoordCube test suite. '''
    print("Running tests...")
    
    # testFlipUDSliceToRaw()
    
    # testMoveOnCubie()
    
    # testMoveOnCoordinate()
    
    # testMovesOnCoordCube(1237, 1592, 371)
    # testMovesOnCoordCube(0, 0, 0)
    # testMovesOnCoordCube(2046, 2186, 494)
    # testMovesOnCoordCube(2047, 2186, 494)
    # # for i in range(1000):
    # #     testMovesOnCoordCube(random.randint(0, 2047), random.randint(0, 2186), random.randint(0, 494))
    # testMovesOnCoordCube(2044, 314, 220)
    # testMovesOnCoordCube(327, 1108, 466)
    
    # testInitialCubieCubeState()
    # testInvertMoves(0, 0, 0)
    # testInvertMoves(2047, 2186, 494)
    # testInvertMoves(1237, 1592, 371)
    # testInvertMove()
    # testInvertMove2()
    testGetUDSlice()
    # testGetUDSlice2()
    # testMoveSymmetryThings()
    
    
    
    print("Completed tests")

if __name__ == "__main__":
    numpy.printoptions(threshold=sys.maxsize)
    string = "RRBUULUUBLDRBRRUDRFBDUFLDFFLDRRDBLFBDFLULLUBFDFFDBRULB"
    cube = FaceletCube(string)
    cube2 = FaceletCube()
    
    coordCube = CoordCube.from_cube(cube)
    
    # print((coord.pruningTable == 1).nonzero())
    # coordCube.solve()
    # coordCube.applySolution()
    
    # cube.move(1)
    # coordCube.move(3)
    # cube.printCoords()
    # coordCube.print()
    # tmpCube = FaceletCube()
    # tmpCube2 = FaceletCube()
    # tmpCube.setEdgeOrientationCoordinate(0)
    # tmpCube.setCornerOrientationCoordinate(0)
    # tmpCube.setUDSliceCoordinate(0)
    # print(tmpCube.edgePositions)
    # for sym in (9, 12): # these symmetries both result in the same raw coordinate, calculations here are correct, though.
    #     # there must be an issue in the coordinate symmetry calculation, likely within SymMult, for this to occur
    #     print(symmetry.edgePositionSymmetryLookup[sym])
    #     tmpCube2.applySymmetryEdge(tmpCube, sym)
    #     tmpCube2.printCoords()
    # flipUDSliceSym = tmpCube.getFlipUDSliceCoordinate()%16
    # print(flipUDSliceSym) # should be 
    # print(coordCube.solve())
    # print(f"CO: {cube.get()}")
    # print(index)
    # index = cube.getFlipUDSliceCoordinate()*2187 + cube.getCornerOrientationCoordinate()
    
    # this proves that getting the flipUDSlice coordinate of a cube from its raw coordinate then 
    # getting the raw coordinate from the flipUDSlice coordinate works, which should mean that
    # getFlipUDSliceCoordinate and FlipUDSliceToRawFlipUDSlice works (at least in terms of back and forth movements)
    # newCO = movetable.cornerOrientationMoveTable[cube.getCornerOrientationCoordinate(), 3]
    # print(f"FlipUDSlice: {cube.getFlipUDSliceCoordinate()}")
    # rawInitialFlipUDSlice = FlipUDSliceToRawFlipUDSlice[cube.getFlipUDSliceCoordinate() // 16]
    # print(f"Initial UD: {rawInitialFlipUDSlice // 2048}, Initial EO: {rawInitialFlipUDSlice % 2048}")
    # print('---------------------')
    # # initial raw coordinate here is different from the other raw coordinate, it is a symmetry, though
    
    # newUD = movetable.FlipUDSliceMoveTable[cube.getFlipUDSliceCoordinate()//16, 3]
    # # confirmed that flipUDslice, once moved, is not symmetrical with the cubie flipUDslice
    # print(f"FlipUDSlice after the move: {newUD}")
    # newUDRaw = FlipUDSliceToRawFlipUDSlice[newUD//16]
    # print(f"RawFlipUDSlice, converted through representant array: {newUDRaw}")
    # newEO, newUD = newUDRaw % 2048, newUDRaw // 2048
    # print(newEO)
    # print(newCO)
    # print(newUD)
    # print('-------------------')
    # index = coord.getIndexFromCoords(cube.getCornerOrientationCoordinate(), cube.getFlipUDSliceCoordinate(), 3)
    # flipCoord, cornCoord = index // 2187, index % 2187
    # print(f"flipCoord: {flipCoord}, cornCoord: {cornCoord}")
    # newUDRaw = FlipUDSliceToRawFlipUDSlice[flipCoord//16]
    # print(f"RawFlipUDSlice, converted through representant array: {newUDRaw}")
    # investigate more this is strange

    runTests()