#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  sys
from Meter import  Meter
from PyQt4 import  QtGui, QtCore


"""fun to read cpu info """
try:
    import psutil
    def currentCPU(time):
        return psutil.cpu_percent(time)
except ImportError:
    print "no moudle named psutil"
class CPUMeter(Meter):
    def __init__(self,parent=None):
        super(CPUMeter,self).__init__()
        self.logo = "CPU"
    def updateValue(self):
        self.value = currentCPU(0)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = CPUMeter()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
