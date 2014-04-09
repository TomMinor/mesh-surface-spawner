# Terrain Data [ Tools ]
#    -> PencilCurves [ ToolList ]
#        -> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN
#    -> RadialBound [ ToolList ]
#        -> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN
#    -> SquareBound [ ToolList ]
#        -> Tool Data [ Size(x,y), Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN

# Store placement data in dynamic attributes, these are saved with the appropriate object
# and are stored in the scene file, so they persist between saving/loading

import maya.cmds as cmds

# Storing attributes
removeSettings('curve1')
storeToolSettings( 'curve1', 'PencilCurve1_pCube0_instances')
a = getSettings('curve1')

#TODO : Add more error checking to getSettings

attributes = [ 'radius', 'scaleMax', 'scaleMin', 'rotationMax', 'rotationMin',
                'instanceSets', 'distMin', 'distMax', 'distMean', 'distFalloff' ]
def removeSettings(name):
    """
        Removes freeform tool setting specific attributes if they exist

        name    :    The object name to attempt to remove the attributes from
    """
    for attribute in attributes:
        if cmds.attributeQuery(attribute, node=name, ex=True):
            cmds.deleteAttr('%s.%s'%(name,attribute))

def getSettings(name):
    settings = {}
    for attribute in attributes:
        if cmds.attributeQuery(attribute, node=name, ex=True):
            settings[attribute] = cmds.getAttr('%s.%s'%(name, attribute))

    # If for some reason the object contains data for both uniform & gaussian,
    # give gaussian priority
    if 'distMean' in settings.values() and 'distFalloff' in settings.values():
        del settings['distMin']
        del settings['distMax']

    # Return an empty list of the proper distribution type isn't clear
    if ('distMean' in settings.values() and 'distMin' in settings.values()) or \
    ('distFalloff' in settings.values() and 'distMax' in settings.values()):
        print "Ambiguous distribution types"
        return []

    return settings

