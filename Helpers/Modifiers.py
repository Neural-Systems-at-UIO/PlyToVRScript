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


def normalize_scale(targetSize):
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

    for window in bpy.context.window_manager.windows:
        screen = window.screen
    
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.screen.screen_full_area(override)
                bpy.ops.object.select_all(action='SELECT')
                #origin to geometry
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                #cursor to centre
                bpy.ops.view3d.snap_cursor_to_center()
                #selection to cursor, use offset
                bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
                #origin to cursor
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    bpy.ops.object.select_all(action='DESELECT')


def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if m.type == "DECIMATE":
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
    try:
        subModelID = int(name[0:name.index("-")])
        if subModelID is None:
            raise ValueError("ModelID is None")
        return subModelID
    except ValueError:
        print("The file name is wrong. Make sure it starts with the numerical ID followed by a dash; e.g. 0001-someName")
        raise ValueError("The file name is wrong. Make sure it starts with the numerical ID followed by a dash; e.g. 0001-someName")


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

        if colourDict:
            obj_name = bpy.context.active_object.name
            print(obj_name)
            subModelID = getSubModelID(obj_name)
            if subModelID not in colourDict:
                print("Missing colour mapping from Atlas. Was looking for " + str(subModelID))
                rgba = [0.8, 0.8, 0.8, 1.0]
            else:
                rgba = [float(colourDict[subModelID][1])/255.0, float(colourDict[subModelID][2])/255.0, float(colourDict[subModelID][3])/255.0, 1.0]
        else:
            rgba = [random.random(), random.random(), random.random(), 1.0]

        mat = bpy.data.materials.new("atlasColour")
        mat.diffuse_color = rgba

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            # no slots
            obj.data.materials.append(mat)

        time.sleep(0.1)
