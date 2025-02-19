# -*- coding:utf-8 -*-
from config import Config

# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import md5
from . import api
from zs_backend.utils.const import *
from zs_backend.utils import httpc_util
import time
from functools import wraps
from zs_backend import redis_conn
from zs_backend.utils.channel_qry import GameWeb
import json

## 获取各种用于api服的渠道数据
@api.route("/sync_channel_data", methods=['GET', 'POST'])
def get_channel_data():
    rr = httpc_util.post(Config.ADMIN_WEB_SITE+"/api/channel_data", {})
    rr = rr.json()
    for dd in rr["data"]:
        channel = dd["name"]
        channel_id = dd["id"]
        redis_conn.hmset(CHANNEL_CONFIG_TABLE+channel, dd)
        redis_conn.hmset(CHANNEL_CONFIG_TABLE+str(channel_id), dd)
        try:
            redis_conn.hset(WX_CONFIG_TABLE, dd["wx_appid"], dd["wx_token"])
        except:
            pass
        try:
            redis_conn.hset(WX_CONFIG_TABLE, dd["h5_wx_appid"], dd["h5_wx_token"])
        except:
            pass

    return jsonify()
