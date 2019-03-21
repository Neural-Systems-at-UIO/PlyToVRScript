from configparser import ConfigParser


class ConfigReader:
    config = ConfigParser()



    def readConfig(self):
        self.config.read("./config")

        print(self.config.sections())
        for section in self.config.sections():
            print("\n\n\n")
            print(section)
            for option in self.config.options(section):
                print(self.config.get(section, option))
