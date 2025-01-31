# -*- coding:utf-8 -*-

from __future__ import division
import time
import json
from flask import render_template, jsonify
from flask.globals import session, request, current_app
from zs_backend import SqlOperate
from . import api
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require, rand, md5
from zs_backend.utils import time_util, html_translate, httpc_util
from zs_backend.utils.const import *
from zs_backend import redis_conn
from zs_backend.utils.recharge_util import gen_order_no, do_add_order_menual

@api.route('/do_pay', methods=['GET'])
def do_pay_for_game():
    ## 玩家ID
    player_id = int(request.args.get('pid'))
    # 接收渠道
    channel_name = request.args.get('channel')
    ## 支付通道
    pay_channel = int(request.args.get('pay_channel'))
    ## 充值金币
    money = int(request.args.get('money'))
    ## 充值时间 时间戳
    request_time = time_util.now_sec()
    ## 转账人姓名
    payname = request.args.get('p_name', "")
    if not payname:
        payname = ""
    ## 备注
    memo = ""

    ## 查询渠道ID
    channel = int(redis_conn.hget(CHANNEL_CONFIG_TABLE + channel_name, "id"))

    ## 生成本次订单编号
    orderno = gen_order_no(channel, pay_channel)

    return do_add_order_menual(channel, orderno, player_id, pay_channel,
                               money, request_time, memo, 0, pay_name = payname)

## 客户端充值
@api.route('/pre_create_order', methods=['POST'])
@httpc_util.check_param(ctype="s2s", debug=True)
def pay_order():
    data = request.form

    ## 玩家ID
    player_id = int(data.get('player_id'))
    # 接收渠道id
    channel = int(data.get('channel'))
    ## 支付通道
    pay_channel = int(data.get('pay_channel'))
    ## 充值金币
    money = int(data.get('money'))
    ## 充值时间 时间戳
    request_time = int(data.get('time'))
    ## 备注
    memo = data.get('memo', '')

    ## 查询该支付通道配置信息
    sql = '''
        select api_url, merchant_code, md5_key, public_key, private_key,
            api_id, api_code, pay_type
        from admin_online_payment
        where id = %d
        and channel_id = %d
    ''' % (pay_channel, channel)
    api_url, mch_id, mch_key, public_key, private_key, \
    api_id, api_code, pay_type = LogQry(channel).qry(sql)[0]

    ## 生成本次订单编号
    orderno = gen_order_no(channel, pay_channel)

    ## 查询玩家等级
    sql = '''
        select vip, level, if(device = "ios", 2, 1)
        from player
        where id = %d
    ''' % player_id
    vip, lv, os = LogQry(channel).qry(sql)[0]

    sql = '''
        insert into admin_recharge
            (time, pid, os, channel, vip, 
            lv, orderno, platformno, coin, cost,
            rechargeid, state, `type`, pay_type, pay_channel,
            request_pid, review_time, review_pid, memo)
        values 
            (%d, %d, %d, %d, %d,
            %d, '%s', "", 0, %d,
            0, %d, %d, %d, %d,
            0, 0, 0, '%s')
    ''' % (request_time, player_id, os, channel, vip,
           lv, orderno, money,
           PAY_STATE_WAIT, RECHARGE_ONLINE, 0, pay_channel,
           memo)

    LogQry(channel).execute(sql)

    pay_load = {
        "appid": api_id,
        "orderno": orderno,
        "mch_id": mch_id,
        "mch_key": mch_key,
        "public_key": public_key,
        "private_key": private_key,
        "url": api_url,
        "api_code": api_code,
        "pay_type": pay_type,
    }
    return jsonify(result="ok", data=pay_load)

## 查询最近10条充值
@api.route('/api/recharge_list', methods=['GET'])
def api_recharge_list():
    # 接收渠道
    channel_name = request.args.get('channel')
    pid = request.args.get('pid')
    ## 查询渠道ID
    channel = int(redis_conn.hget(CHANNEL_CONFIG_TABLE + channel_name, "id"))

    datas = []
    sql = '''
        select time, orderno, cost, state
        from admin_recharge
        where pid = %s
        order by time desc
        limit 10
    ''' % (pid)
    for time, orderno, cost, state in LogQry(channel).qry(sql):
        datas.append({
            "time":time,
            "orderno":orderno,
            "cost":cost,
            "state":state,
            })

    return jsonify(result="succ", datas= datas)
