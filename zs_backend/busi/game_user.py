# -*- coding:utf-8 -*-
import json

from flask import render_template, jsonify, url_for
from flask.globals import session, request, g, current_app
from werkzeug.utils import redirect
from zs_backend.busi.agent_list import map_agent_status
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
from zs_backend.utils import game_util
from zs_backend.busi import game_parameter
from zs_backend.utils import erl
from zs_backend.utils.game_util import set_zfb_info, set_bank_info
from zs_backend.utils.log_table import *
import struct

player_state_d = {
    "ban": u"封号",
    "online": u"在线",
    "whitelist": u"白名单",
    "blacklist": u"黑名单",
    "lock": u"资金冻结"
}


@busi.route('/games/users/datas', methods=['GET'])
@login_require
def manage_game_user():
    status_msg = dict()
    status_msg['beginDate'] = True
    status_msg['endDate'] = True
    status_msg['endDate'] = True
    status_msg['OThers'] = [
        u'<select id="level"></select>',
        u'注册IP：<input type="text" id="reg_ip">'
    ]

    return render_template('user_manage.html', status_msg=status_msg, pdatas={})


@busi.route('/search/games/users/datas', methods=['GET'])
@login_require
def search_game_user_data():
    start = request.args.get('beginDate', '')
    end = request.args.get('endDate', '')
    player_id = request.args.get('PlayerID', '')
    nick = request.args.get('NickName', '')
    reg_ip = request.args.get('reg_ip', '')
    # 接收渠道id
    channel = session['select_channel']
    level = int(request.args.get('level', ''))

    offset = int(request.args.get("offset"))
    pagesize = int(request.args.get("size"))

    Where = ""
    if player_id:
        Where += " AND p.id='%s'" % player_id
    if nick:
        Where += " AND p.nick='%s'" % nick
    if level > 0:
        Where += " AND p.vip=%d" % level
    if reg_ip:
        Where += " AND p.reg_ip='%s'" % reg_ip

    ## 判断是否是当日查询
    start_date = time_util.formatTimestamp(start)
    end_date = time_util.formatTimestamp(end)
    Where += ' AND p.reg_time >= %d ' % start_date
    Where += ' AND p.reg_time <= %d ' % end_date

    ## 查询满足条件的所有玩家
    sql = '''
        select count(1)
        from player p
        where 1 = 1
        %s
    ''' % Where
    total_count = LogQry(channel).qry(sql)[0][0]

    ## 查询所有层级
    memberl_lv = {}
    sql = '''
        select id, member_level_name
        from admin_member_level
    '''
    for k, v in LogQry(channel).qry(sql):
        memberl_lv[k] = v

    sql = '''
        select p.id, p.nick, p.reg_time, p.coin, 
                ifnull((select invite_id from player_agent where pid = p.id), ""),
            p.counter, p.last_login_time, p.account_id, p.vip, p.reg_ip
        from player as p
        where 1 =1 
        %s
        order by p.reg_time desc
        limit %d,%d
    ''' % (Where, offset, pagesize)
    pdatas = []
    for line in LogQry(channel).qry(sql):
        try:
            memberl_lv_name = memberl_lv[max(line[8], 1)]
        except:
            memberl_lv_name = line[8]
        d = {
            "id": line[0],
            "nick": line[1].encode("utf-8"),
            "reg_time": line[2],
            "coin": line[3] + game_util.get_bank_coin(line[5]),
            "agent": line[4],
            "last_login_time": line[6],
            "account_id": line[7],
            "memberl_lv": memberl_lv_name,
            "reg_ip": line[9]
        }
        pdatas.append(d)

    return jsonify({"errcode": 0, "dataLength": total_count, "rowDatas": pdatas})


@busi.route('/games/users/datas/details', methods=['GET'])
@login_require
def get_game_user_detail():
    status_msg = dict()
    status_msg['beginDate'] = False
    status_msg['endDate'] = False
    status_msg['access_level'] = session['access_level']
    status_msg['PlayerID'] = ""
    status_msg['NickName'] = ""
    status_msg['date1'] = time_util.formatDate(time_util.now_sec() - 7 * 86400)
    status_msg['date2'] = time_util.formatDate(time_util.now_sec())

    return render_template('user_game_detail.html', status_msg=status_msg, base_player={})


