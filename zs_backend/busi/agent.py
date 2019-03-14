# -*- coding:utf-8 -*-
import json
import time
from flask import render_template, jsonify, url_for
from flask.globals import session, request, current_app
from werkzeug.utils import redirect
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import time_util, game_util
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require

# 用于初始化页面显示的状态信息
from zs_backend.utils.time_util import formatDateTime, formatDatestamp


def init_status_msg(begin=True, end=True, is_active=None, channel=None, OThers_list=[]):
    status_msg = dict()
    if begin:
        status_msg['beginDate'] = begin
    else:
        status_msg['beginDate'] = False

    if end:
        status_msg['endDate'] = end
    else:
        status_msg['endDate'] = False

    if channel != None:
        status_msg['channel'] = int(channel)

    if is_active != None:
        status_msg['is_active'] = int(is_active)

    OThers = []
    for value_dict in OThers_list:
        for key, value in value_dict.items():
            if key == "id":
                id_check_box = u'''
                    <td colspan=1>
                        代理ID：<input type="text" id="player_id" name="player_id" value="%s"> 
                    </td> ''' % value
                OThers.append(id_check_box)
            if key == "status":
                status_selected = u'''
                    <td colspan=1>
                        代理状态：<select id="is_active" name="is_active">
                                <option value="-1">全部</option>
                                <option value="0">停用</option>
                                <option value="1">启用</option>
                            </select>
                    </td>'''
                OThers.append(status_selected)
            if key == "add":
                add_check_box = u"""
                    <td colspan=1>
                        <input type="button" id="add_agent" onclick="link_to()" class="btn btn-primary btn-sm" 
                        value="添加代理"/>
                    </td>"""
                OThers.append(add_check_box)
    status_msg['OThers'] = OThers
    return status_msg


@busi.route('/games/agent/presentation', methods=['GET'])
@login_require
def show_agent_presentation():
    status_msg = init_status_msg(OThers_list=[{'id': ''}], begin=11, end=11)

    return render_template('agent_presentation_daily.html', status_msg=status_msg, datas={})


def init_agent_daily_data():
    return {
        "dateStamp": 0,
        "total_agent_recv": 0,
        "total_agent_recv_pump": 0,
        "total_agent_present": 0,
        "total_agent_present_pump": 0,
        "total_down_coin": 0,
        "total_down_pump": 0,
        "total_up_coin": 0,
        "total_up_coin_pump": 0
    }


@busi.route('/search/games/agent/presentation', methods=['GET'])
@login_require
def search_agent_presentation():
    start = request.args.get('beginDate', '')
    end = request.args.get('endDate', '')
    player_id = request.args.get('player_id', '')
    channel = session['select_channel']

    start_date = formatDatestamp(start)
    end_date = formatDatestamp(end)

    if start_date > end_date:
        return jsonify(result='fail', msg=u'结束时间不能小于开始时间！')

    where1 = ""
    where2 = ""
    if player_id:
        where1 = "and give_id = %s" % player_id
        where2 = "and recv_id = %s" % player_id

    datas = {}
    PIDS = {}
    start_date1 = start_date
    while start_date1 <= end_date:
        ## 查询当日赠送情况
        date = time_util.formatDate(start_date1)
        sql = '''
            SELECT give_id, sum(if(recv_agent = 0, money, 0)), sum(if(recv_agent = 0, pump, 0)), 
                    sum(if(recv_agent = 1, money, 0)), sum(if(recv_agent = 1, pump, 0))
            FROM log_bank_give 
            WHERE time>=%d 
            AND time<=%d 
            AND give_agent = 1
            %s
            group by give_id
        ''' % (start_date1, start_date1 + 86400, where1)
        for line in LogQry(channel).qry(sql):
            PIDS[str(line[0])] = True
            r = init_agent_daily_data()
            r["dateStamp"] = date
            r["total_down_coin"] = float(line[1])
            r["total_down_coin_pump"] = float(line[2])
            r["total_agent_present"] = float(line[3])
            r["total_agent_present_pump"] = float(line[4])
            datas[line[0]] = r

        ## 查询当日被赠送情况
        sql = '''
            SELECT recv_id, sum(if(give_agent = 0, money, 0)), sum(if(give_agent = 0, pump, 0)), 
                    sum(if(give_agent = 1, money, 0)), sum(if(give_agent = 1, pump, 0))
            FROM log_bank_give 
            WHERE time>=%d 
            AND time<=%d 
            AND recv_agent = 1
            %s
            group by recv_id
        ''' % (start_date1, start_date1 + 86400, where2)
        for line in LogQry(channel).qry(sql):
            PIDS[str(line[0])] = True
            if datas.has_key(line[0]):
                r = datas[line[0]]
            else:
                r = init_agent_daily_data()
            r["dateStamp"] = date
            r["total_up_coin"] = float(line[1])
            r["total_up_coin_pump"] = float(line[2])
            r["total_agent_recv"] = float(line[3])
            r["total_agent_recv_pump"] = float(line[4])
            datas[line[0]] = r

        start_date1 += 86400
    ## 查询这些代理的昵称
    pdatas = {}
    if PIDS:
        sql = '''
            select id, nick 
            from player
            where id in (%s)
        ''' % ",".join(PIDS.keys())
        for line in LogQry(channel).qry(sql):
            pdatas[line[0]] = line[1]

    return jsonify(result='ok', data=datas, pdatas=pdatas)
