#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
from PyQt4 import QtGui
from PyQt4.QtGui import QAction, QWidget, QVBoxLayout, QMenuBar, QLabel
from qtutil import App, MainWindow, createAction
from pmp import GanttWidget, GanttPrintHandler
from pmp import config
from pmp.settings import APPLICATION_NAME, Settings, settings, dlgSpecs
from pmp.projectinfodialog import ProjectInfoDialog
from pmp.evmdialog import EvmDialog
from pmp.optiondialog import OptionDialog

class GanttMainWindow(MainWindow):
    def __init__(self, parent=None):
        path = "settings.ini"
        self._printHandler = None
        try:
            _settings = Settings.load(path)
        except Exception as e:
            logging.warning("couldn't load '%s'" % path)
            logging.debug(e)
            _settings = None
        if _settings is not None:
            settings.merge(_settings)
        super(GanttMainWindow, self).__init__(parent, APPLICATION_NAME)
        if _settings is None:
            self.information("% kann nicht gelesen werden(;_;)" % path)

    def setup_gui(self):
        super(GanttMainWindow, self).setup_gui()
        #-- GUI部品の作成
        self.ganttWidget = GanttWidget()
        self.main_frame = QWidget()
        #-- GUI部品のレイアウト
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.ganttWidget)
        main_layout.addWidget(self.ganttWidget.getChartScrollBar())
        self.main_frame.setLayout(main_layout)
        self.setCentralWidget(self.main_frame)
        self.statusBar().showMessage('Ready')
        #-- メニュー／アクションの作成
        self.createActions()
        self.createMenus()
        #-- other(シグナル/スロットの接続とか)
        self.ganttWidget.currentFileChanged.connect(self._currentFileChanged)
        self.resize(1024, 768)
        if config.lastUsed() != '':
            self.ganttWidget.load(config.lastUsed())

    def _currentFileChanged(self, newFileName):
        self.setWindowTitle(newFileName)

    def createActions(self):
        super(GanttMainWindow, self).createActions()
        def dummy(action):
            logging.debug("Action(%s)" % action.text())
        gw = self.ganttWidget
        self.actions.open = createAction(gw.open, 'Open', "Ctrl+O")
        self.actions.openServer = createAction(gw.openServer, 'open server', "Ctrl+A")
        self.actions.save = createAction(gw.save, 'save', "Ctrl+S")
        self.actions.saveAs = createAction(gw.saveAs, 'save as')
        self.actions.insert = createAction(gw.insert, 'insert', "Ctrl+Insert")
        self.actions.remove = createAction(gw.remove, 'remove', "Ctrl+Delete")
        self.actions.levelUp = createAction(gw.levelUp, 'level up', "Ctrl+Left")
        self.actions.levelDown = createAction(gw.levelDown, 'level down', "Ctrl+Right")
        self.actions.up = createAction(gw.up, 'up', "Ctrl+Up")
        self.actions.down = createAction(gw.down, 'down', "Ctrl+Down")
        self.actions.setSelectModeRow = createAction(self.setSelectModeRow, 'select rows', "Ctrl+1")
        self.actions.setSelectModeCell = createAction(self.setSelectModeCell, 'select cells', "Ctrl+2")
        self.actions.copy = createAction(gw.copy, 'copy', "Ctrl+C")
        self.actions.paste = createAction(gw.paste, 'paste', "Ctrl+V")
        self.actions.day = createAction(gw.timescaleDay, '1 Tag', "Ctrl+D")
        self.actions.week = createAction(gw.timescaleWeek, '1 Woche', "Ctrl+W")
        self.actions.month = createAction(gw.timescaleMonth, '1 Monat', "Ctrl+M")
        self.actions.projectInfo = createAction(self.setProjectInfo, 'project info', "Alt+P")
        self.actions.setOptions = createAction(self.setOptions, "Optionen", "Alt+O")
        self.actions.evm = createAction(self.showEVM, "evm anzeigen")

    def createMenus(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addAction(self.actions.open)
        fileMenu.addAction(self.actions.openServer)
        fileMenu.addAction(self.actions.save)
        fileMenu.addAction(self.actions.saveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actions.print)
        fileMenu.addAction(self.actions.preview)
        fileMenu.addAction(self.actions.pageSettings)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actions.quit)
        editMenu = menuBar.addMenu("Edit")
        editMenu.addAction(self.actions.copy)
        editMenu.addAction(self.actions.paste)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.insert)
        editMenu.addAction(self.actions.remove)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.up)
        editMenu.addAction(self.actions.down)
        editMenu.addAction(self.actions.levelUp)
        editMenu.addAction(self.actions.levelDown)
        timescaleMenu = menuBar.addMenu("Zeitskala")
        timescaleMenu.addAction(self.actions.day)
        timescaleMenu.addAction(self.actions.week)
        timescaleMenu.addAction(self.actions.month)
        selectionModeMenu = menuBar.addMenu("Auswahlmodus")
        selectionModeMenu.addAction(self.actions.setSelectModeRow)
        selectionModeMenu.addAction(self.actions.setSelectModeCell)
        configMenu = menuBar.addMenu("Config")
        configMenu.addAction(self.actions.projectInfo)
        configMenu.addAction(self.actions.setOptions)
        miscMenu = menuBar.addMenu("other")
        miscMenu.addAction(self.actions.evm)
        miscMenu.addAction(self.actions.aboutQt)
        miscMenu.addAction(self.actions.about)

    def printhandler(self):
        if self._printHandler is None:
            self._printHandler = GanttPrintHandler(self.ganttWidget)
        return self._printHandler

    #---------------------------------------------------------------------------
    #   アクション
    #---------------------------------------------------------------------------
    def setProjectInfo(self):
        ProjectInfoDialog(APPLICATION_NAME, self).exec_()

    def setOptions(self):
        OptionDialog.createModal(self.ganttWidget, self).exec_()

    def setSelectModeRow(self):
        self.ganttWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ganttWidget.refresh()

    def setSelectModeCell(self):
        self.ganttWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.ganttWidget.refresh()

    def showEVM(self):
        EvmDialog(APPLICATION_NAME, self).exec_()

def exec():
    logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M:%S',
                filename='~pmp.log',
                )
    logging.info('START')
    app = App()
    app.exec(GanttMainWindow)
    Settings.dump(settings, "settings.ini")
    logging.info('END')
    logging.shutdown()

if __name__ == '__main__':
    exec()
