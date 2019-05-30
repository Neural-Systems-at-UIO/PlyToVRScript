from configparser import ConfigParser

from ConfigurationManager.Configuration import Configuration


class ConfigReader:
    config = ConfigParser()



    def readConfig(self):
        self.config.read("D:/config")

        configuration = Configuration()
        temp = self.config.get("general", "targetSize", fallback="[1.0, 1.0, 1.0]")
        configuration.targetSize = eval(temp)

        configuration.vertexLimit = self.config.getint("modifiers", "targetSize", fallback=1500000)
        configuration.smoothing = self.config.getboolean("modifiers", "smoothing", fallback=True)
        configuration.decimate = self.config.getboolean("modifiers", "decimate", fallback=True)

        configuration.folderPath = self.config.get("input/output", "folderPath", fallback="NOT SET")
        configuration.exportToFBX = self.config.getboolean("input/output", "exportToFBX", fallback=False)
        configuration.fileTypeToImport = eval(self.config.get("input/output", "fileTypeToImport", fallback="['stl']"))

        return configuration
