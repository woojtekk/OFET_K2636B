#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import os
import usb
import sys
import cv2
import time
import math
import signal
import usbtmc
import serial
import datetime
import oled_help
import numpy as np
import pandas as pd
import multiprocessing as mp
import matplotlib.pyplot as plt
from confpar import config_import



FILE_NAME = "OLED_TEST"
DEV_ADDRESS = 'ASRL/dev/ttyUSB0::INSTR'
LUX_ADDRESS = "/dev/ttyACM0"
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
            self.ser = serial.Serial(LUX_ADDRESS)
            self.treshold = self.Lux_Get()

        except serial.serialutil.SerialException:
            print("INIT Luxmeter ....  Device not connected.",)
            self.NoLUX = True

    def Lux_Get(self):
        if self.NoLUX: return 0

        self.txt = ""
        self.ser.flushInput()
        while True:
            c = str(self.ser.read(), "utf-8")
            if c == '\n' or c == '\r': break
            self.txt += c

        self.txt = self.txt.strip("\r\n")

        try:
            self.txt = self.txt.split("/")[0] + "." + self.txt.split("/")[1]
            self.txt = float(self.txt.strip("\r\n"))
            # if self.txt<1: self.Lux_Get()
        except IndexError:
            return -1

        try:
            return float(self.txt)
        except ValueError:
            return -1

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
        self.y1scale = "lin"#"log"
        self.y2scale = "lin"#"log"
        self.type    = "typ"
        self.y1style   = "ro" # "k",
        self.y2style   = "ro" # "k"

    def terminate(self):
        plt.savefig(str(self.fname+".png"))
        print("PNG :", str(self.fname+ ".png"))
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
    if_abort       = False

    TAGS_Header    = ">>head<<"
    TAGS_END       = ">>END<<"

    def handler(self, signum, frame):
        print("\n")
        print("========================================")
        print("=============== ABORT! =================")
        print("========================================")
        self.if_abort = True

    def abort(self):
        self.kwrite('ABORT')
        time.sleep(1)
        self.kwrite('loadscript')
        self.kwrite('beeper.beep(0.2, 800)')
        self.kwrite('beeper.beep(0.1, 850)')
        self.kwrite('smub.source.output = smub.OUTPUT_OFF')
        self.kwrite('smua.source.output = smub.OUTPUT_OFF')
        self.kwrite('delay(0.1)')
        self.kwrite('reset()')
        self.kwrite('smua.reset()')
        self.kwrite('smua.reset()')
        self.kwrite('smub.reset()')
        self.kwrite('endscript')
        self.kwrite('script.anonymous.run()')

        print("==============================================")
        print("!!! OLED characteristic has been aborted !!!!")
        print("!!! Some data has been saved :) ")
        print("==============================================")

    def __init__(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.signal(signal.SIGINT,  self.handler)
        self.Dev_Init()
        self.lux = luxmeter()

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
        return 0

    def info(self):
        """ Print basic info about device """
        print(self.inst.ask("*IDN?"))
        print(" STB:", self.inst.ask("*STB?"), "SRE:", self.inst.ask("*SRE?"), "\n",\
               "ESE:", self.inst.ask("*ESE?"), "ESR:", self.inst.ask("*ESR?"), "\n",\
               "OPC:", self.inst.ask("*OPC?"))

    def kwrite(self, cmd):
        """Write to instrument."""
        try:
            assert type(cmd) == str
            self.inst.write(cmd)
        except AttributeError:
            print('ERROR: Could not write to the device.')

    def kread(self):
        """Read instrument."""
        try:
            r = self.inst.read()
            return r
        except AttributeError:
            print('ERROR: Could not read from device.')
            raise SystemExit

    def kwrun(self,cmd):
        self.kwrite(cmd)
        # time.sleep(0.5)
        self.kwrite('mm.run()')
        return self.kread()

    def set_V(self,V):
        self.kwrite(str('Vg='+str(V)))

    def format(self,n):
        a = '%E' % n
        return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

    def DataSave(self, data):
        """  Save RAW data and dataframe data to another file"""
        if self.if_verbose: print(data.replace(self.TAGS_Header, ""))
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

    def loadTSP(self, script_name, param=''):
        """Load an anonymous TSP script into the K2636 nonvolatile memory."""
        print("Loading: ", script_name)
        try:
            self.kwrite('ABORT')
            self.kwrite('loadscript')
            self.kwrite(param)

            for line in open(str("TSP//" + script_name), mode='r'): self.kwrite(line)

            self.kwrite('print("' + str(self.TAGS_END) + '")')
            self.kwrite('endscript')

        except AttributeError:
            print('ERROR: Could not load tsp script.')
            raise SystemExit

    def runTSP_oled(self, fn="test"):
        """ process all incoming data from K2636B   """
        try:
            if self.if_plot_figure:
                self.pl = OLED_Plot(fn)
                time.sleep(1)

            a  = []

            Vstep  = 0.1
            Vstart = 0
            Vstop  = 1
            V      = Vstart
            RRUN=True

            V_todo = [float(Vstart)]
            pts = range(1, int(abs((float(Vstop) - float(Vstart)) / float(Vstep)) + 1))
            for x in pts: V_todo.append(round(V_todo[x - 1] + float(Vstep), 4))
            if True:
                V_todo.append(Vstop)
                for x in pts: V_todo.append(round(V_todo[len(pts) + x] - float(Vstep), 4))

            first=True
            for V in V_todo:
            # while RRUN:
                if first:
                    self.kwrite('script.anonymous.run()')
                    InComingData = self.kread()
                    first=False
                else:
                    InComingData = self.kwrun(str('Vg='+str(V)))
                    InComminLuxx = self.lux.Lux_Get()

                if self.TAGS_END in InComingData: break
                if self.if_abort : break

                if self.if_plot_figure and (not self.TAGS_Header in InComingData ) :
                    dp = np.array([abs(float(InComingData.split()[0])),\
                                   abs(float(InComingData.split()[1])),\
                                   abs(float(InComminLuxx))])
                    self.pl.plot(dp)

                if self.TAGS_Header in InComingData:
                    InComingData += " \t " + str("lux")         + \
                                    " \t " + str("CurrC oeff.") + \
                                    " \t " + str("CurrA/m^-2.") + \
                                    " \t " + str("lux/m^-1")
                else:
                    CurrM2    = float(InComingData.split()[1])/OLEDarea
                    LummM2    = float(InComminLuxx) / OLEDarea
                    CurrCoeff = ((float(InComminLuxx) / float(InComingData.split()[1])))

                    CurrM2    = self.format(CurrM2)
                    LummM2    = self.format(LummM2)
                    CurrCoeff = self.format(CurrCoeff)

                    InComingData += " \t " + str(InComminLuxx) + \
                                    " \t " + str(CurrCoeff)    + \
                                    " \t " + str(CurrM2)       + \
                                    " \t " + str(LummM2)

                self.DataSave(InComingData)
                a.append(InComingData.replace(self.TAGS_Header, "").split())

            self.kwrite('exit.run()')

            dd = pd.DataFrame(a)                            # a array is converted to the DataFrame
            df = pd.DataFrame()                             # new empty Data Frame is created
            df = pd.concat([df, dd], axis=1, sort=False)    # i donth ahve any idea why but it works
            self.DataSave(df)                               # save final data file
            self.DataSave("DATA: " +str(fn))                # and at the end add data file to the raw file

            if self.if_plot_figure:
                self.pl.plot(finished=True)
                cv2.destroyAllWindows()
            if self.if_abort : self.abort()

        except AttributeError:
            print('ERROR: Some ERROR in runTSP function')
            raise SystemExit

    def runTSP_oled_LTP(self, fn="test",lpp=50):
        """ process all incoming data form K2636B   """
        try:
            if self.if_plot_figure:
                self.pl = OLED_Plot(fn)
                time.sleep(1)

            self.kwrite('script.anonymous.run()')

            a  = []
            LuxTh=-1
            while True:
                InComingData = self.kread()
                InComminLuxx = self.lux.Lux_Get()

                if self.TAGS_END in InComingData: break

                if LuxTh < 0  and (not self.TAGS_Header in InComingData ) :
                    InComminLuxx = self.lux.Lux_Get()
                    LuxTh = float(InComminLuxx)

                if self.if_plot_figure and (not self.TAGS_Header in InComingData ) :
                    dp = np.array([float(InComingData.split()[0]),\
                                   float(InComingData.split()[1]),\
                                   float(InComminLuxx)])
                    self.pl.plot(dp)

                if self.TAGS_Header in InComingData:
                    InComingData += " \t " + str("lux"        ) + " \t "\
                                           + str("CurrCoeff." ) + " \t "\
                                           + str("CurrA/m^-2.") + " \t "\
                                           + str("lux/m^-2"   ) + " \t "\
                                           + str("%lux/m^-2"   )
                else:
                    CurrM2    = float(InComingData.split()[1])/OLEDarea
                    LummM2    = float(InComminLuxx) / OLEDarea
                    CurrCoeff = ((float(InComminLuxx) / float(InComingData.split()[1])))
                    # llux      = 100*float(InComminLuxx)/LuxTh
                    # llux=round(llux,3)
                    # # if llux < lpp:
                    #     self.abort()
                    #     break
                    CurrM2    = self.format(CurrM2)
                    LummM2    = self.format(LummM2)
                    CurrCoeff = self.format(CurrCoeff)
                    llux      = self.format(llux)

                    InComingData += " \t " + str(InComminLuxx) + \
                                    " \t " + str(CurrCoeff)    + \
                                    " \t " + str(CurrM2)       + \
                                    " \t " + str(LummM2)       + \
                                    " \t " + str(llux)

                self.DataSave(InComingData)

                InComingData = InComingData.replace(self.TAGS_Header, "")
                a.append(InComingData.split())
                if self.if_abort: break

            dd = pd.DataFrame(a)                            # a array is converted to the DataFrame
            df = pd.DataFrame()                             # new empty Data Frame is created
            df = pd.concat([df, dd], axis=1, sort=False)    # i donth ahve any idea why but it works
            self.DataSave(df)                               # save final data file
            self.DataSave("DATA: " +str(fn))                # and at the end add data file to the raw file

            if self.if_plot_figure:
                self.pl.plot(finished=True)
                cv2.destroyAllWindows()
            if self.if_abort : self.abort()

        except AttributeError:
            print('ERROR: Some ERROR in runTSP function')
            raise SystemExit

    def oled(self, param):
        """K2636 Transfer sweeps."""
        try:
            print("++++++++++++++++++++++++++++++++++++++ OLED TEST")
            time_start = time.time()

            param_tsp=""
            for i in param.keys():
                param_tsp+=str(i)+" = "+str(param[i])+" \n"

            file_name = str(str(param["FName"]) + '_oled.txt')
            file_name = self.check_file_name(file_name)

            self.loadTSP('k2636b_oled_sweep_init.tsp', param_tsp)

            self.runTSP_oled(file_name)
            # self.stats(file_name)

            time_end = time.time()
            print("Time: " + str(round((time_end - time_start), 2))+"sec.")
            return 0

        except(AttributeError):
            print('Cannot perform output sweep: no keithley connected. Problem in oled subrutine.')

    def oled_ltp(self, *param):
        try:
            print("++++++++++++++++++++++++++++++++++++++ OLED LIFE TIME TEST")
            begin_time = time.time()

            cmd =   "OLED_V  = " + str(float(param[1])) + "\n" \
                    "OLED_dT = " + str(float(param[2])) + "\n" \
                    "DELATE  = " + str(float(param[4])) + "\n" \
                    "NPLC    = " + str(float(param[5])) + "\n" \
                    "BLIMIT_V    = 15    \n" \
                    "BLIMIT_I    = 100e-3 \n" \
                    "BALIMIT_R   = 10e-3 \n"

            file_name = str(str(param[0]) + '_oled_ltp.txt')
            file_name = self.check_file_name(file_name)

            self.loadTSP('k2636b_oled_ltp.tsp', cmd)

            self.runTSP_oled_LTP(file_name,float(param[3]))
            # self.stats(file_name)

            finish_time = time.time()
            print("Time: " + str(round((finish_time - begin_time), 2))+"sec.")
            return 0

        except(AttributeError):
            print('Cannot perform output sweep: no keithley connected.')


# ================================================================
# ============================= MAIN =============================
# ================================================================
if __name__ == '__main__':
    args = oled_help.help()

    try:
        keithley = k2636b()
    except usb.core.USBError:
        print("some errors")
        sys.exit()


    oo=config_import()
    oled_param = dict(V_Start = 0, \
                      V_Stop  = 10, \
                      V_Step  = 1, \
                      DELATE  = 1, \
                      NPLC    = 1, \
                      LIMIT_V = 15, \
                      LIMIT_I = 1, \
                      LIMIT_R = 1, \
                      RANGE_I = 1,\

                      SWEEP = False)

    for i in oled_param.keys():
        oled_param[i]=oo.get_param("OLED", i)


    if args.fig:      k2636b.if_plot_figure = False
    if args.filename: FILE_NAME = args.filename

    if args.oled:
        # ------- TRANSFER: parametry pomiaru
        FName   = FILE_NAME
        oled_param["FName"]   = FILE_NAME
        oled_param["V_Start"] = args.oled[0][0]
        oled_param["V_Stop"]  = args.oled[0][1]
        oled_param["V_Step"]  = args.oled[0][2]
        oled_param["V_Start"] = args.oled[0][0]
        oled_param["NPLC"]    = args.NPLC
        oled_param["COMP"]    = args.DCOMP
        # oled_param["DELATE"]  = args.DEL
        oled_param["SWEEP"]   = args.sweep

        keithley.oled(oled_param)
    #
    # elif args.ltp:
    #     param_ltp=[FILE_NAME ,args.ltp[0][0],args.ltp[0][1],args.ltp[0][2],args.DEL,args.NPLC]
    #     print("LTP",param_ltp)
    #     keithley.oled_ltp(*param_ltp)

    else:
        keithley.info()


    keithley.CloseConnect()
