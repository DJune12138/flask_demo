# -*- coding:utf-8 -*-
import time
from zs_backend.sql import SqlOperate
from . import api
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require, md5, rand
from flask import render_template, request, jsonify, session
from zs_backend.utils import time_util, withdraw_util
from zs_backend.utils import httpc_util, game_util
from zs_backend.utils.const import *
from zs_backend import redis_conn
from zs_backend.utils.log_table import *

# 状态映射
STATUS_SUCC = 1
STATUS_FAIL = 2
STATUS_REVIEW = 3
STATUS_LOCK = 4
status_map = {1: '成功', 2: '失败', 3: '待审'}

# 提款类型映射
WITHDRAW_TYPE_BANK = 0  ## 银行卡
WITHDRAW_TYPE_ZFB = 1 ## 支付宝

# 状态参数
succeed = 1
fail = 2
waiting_audit = 3

## 默认流水要求倍数 
DEFAULT_STAKE_RATE = 2

@api.route('/withdraw_pre', methods=['POST'])
@httpc_util.check_param(ctype="s2s", debug=True)
def withdraw_pre():
    data = request.json

    pid = int(data.get("pid"))
    channel_name = data.get("channel")
    money = int(data.get("money"))
    withdraw_type = int(data.get("type"))

    channel = int(redis_conn.hget(CHANNEL_CONFIG_TABLE + channel_name, "id"))

    ## 查询玩家层级 
    ## tod 绑定银行卡信息
    sql = '''
        select vip, counter
        from player
        where id = %d
    ''' % pid
    vip, counter = LogQry(channel).qry(sql)[0]
    if withdraw_type == WITHDRAW_TYPE_BANK:
        bank, bank_acc, bank_accname, bank_addr = game_util.get_bank_info(counter)
    elif withdraw_type == WITHDRAW_TYPE_ZFB:
        bank = ""
        bank_addr = ""
        bank_acc, bank_accname = game_util.get_zfb_info(counter)

    ## 生成本次订单号
    orderno = withdraw_util.gen_order_no(channel)

    ## 插入数据
    sql = '''
        insert into admin_withdraw 
            (
            pid, member_level, withdraw_deposit_id, withdraw_deposit_type, withdraw_deposit_money,
            application_time, service_charge, platform_withhold, status, dispose_time,
            dispose_user, remark, payee, due_bank, gathering_account,
            open_account_address, failed_reason, channel_id
            )
        values 
            (
            %d, %d, '%s', %d, %d,
            %d, %d, %d, %d, %d,
            %d, '%s', '%s', '%s', '%s',
            '%s', '%s', %d
            )
    ''' % (
        pid, vip, orderno, withdraw_type, money,
        time_util.now_sec(), 0, 0, STATUS_REVIEW, 0,
        0, "", bank_accname, bank, bank_acc,
        bank_addr, "", channel
    )

    print sql
    LogQry(channel).execute(sql)

    return jsonify(result="ok")

## 查询最近10条提现
@api.route('/api/withdraw_list', methods=['GET'])
def api_withdraw_list():
    # 接收渠道
    channel_name = request.args.get('channel')
    pid = request.args.get('pid')
    ## 查询渠道ID
    channel = int(redis_conn.hget(CHANNEL_CONFIG_TABLE + channel_name, "id"))

    datas = []
    sql = '''
        select application_time, withdraw_deposit_money, status
        from admin_withdraw
        where pid = %s
        order by application_time desc
        limit 10
    ''' % (pid)
    for time, money, status in LogQry(channel).qry(sql):
        datas.append({
            "time":time,
            "money":money,
            "status":status,
            })

    return jsonify(result="succ", datas= datas)