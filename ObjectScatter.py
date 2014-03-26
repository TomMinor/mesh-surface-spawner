import maya.cmds as cmds
import random

accuracy = 0.1

import random

cmds.PencilCurveTool()
while(cmds.currentCtx() == 'pencilContext'): cmds.refresh()
print "Finished"

cmds.ls(type="nurbsCurve")

def spawnInCircle(nurbsName, num):
	radius = cmds.getAttr('%s.radius'%cmds.listConnections(cmds.listRelatives(nurbsName))[0])
	position = cmds.xform(nurbsName, q=True, t=True)
	rotation = cmds.xform(nurbsName, q=True, ro=True)
	for obj in xrange(num):
		cmds.polyCone()
		cmds.xform(t=position)
		cmds.xform(ro=rotation)
		cmds.rotate(0, random.uniform(0,360), 0, os=True, r=True)
		cmds.move(	random.uniform(0, radius),0, 0, os=True, r=True)
		
	
spawnInCircle('nurbsCircle1', 30)




def setPivotToBottom(objects, bottomAxis='y'):
    bottomAxis = bottomAxis.lower()
    offetAxis  = [False, False, False]

    if   bottomAxis == 'x': axis = 0
    elif bottomAxis == 'y': axis = 1
    elif bottomAxis == 'z': axis = 2
    else:
        print "Invalid axis %s" % bottomAxis
        return

    offetAxis[axis] = True

    for name in objects:
        offset = cmds.exactWorldBoundingBox(name)[axis]
        pivotName = ['%s.scalePivot'%name, '%s.rotatePivot'%name]
        cmds.move(offset, pivotName, x=offetAxis[0], y=offetAxis[1], z=offetAxis[2])


def volumeScatter(name, count):
    a=[]
    bbox = cmds.exactWorldBoundingBox(name)
    for i in range(count):
        x = random.uniform(bbox[0], bbox[3])
        y = random.uniform(bbox[1], bbox[4])
        z = random.uniform(bbox[2], bbox[5])

        newObj = cmds.polyCone()[0]
        a.append(newObj)

        cmds.move(x,y,z,newObj)
    return a


def constrainToSurface(surface, objects):
    for obj in objects:
        cmds.geometryConstraint( surface, obj )
        cmds.normalConstraint( surface, obj, aim=(0, 1, 0) )

def separateByVertexBrightness(name):
    meshDuplicate = cmds.duplicate(name, rr=True)[0]
    layers = parseMeshVertexColour(meshDuplicate)
    faceLayers = convertVtxToFace(layers, meshDuplicate)
    for faceSelection in faceLayers:
        if faceSelection:
            cmds.polyChipOff(faceSelection, ran=True)
#         if faceSelection:
#             for island in separateIntoPlanarElements(faceSelection):
#                 cmds.geomToBBox(island)
    return faceLayers

def convertVtxToFace(layers, name):
    faceLayers = [ [] for x in range(len(layers)) ]
    for i, layer in enumerate(layers):
        if layer:
            faces = cmds.polyListComponentConversion(['%s.vtx[%i]'%(name,vtx) for vtx in layer], fv=True, tf=True, vfa=True)
            faceLayers[i] = cmds.ls(faces, fl=True)

    #Remove duplicate selected faces from (lower weighted) layers
    uniqueFaces = set()
    for faceLayer in reversed(faceLayers):
        for face in faceLayer:
            if face in uniqueFaces:
                faceLayer.remove(face)
            else:
                uniqueFaces.add(face)
    return faceLayers

def separateIntoPlanarElements(name):
    # Use the automatic UV tool to do the heavy lifting in breaking up the 3d mesh for us
    cmds.polyAutoProjection('%s.f[0:%i]' % (name, cmds.polyEvaluate(name, f=True)), o=1, p=12)
    shells = getUVShells(name)
    for shell in shells: cmds.polyChipOff(shell)
    elements = cmds.polySeparate( name )[:-1]
    cmds.delete(elements[0])    # Delete the duplicate mesh
    return elements[1:]

# Modified version of 'prolow's script from
# http://tech-artists.org/forum/showthread.php?2596-Detecting-Overlapping-UV-Shells-in-Maya
#
def getUVShells(name):
    faces = cmds.ls(cmds.polyListComponentConversion(name, tf=True),fl=True)
    shells = []

    while len(faces) > 0:
        # Select the mesh faces based on the UV islands
        cmds.select( faces[0], r=True )
        cmds.polySelectConstraint(t=0)
        cmds.polySelectConstraint(sh=1,m=2)
        cmds.polySelectConstraint(sh=0,m=0)

        aShell=cmds.ls( sl=True, fl=True )
        shells.append( aShell )
        # Remove the face selection from faces so we don't select it again
        faces=list( set(faces) - set(aShell) )

    return shells









# cmds.select(cmds.polyListComponentConversion(['%s.vtx[%i]'%(meshDuplicate,vtx) for vtx in layers[-1]], fv=True, tf=True, vfa=True))
#
# for layer in layers:
#     if layer:
#         faceSelection = cmds.polyListComponentConversion(['%s.vtx[%i]'%(meshDuplicate,vtx) for vtx in layer], fv=True, tf=True, internal=True)
#         if faceSelection:
#             cmds.select(faceSelection)
#             cmds.polyChipOff(faceSelection, dup=True)
#
# faceIslands = ObjectScatter.separateIntoPlanarElements(meshDuplicate)[1:]

def exponentialRatio(layers, step, expoFunc=lambda x: x**2):

    expoSum = sum(expoFunc(layer) for layer in layers)
    return [(1/expoSum)*(expoFunc(layer)) for layer in layers]

def initMesh(name, stepAccuracy = 0.1):
    global accuracy
    accuracy = stepAccuracy
    cmds.polyColorSet(name, colorSet="meshDensitySet_#", clamped=1, rpt='RGB')
    cmds.polyColorPerVertex(name, r = 0.0, g = 0.0, b = 0.0)



def parseMeshVertexColour(name):
    global accuracy
    # Clamp accuracy
    if accuracy > 1.0: accuracy = 1.0
    itervtx = ['%s.vtx[%i]'%(name,i) for i in xrange(cmds.polyEvaluate(name, v=True)) ]
    vertCol = [cmds.polyColorPerVertex(v, query=True, rgb=True) for v in itervtx ]

    stepTotal = int(1/accuracy)
    layers = [ [] for i in xrange(0, stepTotal) ]

    for vtx, col in enumerate(vertCol):
        for i in xrange(len(layers)):
            minColour = [i*accuracy, i*accuracy, i*accuracy]
            maxColour = [(i+1)*accuracy, (i+1)*accuracy, (i+1)*accuracy]
            if (minColour < col <= maxColour):
                    layers[i].append(vtx)

    return layers

def positionObjects(objects):
        # We're only checking a subset of objects against themselves which is fairly nice
        # if we have lots of islands
        for obj in objects:
                bbox = cmds.exactWorldBoundingBox(obj)
                #print bbox
