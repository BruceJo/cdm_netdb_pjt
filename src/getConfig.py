import os
import configparser as parser

class Config():
    def __init__(self, path):
        self.path = path
        if os.path.exists(self.path) == False:
            print("Not found config file.")
            raise Exception("Not found config file.")

    def getConfig(self):
        cp = parser.ConfigParser()
        cp.optionxform = str    #https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
        cp.read(self.path, encoding='utf-8')
        self.conf = cp._sections

        return self.conf
    
    def updateConfig(self, selection, key, value):
        cp = parser.ConfigParser()
        cp.optionxform = str
        cp.read(self.path, encoding='utf-8')
        cp.set(selection, key, value)
        
        with open(self.path, 'w') as configfile:
            cp.write(configfile)