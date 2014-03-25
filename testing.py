import maya.cmds as cmds
import random
#from ObjectScatter import *
import ObjectScatter
reload(ObjectScatter)


import maya.cmds as cmds
import random

points = [ cmds.pointPosition('curve1.cv[%i]'%i) for i in range(cmds.getAttr('curve1.spans') + cmds.getAttr('curve1.degree')) ]
tangent = [ cmds.pointOnCurve('curve1', pr=(1.0/23)*i, t=True) for i in range(23) ]

for pos in points:
	cmds.select(cmds.polyCone(r=0.2, h=0.2)[0])
	cmds.move(pos[0], pos[1], pos[2])
	cmds.select(['curve1', cmds.ls(sl=True)[0]]) 
	cmds.tangentConstraint(aimVector=(0,1,0), upVector=(1,0,1), worldUpType="vector",worldUpVector=(0,1,0))


new = cmds.polyCube()[0]
cmds.rotate(0, random.uniform(0, 360), 0)
cmds.move(random.uniform(0,8), 0, 0, os=True)


# UI
winName = "Object Scatter"
if(cmds.window(winName, exists=True)):
        cmds.deleteUI(winName)

window = cmds.window( title=winName, iconName=winName, widthHeight=(512, 512), maximizeButton=False )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label='Vertex Paint', command=lambda x: (cmds.PaintVertexColorToolOptions(), cmds.select(all=True)) )

cmds.showWindow(window)

surface = cmds.ls(sl=True, l=True)
bbox = cmds.geomToBBox(surface, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_#"%surface)
objects = volumeScatter(bbox, 600)
setPivotToBottom(objects)
cmds.delete(bbox)
constrainToSurface(surface, objects)
positionObjects(objects)

cmds.delete(objects)
del objects

meshName = cmds.ls(sl=True)[0]
ObjectScatter.initMesh(meshName)

cmds.PaintVertexColorToolOptions()

result = ObjectScatter.separateByVertexBrightness(meshName)

sum=0
for layer in layers: sum += len(layer)

ratios = [ (len(layer)/float(sum)) for layer in layers ]

print ratios

newsum = 0
for x in ratios: newsum += x

objCount = 150
density = [0] * stepTotal

cmds.select(cmds.polyListComponentConversion(['%s.vtx[%i]'%(meshDuplicate,vtx) for vtx in layers[-1]], fv=True, tf=True, vfa=True))

#randomly distribute meshes using ratios of density:amount
for layer in layers:
    #density[i] = int(ratios[i] * objCount)
    if layer:
        print layer
        # Break off the vertex colour islands into separate objects
        faceSelection = cmds.polyListComponentConversion(['%s.vtx[%i]'%(meshDuplicate,vtx) for vtx in layer], fv=True, tf=True, internal=True)
        """ Edge case """
        # If only a less than 4 vertices are selected, the internal flag will mean faceSelection selects nothing
        # Could check if these vertices are involved with any other layer (internal causes problems if it's turned off)
        if faceSelection:
            cmds.select(faceSelection)
            cmds.polyChipOff(faceSelection, dup=True)

faceIslands = ObjectScatter.separateIntoPlanarElements(meshDuplicate)[1:]

thisSet = cmds.sets(n='Ratio_%i'%i)
for face in faceIslands:
    #cmds.geomToBBox(face, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(surface,i))
    cmds.sets(cmds.geomToBBox(face, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(face,i)), add=thisSet)

# The last item is the name of the polySeparate node, this is not needed so we discard it
#separatedFaces = cmds.polySeparate( meshDuplicate )[:-1]

#duplicatedObj, elements = separatedFaces[0], separatedFaces[1:]
#cmds.delete(duplicatedObj)
cmds.delete(meshDuplicate)

"""
accuracyStep = 0.1
stepTotal = int(1/accuracyStep)

if sum:
        ratios = [ (len(layer)/float(sum)) for layer in layers ]

        newsum = 0
        for x in ratios: newsum += x

        objCount = 150
        density = [0] * stepTotal

        #randomly distribute meshes using ratios of density:amount
        for i in range(0, len(ratios)):
            # To better approximate placement in each area of colour the mesh is broken apart
            # into islands, this destroys the vertex colours and the mesh in general
            # For each shade of colour the original mesh is duplicated and worked on to preserve the original
            meshDuplicate = cmds.duplicate(meshName, rr=True)[0]

            cmds.select(deselect=True)
            density[i] = int(ratios[i] * objCount)
            if len(layers[i]) > 0:
                for vtx in layers[i]: cmds.select('%s.vtx[%i]'%(meshDuplicate,vtx), add=True)

                # Break off the vertex colour islands into separate objects
                faceSelection = cmds.polyListComponentConversion(fv=True, tf=True)
                cmds.polyChipOff(faceSelection, dup=True)

                # The last item is the name of the polySeparate node, this is not needed so we discard it
                separatedFaces = cmds.polySeparate( meshDuplicate )[:-1]
                duplicatedObj, elements = separatedFaces[0], separatedFaces[1:]
                #cmds.delete(duplicatedObj)

                for element in elements:
                    faceIslands = ObjectScatter.separateIntoPlanarElements(element)
                    #for island in faceIslands:
                    #    surface = island
                    #    bbox = cmds.geomToBBox(surface, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(surface,i))
                    #    objects = ObjectScatter.volumeScatter(bbox, density[i])
                    #    ObjectScatter.setPivotToBottom(objects)
                    #    #cmds.delete(bbox)
                    #    ObjectScatter.constrainToSurface(surface, objects)
                    #    ObjectScatter.positionObjects(objects)
            cmds.delete(meshDuplicate)"""
