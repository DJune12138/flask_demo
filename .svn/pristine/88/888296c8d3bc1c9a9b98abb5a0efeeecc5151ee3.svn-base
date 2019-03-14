# -*- coding:utf-8 -*-
import time
from zs_backend.sql import SqlOperate
from zs_backend.busi import busi
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


@busi.route('/withdrawal/order/details', methods=['GET'])
@login_require
def withdrawal_order_details():
    """提现订单管理页面"""

    other_msg = dict()
    other_msg['channel_id'] = ''
    other_msg['player_id'] = ''
    other_msg['account'] = ''
    other_msg['others'] = [u'''<td>订单状态：
        <select id="status" name="status"> 
            <option value="0">全部</option> 
            <option value="1">成功</option> 
            <option value="2">失败</option> 
            <option value="3">待审</option> 
        </select>
    </td>''']

    return render_template('withdrawal_order.html', other_msg=other_msg)


@busi.route('/withdrawal/order/retrieve', methods=['GET'])
@login_require
def withdrawal_order_retrieve():
    """提现订单管理查询"""

    # 获取参数
    channel_id = session['select_channel']
    status = request.args.get('status')
    begin_time = request.args.get('beginDate')
    end_time = request.args.get('endDate')
    player_id = request.args.get('PlayerID')
    player_name = request.args.get('Account')

    # 校验参数
    if player_id:
        try:
            int(player_id)
        except ValueError as e:
            return jsonify(result=0, msg=u'玩家ID为整数纯数字！')
    if player_id and player_name:
        return jsonify(result=0, msg=u'玩家ID、玩家账号只能填其一！')

    # 处理数据
    begin_time = time_util.formatTimestamp(begin_time)
    end_time = time_util.formatTimestamp(end_time)
    player_id_str = ''
    if player_id:
        player_id_str = ' AND pid=%s' % player_id
    if player_name:
        retrieve_sql = """SELECT id 
                          FROM player 
                          WHERE account_id='%s';""" % player_name
        player_id = LogQry(int(channel_id)).qry(retrieve_sql)[0][0]
        player_id_str = ' AND pid=%s' % player_id
    type_str = ''
    status_str = ''
    if status != '0':
        status_str = ' AND status=%s' % status

    ## 查询操作员
    sql = 'select id, name from user'
    user_dict = {0: ""}
    for k, v in SqlOperate().select(sql):
        user_dict[k] = v

    # 从数据库获取数据
    retrieve_sql = """
        SELECT pid,withdraw_deposit_id,withdraw_deposit_type,withdraw_deposit_money,application_time,
            service_charge,platform_withhold,status,dispose_time,remark,
            payee,due_bank,gathering_account,open_account_address,failed_reason,
            id,(select member_level_name from admin_member_level where id=member_level),
                dispose_user,(select nick from player where id=pid)
        FROM admin_withdraw 
        WHERE application_time>%s 
        AND application_time<%s
        %s%s%s
        ORDER BY status DESC,application_time DESC;
    """ % (begin_time, end_time, player_id_str, type_str, status_str)
    datas = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    datas_list = list()
    for pid, withdraw_deposit_id, withdraw_deposit_type, withdraw_deposit_money, application_time, \
        service_charge, platform_withhold, status, dispose_time, remark, \
        payee, due_bank, gathering_account, open_account_address, failed_reason, \
        order_id, level_name, dispose_user, nick in datas:
        # 整理数据为字典
        data_dict = dict()
        data_dict['pid'] = pid
        data_dict['nick'] = nick
        data_dict['member_level'] = level_name
        data_dict['withdraw_deposit_id'] = withdraw_deposit_id
        data_dict['withdraw_deposit_type'] = withdraw_deposit_type
        data_dict['withdraw_deposit_money'] = withdraw_deposit_money
        data_dict['application_time'] = application_time
        data_dict['service_charge'] = service_charge
        data_dict['platform_withhold'] = platform_withhold
        data_dict['status'] = status_map[status]
        data_dict['dispose_time'] = dispose_time if dispose_time else 0
        data_dict['dispose_user'] = user_dict[dispose_user]
        data_dict['remark'] = remark
        data_dict['payee'] = payee
        data_dict['due_bank'] = due_bank
        data_dict['gathering_account'] = gathering_account
        data_dict['open_account_address'] = open_account_address
        data_dict['failed_reason'] = failed_reason
        data_dict['order_id'] = order_id
        datas_list.append(data_dict)

    # 返回数据
    return jsonify(result=1, datas=datas_list)


