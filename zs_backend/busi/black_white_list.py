# -*- coding:utf-8 -*-
from flask import render_template, jsonify, url_for
from flask.globals import session, request, g, current_app
from werkzeug.utils import redirect

from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import game_util
from zs_backend.utils.common import login_require
from zs_backend.utils import time_util
from zs_backend.utils import httpc_util
from zs_backend.utils.channel_qry import *
from zs_backend.busi.game_opt_log import log_type_d, log_main_type_d
from zs_backend import redis_conn
from zs_backend.utils.const import *
import json

# 黑白名单映射
black_or_white = {'black': 1, 'white': 2}


@busi.route('/games/users/list', methods=['GET'])
@login_require
def init_page():
    status_msg = {}
    return render_template('black_white_list.html', status_msg=status_msg, datas={})


@busi.route('/games/users/list', methods=['POST'])
@login_require
def show_users_list():
    qry_pid = request.form.get('pid', '')
    Where = ""
    if qry_pid:
        Where = " and pid = %s" % qry_pid
    channel = session['select_channel']

    sql_oper = SqlOperate()

    black_search_sql = """SELECT pid, game_count, total_recharge_rmb, total_withdraw, coin, counter, remark 
                FROM admin_black_list where 1 = 1 %s""" % (Where)
    black_tuple = LogQry(channel).qry(black_search_sql)

    white_search_sql = """SELECT pid, game_count, total_recharge_rmb, total_withdraw, coin, counter, remark 
                FROM admin_white_list where 1 = 1 %s""" % (Where)
    white_tuple = LogQry(channel).qry(white_search_sql)

    datas = dict()
    if len(black_tuple) > 0:
        black_list = list()
        for pid, game_count, total_recharge, total_withdraw, coin, counter, remark in black_tuple:
            data_dict = dict()
            data_dict['pid'] = pid
            data_dict['game_count'] = game_count
            data_dict['total_recharge'] = total_recharge
            data_dict['total_withdraw'] = total_withdraw
            data_dict['coin'] = game_util.coin_translate(channel, coin)
            data_dict['counter'] = game_util.coin_translate(channel, counter)
            data_dict['remark'] = remark
            black_list.append(data_dict)
        datas['black_list'] = black_list

    if len(white_tuple) > 0:
        white_list = list()
        for pid, game_count, total_recharge, total_withdraw, coin, counter, remark in white_tuple:
            data_dict = dict()
            data_dict['pid'] = pid
            data_dict['game_count'] = game_count
            data_dict['total_recharge'] = total_recharge
            data_dict['total_withdraw'] = total_withdraw
            data_dict['coin'] = game_util.coin_translate(channel, coin)
            data_dict['counter'] = game_util.coin_translate(channel, counter)
            data_dict['remark'] = remark
            white_list.append(data_dict)
        datas['white_list'] = white_list

    status_msg = dict()
    status_msg['pid'] = qry_pid

    return render_template('black_white_list.html', status_msg=status_msg, datas=datas)


@busi.route('/games/users/black', methods=['POST'])
@login_require
def add_user_to_black():
    pid = int(request.json.get('pid'))
    channel_id = session['select_channel']
    remark = request.json.get('remark') if request.json.get('remark') else ''

    game_player_sql = """
        SELECT id, nick, total_recharge_rmb, total_withdraw, coin, 
            counter
        FROM player 
        WHERE id=%d""" % pid
    game_count_sql = """SELECT ifnull(sum(game_count), 0) FROM t_player_subgame WHERE pid=%d""" % pid

    game_db_qrl = LogQry(channel_id)
    player_data = game_db_qrl.qry(game_player_sql)
    game_count_data = game_db_qrl.qry(game_count_sql)

    total_recharge = player_data[0][2]
    total_withdraw = player_data[0][3]
    coin = player_data[0][4]
    counter = player_data[0][5]
    game_count = game_count_data[0][0]

    counter_v = game_util.get_bank_coin(counter)

    sql_oper = SqlOperate()
    insert_sql = """INSERT INTO admin_black_list VALUES(%d, %d, %d, %d, %d, %d, '%s')""" \
                 % (pid, total_recharge, total_withdraw, coin, counter_v, game_count, remark)
    print insert_sql
    try:
        LogQry(channel_id).execute(insert_sql)
    except Exception as e:
        print e
        return jsonify(errmsg='加入黑名单失败')

    sql = '''
        insert into admin_opt_log 
            (channel, log_type, operator, obj, val, 
            timestamp, maintype)
        values 
            (%d, %d, %d, %d, "", 
            %d, %d)
    ''' % (channel_id, log_type_d["black"], session['user_id'], pid, time_util.now_sec(),
           log_main_type_d["player"])
    LogQry(channel_id).execute(sql)

    payload = {"pid": pid, "handle": "blacklist", "hanle_val": 1}
    GameWeb(channel_id).post("/api/handle_player", payload)

    return jsonify(errmsg='加入黑名单成功')

