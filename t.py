# -*- coding: utf-8 -*-
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

pg.mkQApp()

pw = pg.PlotWidget()
pw.show()
pw.setWindowTitle('PyOLED')
p1 = pw.plotItem
p1.setTitle("___ File Name ___")
p1.setLabels(left='Current density / A/m^2')
# p1.setGrid()

## create a new ViewBox, link the right axis to its coordinate system
p2 = pg.ViewBox()
p1.showAxis('right')
p1.scene().addItem(p2)
p1.getAxis('right').linkToView(p2)
p2.setXLink(p1)

p1.getAxis('right').setLabel('Luminance / cd/m2 ', color='#0000ff')
p1.setLogMode(x=False, y=True)
## create third ViewBox.
## this time we need to create a new axis as well.
# p3 = pg.ViewBox()
# ax3 = pg.AxisItem('right')
# p1.layout.addItem(ax3, 2, 3)
# p1.scene().addItem(p3)
# ax3.linkToView(p3)
# p3.setXLink(p1)
# ax3.setZValue(-10000)
# ax3.setLabel('axis 3', color='#ff0000')


## Handle view resizing
def updateViews():
    ## view has resized; update auxiliary views to match
    global p1, p2, p3
    p2.setGeometry(p1.vb.sceneBoundingRect())
    # p3.setGeometry(p1.vb.sceneBoundingRect())

    ## need to re-update linked axes since this was called
    ## incorrectly while views had different shapes.
    ## (probably this should be handled in ViewBox.resizeEvent)
    p2.linkedViewChanged(p1.vb, p2.XAxis)
    # p3.linkedViewChanged(p1.vb, p3.XAxis)


updateViews()
p1.vb.sigResized.connect(updateViews)

p1.plot([0.1, 0.2, 0.4, 82, 136, 322])
p2.addItem(pg.PlotCurveItem([0.10, 20, 40, 80, 40, 20], pen='b'))
# p3.addItem(pg.PlotCurveItem([3200, 1600, 800, 400, 200, 100], pen='r'))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()