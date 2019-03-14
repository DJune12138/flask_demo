# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require
from flask import render_template, request, jsonify, session
from zs_backend.utils import log_table
from zs_backend.busi import game_parameter
from zs_backend.utils import game_util
import json


@busi.route('/show/game/detail', methods=['GET'])
@login_require
def show_game_detail():
    """每局游戏详情页面"""

    other_msg = dict()
    line = ['<option value="0">全部</option>']
    for k, v in game_parameter.get_subgame_list().items():
        l = '<option value="%d">%s</option>' % (k, v)
        line.append(l)

    game_select = u'''
            <td colspan=1>
                游戏：<select id="game" name="game">
                        %s
                    </select>
            </td>
            <span>局号：</span>
    <input type="text" name="code" placeholder="请输入数量" id="code"/>''' % "\n".join(line)

    other_msg['others'] = [game_select]

    return render_template('game_detail.html', other_msg=other_msg)


@busi.route('/game/detail/retrieve', methods=['GET'])
@login_require
def game_detail_retrieve():
    """每局游戏详情查询"""

    # 获取参数
    channel = session['select_channel']
    gameid = request.args.get('game')
    auto_id = request.args.get('code')
    pid = request.args.get('PlayerID')
    account_id = request.args.get('Account')
    begin_date = request.args.get('beginDate')
    end_date = request.args.get('endDate')
    time_start = request.args.get('time_start')
    time_end = request.args.get('time_end')
    size = request.args.get('size')
    offset = request.args.get('offset')

    # 校验参数
    if auto_id:
        try:
            int(auto_id)
        except ValueError as e:
            return jsonify(result=0, msg=u'局号为整数纯数字！')
    if pid:
        try:
            int(pid)
        except ValueError as e:
            return jsonify(result=0, msg=u'玩家ID为整数纯数字！')
    if pid and account_id:
        return jsonify(result=0, msg=u'玩家ID与玩家账号只能填其一！')

    # 处理参数
    where = ''
    if pid:
        where += ' AND pid=%s' % pid
    if account_id:
        where += " AND pid=(select id from player where account_id='%s')" % account_id
    if auto_id:
        where += ' AND auto_id=%s' % auto_id
    if gameid != '0':
        where += ' AND gameid=%s' % gameid
    # right_date = begin_date  # 用于返回当天23点59分59秒
    # begin_date_str = begin_date + ' ' + time_start + ':00'
    # end_date_str = begin_date + ' ' + time_end + ':00'
    # try:
    #     begin_date = time_util.formatTimestamp(begin_date_str)
    # except ValueError:
    #     begin_date = time_util.formatDatestamp(begin_date)  # 当天0点0分0秒
    # try:
    #     end_date = time_util.formatTimestamp(end_date_str)
    # except ValueError:
    #     end_date = time_util.formatDatestamp(right_date) + 86399  # 当天23点59分59秒
    begin_date = time_util.formatTimestamp(begin_date)
    end_date = time_util.formatTimestamp(end_date)
    data_table_name = log_table.get_table_log_player_subgame(begin_date)

    # 校验开始时间是否小于结束时间
    if begin_date >= end_date:
        return jsonify(result=0, msg=u'开始时间必须小于结束时间！')

    # 查询数据总量
    retrieve_sql = """SELECT count(1),ifnull(sum(stake_coin), 0),ifnull(sum(output_coin), 0),ifnull(sum(pump), 0)
                      FROM %s force index(time) 
                      WHERE time>=%s 
                      AND time<=%s
                      %s;""" \
                   % (data_table_name, begin_date, end_date, where)
    try:
        total_all = LogQry(int(channel)).qry(retrieve_sql)[0]
    except Exception as e:
        print e
        return jsonify(result=0, msg=u'无数据！')
    total_count = total_all[0]
    total_stake_coin = total_all[1]
    total_output_coin = total_all[2]
    total_pump = total_all[3]

    # 从数据库获取数据
    retrieve_sql = """SELECT time,pid,gameid,roomtype,stake_coin,
                        output_coin,pump,auto_id,(select account_id from player where id=pid),
                          (select nick from player where id=pid) 
                      FROM %s force index(time) 
                      WHERE time>=%s 
                      AND time<=%s
                      %s 
                      ORDER BY time DESC 
                      LIMIT %s,%s;""" \
                   % (data_table_name, begin_date, end_date, where, offset, size)
    datas = LogQry(int(channel)).qry(retrieve_sql)

    # 处理数据
    game_dict = game_parameter.get_subgame_list()
    datas_list = list()
    for time, pid, gameid, roomtype, stake_coin, \
        output_coin, pump, auto_id, account_id, nick in datas:
        data_dict = dict()
        data_dict['time'] = time
        data_dict['account'] = account_id
        data_dict['pid'] = pid
        data_dict['nick'] = nick
        data_dict['game_name'] = game_parameter.get_subgame_by_id(game_dict, gameid)
        data_dict['room_type'] = roomtype
        data_dict['stake_coin'] = stake_coin
        data_dict['output_coin'] = output_coin
        data_dict['pump'] = pump
        data_dict['margin'] = output_coin - stake_coin
        data_dict['auto_id'] = auto_id
        data_dict['channel'] = channel
        datas_list.append(data_dict)
    total_dict = dict()
    total_dict['total_stake_coin'] = int(total_stake_coin)
    total_dict['total_output_coin'] = int(total_output_coin)
    total_dict['total_pump'] = int(total_pump)
    total_dict['total_margin'] = int(total_output_coin - total_stake_coin)

    # 返回数据
    return jsonify(result=1, dataLength=total_count, rowDatas=datas_list, total_all=total_dict)


