# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, session, jsonify, request
from zs_backend.utils.channel_qry import LogQry
from zs_backend import SqlOperate
import json
from zs_backend.utils import time_util
from zs_backend.utils.log_table import *
from zs_backend.busi import game_parameter
from zs_backend.utils.game_util import coin_translate

ALARM_PLAYER_STAKE_COIN = 1  ## 玩家单局游戏押注
ALARM_PLAYER_OUTPUT_COIN = 2  ## 玩家单局游戏产出
ALARM_PLAYER_OUTPUT_COIN_TODAY = 3  ## 玩家当日游戏全部产出
ALARM_REG_SAME_IP = 4  ## 同一IP今日注册账号数
ALARM_REG_SAME_DEVICE = 5  ## 同一设备今日注册账号数
ALARM_PLAYER_OUT_STAKE_COIN_RATE = 6  ## 单局游戏中奖倍数
ALARM_PLAYER_RECHARGE = 7  ## 单次充值
ALARM_PLAYER_RECHARGE_TODAY = 8  ## 当日总共充值
ALARM_PLAYER_WITHDRAW = 9  ## 单次提现
ALARM_PLAYER_WITHDRAW_TODAY = 10  ## 当日总共提现
ALARM_PLAYER_PRESENT = 11  ## 单次赠送
ALARM_PLAYER_PRESENT_TODAY = 12  ## 当日总共赠送

STATE_UNREAD = 0
STATE_READ = 1

@busi.route('/alarm_config_show', methods=['GET'])
@login_require
def alarm_config_show():
    return render_template("alarm.html")

@busi.route('/alarm_config', methods=['GET'])
@login_require
def get_alarm_config_1():
    channel = session['select_channel']

    sql = 'select config from admin_game_alarm_config where id = 1'
    try:
        conf = LogQry(channel).qry(sql)[0][0]
        conf = json.loads(conf)
    except:
        conf = []

    return jsonify(data=conf)

@busi.route('/alarm_config_set', methods=['GET'])
@login_require
def set_alarm_config():
    channel = session['select_channel']
    conf = request.args.get("conf")

    try:
        json.loads(conf)
        sql = '''replace into admin_game_alarm_config values (1, '%s')''' % conf
        LogQry(channel).execute(sql)
        return jsonify(result="succ")
    except:
        return jsonify(result="fail")

@busi.route('/alarm_list', methods=['GET'])
@login_require
def alarm_list():
    begin_time = request.args.get('beginDate')
    end_time = request.args.get('endDate')

    begin_time = time_util.formatTimestamp(begin_time)
    end_time = time_util.formatTimestamp(end_time) + 86400
    channel = session['select_channel']

    size = int(request.args.get('size', ''))
    offset = int(request.args.get('offset', ''))

    subgame = game_parameter.get_subgame_list()

    datas = []
    sql = '''
            select id, pid, time, stype, val, 
                state, ifnull((select nick from player where id = pid), "")
            from admin_game_alarm
            where time >= %d
            and time <= %d
            order by state, time desc
            limit %d, %d
        ''' % (begin_time, end_time, offset, size)
    print sql
    for idx, pid, time, stype, val, \
        state, name in LogQry(channel).qry(sql):
        d = {
            "id": idx,
            "pid": pid,
            "time": time,
            "name": name,
            "state": state,
            "content": html(channel, pid, name, stype, val, subgame),
        }
        datas.append(d)

    sql = 'select count(1) from admin_game_alarm where time >= %d and time <= %d' % (begin_time, end_time)
    total = LogQry(channel).qry(sql)[0][0]

    return jsonify(data = datas, total = total)

def blue_html(val):
    return """<font color="blue">%s</font>""" % val

def pid_html(pid, nick):
    return """<font color="red"><a onclick="new_iframe('玩家信息详情','/games/users/datas/details?pid=%s')">%s</a></font>""" % (pid, nick)

def red_html(val):
    return '<font color="red">%s</font>' % val

