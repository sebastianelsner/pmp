#! python3
# -*- coding: utf-8 -*-

import json, codecs
from logging import getLogger
from datetime import date, datetime
from qtutil import Namespace
from qtutil import Property as _P
from .serialize import to_json, from_json
from PyQt4.QtGui import QPen, QColor, QBrush

logger = getLogger('settings')

class Settings(Namespace):
    KEY2IDX = ['name', 'start', 'end', 'pic', 'pv', 'ev', 'chart']

    def applyTo(self, ganttWidget):
        ganttWidget.pen4progressLine = QPen(self.color.progressLine)
        ganttWidget.pen4chartBoundary = QPen(self.color.boundary)
        ganttWidget.brush4chartFill = QBrush(self.color.chart)
        ganttWidget.brush4chartFillProgress = QBrush(self.color.progress)
        ganttWidget.brush4progress = QBrush(self.color.progress)
        ganttWidget.dateOfProgressLine = self.misc.DATE_OF_PROGRESS_LINE
        self._columnResize(ganttWidget, COLUMN_NAME)
        self._columnResize(ganttWidget, COLUMN_START)
        self._columnResize(ganttWidget, COLUMN_END)
        self._columnResize(ganttWidget, COLUMN_PIC)
        self._columnResize(ganttWidget, COLUMN_PV)
        self._columnResize(ganttWidget, COLUMN_EV)
        self._columnResize(ganttWidget, COLUMN_CHART)

    def getColumn(self, column):
        return settings.column[self._keyFromColumnIndex(column)]

    def getHeaderWidth(self):
        w = 0
        for i in range(COLUMN_CHART):
            c = self.getColumn(i)
            if c.visible:
                w += c.width
        return w

    def _columnIndexFromKey(self, key):
        for i in len(self.KEY2IDX):
            if key == self.KEY2IDX[i]:
                return i
        return -1

    def _keyFromColumnIndex(self, columnIndex):
        return self.KEY2IDX[columnIndex]

    def _columnResize(self, ganttWidget, columnIndex):
        obj = settings.column[self.KEY2IDX[columnIndex]]
        ganttWidget.header().resizeSection(columnIndex, obj.width)
        ganttWidget.setColumnHidden(columnIndex, not obj.visible)

    @staticmethod
    def dump(obj, path):
        logger.info("start:dump(%s):" % path)
        with codecs.open(path, 'w', 'utf8') as f:
            #return
            json.dump(obj, f, indent=2, default=to_json, ensure_ascii=False)
        logger.info("end  :dump(%s):" % path)

    @staticmethod
    def load(path):
        logger.info("start:load(%s):" % path)
        with open(path, mode='r', encoding='utf-8') as f:
            rslt = json.load(f, object_hook=from_json)
            logger.info("end  :load(%s):" % path)
            return rslt


settings = Settings()

#-------------------------------------------------------------------------------
#全般／共通項目
#-------------------------------------------------------------------------------
DEBUG=True
APPLICATION_NAME = "PMP(Poor Man's ms-Projcect)"

#-------------------------------------------------------------------------------
#データ部(画面左側)の表示諸元
#-------------------------------------------------------------------------------
HEADER_LABELS = ["Artikelname","Startdatum","Schlussdatum","Verantwortliche", "PV", "EV", ""]

COLUMN_NAME     = 0
COLUMN_START    = 1
COLUMN_END      = 2
COLUMN_PIC      = 3
COLUMN_PV       = 4
COLUMN_EV       = 5
COLUMN_CHART    = 6


#-------------------------------------------------------------------------------
#ヘッダ部(画面右上、カレンダ)の表示諸元
#-------------------------------------------------------------------------------

HEADER_HEIGHT   = 60

#カレンダ部のY座標を示す添字
CALENDAR = Namespace()
CALENDAR.YEAR   = 0
CALENDAR.MONTH  = 1
CALENDAR.WEEK   = 2
CALENDAR.DAY    = 3
CALENDAR.BOTTOM = 4

#1日の表示幅
TIMESCALE_DAY = Namespace()
TIMESCALE_DAY.WIDTH = 24.0
TIMESCALE_DAY.YEAR = True
TIMESCALE_DAY.MONTH = True
TIMESCALE_DAY.WEEK = False
TIMESCALE_DAY.DAY = True
TIMESCALE_DAY.CHART = CALENDAR.DAY

TIMESCALE_WEEK = Namespace()
TIMESCALE_WEEK.WIDTH = 8.0
TIMESCALE_WEEK.YEAR = True
TIMESCALE_WEEK.MONTH = True
TIMESCALE_WEEK.WEEK = True
TIMESCALE_WEEK.DAY = False
TIMESCALE_WEEK.CHART = CALENDAR.WEEK

TIMESCALE_MONTH = Namespace()
TIMESCALE_MONTH.WIDTH = 3.0
TIMESCALE_MONTH.YEAR = True
TIMESCALE_MONTH.MONTH = True
TIMESCALE_MONTH.WEEK = True
TIMESCALE_MONTH.DAY = False
TIMESCALE_MONTH.CHART = CALENDAR.WEEK