@busi.route('/game/position/detail/retrieve', methods=['GET'])
@login_require
def game_position_detail_retrieve():
    """对局详情查询"""

    # 获取参数
    auto_id = request.args.get('auto_id')
    time = request.args.get('time')
    channel = session['select_channel']

    # 处理参数
    data_table_name = log_table.get_table_log_subgame(int(time))

    # 从数据库获取数据
    retrieve_sql = """
        SELECT gameid, detail 
        FROM %s 
        WHERE auto_id=%s;
    """ % (data_table_name, auto_id)
    gameid, detail = LogQry(int(channel)).qry(retrieve_sql)[0]

    dd = []
    detail_config = game_parameter.detail_config()
    define = game_parameter.detail_define()
    try:
        ll = json.loads(detail)

        ## 遍历每条记录
        for line in ll:
            ## 对每条记录继续遍历
            ss = []
            for k, v in line:
                try:
                    df = define[int(k)]
                    if df["type"] == "coin":
                        ss.append("【%s】: %s" % (df["txt"], str(game_util.coin_translate(int(channel), int(v)))))
                    elif df["type"] == "pid":
                        if int(v) < 90001:
                            ss.append("【%s】: %s" % (df["txt"], str(v)))
                        else:
                            sql = "select account_id from player where id = %s" % v
                            acc = LogQry(int(channel)).qry(sql)[0][0]
                            ss.append("【%s】: %s(%s)" % (df["txt"], str(v), acc))
                    elif df["type"] == "desc":
                        ss.append("【%s】: %s" % (df["txt"], df["kv"][int(v)]))
                    elif df["type"] == "config":
                        ## 此处需要解析配置
                        v = v if type(v) == type([]) else [v]
                        tl = []
                        for ele in v:
                            try:
                                tl.append(detail_config[gameid][ele])
                            except BaseException, e:
                                print "game_detail_config...", gameid, ele
                                tl.append(str(ele))

                        ss.append("【%s】: %s" % (df["txt"], " ".join(tl)))
                    else:
                        ss.append("【%s】: %s" % (df["txt"], str(v)))
                except BaseException, e:
                    print "game_detail", k, v
                    ss.append("【%s】: %s" % (str(k), str(v)))

            dd.append(ss)
    except BaseException, e:
        print e
        pass

    # 返回数据
    return jsonify(src=detail, items=dd)
