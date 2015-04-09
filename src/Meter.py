#!/usr/bin/python
#coding=utf-8
import sys
from math import  sin, cos
from PyQt4 import  QtGui, QtCore  
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QColor 
from PyQt4.QtGui import QPolygon
from PyQt4.QtCore import QString


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Meter(QtGui.QWidget):
    """
    a PyQt instance of QtMeter from Qt example code
    """
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.value = 0
        self.minValue = 0
        self.maxValue = 100
        self.logo = ""
        self.scaleMajor = 10
        self.scaleMijor = 10
        self.startAngle = 60
        self.endAngle = 60
        self.crownColor = Qt.blue
        self.foreground = Qt.green
        self.background = Qt.black
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.resize(200,200)
    def updateValue(self):
        pass
    def paintEvent(self,QPaintEvent):

        self.updateValue()
        self.side  = min(self.width(),self.height())
        self.painter = QPainter()
        self.painter.begin(self)
        #self.painter.setRenderHint(QPainter.Antialiasing) 
        self.painter.translate(self.width()/2,self.height()/2)
        self.painter.scale(self.side / 200.0, self.side / 200.0)
        self.painter.setPen(Qt.NoPen)

        self.drawCrown()
        self.drawBackgroud()
        self.drawLogo()
        self.drawScale()
        self.drawScaleNum()
        self.drawNumbericValue()
        self.drawPointer()
        self.painter.end()
        
    def setValue(self,updatefun):
        self.value = updatefun()
    def setLogo(self,logo):
        self.logo = logo
    def drawCrown(self):
        self.painter.save()
        self.painter.setPen(QtGui.QPen(self.crownColor, 3))
        self.painter.drawEllipse(-92, -92, 184, 184)
        self.painter.restore()
    def drawBackgroud(self):
        self.painter.save()
        self.painter.setBrush(self.background)
        self.painter.drawEllipse(-92, -92, 184, 184)
        self.painter.restore()
    def drawScale(self):
        self.painter.save()
        self.painter.rotate(self.startAngle)
        self.painter.setPen(self.foreground)
        steps = self.scaleMajor * self.scaleMijor
        angleStep = (360.0 - self.startAngle - self.endAngle) /steps
        pen = QtGui.QPen(self.painter.pen())

        for i in xrange(steps+1):
            if i % self.scaleMajor == 0:
                pen.setWidth(1)
                self.painter.setPen(pen)
                self.painter.drawLine(0, 62, 0, 72)
            else:
                pen.setWidth(0)
                self.painter.setPen(pen)
                self.painter.drawLine(0, 62, 0, 65)
            self.painter.rotate(angleStep)
        self.painter.restore()
    def drawScaleNum(self):
        self.painter.save()
        self.painter.setPen(self.foreground)
        startRad = (360 - self.startAngle - 90) * (3.14 / 180)
        deltaRad = (360 - self.startAngle - self.endAngle) * (3.14 / 180) / self.scaleMajor
        fm = QtGui.QFontMetricsF(self.font())

        for i in xrange(self.scaleMajor+1):
            sina = sin(startRad - i * deltaRad)
            cosa = cos(startRad - i * deltaRad)

            tmpVal = 1.0 * i *((self.maxValue - self.minValue) / self.scaleMajor) + self.minValue

            numstr = QString( "%1" ).arg(tmpVal)
            w = fm.size(Qt.TextSingleLine,numstr).width()
            h = fm.size(Qt.TextSingleLine,numstr).height()
            x = 82 * cosa - w / 2
            y = -82 * sina + h / 4
            self.painter.drawText(x, y, numstr)
        self.painter.restore()
    def drawLogo(self):
        self.painter.save()
        self.painter.setPen(self.foreground)
        self.painter.setBrush(self.foreground)
        logostr = QString(self.logo)
        fm = QtGui.QFontMetricsF(self.font())
        w = fm.size(Qt.TextSingleLine,logostr).width()
        self.painter.drawText(-w / 2, -30, logostr)
        self.painter.restore()
    def drawNumbericValue(self):
        self.painter.save()
        color = QtGui.QColor(150, 150, 200)
        pen = self.painter.pen()
        pen.setWidth(3)
        self.painter.setPen(pen)
        self.painter.setPen(color)
        self.painter.drawRect(-30, 30, 60, 14)
        
        cpustr  =  QString("%1").arg(self.value)
        fm = QtGui.QFontMetricsF(self.font())
        w = fm.size(Qt.TextSingleLine,cpustr).width()
        self.painter.setPen(self.foreground)
        self.painter.drawText(-w / 2, 42, cpustr)
        self.painter.restore()
    def drawPointer(self):
        self.painter.save()
        self.pointerHand=QPolygon([-2,0, 2,0, 0,60])
        self.pointerColor = QColor(127 , 0, 127)
        self.painter.setBrush(self.pointerColor)

        self.painter.rotate(self.startAngle)
        degRotate = (360.0 - self.startAngle - self.endAngle)/(self.maxValue - self.minValue)*(self.value - self.minValue)
        self.painter.rotate(degRotate)
        self.painter.drawConvexPolygon(self.pointerHand)
        self.painter.restore()
        

