try:
    import maya.cmds as cmds
    #stuff
except:
    pass

attributes = [ 'instancedObject', 'density', 'scale', 'rotation', 'offset' ]
def removeSettings(name):
    """
        Removes instance setting specific attributes if they exist

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

    return settings


class storeInstanceSettings:
    def __init__(self, name, instancedObject, density, scale=(1.0,1.0,1.0), rotation=(0.0,0.0,0.0), offset=(0.0,0.0,0.0)):
        """
            Initialise dynamic attributes that are stored in the instance set (name)
            These will persist in the scene until deleted, even if the scene is saved and reloaded

            name            :   The name of the curve object in the scene to store these attributes in
            instancedObject :   The name of the set object instances are referenced by
            density         :   How much this group of instances contributes to the total instance count, e.g
                                3 instance sets of density 1.0 forming a collection of 90 instances would store 30 instances each
                                4 instance sets of densities (1.0, 1.0, 0.5, 0.25) and 120 instances would store (43,43,22,11) instances respectively

            scale           :   A relative scale to the random scale assigned to the object instances when they were spawned,
                                all objects in the set will be scaled uniformly by this value

            rotation        :   A relative rotation to the random rotation assigned to the object instances when they were spawned,
                                all objects in the set will be rotation uniformly by this value
        """
        self.name = name
        # Instance set settings
        self.setInstancedObject(instancedObject)
        self.setDensity(density)
        self.setScale(scale)
        self.setRotation(rotation)
        self.setOffset(offset)

    def setInstancedObject(self, instancedObject):
        if not cmds.attributeQuery('instancedObject', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='instancedObject', dt='string', hidden=True)

        cmds.setAttr('%s.instancedObject'%(self.name), instancedObject, type='string')

    def setDensity(self, density):
        if cmds.attributeQuery('density', node=self.name, ex=True):
            cmds.setAttr('%s.density'%(self.name), density)
        else:
            cmds.addAttr(self.name, ln ='density', at='double', dv = density, hidden=True)

    def setOffset(self, offset):
        if not cmds.attributeQuery('offset', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='offset', dt='double3', hidden=True)

        cmds.setAttr('%s.offset'%(self.name), *offset, type='double3')

    def setScale(self, scale):
        if not cmds.attributeQuery('scale', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='scale', dt='double3', hidden=True)

        cmds.setAttr('%s.scale'%(self.name), *scale, type='double3')

    def setRotation(self, rotation):
        if not cmds.attributeQuery('rotation', node=self.name, ex=True):
            cmds.addAttr(self.name, ln ='rotation', dt='double3', hidden=True)

        cmds.setAttr('%s.rotation'%(self.name), *rotation, type='double3')