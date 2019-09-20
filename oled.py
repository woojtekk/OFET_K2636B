#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import usb
import sys
import os
import k2636b_help
import signal
import usbtmc
import serial
import time
import datetime
import pandas as pd




FILE_NAME = "TR_TEST"
# DEV_ADDRESS = 'ASRL/dev/ttyUSB0'
DEV_ADDRESS = 'ASRL/dev/ttyUSB0::INSTR'
#DEV_ADDRESS = '/dev/usbtmc0'


class luxmeter():
    def __init__(self):
        self.NoLUX = False
        try:
            self.ser = serial.Serial("/dev/ttyACM0")
            time.sleep(1)
            self.Lux_Get()

        except serial.serialutil.SerialException:
            print("INIT luxmeter ....  Dev. not connected",)
            self.NoLUX = True

    def Lux_Get(self):
        if self.NoLUX: return 0.0

        txt = ""
        self.ser.flushInput()
        while True:
            c = str(self.ser.read(), "utf-8")
            if c == '\n' or c == '\r': break
            txt += c

        txt = txt.strip("\r\n")

        try:
            txt = txt.split("/")[0] + "." + txt.split("/")[1]
        except IndexError:
            # print("::IE::",txt)
            # self.Lux_Get()
            return 0.0

        try:
            return float(txt)
        except ValueError:
            # print("::VE::", txt)
            # self.rr()
            return 0.0

        return float(txt.strip("\r\n"))

class k2636b():
    data_path = str(os.path.dirname(os.path.realpath(__file__)) + "/data/")

    if_camera = False
    if_verbose = True
    if_plot_figure = True

    TAGS_Header = ">>head<<"
    TAGS_END = ">>END<<"

    def handler(self, signum, frame):
        print("\n")
        print("========================================")
        print("========== Forever is over! ============")
        print("========================================")
        print("=============== ABORT! =================")
        print("========================================")

        self.kwrite('ABORT')
        self.kwrite('loadscript')
        self.kwrite('beeper.beep(0.2, 800)')
        self.kwrite('beeper.beep(0.1, 850)')
        self.kwrite('print("' + str(self.TAGS_END) + '")')
        self.kwrite('reset()')
        self.kwrite('endscript')

        self.kwrite('script.anonymous.run()')

    def __init__(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.signal(signal.SIGINT, self.handler)
        """ connect2 if you are using usb connection via usbtcm   """
        self.Dev_Init()
        self.lux = luxmeter()

    def Dev_Init(self):
        try:
            self.inst = usbtmc.Instrument(0x05e6, 0x2636)
            self.inst.write("*CLS")
        except usbtmc.usbtmc.UsbtmcException:
            print('Cannot open Device Port.')
            sys.exit()
            return 0

    def CloseConnect(self):
        """Close connection to keithley."""


    def info(self):
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
            print('ERROR: Could not find tsp script. Check path.')
            raise SystemExit

    def runTSP_oled(self, fn="test"):
        """ process all incoming data form K2636B   """

        try:
            if self.if_plot_figure:
                self.pl = plot.NBPlot(fn)
                time.sleep(1)

            self.kwrite('script.anonymous.run()')

            a = []
            df = pd.DataFrame()

            while True:
                txt = self.kread()
                llux = self.lux.Lux_Get()

                if self.TAGS_END in txt: break
                if self.TAGS_Header in txt:
                    dd = pd.DataFrame(a)
                    df = pd.concat([df, dd], axis=1, sort=False)
                    a.clear()
                elif self.if_plot_figure:
                    dp = np.array([float(txt.split()[0]), float(txt.split()[1]), float(llux)])
                    self.pl.plot(dp)

                if self.TAGS_Header in txt:
                    txt += " \t " + str("lux") + " \t " + str("CurrCoeff.")
                else:
                    CurrCoeff = 0.01 * (float(llux) / float(txt.split()[1]))
                    CurrCoeff = round(CurrCoeff, 3)
                    txt += " \t " + str(llux) + "\t" + str(CurrCoeff)

                self.DataSave(fn, txt)

                txt = txt.replace(self.TAGS_Header, "")
                a.append(txt.split())

            dd = pd.DataFrame(a)
            df = pd.concat([df, dd], axis=1, sort=False)
            self.DataSave(fn, df)

            print("DATA File: ", fn)
            if self.if_plot_figure:
                self.pl.plot(finished=True)
            if self.if_plot_figure:
                cv2.destroyAllWindows()


        except AttributeError:
            print('ERROR: some error in runTSP function')
            raise SystemExit

    def DataSave(self, fn, data):
        """  Save RAW data and dataframe data to another file"""
        if self.if_verbose: print(data)
        if isinstance(data, pd.DataFrame):
            data.to_csv(fn, sep=' ', encoding='utf-8', index=False, header=None)
        else:
            with open(str(fn + "_raw.txt"), 'a') as the_file: \
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

        return filename

    # ------------- oled
    def oled(self, *param):
        """K2636 Transfer sweeps."""
        print(param)
        try:
            print("++++++++++++++++++++++++++++++++++++++")
            self.if_camera = False
            begin_time = time.time()
            # (OLED_VStart), (OLED_VEnd), (OLED_VStep)
            # [FName, VGS_start, VGS_stop, VGS_step, VDS_comp, VGS_comp, NPLC, DEL, SWEEP]
            if param[8]: ss = "true"
            sample = param[0]
            cmd = "OLED_VStart = " + str(float(param[1])) + "\n" \
                                                            "OLED_VEnd   = " + str(float(param[2])) + "\n" \
                                                                                                      "OLED_VStep  = " + str(
                float(param[3])) + "\n" \
                                   "SWEEP    = " + "True" + "\n" \
                                                            "NPLC     = " + str(float(param[6])) + "\n" \
                                                                                                   "DELATE   = " + str(
                float(2)) + "\n"

            file_name = str(sample + '_oled.txt')
            file_name = self.check_file_name(file_name)

            self.loadTSP('k2636b_oled_sweep.tsp', cmd)

            self.runTSP_oled(file_name)
            # self.stats(file_name)

            finish_time = time.time()
            print('OLED characteristic complete. [%.2f] sec.' % ((finish_time - begin_time)))

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
        print("++")
    except usb.core.USBError:
        print("some errors")
        sys.exit()

    if args.fig: k2636b.if_plot_figure = False

    if args.filename != "tr00": FILE_NAME = args.filename

    if args.oled:
        print(args.oled)
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
