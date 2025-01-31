# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.utils.common import login_require, md5, rand
from . import api
from zs_backend.utils.const import *
from zs_backend.utils import httpc_util
from zs_backend.utils import time_util
import time
from zs_backend import redis_conn
from zs_backend.utils import qrcode_util
import json
import urllib
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils import recharge_util
import time

def request_data():
	if request.json:
		return request.json
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	return data

def do_pay_after(channel, orderno, platform_orderno, money, memo):
	channel = int(channel)

	## 查询是否存在该订单
	sql = 'select state, pid from admin_recharge where orderno = "%s"' % orderno
	r = LogQry(channel).qry(sql)

	if r:
		## 已经成功了的 重复执行了
		if r[0][0] == PAY_STATE_SUCC:
			return True

		if r[0][0] == PAY_STATE_WAIT:
			pid = int(r[0][1])
			## 支付成功 给玩家发钱吧
			## 此处可能会有充值活动 产生充值金币波动问题
			recharge_info = recharge_util.get_coin_recharge_discounts(channel, money, pid)
			recharge_id, add_recharge, coin = recharge_info

			sql = '''
				update admin_recharge
				set coin = %d, state = %d, memo = '%s', rechargeid = %d, add_recharge = %d
				where orderno = '%s'
			''' % (coin, PAY_STATE_SUCC, memo, recharge_id, add_recharge, orderno)
			LogQry(channel).execute(sql)

			## todo 给游戏后台发送消息
			pay_load = {
				"pid": pid,
				"money": money,
				"coin": coin,
				"type":COIN_CHANGE_RECHARGE,
			}
			GameWeb(channel).post("/api/set_player_coin", pay_load)

			return True

	return False

## 扫码支付回调
def pay_cb_zfb():
	dd = {}
	for k, v in request.form.items():
		if k == "sign_type":
			continue
		dd[k] = urllib.unquote(v)

	if dd["trade_status"] == u"TRADE_SUCCESS":
		## 此处比较恶心 一直没有找到支付宝怎么透传参数 渠道号 支付通道ID只能通过订单编号拆串取得
		orderno = dd["out_trade_no"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 查询公钥
		sql = 'select public_key from admin_online_payment where id = %s' % pay_channel
		public_key = LogQry(channel).qry(sql)[0][0]

		## 重新拼私钥 加上前后一段
		public_key = '''-----BEGIN PUBLIC KEY-----
%s
-----END PUBLIC KEY-----
''' % public_key

		if httpc_util.check_sign(dd, public_key, dd["sign"], sign_type = "RSA2"):
			pass
		else:
			print "check sign fail:", dd
			payload = {"return_code":"FAIL", "return_msg":"check sign err"}
			return jsonify(payload)

		## 签名校验通过 支付成功
		money = int(float(dd["receipt_amount"]) * 100)
		platform_orderno = dd["trade_no"]
		
		if do_pay_after(channel, orderno, platform_orderno, money, dd["gmt_payment"]):
			payload = {"return_code":"SUCCESS", "return_msg":"OK"}
			return jsonify(payload)
		else:
			print dd
			payload = {"return_code":"FAIL", "return_msg":"send err"}
			return jsonify(payload)
	else:
		print dd
		payload = {"return_code":"FAIL", "return_msg":"trade status err"}
		return jsonify(payload)

## 微信扫码支付回调
def pay_cb_wx():
	data = httpc_util.xml_to_dict(request.get_data())
	
	if data["return_code"] == "SUCCESS":
		orderno = data["out_trade_no"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名
		src = "&".join(["%s=%s" % (i, data[i]) for i in sorted(data.keys()) if i != "sign"])
		src += "&key=%s" % mch_key
		sign = md5(src).upper()
		if data["result_code"] == "SUCCESS" and data["sign"] == sign: 
			## 签名校验通过 支付成功
			money = data["total_fee"]
			platform_orderno = data["transaction_id"]
			orderno = data["out_trade_no"]
			
			if do_pay_after(channel, orderno, platform_orderno, int(money), data["time_end"]):
				payload = {"return_code":"SUCCESS", "return_msg":"OK"}
				return httpc_util.dict_to_xml(payload)
			else:
				payload = {"return_code":"FAIL", "return_msg":"send err"}
				return httpc_util.dict_to_xml(payload)
		else:
			payload = {"return_code":"FAIL", "return_msg":"check sign err"}
			return httpc_util.dict_to_xml(payload)

## 易知富支付回调
def pay_cb_yi_zhi_fu():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["returnCode"] == "SUCCESS":
		orderno = data["outTradeNo"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名
		if data["resultCode"] == "SUCCESS" and httpc_util.check_sign(data, mch_key, data["sign"]):
			## 签名校验通过 支付成功
			money = int(float(data["totalFee"]) * 100)
			platform_orderno = data["transactionId"]
			orderno = data["outTradeNo"]
			
			if do_pay_after(channel, orderno, platform_orderno, int(money), data["timeEnd"]):
				return jsonify({"return_code":"SUCCESS", "return_msg":"OK"})
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})

## 新宝支付回调
def pay_cb_xin_bao():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["code"] == "00":
		orderno = data["order_no"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名
		if httpc_util.check_sign(data, mch_key, data["sign"], connect_key = False):
			## 签名校验通过 支付成功
			money = int(float(data["amount"]) * 100)
			platform_orderno = data["trade_no"]
			orderno = data["order_no"]
			memo = ""

			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			if result:
				return "ok"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})

