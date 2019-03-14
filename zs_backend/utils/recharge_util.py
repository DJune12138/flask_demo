# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.utils.common import login_require
from flask import render_template, session, request, jsonify, g
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
import json
from zs_backend.utils.const import *
from zs_backend.utils.common import rand

def gen_order_no(channel, pay_channel):
    key = "%s_%s" % (PAY_ORDER_TABLE, channel)
    count = redis_conn.incrby(key)
    if count >= 90000:
        redis_conn.set(key, 0)
    datestr = time_util.formatTimeWithDesc(time_util.now_sec(), "%y%m%d%H%M%S")
    orderno = "%s_%s_%s%05d%03d" % (channel, pay_channel, datestr, count, rand(1, 999))

    return orderno

def do_add_order_menual(channel, orderno, player_id, pay_channel, money,
                        request_time, memo, request_pid, pay_name = ""):
    ## 查询玩家等级
    sql = '''
        select vip, level
        from player
        where id = %d
    ''' % player_id
    vip, lv = LogQry(channel).qry(sql)[0]

    ## 查询层级是否存在
    sql = 'select count(1) from admin_pay_channel where id = %d' % pay_channel
    if LogQry(channel).qry(sql)[0][0] != 1:
        return jsonify(result="fail", error_msg=u'支付通道不存在')

    sql = '''
        insert into admin_recharge
            (time, pid, os, channel, vip, 
            lv, orderno, platformno, coin, cost,
            rechargeid, state, type, pay_type, pay_channel,
            request_pid, review_time, review_pid, memo, pay_name)
        values 
            (%d, %d, 1, "", %d,
            %d, '%s', "", 0, %d,
            0, %d, %d, %d, %d,
            %d, 0, 0, '%s', '%s')
    ''' % (request_time, player_id, vip,
           lv, orderno, money,
           PAY_STATE_REVIEW, RECHARGE_TYPE_KF, 0, pay_channel,
           request_pid, memo, pay_name)
    LogQry(channel).execute(sql)

    return jsonify(result="ok", orderno=orderno)

def get_coin_recharge_discounts(channel, recharge, pid):
    ## 查询当前是否有优惠活动
    Now = time_util.now_sec()
    sql = '''
        select id, participation_member, participation_level, activity_type, recharge_detail,
                request_times, max_add_recharge
        from admin_recharge_discounts
        where begin_time <= %d and end_time >= %d
        and status = %d
    ''' % (Now, Now, pass_audit)
    data = LogQry(channel).qry(sql)
    if not data:
        return 0, 0, recharge * 100

    ## 查询该玩家的所属层级
    sql = 'select vip, total_recharge_rmb from player where id = %d' % pid
    vip, is_recharge = LogQry(channel).qry(sql)[0]
    is_recharge = is_recharge > 0

    ## 计算玩家当前参与过的充值优惠情况
    got_recharge_discount = {}
    sql = '''
        select rechargeid, sum(add_recharge), count(1)
        from admin_recharge
        where pid = %d
        group by rechargeid
    ''' % pid
    for i, k, v in LogQry(channel).qry(sql):
        got_recharge_discount[int(i)] = {
            "total": int(k),
            "times": int(v),
        }

    # 遍历各个优惠活动 查找给予玩家最大利益的优惠
    can_get_discounts = {}
    for aid, participation_member, participation_level, activity_type, recharge_detail, \
        request_times, max_add_recharge in data:
        ## 先判断可参与玩家 以及 参与层级
        ## 如果只是针对新玩家 但是又已经充值了 则忽略
        if participation_member == PARTICIPATION_TYPE_NEW and is_recharge:
            continue
        if participation_member == PARTICIPATION_TYPE_OLD and (not is_recharge):
            continue
        ## 判断最大赠送金额
        if not max_add_recharge:
            max_add_recharge = 999999999999999999
        if got_recharge_discount.has_key(aid) and got_recharge_discount[aid]["total"] >= max_add_recharge:
            continue
        ## 判断最大可申请次数
        if got_recharge_discount.has_key(aid) and got_recharge_discount[aid]["times"] >= request_times:
            continue
        ## 玩家层级不在此部分
        if str(vip) not in participation_level.split(","):
            continue
        ## 判断活动可赠送的金额数 
        recharge_detail = eval(recharge_detail)
        recharge_detail.sort(reverse=True)
        ## 剩余可赠送金额 单位分
        if got_recharge_discount.has_key(aid):
            rest_add_recharge = max_add_recharge - got_recharge_discount[aid]["total"]
        else:
            rest_add_recharge = max_add_recharge
        ## 固定金额
        if activity_type == ACTIVITY_TYPE_FIX:
            for min_recharge, add_recharge in recharge_detail:
                if recharge >= min_recharge:
                    can_get_discounts[aid] = min(add_recharge, rest_add_recharge)
                    break
        ## 百分比
        elif activity_type == ACTIVITY_TYPE_PERCENT:
            for min_recharge, add_percent in recharge_detail:
                if recharge >= min_recharge:
                    can_get_discounts[aid] = min(int(recharge * add_percent / 10000), rest_add_recharge)
                    break

    print can_get_discounts
    ## 找不到可优惠的活动
    if not can_get_discounts:
        return 0, 0, recharge * 100

    ## 有可优惠的活动 则找到最大可赠送的
    final_add_recharge = 0
    final_recharge_id = 0
    for k, v in can_get_discounts.items():
        if v >= final_add_recharge:
            final_recharge_id = k
            final_add_recharge = v

    return final_recharge_id, final_add_recharge, (final_add_recharge + recharge) * 100
    