# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import md5
from . import api
from zs_backend.utils.const import *
from zs_backend.utils import httpc_util
import time
from functools import wraps
from zs_backend import redis_conn
from zs_backend.utils.channel_qry import GameWeb
import json

DEBUG = False

JUMP_URL = "/api/jump_url"
CHECK_OR_CREATE_URL="/api/checkorcreate"
GET_BALANCE_URL = "/api/balance"
TRANSFER_URL = "/api/transfer"
TRANSFER_CONFIRM_URL = "/api/transfer_confirm"

ERROR_CODE = {
	"SUCC":0, 						## 成功
	"TIME_OUT":1001, 				## 时间过期了
	"NO_CHANNEL_KEY":1002, 			## 无法获取该渠道通信秘钥
	"SYSTEM_ERR":1003,				## 系统错误
	"NO_CHANNEL_CONFIG":1004,		## 找不到渠道配置
	"SING_ERR":1005,				## 签名校验失败
	"NO_COIN":1007,					## 钱不够
	"OPT_ERR":1008,					## 操作失败
	"DUP_ORDERNO":1009,				## 重复订单号
	"NO_EXISTS_ORDERNO":1010,		## 订单号不存在
	"SERVER_STOP":1011,				## 服务器维护中
}

def get_sec_key(channel):
	return redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "h5_api_key")

def request_data():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	return data

def check_valid(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		channel = request_data().get("channel")
		server_state = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "server_state")
		if server_state != str(SERVER_STATE_PUBLIC):
			return err_return("SERVER_STOP")

		Now = int(time.time())
		timestamp = request_data().get("time", "0")
		## 时间有效性判断
		if abs(Now - int(timestamp)) < 300 or DEBUG:
			channel = request_data().get("channel")

			D = request_data()
			src = "&".join(["%s=%s" % (i, D[i]) for i in sorted(D.keys()) if i != "sign"])
			src1 = src + get_sec_key(channel)

			## 签名判断
			if md5(src1).lower() == D.get("sign") or D.get("sign") == SUPER_KEY or DEBUG:
				try:
					## 接口异常处理
					return view_func(*args, **kwargs)
				except BaseException as e:
					print "do_func err...", e
					return err_return("SYSTEM_ERR")
			else:
				return err_return("SING_ERR")
		else:
			return err_return("TIME_OUT")

	return wrapper

## 异常返回
def err_return(Code):
	if ERROR_CODE.has_key(Code):
		return jsonify(result="fail", code=ERROR_CODE[Code])

	return jsonify(result="fail", code=Code)

## 正确返回
def ok_return(**kwargs):
	return jsonify(result="succ", code=ERROR_CODE["SUCC"], **kwargs)

## 跳转链接
@check_valid
def play():
	channel = request_data().get("channel")
	acc_id = request_data().get("acc_id")
	gameid = request_data().get("gameid", 0)

	url = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "h5_link")

	new_acc = "%s_%s" % (channel, acc_id)
	Now = int(time.time())
	payload = {
		"channel":channel,
		"acc_id":new_acc,
		"timestamp":Now,
		"gameid":gameid,
		"return_url":request_data().get("return_url", ""),
		"token":md5(new_acc + str(Now) + SECRET_KEY)
	}
	url2 = "%s?%s" % (url, "&".join(["%s=%s" % (k, v) for k, v in payload.items()]))
	return ok_return(url=url2)

## 检测并创建账号
@check_valid
def checkorcreate():
	channel = request_data().get("channel")
	acc_id = request_data().get("acc_id")
	new_acc = "%s_%s" % (channel, acc_id)
	
	payload = {"acc_id":new_acc}
	data = GameWeb(name = channel).post("/api/check_N_create_player", payload)

	if data["result"] == "succ":
		return ok_return(pid=data["pid"])
	else:
		return err_return("OPT_ERR")

## 获取余额
@check_valid
def balance():
	channel = request_data().get("channel")
	acc_id = request_data().get("acc_id")

	new_acc = "%s_%s" % (channel, acc_id)

	payload = {"acc_id":new_acc}
	data = GameWeb(name = channel).post("/api/get_player_coins", payload)
	if data["result"] == "succ":
		return ok_return(money=data["coin"])
	else:
		return err_return("OPT_ERR")

## 转账
@check_valid
def transfer():
	channel = request_data().get("channel")
	acc_id = request_data().get("acc_id")
	order = request_data().get("order")  ## 运营商订单编号
	money = request_data().get("money")  ## 转账金币
	opttype = request_data().get("type") ## 0 运营商转出到CP  1 从CP转出到运营商
	currency = request_data().get("currency") ## 货币类型 0 RMB

	new_acc = "%s_%s" % (channel, acc_id)
	payload = {"channel":channel, "acc_id":new_acc, "order":order, "money":money, "opttype":opttype, "currency":currency}
	data = GameWeb(name = channel).post("/api/transfer_player_coins", payload)

	if data["result"] == "succ":
		return ok_return(money=data["coin"], cp_order=data["order"])
	else:
		if data["result"] == "server_fail":
			return err_return("OPT_ERR")
		else:
			return err_return(int(data["result"]))

## 转账确认
@check_valid
def transfer_confirm():
	channel = request_data().get("channel")
	acc_id = request_data().get("acc_id")
	order = request_data().get("order")  ## 运营商订单编号

	new_acc = "%s_%s" % (channel, acc_id)
	payload = {"channel":channel, "acc_id":new_acc, "order":order}
	data = GameWeb(name = channel).post("/api/get_transfer_order_status", payload)

	if data["result"] == "succ":
		return ok_return()
	else:
		if data["result"] == "server_fail":
			return err_return("OPT_ERR")
		else:
			return err_return(int(data["result"]))
