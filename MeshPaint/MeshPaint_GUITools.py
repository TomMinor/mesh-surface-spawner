class freeformCurveTool:
	"""
		Constructor
	"""
	def __init__(self, updateStep=1.0, name='freeformCurve'):
		self.updateStep = updateStep
		self.beingDrawn = True
		self.lastPos = (0,0,0)
		self.currentCurve = None
		self.ctxName = cmds.draggerContext( '%s.ctx'%name,	pressCommand=__self.onClick, 
															dragCommand=__self.onDrag, 
															releaseCommand=__self.onRelease,
															cursor='crossHair' )
	def curveDrawn(self):
		"""
			Return the status of whether the curve is currently being drawn or not
			
			Returns	:	True if the curve has finished drawing, False if it is being drawn
		"""
		return self.beingDrawn

	def setAsCurrentTool(self):
		"""
			Set the current tool context to be this tool
		"""
		cmds.setToolTo(self.ctxName)
	
	def __onClick(self):
		"""
			Called on mouse click
			
			Initiates state to being drawn and sets the initial point on the curve
			to the mouse position
		"""
		cmds.refresh()
		self.beingDrawn = True
		clickPos = cmds.autoPlace(um=True)
		self.currentCurve = cmds.curve(p=clickPos)
		self.lastPos = (0,0,0)
	
	def __onDrag(self):
		"""
			Called on mouse drag
			
			Adds a new point to the curve when a certain distance (updateStep) is surpassed
		"""
		distance = lambda a,b : math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
		clickPos = cmds.autoPlace(um=True)
		
		if distance(self.lastPos,clickPos) > self.updateStep:
			cmds.curve(self.currentCurve, append=True, p=clickPos)
			self.lastPos = clickPos
			cmds.refresh()
		
	def __onRelease(self):
		"""
			Called on mouse release
			
			Finalizes curve and sets the state to drawn
		"""
		self.beingDrawn = False
		cmds.refresh()
		clickPos = cmds.autoPlace(um=True)
		cmds.curve(self.currentCurve, p=clickPos, append=True)
