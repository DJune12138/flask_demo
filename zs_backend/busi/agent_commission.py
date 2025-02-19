# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import time_util, game_util
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require
from flask import render_template, request, session, jsonify
from zs_backend.sql import SqlOperate

@busi.route('/agent_commission/init', methods=['GET'])
@login_require
def agent_commission_init():
	"""佣金结算页面"""

	return render_template('agent_commission_settlement.html')

@busi.route('/agent_commission/show', methods=['GET'])
@login_require
def agent_commission_show():
	# 获取参数
	channel = session['select_channel']
	begin_time = request.args.get('begin_time')
	end_time = request.args.get('end_time')
	pid = request.args.get("pid", "")

	if end_time < begin_time:
		return jsonify(u'查询结束日期必须大于开始日期')

	## pid为空 则为查询本账号绑定的代理ID
	if pid == "":
		## 获取该账号绑定ID
		sql = 'select game_player_id from user where id = %d' % session['user_id']
		pid = SqlOperate().select(sql)[0][0]

		## 如果pid为0 则表示总代 那就查询所有顶级代理
		## 如果不为0 则查询该id是否为代理 是代理 则查询该代理明细
		if pid == "":
			return jsonify(datas = [])

	if pid == "0":
		sql = 'select pid from admin_agent_list where pid > 0'
	else:
		sql = 'select pid from admin_agent_list where pid = %s or pre_pid = %s' % (pid, pid)
	agent_pids = [str(i[0]) for i in LogQry(channel).qry(sql)]
	if not agent_pids:
		return jsonify(datas = [])

	## 查询所有层级
	sql = '''
		select id, level_name, first_ladder, second_ladder, third_ladder, 
			fourth_ladder, fifth_ladder
		from admin_agent_level'''
	agent_lv_map = {}
	for k, name, l1, l2, l3, l4, l5 in LogQry(channel).qry(sql):
		agent_lv_map[k] = {
			"name":name,
			"ladder":[l1, l2, l3, l4, l5],
		}

	## 查询对应代理的对应层级
	sql = '''
		select pid, agent_level, (select nick from player where id = pid), 
				(select count(1) from player_agent where invite_id = pid)
		from admin_agent_list
		where pid in (%s)
	''' % ",".join(agent_pids)
	agent_list = {}
	for pid, lv, name, count in LogQry(channel).qry(sql):
		agent_list[pid] = [lv, name, count]

	## 转换查询日期格式
	begin_time = begin_time[0:4] + begin_time[5:7] + begin_time[8:]
	end_time = end_time[0:4] + end_time[5:7] + end_time[8:]

	## 根据查询日期 查询出这段时间里边代理总的佣金等 
	## 需要去除已经结算的
	sql = '''
		select pid, ifnull(sum(pump), 0), ifnull(sum(win), 0)
		from t_agent_day a
		where pid in (%s)
		and time >= %s and time <= %s
		and time > 
			(select ifnull(max(date2) , 0)
			from admin_agent_settlement 
			where pid = a.pid)
		group by pid
	''' % (",".join(agent_pids), begin_time, end_time)
	datas = {}
	for pid, pump, win in LogQry(channel).qry(sql):
		lv = agent_list[pid][0]
		pump = int(pump)
		win = int(win)
		pump_commission, pump_rate = calc_pump_commission(agent_lv_map[lv]["ladder"], pump)
		win_commission, win_rate = calc_win_commission(agent_lv_map[lv]["ladder"], win)
		datas[pid] = {
			"lv":agent_lv_map[lv]["name"],
			"pid":pid,
			"name":agent_list[pid][1],
			"player_count":agent_list[pid][2],
			"pump":pump,
			"win":win,
			"pump_commission":pump_commission,
			"win_commission":win_commission,
			"pump_rate":pump_rate,
			"win_rate":win_rate,
		}

	return jsonify(datas = datas)

## 计算抽水返佣
def calc_pump_commission(ladders, pump):
	for ladder in ladders:
		ladder = eval(ladder)
		if int(ladder["bet_max"]) >= pump and pump >= int(ladder["bet_min"]):
			rate = int(ladder["backwater"])
			break
	else:
		rate = int(ladder["backwater"])

	return int(pump * rate / 10000), rate

## 计算输赢返佣
def calc_win_commission(ladders, win):
	for ladder in ladders:
		ladder = eval(ladder)
		if int(ladder["win_lose_max"]) >= win and win >= int(ladder["win_lose_min"]):
			rate = int(ladder["rebate"])
			return int(win * rate / 10000), rate
	else:
		rate = int(ladder["rebate"])
		return int(win * rate / 10000), rate

