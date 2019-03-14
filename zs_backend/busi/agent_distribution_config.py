# -*- coding:utf-8 -*-

## 代理分销设置

from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g, session
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from zs_backend.utils.channel_qry import *
from . import busi
from zs_backend.utils import game_util
import json

INIT_COMMISSION = [0, 0, 0, 0]


def get_config(channel, sql):
    try:
        (pump, commission) = LogQry(channel).qry(sql)[0]
        if pump != "":
            pump = json.loads(pump)
        if commission != "":
            commission = json.loads(commission)
    except Exception as e:
        pump = {}
        commission = INIT_COMMISSION

    return (pump, commission)


@busi.route('/agent_distribution_config', methods=['GET'])
@login_require
def agent_distribution_init():
    if session['select_channel'] > 0:
        return query(session['select_channel'])
    else:
        return render_template('agent_distribution_config.html',
                           pump={}, commission=INIT_COMMISSION)

@busi.route('/agent_distribution_qry', methods=['GET'])
@login_require
def query():
    channel = session['select_channel']
    return query(channel)

def query(channel):
    sql = '''
		select pump_section, commission_section
		from admin_distribution_config
	''' 
    (pump, commission) = get_config(session['select_channel'], sql)
    pp = []
    for I1, I2, I3, I4, I5, I6 in pump:
        I1 = game_util.coin_translate(channel, int(I1))
        I2 = game_util.coin_translate(channel, int(I2))
        I4 = game_util.coin_translate(channel, int(I4))
        I5 = game_util.coin_translate(channel, int(I5))
        pp.append([I1, I2, I3, I4, I5, I6])

    return render_template('agent_distribution_config.html', select_channel=channel,
        pump=pp, commission=commission)

@busi.route('/agent_distribution_save', methods=['POST'])
@login_require
def save_pump():
    channel = session['select_channel']
    pump = request.form.get('pump')

    try:
        json.loads(pump)
    except:
        return jsonify(error_msg = u"数据格式不对")

    sql = '''
		select pump_section, commission_section
		from admin_distribution_config
	''' 
    (oldpump, commission) = get_config(channel, sql)

    up_sql = '''
		replace into admin_distribution_config
		values (1, '%s', '%s')
	''' % (pump, json.dumps(commission))
    LogQry(channel).execute(up_sql)

    return jsonify()

@busi.route('/agent_distribution_save_commission', methods=['POST'])
@login_require
def save_commission():
    channel = session['select_channel']

    rate = request.form.get("rate")
    try:
        rate_list = [int(i) for i in rate.split(",")]
    except:
        return jsonify(error_msg = u"佣金比例必须为整数")

    sql = '''
		select pump_section, commission_section
		from admin_distribution_config
	''' 
    (pump, commission) = get_config(channel, sql)
    commission = rate_list

    up_sql = '''
		replace into admin_distribution_config
		values (1, '%s', '%s')
	''' % (json.dumps(pump), json.dumps(commission))
    LogQry(channel).execute(up_sql)

    return jsonify()
