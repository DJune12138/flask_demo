# -*- coding:utf-8 -*-
import json
import time
from flask import render_template, jsonify, url_for
from flask.globals import session, request, current_app
from werkzeug.utils import redirect
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import time_util
from zs_backend.utils.common import login_require
from zs_backend.utils.channel_qry import GameWeb, LogQry


def others_qyr_html(orderno):
    return [
        '<span>订单号：<input type="text" id="orderno" name="orderno" value="%s"></span>' % orderno
    ]


@busi.route('/transfer/list', methods=['GET'])
@login_require
def transfer_coin():
    page = dict()
    page["others"] = others_qyr_html("")
    page["beginDate"] = 11
    page["endDate"] = 11
    page["playerid"] = ""
    page["channel"] = ""
    page["datas"] = []

    return render_template('transfer_list.html', page=page)


@busi.route('/transfer/list', methods=['POST'])
@login_require
def transfer_coin_list():
    start_time = request.form.get('beginDate')
    end_time = request.form.get('endDate')

    start_date = time_util.formatTimestamp(start_time)
    end_date = time_util.formatTimestamp(end_time)

    pid = request.form.get('PlayerID')
    Account = request.form.get('Account', '')
    channel = session['select_channel']
    orderno = request.form.get('orderno')

    where = ''
    if pid:
        where += " AND pid=%s" % pid
    if orderno:
        where += " AND orderno='%s' " % orderno
    if Account:
        where += " AND pid = (select id from player where account_id='%s') " % Account

    retrieve_sql = """SELECT time,pid,state,type,num,
                              coin_now,uniqueno,orderno,(select nick from player where id=pid),
                                  (select account_id from player where id=pid)
                      FROM log_transfer
                      WHERE time>=%s AND time<=%s%s
		              ORDER BY time DESC;""" \
                   % (start_date, end_date, where)
    data = LogQry(int(channel)).qry(retrieve_sql)
    data_list = list()
    for dateStamp, pid, state, type, num, \
        coin, uniqueno, orderno, nick, acc in data:
        data_dict = dict()
        data_dict['dateStamp'] = dateStamp
        data_dict['pid'] = pid
        data_dict['state'] = state
        data_dict['type'] = type
        data_dict['num'] = num
        data_dict['coin'] = coin
        data_dict['uniqueno'] = uniqueno
        data_dict['orderno'] = orderno
        data_dict['nick'] = nick
        data_dict['acc'] = acc
        data_list.append(data_dict)

    return jsonify(result='ok', data=data_list)