@busi.route('/search/games/users/datas/game_data_tj', methods=['GET'])
@login_require
def search_game_user_data_tj():
    channel = session['select_channel']
    PID = request.args.get('PlayerID', '')
    NickName = request.args.get('NickName', '')
    Account = request.args.get('Account', '')
    date1 = time_util.formatTimeWithDesc(time_util.formatDatestamp(request.args.get('date1')), "%Y%m%d")
    date2 = time_util.formatTimeWithDesc(time_util.formatDatestamp(request.args.get('date2')), "%Y%m%d")

    # 校验参数
    if not PID and not NickName and not Account:
        return jsonify(result='failed', msg=u'请输入玩家账号或玩家ID或玩家昵称！')
    if (PID and NickName) or (PID and Account) or (NickName and Account):
        return jsonify(result='failed', msg=u'玩家账号、玩家ID、玩家昵称只能输入其一！')

    # 玩家账号、玩家昵称转换成玩家ID
    if NickName:
        retrieve_sql = """SELECT id FROM player WHERE nick='{}';""".format(NickName)
        try:
            PID = LogQry(channel).qry(retrieve_sql)[0][0]
        except IndexError:
            return jsonify(result='failed', msg=u'该玩家不存在！')
    elif Account:
        retrieve_sql = """SELECT id FROM player WHERE account_id='{}';""".format(Account)
        try:
            PID = LogQry(channel).qry(retrieve_sql)[0][0]
        except IndexError:
            return jsonify(result='failed', msg=u'该玩家不存在！')

    subgame_list = game_parameter.get_subgame_list()

    sql = '''
        select time, gameid, sum(game_count), sum(stake_coin), sum(output_coin),
            (select ifnull(sum(today_recharge), 0) from t_player_general where time = a.time and pid = a.pid),
                (select ifnull(sum(today_withdraw), 0) from t_player_general where time = a.time and pid = a.pid),
                (select ifnull(sum(bankrupt_times), 0) from t_player_general where time = a.time and pid = a.pid)
        from t_player_subgame a
        where time >= %s and time <= %s
        and pid = %s
        group by time, gameid
        order by time desc
    ''' % (date1, date2, PID)

    datas = []
    for search_data in LogQry(channel).qry(sql):
        pre_record = {}
        pre_record['time'] = search_data[0]
        pre_record['game_id'] = game_parameter.get_subgame_by_id(subgame_list, search_data[1])
        pre_record['game_count'] = int(search_data[2])
        pre_record['stake_coin'] = int(search_data[3])
        pre_record['win_coin'] = int(search_data[4])
        pre_record['total_win'] = pre_record['stake_coin'] - pre_record['win_coin']
        pre_record['today_recharge'] = int(search_data[5])
        pre_record['today_withdraw'] = int(search_data[6])
        pre_record['bankrupt_count'] = int(search_data[7])
        datas.append(pre_record)

    total_count = len(datas)

    return jsonify({"errcode": 0, "dataLength": total_count, "rowDatas": datas})


@busi.route('/search/games/users/datas/prestented_data_tj', methods=['GET'])
@login_require
def prestented_data_tj():
    PID = request.args.get('PlayerID', '')
    # 接收渠道id
    channel = session['select_channel']
    NickName = request.args.get('NickName', '')
    date1 = time_util.formatDatestamp(request.args.get('date1'))
    date2 = time_util.formatDatestamp(request.args.get('date2')) + 86400

    ## 查询玩家ID
    Where = ""
    if NickName:
        Where += "and nick = '%s'" % NickName
    if PID:
        Where += " and id = %s" % PID
    print "WHERE:", Where
    if not Where:
        return jsonify([])
    PID = LogQry(channel).qry("select id from player where 1 =1 %s" % Where)[0][0]

    sql = '''
        select time, give_id, recv_id, money, pump
        from log_bank_give
        where time >= %d and time <= %d
        and (give_id = %d or recv_id = %d)
        order by time
    ''' % (date1, date2, PID, PID)

    datas = []
    pre_date = 0
    pre_record = {}
    print sql
    for search_data in LogQry(channel).qry(sql):
        cur_date = time_util.formatDate(search_data[0])

        if cur_date == pre_date:
            if search_data[1] == PID:
                ## 卖分
                pre_record["down_coin"] = pre_record["down_coin"] + search_data[3]
            if search_data[2] == PID:
                ## 卖分
                pre_record["up_coin"] = pre_record["up_coin"] + search_data[3]
            pre_record["pump"] = pre_record["pump"] + search_data[4]
            pre_record["count"] = pre_record["count"] + 1
            continue

        if pre_record:
            datas.append(pre_record)

        pre_record = {}
        pre_date = cur_date
        pre_record['time'] = cur_date
        pre_record["up_coin"] = 0
        pre_record["down_coin"] = 0
        if search_data[1] == PID:
            ## 卖分
            pre_record["down_coin"] = search_data[3]
        if search_data[2] == PID:
            ## 卖分
            pre_record["up_coin"] = search_data[3]
        pre_record["pump"] = search_data[4]
        pre_record["count"] = 1

    if pre_record:
        datas.append(pre_record)

    total_count = len(datas)

    return jsonify({"errcode": 0, "dataLength": total_count, "rowDatas": datas})


