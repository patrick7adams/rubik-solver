# from const import Symmetry, EdgePositionSymmetryMap, EdgeOrientationSymmetryMap, CornerPositionSymmetryMap, CornerOrientationSymmetryMap
# from const import multiplyEdge, multiplyCorner, Moves

# def createSymmetryLookupTables():
#     ''' Creates a table for every symmetry. '''
#     edgePos, edgeOri, cornPos, cornOri = {}, {}, {}, {}
#     for i in range(2): # S_F2
#         for k in range(4): # S_U4
#             for j in range(2): # S_LR2
#                 n = i*8 + k*2 + j
#                 prodEdgePos = EdgePositionSymmetryMap[Symmetry.NN]
#                 prodEdgeOri = EdgeOrientationSymmetryMap[Symmetry.NN]
#                 prodCornPos = CornerPositionSymmetryMap[Symmetry.NN]
#                 prodCornOri = CornerOrientationSymmetryMap[Symmetry.NN]
#                 if i == 1:
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.F2], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.F2])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.F2], prodCornOri, CornerOrientationSymmetryMap[Symmetry.F2])
#                 for l in range(k):
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.U4], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.U4])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.U4], prodCornOri, CornerOrientationSymmetryMap[Symmetry.U4])
#                 if j == 1:
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.LR], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.LR])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.LR], prodCornOri, CornerOrientationSymmetryMap[Symmetry.LR])
#                 edgePos[n] = prodEdgePos
#                 edgeOri[n] = prodEdgeOri
#                 cornPos[n] = prodCornPos
#                 cornOri[n] = prodCornOri
#     return edgePos, edgeOri, cornPos, cornOri

# def createInvSymmetryLookupTables():
#     ''' Creates a table for every inverse symmetry. TODO: maybe refactor with new inverse methods below? '''
#     edgePos, edgeOri, cornPos, cornOri = {}, {}, {}, {}
#     tmpCube = FaceletCube()
#     for i in range(2): # S_F2
#         for k in range(4): # S_U4
#             for j in range(2): # S_LR2
#                 n = i*8 + k*2 + j
#                 prodEdgePos = EdgePositionSymmetryMap[Symmetry.NN]
#                 prodEdgeOri = EdgeOrientationSymmetryMap[Symmetry.NN]
#                 prodCornPos = CornerPositionSymmetryMap[Symmetry.NN]
#                 prodCornOri = CornerOrientationSymmetryMap[Symmetry.NN]
#                 if j == 1:
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.LR], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.LR])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.LR], prodCornOri, CornerOrientationSymmetryMap[Symmetry.LR])
#                 for l in range(4-k if k > 0 else 0):
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.U4], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.U4])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.U4], prodCornOri, CornerOrientationSymmetryMap[Symmetry.U4])
#                 if i == 1:
#                     prodEdgePos, prodEdgeOri = multiplyEdge(prodEdgePos, EdgePositionSymmetryMap[Symmetry.F2], prodEdgeOri, EdgeOrientationSymmetryMap[Symmetry.F2])
#                     prodCornPos, prodCornOri = multiplyCorner(prodCornPos, CornerPositionSymmetryMap[Symmetry.F2], prodCornOri, CornerOrientationSymmetryMap[Symmetry.F2])
#                 edgePos[n] = prodEdgePos
#                 edgeOri[n] = prodEdgeOri
#                 cornPos[n] = prodCornPos
#                 cornOri[n] = prodCornOri
            
            
#     return edgePos, edgeOri, cornPos, cornOri

# def createSymMultLookupTable():
#     ''' Multiplies a symmetry with another symmetry. '''
#     tmpSymMult = {}
#     for i in range(16):
#         for k in range(16): # every possible symmetry
#             cornPosProd = multiplyCorner(cornerPositionSymmetryLookup[i], cornerPositionSymmetryLookup[k], \
#                 cornerOrientationSymmetryLookup[i], cornerOrientationSymmetryLookup[k])[0]
#             for j in range(16):
#                 if all(cornPosProd[l] == cornerPositionSymmetryLookup[j][l] for l in range(3)):
#                     tmpSymMult[(i, k)] = j
#                     break
#     return tmpSymMult


# def invEdgeSymmetry(edgePos, edgeOri):
#     ''' Returns the inverse symmetry of the edge positions and orientations provided.'''
#     tmpEdgePos = [-1 for i in range(12)]
#     for i in range(12):
#         tmpEdgePos[edgePos[i]] = i
#     return (tmpEdgePos, [(2-item)%2 for item in edgeOri])

# def invCornerSymmetry(cornPos, cornOri):
#     tmpCornPos = [-1 for i in range(8)]
#     for i in range(8):
#         tmpCornPos[cornPos[i]] = i
#     return (tmpCornPos, [(3-item)%3 for item in cornOri])




# # print(EdgePositionSymmetryMap[Symmetry.F2])
# # print(EdgePositionSymmetryMap[Symmetry.U4])
        