## 格式化预警内容
def html(channel, pid, name, stype, val, subgame):
    if stype == ALARM_PLAYER_STAKE_COIN:
        [gameid, stake_coin, alarm_val] = val.split(",")
        return u"玩家%s在%s中单局押注金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            blue_html(game_parameter.get_subgame_by_id(subgame, int(gameid))), red_html(coin_translate(channel, stake_coin)), 
            red_html(coin_translate(channel, alarm_val)))
    elif stype == ALARM_PLAYER_OUTPUT_COIN:
        [gameid, win_coin, alarm_val] = val.split(",")
        return u"玩家%s在%s中单局盈利金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            blue_html(game_parameter.get_subgame_by_id(subgame, int(gameid))), red_html(coin_translate(channel, win_coin)), 
                red_html(coin_translate(channel, alarm_val)))
    elif stype == ALARM_PLAYER_OUTPUT_COIN_TODAY:
        [win_coin, alarm_val] = val.split(",")
        return u"玩家%s今日游戏盈利金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(coin_translate(channel, win_coin)), red_html(coin_translate(channel, alarm_val)))
    elif stype == ALARM_REG_SAME_IP:
        [count, alarm_val] = val.split(",")
        return u"%s今日注册账号数达到%s,高于%s的预警值" % (red_html(pid), red_html(count), red_html(alarm_val))
    elif stype == ALARM_REG_SAME_DEVICE:
        [count, alarm_val] = val.split(",")
        return u"%s今日注册账号数达到%s,高于%s的预警值" % (red_html(pid), red_html(count), red_html(alarm_val))
    elif stype == ALARM_PLAYER_OUT_STAKE_COIN_RATE:
        [gameid, count, alarm_val] = val.split(",")
        return u"玩家%s在%s中游戏中奖倍数达到%s,高于%s的预警值" % (pid_html(pid, name), \
            blue_html(game_parameter.get_subgame_by_id(subgame, int(gameid))), red_html(count), red_html(alarm_val))
    elif stype == ALARM_PLAYER_RECHARGE:
        [recharge, alarm_val] = val.split(",")
        return u"玩家%s今日单笔充值金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(recharge), red_html(alarm_val))
    elif stype == ALARM_PLAYER_RECHARGE_TODAY:
        [total_recharge, alarm_val] = val.split(",")
        return u"玩家%s今日总充值金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(total_recharge), red_html(alarm_val))
    elif stype == ALARM_PLAYER_WITHDRAW:
        [withdraw, alarm_val] = val.split(",")
        return u"玩家%s今日单笔提现金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(withdraw), red_html(alarm_val))
    elif stype == ALARM_PLAYER_WITHDRAW_TODAY:
        [total_withdraw, alarm_val] = val.split(",")
        return u"玩家%s今日总充值金额达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(total_withdraw), red_html(alarm_val))
    elif stype == ALARM_PLAYER_PRESENT:
        [present, alarm_val] = val.split(",")
        return u"玩家%s今日单笔赠送金币达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(present), red_html(alarm_val))
    elif stype == ALARM_PLAYER_PRESENT_TODAY:
        [total_present, alarm_val] = val.split(",")
        return u"玩家%s今日总赠送金币达到%s,高于%s的预警值" % (pid_html(pid, name), \
            red_html(total_present), red_html(alarm_val))
    return ""

@busi.route('/alarm_read', methods=['GET'])
@login_require
def alarm_read():
    channel = session['select_channel']

    ids = request.args.get("ids")

    if ids:
        sql = 'update admin_game_alarm set state = %d where id in (%s) ' % (STATE_READ, ids)
        LogQry(channel).execute(sql)
        return jsonify(result="succ")
    else:
        return jsonify(result="fail")

@busi.route('/alarm_count', methods=['GET'])
@login_require
def alarm_count():
    begin_time = request.args.get('beginDate')
    end_time = request.args.get('endDate')

    begin_time = time_util.formatTimestamp(begin_time)
    end_time = time_util.formatTimestamp(end_time) + 86400
    channel = session['select_channel']

    sql = '''
        select count(1)
        from admin_game_alarm
        where time >= %d
        and time <= %d
        and state = %d
    ''' % (begin_time, end_time, STATE_UNREAD)
    total_count = LogQry(channel).qry(sql)

    return jsonify(count = total_count)
