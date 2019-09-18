import os
from configparser import ConfigParser


class ConfigWriter:

	def storeConfig(self, configuration):
		config = ConfigParser()
		config["general"] = {
			"targetSize": str(configuration.targetSize)
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
