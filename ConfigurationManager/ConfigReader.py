from configparser import ConfigParser

from ConfigurationManager.Configuration import Configuration


class ConfigReader:
    config = ConfigParser()



    def readConfig(self):
        self.config.read("config")

        configuration = Configuration()
        configuration.targetSize = eval(self.config.get("general", "targetSize"))
        configuration.executedFromBlender = eval(self.config.get("general", "executedFromBlender"))

        configuration.vertexLimit = self.config.getint("modifiers", "vertexlimit")
        configuration.smoothing = self.config.getboolean("modifiers", "smoothing")
        configuration.decimate = self.config.getboolean("modifiers", "decimate")

        configuration.folderPath = self.config.get("input/output", "folderPath")
        configuration.exportToFBX = self.config.getboolean("input/output", "exportToFBX")
        configuration.fileTypeToImport = eval(self.config.get("input/output", "fileTypeToImport"))

        return configuration
