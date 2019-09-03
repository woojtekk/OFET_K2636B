import datetime
import plot
import numpy as np
import math
import configparser

class configure():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('example.ini')
        print(config.get("K2636B","adress"))


if __name__ == '__main__':
    cc=configure()
