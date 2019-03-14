# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g, session
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from . import busi
import json
from zs_backend.utils.channel_qry import *

@busi.route('/admin_presented_config', methods=['GET'])
@login_require
def presented_config_init():
	select_channel = session['select_channel']

	if select_channel > 0:
		select_channel = session['select_channel']
		return get_info(select_channel)
		
	else:
		Rate = 0
		return render_template('presented.html', rate = Rate)
		
@busi.route('/presented_config_action', methods=['POST'])
@login_require
def do_action():
	data = request.form
	opt = int(data.get("opt_type"))

	if opt == 1:
		select_channel = session['select_channel']
		return get_info(select_channel)
	elif opt == 2:
		return update_config()
	else:
		return

def to_int(v):
	try:
		return int(v)
	except:
		return 0

def update_config():
	data = request.form
	Channel = session['select_channel']

	p2p = to_int(data.get("p2p"))
	p2a = to_int(data.get("p2a"))
	a2p = to_int(data.get("a2p"))
	a2a = to_int(data.get("a2a"))

	p2p_tax = to_int(data.get("p2p_tax"))
	p2a_tax = to_int(data.get("p2a_tax"))
	a2p_tax = to_int(data.get("a2p_tax"))
	a2a_tax = to_int(data.get("a2a_tax"))

	p2p_min_coin = to_int(data.get("p2p_min_coin"))
	p2a_min_coin = to_int(data.get("p2a_min_coin"))
	a2p_min_coin = to_int(data.get("a2p_min_coin"))
	a2a_min_coin = to_int(data.get("a2a_min_coin"))

	p2p_max_coin = to_int(data.get("p2p_max_coin"))
	p2a_max_coin = to_int(data.get("p2a_max_coin"))
	a2p_max_coin = to_int(data.get("a2p_max_coin"))
	a2a_max_coin = to_int(data.get("a2a_max_coin"))

	p_coin = to_int(data.get("p_coin"))
	max_presented_times = to_int(data.get("max_presented_times"))

	role_str = session['role_str']

	d = {
		"p2p":p2p,
		"p2a":p2a,
		"a2p":a2p,
		"a2a":a2a,
		"p2p_tax":p2p_tax,
		"p2a_tax":p2a_tax,
		"a2p_tax":a2p_tax,
		"a2a_tax":a2a_tax,
		"p_coin":p_coin,
		"max_presented_times":max_presented_times,
		"p2p_min_coin":p2p_min_coin,
		"p2a_min_coin":p2a_min_coin,
		"a2p_min_coin":a2p_min_coin,
		"a2a_min_coin":a2a_min_coin,
		"p2p_max_coin":p2p_max_coin,
		"p2a_max_coin":p2a_max_coin,
		"a2p_max_coin":a2p_max_coin,
		"a2a_max_coin":a2a_max_coin,
	}

	sql = '''
		replace into admin_presented_config
			(channel, config)
		values ('%s','%s')
	''' % (Channel, json.dumps(d))
	try:
		LogQry(Channel).execute(sql)
	except Exception as e:
		pass

	GameWeb(Channel).post("/api/change_give_cond", d)

	return render_template('presented.html', config = d)

def get_info(select_channel):	
	sql = '''
		select config
		from admin_presented_config
		where channel = %d
	''' % select_channel
	try:
		Config = LogQry(select_channel).qry(sql)[0][0]
		Config = json.loads(Config)
	except Exception as e:
		Config = {
			"p2p_min_coin":0,
			"p2a_min_coin":0,
			"a2p_min_coin":0,
			"a2a_min_coin":0,
			"p2p_max_coin":0,
			"p2a_max_coin":0,
			"a2p_max_coin":0,
			"a2a_max_coin":0,
			"p2p_tax":0,
			"p2a_tax":0,
			"a2p_tax":0,
			"a2a_tax":0,
		}

	return render_template('presented.html', config = Config)
