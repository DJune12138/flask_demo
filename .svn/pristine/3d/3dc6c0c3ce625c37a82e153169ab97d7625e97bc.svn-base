# -*- coding:utf-8 -*-
from flask import render_template, jsonify, url_for
from flask.globals import session, request, g, current_app
from werkzeug.utils import redirect

from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import erl
from zs_backend.utils.common import login_require
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
from zs_backend.utils.const import *
from zs_backend.utils.common import md5
import json
from zs_backend.utils.channel_qry import GameWeb, LogQry
from zs_backend.busi import pay_channel

STATUS_USE = 0
STATUS_NOUSE = 1


@busi.route('/wx_agent', methods=['GET'])
@login_require
def show_wx_agent():
    page = dict()
    page['OThers'] = status_search()

    return render_template('wx_agent.html', page=page)


@busi.route('/wx_agent/list', methods=['GET'])
@login_require
def pay_wx_agent():
    channel = session['select_channel']

    status = request.args.get('status', "")
    return get_info(channel, status)


def status_search(status=-1):
    SELECTED0, SELECTED1 = "", ""
    if status == '0':
        SELECTED0 = "selected"
    elif status == '1':
        SELECTED1 = "selected"

    status_html = u'''
		<td>状态
			<select id="status" name="status"> 
				<option value="-1">全部</option> 
				<option value="0" %s>启用</option> 
				<option value="1" %s>停用</option> 
			</select>
		</td>''' % (SELECTED0, SELECTED1)

    return [status_html]


def get_info(channel, status):
    where = ""
    if status and status != '-1':
        where += " AND status = %s" % status

    retrieve_sql = """SELECT id,wx,seq,memo,status
                      FROM admin_wx_agent
                      WHERE channel=%d%s
                      ORDER BY status,seq;""" \
                   % (channel, where)
    data = LogQry(channel).qry(retrieve_sql)

    data_list = list()
    for primary_id, wx, seq, memo, status in data:
        data_dict = dict()
        data_dict['id'] = primary_id
        data_dict['wx'] = wx
        data_dict['seq'] = seq
        data_dict['memo'] = memo
        data_dict['status'] = status
        data_list.append(data_dict)

    return jsonify(result='ok', data=data_list)


@busi.route('/wx_agent/<re(".+"):operation>', methods=['GET'])
@login_require
def wx_agent_opt(operation):
    if operation == "add":
        return wx_agent_add()

    if operation == "edit":
        return wx_agent_edit()

    if operation == "del":
        return wx_agent_del()


def wx_agent_add():
    channel = session['select_channel']
    wx = request.args.get('wx')
    seq = int(request.args.get('seq'))
    memo = request.args.get('memo')

    sql = '''
		select count(1)
		from admin_wx_agent
		where channel = %d 
		and wx = '%s'
	''' % (channel, wx)

    count = LogQry(channel).qry(sql)[0][0]
    if count > 0:
        return jsonify(result="fail", error_msg="wx dup")

    sql = '''
		insert into admin_wx_agent
			(wx, seq, memo, status, channel)
		values 
			('%s', %d, '%s', %d, %d)
	''' % (wx, seq, memo, STATUS_USE, channel)
    LogQry(channel).execute(sql)

    return jsonify(result="ok")


def wx_agent_edit():
    channel = session['select_channel']
    idx = int(request.args.get('id'))
    wx = request.args.get('wx')
    seq = int(request.args.get('seq'))
    memo = request.args.get('memo')
    status = int(request.args.get('status'))

    sql = '''
		replace into admin_wx_agent
			(id, wx, seq, memo, status, channel)
		values 
			(%d, '%s', %d, '%s', %d, %d)
	''' % (idx, wx, seq, memo, status, channel)
    LogQry(channel).execute(sql)

    return jsonify(result="ok")


def wx_agent_del():
    channel = session['select_channel']
    idx = int(request.args.get('id'))

    delete_sql = """DELETE FROM admin_wx_agent
                    WHERE id=%s;""" % idx
    LogQry(channel).execute(delete_sql)

    return jsonify(result="ok")
