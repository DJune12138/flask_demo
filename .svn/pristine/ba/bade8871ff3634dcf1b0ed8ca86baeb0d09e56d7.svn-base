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
from zs_backend import redis_conn
from zs_backend.utils.common import md5
import json
from zs_backend.utils.channel_qry import GameWeb, LogQry

@busi.route('/gm/h5_moni_login', methods=['GET'])
@login_require
def h5_moni_login_show():
	page = {}
	page["channel"] = session['select_channel']
	page["acc_id"] = ""
	return render_template('h5_moni_login.html', page=page)

@busi.route('/gm/h5_moni_login', methods=['POST'])
@login_require
def h5_moni_login():
	channel_id = session['select_channel']
	acc_id = request.form.get("Account")

	try:
		url = redis_conn.hget(CHANNEL_CONFIG_TABLE+str(channel_id), "h5_link")
		channel = redis_conn.hget(CHANNEL_CONFIG_TABLE+str(channel_id), "name")
	except:
		url=""

	new_acc = "%s_%s" % (channel, acc_id)
	Now = int(time_util.now_sec())
	payload = {
		"channel":channel,
		"acc_id":new_acc,
		"timestamp":Now,
		"gameid":0,
		"token":md5(new_acc + str(Now) + SECRET_KEY)
	}
	url2 = "%s?%s" % (url, "&".join(["%s=%s" % (k, v) for k, v in payload.items()]))

	page = {}
	page["url"] = url2
	page["acc_id"] = acc_id
	return render_template('h5_moni_login.html', page=page)
