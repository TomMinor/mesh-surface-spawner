import sys 
sys.path.append('/usr/lib64/python2.6/site-packages')
import numpy

window = cmds.window(title='Mesh Painter', widthHeight=(200, 100))
cmds.columnLayout(adjustableColumn=True)

cmds.inViewMessage( amg='''
%s is <hl>penis</hl>.
%s is <hl>penis</hl>. 
<h5>8=====D</h5>'
'''%('idy', 'idy'), pos='topLeft', fade=True )

# Grab screen mouse position
cmds.pause(sec=3)
for i in range(100):
	position = cmds.autoPlace(um=True)
	cmds.polyCube()
	cmds.move( position[0], position[1], position[2], relative=True )
	
# Enum dropdown
cmds.window()
cmds.columnLayout()
cmds.attrEnumOptionMenuGrp( l='Output Format',
                            at='defaultRenderGlobals.imageFormat',
                            ei=[(0, 'GIF'),(1, 'SoftImage'), (2, 'RLA'),
                                (3, 'TIFF'), (4, 'TIFF16'), (5, 'SGI'),
                                (6, 'Alias PIX'), (7, 'Maya IFF'), (8, 'JPEG'),
                                (9, 'EPS'), (10, 'Maya16 IFF'), (11, 'Cineon'),
                                (12, 'Quantel'), (13, 'SGI16'), (19, 'Targa'),
                                (20, 'BMP') ] )
cmds.showWindow()

# Menu
cmds.window( menuBar=True )
cmds.menu( label='Position' )
cmds.radioMenuItemCollection()
cmds.menuItem( label='Top', radioButton=False )
cmds.menuItem( label='Middle', radioButton=False )
cmds.menuItem( label='Bottom', radioButton=True )
cmds.menu( label='Number' )
cmds.radioMenuItemCollection()
cmds.menuItem( label='One', radioButton=True )
cmds.menuItem( label='Two', radioButton=False )
cmds.menuItem( label='Three', radioButton=False )
cmds.showWindow()

# Checkbox
cmds.window()
cmds.columnLayout()
cmds.button()
cmds.popupMenu()
cmds.menuItem()
cmds.menuItem()
cmds.menuItem()
cmds.text()
cmds.popupMenu( button=1 )
cmds.menuItem()
cmds.menuItem()
cmds.menuItem()
cmds.checkBox( 'aCheckBox' )
cmds.popupMenu( parent='aCheckBox', alt=True, ctl=True )
cmds.menuItem()
cmds.menuItem()
cmds.menuItem()
cmds.showWindow()

# Tabs
cmds.window( widthHeight=(200, 150) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=2)
cmds.button()
cmds.button()
cmds.button()
cmds.setParent( '..' )

child2 = cmds.rowColumnLayout(numberOfColumns=2)
cmds.button()
cmds.button()
cmds.button()
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'One'), (child2, 'Two')) )

cmds.showWindow()


# Shelf tabs (buttons can be removed)
cmds.window()
cmds.shelfTabLayout( 'mainShelfTab', image='smallTrash.png', imageVisible=True )
cmds.shelfLayout( 'Dynamics' )
cmds.setParent( '..' )
cmds.shelfLayout( 'Rendering' )
cmds.setParent( '..' )
cmds.shelfLayout( 'Animation' )
cmds.setParent( '..' )
cmds.showWindow()

# Scroll & sliders
cmds.window( widthHeight=(350, 150) )
scrollLayout = cmds.scrollLayout(
	horizontalScrollBarThickness=16,
	verticalScrollBarThickness=16)
cmds.rowColumnLayout( numberOfColumns=3 )

for index in range(10):
	cmds.text()
	cmds.intField()
	cmds.intSlider()

cmds.showWindow()

value = cmds.scrollLayout(scrollLayout, query=True, scrollAreaValue=True)
top = value[0]
left = value[1]


# ===Row/Column===
#    The following script will position the buttons in 3 columns, each
#    column a different width.
#
#    +----++--------++------------+
#    | b1 ||   b2   ||     b3     |
#    +----++--------++------------+
#    +----++--------++------------+
#    | b4 ||   b5   ||     b6     |
#    +----++--------++------------+
#    +----+
#    | b7 |
#    +----+
#
cmds.window()
cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 60), (2, 80), (3, 100)] )
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.showWindow()

#    The following script will position the buttons in 2 rows, each
#    row a different height.
#
#    +----++----++----++----+
#    | b1 || b3 || b5 || b7 |
#    +----++----++----++----+
#    +----++----++----+
#    |    ||    ||    |
#    | b2 || b4 || b6 |
#    |    ||    ||    |
#    +----++----++----+
#
cmds.window()
cmds.rowColumnLayout( numberOfRows=2, rowHeight=[(1, 30), (2, 60)] )
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.button()
cmds.showWindow()

# Panel layout0
cmds.window()
cmds.paneLayout( configuration='quad' )
cmds.button()
cmds.textScrollList( append=['one', 'two', 'three'] )
cmds.scrollField()
cmds.scrollLayout()
cmds.columnLayout()
cmds.button()
cmds.button()
cmds.button()
cmds.showWindow()
