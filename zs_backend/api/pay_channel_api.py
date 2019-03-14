# -*- coding:utf-8 -*-
from flask import render_template, jsonify, url_for
from flask.globals import session, request, g, current_app
from werkzeug.utils import redirect
import time
from zs_backend import SqlOperate
from zs_backend.api import api
from zs_backend.utils import erl
from zs_backend.utils.common import login_require
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
from zs_backend.utils.const import *
from zs_backend import redis_conn
from zs_backend.utils.common import md5, rand_list
import json
from zs_backend.utils.channel_qry import GameWeb, LogQry
import base64
import os
import urllib

STATUS_USE = 0  ## 状态 已使用
STATUS_NOUSE = 1  ## 状态 未使用

DECIMAL_OPEN = 0
DECIMAL_CLOSE = 1

@api.route('/player_pay_channel', methods=['POST', 'GET'])
def get_player_pay_channel():
    if request.method == 'POST':
        data = request.json
    else:
        data = request.args

    vip_lv = int(data.get("vip_lv"))
    channel = data.get("channel")

    ## 查询公司入款的配置
    bank = []
    wx = []
    zfb = []
    sql = '''
        select id, receipt_type, config, decimal_open, min_recharge, 
            max_recharge, player_lv, memo
        from admin_pay_channel
        where status = %d
    ''' % (STATUS_USE)
    for line in LogQry(name=channel).qry(sql):
        plv = [int(i) for i in line[6].strip().split(",")]
        if vip_lv in plv:
            cfg = {
                "id": line[0],
                "type": line[1],
                "config": line[2],
                "decimal_open": line[3],
                "min_recharge": line[4],
                "max_recharge": line[5],
                "memo": line[7],
                "pay_type": RECHARGE_PLAYER,
            }
            if line[1] == 0:
                bank.append(cfg)
            elif line[1] == 1:
                wx.append(cfg)
            elif line[1] == 3:
                zfb.append(cfg)

    ## 查询在线支付的配置
    wx_online = []
    zfb_online = []
    sql = '''
        select id, pay_type, single_minimum, single_highest, apply_level
        from admin_online_payment
        where status = %d
    ''' % (STATUS_USE)
    for line in LogQry(name=channel).qry(sql):
        if not line[4]:
            continue
        plv = [int(i) for i in line[4].strip().split(",")]
        if vip_lv in plv:
            cfg = {
                "id": line[0],
                "type": line[1],
                "min_recharge": line[2],
                "max_recharge": line[3],
                "pay_type": RECHARGE_ONLINE,
            }
            if line[1] in [1, 2]:
                wx_online.append(cfg)
            elif line[1] in [3, 4]:
                zfb_online.append(cfg)

    pay_load = {}
    ## 得到最终的支付方式
    if wx_online:
        pay_load["wx"] = rand_list(wx_online)
    elif wx:
        pay_load["wx"] = rand_list(wx)

    if zfb_online:
        pay_load["zfb"] = rand_list(zfb_online)
    elif zfb:
        pay_load["zfb"] = rand_list(zfb)

    if bank:
        pay_load["bank"] = rand_list(bank)

    ## 查询代理充值配置
    wxagent_l = []
    sql = '''
        select wx
        from admin_wx_agent
        where status = %d
        order by seq
    ''' % STATUS_USE
    for i in LogQry(name=channel).qry(sql):
        wxagent_l.append(i[0])
    pay_load["wx_agent"] = wxagent_l

    return jsonify(pay_load)
