import os
import bpy
import time
import numpy


#How to use
#filename = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/BlenderTest.py"
#exec(compile(open(filename).read(), filename, 'exec'))


##############   PARAMETERS   ########################
folderPath = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData"
vertexLimit = 1500000
fileTypeToImport = 'stl'
exportToFBX = False
targetSize = numpy.array([1.0, 1.0, 1.0])
attemptSmoothing = True


######################################################

def smoothMeshes():
    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.select = True
            bpy.context.scene.objects.active = mesh
            mesh.modifiers.new('smoothingMod', type='SMOOTH')
            mesh.modifiers['smoothingMod'].factor = 1.0
            mesh.modifiers['smoothingMod'].iterations = 5.0
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='smoothingMod')
            mesh.select = False


def decimateMeshes(decRatio):
    modifierName = 'DecimateMod'
    bpy.ops.object.select_all(action='DESELECT')
    for mesh in bpy.data.objects:
        if mesh.type != 'MESH':
            continue
        mesh.select = True
        bpy.context.scene.objects.active = mesh
        modifier = mesh.modifiers.new(modifierName, 'DECIMATE')
        modifier.ratio = decRatio
        modifier.use_collapse_triangulate = True
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)
        mesh.select = False


def normalize_scale():
    bpy.context.area.type = 'VIEW_3D'

    maxX = maxY = maxZ = 0
    minX = minY = minZ = 999999999
    bpy.ops.object.select_all(action='DESELECT')

    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.select = True
            x, y, z = mesh.dimensions
            maxX = max(maxX, x)
            minX = min(minX, x)
            maxY = max(maxY, y)
            minY = min(minY, y)
            maxZ = max(maxZ, z)
            minZ = min(minZ, z)

    xyzScales = numpy.array(
        [targetSize[0] / (maxX - minX), targetSize[1] / (maxY - minY), targetSize[2] / (maxZ - minZ)])
    maxUsableScale = xyzScales.min()

    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.scale = mesh.scale * maxUsableScale

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            bpy.ops.view3d.view_selected(ctx)
            bpy.ops.view3d.snap_cursor_to_selected(ctx)
            break

    # bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # bpy.ops.view3d.snap_cursor_to_center()
    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.location = (0, 0, 0)

    bpy.context.area.type = 'TEXT_EDITOR'


def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if (m.type == "DECIMATE"):
            obj.modifiers.remove(modifier=m)


def export_all_fbx(exportFolder):
    objects = bpy.data.objects
    for object in objects:
        bpy.ops.object.select_all(action='DESELECT')
        object.select = True
        exportName = os.path.abspath(os.path.join(exportFolder, object.name)) + '.fbx'
        bpy.ops.export_scene.fbx(filepath=exportName, use_selection=True, object_types={'MESH'}, apply_unit_scale=True,
                                 path_mode='ABSOLUTE')


def import_stl(folderPath, fileName):
    bpy.ops.import_mesh.stl(filepath=os.path.abspath(os.path.join(folderPath, fileName)))
    activeObject = bpy.context.active_object
    activeObject.name = fileName[:-4]
    mat = bpy.data.materials.get("Material")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="Material")

    mat.use_vertex_color_paint = True


def import_dae(folderPath, fileName):
    bpy.ops.wm.collada_import(filepath=os.path.abspath(os.path.join(folderPath, fileName)))
    bpy.ops.object.join()
    activeObject = bpy.context.active_object
    activeObject.name = fileName[:-4]
    mat = bpy.data.materials.get("Material")
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name="Material")

    mat.use_vertex_color_paint = True


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

normalize_scale()

if attemptSmoothing:
    smoothMeshes()

# Export processed files
if exportToFBX:
    export_all_fbx(folderPath)

print("Number of verts after reduction is " + str(totalVertexCount))
print("Execution time " + str(time.time() - startTime))
