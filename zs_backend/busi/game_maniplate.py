# -*- coding:utf-8 -*-

from flask import render_template, jsonify
from flask.globals import session, request, g

from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from zs_backend.utils.channel_qry import *
from zs_backend.utils import time_util

from zs_backend.busi.game_opt_log import log_type_d, log_main_type_d
from zs_backend.utils import game_util
from zs_backend.busi import game_parameter

from copy import deepcopy

full_page = {
    "other_qry": [],
    "datas": [],
    "channel": ""
}


def full_query_html(status=None):
    print status
    line = []
    for k, v in game_parameter.get_subgame_list().items():
        if k == status:
            l = '<option value="%d" selected>%s</option>' % (k, v)
        else:
            l = '<option value="%d">%s</option>' % (k, v)
        line.append(l)

    subgame = u'''
        <td>选择游戏：
            <select id="subgame" name="subgame">
                %s
            </select>
        </td>
    ''' % "\n".join(line)

    return [subgame]


## 获取对应渠道的子游戏列表
@busi.route('/games/maniplate/channel_game', methods=['POST'])
@login_require
def subgame_list():
    Channel = session['select_channel']
    Result = game_parameter.get_subgame_list()
    return jsonify(Result)


## 全盘控
@busi.route('/games/maniplate/fullhandicaper', methods=['GET'])
@login_require
def maniplate_full_handicaper():
    page = deepcopy(full_page)
    page["other_qry"] = full_query_html()
    return render_template('maniplate_full_handicaper.html', page=page)


## 全盘控
@busi.route('/games/maniplate/fullhandicaper', methods=['POST'])
@login_require
def maniplate_full_handicaper_query():
    channel = session['select_channel']

    status = int(request.form.get("subgame"))  # 用于保存选中的游戏状态

    page = deepcopy(full_page)
    page["other_qry"] = full_query_html(status=status)
    page["channel"] = channel
    page["subgame"] = request.form.get("subgame")

    ll = GameWeb(channel).post("/api/subgame_ctl_list",
                               {"gameid": request.form.get("subgame")})
    ll.sort(key=lambda x: x["room_type"])
    page["datas"] = ll

    for ele in ll:
        ele["pump"] = game_util.coin_translate(channel, ele["pump"])
        ele["robot_win"] = game_util.coin_translate(channel, ele["robot_win"])
        ele["water"] = game_util.coin_translate(channel, ele["water"])
        ele["accwater"] = game_util.coin_translate(channel, ele["accwater"])

    return render_template('maniplate_full_handicaper.html', page=page)


## 全盘控设置
@busi.route('/games/maniplate/fullhandicaper_set', methods=['POST'])
@login_require
def maniplate_full_handicaper_set():
    channel = session['select_channel']
    subgame = int(request.form.get("subgame"))
    water = int(request.form.get("water"))
    check = request.form.get("check")[:-1]

    room_id_list = []
    for room in check.split(","):
        [room_id, room_name] = room.split("_")
        room_id_list.append(room_id)
        sql = '''
            insert into admin_opt_log 
                (channel, maintype, log_type, operator, obj, 
                val, timestamp)
            values 
                (%d, %d, %d, %d, %s, 
                '%s', %d)
            ''' % (channel, log_main_type_d["win_ctl"], log_type_d["full_game_ctl"], session['user_id'], subgame,
                   room_name + "_" + str(water), time_util.now_sec())
        LogQry(channel).execute(sql)

    room_id_str = ",".join(room_id_list)
    print {"gameid": subgame, "gametype": room_id_str, "water": water}
    Result = GameWeb(channel).post("/api/subgame_ctl",
                                   {"gameid": subgame, "gametype": room_id_str, "water": water})
    print Result
    return jsonify(Result)
