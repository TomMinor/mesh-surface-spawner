import maya.cmds as cmds
import random

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

def separateIntoPlanarElements(name):
    # Use the automatic UV tool to do the heavy lifting in breaking up the 3d mesh for us
    cmds.polyAutoProjection('%s.f[0:%i]' % (name, cmds.polyEvaluate(name, f=True)), o=1, p=12)
    shells = getUVShells(name)
    for shell in shells: cmds.polyChipOff(shell)
    elements = cmds.polySeparate( name )[:-1]
    cmds.delete(elements[0])    # Delete the duplicate mesh
    return elements[1:]

def initMesh(name):
        cmds.polyColorSet(name, colorSet="meshDensitySet_#", clamped=1, rpt='RGB')
        cmds.polyColorPerVertex(name, r = 0.0, g = 0.0, b = 0.0)

def updateColourData(name):
        itervtx = ['%s.vtx[%i]'%(name,i) for i in xrange(cmds.polyEvaluate(name, v=True)) ]
        vertCol = [cmds.polyColorPerVertex(v, query=True, rgb=True) for v in itervtx ]

        accuracyStep = 0.1
        stepTotal = int(1/accuracyStep)
        layers = [ [] for i in xrange(0, stepTotal) ]

        for vtx, col in enumerate(vertCol):
            for i in xrange(len(layers)):
                minColour = [i*accuracyStep, i*accuracyStep, i*accuracyStep]
                maxColour = [(i+1)*accuracyStep, (i+1)*accuracyStep, (i+1)*accuracyStep]
                if (minColour < col <= maxColour):
                        layers[i].append(vtx)

        return layers

def positionObjects(objects):
        # We're only checking a subset of objects against themselves which is fairly nice
        # if we have lots of islands
        for obj in objects:
                bbox = cmds.exactWorldBoundingBox(obj)
                #print bbox
