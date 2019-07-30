#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
======================
Multiprocess plotting
======================

Demo of using multiprocessing for generating data in one process and
plotting in another.

Written by Robert Cimrman
"""

import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import numpy as np
import os
import random

class ProcessPlotter(object):
    def __init__(self,fname):
        self.x = []
        self.y1 = []
        self.y2 = []

        if isinstance(fname, list):
            self.fname        = fname[0]
            self.xlabel  = fname[1]
            self.y1label = fname[2]
            self.y2label = fname[3]
            self.title   = fname[4]
            self.xscale  = fname[5]
            self.y1scale = fname[6]
            self.y2scale = fname[7]
            self.type    = fname[8]
        else:
            self.fname   = fname
            self.xlabel  = "VGS [V] / Time [sec.]"
            self.y1label = "IDS [A]"
            self.y2label = "IGS [A]"
            self.title   = fname
            self.xscale  = "lin"
            self.y1scale = "log"
            self.y2scale = "log"
            self.type    = "typ"



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
                self.ax.plot(self.x, self.y1, 'ro',marker='o',color='b')
                self.bx.plot(self.x, self.y2, 'ro',marker='o',color='r')

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

class NBPlot(object):
    def __init__(self,fname):
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = ProcessPlotter(fname)
        self.plot_process = mp.Process( target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()

    def plot(self,data=np.array([0,0]), finished=False):
        send = self.plot_pipe.send
        if finished:
            send(None)
            time.sleep(0.5)
        else:
            send(data)


#======================================================
#======================================================
#======================================================
#======================================================


if __name__ == '__main__':

    # fn=["fname","X","Y1","Y2","TITLE","xxx","log","log","typ"]
    fn="asdasdas"
    pl = NBPlot(fn)
    x=0
    while x<=20:
        x+= 1
        y = random.randint(1,101)
        z = random.randint(1, 101)
        d = np.array([float(x), float(y), float(z)])
        pl.plot(d)

        time.sleep(0.5)
        print(isinstance(50, list))

