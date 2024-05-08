# defines the cube according to facelets
from const import CornerFaceletMap, EdgeFaceletMap, CornerStrings, Corners, EdgeStrings, Edges, Symmetry, Moves
from const import CornerPositionMoveMap, CornerOrientationMoveMap, CornerPositionSymmetryMap, CornerOrientationSymmetryMap
from const import EdgePositionMoveMap, EdgeOrientationMoveMap, EdgePositionSymmetryMap, EdgeOrientationSymmetryMap
from const import multiplyCorner, multiplyEdge
import os, time, itertools
import numpy as np




class FaceletCube:
    ''' Defines the cube according to facelets and cubies (edges + corners with orientations)'''
    def __init__(self, string=None):
        if string:
            self.cornerPositions, self.edgePositions = [], []
            self.cornerOrientations, self.edgeOrientations = [], []
            self.from_str(string)
        else:
            self.cornerPositions = list(CornerPositionSymmetryMap[Symmetry.NN])
            self.edgePositions = list(EdgePositionSymmetryMap[Symmetry.NN])
            self.cornerOrientations = list(CornerOrientationSymmetryMap[Symmetry.NN])
            self.edgeOrientations = list(EdgeOrientationSymmetryMap[Symmetry.NN])
        
    
    def __str__(self):
        ''' TODO: Converts the cubie corner and edge positions back into facelets and pretty prints them '''
        return "done"
    
    def from_str(self, string):
        ''' Creates a facelet cube from a string of the format 
        'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB', where the sides correspond to the colors.
        '''
        for Corner_facelets in CornerFaceletMap.values():
            actual_corner = ''.join(string[facelet] for facelet in Corner_facelets)
            orientation = actual_corner.find("U") if "U" in actual_corner else actual_corner.find("D")
            self.cornerOrientations.append(orientation)
            position = CornerStrings.index(actual_corner[orientation:] + actual_corner[:orientation])
            self.cornerPositions.append(Corners(position))
        for Edge_facelets in EdgeFaceletMap.values():
            actual_edge = ''.join(string[facelet] for facelet in Edge_facelets)
            orientation = 0
            if "U" in actual_edge: orientation = actual_edge.find("U")
            elif "D" in actual_edge: orientation = actual_edge.find("D")
            elif "F" in actual_edge: orientation = actual_edge.find("F")
            else: orientation = actual_edge.find("B")
            self.edgeOrientations.append(orientation)
            position = EdgeStrings.index(actual_edge[orientation:] + actual_edge[:orientation])
            self.edgePositions.append(Edges(position))
            
    def getCornerOrientationCoordinate(self):
        ''' 2187 cases, one case for every permutation of corner orientations. '''
        return sum(self.cornerOrientations[i]*(3**(6-i)) for i in range(len(self.cornerOrientations)-1))
    
    def setCornerOrientationCoordinate(self, coord):
        ''' From the provided corner orientation coordinate, modify the orientations of the 
        corners to align with the coordinates. '''
        self.cornerOrientations = [0 for i in range(8)]
        tmpCoord = coord
        for i in range(7):
            self.cornerOrientations[i] = tmpCoord // 3**(6-i)
            tmpCoord -= self.cornerOrientations[i] * 3**(6-i)
        self.cornerOrientations[-1] = (3 - sum(self.cornerOrientations)) % 3
    
    def getEdgeOrientationCoordinate(self):
        ''' 2048 cases, one case for every permutation of edge orientations. '''
        return sum(self.edgeOrientations[i]*(2**(10-i)) for i in range(len(self.edgeOrientations)-1))
    
    def setEdgeOrientationCoordinate(self, coord):
        ''' From the provided edge orientation coordinate, modify the orientations of the
        edges to align with the coordinates. '''
        self.edgeOrientations = [0 for i in range(12)] 
        tmpCoord = coord
        for i in range(11):
            self.edgeOrientations[i] = tmpCoord // 2**(10-i)
            tmpCoord -= self.edgeOrientations[i] * 2**(10-i)
        self.edgeOrientations[-1] = (2 - sum(self.edgeOrientations)) % 2
    
    def getUDSliceCoordinate(self):
        '''495 cases, one case for every permutation of the four UDSlice coordinates (the edges that 
        aren't on the U and D slice)'''
        UDSliceEdges = list(0 for i in range(12))
        for i, edge in enumerate(self.edgePositions):
            if edge in (Edges.FL, Edges.FR, Edges.BL, Edges.BR):
                UDSliceEdges[i] = 1
        if UDSliceLookupDict:
            return UDSliceLookupDict[tuple(UDSliceEdges)]
        else:
            return FaceletCube.getUDSliceFromEdgesList(UDSliceEdges)
    
    @staticmethod
    def getUDSliceFromEdgesList(edgesList):
        coordSum = 0
        numEdgesPassed = 0
        for i in range(edgesList.index(1), len(edgesList)):
            if edgesList[i] == 1:
                numEdgesPassed += 1
            else:
                coordSum += binomial(i, numEdgesPassed-1)
        return int(coordSum)
        
    def setUDSliceCoordinate(self, coord):
        ''' From the provided UDSlice coordinate, modify the positions of the UDSlice edges to align with 
        the UDSlice coordinate'''
        arr = InvUDSliceLookupDict[coord]
        UDEdgeIndices = list(self.edgePositions.index(item) for item in (Edges.FR, Edges.FL, Edges.BL, Edges.BR))
        swapIndices = list(i for i in range(len(arr)) if arr[i])
        for item in UDEdgeIndices:
            if item in swapIndices:
                swapIndices.remove(item)
                UDEdgeIndices.remove(item)
        for i in range(len(swapIndices)):
            tmp = self.edgePositions[swapIndices[i]]
            self.edgePositions[swapIndices[i]] = self.edgePositions[UDEdgeIndices[i]]
            self.edgePositions[UDEdgeIndices[i]] = tmp
            
    @staticmethod
    def createUDSliceCoordinateLookupTable():
        coordinateLookupTable = {}
        for i in range(3, 12):
            for k in range(2, i):
                for j in range(1, k):
                    for l in range(0, j):
                        arr = tuple(1 if x in (i, k, j, l) else 0 for x in range(12))
                        coordinateLookupTable[arr] = FaceletCube.getUDSliceFromEdgesList(arr)
        return coordinateLookupTable
    
    def getRawFlipUDSliceCoordinate(self):
        ''' Combines UDSlice and EdgeOrientation into 1013760 cases, which describes both of the orientations'''
        return self.getUDSliceCoordinate() * 2048 + self.getEdgeOrientationCoordinate()
    
    @staticmethod
    def FlipUDSliceLookup(coord):
        ''' Checks if a coordinate is in the flipUDslice lookup table through a binary search.'''
        lowerBound = 0
        upperBound = 64430
        while lowerBound < upperBound:
            middle = (lowerBound + upperBound) // 2
            if coord < FlipUDSliceToRawFlipUDSlice[middle]: upperBound = middle
            elif coord > FlipUDSliceToRawFlipUDSlice[middle]: lowerBound = middle+1
            else: return middle
        return -1
    
    def setRawFlipUDSliceCoordinate(self, coord):
        self.setUDSliceCoordinate(coord // 2048)
        self.setEdgeOrientationCoordinate(coord % 2048)
    
    def getFlipUDSliceCoordinate(self):
        ''' Returns the sym coordinate flipUDSlice.'''
        tmpCube = FaceletCube()
        # print(self.getRawFlipUDSliceCoordinate())
        # print(self.edgePositions)
        rv = -1
        for i in range(16):
            tmpCube.applySymmetryEdge(self, i)
            RawSymmetryCoord = tmpCube.getRawFlipUDSliceCoordinate()
            # print(f"{i}: {RawSymmetryCoord}")
            index = FaceletCube.FlipUDSliceLookup(RawSymmetryCoord)
            # THESE SHOULD NOT HAVE MULTIPLE SYMMETRIES I THINK
            # New issue: When symmetries are applied to certain cubes, some cubes will have multiple of the same symmetry.
            
            if index != -1:
                # rv = 16*index+i # change this back if it doesn't work, but it seems to be the solution for something
                return 16*index+i
    
        return rv
        raise ValueError()
            # check if the symmetry coord is in the indexToRepresentants array; if it is, then return the index*16 + the symmetry
            
    def getCornerPermutationCoordinate(self):
        # if cornerPermLookupDict:
        #     return cornerPermLookupDict[self.cornerPositions]
        coord = 0
        for i in range(1, 8):
            num = sum(k for k in range(i) if self.cornerPositions[k] > self.cornerPositions[i])
            coord += factorial(num)
        return coord
            
    
    def setCornerPermutationCoordinate(self, coord):
        self.cornerPositions = InvCornerPermLookupDict[coord]
        
    def printCoords(self):
        print('-----------Cube Coordinates------------')
        print(f"CornerOrientation: {self.getCornerOrientationCoordinate()}")
        print(f"EdgeOrientation: {self.getEdgeOrientationCoordinate()}")
        print(f"UDSlice: {self.getUDSliceCoordinate()}")
        print(f"RawFlipUDSlice: {self.getRawFlipUDSliceCoordinate()}")
        print(f"FlipUDSlice: {self.getFlipUDSliceCoordinate()}\n")
    
    @staticmethod
    def createRawCornerPermutationLookupTable():
        tmpCube = FaceletCube()
        cornerCombinations = list(itertools.permutations(tmpCube.cornerPositions))
        lookupTable = {}
        for i in range(40320):
            tmpCube.cornerPositions = cornerCombinations[i]
            lookupTable[tuple(tmpCube.cornerPositions)] = tmpCube.getCornerPermutationCoordinate()
        return lookupTable
        # for
        
    def getEdgePermutationCoordinate(self):
        # if edgePermLookupDict:
        #     return edgePermLookupDict[self.edgePositions[:8]]
        coord = 0
        for i in range(1, 8):
            num = sum(k for k in range(i) if self.edgePositions[k] > self.edgePositions[i])
            coord += factorial(num)
        return coord
    
    def setEdgePermutationCoordinate(self, coord):
        self.edgePositions = invEdgePermLookupDict[coord] + self.edgePositions[8:]
    
    @staticmethod
    def createRawEdgePermutationLookupTable():
        tmpCube = FaceletCube()
        edgeCombinations = list(itertools.permutations(tmpCube.edgePositions[:8]))
        lookupTable = {}
        for i in range(40320):
            tmpCube.edgePositions = list(edgeCombinations[i]) + tmpCube.edgePositions[8:]
            lookupTable[tuple(tmpCube.edgePositions)] = tmpCube.getEdgePermutationCoordinate()
        return lookupTable
    
    def move(self, move):
        self.cornerPositions, self.cornerOrientations = multiplyCorner( \
            self.cornerPositions, CornerPositionMoveMap[move], \
            self.cornerOrientations, CornerOrientationMoveMap[move])
        self.edgePositions, self.edgeOrientations = multiplyEdge( \
            self.edgePositions, EdgePositionMoveMap[move], \
            self.edgeOrientations, EdgeOrientationMoveMap[move])
        
#         invSymmetryLookup = FaceletCube.createInvSymmetryLookupTable()
# SymMult = FaceletCube.createSymMultLookupTable()
    def applySymmetryEdge(self, cube, index):
        prodPos, prodOri = multiplyEdge(FaceletCube.edgePositionSymmetryLookup[FaceletCube.invSymmetryLookup[index]], cube.edgePositions, \
            FaceletCube.edgeOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[index]], cube.edgeOrientations)
        self.edgePositions, self.edgeOrientations = multiplyEdge(prodPos, FaceletCube.edgePositionSymmetryLookup[index], \
            prodOri, FaceletCube.edgeOrientationSymmetryLookup[index])
        
    def applyInvSymmetryEdge(self, cube, index):
        prodPos, prodOri = multiplyEdge(FaceletCube.edgePositionSymmetryLookup[index], cube.edgePositions, \
            FaceletCube.edgeOrientationSymmetryLookup[index], cube.edgeOrientations)
        self.edgePositions, self.edgeOrientations = multiplyEdge(prodPos, FaceletCube.edgePositionSymmetryLookup[FaceletCube.invSymmetryLookup[index]], \
            prodOri, FaceletCube.edgeOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[index]])
        
    def applySymmetryCorner(self, cube, index):
        prodPos, prodOri = multiplyCorner(FaceletCube.cornerPositionSymmetryLookup[FaceletCube.invSymmetryLookup[index]], cube.cornerPositions, \
            FaceletCube.cornerOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[index]], cube.cornerOrientations)
        self.cornerPositions, self.cornerOrientations = multiplyCorner(prodPos, FaceletCube.cornerPositionSymmetryLookup[index], \
            prodOri, FaceletCube.cornerOrientationSymmetryLookup[index])
        
    def applyInvSymmetryCorner(self, cube, index):
        prodPos, prodOri = multiplyCorner(FaceletCube.cornerPositionSymmetryLookup[index], cube.cornerPositions, \
            FaceletCube.cornerOrientationSymmetryLookup[index], cube.cornerOrientations) # maybe change the order back if things don't work
        self.cornerPositions, self.cornerOrientations = multiplyCorner(prodPos, FaceletCube.cornerPositionSymmetryLookup[FaceletCube.invSymmetryLookup[index]], \
            prodOri, FaceletCube.cornerOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[index]])
        
        
    def applySymmetry(self, cube, index):
        ''' Applies the symmetry at the index to the cube, where the symmetry is described as:
        S(i)' * C * S(i), where S(i) is the symmetry, C is the cube, and S(i)' is the inverse of the symmetry.
        Takes the values from the current cube and updates the parameter cube with the new symmetry. '''
        self.applySymmetryEdge(cube, index)
        self.applySymmetryCorner(cube, index)
        
    def applySymmetryDirect(self, symName):    
        ''' Directly applies a symmetry to the cube. '''
        self.cornerPositions, self.cornerOrientations = \
            multiplyCorner(self.cornerPositions, CornerPositionSymmetryMap[symName], \
                           self.cornerOrientations, CornerOrientationSymmetryMap[symName])
        self.edgePositions, self.edgeOrientations = \
            multiplyEdge(self.edgePositions, EdgePositionSymmetryMap[symName], \
                           self.edgeOrientations, EdgeOrientationSymmetryMap[symName])
    
    @staticmethod
    def createSymmetryLookupTables():
        ''' Creates a table for every symmetry. '''
        edgePos, edgeOri, cornPos, cornOri = {}, {}, {}, {}
        tmpCube = FaceletCube()
        index = 0
        for i in range(2): # S_F2
            for k in range(4): # S_U4
                for j in range(2): # S_LR2
                    edgePos[index] = [item for item in tmpCube.edgePositions]
                    edgeOri[index] = [item for item in tmpCube.edgeOrientations]
                    cornPos[index] = [item for item in tmpCube.cornerPositions]
                    cornOri[index] = [item for item in tmpCube.cornerOrientations]
                    tmpCube.applySymmetryDirect(Symmetry.LR)
                    index += 1
                tmpCube.applySymmetryDirect(Symmetry.U4)
            tmpCube.applySymmetryDirect(Symmetry.F2)
    #     edgePositionSymmetryLookup, edgeOrientationSymmetryLookup, \
    # cornerPositionSymmetryLookup, cornerOrientationSymmetryLookup = FaceletCube.createSymmetryLookupTables()
        FaceletCube.edgePositionSymmetryLookup, FaceletCube.edgeOrientationSymmetryLookup = edgePos, edgeOri
        FaceletCube.cornerPositionSymmetryLookup, FaceletCube.cornerOrientationSymmetryLookup = cornPos, cornOri
    
    @staticmethod
    def createInvSymmetryLookupTable():
        if not FaceletCube.edgePositionSymmetryLookup: return -1
        invSymmetry = {}
        for i in range(16): # S(i) * S(i)^-1 = Identity (Symmetry.NN)
            for k in range(16):
                prodCornPos = multiplyCorner(FaceletCube.cornerPositionSymmetryLookup[i], FaceletCube.cornerPositionSymmetryLookup[k], \
                    FaceletCube.cornerOrientationSymmetryLookup[i], FaceletCube.cornerOrientationSymmetryLookup[k])[0]
                if all(prodCornPos[i] == i for i in range(3)):
                    invSymmetry[i] = k
        FaceletCube.invSymmetryLookup = invSymmetry

    @staticmethod
    def createSymMultLookupTable():
        ''' Multiplies a symmetry with another symmetry. '''
        tmpSymMult = np.empty((16, 16), dtype=np.int32)
        for i in range(16):
            for k in range(16): # every possible symmetry
                cornPosProd = multiplyCorner(FaceletCube.cornerPositionSymmetryLookup[i], FaceletCube.cornerPositionSymmetryLookup[k], \
                    FaceletCube.cornerOrientationSymmetryLookup[i], FaceletCube.cornerOrientationSymmetryLookup[k])[0]
                for j in range(16):
                    if all(cornPosProd[l] == FaceletCube.cornerPositionSymmetryLookup[j][l] for l in range(8)):
                        tmpSymMult[i, k] = j
                        break
        FaceletCube.SymMult = tmpSymMult
        
    @staticmethod
    def createMoveTable():
        tmpCube = FaceletCube()
        tmpCube2 = FaceletCube()
        moveTable = {}
        
        def isIdentity(cube):
            rv = True
            for i2 in range(8):
                if cube.cornerPositions[i2] != i2 or cube.cornerOrientations[i2] != 0: 
                    rv = False
                    break
            return rv
        
        for move in Moves:
            for k in range(4):
                tmpCube.move(move)
                if k != 3:
                #     print(f"-----------\nMove {move*3+k}")
                #     print(tmpCube.cornerPositions)
                    for i in range(16):
                        # if i == 9 and move*3+k == 5:
                        #     print(tmpCube.cornerPositions)
                        tmpCube2.applyInvSymmetryCorner(tmpCube, i)
                        # if i == 9 and move*3+k == 5:
                        #     print(tmpCube2.cornerPositions)
                        n = 0
                        for move2 in Moves:
                            for k2 in range(4):
                                tmpCube2.move(move2)
                                if k2 != 3 and isIdentity(tmpCube2):
                                    n += 1
                                    moveTable[i, (3*move+k)] = (3*move2+(2-k2)) # probably the most aura I've used on a level one crook (bug)
                        assert n == 1
        # check this function out a little more, make sure it actually works
        FaceletCube.SymMove = moveTable
      
    @staticmethod  
    def debug():
        # for i, v in FaceletCube.cornerPositionSymmetryLookup.items():
        #     print(f'{i}: {v}\n')
        # tmpCube, tmpCube2 = FaceletCube(), FaceletCube()
        # tmpCube.move(4)
        # tmpCube.move(4)
        # tmpCube.move(4)
        # tmpCube2.applyInvSymmetryCorner(tmpCube, 6)
        # print('Symmetries:')
        # print(FaceletCube.cornerPositionSymmetryLookup[FaceletCube.invSymmetryLookup[6]])
        # print(FaceletCube.cornerOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[6]])
        # cornOris = [0, 1, 2, 0, 0, 2, 1, 0]
        # cornPos = [1, 6, 2, 0, 5, 7, 3, 4]
        # rvPos, rvOri = multiplyCorner(cornPos, FaceletCube.cornerPositionSymmetryLookup[FaceletCube.invSymmetryLookup[6]], \
        #     cornOris, FaceletCube.cornerOrientationSymmetryLookup[FaceletCube.invSymmetryLookup[6]])
        # print(rvPos)
        # print(rvOri)
        # print('whatup')
        pass
        
    
    @staticmethod
    def createFlipUDSliceIndexToRepresentant():
        ''' TODO: check for file present'''
        if os.path.exists('.\\lookups\\FlipUDSlice.npy'):
            return np.load('.\\lookups\\FlipUDSlice.npy')
        occupied = np.zeros(495*2048, dtype='bool')
        indexToRepresentantArr = np.zeros(64430, dtype=np.uint32)
        repArrIndex = 0
        tmpCube = FaceletCube()
        tmpCube2 = FaceletCube()
        for i in range(495): # all UDSlice values
            tmpCube.setUDSliceCoordinate(i)
            for k in range(2048): # All EdgeOrientation values
                if not occupied[i*2048+k]:
                    tmpCube.setEdgeOrientationCoordinate(k)
                    indexToRepresentantArr[repArrIndex] = i*2048+k
                    repArrIndex += 1
                    for s in range(16): # All Symmetries
                        tmpCube2.applySymmetryEdge(tmpCube, s)
                        coord = tmpCube2.getRawFlipUDSliceCoordinate()
                        occupied[coord] = True

        indexToRepresentantArr.tofile('.\\lookups\\FlipUDSliceView', sep='\n')
        np.save('.\\lookups\\FlipUDSlice', indexToRepresentantArr)
        
        return indexToRepresentantArr
    
    @staticmethod
    def createCornerPermIndexToRepresentant():
        if os.path.exists('.\\lookups\\CornerPermutations.npy'):
            return np.load('.\\lookups\\CornerPermutations.npy')
        occupied = np.zeros(40320, dtype='bool')
        indexToRepresentantArr = np.zeros(2768, dtype=np.uint32)
        tmpCube, tmpCube2 = FaceletCube(), FaceletCube()
        index = 0
        for i in range(40320):
            if not occupied[i]:
                tmpCube.setCornerPermutationCoordinate(i)
                indexToRepresentantArr[index] = i
                index += 1
                for k in range(16):
                    tmpCube2.applySymmetryCorner(tmpCube, k)
                    coord = tmpCube2.getCornerPermutationCoordinate()
                    occupied[coord] = True
                    

