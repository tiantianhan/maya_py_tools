#!/usr/bin/env python

"""
toolUtils.py : A library of common functions used for building other tools

"""

import maya.cmds as cmds

def lockItemsInSpace(items, doLock=True) :
    """
    Lock or unlock the translation, position and rotation of a list of objects
    """
    for item in items :
        cmds.setAttr( item + ".translateX", lock=doLock )
        cmds.setAttr( item + ".translateY", lock=doLock )
        cmds.setAttr( item + ".translateZ", lock=doLock )

        cmds.setAttr( item + ".rotateX", lock=doLock )
        cmds.setAttr( item + ".rotateY", lock=doLock )
        cmds.setAttr( item + ".rotateZ", lock=doLock )

        cmds.setAttr( item + ".scaleX", lock=doLock )
        cmds.setAttr( item + ".scaleY", lock=doLock )
        cmds.setAttr( item + ".scaleZ", lock=doLock )

if __name__ == '__main__':
    print ( "Import this module in other py scripts to build Maya tools.")
