import maya.cmds as cmds

# Parse a curve
for i in range(1,100):
	cmds.spaceLocator(p=cmds.pointOnCurve(newCurve, pr=1.0/100.0 * i, top=True, p=True ))
	cmds.xform(cp=True)
	cmds.xform(ro=cmds.pointOnCurve(newCurve, pr=1.0/100.0 * i, top=True, t=True))

#ToFix : Tweak scriptjob to be killed in different scenarios (onScene etc)
class MeshPaintGUI:
	def __init__(self):
		self.curvePaths = []
		self.squareBounds = []
		self.radialBounds = []
		# Initialize object creation job to invalid job ID so 
		# an actual job ID is not accidently killed 
		exists=self.newObjectJob = -1

	def newItemJob(self):
		# Reset the object creation handling job 
		if(cmds.scriptJob(exists=self.newObjectJob)):
			cmds.scriptJob(kill=self.newObjectJob)
		self.newObjectJob = cmds.scriptJob(event=('DagObjectCreated', self.onNewObject))
		# Store the current tool so we can change back to it when the user has finished painting
		self.currentContext = cmds.currentCtx()

	def paintPencilCurve(self):
		self.newItemJob()
		self.objectList = self.curvePaths
		cmds.PencilCurveTool()

	def paintSquareBound(self):
		self.newItemJob()
		self.objectList = self.squareBounds
		cmds.setToolTo("CreateNurbsSquareCtx")

	def paintRadialBound(self):
		self.newItemJob()
		self.objectList = self.radialBounds
		cmds.setToolTo("CreateNurbsCircleCtx")

	def onNewObject(self):
		#Reset the user's tool to it's previous context
		cmds.setToolTo(self.currentContext)
		#Remove the job waiting for new scene objects
		cmds.scriptJob(kill=self.newObjectJob)

		#Grab the newest created item
		newObject = cmds.ls()[-1]

		# Only process valid objects (curves) -
		# Invalid types shouldn't be a problem since the class paint commands will
		# start the job immediately before the user makes an object, but another script
		# could create objects while the user is painting so this check will
		# prevent non-curve objects from being added
		if(cmds.objectType(newObject) == 'nurbsCurve'):
			self.objectList.append(newObject)
		else:
			print "Attempted to add invalid object type to mesh of type %s" % cmds.objectType(newObject)

	def debugPrintLists(self):
		print "Curves",
		print self.curvePaths
		print "Squares",
		print self.squareBounds
		print "Circles",
		print self.radialBounds

test = MeshPaintGUI()
test.paintPencilCurve()
test.paintSquareBound()
test.paintRadialBound()

test.debugPrintLists()

def setObjectAsCanvas(name):
	cmds.polyEvaluate(f=True)
	subdivSurface = cmds.polyToSubdiv(maxPolyCount=cmds.polyEvaluate(f=True), maxEdgesPerVert=32, ch=False)[0]
	liveSurface = cmds.subdToNurbs(subdivSurface, ot=0, ch=False)
	cmds.delete(subdivSurface)
	cmds.hide(liveSurface)
	cmds.makeLive(liveSurface)

	return liveSurface

liveSurface = setObjectAsCanvas(cmds.ls(sl=True))


cmds.makeLive(n=True)


# This is not needed anymore
# def isInteractiveMode():
# 	""" Returns a boolean of whether the user has enabled interactive mode in the NURBS primitive menu
# 	"""
# 	return bool(cmds.optionVar(q='createNurbsPrimitiveAsTool'))
# 	#cmds.optionVar(iv=('createNurbsPrimitiveAsTool', val))
#
# def setInteractiveMode(state):
# 	"""
# 		Enable or disable interactive mode for NURBS primitives
#
# 		state	: [bool] True enables interactive mode, False disables it
# 	"""
# 	if (cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', ex=True)):
# 		cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', e=True, cb=state )
# 		cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', enable=state, e=True)
#
# 	if (cmds.menuItem('toggleNurbsPrimitivesAsToolItemExitOnComplete', ex=True)):
# 		cmds.menuItem('toggleNurbsPrimitivesAsToolItemExitOnComplete', enable=state, e=True)

#Disable UI elements

# def enablePainting():
# 	# Turn on interactive creation for nurbs objects
# 	# and remember its current value so it can be reverted later
# 	interactiveModeEnabled = cmds.optionVar(q='createNurbsPrimitiveAsTool')
# 	if(not interactiveModeEnabled):
# 		cmds.optionVar(iv=('createNurbsPrimitiveAsTool', 1))
# 		cmds.menuItem('toggleNurbsPrimitivesAsToolItemExitOnComplete', edit=True, enable=False)
# 		cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', edit=True, enable=False)
#
# 	cmds.PencilCurveTool()
# 	while(cmds.currentCtx() == 'pencilContext'):
# 		cmds.refresh()
#
#
# 	cmds.optionVar(intValue=('createNurbsPrimitiveAsTool', interactiveModeEnabled))
# 	cmds.menuItem('toggleNurbsPrimitivesAsToolItemExitOnComplete', edit=True, enable=True)
# 	cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', edit=True, enable=True)
#
# cmds.setAttr('blinn*.color', 1, 0.524614, 0, type='double3')
