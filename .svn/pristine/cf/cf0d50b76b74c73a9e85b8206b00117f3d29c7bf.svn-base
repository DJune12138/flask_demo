# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi, game_parameter
from zs_backend.busi.game_opt_log import log_type_d
from zs_backend.busi.game_user import get_player_state
from zs_backend.utils import time_util, game_util
from zs_backend.utils.channel_qry import GameWeb
from zs_backend.utils.common import login_require
from flask import render_template, session, request, jsonify
from zs_backend.utils.channel_qry import LogQry


@busi.route('/player/money/details', methods=['GET'])
@login_require
def show_player_money_details():
    """玩家加扣款页面"""

    status_msg = dict()
    status_msg['beginDate'] = False
    status_msg['endDate'] = False
    status_msg['access_level'] = session['access_level']
    status_msg['PlayerID'] = ""
    status_msg['NickName'] = ""
    status_msg['date1'] = time_util.formatDate(time_util.now_sec() - 7 * 86400)
    status_msg['date2'] = time_util.formatDate(time_util.now_sec())

    return render_template('player_monies.html', status_msg=status_msg, base_player={})


@busi.route('/player/money/search', methods=['GET'])
@login_require
def search_player_money_detail():
    """玩家搜索"""

    access_level = session['access_level']
    PID = request.args.get('PlayerID', '')
    NickName = request.args.get('NickName', '')
    # 接收渠道id
    channel = session['select_channel']

    print access_level, "access_level"

    status_msg = dict()
    status_msg['beginDate'] = False
    status_msg['endDate'] = False
    status_msg['access_level'] = access_level
    status_msg['PlayerID'] = PID
    status_msg['NickName'] = NickName
    status_msg['channel'] = channel
    status_msg['date1'] = time_util.formatDate(time_util.now_sec() - 7 * 86400)
    status_msg['date2'] = time_util.formatDate(time_util.now_sec())

    WHERE = ""
    if PID:
        WHERE += " and id = %s" % PID
    if NickName:
        WHERE += " and nick = '%s'" % NickName

    if not WHERE:
        return render_template('player_monies.html', status_msg=status_msg, base_player={})

    sql = '''
        select id, nick, reg_time, client_id, reg_ip,
            coin, counter, device, did, last_login_ip,
            phone, last_login_time, did, subgame, total_recharge_rmb,
            total_withdraw, time_long, (select count(1) from t_player_general where pid = a.id),
                ifnull((select p_code from player_agent where pid = a.id), ""),
                ifnull((select invite_code from player_agent where pid = a.id), ""),
            ban, account_id
        from player a
        where 1=1 %s
    ''' % WHERE

    base_player = {}
    for line in LogQry(channel).qry(sql):
        status_msg['PlayerID'] = line[0]
        base_player["id"] = line[0]
        base_player["nick"] = line[1]
        base_player["reg_time"] = time_util.formatDateTime(line[2])
        base_player["channel_id"] = line[3]
        base_player["reg_ip"] = line[4]
        base_player["account_id"] = line[21]

        coin = GameWeb(channel).post("/api/get_player_info", {'pid': int(line[0])})['result']['coin']
        bank = GameWeb(channel).post("/api/get_player_info", {'pid': int(line[0])})['result']['dep']
        base_player["coin"] = game_util.coin_translate(channel, coin)
        base_player["banker"] = game_util.coin_translate(channel, bank)

        base_player["platform"] = line[7]
        base_player["did"] = line[8]
        base_player["last_login_ip"] = line[9]

        base_player["phone"] = line[10]
        base_player["last_login_time"] = time_util.formatDateTime(line[11])
        base_player["did"] = line[12]

        base_player["subgame"] = game_parameter.get_subgame_name(line[13])
        base_player["total_recharge_rmb"] = line[14]

        base_player["total_withdraw"] = line[15]
        base_player["time_long"] = line[16]
        base_player["game_count"] = line[17]
        base_player["p_code"] = line[18]
        base_player["invite_code"] = line[19]
        base_player["status"] = get_player_state(line[20])

        ## 查询新手卡数
        sql = '''
            select count(1)
            from log_activity
            where activity_type = 4
            and detail like '%%%d,%%'
        ''' % line[0]
        base_player["newbie_card"] = LogQry(channel).qry(sql)[0][0]

    return render_template('player_monies.html', status_msg=status_msg, base_player=base_player)
