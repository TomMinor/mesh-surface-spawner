class MeshPaintGUI:
	def __init__(self):
		self.tools = MeshPaintTools
		self.curvePaths = []
		self.squareBounds = []
		self.radialBounds = []
		

	def debugPrintLists(self):
		print "Curves",
		print self.curvePaths
		print "Squares",
		print self.squareBounds
		print "Circles",
		print self.radialBounds
		
class MeshPaintTools:
		def __init__(self):
			# Initialize object creation job to invalid job ID so 
			# an actual job ID is not accidently killed 
			exists=self.newObjectJob = -1
	
		def placeInstance(self, object):
			lastContext = cmds.currentCtx()
			cmds.setToolTo('selectSuperContext')
			
			objInstance = cmds.instance(object)[0]
			while cmds.currentCtx() == 'selectSuperContext':
				pos = cmds.autoPlace(um=True)
				cmds.xform(objInstance, t=pos)
				cmds.refresh()
			cmds.setToolTo(lastContext)
	
		def pencilCurve(self, object, placementList):
			self.newItemJob()
			self.objectList = self.curvePaths
			cmds.PencilCurveTool()

		def squareBound(self, object):
			self.newItemJob()
			self.objectList = self.squareBounds
			cmds.setToolTo("CreateNurbsSquareCtx")
	
		def radialBound(self, object):
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
