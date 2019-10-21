#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import os
import usb
import sys
import cv2
import time
import signal
import usbtmc
import serial
import datetime
import k2636b_help
import numpy as np
import pandas as pd
import multiprocessing as mp
import matplotlib.pyplot as plt



FILE_NAME = "OLED_TEST"
DEV_ADDRESS = 'ASRL/dev/ttyUSB0::INSTR'
#DEV_ADDRESS = '/dev/usbtmc0'
OLEDarea = 4.5e-6
DataFileName="OLED_Test"

class luxmeter():
    """
    read luminance form light sensor connected to arduino.
    communication via serial port. Arduino every 0.5 sec
    send value on light intensity.
    cde for arduino available on github
    """

    def __init__(self):
        self.NoLUX = False
        self.treshold = 0
        try:
            self.ser = serial.Serial("/dev/ttyACM0")
            time.sleep(1)
            self.treshold = self.Lux_Get()
            self.treshold = self.Lux_Get()
            print(self.treshold)

        except serial.serialutil.SerialException:
            print("INIT Luxmeter ....  Dev. not connected",)
            self.NoLUX = True

    def Lux_Get(self):
        if self.NoLUX: return 0.001

        self.txt = ""
        self.ser.flushInput()
        while True:
            c = str(self.ser.read(), "utf-8")
            if c == '\n' or c == '\r': break
            self.txt += c

        self.txt = self.txt.strip("\r\n")

        try:
            self.txt = self.txt.split("/")[0] + "." + self.txt.split("/")[1]
            self.txt = float(self.txt.strip("\r\n"))-float(self.treshold)
        except IndexError:
            return 0.001

        try:
            return float(self.txt)
        except ValueError:
            return 0.001


class OLED_Plot_ProcessPlotter(object):
    def __init__(self,fname):
        self.x = []
        self.y1 = []
        self.y2 = []
        self.fname   = fname
        self.xlabel  = "V [V]"
        self.y1label = "I [A]"
        self.y2label = "Luminance [lum]"
        self.title   = fname
        self.xscale  = "lin"
        self.y1scale = "log"
        self.y2scale = "log"
        self.type    = "typ"
        self.y1style   = "ro" # "k",
        self.y2style   = "ro" # "k"

    def terminate(self):
        plt.savefig(str(self.fname+".png"))
        print("PNG saved to file:", str(self.fname+ ".png"))
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            command = self.pipe.recv()
            if command is None:
                self.terminate()
                return False
            else:
                self.x.append(command[0])
                self.y1.append(command[1])
                self.y2.append(command[2])
                self.ax.plot(self.x, self.y1, self.y1style, marker='o',color='b')
                self.bx.plot(self.x, self.y2, self.y2style, marker='o',color='r')

        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        self.bx = self.ax.twinx()

        self.fig.suptitle(os.path.basename(self.fname))
        self.ax.set_xlabel(self.xlabel  , color='b')
        self.ax.set_ylabel(self.y1label , color='b')
        self.bx.set_ylabel(self.y2label , color='r')

        self.ax.ticklabel_format(style='sci', axis='y', scilimits=(1, 4))
        self.bx.ticklabel_format(style='sci', axis='y', scilimits=(1, 4))
        self.ax.set_yscale(self.y1scale)
        self.bx.set_yscale(self.y2scale)

        self.ax.grid(color='b', linestyle='--', linewidth=0.1)

        timer = self.fig.canvas.new_timer(interval=100)
        timer.add_callback(self.call_back)
        timer.start()

        plt.show()

