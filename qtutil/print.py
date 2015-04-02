#! python3
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

class PrintHandler(object):
    def printer(self):
        """printerオブジェクトを取得する。派生クラスでオーバライド"""
        return QtGui.QPrinter()

    def pageCount(self):
        """druckenページ数の取得。派生クラスでオーバライド"""
        return 3

    def print(self, printer):
        """drucken用の描画処理"""
        def within(fromPage, toPage, currentPage):
            if fromPage == 0 and toPage == 0:
                return True
            if fromPage <= currentPage and currentPage <= toPage:
                return True
            return False

        fromPage = printer.fromPage()
        toPage = printer.toPage()
        painter = QtGui.QPainter(printer)
        self.preparePrint(printer)
        painter.begin(printer)
        firstPage = True
        pageCount = self.pageCount()
        for i in range(1, pageCount+1):
            if not within(fromPage, toPage, i):
                continue
            if not firstPage:
                printer.newPage()
            self.printPage(painter, i, pageCount)
            firstPage = False
        painter.end()

    def preparePrint(self, printer):
        """druckenの前準備。派生クラスでオーバライド"""
        pass

    def pageSetting(self):
        printer = self.printer()
        dialog = QtGui.QPageSetupDialog(printer)
        dialog.exec()

    def printPage(self, painter, pageNo, pageCount):
        """drucken用のページ描画処理。派生クラスでオーバライド"""
        painter.save()
        rect = painter.viewport()
        side = min(rect.width(), rect.height())
        painter.setViewport((rect.width() - side) / 2, (rect.height() - side) / 2, side, side)
        painter.setWindow(-50, -50, 100, 100)
        #----
        if pageNo > 1:
            painter.drawRect(-49,-49,98,98)
            if pageNo > 2 and pageNo < 5:
                painter.drawEllipse(QtCore.QPoint(0,0),49,49)
        painter.restore()

    def printAction(self):
        printer = self.printer()
        dialog = QtGui.QPrintDialog(printer)
        if dialog.exec():
            self.print(printer)

    def createPreviewDialog(self, printer):
        return QtGui.QPrintPreviewDialog(printer)

    def printPreview(self):
        printer = self.printer()
        preview = self.createPreviewDialog(printer)
        preview.paintRequested.connect(self.print)
        preview.exec()
