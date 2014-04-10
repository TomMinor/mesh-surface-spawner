import FreeformAttributes
import InstanceAttributes

FreeformAttributes.removeSettings('curve1')

# This would be sorted out when the tool is made
FreeformTools =  [ FreeformAttributes.storeToolSettings( 'curve1', ['set1', 'set2', 'set3']) ]
instances = [     InstanceAttributes.storeInstanceSettings( 'set1', 'pCone1', 1.0),
                InstanceAttributes.storeInstanceSettings( 'set2', 'pSphere1', 0.75),
                InstanceAttributes.storeInstanceSettings( 'set3', 'pCube1', 1.0)    ]

# Perhaps add a dynamic attr to determine the tool type, e.g 'curve1.meshPaint_Tool' = 'freeform'
tools = ['curve1']
cmds.addAttr('curve1', longName = 'meshPaint_Tool', dt='string')
cmds.setAttr('curve1.meshPaint_Tool', 'freeform', type='string')

cmds.addAttr('curve2', longName = 'meshPaint_Tool', dt='string')
cmds.setAttr('curve2.meshPaint_Tool', 'freeform', type='string')

freeformTools = []
for curve in cmds.listRelatives(cmds.ls(type='nurbsCurve'), p=True):
    if cmds.attributeQuery('meshPaint_Tool', node=curve, ex=True) and \
    cmds.getAttr('%s.meshPaint_Tool'%(curve)) == 'freeform':
        freeformTools.append(curve)

window = cmds.window()
layout = cmds.formLayout()
control = cmds.treeView( parent = layout, numberOfButtons = 1, abr = True, arp=False )

cmds.formLayout(layout,e=True, attachForm=(control,'top', 2))
cmds.formLayout(layout,e=True, attachForm=(control,'left', 2))
cmds.formLayout(layout,e=True, attachForm=(control,'bottom', 2))
cmds.formLayout(layout,e=True, attachForm=(control,'right', 2))
cmds.showWindow( window )

# Focus on allowing 1 active live object first
cmds.treeView( control, e=True, addItem = ("terrain", ""))

for tool in freeformTools:
    cmds.treeView( control, e=True, addItem = (tool, "terrain"))

cmds.treeView( control, e=True, buttonTooltip=('terrain', 1, 'Example tooltip') )

cmds.treeView(control,edit=True, pressCommand=[(1,pressTreeCallBack)])
cmds.treeView(control,edit=True, selectCommand=selectTreeCallBack)
cmds.treeView(control,edit=True, itemRenamedCommand=renameTreeCallback)

a=[]
for instance in toolAttr['instanceSets']:
    a.append(InstanceAttributes.getSettings(instance))

for dict in a:
    print dict

selectedTreeNode = "terrain"
def selectTreeCallBack(*args):
    global selectedTreeNode
     cmds.treeView( control, e=True, bh = [selectedTreeNode, False])
    selectedTreeNode = args[0]
    cmds.treeView( control, e=True, bh = [selectedTreeNode, True])
    #cmds.treeView( control, e=True, ornament = (args[0], 1, 0, 4,))
    print 'selection %s' % (args[0])

def renameTreeCallback(oldname, newname):
    cmds.rename(oldname, newname)
    if selectedTreeNode == oldname:
        global selectedTreeNode
        selectedTreeNode = newname

def pressTreeCallBack(item, state):
    print "pressed"
    print item,
    print state