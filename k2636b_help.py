#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse


def help():
    parser = argparse.ArgumentParser(description='~~~~~~~~~~~~~~~~~ ELECTRIZED GIWAXS ~~~~~~~~~~~~~~~~')

    parser.add_argument('-t',
                        dest='trans',
                        action='append',
                        nargs=4,
                        metavar=('VDS', 'VGS_START', 'VGS_STOP', 'VGS_DELTA '),
                        help='help: TRANSFER test')

    parser.add_argument('-i',
                        dest='iv',
                        action='append',
                        nargs=3,
                        metavar=('START', 'STOP', 'STEP'),
                        help='help: iv-sweep test')

    parser.add_argument('-o',
                        dest="out",
                        action='append',
                        nargs=6,
                        metavar=('VDS_START', 'VDS_STOP', 'VDS_DELAT', 'VGS_START', 'VGS_STOP', 'VGS_DELTA '),
                        help='help: OUTPUT test')

    parser.add_argument('-c',
                        dest="ttime",
                        action='append',
                        nargs=4,
                        metavar=('VDS', 'VGS', 'Tstep', 'Tperiod'),
                        help='help: time test')

    parser.add_argument('-f',
                        dest="filename",
                        help='Output file name',
                        default="tr00")

    parser.add_argument('--NPLC',
                        type=float,
                        help='help: NPLC [1]  Fast: 0.1 Normal 1 Slow: 10',
                        default=1.0)

    parser.add_argument('--bar',
                        action='store_true',
                        help="show progress bar")

    parser.add_argument('--fig',
                        help="show dat graph",
                        action='store_false')

    parser.add_argument('--DEL',
                        type=int,
                        help='help: DEL  [0s] - wait before measurements [seconds]',
                        default=0.05)

    parser.add_argument('--DCOMP',
                        type=float,
                        help='help: VDS Comp',
                        default=0.001)

    parser.add_argument('--GCOMP',
                        type=float,
                        help='help: VGS Comp',
                        default=0.001)

    parser.add_argument('--sweep',
                        help='help: wait n sec before mesure current',
                        dest="sweep",
                        default="true")

    return parser.parse_args()
