# -*- coding:utf-8 -*-
from flask import render_template, jsonify, url_for
from flask.globals import session, request, g, current_app
from werkzeug.utils import redirect

from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import erl
from zs_backend.utils.common import login_require
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
from zs_backend.busi.game_opt_log import log_type_d, log_main_type_d
from zs_backend.utils.game_util import set_zfb_info, set_bank_info


@busi.route('/gm/user/alter_bank_pwd', methods=['GET'])
@login_require
def alter_bank_pwd():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    pwd = int(request.args.get('pwd'))

    payload = {"pid": pid, "psw": pwd}
    GameWeb(channel).post("/api/change_bank_psw", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["alter_bank_pwd"], session['user_id'], pid, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({"msg": u"修改保险柜密码成功"})


@busi.route('/gm/user/alter_nick', methods=['GET'])
@login_require
def alter_nick():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    nick = request.args.get('nick')

    payload = {"pid": pid, "nick": nick}
    GameWeb(channel).post("/api/change_nick", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            '%s', %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["alter_nick"], session['user_id'], pid, nick,
        time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/send_coin', methods=['GET'])
@login_require
def gm_user_send_coin():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    num = request.args.get('num')
    reason = request.args.get('reason')
    type_id = request.args.get('type')

    if int(type_id) == 3 or int(type_id) == 4:
        num = 0 - float(num)

    payload = {"pid": pid, "val": float(num)}
    GameWeb(channel).post("/api/set_deposit", payload)

    val = type_id + '--' + str(num) + '--' + reason

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            '%s', %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["send_coin"], session['user_id'], pid, val, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/send_item', methods=['GET'])
@login_require
def gm_user_send_item():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    num = int(request.args.get('num'))
    type_id = request.args.get('type')

    if int(type_id) == 2:
        num = 0 - num

    payload = {"pid": pid, "items": [[20010001, num]]}
    GameWeb(channel).post("/api/give_items", payload)

    val = type_id + '--' + str(num)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            '%s', %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["send_item"], session['user_id'], pid, val, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/alter_vip', methods=['GET'])
@login_require
def gm_user_alter_vip():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    vip = int(request.args.get('vip'))

    ## 查询层级
    sql = 'select member_level_name from admin_member_level where id = %d' % vip
    vip_name = LogQry(channel).qry(sql)[0][0]
    val = u"%d_%s" % (vip, vip_name)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            '%s', %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["alter_vip"], session['user_id'], pid, \
           val, time_util.now_sec())
    LogQry(channel).execute(sql)

    payload = {"pid": pid, "vip": vip}
    GameWeb(channel).post("/api/set_player_vip", payload)

    return jsonify({})


@busi.route('/gm/user/forbid', methods=['GET'])
@login_require
def gm_user_forbid():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    reason = request.args.get("reason")

    payload = {"pid": pid, "handle": "ban", "hanle_val": 1, "reason":reason}
    GameWeb(channel).post("/api/handle_player", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            '%s', %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["forbid"], session['user_id'], pid, reason, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/cancel_forbid', methods=['GET'])
@login_require
def gm_user_cancel_forbid():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']

    payload = {"pid": pid, "handle": "ban", "hanle_val": 0}
    GameWeb(channel).post("/api/handle_player", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (
        channel, log_main_type_d["player"], log_type_d["cancel_forbid"], session['user_id'], pid, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/cold', methods=['GET'])
@login_require
def gm_user_cold():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']

    payload = {"pid": pid, "handle": "lock", "hanle_val": 1}
    GameWeb(channel).post("/api/handle_player", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["cold"], session['user_id'], pid, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/cancel_cold', methods=['GET'])
@login_require
def gm_user_cancel_cold():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']

    payload = {"pid": pid, "handle": "lock", "hanle_val": 0}
    GameWeb(channel).post("/api/handle_player", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["cancel_cold"], session['user_id'], pid, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/gm/user/outline', methods=['GET'])
@login_require
def gm_user_outline():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']

    payload = {"pid": pid, "handle": "kick", "hanle_val": 1}
    GameWeb(channel).post("/api/handle_player", payload)

    return jsonify({})


@busi.route('/gm/user/alter_pass', methods=['GET'])
@login_require
def gm_user_alter_pass():
    pid = int(request.args.get('PlayerID'))
    channel = session['select_channel']
    password = request.args.get("pass")

    payload = {"pid": pid, "pass": password}
    GameWeb(channel).post("/api/reset_login_pass", payload)

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["alter_pass"], session['user_id'], pid, time_util.now_sec())
    LogQry(channel).execute(sql)

    return jsonify({})


@busi.route('/game/user/set/zfb', methods=['POST'])
@login_require
def set_zfb():
    """设置绑定支付宝"""

    # 获取参数
    channel = session['select_channel']
    pid = request.form.get('pid')
    acc = request.form.get('acc')
    name = request.form.get('name')

    # 校验参数
    if not acc:
        return jsonify(result='fail', msg=u'账号不能为空！')

    # 与游戏对接
    zfb = set_zfb_info(channel, pid, acc, name)
    if not zfb:
        return jsonify(result='ok', msg=u'设置失败！')

    # 写入日志
    val = '/'.join([acc, name])
    create_sql = """INSERT INTO admin_opt_log (channel,maintype,log_type,operator,obj, 
                                  val, timestamp)
                    VALUES (%s,%s,%s,%s,%s, 
                            '%s',%s);""" \
                 % (channel, log_main_type_d["player"], log_type_d["alter_zfb"], session['user_id'], pid,
                    val, time_util.now_sec())
    LogQry(channel).execute(create_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'设置成功！')


@busi.route('/game/user/set/bank', methods=['POST'])
@login_require
def set_bank():
    """设置绑定银行卡"""

    # 获取参数
    channel = session['select_channel']
    pid = request.form.get('pid')
    acc = request.form.get('acc')
    name = request.form.get('name')
    bank = request.form.get('bank')
    addr = request.form.get('addr')

    # 校验参数
    if not acc:
        return jsonify(result='fail', msg=u'账号不能为空！')

    # 与游戏对接
    banker = set_bank_info(channel, pid, acc, name, bank, addr)
    if not banker:
        return jsonify(result='ok', msg=u'设置失败！')

    # 写入日志
    val = '/'.join([acc, name, bank, addr])
    create_sql = """INSERT INTO admin_opt_log (channel,maintype,log_type,operator,obj, 
                                  val, timestamp)
                    VALUES (%s,%s,%s,%s,%s, 
                            '%s',%s);""" \
                 % (channel, log_main_type_d["player"], log_type_d["alter_bank"], session['user_id'], pid,
                    val, time_util.now_sec())
    LogQry(channel).execute(create_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'设置成功！')


@busi.route('/game/user/set/invited/code', methods=['POST'])
@login_require
def set_invited_code():
    """修改受邀码"""

    # 获取参数
    channel = session['select_channel']
    pid = request.form.get('pid')
    agent_id = request.form.get('agent_id')

    # 校验参数
    if not agent_id:
        return jsonify(result='fail', msg=u'受邀码不能为空！')
    try:
        agent_id = int(agent_id)
    except ValueError:
        return jsonify(result='fail', msg=u'受邀码为整数纯数字！')

    # 与游戏对接
    status = GameWeb(channel).post('/api/bind_agent', {'pid': int(pid), 'agent_id': agent_id})
    if status['result'] != 0:
        return jsonify(result='fail', msg=u'修改受邀码失败！')

    # 写入日志
    create_sql = """INSERT INTO admin_opt_log (channel,maintype,log_type,operator,obj, 
                                      val, timestamp)
                    VALUES (%s,%s,%s,%s,%s, 
                            '%s',%s);""" \
                 % (channel, log_main_type_d["player"], log_type_d["alter_code"], session['user_id'], pid,
                    agent_id, time_util.now_sec())
    LogQry(channel).execute(create_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'设置成功！')