@busi.route('/games/users/white', methods=['POST'])
@login_require
def add_user_to_white():
    pid = int(request.json.get('pid'))
    channel_id = session['select_channel']
    remark = request.json.get('remark') if request.json.get('remark') else ''

    game_player_sql = """SELECT id, nick, total_recharge_rmb, total_withdraw, coin, counter
                    FROM player WHERE id=%d""" % pid
    game_count_sql = """SELECT ifnull(sum(game_count), 0) FROM t_player_subgame WHERE pid=%d""" % pid

    game_db_qrl = LogQry(channel_id)
    player_data = game_db_qrl.qry(game_player_sql)
    game_count_data = game_db_qrl.qry(game_count_sql)

    total_recharge = player_data[0][2]
    total_withdraw = player_data[0][3]
    coin = player_data[0][4]
    counter = player_data[0][5]
    game_count = game_count_data[0][0]

    counter_v = game_util.get_bank_coin(counter)

    sql_oper = SqlOperate()
    insert_sql = """INSERT INTO admin_white_list VALUES(%d, %d, %d, %d, %d, %d, '%s')""" \
                 % (pid, total_recharge, total_withdraw, coin, counter_v, game_count, remark)

    try:
        LogQry(channel_id).execute(insert_sql)
    except Exception as e:
        print e
        return jsonify(errmsg='加入白名单失败')

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (channel_id, log_main_type_d["player"], log_type_d["white"], session['user_id'], pid,
           time_util.now_sec())
    LogQry(channel_id).execute(sql)

    payload = {"pid": pid, "handle": "whitelist", "hanle_val": 1}
    GameWeb(channel_id).post("/api/handle_player", payload)

    return jsonify(errmsg='加入白名单成功')


@busi.route('/games/users/black', methods=['DELETE'])
@login_require
def delete_black_player():
    pid = int(request.json.get('pid'))
    channel = session['select_channel']

    sql_oper = SqlOperate()
    delete_sql = """DELETE FROM admin_black_list WHERE pid=%d""" % pid

    try:
        LogQry(channel).execute(delete_sql)
    except Exception as e:
        print e
        return jsonify(errmsg='移除黑名单失败')

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            "", %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["del_black"], session['user_id'], pid,
           time_util.now_sec())
    LogQry(channel).execute(sql)

    payload = {"pid": pid, "handle": "blacklist", "hanle_val": 0}
    GameWeb(channel).post("/api/handle_player", payload)

    return jsonify(errmsg='移除黑名单成功')


