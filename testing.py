import maya.cmds as cmds
import random
#from ObjectScatter import *
import ObjectScatter
reload(ObjectScatter)

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

layers = ObjectScatter.updateColourData(meshName)

sum=0
for layer in layers: sum += len(layer)

"""
Density
Divide the total objects between vtx colours and bbox

- Compromise between bbox size and vertex colour, we want them to be clumped together
more at brighter areas but spaced out in dimmer areas
- But if the user sets a clump of vertices to ~0.9 and theres a set of vertices set to 1.0
in the center, we don't want ~200 objects squashed into that area
- Possibly add back in the cumulative placement, at least then there is some interaction between each layer
"""


accuracyStep = 0.1
stepTotal = int(1/accuracyStep)


ratios = [ (len(layer)/float(sum)) for layer in layers ]

newsum = 0
for x in ratios: newsum += x

objCount = 150
density = [0] * stepTotal

#randomly distribute meshes using ratios of density:amount
for i in range(0, len(ratios)):
	meshDuplicate = cmds.duplicate(meshName, rr=True)[0]
	
	density[i] = int(ratios[i] * objCount)
	
	if layers[i]:
		# Break off the vertex colour islands into separate objects	
		faceSelection = cmds.polyListComponentConversion(['%s.vtx[%i]'%(meshDuplicate,vtx) for vtx in layers[i]], fv=True, tf=True)
	
		if faceSelection:
			cmds.polyChipOff(faceSelection, dup=True)
	    	faceIslands = ObjectScatter.separateIntoPlanarElements(meshDuplicate)
	    	
	    	thisSet = cmds.sets(n='Ratio_%i'%i)
	    	for face in faceIslands:
	    		#cmds.geomToBBox(face, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(surface,i))
	    		cmds.sets(cmds.geomToBBox(face, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(surface,i)), add=thisSet)
	    			    		    	
	    	# The last item is the name of the polySeparate node, this is not needed so we discard it
	    	#separatedFaces = cmds.polySeparate( meshDuplicate )[:-1]
	
	    	#duplicatedObj, elements = separatedFaces[0], separatedFaces[1:]
	    	#cmds.delete(duplicatedObj)


 	#cmds.delete(meshDuplicate)

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
            		#	surface = island
            		#	bbox = cmds.geomToBBox(surface, ko=True,shaderColor=[1,0.5,0.043],n="%s_bbox_%i_#"%(surface,i))
            		#	objects = ObjectScatter.volumeScatter(bbox, density[i])
            		#	ObjectScatter.setPivotToBottom(objects)
            		#	#cmds.delete(bbox)
            		#	ObjectScatter.constrainToSurface(surface, objects)
            		#	ObjectScatter.positionObjects(objects)
            cmds.delete(meshDuplicate)"""
