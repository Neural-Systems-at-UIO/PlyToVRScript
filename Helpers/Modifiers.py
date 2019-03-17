import bpy
import numpy


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


def normalize_scale(targetSize):  #numpy.array([1.0, 1.0, 1.0])
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