from configparser import ConfigParser


class ConfigWriter:
    # folderPath = "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData"
    # vertexLimit = 1500000
    # fileTypeToImport = 'stl'
    # exportToFBX = False
    # targetSize = numpy.array([1.0, 1.0, 1.0])
    # attemptSmoothing = True

    config = ConfigParser()

    config["general"] = {
        "folderPath": "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData",
        "targetSize": "[1.0, 1.0, 1.0]"
    }

    config["modifiers"] = {
        "vertexLimit": "1500000",
        "smoothing": "True",
        "decimate": "False"

    }

    config["input/output"] = {
        "folderPath": "D:/Users/NoobsDeSroobs/PycharmProjects/PlyToVRScript/SourceData",
        "exportToFBX": 'False',
        "fileTypeToImport": "['stl']"
    }

    def storeConfig(self):
        with open("./config", 'w') as file:
            self.config.write(file)