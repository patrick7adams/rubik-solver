from enum import IntEnum

class Facelets(IntEnum):
    U1 = 0
    U2 = 1
    U3 = 2
    U4 = 3
    U5 = 4
    U6 = 5
    U7 = 6
    U8 = 7
    U9 = 8
    R1 = 9
    R2 = 10
    R3 = 11
    R4 = 12
    R5 = 13
    R6 = 14
    R7 = 15
    R8 = 16
    R9 = 17
    F1 = 18
    F2 = 19
    F3 = 20
    F4 = 21
    F5 = 22
    F6 = 23
    F7 = 24
    F8 = 25
    F9 = 26
    D1 = 27
    D2 = 28
    D3 = 29
    D4 = 30
    D5 = 31
    D6 = 32
    D7 = 33
    D8 = 34
    D9 = 35
    L1 = 36
    L2 = 37
    L3 = 38
    L4 = 39
    L5 = 40
    L6 = 41
    L7 = 42
    L8 = 43
    L9 = 44
    B1 = 45
    B2 = 46
    B3 = 47
    B4 = 48
    B5 = 49
    B6 = 50
    B7 = 51
    B8 = 52
    B9 = 53
    
class Moves(IntEnum):
    U = 0
    R = 1
    F = 2
    D = 3
    L = 4
    B = 5
    
class ExtendedMoves(IntEnum):
    U = 0
    U2 = 1
    U3 = 2
    R = 3
    R2 = 4
    R3 = 5
    F = 6
    F2 = 7
    F3 = 8
    D = 9
    D2 = 10
    D3 = 11
    L = 12
    L2 = 13
    L3 = 14
    B = 15
    B2 = 16
    B3 = 17
    
P2Moves = (0, 1, 2, 4, 7, 10, 13, 15, 16, 17)

class Corners(IntEnum):
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3
    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7
    
class Edges(IntEnum):
    UR = 0
    UF = 1
    UL = 2
    UB = 3
    DR = 4
    DF = 5
    DL = 6
    DB = 7
    FR = 8
    FL = 9
    BL = 10
    BR = 11
    
CornerStrings = ["URF", "UFL", "ULB", "UBR", "DFR", "DLF", "DBL", "DRB"]
EdgeStrings = ["UR", "UF", "UL", "UB", "DR", "DF", "DL", "DB", "FR", "FL", "BL", "BR"]
    
CornerFaceletMap = {
    Corners.URF: (Facelets.U9, Facelets.R1, Facelets.F3),
    Corners.UFL: (Facelets.U7, Facelets.F1, Facelets.L3),
    Corners.ULB: (Facelets.U1, Facelets.L1, Facelets.B3),
    Corners.UBR: (Facelets.U3, Facelets.B1, Facelets.R3),
    Corners.DFR: (Facelets.D3, Facelets.F9, Facelets.R7),
    Corners.DLF: (Facelets.D1, Facelets.L9, Facelets.F7),
    Corners.DBL: (Facelets.D7, Facelets.B9, Facelets.L7),
    Corners.DRB: (Facelets.D9, Facelets.R9, Facelets.B7)
}

EdgeFaceletMap = {
    Edges.UR: (Facelets.U6, Facelets.R2),
    Edges.UF: (Facelets.U8, Facelets.F2),
    Edges.UL: (Facelets.U4, Facelets.L2),
    Edges.UB: (Facelets.U2, Facelets.B2),
    Edges.DR: (Facelets.D6, Facelets.R8),
    Edges.DF: (Facelets.D2, Facelets.F8),
    Edges.DL: (Facelets.D4, Facelets.L8),
    Edges.DB: (Facelets.D8, Facelets.B8),
    Edges.FR: (Facelets.F6, Facelets.R4),
    Edges.FL: (Facelets.F4, Facelets.L6),
    Edges.BL: (Facelets.B6, Facelets.L4),
    Edges.BR: (Facelets.B4, Facelets.R6),
}

