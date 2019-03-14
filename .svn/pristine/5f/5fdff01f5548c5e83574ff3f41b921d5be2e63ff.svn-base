# -*- coding:utf-8 -*-
import time
from zs_backend.sql import SqlOperate
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require, md5, rand
from flask import render_template, request, jsonify, session
from zs_backend.utils import time_util
from zs_backend.utils import httpc_util
from zs_backend.utils.const import *
from zs_backend import redis_conn
from zs_backend.utils.log_table import *
from zs_backend.utils.common import rand

def gen_order_no(channel):
    key = "%s_%s" % (WITHDRAW_ORDER_TABLE, channel)
    count = redis_conn.incrby(key)
    if count >= 90000000:
        redis_conn.set(key, 0)
    datestr = time_util.formatTimeWithDesc(time_util.now_sec(), "%y%m%d%H%M%S")
    orderno = "%s_%s%08d%03d" % (channel, datestr, count, rand(1, 999))

    return orderno