def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * factorial(n-1)

def binomial(n, k):
    return factorial(n) / (factorial(k) * factorial(n-k))

FaceletCube.createSymmetryLookupTables()
FaceletCube.createInvSymmetryLookupTable()
FaceletCube.createSymMultLookupTable()
FaceletCube.createMoveTable()

UDSliceLookupDict = FaceletCube.createUDSliceCoordinateLookupTable()
InvUDSliceLookupDict = {k:i for i, k in UDSliceLookupDict.items()}

cornerPermLookupDict = FaceletCube.createRawCornerPermutationLookupTable()
InvCornerPermLookupDict = {k:i for i, k in cornerPermLookupDict.items()}

edgePermLookupDict = FaceletCube.createRawEdgePermutationLookupTable()
invEdgePermLookupDict = {k:i for i, k in edgePermLookupDict.items()}

FlipUDSliceToRawFlipUDSlice = FaceletCube.createFlipUDSliceIndexToRepresentant()
# CornerPermToRawCornerPerm = FaceletCube.createCornerPermIndexToRepresentant()
# print(FaceletCube.invSymmetryLookup)
# for i, v in FaceletCube.cornerPositionSymmetryLookup.items():
#     print(f"{i}: {v}\n")
# for i, v in CornerPositionSymmetryMap.items():
#     print(f"{i}: {v}\n")
# print(FaceletCube.SymMove[6, 14])
# FaceletCube.debug()