@busi.route('/games/users/white', methods=['DELETE'])
@login_require
def delete_white_player():
    pid = int(request.json.get('pid'))
    channel = session['select_channel']

    sql_oper = SqlOperate()
    delete_sql = """DELETE FROM admin_white_list WHERE pid=%d""" % pid

    try:
        LogQry(channel).execute(delete_sql)
    except Exception as e:
        print e
        return jsonify(errmsg='移除白名单失败')

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values (%d, %d, %d, %d, %d, "", %d)
    ''' % (channel, log_main_type_d["player"], log_type_d["del_white"], session['user_id'], pid,
           time_util.now_sec())
    LogQry(channel).execute(sql)

    payload = {"pid": pid, "handle": "whitelist", "hanle_val": 0}
    GameWeb(channel).post("/api/handle_player", payload)

    return jsonify(errmsg='移除白名单成功')


@busi.route('/games/ip/black/create', methods=['POST'])
@login_require
def add_ip_to_black():
    """添加ip黑名单"""

    # 获取参数
    ip = request.json.get('ip')
    channel_id = session['select_channel']
    remark = request.json.get('remark') if request.json.get('remark') else ''

    # 校验参数
    if not ip:
        return jsonify(result=0, msg=u'请输入国家/地区/IP！')

    # 将数据存进数据库
    create_sql = """
        INSERT INTO admin_ip_black_white_list 
        VALUES(0,%s,'%s',%s,'%s');
    """ % (black_or_white['black'], ip, channel_id, remark)
    LogQry(channel_id).execute(create_sql)

    sync_ip_black_white(int(channel_id))

    # 返回应答
    return jsonify(result=1, msg=u'加入黑名单成功！')


@busi.route('/games/ip/white/create', methods=['POST'])
@login_require
def add_ip_to_white():
    """添加ip白名单"""

    # 获取参数
    ip = request.json.get('ip')
    channel_id = session['select_channel']
    remark = request.json.get('remark') if request.json.get('remark') else ''

    # 校验参数
    if not ip:
        return jsonify(result=0, msg=u'请输入国家/地区/IP！')

    # 将数据存进数据库
    create_sql = """
        INSERT INTO admin_ip_black_white_list 
        VALUES(0,%s,'%s',%s,'%s');
    """ % (black_or_white['white'], ip, channel_id, remark)
    LogQry(channel_id).execute(create_sql)

    sync_ip_black_white(int(channel_id))

    # 返回应答
    return jsonify(result=1, msg=u'加入白名单成功！')


@busi.route('/games/ip/retrieve', methods=['GET'])
@login_require
def ip_tp_black_white_retrieve():
    """查询ip黑白名单"""

    # 获取参数
    channel_id = session['select_channel']
    ip = request.args.get('ip')

    # 处理数据
    search_ip_str = ''
    if ip:
        search_ip_str = " AND country_area_ip LIKE '%%%s%%'" % ip

    # 从数据库取出并处理黑名单数据
    retrieve_sql = """
        SELECT country_area_ip,remark,id 
        FROM admin_ip_black_white_list 
        WHERE type=%s 
        AND channel_id=%s 
        %s;""" % (black_or_white['black'], channel_id, search_ip_str)
    datas = LogQry(channel_id).qry(retrieve_sql)
    black_list = list()
    for data in datas:
        black_dict = dict()
        black_dict['ip'] = data[0]
        black_dict['remark'] = data[1]
        black_dict['id'] = data[2]
        black_list.append(black_dict)

    # 从数据库取出并处理白名单数据
    retrieve_sql = """
        SELECT country_area_ip,remark,id 
        FROM admin_ip_black_white_list 
        WHERE type=%s 
        AND channel_id=%s 
        %s;
    """ % (black_or_white['white'], channel_id, search_ip_str)
    datas = LogQry(channel_id).qry(retrieve_sql)
    white_list = list()
    for data in datas:
        white_dict = dict()
        white_dict['ip'] = data[0]
        white_dict['remark'] = data[1]
        white_dict['id'] = data[2]
        white_list.append(white_dict)

    # 额外参数
    status_msg = dict()
    status_msg['select_channel_ip'] = int(channel_id)
    status_msg['user_or_ip'] = 2
    status_msg['ip'] = ip
    datas = ''  # 由于游戏账号黑白名单设置需要用到，为防止报错带上此参数

    # 返回模版与数据
    return render_template('black_white_list.html', black=black_list, white=white_list, status_msg=status_msg,
                           datas=datas)


@busi.route('/games/ip/black/white/delete', methods=['DELETE'])
@login_require
def delete_ip():
    """删除ip黑白名单"""

    # 获取参数
    pid = request.json.get('pid')
    channel_id = session['select_channel']

    # 从数据库中删除数据
    delete_sql = """DELETE FROM admin_ip_black_white_list WHERE id=%s;""" % pid
    LogQry(channel_id).execute(delete_sql)

    sync_ip_black_white(channel_id)

    # 返回应答
    return jsonify(msg=u'删除成功！')

def sync_ip_black_white(channel):
    sql = '''
        select type, group_concat(country_area_ip separator '~')
        from admin_ip_black_white_list
        where channel_id = %d
        group by type
    ''' % channel

    payload = {}
    for k, v in LogQry(channel).qry(sql):
        if k == black_or_white["black"]:
            key = "black"
        elif k == black_or_white["white"]:
            key = "white"
        else:
            continue

        payload[key] = v

    if payload:
        redis_conn.hmset(BLACK_WHITE_TABLE+str(channel), payload)
