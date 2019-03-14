# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require
from flask import render_template, request, jsonify, session
from zs_backend.utils import time_util
from zs_backend.utils.property_id import id_map_property, overdue_map_id


@busi.route('/card/data/details', methods=['GET'])
@login_require
def show_card_data():
    """卡号数据查询页面"""

    other_msg = dict()
    other_msg['others'] = [u"""<select><option value="code">激活码</option><option value="PlayerID">玩家ID</option><option value="date">日期</option></select><input type="text" id="search_text"/>"""]
    other_msg['beginDate'] = True
    other_msg['endDate'] = True

    return render_template('card_data.html', other_msg=other_msg)


@busi.route('/card/data/retrieve', methods=['GET'])
@login_require
def card_data_retrieve():
    """卡号数据查询"""

    # 获取参数
    channel_id = session['select_channel']
    code = request.args.get('code')
    pid = request.args.get('PlayerID')
    begin_date = request.args.get('beginDate')
    end_date = request.args.get('endDate')
    size = request.args.get('size')
    offset = request.args.get('offset')

    # 校验并处理参数
    where_str = ''
    if code:
        code_list = list()
        for i in code:
            code_list.append(ord(i))
        code_str = str(code_list).replace(' ', '')
        where_str += " AND detail LIKE '%%,%s,%%'" % code_str
    elif pid:
        try:
            int(pid)
        except ValueError:
            return jsonify(result=0, msg=u'玩家ID为整数纯数字！')
        where_str += " AND detail like '[%s,[%%'" % pid
    elif begin_date and end_date:
        begin_date = time_util.formatTimestamp(begin_date)
        end_date = time_util.formatTimestamp(end_date)
        where_str += " AND time>=%s AND time<=%s" % (begin_date, end_date)

    # 从数据库获取数据
    retrieve_sql = """SELECT count(*)
                      FROM log_activity
                      WHERE activity_type=4
                      %s;""" % where_str
    total_count = LogQry(int(channel_id)).qry(retrieve_sql)[0][0]
    retrieve_sql = """SELECT detail,time
                      FROM log_activity
                      WHERE activity_type=4
                      %s
                      ORDER BY time DESC
                      LIMIT %s,%s;""" \
                   % (where_str, offset, size)
    datas = LogQry(int(channel_id)).qry(retrieve_sql)

    # 如果有数据就处理数据并返回
    if datas:
        datas_list = list()
        for detail, time in datas:
            data_dict = dict()
            detail_list = eval(detail)
            activation_code = ''
            for i in detail_list[1]:
                activation_code += chr(int(i))
            data_dict['activation_code'] = activation_code
            data_dict['type'] = detail_list[2]
            data_dict['award'] = id_map_property(str(detail_list[3]))
            data_dict['overdue_time'] = overdue_map_id[detail_list[2]]
            data_dict['player'] = detail_list[0]
            data_dict['use_time'] = time_util.formatDateTime(time)
            datas_list.append(data_dict)
        return jsonify(result=1, data=datas_list, dataLength=total_count)

    # 如果没有数据并且输入了激活码就调用游戏服接口判断该激活码的状态
    elif not datas and code:
        status = GameWeb(int(channel_id)).post('/api/code_stat', {'code': code})
        if status['result'] == 0:
            return jsonify(result=0, msg=u'该激活码未使用！', data=[], dataLength=total_count)
        else:
            return jsonify(result=0, msg=u'该激活码不存在！', data=[], dataLength=total_count)

    # 其余情况均返回提示无数据
    else:
        return jsonify(result=0, msg=u'无数据！', data=[], dataLength=total_count)
