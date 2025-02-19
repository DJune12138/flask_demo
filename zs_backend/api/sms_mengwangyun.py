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
from zs_backend.utils import httpc_util

SMS_URL = "http://api01.monyun.cn:7901/sms/v2/std/single_send"
CONTENT_STR = u'''您的验证码是%s，在2分钟内输入有效。如非本人操作请忽略此短信。'''

def make_pwd(uid, pwd, TimeStr):
	Str = "%s00000000%s%s" % (uid, pwd, TimeStr)
	return md5(Str).lower()

def send_sms(channel, mobile, code, Time):
	## 获取短息你配置
	conf = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "sms_config")
	[uid, pwd, key] = conf.split(",")

	## 生成短信内容
	Content = (CONTENT_STR % code).encode("gbk")

	TimeStr = time.strftime("%m%d%H%M%S", time.localtime(Time))
	payload = {
		"userid":uid, 
		"pwd":make_pwd(uid, pwd, TimeStr), 
		"mobile":str(mobile), 
		"content":Content, 
		"timestamp":TimeStr
	}

	try:
		r = None
		r = httpc_util.post(SMS_URL, payload)
		rr = json.loads(r.text)

		if rr["result"] == 0:
			return True
	except:
		pass

	print "sms err:", r, channel, payload
	return False
