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
from zs_backend.utils import erl
from zs_backend.utils.log_table import *

from copy import deepcopy

single_player_page = {
    "loseControlNum": 0,
    "loseControlMoney": 0,
    "winControlNum": 0,
    "winControlMoney": 0,
    "filterType_1_1": 0,
    "filterType_1_2": 0,
    "filterType_2_1": 0,
    "filterType_2_2": 0,
    "filterType_3_1": 0,
    "filterType_3_2": 0,
    "filterTypeVal": "0,,,,",
    "datas": [],
    "subgamelist": [],
    "filter": [],

    "other_qry": []
}


def get_total_ctl_info(channel):
    sql = '''
        select sum(if(water > 0, 1, 0)), sum(if(water > 0, water, 0)), 
                    sum(if(water < 0, 1, 0)), sum(if(water < 0, water, 0))
        from player
    '''
    return LogQry(channel).qry(sql)[0]


def query_single_player_html(PlayerStatus=0, TotalWin="", ProtectStatus=0,
                             IP="", filterTypeVal="0,,,,,,"):
    SELECTED0 = ""
    SELECTED1 = ""
    if PlayerStatus == 0:
        SELECTED0 = "selected"
    else:
        SELECTED1 = "selected"
    playerstatus = u'''
        <td>玩家状态：
            <select id="playerstatus" name="playerstatus"> 
                <option value="0" %s>全部</option> 
                <option value="1" %s>在线</option> 
            </select>
        </td>''' % (SELECTED0, SELECTED1)

    totalwin = u'''
        <td>总输赢：
            <input type="text" id="totalwin" name="totalwin" value="%s"> 
        </td>''' % TotalWin

    ip = u'''<td>IP地址：<input type="text" id="ip" name="ip" value="%s"> </td>''' % IP

    SELECTED0 = ""
    SELECTED1 = ""
    SELECTED2 = ""
    if ProtectStatus == 0:
        SELECTED0 = "selected"
    elif ProtectStatus == 1:
        SELECTED1 = "selected"
    else:
        SELECTED2 = "selected"
    protectstatus = u'''
        <td>保护状态：
            <select id="protectstatus" name="protectstatus"> 
                <option value="0" %s>全部</option> 
                <option value="1" %s>保护中</option> 
                <option value="2" %s>未保护</option> 
            </select>
            <input type="text" id="filterTypeVal" name="filterTypeVal" value="%s" hidden>
        </td>''' % (SELECTED0, SELECTED1, SELECTED2, filterTypeVal)

    return [playerstatus, totalwin, ip, protectstatus]


## 单控玩家输赢
@busi.route('/games/maniplate/oneplayer', methods=['GET'])
@login_require
def maniplate_single_player():
    page = deepcopy(single_player_page)
    page["other_qry"] = query_single_player_html()

    return render_template('maniplate_single_player.html', page=page)


## 单控玩家输赢
@busi.route('/games/maniplate/oneplayer', methods=['POST'])
@login_require
def maniplate_single_player_post():
    page = deepcopy(single_player_page)

    data = request.form

    PlayerStatus = int(data.get("playerstatus"))
    PlayerID = data.get("PlayerID").strip()
    NickName = data.get("NickName")
    Channel = session['select_channel']
    TotalWin = data.get("totalwin").strip()
    ProtectStatus = int(data.get("protectstatus"))
    IP = data.get("ip").strip()

    ctl_info = get_total_ctl_info(Channel)
    page["winControlNum"] = int(float(ctl_info[0]))
    page["winControlMoney"] = game_util.coin_translate(Channel, int(ctl_info[1]))
    page["loseControlNum"] = int(float(ctl_info[2]))
    page["loseControlMoney"] = game_util.coin_translate(Channel, int(ctl_info[3]))

    if PlayerStatus == 1:
        ## 查询在线玩家  那没办法 只能去erlang那边请求了
        payLoad = {"PlayerID": PlayerID, "NickName": NickName, "TotalWin": TotalWin,
                   "ProtectStatus": ProtectStatus, "IP": IP}
        page["datas"] = GameWeb(Channel).post("/api/player_ctl_qry", payLoad)
    elif PlayerStatus == 0:
        ## 查询游戏列表
        subgamelist = game_parameter.get_subgame_list()

        ## 全部 那好吧 去游戏服的mysql查吧
        sql = '''
            select id, nick, coin, total_output - total_stake, today_output - today_stake, 
                "", water, set_water, acc_water, (select invite_id from player_agent where pid = id), 
                time_long, subgame, last_login_ip, last_set_water_time, ban
            from player
            where 1 = 1
        '''

        if PlayerID != "":
            sql += " and id = %s" % PlayerID
        if NickName != "":
            sql += " and nick = '%s'" % NickName
        if ProtectStatus == 1:
            sql += " and water <> 0"
        elif ProtectStatus == 2:
            sql += " and water = 0"
        if IP != "":
            sql += " and last_login_ip = '%s'" % IP

        QueryData = LogQry(Channel).qry(sql)
        if TotalWin != "":
            sql = '''
                select pid
                from (
                    select pid, (sum(output_coin - stake_coin)) as val
                    from t_player_subgame
                    where pid in ('%s')
                    group by pid
                    ) as a
                where val >= %s
            ''' % (",".join([str(i[0]) for i in QueryData]), TotalWin)
            pids = [i[0] for i in LogQry(Channel).qry(sql)]
            Datas = [i for i in QueryData if i[0] in pids]
        else:
            Datas = QueryData

        ## 处理玩家在线状态问题
        FinalDatas = []
        for item in Datas:
            item = list(item)
            subgame = erl.binary_to_term(item[11])
            if subgame[0] == "subgame_info":
                item[11] = game_parameter.get_subgame_by_id(subgamelist, subgame[1])
            else:
                item[11] = u""
                ban = erl.binary_to_term(item[14])
                for k, v in ban:
                    if k == "online" and v == 1:
                        item[14] = u"在线"
            item.pop()
            FinalDatas.append(item)

        page["datas"] = FinalDatas

    return jsonify(result='ok', data=page)

@busi.route('/games/maniplate/oneplayer_protect', methods=['POST'])
@login_require
def maniplate_single_player_protect():
    """设置玩家保护值"""

    # 获取参数
    detail = request.form.get('detail')
    Channel = session['select_channel']

    # 与游戏对接
    result = GameWeb(Channel).post("/api/player_ctl", {"pid_l": eval(detail)})

    # 处理数据
    sql_str = ''
    now_time = time_util.now_sec()
    for pid, water in eval(detail):
        sql_str += "({},{},{},{},{},'{}',{}),".format(Channel, log_main_type_d["win_ctl"], log_type_d["single_ctl"],
                                                      session['user_id'], pid, water, now_time)
    sql_str = sql_str.rstrip(',')

    # 记录操作日志
    create_sql = """INSERT INTO admin_opt_log (channel,maintype,log_type,operator,obj,
                                  val,timestamp)
                    VALUE %s;""" % sql_str
    LogQry(Channel).execute(create_sql)

    # 返回应答
    return jsonify(result=result)
