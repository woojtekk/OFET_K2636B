#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#import signal
import os
import sys
import time
import visa
import signal
import serial
from serial import Serial
import pandas as pd
import matplotlib.pyplot as plt
import usbtmc


class OLED():

    def __init__(self):
        self.dev_open()

    def __call__(self, *args, **kwargs):
        return 0

    def dev_open(self):
        self.inst=usbtmc.Instrument(0x05e6,0x2636)
        self.inst.write("*CLS")
        return 0

    def dev_close(self):
        self.inst.close()
        return 0

    def dev_write(self):
        return 0

    def dev_read(self):
        return 0

    def info(self):
        return 0


if __name__ == '__main__':
    ol = OLED()
    ol.info()
    ol.dev_close()
