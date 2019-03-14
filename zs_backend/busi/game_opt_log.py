# -*- coding:utf-8 -*-

from flask import render_template, jsonify
from flask.globals import session, request, g

from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require, get_highest_role_id
from zs_backend.utils.channel_qry import *
from zs_backend.utils import time_util
from copy import deepcopy
from zs_backend.utils import game_util
from zs_backend.busi import game_parameter

log_main_type_d = {
    "win_ctl": 0,  ## 输赢控制
    "system": 1,  ## 系统配置
    "player": 2,  ## 玩家相关
    "recharge": 3,  ## 财务相关
    "gm": 4,  ## gm控制类
}

log_type_d = {
    "single_ctl": 0,
    "full_game_ctl": 1,
    "send_item": 2,
    "send_coin": 3,
    "white": 4,
    "black": 5,
    "forbid": 6,
    "cancel_forbid": 7,
    "cold": 8,
    "cancel_cold": 9,
    "del_black": 10,
    "del_white": 11,
    "alter_bank_pwd": 12,
    "alter_nick": 13,
    "delete_staff": 14,
    "add_staff": 15,
    "edit_staff": 16,
    "delete_channel": 17,
    "add_channel": 18,
    "edit_channel": 19,
    "alter_pass": 20,
    "alter_vip": 21,
    "alter_zfb": 22,
    "alter_bank": 23,
    "alter_code": 24,
}

init_page = {
    "list": [],
    "beginDate": 11,
    "endDate": 11
}


@busi.route('/games/maniplate/log', methods=['GET'])
@login_require
def show_manipulate_log():
    page = deepcopy(init_page)
    return render_template('maniplate_game_log.html', page=page)


@busi.route('/games/maniplate/log_data', methods=['POST'])
@login_require
def show_manipulate_log_data():
    start = request.form.get('beginDate')
    end = request.form.get('endDate')
    channel = session['select_channel']

    start = time_util.start(start)
    end = time_util.end(end)

    sql = '''
		select log_type, operator, obj, val, timestamp 
		from admin_opt_log 
		where channel = %d and timestamp >= %d and timestamp <= %d and maintype = %d
		order by timestamp desc limit 30
	''' % (channel, start, end, log_main_type_d["win_ctl"])

    page = deepcopy(init_page)

    page["beginDate"] = start
    page["endDate"] = end
    page["SelectChannel"] = channel

    ## 查询子游戏列表
    SubGameList = game_parameter.get_subgame_list()

    for log_type, operator, obj, val, timestamp in LogQry(channel).qry(sql):
        OperatorName = SqlOperate().select("select name from user where id = %d" % operator)[0][0]
        if log_type == log_type_d["single_ctl"]:
            log_type_str = u"单控"
            obj_sql = "select nick from player where id = %d" % obj
            try:
                obj_name = LogQry(channel).qry(obj_sql)[0][0]
            except:
                obj_name = ""

            log_content = u"管理员%s对玩家%s(%s)设置了保护值：%s" % \
                          (blue_html(OperatorName), blue_html(obj_name), blue_html(obj), red_html(val))
        elif log_type == log_type_d["full_game_ctl"]:
            log_type_str = u"控大盘"
            [room_name, water] = val.split("_")
            log_content = u"管理员%s对%s(%s)水池调整成：%s" % \
                          (blue_html(OperatorName), blue_html(game_parameter.get_subgame_by_id(SubGameList, obj)),
                           blue_html(room_name), red_html(water))

        page["list"].append([OperatorName, log_type_str, log_content, timestamp])

    return jsonify(result='ok', data=page)


@busi.route('/games/users/manage/log', methods=['GET'])
@login_require
def show_manage_log():
    page = dict()
    page['beginDate'] = True
    page['endDate'] = True
    return render_template('user_game_managed_log.html', status_msg={}, page=page)


