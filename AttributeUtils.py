# Terrain Data [ Tools ]
#	-> PencilCurves [ ToolList ]
#		-> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN
#	-> RadialBound [ ToolList ]
#		-> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN
#	-> SquareBound [ ToolList ]
#		-> Tool Data [ Size(x,y), Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN

# Store placement data in dynamic attributes, these are saved with the appropriate object
# and are stored in the scene file, so they persist between saving/loading


cmds.deleteAttr('pPlane1.Tool_PencilCurves')
# Terrain Data [ Tools ]
addStringArrayAttr('pPlane1', 'Tool_PencilCurves', 	[])
addStringArrayAttr('pPlane1', 'Tool_RadialBound', 	[])
addStringArrayAttr('pPlane1', 'Tool_SquareBound', 	[])

#	-> PencilCurves [ ToolList ]
addStringArrayAttr('pPlane1', 'Tool_PencilCurves', ['curve1'], append=True)
#		-> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
cmds.addAttr('curve1', longName = 'Radius', dv=1.0, h=False)

# Dist
# Gauass
cmds.addAttr('curve1', ln ='distMean', 		at='double', dv = 1.0, h=False, keyable=True)
cmds.addAttr('curve1', ln ='distFalloff', 	at='double', dv = 1.0, h=False, keyable=True)
# or
# Uniform
cmds.addAttr('curve1', ln ='distMin', 	at='double', dv = 1.0, h=False, keyable=True)
cmds.addAttr('curve1', ln ='distMax', 	at='double', dv = 1.0, h=False, keyable=True)

#Scale
addVectorAttr('curve1', 'scaleMin', [0.0, 0.0, 0.0], False)
addVectorAttr('curve1', 'scaleMax', [1.0, 1.0, 1.0], False)
#Rotation
addVectorAttr('curve1', 'rotationMin', [0.0, 0.0, 0.0], False)
addVectorAttr('curve1', 'rotationMax', [0.0, 360.0, 0.0], False)
#Offset
addVectorAttr('curve1', 'offset', [0.0, 0.0, 0.0], False)

addStringAttr('curve1', 'ObjectInstanceSettings', '

instanceSet = 'PencilCurve1_pCube0_instances'

addStringArrayAttr('curve1', 'Tool_PencilCurves', ['curve1'], append=True)
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN
addStringArrayAttr('pPlane1', 'Tool_PencilCurves', ['curve2'], append=True)
#		-> Tool Data [ Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN
#	-> RadialBound [ ToolList ]
#		-> Tool Data [ Radius, Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN
#	-> SquareBound [ ToolList ]
#		-> Tool Data [ Size(x,y), Distribution(Uniform(Min/Max), Gaussian(Mean, Falloff)), Scale(Min/max), Rotation(Min/Max), Offset, TypeData ]
#			-> Type Data [ Density, (Scale, Rotation, Offset)Absolute, ObjectData ]
#				-> Object Data [ instancedObject, instanceList ]
#					-> instanceList
#						- instance0.... instanceN

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

		nodeName		:	Node to query attributes from
		attributeList	:	Attributes to be queried
		skipMissingAttr	:	If False (default), an error message will be printed and an empty list returned
							If True, any missing attribute will be ignored and the respective dictionary
							element will be an empty list
		Return			:	A dictionary where each element of the attributeList is used as a key to access
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

		objectName		: 	Object to add attribute to
		attrName		: 	Name of the string attribute to be added
		values			:	The string value to initialise the attribut eto
		hidden			: 	If this is True, the attribute will not be visible in the UI (True by default)
	"""
	cmds.addAttr(objectName, longName = attrName, dataType="string", h=hidden)
	cmds.setAttr('%s.%s'%(objectName,attrName), value, type="string")

# Make this delete stuff if it exists
def addStringArrayAttr(objectName, attrName, values, append=False, hidden=True):
	"""
		Adds a stringArray attribute to an object and populates it with values

		objectName		: 	Object to add attribute to
		attrName		: 	Name of the stringArray attribute to be added
		values			:	A list of strings to populate the stringArray attribute
		append			: 	Append the values to the stringArray if it exists, if False the array will be replaced
		hidden			: 	If this is True, the attribute will not be visible in the UI (True by default)
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

		objectName		: 	Object to add attribute to
		attrName		: 	Name of the stringArray attribute to modify
		element			: 	Value of the element to remove
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

		objectName		: 	Object to add attribute to
		attrName		: 	Name of the attribute to add
		value			: 	3-tuple containing the value of the vector elements
		hidden			: 	If this is True, the attribute will not be visible in the UI (True by default)
	"""
	cmds.addAttr(objectName, longName = attrName, dataType='double3', h=hidden)
	cmds.setAttr('%s.%s'%(objectName, attrName), value[0], value[1], value[2], type='double3')

