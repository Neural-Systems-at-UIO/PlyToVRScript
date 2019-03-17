import os
import bpy
import time
import numpy


#How to use
#filename = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/BlenderTest.py"
#exec(compile(open(filename).read(), filename, 'exec'))


##############   PARAMETERS   ########################
from Helpers.Importers import import_stl, import_dae, export_all_fbx
from Helpers.Modifiers import decimateMeshes, normalize_scale, smoothMeshes

folderPath = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData"
vertexLimit = 1500000
fileTypeToImport = 'stl'
exportToFBX = False
targetSize = numpy.array([1.0, 1.0, 1.0])
attemptSmoothing = True


######################################################

startTime = time.time()

for o in bpy.data.objects:
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

for mesh in bpy.data.objects:
    if mesh.type == 'MESH':
        totalVertexCountAfter += len(mesh.data.vertices)

bpy.ops.object.select_all(action='DESELECT')
# Remove junk and bloat data
for mesh in bpy.data.objects:
    if '.001' in mesh.name:
        mesh.select = True

for mesh in bpy.data.objects:
    if 'node' in mesh.name:
        mesh.select = True

for mesh in bpy.data.objects:
    if 'light' in mesh.name:
        mesh.select = True
bpy.ops.object.delete()

normalize_scale(targetSize)

if attemptSmoothing:
    smoothMeshes()

# Export processed files
if exportToFBX:
    export_all_fbx(folderPath)

print("Number of verts after reduction is " + str(totalVertexCount))
print("Execution time " + str(time.time() - startTime))
