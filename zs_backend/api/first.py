# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from zs_backend.utils.common import rand_list
from config import Config
from zs_backend.utils import time_util
from zs_backend.utils import httpc_util
from zs_backend.utils.ip2Region import Ip2Region

from zs_backend import redis_conn

from wx import get_wx_app_list, get_wx_h5_list
from zs_backend.utils.const import *

def sdk_download_tj():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	channel = data.get("channel")
	os = data.get("os")

	ip = request.remote_addr if len(request.access_route) == 0 else request.access_route[0]
	invite = data.get("code")
	if invite:
		redis_conn.set("%s_%s_%s" %(INVITE_CODE_TABLE, channel, ip), invite, ex = 3600 * 60)

	redis_conn.hincrby("download_count", "%s_%s" % (channel, os))
	print "download...", channel, os, request.remote_addr, time_util.formatDateTime(time_util.now_sec())

	return jsonify({})

def sdk_reset_click_tj():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	channel = data.get("channel")

	ios = redis_conn.hget("download_count", "%s_ios" % channel)
	redis_conn.hset("download_count", "%s_ios" % channel, 0)
	android = redis_conn.hget("download_count", "%s_android" % channel)
	redis_conn.hset("download_count", "%s_android" % channel, 0)

	try:
		ios = int(ios)
	except:
		ios = 0

	try:
		android = int(android)
	except:
		android = 0

	return jsonify({"ios":ios, "android":android})

def get_country_from_ip(ip):
	country = ""
	area = ""
	if ip:
		ip_data = Ip2Region("./config/ip2region.db").memorySearch(ip)["region"].split("|")
		country = ip_data[0]
		area = ip_data[2]

	return country, area

@httpc_util.check_param(ctype="c2s", debug=True, checktime=False)
def sdk_sys():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	if data.has_key("channel"):
		Channel = data.get("channel")
	else:
		return

	## 玩家设备号或者mac地址
	mac = data.get("mac", "")
	ip = data.get("ip", "")
	if not ip:
		ip = request.remote_addr if len(request.access_route) == 0 else request.access_route[0]

	## 判断服务器状态
	channel_tab = CHANNEL_CONFIG_TABLE+Channel
	server_state = redis_conn.hget(channel_tab, "server_state")

	s_area = ""
	if server_state == str(SERVER_STATE_PRE_PUBLIC):
		## 预发布状态 判断是否在白名单 如果不在白名单 返回停服状态
		white = redis_conn.hget(channel_tab, "white")
		if not white:
			return jsonify(stop_server = True)
		else:
			white = white.split("~")
			if (mac not in white) and (ip not in white):
				return jsonify(stop_server = True)
	elif server_state == str(SERVER_STATE_PUBLIC):
		## 已发布状态 需要判断是否在黑名单 如果在黑名单 则返回停服状态
		black = redis_conn.hget(channel_tab, "black")
		print "Channel black...", Channel, ip, black
		country, area = get_country_from_ip(ip)
		s_area = country + area
		if black and black != "None":
			black = black.split("~")
			if (mac in black) or (ip in black) or (country in black) or (area in black):
				return jsonify(stop_server = True)
	else:
		return jsonify(stop_server = True)

	if data.has_key("app") and data.get("app") == "true":
		AppIDList = get_wx_app_list(Channel)
		BGPList = redis_conn.hgetall(BGP_TABLE + Channel)
	else:
		AppIDList = get_wx_h5_list(Channel)
		BGPList = redis_conn.hgetall(BGP_TABLE + Channel + "_h5")
		if not BGPList:
			BGPList = redis_conn.hgetall(BGP_TABLE + Channel)

	## 根据渠道获得可以的bgp服务器列表
	CanUseList = []
	for k, v in BGPList.items():
		vv = v.split("_")
		if len(vv) > 1 and s_area.find(vv[1]) >= 0: ## and int(vv[0]) < BGP_MAX_CONN
			CanUseList.append(k)
	if not CanUseList:
		CanUseList = BGPList.keys()

	try:
		notice_l = eval(redis_conn.hget(channel_tab, "notice"))
	except Exception as e:
		print "get notice excepiton:", e
		notice_l = []

	invite_key = "%s_%s_%s" % (INVITE_CODE_TABLE, Channel, ip)
	invite_code = redis_conn.get(invite_key)
	if invite_code == "None" or (not invite_code):
		invite_code = ""
	else:
		redis_conn.delete(invite_key)

	param = {
		"ip":CanUseList[:3],
		"appid":rand_list(AppIDList),
		"time":time_util.now_sec(),
		"stop_server":False,
		"notice":notice_l,
		"client_ip":ip,
		"invite_code":invite_code,
	}

	return jsonify(param)

def sdk_bgp_conn():
	data = request.args

	if data.get("clear"):
		## 删除链接
		return clear_bgp_conn()

	size = data.get("size")
	country = data.get("country")
	val = "%s_%s" % (size, country)

	for channel, key in data.items():
		if len(key.split("_")) == 2:
			redis_conn.hset(BGP_TABLE + channel, key, val)

	return jsonify()

def clear_bgp_conn():
	data = request.args
	for channel, key in data.items():
		if channel == "clear":
			continue
		if key == "True":
			for k, v in redis_conn.hgetall(BGP_TABLE + channel):
				redis_conn.hdel(BGP_TABLE + channel, k)
		else:
			redis_conn.hdel(BGP_TABLE + channel, key)

	return jsonify()

@httpc_util.check_param(ctype="c2s", debug=True, checktime=False)
def sdk_hotup_url():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	channel = data.get("channel")

	return redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "hotup_url")

def sdk_ip():
	ip = request.args.get("ip")
	country, area = get_country_from_ip(ip)
	return "%s %s" % (country, area)
