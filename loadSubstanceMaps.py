#!/usr/bin/env python

"""
loadSubstanceMaps.py: make Substance Painter png maps into aiStandardSurface.
Expects folder structure:
    myMaterial/
        xx_BaseColor.png
        xx_Metalness.png
        xx_Normal.png
        xx_Roughness.png
        IgnoresOtherStuff.xx

Creates aiStandardSurface named myMaterial_mat with provided BaseColor, Metalness, Normal and Roughness.
Reference: https://catluo.com/coding
"""

import maya.cmds as cmds
import os

#Suffixes
BASE_COLOR = "_BaseColor"
ROUGHNESS = "_Roughness"
METALNESS = "_Metalness"
NORMAL = "_Normal"

def getPath(folderName, fileName):
    return os.path.join(folderName, fileName) #TODO use relative file paths?

def getRelativePath(folderName, fileName):
    sceneDir = os.path.dirname(cmds.file(q=True, expandName=True))
    absDir = os.path.join(folderName, fileName)

    return os.path.relpath(absDir, start = sceneDir)

def createTextureFileNode(baseName):
    #Create file and place2dTexture nodes
    tex = cmds.shadingNode('file', name=baseName, asTexture=True, isColorManaged=True)
    p2d = cmds.shadingNode('place2dTexture', name=baseName+'p2dTexture', asUtility=True)

    #Connect attributes
    cmds.connectAttr(p2d + '.outUV', tex + '.uvCoord')
    cmds.connectAttr(p2d + '.outUvFilterSize', tex + '.uvFilterSize')
    cmds.connectAttr(p2d + '.vertexCameraOne', tex + '.vertexCameraOne')
    cmds.connectAttr(p2d + '.vertexUvOne', tex + '.vertexUvOne')
    cmds.connectAttr(p2d + '.vertexUvThree', tex + '.vertexUvThree')
    cmds.connectAttr(p2d + '.vertexUvTwo', tex + '.vertexUvTwo')
    cmds.connectAttr(p2d + '.coverage', tex + '.coverage')
    cmds.connectAttr(p2d + '.mirrorU', tex + '.mirrorU')
    cmds.connectAttr(p2d + '.mirrorV', tex + '.mirrorV')
    cmds.connectAttr(p2d + '.noiseUV', tex + '.noiseUV')
    cmds.connectAttr(p2d + '.offset', tex + '.offset')
    cmds.connectAttr(p2d + '.repeatUV', tex + '.repeatUV')
    cmds.connectAttr(p2d + '.rotateFrame', tex + '.rotateFrame')
    cmds.connectAttr(p2d + '.rotateUV', tex + '.rotateUV')
    cmds.connectAttr(p2d + '.stagger', tex + '.stagger')
    cmds.connectAttr(p2d + '.translateFrame', tex + '.translateFrame')
    cmds.connectAttr(p2d + '.wrapU', tex + '.wrapU')
    cmds.connectAttr(p2d + '.wrapV', tex + '.wrapV')

    #Return the file node
    return tex


def createBaseColorNode(folderName, fileName, material):
    tex = createTextureFileNode(fileName)
    cmds.setAttr(tex + '.fileTextureName', getPath(folderName, fileName), type='string')
    cmds.setAttr(tex + '.colorSpace', 'sRGB', type='string')

    cmds.connectAttr(tex + '.outColor', material + '.baseColor')

    return

def createMetalnessNode(folderName, fileName, material):
    tex = createTextureFileNode(fileName)
    cmds.setAttr(tex + '.fileTextureName', getPath(folderName, fileName), type='string')
    cmds.setAttr(tex + '.colorSpace', 'Raw', type='string')

    cmds.connectAttr(tex + '.outColorR', material + '.metalness')

    return

def createRoughnessNode(folderName, fileName, material):
    tex = createTextureFileNode(fileName)
    cmds.setAttr(tex + '.fileTextureName', getPath(folderName, fileName), type='string')
    cmds.setAttr(tex + '.colorSpace', 'Raw', type='string')

    cmds.connectAttr(tex + '.outColorR', material + '.specularRoughness')

    return

def createNormalNode(folderName, fileName, material):
    tex = createTextureFileNode(fileName)
    cmds.setAttr(tex + '.fileTextureName', getPath(folderName, fileName), type='string')
    cmds.setAttr(tex + '.colorSpace', 'Raw', type='string')

    #Create aiNormalMap node
    norm = cmds.shadingNode('aiNormalMap', name=fileName+'_aiNormalMap', asUtility=True)

    cmds.connectAttr(tex + '.outColorR', norm + '.inputX')
    cmds.connectAttr(tex + '.outColorG', norm + '.inputY')
    cmds.connectAttr(tex + '.outColorB', norm + '.inputZ')

    cmds.connectAttr(norm + '.outValue', material + '.normalCamera')



    return

def createTexNodeByType(folderName, fileName, material, texType):
    if(texType == BASE_COLOR):
         createBaseColorNode(folderName, fileName, material)

    if(texType == METALNESS):
         createMetalnessNode(folderName, fileName, material)

    if(texType == ROUGHNESS):
         createRoughnessNode(folderName, fileName, material)

    if(texType == NORMAL):
         createNormalNode(folderName, fileName, material)

def browse(srcTextField):
    dir = cmds.fileDialog2(fm=3, dialogStyle=1)[0]
    cmds.textField(srcTextField, edit=True, tx=dir)
    return dir

def import_maps(srcTextField):
    folderName = cmds.textField(srcTextField, query=True, text=True)

    if not folderName:
        cmds.error("No folder selected.")
        return


    #Create aiStandardSurface and shading group node
    baseMatName = os.path.basename(os.path.normpath(folderName))
    surfaceName = cmds.shadingNode('aiStandardSurface', name=baseMatName + '_mat', asShader=True)
    SGName = cmds.sets(name=baseMatName + '_SG', empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr(surfaceName + '.outColor', SGName + '.surfaceShader')


    #Find the relevant files in the folder and create the file nodes
    fileList = cmds.getFileList( folder=folderName, filespec='*.png')

    nodesCreated = 0;
    totalNodes = 0;
    for suffix in [BASE_COLOR, METALNESS, ROUGHNESS, NORMAL]:
        totalNodes = totalNodes + 1;

        for fileName in fileList:
            if(suffix in fileName):
                createTexNodeByType(folderName, fileName, surfaceName, suffix)
                nodesCreated = nodesCreated + 1;

    #Sanity check
    if nodesCreated != totalNodes:
        cmds.error("Made " + nodesCreated + " file nodes, expected " + totalNodes + ". Check file names?")

    return


##UI

#Create fresh window
winID = "load_substance_maps"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)
win = cmds.window(winID, title="Load Substance Maps", sizeable=False)
cmds.window( win, edit=True, widthHeight=(500, 140) )

#Layout
cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 440), (2, 60)])

cmds.text( label='Select folder containing Substance Painter maps.', height=30 )
cmds.separator(style='none')

srcDir = cmds.textField()
cmds.button(label="Browse", command='browse(srcDir)')

cmds.separator(style='none', height=30)
cmds.separator(style='none')

cmds.button(label="Import as aiStandardSurface", command='import_maps(srcDir)', height=40)

cmds.showWindow()
