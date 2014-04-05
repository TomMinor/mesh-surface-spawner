import maya.cmds as cmds

cmds.makeLive()

def setObjectAsCanvas(name):
	cmds.polyEvaluate(f=True)
	liveSurface = cmds.subdToNurbs(cmds.polyToSubdiv(maxPolyCount=cmds.polyEvaluate(f=True), maxEdgesPerVert=32, ch=False)[0], ot=0, ch=False)
	cmds.hide(liveSurface)
	cmds.makeLive(liveSurface)

	return liveSurface
	
liveSurface = setObjectAsCanvas(cmds.ls(sl=True))
cmds.setToolTo('pencilContext')

cmds.makeLive(n=True)

cmds.ls(sl=True, showType=True)
cmds.ls(type='nurbsCurve')

"""
// Nurbs interactive creation
int $val = (!`optionVar -q createNurbsPrimitiveAsTool`);
optionVar -intValue createNurbsPrimitiveAsTool $val;

if ( `menuItem -ex toggleCreateNurbsPrimitivesAsToolItem` )
menuItem -e -cb $val toggleCreateNurbsPrimitivesAsToolItem;

if ( `menuItem -ex toggleNurbsPrimitivesAsToolItemExitOnComplete` )
menuItem -e -enable $val toggleNurbsPrimitivesAsToolItemExitOnComplete;
"""

cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', exists=True)

#Disable UI elements
cmds.menuItem('toggleNurbsPrimitivesAsToolItemExitOnComplete', edit=True, enable=True)
cmds.menuItem('toggleCreateNurbsPrimitivesAsToolItem', edit=True, enable=True)

# Turn on interactive creation for nurbs objects 
# and remember its current value so it can be reverted later
if(!cmds.optionVar(q='createNurbsPrimitiveAsTool')):
	cmds.optionVar(intValue=('createNurbsPrimitiveAsTool', 1))



cmds.setAttr('blinn*.color', 1, 0.524614, 0, type='double3')
