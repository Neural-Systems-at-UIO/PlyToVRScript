import os
import time
import sys

import bpy

sys.path.append(str(os.path.realpath(os.path.join(__file__, ".."))))
from ConfigurationManager import ConfigReader

##############   PARAMETERS   ########################
from Helpers.Importers import import_stl, import_dae, import_obj, export_all_fbx
from Helpers.Modifiers import decimateMeshes, colourObjects, removeJunk, normalize_scale, smoothMeshes


class BlenderProcessor:
	
	@staticmethod
	def processFolder(configuration, subFolder):
		print("Processing " + subFolder)
		startTime = time.time()
		
		for o in bpy.data.objects:
			o.select_set(state=True)
		
		bpy.ops.object.delete()
		importAllOverride = len(configuration.fileTypeToImport) is 1 and not configuration.fileTypeToImport[0]
		for subFile in os.listdir(subFolder):
			filePath = os.path.join(subFolder, subFile)
			if os.path.isfile(filePath):
				if filePath.endswith("stl") and (importAllOverride or 'stl' in configuration.fileTypeToImport):
					import_stl(subFolder, subFile)
				if filePath.endswith("dae") and (importAllOverride or 'dae' in configuration.fileTypeToImport):
					import_dae(subFolder, subFile)
				if filePath.endswith("obj") and (importAllOverride or 'obj' in configuration.fileTypeToImport):
					import_obj(subFolder, subFile)
				if filePath.endswith("fbx") and (importAllOverride or 'fbx' in configuration.fileTypeToImport):
					import_obj(subFolder, subFile)
		
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
		
		colourObjects(subFolder)
		
		for mesh in bpy.data.objects:
			if mesh.type == 'MESH':
				totalVertexCountAfter += len(mesh.data.vertices)
		
		bpy.ops.object.select_all(action='DESELECT')
		# Remove junk and bloat data
		removeJunk()
		
		normalize_scale(configuration.targetSize)
		
		if configuration.smoothing:
			print("Smoothing.")
			smoothMeshes()
		
		# Export processed files
		if configuration.exportToFBX:
			print("Exporting to FBX.")
			export_all_fbx(subFolder + "/fbx")
		
		bpy.ops.wm.save_as_mainfile(filepath=os.path.join(subFolder, "project.blend"))
		print("Number of verts after reduction is " + str(totalVertexCountAfter))
		print("Execution time " + str(time.time() - startTime))


configReader = ConfigReader.ConfigReader()
topConfiguration = configReader.readConfig()

######################################################

processor = BlenderProcessor()

for filename in os.listdir(topConfiguration.folderPath):
	fullPath = os.path.join(topConfiguration.folderPath, filename)
	print("Considering " + fullPath)
	if os.path.isdir(fullPath):
		processor.processFolder(topConfiguration, fullPath)
