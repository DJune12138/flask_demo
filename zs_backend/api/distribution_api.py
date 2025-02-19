# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require, md5, rand
from . import api
from zs_backend.utils.const import *
from zs_backend.utils import httpc_util, time_util
from zs_backend.utils.channel_qry import LogQry, GameWeb
import json
from zs_backend.utils import distribution_util

## 获取分销配置
@api.route('/api/distribution_config', methods=['GET'])
def api_distribution_config():
	channel = request.args.get("channel")

	sql = 'select pump_section, commission_section from admin_distribution_config limit 1'
	pump, commission = LogQry(name = channel).qry(sql)[0]

	return jsonify(pump = json.loads(pump), commission = json.loads(commission))

## 获取分销佣金发放记录
@api.route('/api/distribution_settlement', methods=['GET'])
def api_distribution_settlement():
	channel = request.args.get("channel")
	pid = int(request.args.get("pid"))

	sql = '''
		select date1, date2, pump_commission, win_commission, fee, 
			other_fee
		from admin_distribution_settlement
		where pid = %d
	''' % pid
	datas = []
	for date1, date2, v1, v2, v3, v4 in LogQry(name = channel).qry(sql):
		datas.append(["%s-%s" % (date1, date2), v1 + v2 - v3 - v4])

	return jsonify(datas = datas)

## 获取玩家未发放分销佣金
@api.route('/api/distribution_settlement/no', methods=['GET'])
def api_distribution_settlement_no():
	channel = request.args.get("channel")
	pid = int(request.args.get("pid"))

	## 根据查询日期 偏移量
	sql = '''
		select pid, pump, win, pump_detail, win_detail
		from t_distribution_day a
		where pid = %d
		and time > 
			(select ifnull(max(date2) , 0)
			from admin_distribution_settlement 
			where pid = a.pid)
	''' % pid
	datas = {"pump":{}, "win":{}, "pump_detail":{}, "win_detail":{}}
	for pid, pump, win, pump_detail, win_detail in LogQry(name = channel).qry(sql):
		print pump_detail, win_detail
		datas = merge_dict(datas, json.loads(pump), json.loads(win), json.loads(pump_detail), json.loads(win_detail))

	## 查询分销配置
	sql = 'select pump_section, commission_section from admin_distribution_config limit 1'
	pump_config, commission_config = LogQry(name = channel).qry(sql)[0]
	pump_config = json.loads(pump_config)
	commission_config = json.loads(commission_config)

	## 计算返佣
	datas = distribution_util.calc_commission(datas, pump_config, commission_config)

	res = {
		"pump_commission":datas["pump_commission"],
		"win_commission":datas["win_commission"],
		"count":[len(datas["win_detail"][str(i)]) for i in range(0, len(datas["win_detail"]))],
	}

	return jsonify(datas = res)

## 合并字典
def merge_dict(d, pump, win, pump_detail, win_detail):
	for k, v in pump.items():
		if not d["pump"].has_key(k):
			d["pump"][k] = 0
		d["pump"][k] += v

	for k, v in win.items():
		if not d["win"].has_key(k):
			d["win"][k] = 0
		d["win"][k] += v

	for k, v in pump_detail.items():
		if not d["pump_detail"].has_key(k):
			d["pump_detail"][k] = {}
		for kk, vv in v.items():
			if not d["pump_detail"][k].has_key(kk):
				d["pump_detail"][k][kk] = 0
			d["pump_detail"][k][kk] += vv

	for k, v in win_detail.items():
		if not d["win_detail"].has_key(k):
			d["win_detail"][k] = {}
		for kk, vv in v.items():
			if not d["win_detail"][k].has_key(kk):
				d["win_detail"][k][kk] = 0
			d["win_detail"][k][kk] += vv

	return d
