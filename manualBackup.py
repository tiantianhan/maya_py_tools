#!/usr/bin/env python

"""
manualBackup.py : manually make a backup

Motivation: incremental save creates too many files with trivial changes.
Where manual backup is preferred, this script makes it easier to create and save a backup
copy of the current scene
"""

import maya.cmds as cmds

saveDir = cmds.fileDialog2(ff="*.mb", dialogStyle=1)[0]
thisDir = cmds.file(q=True, expandName=True)
print ("Saving backup to " + saveDir)

cmds.file(rn=saveDir)
cmds.file(save=True)
cmds.file(rn=thisDir)

print ("Done.")