class OLED_Plot(object):

    def __init__(self,fname):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter      = OLED_Plot_ProcessPlotter(fname)
        self.plot_process = mp.Process( target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def plot(self,data=np.array([0,0]), finished=False):
        if finished:
            self.plot_pipe.send(None)
            time.sleep(0.25)
        else:
            self.plot_pipe.send(data)

class k2636b():
    data_path = str(os.path.dirname(os.path.realpath(__file__)) + "/data/")

    if_camera      = False
    if_verbose     = True
    if_plot_figure = True

    TAGS_Header = ">>head<<"
    TAGS_END    = ">>END<<"

    def handler(self, signum, frame):
        print("\n")
        print("========================================")
        print("=============== ABORT! =================")
        print("========================================")

        self.kwrite('ABORT')
        time.sleep(1)
        self.kwrite('loadscript')
        self.kwrite('print("' + str(self.TAGS_END) + '")')
        self.kwrite('beeper.beep(0.2, 800)')
        self.kwrite('beeper.beep(0.1, 850)')
        self.kwrite('delay(0.5)')
        self.kwrite('reset()')
        self.kwrite('endscript')
        self.kwrite('script.anonymous.run()')

    def __init__(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.signal(signal.SIGINT,  self.handler)
        self.Dev_Init()
        self.lux = luxmeter()
        print(self.lux.treshold)

    def Dev_Init(self):
        """ Initialize device  """
        try:
            """ establish connection with device and set timeout for 10 sec
                after timeout=10 sec connection will be terminated.   
            """
            self.inst = usbtmc.Instrument(0x05e6, 0x2636,timeout=10)
            self.inst.write("*CLS")
            # print(self.kread())
        except usbtmc.usbtmc.UsbtmcException:
            print('Cannot open Device Port.')
            sys.exit()
            return 0

    def CloseConnect(self):
        """Close connection to keithley."""

    def info(self):
        """ Print basic info about device """
        print(self.inst.ask("*IDN?"))
        print("STB:", self.inst.ask("*STB?"))
        print("SRE:", self.inst.ask("*SRE?"))
        print("ESE:", self.inst.ask("*ESE?"))
        print("ESR:", self.inst.ask("*ESR?"))
        print("OPC:", self.inst.ask("*OPC?"))

    def kwrite(self, cmd):
        """Write to instrument."""
        try:
            assert type(cmd) == str
            self.inst.write(cmd)
        except AttributeError:
            print('ERROR: Could not write device.')

    def kread(self):
        """Read instrument."""
        try:
            r = self.inst.read()
            return r
        except AttributeError:
            print('ERROR: Could not read from device.')
            raise SystemExit

    def loadTSP(self, script_name, param=''):
        """Load an anonymous TSP script into the K2636 nonvolatile memory."""
        print("Loading: ", script_name)
        try:
            self.kwrite('ABORT')
            self.kwrite('loadscript')
            self.kwrite(param)

            for line in open(str("TSP//" + script_name), mode='r'): self.kwrite(line)

            self.kwrite('print("' + str(self.TAGS_END) + '")')
            self.kwrite('reset()')
            self.kwrite('endscript')

        except AttributeError:
            print('ERROR: Could not load tsp script.')
            raise SystemExit

    def runTSP_oled(self, fn="test"):
        """ process all incoming data form K2636B   """
        try:
            if self.if_plot_figure:
                self.pl = OLED_Plot(fn)
                time.sleep(1)

            self.kwrite('script.anonymous.run()')

            a  = []
            df = pd.DataFrame()

            while True:
                InComingData = self.kread()
                InComminLuxx = self.lux.Lux_Get()

                if self.TAGS_END    in InComingData: break

                if self.if_plot_figure and (not self.TAGS_Header in InComingData ) :
                    dp = np.array([float(InComingData.split()[0]), float(InComingData.split()[1]), float(InComminLuxx)])
                    self.pl.plot(dp)

                if self.TAGS_Header in InComingData:
                    InComingData += " \t " + str("lux") + " \t " + str("CurrCoeff.")
                else:
                    self.OLEDarea=4.5e-6  #convert to m2
                    CurrM2    = float(InComingData.split()[1])/self.OLEDarea
                    LummM2    = float(InComminLuxx) / self.OLEDarea
                    CurrCoeff = (0.01 * (float(InComminLuxx) / float(InComingData.split()[1])))

                    CurrM2    = self.format(CurrM2)
                    LummM2    = self.format(LummM2)
                    CurrCoeff = self.format(CurrCoeff)

                    InComingData += " \t " + str(InComminLuxx) + " \t " + str(CurrM2) + " \t " + str(LummM2) + "\t" + str(CurrCoeff)

                self.DataSave(fn, InComingData)

                InComingData = InComingData.replace(self.TAGS_Header, "")
                a.append(InComingData.split())

            dd = pd.DataFrame(a)
            df = pd.concat([df, dd], axis=1, sort=False)
            self.DataSave(fn, df)

            txt="DATA File: " +str(fn)
            self.DataSave(fn, txt)

            if self.if_plot_figure:
                self.pl.plot(finished=True)
                cv2.destroyAllWindows()

        except AttributeError:
            print('ERROR: Some ERROR in runTSP function')
            raise SystemExit


    def format(self,n):
        a = '%E' % n
        return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]



    def DataSave(self, fn, data):
        """  Save RAW data and dataframe data to another file"""
        if self.if_verbose: print(data)
        if isinstance(data, pd.DataFrame):
            data.to_csv(self.DataFileName, sep=' ', encoding='utf-8', index=False, header=None)
        else:
            with open(str(self.DataFileName + "_raw.txt"), 'a') as the_file: \
                    the_file.write(str(data) + "\n")

    def check_file_name(self, fname):
        fname = self.data_path + fname
        index = 0
        root, ext = os.path.splitext(os.path.expanduser(fname))
        fname = os.path.basename(root)
        dir = os.path.dirname(root)
        filename = "{0}_{1:03d}{2}".format(fname, index, ext)
        while filename in os.listdir(dir):
            filename = "{0}_{1:03d}{2}".format(fname, index, ext)
            index += 1
        filename = str(dir + "/" + filename)
        with open(str("filename.log"), 'a') as the_file: the_file.write(
            str(datetime.datetime.now()) + "\t" + str(filename) + "\n")

        self.DataFileName=filename

        return filename

    # ------------- oled
    def oled(self, *param):
        """K2636 Transfer sweeps."""
        # print(param)
        try:
            print("++++++++++++++++++++++++++++++++++++++")
            self.if_camera = False
            begin_time = time.time()
            # (OLED_VStart), (OLED_VEnd), (OLED_VStep)
            # [FName, VGS_start, VGS_stop, VGS_step, VDS_comp, VGS_comp, NPLC, DEL, SWEEP]
            if param[8]: ss = "true"
            sample = param[0]
            # self.DataFileName = str(param[0]+ '_oled.txt')
            # self.DataFileName = \
            self.check_file_name(str(param[0]+ '_oled.txt'))

            cmd =   "OLED_VStart = " + str(float(param[1])) + "\n" \
                    "OLED_VEnd   = " + str(float(param[2])) + "\n" \
                    "OLED_VStep  = " + str(float(param[3])) + "\n" \
                    "SWEEP    = " + "True" + "\n" \
                    "NPLC     = " + str(float(param[6])) + "\n" \
                    "DELATE   = " + str(float(2)) + "\n"

            file_name = str(sample + '_oled.txt')
            file_name = self.check_file_name(file_name)

            self.loadTSP('k2636b_oled_sweep.tsp', cmd)

            self.runTSP_oled(file_name)
            # self.stats(file_name)

            finish_time = time.time()
            txt = "OLED characteristic complete. " + str(round((finish_time - begin_time), 2))
            print(txt)

            return 0

        except(AttributeError):
            print('Cannot perform output sweep: no keithley connected.')



# ================================================================
# ============================= MAIN =============================
# ================================================================
if __name__ == '__main__':
    args = k2636b_help.help()

    try:
        keithley = k2636b()
        keithley.info()
    except usb.core.USBError:
        print("some errors")
        sys.exit()

    if args.fig: k2636b.if_plot_figure = False

    if args.filename != "tr00": FILE_NAME = args.filename

    if args.oled:
        # print(args.oled)
        # ------- TRANSFER: parametry pomiaru
        FName = FILE_NAME
        VGS_start = args.oled[0][0]
        VGS_stop = args.oled[0][1]
        VGS_step = args.oled[0][2]
        VDS_comp = args.DCOMP
        VGS_comp = args.GCOMP
        NPLC = args.NPLC
        PICNPLC = NPLC
        DEL = args.DEL
        SWEEP = True

        param_transfer = [FName,VGS_start, VGS_stop, VGS_step, VDS_comp, VGS_comp, NPLC, DEL, SWEEP]
        keithley.oled(*param_transfer)

    keithley.CloseConnect()
