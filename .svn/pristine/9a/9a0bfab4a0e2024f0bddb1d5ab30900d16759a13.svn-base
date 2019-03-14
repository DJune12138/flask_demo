# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g, session
from zs_backend.sql import SqlOperate
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require
from . import busi


@busi.route('/game/data/compare', methods=['GET'])
@login_require
def game_data_compare():
    beginDate1 = time_util.formatTimeWithDesc(time_util.now_sec() - 86400, '%Y-%m-%d')
    endDate1 = time_util.formatTimeWithDesc(time_util.now_sec() - 86400, '%Y-%m-%d')
    beginDate2 = time_util.formatTimeWithDesc(time_util.now_sec(), '%Y-%m-%d')
    endDate2 = time_util.formatTimeWithDesc(time_util.now_sec(), '%Y-%m-%d')
    status_msg = dict()
    status_msg['beginDate'] = False
    status_msg['endDate'] = False
    status_msg['OThers'] = [u'''<td colspan=1>
                                    日期1：<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:\'yyyy-mm-dd\'})" 
                                        id="beginDate1" name="beginDate1" value="%s" required>
                                    --<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:\'yyyy-mm-dd\'})" 
                                        id="endDate1" name="endDate1" value="%s" required> 
                            </td> ''' % (beginDate1, endDate1),
                            u'''<td colspan=1>数据对比</td> ''',
                            u'''<td colspan=1>
                                    日期2：<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:\'yyyy-mm-dd\'})" 
                                        id="beginDate2" name="beginDate2" value="%s" required>
                                    --<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:\'yyyy-mm-dd\'})" 
                                        id="endDate2" name="endDate2" value="%s" required> 
                            </td> ''' % (beginDate2, endDate2)]

    return render_template('game_data_compare.html', status_msg=status_msg, pre={}, cur={})


@busi.route('/search/game/data/compare', methods=['GET'])
@login_require
def search_game_data_compare():
    start1 = request.args.get('beginDate1', '')
    end1 = request.args.get('endDate1', '')
    start2 = request.args.get('beginDate2', '')
    end2 = request.args.get('endDate2', '')
    channel = session['select_channel']

    start_date1 = time_util.start(start1)
    end_date1 = time_util.end(end1)
    start_date2 = time_util.start(start2)
    end_date2 = time_util.end(end2)

    if start_date1 > end_date1 or start_date2 > end_date2:
        return jsonify(result='fail', msg=u'结束时间不能小于开始时间！')

    # --------------------------
    # 页面左边日期输入框所查数据
    start_time1 = int(time_util.formatTimeWithDesc(start_date1, "%Y%m%d"))
    end_time1 = int(time_util.formatTimeWithDesc(end_date1, "%Y%m%d"))

    game_normal_sql_1 = """
            SELECT time, os, reg_count, active_count, total_recharge, game_win, withdraw
            FROM t_system
            WHERE time>=%d AND time<%d
            order by time desc;
        """ % (start_time1, end_time1)
    print 'game_normal_sql_1', game_normal_sql_1
    print LogQry(channel).qry(game_normal_sql_1)
    left_record = {
        "reg_count": 0,
        "active_count": 0,
        "game_win": 0,
        "up_coin": 0,
        "down_coin": 0,
        "recharge": 0,
        "withdraw": 0
    }
    left_pre_date = 0
    for time_int, platform, reg_count, active_count, total_recharge, game_win, withdraw in LogQry(channel).qry(
            game_normal_sql_1):
        left_record['reg_count'] += reg_count
        left_record['active_count'] += active_count
        left_record['recharge'] += total_recharge
        left_record['game_win'] += game_win
        left_record['withdraw'] += withdraw

    bank_give_sql_1 = """SELECT give_agent, recv_agent, money 
                            FROM log_bank_give
                            WHERE time>=%d AND time<%d 
                            AND ((give_agent=1 AND recv_agent=0) 
                            OR (give_agent=0 AND recv_agent=1));
                            """ % (start_date1, end_date1 + 86400)
    for give_agent, recv_agent, money in LogQry(channel).qry(bank_give_sql_1):
        if give_agent == 1:
            left_record['down_coin'] += money
        elif recv_agent == 1:
            left_record['up_coin'] += money
    print left_record, "left_record"
    # --------------------------
    # 页面右边日期输入框所查数据
    start_time2 = int(time_util.formatTimeWithDesc(start_date2, "%Y%m%d"))
    end_time2 = int(time_util.formatTimeWithDesc(end_date2, "%Y%m%d"))

    game_normal_sql_2 = """
            SELECT time, reg_count, active_count, total_recharge, game_win, withdraw
            FROM t_system
            WHERE time>=%d AND time<%d
            order by time desc;
        """ % (start_time2, end_time2)
    print game_normal_sql_2, start_time2

    right_record = {
        "reg_count": 0,
        "active_count": 0,
        "game_win": 0,
        "up_coin": 0,
        "down_coin": 0,
        "recharge": 0,
        "withdraw": 0
    }
    right_pre_date = 0
    for time_int, reg_count, active_count, total_recharge, game_win, withdraw in LogQry(channel).qry(
            game_normal_sql_2):
        right_record['reg_count'] += reg_count
        right_record['active_count'] += active_count
        right_record['recharge'] += total_recharge
        right_record['game_win'] += game_win
        right_record['withdraw'] += withdraw

    bank_give_sql_2 = """SELECT give_agent, recv_agent, money 
                            FROM log_bank_give
                            WHERE time>=%d AND time<%d 
                            AND ((give_agent=1 AND recv_agent=0) 
                            OR (give_agent=0 AND recv_agent=1));
                            """ % (start_date2, end_date2 + 86400)
    for give_agent, recv_agent, money in LogQry(channel).qry(bank_give_sql_2):
        if give_agent == 1:
            right_record['down_coin'] += money
        elif recv_agent == 1:
            right_record['up_coin'] += money

    return jsonify(result='ok', pre=left_record, cur=right_record)
