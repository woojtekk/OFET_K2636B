#!/usr/bin/env python

import configparser
import io

class config_import():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("confpar.ini")

    def get_param(self,section,param):
        try:
            value=self.config.get(section, param)
        except configparser.NoOptionError:
            print("ERROR: config file. no parameter:",param)
            return -1
        return value

    def put_param(self,section,param):
        return 0



oo = config_import()
print(oo.get_param("OLED","nplc"))





