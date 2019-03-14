# -*- coding:utf-8 -*-

from flask.globals import session
import pymysql
from zs_backend.utils import httpc_util
from zs_backend.utils.const import *
from zs_backend import redis_conn

class Qry(object):
    def __init__(self, Cfgline):
        self.DB = {}
        for v in Cfgline.split(","):
            vv = v.split("=")
            self.DB[vv[0].strip()] = vv[1].strip()

    def qry(self, sql):
        # 链接数据库
        conn = pymysql.connect(host=self.DB["host"], user=self.DB["user"],
                               passwd=self.DB["passwd"], db=self.DB["db"], charset='utf8', connect_timeout=3)
        cursor = conn.cursor()
        cursor.execute(sql)
        L = cursor.fetchall()
        cursor.close()
        conn.close()

        return L

    def execute(self, sql):
        # 链接数据库
        conn = pymysql.connect(host=self.DB["host"], user=self.DB["user"],
                               passwd=self.DB["passwd"], db=self.DB["db"], charset='utf8', connect_timeout=3)
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

class LogQry(Qry):
    def __init__(self, ChannelID = None, **kwargs):
        if kwargs.has_key("name") and kwargs["name"]:
            db_str = redis_conn.hget(CHANNEL_CONFIG_TABLE+kwargs["name"], "game_log_db")
        else:
            db_str = redis_conn.hget(CHANNEL_CONFIG_TABLE+str(ChannelID), "game_log_db")
        
        if not db_str:
            print "LogQry err...", ChannelID, kwargs
        return Qry.__init__(self, db_str)

class GameWeb(object):
    def __init__(self, ChannelID = None, **kwargs):
        if kwargs.has_key("name") and kwargs["name"]:
            self.web_site = redis_conn.hget(CHANNEL_CONFIG_TABLE+kwargs["name"], "web_url")
        else:
            self.web_site = redis_conn.hget(CHANNEL_CONFIG_TABLE+str(ChannelID), "web_url")

    def get(self, url, data):
        r = httpc_util.get(self.web_site + url, data, ctype = "json")
        return r

    def post(self, url, data):
        r = httpc_util.post(self.web_site + url, data, ctype = "json")
        return r
