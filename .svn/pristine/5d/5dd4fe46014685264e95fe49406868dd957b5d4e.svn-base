# /usr/bin/env python
# encoding: UTF-8

import pymysql
import time
import traceback
from datetime import datetime

## 执行单条sql
def sql_execute(cursor, sql):
    cursor.execute(sql)

def do_stats(func):
    def _wrapper(Db, min_date_stamp, max_date_stamp, **kargs):
        HOST = "localhost"
        DBUSER = "root"
        DBPASSWD = "123456"

        if kargs.has_key("host"):
            HOST = kargs["host"]
        if kargs.has_key("user"):
            DBUSER = kargs["user"]
        if kargs.has_key("passwd"):
            DBPASSWD = kargs["passwd"]

        ## 链接数据库
        conn = pymysql.connect(host=HOST, user=DBUSER, passwd=DBPASSWD, db=Db, charset='utf8')
        cursor = conn.cursor()

        try:
            func(Db, min_date_stamp, max_date_stamp, cursor=cursor)
            ## 提交
            sql_execute(cursor, "commit")
        except:
            print traceback.format_exc()
        finally:
            cursor.close()
            conn.close()

    return _wrapper

## 获取前一个小时的时间戳
def get_pre_1_hour_stamp():
    H = int(time.strftime('%H', time.localtime(time.time())))
    Today = today0()

    Begin = Today + (H - 1) * 3600
    End = Today + H * 3600 - 1

    return Begin, End

## 获取前0.5小时的时间戳
def get_pre_30_min_stamp():
    H = int(time.strftime('%H', time.localtime(time.time())))
    Min = int(time.strftime('%M', time.localtime(time.time())))

    Today = today0()

    Begin = Today + H * 3600
    End = Begin + 1800

    if Min < 30:
        Begin -= 1800
        End -= 1800

    print "Begin,End:", Begin, End
    return Begin, End

## 获取数据库单条结果
def fetchone(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchone()


## 一次性获取数据库结果
def fetchall(cursor, sql):
    cursor.execute(sql)
    return cursor.fetchall()


## 分批次获取结果，并执行外部函数
def fetchmany(cursor, sql, F):
    cursor.execute(sql)
    result = cursor.fetchmany()
    while result:
        for row in result:
            F(row)
        result = cursor.fetchmany()


## 批量执行更新函数
def sql_executemany(cursor, sql, TupleListValues):
    cursor.executemany(sql, TupleListValues)


## 今天零点
def today0():
    tt = datetime.now().timetuple()
    unix_ts = time.mktime(tt)
    return int(unix_ts - tt.tm_hour * 60 * 60 - tt.tm_min * 60 - tt.tm_sec)
    
def get_table_log_coin(Time):
    return "log_coin_%s" % time.strftime("%Y_%W", time.localtime(Time))

def get_table_log_subgame(Time):
    return "log_subgame_%s" % time.strftime("%Y_%W", time.localtime(Time))

def get_table_log_player_subgame(Time):
    return "log_player_subgame_%s" % time.strftime("%Y_%W", time.localtime(Time))