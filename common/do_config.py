from configparser import ConfigParser
from common import contants

class Config:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(contants.global_dir,encoding='utf-8')
        self.switch = self.config.getboolean('global','switch')
        self.dir = None

        if self.switch:
            self.dir = contants.dev_dir
            self.conf = self.config.read(contants.dev_dir,encoding='GBK')

        else:
            self.dir=contants.uat_dir
            self.conf = self.config.read(contants.uat_dir, encoding='GBK')


    def get(self,section,option):
        return self.config.get(section,option)

    def set(self,section,option,value):
        self.config = ConfigParser()
        self.config.read(self.dir, encoding='GBK')
        self.config.set(section,option,str(value))
        with open(self.dir, "w+") as f:
            self.config.write(f)
            f.close()

config = Config()