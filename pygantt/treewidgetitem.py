#! python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QModelIndex
from .util import s2dt, dt2s
from .settings import *

class TreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, task=None):
        super(TreeWidgetItem, self).__init__()
        if task is not None:
            self.taskToItem(task)

    def taskToItem(self, task):
        self.name = task.name
        self.start = dt2s(task.start)
        self.end = dt2s(task.end)
        self.setText(COLUMN_ASIGNEE, "unknown")
        self.pv = str(task.pv)
        self.ev = str(task.ev)
        self.task = task
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        if task.children is not None and len(task.children) > 0:
            self.addChildren(TreeWidgetItem.Items(task.children))

    def dataChanged2(self, column):
        task = self.task
        if column == COLUMN_NAME:
            task.name = item.name
        elif column == COLUMN_START:
            task.start = s2dt(self.start)
        elif column == COLUMN_END:
            task.end = s2dt(self.end)
        elif column == COLUMN_PV:
            task.pv = int(self.pv)
        elif column == COLUMN_EV:
            task.ev = int(self.ev)

    def childItems(self):
        items = []
        for i in range(self.childCount()):
            items.append(self.child(i))
        return items

    def itemProperty(func):
        """デコレータ"""
        pass

    @property
    def task(self):
        return self.data(COLUMN_CHART, Qt.UserRole)

    @task.setter
    def task(self, value):
        self.setData(COLUMN_CHART, Qt.UserRole, value)

    @property
    def name(self):
        return self.data(COLUMN_NAME, Qt.DisplayRole)

    @name.setter
    def name(self, value):
        self.setData(COLUMN_NAME, Qt.DisplayRole, value)

    @property
    def start(self):
        return self.data(COLUMN_START, Qt.DisplayRole)

    @start.setter
    def start(self, value):
        self.setData(COLUMN_START, Qt.DisplayRole, value)

    @property
    def end(self):
        return self.data(COLUMN_END, Qt.DisplayRole)

    @end.setter
    def end(self, value):
        self.setData(COLUMN_END, Qt.DisplayRole, value)

    @property
    def pv(self):
        return self.data(COLUMN_PV, Qt.DisplayRole)

    @pv.setter
    def pv(self, value):
        self.setData(COLUMN_PV, Qt.DisplayRole, value)

    @property
    def ev(self):
        return self.data(COLUMN_EV, Qt.DisplayRole)

    @ev.setter
    def ev(self, value):
        self.setData(COLUMN_EV, Qt.DisplayRole, value)

    @staticmethod
    def Items(tasks):
        return [TreeWidgetItem(tasks[i]) for i in range(0, len(tasks))]