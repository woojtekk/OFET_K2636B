import datetime
import plot
import numpy as np
import math
import configparser

class configure():
    def __init__(self):
        print("init")
        config = configparser.ConfigParser()
        config.read('example.ini')
        for x in config.sections():
            print(x,config.items(x))

if __name__ == '__main__':
    cc=configure()
