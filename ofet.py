#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import k2636b_help
from k2636b import k2636b

FILE_NAME = "TR_TEST"
# DEV_ADDRESS = 'ASRL/dev/ttyUSB0'
DEV_ADDRESS = 'ASRL/dev/ttyUSB0::INSTR'
#DEV_ADDRESS = '/dev/usbtmc0'


# ============================= MAIN

if __name__ == '__main__':
    args = k2636b_help.help()

    keithley = k2636b()

    if args.bar: k2636b.BAR = True
    if args.fig: k2636b.FIG = False

    if args.filename != "tr00": FILE_NAME = args.filename

    if args.trans:
        # ------- TRANSFER: parametry pomiaru
        FName = FILE_NAME
        VDS = args.trans[0][0]
        VGS_start = args.trans[0][1]
        VGS_stop = args.trans[0][2]
        VGS_step = args.trans[0][3]
        VDS_comp = args.DCOMP
        VGS_comp = args.GCOMP
        NPLC = args.NPLC
        PICNPLC = NPLC
        DEL = args.DEL
        SWEEP = True

        param_transfer = [FName, VDS, VGS_start, VGS_stop, VGS_step, VDS_comp, VGS_comp, NPLC, DEL, SWEEP]
        keithley.transfer(*param_transfer)

    if args.out:
        # ------- TRANSFER: parametry pomiaru

        # 'VDS_START','VDS_STOP','VDS_DELAT','VGS_START','VGS_STOP','VGS_DELTA'
        FName = FILE_NAME
        VDS_start = args.out[0][0]
        VDS_stop = args.out[0][1]
        VDS_step = args.out[0][2]
        VGS_start = args.out[0][3]
        VGS_stop = args.out[0][4]
        VGS_step = args.out[0][5]
        VDS_comp = args.DCOMP
        VGS_comp = args.GCOMP
        NPLC = args.NPLC
        PICNPLC = NPLC
        DEL = args.DEL
        SWEEP = True

        param_output = [FName, VDS_start, VDS_stop, VDS_step, VGS_start, VGS_stop, VGS_step, NPLC, DEL, SWEEP]
        keithley.output(*param_output)

    if args.ttime:
        param = [FILE_NAME, args.ttime[0][0], args.ttime[0][1], args.ttime[0][2], args.ttime[0][3]]
        keithley.czasowe(*param)

    if args.iv:
        param = [FILE_NAME, args.iv[0][0], args.iv[0][1], args.iv[0][2]]
        keithley.iv_sweep(*param)

    keithley.CloseConnect()
