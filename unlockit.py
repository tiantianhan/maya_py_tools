#!/usr/bin/env python

"""
unlockit.py : unlock the translation, rotation, scale, and visibility of all selected

Motivation: Useful for adjusting locked reference objects
"""

import maya.cmds as cmds

import toolUtils as utils

selected = cmds.ls( selection=True )

utils.lockItemsInSpace(selected, doLock=False)
    