@busi.route('/search/games/users/datas/details', methods=['GET'])
@login_require
def search_game_user_detail():
    PID = request.args.get('PlayerID', '')
    NickName = request.args.get('NickName', '')
    Account = request.args.get('Account', '')
    # 接收渠道id
    channel = session['select_channel']

    if (PID and NickName) or (PID and Account) or (NickName and Account):
        return jsonify(result=0, msg=u'玩家ID、玩家昵称、玩家账号只能输入其一！')

    WHERE = ""
    if PID:
        WHERE += " and id = %s" % PID
    if NickName:
        WHERE += " and nick = '%s'" % NickName
    if Account:
        WHERE += " and account_id = '%s'" % Account

    if not WHERE:
        return jsonify(result='failed', msg=u'请输入玩家ID或玩家昵称或玩家账号！')

    sql = '''
        select id, nick, reg_time, client_id, reg_ip,
            coin, account_id, device, did, last_login_ip,
            phone, last_login_time, did, subgame, total_recharge_rmb,
            total_withdraw, time_long, 
                (select ifnull(sum(game_count), 0) from t_player_subgame where pid = a.id)
        from player a
        where 1=1 %s
    ''' % WHERE

    base_player = {}
    for line in LogQry(channel).qry(sql):
        base_player["id"] = line[0]
        base_player["nick"] = line[1]
        base_player["reg_time"] = time_util.formatDateTime(line[2])
        base_player["channel_id"] = line[3]
        base_player["reg_ip"] = line[4]
        base_player["account_id"] = line[6]

        base_player["phone"] = line[10]

        try:
            r = GameWeb(channel).post("/api/get_player_info", {'pid': int(line[0])})
            coin = r['result']['coin']
            bank = r['result']['dep']
            base_player["coin"] = game_util.coin_translate(channel, coin)
            base_player["banker"] = game_util.coin_translate(channel, bank)
            vip = r["result"]['vip']
            counter = r['result']["counter"]
            counter = "".join([struct.pack("B", int(x)) for x in counter])
            bank, acc, name, addr = game_util.get_bank_info(counter)
            base_player["bank_no"] = "%s/%s/%s" % (bank, acc, addr)
            base_player["bank_acc"] = name
            acc, name = game_util.get_zfb_info(counter)
            base_player["zfb"] = "%s/%s" % (acc, name)
            status = r['result']["ban"]
            status = "".join([struct.pack("B", int(x)) for x in status])
            base_player["status"] = get_player_state(status)
            sql = 'select member_level_name from admin_member_level where id = %d' % int(vip)
            base_player["vip"] = LogQry(channel).qry(sql)[0][0]
        except BaseException as e:
            print "qry user detail..", e
            pass

        base_player["platform"] = line[7]
        base_player["did"] = line[8]
        base_player["last_login_ip"] = line[9]
        base_player["last_login_time"] = time_util.formatDateTime(line[11])
        base_player["did"] = line[12]

        base_player["subgame"] = game_parameter.get_subgame_name(line[13])
        base_player["total_recharge_rmb"] = line[14]

        base_player["total_withdraw"] = line[15]
        base_player["time_long"] = line[16] / 60
        base_player["game_count"] = int(line[17])

        ## 查询新手卡数
        sql = '''
            select count(1)
            from log_activity
            where activity_type = 4
            and detail like '[%s,[%%'
        ''' % line[0]
        base_player["newbie_card"] = LogQry(channel).qry(sql)[0][0]

        ## 查询代理相关信息
        sql = '''
            select (select level_name from admin_agent_level where id = agent_level), status
            from admin_agent_list a
            where pid = %d
        ''' % line[0]
        try:
            agent_lv, agent_status = LogQry(channel).qry(sql)[0]
            base_player["agent_status"] = map_agent_status[int(agent_status)]
            base_player["agent_lv"] = agent_lv
        except:
            base_player["agent_status"] = ""
            base_player["agent_lv"] = ""

        ## 查询推广玩家数
        sql = '''
            select p_code, invite_id, invite_code, (select count(1) from player_agent where invite_id = %d)
            from player_agent
            where pid = %d
        ''' % (line[0], line[0])
        try:
            (p_code, invite_id, invite_code, invite_count) = LogQry(channel).qry(sql)[0]
            base_player["p_code"] = p_code
            base_player["invite_id"] = invite_id
            base_player["invite_code"] = invite_code
            base_player["invite_count"] = invite_count
        except BaseException as e:
            # print "qry agent info...", e
            base_player["p_code"] = ""
            base_player["invite_id"] = 0
            base_player["invite_code"] = ""
            base_player["invite_count"] = 0

    return jsonify(result="ok", data=base_player)

def get_player_state(Data):
    val = erl.binary_to_term(Data)
    s = []
    reason = ""
    time = ""
    try:
        for k, v in val:
            if k == "reason":
                reason = v
            elif k == "time":
                time = time_util.formatDateTime(int(v))
            elif v == 1:
                s.append(player_state_d[k])
        if not s:
            return ""
        ss = "/".join(s)
        if reason:
            return "%s(%s %s)" % (ss, reason, time)
        return ss
    except:
        return ""
