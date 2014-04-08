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

def addStringArrayAttr(objectName, attrName, values, hidden=True):
	"""
		Adds a stringArray attribute to an object and populates it with values
		
		objectName		: 	Object to add attribute to
		attrName		: 	Name of the stringArray attribute to be added
		values			:	A list of strings to populate the stringArray attribute
		hidden			: 	If this is True, the attribute will not be visible in the UI (True by default)
	"""
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
	cmds.addAttr(objectName, longName = attrName, attributeType='double3')
	cmds.addAttr(objectName, ln ='%sX'%(attrName), p=attrName, at='double', dv=value[0], h=hidden)
	cmds.addAttr(objectName, ln ='%sY'%(attrName), p=attrName, at='double', dv=value[1], h=hidden)
	cmds.addAttr(objectName, ln ='%sZ'%(attrName), p=attrName, at='double', dv=value[2], h=hidden)