#ヘッダ部のテキスト描画の際のマージン
CALENDAR_BOTTOM_MARGIN = 3
CALENDAR_LEFT_MARGIN = 0 #未使用。一律センタリング


#-------------------------------------------------------------------------------
#chart部(画面右下)の表示諸元
#-------------------------------------------------------------------------------

#ガントchartの行高さ
ROW_HEIGHT = 20

#ガントchartの線1本の高さ(行高さではない)
CHART_HEIGHT = 10

#ガントchart内のprogressの線1本の高さ
PROGRESST_HEIGHT = 6

CHART_BOUNDARY_COLOR    = (128,128,128,128) #chartframe色
CHART_COLOR             = ( 64,128,128,128) #chart塗潰し色
PROGRESS_COLOR          = (160, 64, 64,255) #chart内のprogress塗潰し色
AGGREGATED_TASK_COLOR   = ( 64,128,255,128) #chart塗潰し色
PROGRESS_LINE_COLOR     = (255,  0,  0,255) #progressLine色

#-------------------------------------------------------------------------------
#Leuchtfarbe
#-------------------------------------------------------------------------------
settings.color.boundary       = QColor(128,128,128,128) #chartframe色
settings.color.chart          = QColor( 64,128,128,128) #chart塗潰し色
settings.color.progress       = QColor(160, 64, 64,255) #chart内のprogress塗潰し色
settings.color.progress = QColor( 64,128,255,128) #chart塗潰し色
settings.color.progressLine   = QColor(255,  0,  0,255) #progressLine色

#-------------------------------------------------------------------------------
#列:幅、表示/非表示
#-------------------------------------------------------------------------------
settings.column.name.visible    = True
settings.column.name.width      = 360
settings.column.start.visible   = True
settings.column.start.width     = 80
settings.column.end.visible     = True
settings.column.end.width       = 80
settings.column.pic.visible     = True
settings.column.pic.width       = 80
settings.column.pv.visible      = True
settings.column.pv.width        = 40
settings.column.ev.visible      = True
settings.column.ev.width        = 40
settings.column.chart.visible   = True
settings.column.chart.width     = 600

#-------------------------------------------------------------------------------
#drucken諸元
#-------------------------------------------------------------------------------
settings.print.HORIZONTAL_PAGE_COUNT    = 1     #horizontalpagecount
settings.print.ROWS_PER_PAGE            = 70    #rowsperpage
settings.print.HEADER_HEIGHT_RATIO      = 0.10  #headerheightratio(=ヘッダ高さ/ページ高さ)
settings.print.HEADER_WIDTH_RATIO       = 0.25  #headerwidthratio(=ヘッダ幅/ページ高さ)

#-------------------------------------------------------------------------------
#otherの諸元
#-------------------------------------------------------------------------------
settings.misc.DATE_OF_PROGRESS_LINE = date.today()
settings.server.url = ''
settings.server.userid = ''
settings.server.password = ''

#-------------------------------------------------------------------------------
#Optionenダイアログ表示
#-------------------------------------------------------------------------------
dlgSpecs = [
    ['Leuchtfarbe',
        _P('frame', QColor, 'color.boundary', QColor(128,128,128,128)),
        _P('chart', QColor, 'color.chart', QColor( 64,128,128,128)),
        _P('progress', QColor, 'color.progress', QColor(160, 64, 64,255)),
        _P('aggregatedTask', QColor, 'color.aggregatedTask', QColor( 64,128,255,128)),
        _P('progressLine', QColor, 'color.progressLine', QColor( 64,128,128,255)),
    ],
    ['drucken',
        _P('headerwidthratio', float, 'print.HEADER_WIDTH_RATIO', 0.25),
        _P('headerheightratio', float, 'print.HEADER_HEIGHT_RATIO', 0.10),
        _P('rowsperpage', int, 'print.ROWS_PER_PAGE', 70),
        _P('horizontalpagecount', int, 'print.HORIZONTAL_PAGE_COUNT', 1),
    ],
    ['columndisplay',
        #"startvisible","endvisible","picvisible", "PV", "EV"
        _P('namevisible', bool, 'column.name.visible',True),
        _P('startvisible', bool, 'column.start.visible',True),
        _P('endvisible', bool, 'column.end.visible',  True),
        _P('picvisible', bool, 'column.pic.visible',  True),
        _P('PV',     bool, 'column.pv.visible',   True),
        _P('EV',     bool, 'column.ev.visible',   True),
        _P('chart',bool, 'column.chart.visible',   True),
    ],
    ['server',
        _P('URL', ｓｔｒ, 'server.url', ''),
        _P('userid', ｓｔｒ, 'server.userid', ''),
        _P('password', ｓｔｒ, 'server.password', ''),
    ],
    ['other',
        _P('progressLineDate', date, 'misc.DATE_OF_PROGRESS_LINE', date.today()),
    ],
]