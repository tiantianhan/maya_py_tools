#!/usr/bin/env python

"""
lockit.py : lock the translation, rotation, scale, and visibility of all selected

Motivation: Useful for reference objects that need to be locked
"""

import maya.cmds as cmds

import toolUtils as utils

selected = cmds.ls( selection=True )

utils.lockItemsInSpace(selected, doLock=True)
