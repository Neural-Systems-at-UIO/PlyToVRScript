import os
import bpy
import time
import numpy



Idea
Make a script that is the GUI and then make that script launch a terminal, or have the script itself be launched in a terminal.
The first script opens a GUI and then the script launches blender with another script based on the settings from the GUI.



# How to use
# blender --background --python C:/Projects/PlyToVRScript/BlenderTest.py
# filename = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/BlenderTest.py"
# exec(compile(open(filename).read(), filename, 'exec'))


##############   PARAMETERS   ########################
from ConfigurationManager.ConfigReader import ConfigReader
from ConfigurationManager.ConfigWriter import ConfigWriter
from Helpers.Importers import import_stl, import_dae, export_all_fbx
from Helpers.Modifiers import decimateMeshes, colourObjects, removeJunk, normalize_scale, smoothMeshes

if __name__ == "__main__":
    config = ConfigReader()
    config.readConfig()

    folderPath = "C:/Projects/PlyToVRScript/SourceData"
    vertexLimit = 1500000
    fileTypeToImport = 'stl'
    exportToFBX = True
    targetSize = numpy.array([1.0, 1.0, 1.0])
    attemptSmoothing = True

    ######################################################

    startTime = time.time()

    for o in bpy.data.objects:
        print(dir(o))
        o.select = True

    bpy.ops.object.delete()

    for root, dir, files in os.walk(folderPath):
        for file in files:
            if file.endswith("stl") and fileTypeToImport == 'stl':
                import_stl(folderPath, file)
                print("Importing " + file)
            elif file.endswith("dae") and fileTypeToImport == 'dae':
                import_dae(folderPath, file)
                print("Importing " + file)

    # bpy.ops.wm.save_mainfile(filepath="") Bruk denne for lagring av blender filene.

    totalVertexCount = 0

    for mesh in bpy.data.objects:
        if mesh.type != 'MESH':
            continue
        totalVertexCount += len(mesh.data.vertices)

    print("Number of verts before reduction is " + str(totalVertexCount))

    totalVertexCountAfter = 0

    if totalVertexCount > vertexLimit:
        ratio = vertexLimit / totalVertexCount
        decimateMeshes(ratio)

    colourObjects()

    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            totalVertexCountAfter += len(mesh.data.vertices)

    bpy.ops.object.select_all(action='DESELECT')
    # Remove junk and bloat data
    removeJunk()

    normalize_scale(targetSize)

    if attemptSmoothing:
        smoothMeshes()

    # Export processed files
    if exportToFBX:
        export_all_fbx(folderPath)

    print("Number of verts after reduction is " + str(totalVertexCountAfter))
    print("Execution time " + str(time.time() - startTime))