## 68支付回调
def pay_cb_68():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["code"] == "00":
		orderno = data["order_no"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名
		if httpc_util.check_sign(data, mch_key, data["sign"], connect_key = False):
			## 签名校验通过 支付成功
			money = int(float(data["amount"]) * 100)
			platform_orderno = data["trade_no"]
			orderno = data["order_no"]
			memo = ""

			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			print "result:", result
			if result:
				return "ok"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})

## 陌陌支付回调
def pay_cb_mo_mo_fu():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["returncode"] == "00":
		orderno = data["orderid"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]

		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名 去除值为空的
		data2 = {}
		for k, v in data.items():
			if v:
				data2[k] = v
		if httpc_util.check_sign(data2, mch_key, data2["sign"], lower = False):
			## 签名校验通过 支付成功
			money = int(float(data["amount"]) * 100)
			platform_orderno = data["transaction_id"]
			memo = ""

			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			if result:
				return "OK"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})

## cs支付回调
def pay_cb_cs():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["code"] == "00":
		orderno = data["order_no"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]
		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]
		## 先判断签名
		if httpc_util.check_sign(data, mch_key, data["sign"], connect_key = True):
			## 签名校验通过 支付成功
			money = int(float(data["amount"]) * 100)
			platform_orderno = data["trade_no"]
			orderno = data["order_no"]
			memo = ""
			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			if result:
				return "ok"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})

## 佰富支付回调
def pay_cb_bai_fu():
	dd = request_data()
	dd1 = {}
	for k, v in dd.items():
		dd1[k] = v

	data = json.loads(dd1["paramData"])

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["resultCode"] == "00":
		orderno = data["orderNum"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]
		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		## 先判断签名
		src = ",".join(['"%s":"%s"' % (i, data[i]) for i in sorted(data.keys()) if i != "sign"])
		src = "{%s}%s" % (src, mch_key)
		if md5(src).upper() == data["sign"]:
			## 签名校验通过 支付成功
			money = int(data["payAmount"])
			platform_orderno = ""
			memo = ""
			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			if result:
				return "000000"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
		
## 优码付支付回调
def pay_cb_you_ma_fu():
	dd = request_data()
	data = {}
	for k, v in dd.items():
		data[k] = v

	if not data:
		return jsonify(err="nodata")
	if not data.has_key("sign"):
		return jsonify(err="nosign")

	if data["returncode"] == "00":
		orderno = data["orderid"]
		ll = orderno.split("_")
		channel = int(ll[0])
		pay_channel = ll[1]
		## 获取商户秘钥
		sql = 'select md5_key from admin_online_payment where id = %s' % pay_channel
		mch_key = LogQry(channel).qry(sql)[0][0]

		if data.has_key("attach"):
			data.pop("attach")
		## 先判断签名
		if httpc_util.check_sign(data, mch_key, data["sign"], connect_key = True, lower = False):
			## 签名校验通过 支付成功
			money = int(float(data["amount"]) * 100)
			platform_orderno = data["transaction_id"]
			memo = ""
			result = do_pay_after(channel, orderno, platform_orderno, money, memo)
			if result:
				return "OK"
			else:
				return jsonify({"return_code":"FAIL", "return_msg":"send err"})
		else:
			return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
	else:
		print data
		return jsonify({"return_code":"FAIL", "return_msg":"check sign err"})
		