@busi.route('/search/games/users/manage/log', methods=['GET'])
@login_require
def show_manage_log_data():
    start = request.args.get('beginDate')
    end = request.args.get('endDate')
    pid = request.args.get('PlayerID')
    nick = request.args.get('NickName')
    channel = session['select_channel']
    size = int(request.args.get('size', ''))
    offset = int(request.args.get('offset', ''))

    start = time_util.start(start)
    end = time_util.end(end)

    # 校验参数
    if pid:
        try:
            int(pid)
        except ValueError:
            return jsonify(result='fail', msg=u'玩家ID为整数纯数字！')
    if pid and nick:
        return jsonify(result='fail', msg=u'玩家ID与玩家昵称只能输入其一！')
    if start >= end:
        return jsonify(result='fail', mag=u'结束日期不能小于开始日期！')

    # 转换昵称
    if nick:
        retrieve_sql = """SELECT id FROM player WHERE nick='%s';""" % nick
        pid = LogQry(channel).qry(retrieve_sql)[0][0]

    if pid or nick:
        sql = '''
            select log_type, operator, obj, val, timestamp 
            from admin_opt_log 
            where channel = %d and timestamp >= %d and timestamp <= %d and maintype = %d and obj = %s
            order by timestamp desc 
            LIMIT %d,%d
        ''' % (channel, start, end, log_main_type_d["player"], pid, offset, size)

        count_sql = '''
            select count(1)
            from admin_opt_log 
            where channel = %d and timestamp >= %d and timestamp <= %d and maintype = %d and obj = %s
            order by timestamp desc;
        ''' % (channel, start, end, log_main_type_d["player"], pid)
    else:
        sql = '''
                    select log_type, operator, obj, val, timestamp 
                    from admin_opt_log 
                    where channel = %d and timestamp >= %d and timestamp <= %d and maintype = %d 
                    order by timestamp desc 
                    LIMIT %d,%d
                ''' % (channel, start, end, log_main_type_d["player"], offset, size)

        count_sql = '''
                    select count(1)
                    from admin_opt_log 
                    where channel = %d and timestamp >= %d and timestamp <= %d and maintype = %d 
                    order by timestamp desc;
                ''' % (channel, start, end, log_main_type_d["player"])

    total_count = LogQry(channel).qry(count_sql)

    page = deepcopy(init_page)

    page["beginDate"] = start
    page["endDate"] = end
    page["SelectChannel"] = channel

    for log_type, operator, obj, val, timestamp in LogQry(channel).qry(sql):
        OperatorName = SqlOperate().select("select name from user where id = %d" % operator)[0][0]
        if log_type == log_type_d["white"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s加入白名单" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["black"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s加入黑名单" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["forbid"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s封号,原因为:%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["cancel_forbid"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s解封" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["cold"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s资金冻结" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["cancel_cold"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s资金解冻" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["alter_pass"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s修改登录密码" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["send_coin"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s赠送金币%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["send_item"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s赠送喇叭%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["del_white"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s移除白名单" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["del_black"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s移除黑名单" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["alter_bank_pwd"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s修改保险柜密码" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name))

        elif log_type == log_type_d["alter_nick"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s修改昵称为：%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), blue_html(val))

        elif log_type == log_type_d["alter_vip"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s调整了会员层级为%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["alter_zfb"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s绑定了支付宝%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["alter_bank"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s绑定了银行卡%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        elif log_type == log_type_d["alter_code"]:
            obj_sql = "select nick from player where id = %d" % obj
            if LogQry(channel).qry(obj_sql):
                nick = LogQry(channel).qry(obj_sql)[0][0]
            else:
                nick = ''
            obj_name = nick + "(ID:%d)" % obj
            log_content = u"管理员%s对玩家%s修改了受邀码为%s" % \
                          (blue_html(OperatorName), red_html_link(obj, nick, channel, obj_name), red_html(val))

        page["list"].append({"OperatorName": OperatorName, "obj_name": obj_name,
                             "log_content": log_content, "timestamp": timestamp})

    return jsonify({"result": "ok", "errcode": 0, "dataLength": total_count, "rowDatas": page["list"]})


@busi.route('/users/manage/log', methods=['GET'])
@login_require
def show_users_manage_log():
    page = dict()
    page['beginDate'] = 11
    page['endDate'] = 11
    return render_template('user_managed_log.html', status_msg={}, page=page)


@busi.route('/search/users/manage/log', methods=['GET'])
@login_require
def search_users_manage_log():
    start = time_util.formatDatestamp(request.args.get('beginDate'))
    end = time_util.formatDatestamp(request.args.get('endDate'))

    role_str = session['role_str']
    highest_role = get_highest_role_id(role_str)

    if highest_role == 1:
        sql = '''
            select log_type, operator, obj, val, timestamp 
            from admin_opt_log 
            where channel=0 and timestamp >= %d and timestamp <= %d and maintype = 1
            order by timestamp desc limit 30;
        ''' % (start, end + 86400)

    else:
        sql = '''
            select log_type, operator, obj, val, timestamp 
            from admin_opt_log 
            where channel=0 and val=%s and timestamp >= %d and timestamp <= %d and maintype = 1
            order by timestamp desc limit 30;
        ''' % (highest_role, start, end + 86400)

    print sql

    page = deepcopy(init_page)

    page["beginDate"] = start
    page["endDate"] = end

    for log_type, operator, obj, val, timestamp in SqlOperate().select(sql):
        print obj
        OperatorName = SqlOperate().select("select name from user where id = %d" % operator)[0][0]

        if log_type == log_type_d["delete_staff"]:
            obj_sql = "select name from user where id = %d" % obj
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            log_content = u"管理员%s删除员工%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        if log_type == log_type_d["add_staff"]:
            obj_sql = "select name from user where id = %d" % obj
            print obj_sql
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            print 'obj_name', obj_name
            log_content = u"管理员%s添加员工%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        if log_type == log_type_d["edit_staff"]:
            obj_sql = "select name from user where id = %d" % obj
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            log_content = u"管理员%s修改员工%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        if log_type == log_type_d["add_channel"]:
            obj_sql = "select name from channel where id = %d" % obj
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            log_content = u"管理员%s添加渠道%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        if log_type == log_type_d["edit_channel"]:
            obj_sql = "select name from channel where id = %d" % obj
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            log_content = u"管理员%s修改渠道%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        if log_type == log_type_d["delete_channel"]:
            obj_sql = "select name from channel where id = %d" % obj
            if SqlOperate().select(obj_sql):
                name = SqlOperate().select(obj_sql)[0][0]
            else:
                name = ''
            obj_name = name + "(ID:%d)" % obj
            log_content = u"管理员%s删除渠道%s" % \
                          (blue_html(OperatorName), red_html(obj_name))

        page["list"].append([OperatorName, obj_name, log_content, timestamp])

    return render_template('user_managed_log.html', page=page)


def blue_html(val):
    return """<font color="blue">%s</font>""" % val


def red_html_link(obj, nick, channel, val):
    return """<font color="red"><a onclick="new_iframe('玩家信息详情','/games/users/datas/details?pid=%s')">%s</a></font>""" % (
        obj, val)


def red_html(val):
    return '<font color="red">%s</font>' % val