CornerPositionMoveMap = {
    Moves.U: (Corners.UBR, Corners.URF, Corners.UFL, Corners.ULB, \
            Corners.DFR, Corners. DLF, Corners.DBL, Corners.DRB),
    Moves.R: (Corners.DFR, Corners.UFL, Corners.ULB, Corners.URF, \
            Corners.DRB, Corners.DLF, Corners.DBL, Corners.UBR),
    Moves.F: (Corners.UFL, Corners.DLF, Corners.ULB, Corners.UBR, \
            Corners.URF, Corners.DFR, Corners.DBL, Corners.DRB),
    Moves.D: (Corners.URF, Corners.UFL, Corners.ULB, Corners.UBR, \
            Corners.DLF, Corners.DBL, Corners.DRB, Corners.DFR),
    Moves.L: (Corners.URF, Corners.ULB, Corners.DBL, Corners.UBR, \
            Corners.DFR, Corners.UFL, Corners.DLF, Corners.DRB),
    Moves.B: (Corners.URF, Corners.UFL, Corners.UBR, Corners.DRB, \
            Corners.DFR, Corners.DLF, Corners.ULB, Corners.DBL)
}

CornerOrientationMoveMap = {
    Moves.U: (0, 0, 0, 0, 0, 0, 0, 0),
    Moves.R: (2, 0, 0, 1, 1, 0, 0, 2),
    Moves.F: (1, 2, 0, 0, 2, 1, 0, 0),
    Moves.D: (0, 0, 0, 0, 0, 0, 0, 0),
    Moves.L: (0, 1, 2, 0, 0, 2, 1, 0),
    Moves.B: (0, 0, 1, 2, 0, 0, 2, 1)
}

EdgePositionMoveMap = {
    Moves.U: (Edges.UB, Edges.UR, Edges.UF, Edges.UL, Edges.DR, Edges.DF, \
        Edges.DL, Edges.DB, Edges.FR, Edges.FL, Edges.BL, Edges.BR),
    Moves.R: (Edges.FR, Edges.UF, Edges.UL, Edges.UB, Edges.BR, Edges.DF, \
        Edges.DL, Edges.DB, Edges.DR, Edges.FL, Edges.BL, Edges.UR),
    Moves.F: (Edges.UR, Edges.FL, Edges.UL, Edges.UB, Edges.DR, Edges.FR, \
        Edges.DL, Edges.DB, Edges.UF, Edges.DF, Edges.BL, Edges.BR),
    Moves.D: (Edges.UR, Edges.UF, Edges.UL, Edges.UB, Edges.DF, Edges.DL, \
        Edges.DB, Edges.DR, Edges.FR, Edges.FL, Edges.BL, Edges.BR),
    Moves.L: (Edges.UR, Edges.UF, Edges.BL, Edges.UB, Edges.DR, Edges.DF, \
        Edges.FL, Edges.DB, Edges.FR, Edges.UL, Edges.DL, Edges.BR),
    Moves.B: (Edges.UR, Edges.UF, Edges.UL, Edges.BR, Edges.DR, Edges.DF, \
        Edges.DL, Edges.BL, Edges.FR, Edges.FL, Edges.UB, Edges.DB)
}

EdgeOrientationMoveMap = {
    Moves.U: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    Moves.R: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    Moves.F: (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0),
    Moves.D: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    Moves.L: (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    Moves.B: (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)
}

def multiplyEdge(edgepos1, edgepos2, edgeori1, edgeori2):
    ''' Multiplies the first tuple of edges by the second tuple of edges. For example:
    Multiplying (UB, UR, UF, UL) by (UL, UF, UB, UR) will return (UR, UL, UF, UB). Multiplying returns
    the value at the index of the first value. Because UB maps to 3, the first returned position will be edgepos2[3]. 
    In general the returned position is pos1[pos2[i]]. The orientations are simply added to each other and taken
    the modulus of. '''
    return ([edgepos1[edgepos2[i]] for i in range(12)], [(edgeori2[i] + edgeori1[edgepos2[i]]) % 2 for i in range(12)])
    
def multiplyCorner(cornpos1, cornpos2, cornori1, cornori2):
    ''' Multiplies the first corner by the second corner. Reference multiplyEdge for more details.'''
    cornPositions = [cornpos1[cornpos2[i]] for i in range(8)]
    cornOrientations = [(cornori2[i] + cornori1[cornpos2[i]]) % 3 for i in range(8)]
    # the most aura I've ever used on the multiplyCorner function (dammit)
    return (cornPositions, cornOrientations)