## 返佣处理
@busi.route('/agent_commission/do', methods=['GET'])
@login_require
def agent_commission_do():
	# 获取参数
	channel = session['select_channel']
	begin_time = request.args.get('begin_time')
	end_time = request.args.get('end_time')
	pid = request.args.get("pid", "")

	pump_val = int(request.args.get("pump"))
	win_val = int(request.args.get("win"))
	fee = int(request.args.get("fee"))
	other_fee = int(request.args.get("other_fee"))

	stype = int(request.args.get("type"))
	memo = request.args.get("memo", "")

	## 转换查询日期格式
	begin_time = begin_time[0:4] + begin_time[5:7] + begin_time[8:]
	end_time = end_time[0:4] + end_time[5:7] + end_time[8:]

	if pid == "0":
		return jsonify()
	pid = int(pid)

	## 先查询该代理
	sql = 'select pid, agent_level from admin_agent_list'
	agent_list = {}
	for k, v in LogQry(channel).qry(sql):
		agent_list[k] = v
	if not agent_list.has_key(pid):
		return jsonify(error_msg = u"该代理不存在", result = "fail")

	## 获取该代理本次结算时间 同上次最后结算时间中是否有未结算的记录
	sql = '''
		select count(1) 
		from t_agent_day
		where pid = %d
		and time > (select ifnull(max(date2), 0) from admin_agent_settlement where pid = %d)
		and time < %s
	''' % (pid, pid, begin_time)
	if LogQry(channel).qry(sql)[0][0] != 0:
		return jsonify(error_msg = u"该代理中间还有未结算的记录, 请调整日期再结算", result = "fail")

	## 查询所有层级
	sql = '''
		select id, level_name, first_ladder, second_ladder, third_ladder, 
			fourth_ladder, fifth_ladder
		from admin_agent_level'''
	agent_lv_map = {}
	for k, name, l1, l2, l3, l4, l5 in LogQry(channel).qry(sql):
		agent_lv_map[k] = {
			"name":name,
			"ladder":[l1, l2, l3, l4, l5],
		}

	## 获得该代理名下所有代理 以及对应的返佣记录
	sql = 'select pid from admin_agent_list where pid = %d or pre_pid = %d' % (pid, pid)
	agent_pids = [str(i[0]) for i in LogQry(channel).qry(sql)]
	## 根据查询日期 查询出这段时间里边代理总的佣金等 
	## 需要去除已经结算的
	sql = '''
		select pid, ifnull(sum(pump), 0), ifnull(sum(win), 0)
		from t_agent_day a
		where pid in (%s)
		and time >= %s and time <= %s
		and time > 
			(select ifnull(max(date2) , 0)
			from admin_agent_settlement 
			where pid = a.pid)
		group by pid
	''' % (",".join(agent_pids), begin_time, end_time)
	datas = {}
	for aid, pump, win in LogQry(channel).qry(sql):
		pump = int(pump)
		win = int(win)
		lv = agent_list[aid]
		pump_commission, pump_rate = calc_pump_commission(agent_lv_map[lv]["ladder"], pump)
		win_commission, win_rate = calc_win_commission(agent_lv_map[lv]["ladder"], win)
		datas[aid] = {
			"pid":aid,
			"pump_commission":pump_commission,
			"win_commission":win_commission,
		}

	## 计算该代理真正可以拿到的钱
	real_pump = 2 * datas[pid]["pump_commission"] - sum([X["pump_commission"] for X in datas.values()])
	real_win = 2 * datas[pid]["win_commission"] - sum([X["win_commission"] for X in datas.values()])

	## 判断同客户端传上来的是否一致
	if real_pump != pump_val or real_win != win_val:
		return jsonify(result = "fail", error_msg = u'佣金统计不对')

	## 查询结算时 下级会员数
	sql = 'select count(1) from player_agent where invite_id = %d' % pid
	count = LogQry(channel).qry(sql)[0][0]

	## 生成本次处理记录
	sql = '''
		insert into admin_agent_settlement
			(pid, date1, date2, pump_commission, win_commission,
			fee, other_fee, type, memo, count)
		values (%d, %s, %s, %d, %d,
			%d, %d, %d, '%s', %d)
	''' % (pid, begin_time, end_time, real_pump, real_win,
		fee, other_fee, stype, memo, count)
	LogQry(channel).execute(sql)

	return jsonify(result = "ok")

## 查询玩家佣金发放记录
@busi.route('/agent_commission_his', methods=['GET'])
@login_require
def agent_commission_his():
	pid = request.args.get("pid", "")
	channel = session['select_channel']

	size = request.args.get('size')
	offset = request.args.get('offset')

	where = ""
	if pid:
		where += "and pid = %s" % pid

	sql = 'select count(1) from admin_agent_settlement where 1 = 1 %s' % where
	total_count = LogQry(channel).qry(sql)[0][0]

	sql = '''
		select pid, date1, date2, pump_commission, win_commission, 
			fee, other_fee, memo, (select nick from player where id = pid), type
		from admin_agent_settlement
		where 1 = 1
		%s
		limit %s, %s
	''' % (where, offset, size)
	datas = []
	for pid, date1, date2, pump_commission, win_commission, \
		fee, other_fee, memo, name, stype in LogQry(channel).qry(sql):
		datas.append({
			"date1":date1,
			"date2":date2,
			"name":name,
			"pid":pid,
            "pump_commission":pump_commission,
            "win_commission":win_commission,
            "fee":fee,
            "stype":stype,
			"other_fee":other_fee,
			"memo":memo
			})

	return jsonify(datas = datas, total_count = total_count)
