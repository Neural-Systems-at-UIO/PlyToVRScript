import os
import random
import time

import bpy
import numpy



def smoothMeshes():
    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.select_set(state=True)
            bpy.context.view_layer.objects.active = mesh
            mesh.modifiers.new('smoothingMod', type='SMOOTH')
            mesh.modifiers['smoothingMod'].factor = 1.0
            mesh.modifiers['smoothingMod'].iterations = 5.0
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='smoothingMod')
            mesh.select_set(state=False)


def decimateMeshes(decRatio):
    modifierName = 'DecimateMod'
    bpy.ops.object.select_all(action='DESELECT')
    for mesh in bpy.data.objects:
        if mesh.type != 'MESH':
            continue
        mesh.select_set(state=True)
        bpy.context.view_layer.objects.active = mesh
        modifier = mesh.modifiers.new(modifierName, 'DECIMATE')
        modifier.ratio = decRatio
        modifier.use_collapse_triangulate = True
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifierName)
        mesh.select_set(state=False)


def normalize_scale(targetSize, executedFromBlender):  # numpy.array([1.0, 1.0, 1.0])
    print("ewqweqweq")
    if executedFromBlender:
        print("asdasdasda")
        bpy.context.area.type = 'VIEW_3D'

    maxX = maxY = maxZ = 0
    minX = minY = minZ = 999999999
    bpy.ops.object.select_all(action='DESELECT')

    for mesh in bpy.data.objects:
        if mesh.type == 'MESH':
            mesh.select_set(state=True)
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

    if executedFromBlender:
        print("asdasdasda")
        bpy.context.area.type = 'TEXT_EDITOR'


def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if (m.type == "DECIMATE"):
            obj.modifiers.remove(modifier=m)


def removeJunk():
    for mesh in bpy.data.objects:
        if '.001' in mesh.name:
            mesh.select_set(state=True)
        if 'node' in mesh.name:
            mesh.select_set(state=True)
        if 'light' in mesh.name:
            mesh.select_set(state=True)
    bpy.ops.object.delete()


def getSubModelID(name):
    subModelID = -1
    try:
        subModelID = int(name[0:name.index("-")])
    except:
        subModelID = int(name[name.index("_v2")+3:])
    return subModelID


def colourObjects(currentFolderPath):
    # Assumes there is exactly one txt file and that it is the atlas
    atlasPath = "does not exist"
    colourDict = dict()
    for file in os.listdir(currentFolderPath):
        if file.endswith(".txt"):
            atlasPath = os.path.join(currentFolderPath, file)
            f = open(atlasPath, "r")
            for line in f:
                if line.startswith("#"):
                    continue
                splitLine = line.split()
                colourDict[int(splitLine[0])] = splitLine
            break


    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue

        bpy.context.view_layer.objects.active = obj
        obj.select_set(state=True)

        if colourDict:
            obj_name = bpy.context.active_object.name
            print(obj_name)
            subModelID = getSubModelID(obj_name)
            if subModelID not in colourDict:
                print("Missing colour mapping from Atlas. Was looking for " + str(subModelID))
                rgba = [0.8, 0.8, 0.8, 1.0]
            else:
                rgba = [float(colourDict[subModelID][1])/255, float(colourDict[subModelID][2])/255, float(colourDict[subModelID][3])/255, 1.0]
                print(str(subModelID) + ' | ' + str(rgba) + ' | ' + str(colourDict[subModelID]))
        else:
            print("Random")
            rgba = [random.random() for i in range(3)].append(1.0)


        mat = bpy.data.materials.new("atlasColour")
        mat.diffuse_color = rgba

        # Assign it to object
        if obj.data.materials:
            # assign to 1st material slot
            obj.data.materials[0] = mat
        else:
            # no slots
            obj.data.materials.append(mat)

        obj.select_set(state=False)
        time.sleep(0.1)
