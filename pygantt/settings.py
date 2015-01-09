#! python3
# -*- coding: utf-8 -*-

from argparse import Namespace

settings = Namespace()

#-------------------------------------------------------------------------------
#全般／共通項目
#-------------------------------------------------------------------------------
DEBUG=True

#-------------------------------------------------------------------------------
#データ部(画面左側)の表示諸元
#-------------------------------------------------------------------------------
COLUMN_NAME  = 0 #未使用
COLUMN_CHART = 4


#-------------------------------------------------------------------------------
#ヘッダ部(画面右上、カレンダ)の表示諸元
#-------------------------------------------------------------------------------

#カレンダ部のY座標を示す添字
CALENDAR = Namespace()
CALENDAR.YEAR   = 0
CALENDAR.MONTH  = 1
CALENDAR.DAY    = 2
CALENDAR.BOTTOM = 3

#1日の表示幅
TIMESCALE_DAY = Namespace()
TIMESCALE_DAY.WIDTH = 30.0
TIMESCALE_DAY.YEAR = True
TIMESCALE_DAY.MONTH = True
TIMESCALE_DAY.DAY = True
TIMESCALE_DAY.CHART = CALENDAR.DAY

TIMESCALE_WEEK = Namespace()
TIMESCALE_WEEK.WIDTH = 21.0/7.0
TIMESCALE_WEEK.YEAR = True
TIMESCALE_WEEK.MONTH = True
TIMESCALE_WEEK.DAY = False
TIMESCALE_WEEK.CHART = CALENDAR.MONTH

TIMESCALE_MONTH = Namespace()
TIMESCALE_MONTH.WIDTH = 30.0/30.0
TIMESCALE_MONTH.YEAR = True
TIMESCALE_MONTH.MONTH = True
TIMESCALE_MONTH.DAY = False
TIMESCALE_MONTH.CHART = CALENDAR.MONTH

#ヘッダ部のテキスト描画の際のマージン
CALENDAR_BOTTOM_MARGIN = 3
CALENDAR_LEFT_MARGIN = 0 #未使用。一律センタリング


#-------------------------------------------------------------------------------
#チャート部(画面右下)の表示諸元
#-------------------------------------------------------------------------------

#ガントチャートの線1本の高さ(行高さではない)
CHART_HEIGHT = 10

#ガントチャート内の進捗率の線1本の高さ
PROGRESST_HEIGHT = 6