class storeToolSettings:
    def __init__(self, name, instanceSets, radius=1.0, distribution = ('gauss', 0.0, 1.0), scale=[(0.0,0.0,0.0), (1.0,1.0,1.0)], rotation=[(0.0,0.0,0.0), (360.0,360.0,360.0)]):
        """
            Initialise dynamic attributes that are stored in the tool curve (name)
            These will persist in the scene until deleted, even if the scene is saved and reloaded

            name            :    The name of the curve object in the scene to store these attributes in
            instanceSets    :    The names of the sets referencing the various object instances
            radius          :    The radius of the tool, used for spawning objects along the freeform curve
            distribution    :    Random distribution type when spawning objects, currently supports "uniform" and "gauss" types
                                Possible types:
                                    ("uniform", min, max)
                                    ("gauss", mean, falloff)
            scale           :    The minimum and maximum scale vectors, in the form [(minx,miny,minz), (maxx,maxy,maxz)]
            rotation        :    The minimum and maximum rotation vectors, in the form [(minx,miny,minz), (maxx,maxy,maxz)]
        """
        self.name = name

        # Currently 2 supported types of random placement
        if(distribution[0] == 'gauss'):
            meanVal, falloffVal = distribution[1], distribution[2]
            self.setGaussian(meanVal, falloffVal)
        elif(distribution[0] == 'uniform'):
            minVal, maxVal = distribution[1], distribution[2]
            self.setUniform(minVal, maxVal)
        else:
            raise ValueError('Unexpected distribution type %s'%(distribution[0]))

        # Tool settings
        self.setRadius(radius)

        self.setScaleMin(scale[0])
        self.setScaleMax(scale[1])

        self.setRotationMin(rotation[0])
        self.setRotationMax(rotation[1])

        # Name of the set whose members are the instances made using this freeform tool
        self.setInstanceSet(instanceSets)

    def setRadius(self, radius):
        if cmds.attributeQuery('radius', node=self.name, ex=True):
            cmds.setAttr('%s.radius'%(self.name), radius)
        else:
            cmds.addAttr(self.name, ln ='radius', at='double', dv = radius, hidden=True)

    def setScaleMax(self, maximum):
        if not cmds.attributeQuery('scaleMax', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='scaleMax', dt='double3', hidden=True)

        cmds.setAttr('%s.scaleMax'%(self.name), *maximum, type='double3')

    def setScaleMin(self, minimum):
        if not (cmds.attributeQuery('scaleMin', node=self.name, ex=True)):
            cmds.addAttr(self.name, ln ='scaleMin', dt='double3', hidden=True)

        cmds.setAttr('%s.scaleMin'%(self.name), *minimum, type='double3')

    def setRotationMax(self, maximum):
        if not cmds.attributeQuery('rotationMin', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='rotationMin', dt='double3', hidden=True)

        cmds.setAttr('%s.rotationMin'%(self.name), *maximum, type='double3')

    def setRotationMin(self, minimum):
        if not cmds.attributeQuery('rotationMax', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='rotationMax', dt='double3', hidden=True)

        cmds.setAttr('%s.rotationMax'%(self.name), *minimum, type='double3')

    def setInstanceSet(self, instances):
        if not cmds.attributeQuery('instanceSets', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='instanceSets', dt='stringArray', hidden=True)

        cmds.setAttr('%s.instanceSets'%(self.name), len(instances), type='stringArray', *instances)

    def setGaussian(self, mean, falloff):
        # Remove uniform data
        if cmds.attributeQuery('distMin', node=self.name, ex=True): cmds.deleteAttr('%s.distMin'%self.name)
        if cmds.attributeQuery('distMax', node=self.name, ex=True): cmds.deleteAttr('%s.distMax'%self.name)

        if cmds.attributeQuery('distMean', node=self.name, ex=True):
            cmds.setAttr('%s.distMean'%(self.name), mean)
        else:
            cmds.addAttr(self.name, ln ='distMean', dv = mean, hidden=True)

        if cmds.attributeQuery('distFalloff', node=self.name, ex=True):
            cmds.setAttr('%s.distFalloff'%(self.name), falloff)
        else:
            cmds.addAttr(self.name, ln ='distFalloff', dv = falloff, hidden=True)

    def setUniform(self, minimum, maximum):
        # Remove gauss data
        if cmds.attributeQuery('distMean',    node=self.name, ex=True): cmds.deleteAttr('%s.distMean'%self.name)
        if cmds.attributeQuery('distFalloff', node=self.name, ex=True): cmds.deleteAttr('%s.distFalloff'%self.name)

        if cmds.attributeQuery('distMin', node=self.name, ex=True):
            cmds.setAttr('%s.distMin'%(self.name), minimum)
        else:
            cmds.addAttr(self.name, ln ='distMin', dv = minimum, hidden=True)

        if cmds.attributeQuery('distMax', node=self.name, ex=True):
            cmds.setAttr('%s.distMax'%(self.name), maximum)
        else:
            cmds.addAttr(self.name, ln ='distMax', dv = maximum, hidden=True)


# Instance specific data (transforms added to random rotations provided by tool settings)
instanceSet = 'PencilCurve1_pCube0_instances'

cmds.addAttr(instanceSet, ln ='density', at='double', dv = 1.0, minValue=0.0, maxValue=1.0, h=False)
#Offset
addVectorAttr(instanceSet, 'objOffset', [0.0, 0.0, 0.0], False)
#Rotation
addVectorAttr(instanceSet, 'objScale', [0.0, 0.0, 0.0], False)
#Scale
addVectorAttr(instanceSet, 'objRot', [1.0, 1.0, 1.0], False)

#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN
addStringArrayAttr('pPlane1', 'Tool_PencilCurves', ['curve2'], append=True)
#        -> Tool Data [ Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN
#    -> RadialBound [ ToolList ]
#        -> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN
#    -> SquareBound [ ToolList ]
#        -> Tool Data [ Size(x,y), Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#            -> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#                -> Object Data [ instancedObject, instanceList ]
#                    -> instanceList
#                        - instance0.... instanceN

cmds.sets('cones', q=True)
#Scale
addVectorAttr('cones', 'meshPaint_Scale', (1.0, 1.0, 1.0), False)
#Rotation
addVectorAttr('cones', 'meshPaint_Rotation', (0.0, 0.0, 2.0), False)
#Offset
addVectorAttr('cones', 'meshPaint_Offset', (0.0, 0.0, 0.0), False)
#Load
queryAttributes('cones', ['meshPaint_Scale', 'meshPaint_Rotation', 'meshPaint_Offset'])

