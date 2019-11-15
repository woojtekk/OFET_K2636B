#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse


def help():
    parser = argparse.ArgumentParser(description='~~~~~~~~~~~~~~~~~ ELECTRIZED GIWAXS ~~~~~~~~~~~~~~~~')


    parser.add_argument('-l',
                        dest='oled',
                        action='append',
                        nargs=3,
                        metavar=('V_start', 'V_stop', 'V_delta '),
                        help='help: oled test')


    parser.add_argument('-lt',
                        # dest="life_time",
                        action='append',
                        nargs=3,
                        metavar=(' V', 'Time_step', 'Time_period'),
                        help='help: life time measurements')

    parser.add_argument('-ltp',
                        # dest="life_time_p",
                        action='append',
                        nargs=3,
                        metavar=('V', 'Time_step', 'LTPercent'),
                        help='help: life time measurements e.g.: LT90')

    parser.add_argument('-f',
                        dest="filename",
                        help='Output file name',
                        default="OLED_00")

    parser.add_argument('--fig',
                        help="show dat graph",
                        action='store_false')

    parser.add_argument('--NPLC',
                        type=float,
                        help='help: NPLC [1]  Fast: 0.1 Normal 1 Slow: 10',
                        default=1.0)

    parser.add_argument('--DEL',
                        type=int,
                        help='help: DEL  [0s] - wait before measurements [seconds]',
                        default=1)

    parser.add_argument('--DCOMP',
                        type=float,
                        help='help: VDS Comp',
                        default=0.001)

    parser.add_argument('--sweep',
                        help='help: wait n sec before mesure current',
                        dest="sweep",
                        default="False")

    return parser.parse_args()
