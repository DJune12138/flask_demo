# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require, md5, rand
from zs_backend.utils.const import *
from zs_backend.utils import time_util
import json
import time
from zs_backend import redis_conn
from . import sms_aliyun
from . import sms_qq
from . import sms_mengwangyun

from zs_backend.utils import httpc_util

## 3天
TOKEN_VALID_TIMELONG = 3 * 24 * 60 * 60

@httpc_util.check_param(ctype="c2s", debug=True)
def sms_check():
	data = request.form

	Mobile = int(data.get('mobile'))
	Timestamp = int(data.get("timestamp"))
	Code = data.get("code")
	Token = data.get('token')

	print data

	Now = int(time.time())
	## 先判断是不是3天内的
	if Now - Timestamp < TOKEN_VALID_TIMELONG:
		## 判断token是不是一致
		if md5("%d%s%d%s" % (Mobile, Code, Timestamp, SECRET_KEY)) == Token:
			## 生成后续给服务端校验的token
			NewToken = md5("%d%s%d%s" % (Mobile, Code, Now, SECRET_KEY))
			print "check...", Mobile, Now, SECRET_KEY, NewToken
			return jsonify({"result":"succ", "timestamp":Now, "token":NewToken})

	return jsonify({"result":"fail"})

def request_data():
	if request.json:
		return request.json
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	return data

@httpc_util.check_param(ctype="c2s", debug=True)
def sms_send():
	data = request_data()

	channel = data.get("channel")
	Mobile = int(data.get('mobile'))

	## 生成本次激活码
	Code = "%06d" % rand(1, 999999)
	Time = time_util.now_sec()

	sms_type = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "sms_type")
	if int(sms_type) == SMS_TYPE_MENGWANGYUN:
		rr = sms_mengwangyun.send_sms(channel, Mobile, Code, Time)
	elif int(sms_type) == SMS_TYPE_QQ:
		rr = sms_qq.send_sms(channel, Mobile, [Code], Time)
	if int(sms_type) == SMS_TYPE_ALIYUN:
		rr = sms_aliyun.send_sms(channel, Mobile, '{"code":"%s"}' % Code)

	if rr:
		## 生成后续给服务端校验的token
		NewToken = md5("%d%s%d%s" % (Mobile, Code, Time, SECRET_KEY))
		print "sms code:", Mobile, Code, Time, NewToken
		return jsonify({"result":"succ", "timestamp":Time, "token":NewToken})
	else:
		return jsonify({"result":"fail"})
