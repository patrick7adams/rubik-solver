# defines the cube according to facelets
from const import CornerFaceletMap, EdgeFaceletMap, CornerStrings, Corners, EdgeStrings, Edges, Moves
from const import CornerPositionMoveMap, CornerOrientationMoveMap, EdgePositionMoveMap, EdgeOrientationMoveMap
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
            self.cornerPositions = [i for i in range(8)]
            self.edgePositions = [i for i in range(12)]
            self.cornerOrientations = [0 for i in range(8)]
            self.edgeOrientations = [0 for i in range(12)]
        
    
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

def factorial(n):
        if n == 0 or n == 1:
            return 1
        else:
            return n * factorial(n-1)

def binomial(n, k):
    return factorial(n) / (factorial(k) * factorial(n-k))

UDSliceLookupDict = FaceletCube.createUDSliceCoordinateLookupTable()
InvUDSliceLookupDict = {k:i for i, k in UDSliceLookupDict.items()}

cornerPermLookupDict = FaceletCube.createRawCornerPermutationLookupTable()
InvCornerPermLookupDict = {k:i for i, k in cornerPermLookupDict.items()}

edgePermLookupDict = FaceletCube.createRawEdgePermutationLookupTable()
invEdgePermLookupDict = {k:i for i, k in edgePermLookupDict.items()}