@busi.route('/withdrawal/order/update', methods=['PUT'])
@login_require
def withdrawal_order_update():
    """提现订单管理更新"""

    # 获取参数
    order_id = request.form.get('order_id')
    status = int(request.form.get('status'))
    failed_reason = request.form.get('failed_reason')
    remark = request.form.get('remark')
    platform_withhold = request.form.get('platform_withhold')
    service_charge = request.form.get('service_charge')

    ## 查询订单
    sql = '''
        select pid, withdraw_deposit_money 
        from admin_withdraw 
        where id = %s and 
        (status = %d or (status = %d and dispose_user = %d))
    ''' % (order_id, STATUS_REVIEW, STATUS_LOCK, session['user_id'])
    data = LogQry(session['select_channel']).qry(sql)
    if len(data) != 1:
        return jsonify(result=0, msg=u'查询不到该订单或者已被锁定')

    money = data[0][1]
    pid = data[0][0]

    # 校验并处理参数
    if status == STATUS_SUCC:
        try:
            platform_withhold = int(float(platform_withhold) * 100)
            service_charge = int(float(service_charge) * 100)
        except ValueError as e:
            return jsonify(result=0, msg=u'手续费和平台扣款为数字，且最多两位！')

    # 修改数据库中数据
    if status == STATUS_SUCC:
        update_sql = """
            UPDATE admin_withdraw 
            SET status=%d,platform_withhold=%s,service_charge=%s,remark='%s',dispose_time=%s,
                dispose_user='%s' 
            WHERE id=%s;
        """ % (status, platform_withhold, service_charge, remark, int(time.time()),
               session.get('user_id'), order_id)
        LogQry(session['select_channel']).execute(update_sql)
        pay_load = {
            "pid": pid,
            "money": money,
            "type": COIN_CHANGE_WITHDRAW_SUCC,
            "remark": remark,
        }
        GameWeb(session['select_channel']).post("/api/set_player_coin", pay_load)
    elif status == STATUS_FAIL:
        update_sql = """
            UPDATE admin_withdraw 
            SET status=%d,failed_reason='%s',remark='%s',dispose_time=%s,dispose_user='%s' 
            WHERE id=%s;
        """ % (status, failed_reason, remark, int(time.time()), session.get('user_id'), order_id)
        LogQry(session['select_channel']).execute(update_sql)
        pay_load = {
            "pid": pid,
            "money": money,
            "type": COIN_CHANGE_WITHDRAW_FAIL,
            "remark": failed_reason,
        }
        GameWeb(session['select_channel']).post("/api/set_player_coin", pay_load)

    # 返回应答
    return jsonify(result=1, msg=u'处理成功！')

@busi.route('/withdrawal/order/count', methods=['GET'])
@login_require
def withdrawal_order_count():
    """给首页返回待审核提现订单条数"""

    # 构造查询参数
    channel = session['select_channel']
    now_time = time_util.now_sec()
    seven_days_ago = now_time - 7 * 24 * 60 * 60

    # 查询数据库
    retrieve_sql = """SELECT count(1)
                      FROM admin_withdraw
                      WHERE application_time>=%s
                      AND application_time<=%s
                      AND status=%s;""" \
                   % (seven_days_ago, now_time, waiting_audit)
    data = LogQry(channel).qry(retrieve_sql)

    # 处理数据
    count = data[0][0]

    # 查询一分钟以内是否有新订单
    one_min_ago = now_time - 60
    retrieve_sql = """SELECT count(1)
                      FROM admin_withdraw
                      WHERE application_time>=%s
                      AND application_time<=%s
                      AND status=%s;""" \
                   % (one_min_ago, now_time, PAY_STATE_REVIEW)
    data = LogQry(channel).qry(retrieve_sql)[0][0]
    if data == 0:
        is_new = 0
    else:
        is_new = 1

    # 返回数据
    return jsonify(count=count, is_new=is_new)


@busi.route('/withdrawa/order/lock', methods=['GET'])
@login_require
def withdrawa_order_lock():
    orderid = request.args.get('orderid')
    channel = session['select_channel']

    sql = '''
        select count(1) from admin_withdraw where id = %s and status = %d
    ''' % (orderid, STATUS_REVIEW)
    count = LogQry(channel).qry(sql)[0][0]
    if count == 0:
        return jsonify(result="fail", msg=u'订单已被锁定或者订单不存在')

    sql = '''
        update admin_recharge
        set status = %d, dispose_user = %d, dispose_time = %d
        where id = %s and status = %d
    ''' % (STATUS_LOCK, session["user_id"], time_util.now_sec(), orderid, STATUS_REVIEW)

    return jsonify(result="ok")


## 计算提现所需流水
def get_least_stake_coin(channel, pid):
    ## 查询充值默认流水倍数
    sql = 'select val from admin_system_parameter where name = "need_water"'
    r = LogQry(channel).qry(sql)
    if len(r) > 0:
        Defualt_rate = float(r[0][0])
    else:
        Defualt_rate = DEFAULT_STAKE_RATE

    ## 上次提现到本次提现过程中充值
    sql = '''
        select ifnull(sum(cost * if(rechargeid = 0, %d, (select journal_require from admin_recharge_discounts where id = rechargeid))), 0)
        from admin_recharge
        where pid = %d
        and state = %d
        and time >= (
            select ifnull(max(dispose_time), 0)
            from admin_withdraw
            where pid = %d
            and status = %d
        )
    ''' % (Defualt_rate, pid, PAY_STATE_SUCC, pid, STATUS_SUCC)
    need_stake_coin = int(LogQry(channel).qry(sql)[0][0])

    ## 查询从最后一次提现后的时间 
    sql = '''
        select ifnull(max(dispose_time), 0), (select reg_time from player where id = %d), 
            (select vip from player where id = %d)
        from admin_withdraw
        where pid = %d
    ''' % (pid, pid, pid)
    print sql
    last_withdraw_time, reg_time, vip = LogQry(channel).qry(sql)[0]

    ## 查询从最后一次提现到当前的所有流水
    _pre_time = max(last_withdraw_time, reg_time)
    _use_time = _pre_time
    last_table = get_table_log_player_subgame(time_util.now_sec())
    total_stake_coin = 0
    while True:
        _use_table = get_table_log_player_subgame(_use_time)
        sql = 'select ifnull(sum(stake_coin), 0) from %s where pid = %d and time >= %d' \
              % (_use_table, pid, _pre_time)
        total_stake_coin += int(LogQry(channel).qry(sql)[0][0])
        _use_time += (7 * 24 * 3600)
        if _use_table == last_table:
            break

    return need_stake_coin / 100, total_stake_coin


@busi.route('/withdraw/stake_coin', methods=['GET'])
@login_require
def withdraw_stake_coin():
    channel = session['select_channel']
    pid = int(request.args.get("pid"))

    need_stake_coin, total_stake_coin = get_least_stake_coin(channel, pid)

    return jsonify(need_stake_coin=need_stake_coin, total_stake_coin=total_stake_coin)
