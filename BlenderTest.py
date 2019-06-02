import os
import bpy
import time
import numpy



#Idea
#Make a script that is the GUI and then make that script launch a terminal, or have the script itself be launched in a terminal.
#The first script opens a GUI and then the script launches blender with another script based on the settings from the GUI.



# How to use
# blender --background --python C:/Projects/PlyToVRScript/BlenderTest.py
# filename = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/BlenderTest.py"
# exec(compile(open(filename).read(), filename, 'exec'))


##############   PARAMETERS   ########################
from ConfigurationManager.ConfigReader import ConfigReader
from ConfigurationManager.ConfigWriter import ConfigWriter
from Helpers.Importers import import_stl, import_dae, export_all_fbx
from Helpers.Modifiers import decimateMeshes, colourObjects, removeJunk, normalize_scale, smoothMeshes



config = ConfigReader()
configuration = config.readConfig()

######################################################

startTime = time.time()

for o in bpy.data.objects:
    o.select = True

bpy.ops.object.delete()
print(configuration.folderPath)
for root, dir, files in os.walk(configuration.folderPath):
    for file in files:
        if file.endswith("stl") and 'stl' in configuration.fileTypeToImport:
            import_stl(configuration.folderPath, file)
            print("Importing " + file)
        elif file.endswith("dae") and configuration.fileTypeToImport == 'dae':
            import_dae(configuration.folderPath, file)
            print("Importing " + file)

# bpy.ops.wm.save_mainfile(filepath="") Bruk denne for lagring av blender filene.

totalVertexCount = 0

for mesh in bpy.data.objects:
    if mesh.type != 'MESH':
        continue
    totalVertexCount += len(mesh.data.vertices)

print("Number of verts before reduction is " + str(totalVertexCount))

totalVertexCountAfter = 0

if totalVertexCount > configuration.vertexLimit and configuration.decimate:
    print("Decimating. Target: " + str(configuration.vertexLimit))
    ratio = configuration.vertexLimit / totalVertexCount
    decimateMeshes(ratio)

colourObjects()

for mesh in bpy.data.objects:
    if mesh.type == 'MESH':
        totalVertexCountAfter += len(mesh.data.vertices)

bpy.ops.object.select_all(action='DESELECT')
# Remove junk and bloat data
removeJunk()

normalize_scale(configuration.targetSize, configuration.executedFromBlender)

if configuration.smoothing:
    print("Smoothing.")
    smoothMeshes()

# Export processed files
if configuration.exportToFBX:
    print("Exporting to FBX.")
    export_all_fbx(configuration.folderPath)

print("Number of verts after reduction is " + str(totalVertexCountAfter))
print("Execution time " + str(time.time() - startTime))
