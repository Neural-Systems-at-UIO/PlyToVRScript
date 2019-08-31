import os
import bpy


def export_all_fbx(exportFolder):
	print("Exporting to " + exportFolder)
	if not os.path.exists(exportFolder):
		os.makedirs(exportFolder)
	objects = bpy.data.objects
	for object in objects:
		bpy.ops.object.select_all(action='DESELECT')
		object.select = True
		exportName = os.path.abspath(os.path.join(exportFolder, object.name)) + '.fbx'
		bpy.ops.export_scene.fbx(filepath=exportName, use_selection=True, object_types={'MESH'}, apply_unit_scale=True, path_mode='ABSOLUTE')
		print("Exported: " + exportFolder)


def import_stl(folderPath, fileName):
	filePath = os.path.join(folderPath, fileName)
	print("Importing STL file " + filePath)
	bpy.ops.import_mesh.stl(filepath=os.path.abspath(filePath))
	activeObject = bpy.context.active_object
	activeObject.name = fileName[:-4]

def import_dae(folderPath, fileName):
	filePath = os.path.join(folderPath, fileName)
	print("Importing DAE file " + filePath)
	bpy.ops.wm.collada_import(filepath=os.path.abspath(filePath))
	bpy.ops.object.join()
	activeObject = bpy.context.active_object
	activeObject.name = fileName[:-4]

def import_obj(folderPath, fileName):
	filePath = os.path.join(folderPath, fileName)
	print("Importing obj file " + filePath)
	bpy.ops.import_scene.obj(filepath=os.path.abspath(filePath))
	bpy.ops.object.join()
	activeObject = bpy.context.active_object
	activeObject.name = fileName[:-4]