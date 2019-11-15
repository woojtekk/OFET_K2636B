# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import random
import time



### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="PyOLED") # creates a window
p = win.addPlot(title="___ File Name ___")  # creates empty space for the plot in the window

curve = p.plot()                        # create an empty "plot" (a curve to plot)


windowWidth = 500                       # width of the window displaying the curve
Xm = []
Ym = []
ptr = 0                     # set first x position

# Realtime data plot. Each time this function is called, the data display is updated
def update(x,y):
    global curve, ptr, Xm    
    Xm.append(x)
    Ym.append(y)
    curve.setData(Xm,Ym)                     # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
x=0
while True:
    y = random.random()
    update(x,y)
    x+= random.random()
    time.sleep(0.51)
    if x>=5: break



### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################