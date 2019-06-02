import os
from configparser import ConfigParser


class ConfigWriter:
	# folderPath = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData"
	# vertexLimit = 1500000
	# fileTypeToImport = 'stl'
	# exportToFBX = False
	# targetSize = numpy.array([1.0, 1.0, 1.0])
	# attemptSmoothing = True



	# config["general"] = {
	#     "targetSize": "[1.0, 1.0, 1.0]"
	# }
	#
	# config["modifiers"] = {
	#     "vertexLimit": "1500000",
	#     "smoothing": "True",
	#     "decimate": "False"
	#
	# }
	#
	# config["input/output"] = {
	#     "folderPath": "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData",
	#     "exportToFBX": 'False',
	#     "fileTypeToImport": "['stl']"
	# }

	def storeConfig(self, configuration):
		config = ConfigParser()
		config["general"] = {
			"targetSize": str(configuration.targetSize),
			"executedFromBlender": str(configuration.executedFromBlender)
		}

		config["modifiers"] = {
			"vertexLimit": str(configuration.vertexLimit),
			"smoothing": str(configuration.smoothing),
			"decimate": str(configuration.decimate)

		}

		config["input/output"] = {
			"folderPath": str(configuration.folderPath),
			"exportToFBX": str(configuration.exportToFBX),
			"fileTypeToImport": str(configuration.fileTypeToImport)
		}

		with open("config", 'w+') as file:
			config.write(file)