cmds.sets('cubes', q=True)
#Scale
addVectorAttr('cubes', 'meshPaint_Scale', (1.0, 1.0, 1.0), False)
#Rotation
addVectorAttr('cubes', 'meshPaint_Rotation', (0.0, 0.0, 2.0), False)
#Offset
addVectorAttr('cubes', 'meshPaint_Offset', (0.0, 0.0, 0.0), False)
#Load
queryAttributes('cubes', ['meshPaint_Scale', 'meshPaint_Rotation', 'meshPaint_Offset'])

addStringArrayAttr('pPlane1', 'meshPaint_Tools', ['curve1'])
queryAttributes('pPlane1', ['meshPaint_Tools'])

def queryAttributes(nodeName, attributeList, skipMissingAttr=False):
    """
        Queries the passed node for every attribute in the attribute list

        nodeName        :    Node to query attributes from
        attributeList    :    Attributes to be queried
        skipMissingAttr    :    If False (default), an error message will be printed and an empty list returned
                            If True, any missing attribute will be ignored and the respective dictionary
                            element will be an empty list
        Return            :    A dictionary where each element of the attributeList is used as a key to access
                            the queried attributes
    """
    queriedAttributes = dict((attribute, []) for attribute in attributeList)
    for attribute in queriedAttributes:
        if cmds.attributeQuery(attribute, node=nodeName, exists=True):
            queriedAttributes[attribute] = (cmds.getAttr('%s.%s'%(nodeName, attribute)))
        else:
            if(not skipMissingAttr):
                print "Attribute %s not found in node %s"%(attribute, nodeName)
                return []
    return queriedAttributes

def addStringAttr(objectName, attrName, value, hidden=True):
    """
        Adds a string attribute to an object and assigns a value to it

        objectName        :     Object to add attribute to
        attrName        :     Name of the string attribute to be added
        values            :    The string value to initialise the attribut eto
        hidden            :     If this is True, the attribute will not be visible in the UI (True by default)
    """
    cmds.addAttr(objectName, longName = attrName, dataType="string", h=hidden)
    cmds.setAttr('%s.%s'%(objectName,attrName), value, type="string")

# Make this delete stuff if it exists
def addStringArrayAttr(objectName, attrName, values, append=False, hidden=True):
    """
        Adds a stringArray attribute to an object and populates it with values

        objectName        :     Object to add attribute to
        attrName        :     Name of the stringArray attribute to be added
        values            :    A list of strings to populate the stringArray attribute
        append            :     Append the values to the stringArray if it exists, if False the array will be replaced
        hidden            :     If this is True, the attribute will not be visible in the UI (True by default)
    """
    if append and cmds.attributeQuery(attrName, node=objectName, exists=True):
        newArray = cmds.getAttr('%s.%s'%(objectName, attrName)) + values
        cmds.setAttr('%s.%s'%(objectName, attrName), len(values), type="stringArray", *newArray)
    else:
        cmds.addAttr(objectName, longName = attrName, dataType="stringArray")
        cmds.setAttr('%s.%s'%(objectName, attrName), len(values), type="stringArray", *values)

def deleteStringArrayElement(objectName, attrName, element):
    """
        Removes an element from an stringArray attribute

        objectName        :     Object to add attribute to
        attrName        :     Name of the stringArray attribute to modify
        element            :     Value of the element to remove
    """
    strings = cmds.getAttr('%s.%s'%(objectName, attrName))
    if element not in strings:
        print "Element not found in string array"
        return
    strings.remove(element)
    cmds.setAttr('%s.%s'%(objectName, attrName), len(strings), type="stringArray", *strings)

def addVectorAttr(objectName, attrName, value=(0.0,0.0,0.0), hidden=True):
    """
        Adds a new attribute to an object that represents a (double) vector with 3 elements

        objectName        :     Object to add attribute to
        attrName        :     Name of the attribute to add
        value            :     3-tuple containing the value of the vector elements
        hidden            :     If this is True, the attribute will not be visible in the UI (True by default)
    """
    cmds.addAttr(objectName, longName = attrName, dataType='double3', h=hidden)
    cmds.setAttr('%s.%s'%(objectName, attrName), value[0], value[1], value[2], type='double3')

