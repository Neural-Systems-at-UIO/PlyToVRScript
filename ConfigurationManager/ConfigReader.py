from configparser import ConfigParser

from ConfigurationManager.Configuration import Configuration


class ConfigReader:
    config = ConfigParser()



    def readConfig(self):
        self.config.read("config")

        configuration = Configuration()
        configuration.targetSize = eval(self.config.get("general", "targetSize", fallback="[1, 1, 1]"))

        configuration.vertexLimit = self.config.getint("modifiers", "vertexlimit", fallback=1500000)
        configuration.smoothing = self.config.getboolean("modifiers", "smoothing", fallback=True)
        configuration.decimate = self.config.getboolean("modifiers", "decimate", fallback=True)

        configuration.folderPath = self.config.get("input/output", "folderPath", fallback="")
        configuration.exportToFBX = self.config.getboolean("input/output", "exportToFBX", fallback=True)
        configuration.fileTypeToImport = eval(self.config.get("input/output", "fileTypeToImport", fallback="[]"))

        return configuration
