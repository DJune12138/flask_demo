# -*- coding:utf-8 -*-
import json
from flask import render_template, session, request, jsonify
from zs_backend.busi import busi
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require
from zs_backend.utils.distribution_util import calc_commission

@busi.route('/distribution_agent_list/init', methods=['GET'])
@login_require
def distribution_agent_list_init():
    return render_template('agent_distribution_list.html')

@busi.route('/distribution_agent_list/show', methods=['GET'])
@login_require
def distribution_agent_list_show():
    # 获取参数
    channel = session['select_channel']
    pid = request.args.get('pid')
    nick = request.args.get("nick")

    size = request.args.get('size')
    offset = request.args.get('offset')

    if pid:
        pid = int(pid)
    else:
        pid = 0

    if nick:
        sql = 'select id from player where nick = "%s"' % nick
        try:
            pid = LogQry(channel).qry(sql)[0][0]
        except:
            pid = -1

    sql = 'select count(1) from player_agent where invite_id = %d' % pid
    total_count = LogQry(channel).qry(sql)[0][0]

    datas = []
    sql = '''
        select pid, (select nick from player where id = pid), (select reg_time from player where id = pid), 
                (select count(1) from player_agent where invite_id = a.pid)
        from player_agent a
        where invite_id = %d
        LIMIT %s,%s;
    ''' % (pid, offset, size)
    for line in LogQry(channel).qry(sql):
        datas.append({
            "pid":line[0],
            "nick":line[1],
            "reg_time":line[2],
            "count":line[3]
            })

    return jsonify(result = "ok", datas = datas, total_count = total_count)

@busi.route('/distribution_commission/int', methods=['GET'])
@login_require
def distribution_commission_init():
    """佣金结算页面"""
    return render_template('commission_settlement.html')

@busi.route('/distribution_commission/show', methods=['GET'])
@login_require
def distribution_commission_show():
    """佣金计算查询"""

    # 获取参数
    channel = session['select_channel']
    begin_time = request.args.get('begin_time')
    end_time = request.args.get('end_time')
    begin_time = request.args.get('begin_time')
    end_time = request.args.get('end_time')

    size = request.args.get('size')
    offset = request.args.get('offset')

    ## 转换查询日期格式
    begin_time = begin_time[0:4] + begin_time[5:7] + begin_time[8:]
    end_time = end_time[0:4] + end_time[5:7] + end_time[8:]

    ## 查询总总量
    sql = 'select count(distinct pid) from t_distribution_day where time >= %s and time <= %s' % (begin_time, end_time)
    total_count = LogQry(channel).qry(sql)[0][0]

    ## 根据偏移量查询所有ID
    sql = '''
        select distinct pid 
        from t_distribution_day 
        where time >= %s and time <= %s
        LIMIT %s,%s;
    ''' % (begin_time, end_time, offset, size)
    pids = [str(i[0]) for i in LogQry(channel).qry(sql)]
    if not pids:
        return jsonify(result = "ok", datas = [], total_count = total_count)

    ## 查询这些ID的下级会员数
    members = {}
    sql = 'select invite_id, count(1) from player_agent where invite_id in (%s) group by invite_id' % ",".join(pids)
    for pid, count in LogQry(channel).qry(sql):
        members[pid] = int(count)

    ## 查询分销配置
    sql = 'select pump_section, commission_section from admin_distribution_config limit 1'
    pump_config, commission_config = LogQry(channel).qry(sql)[0]
    pump_config = json.loads(pump_config)
    commission_config = json.loads(commission_config)

    ## 根据查询日期 偏移量
    sql = '''
        select pid, pump, win
        from t_distribution_day a
        where pid in (%s)
        and time >= %s and time <= %s
        and time > 
            (select ifnull(max(date2) , 0)
            from admin_distribution_settlement 
            where pid = a.pid)
    ''' % (",".join(pids), begin_time, end_time)
    datas = {}
    for pid, pump, win in LogQry(channel).qry(sql):
        if not datas.has_key(pid):
            datas[pid] = {
                "pump" : {},
                "win" : {}
            }
        datas[pid] = merge_dict(datas[pid], json.loads(pump), json.loads(win))
        if members.has_key(pid):
            datas[pid]["members_count"] = members[pid]
        else:
            datas[pid]["members_count"] = 0

    ## 遍历玩家数据 计算返佣
    for pid, data in datas.items():
        datas[pid] = calc_commission(data, pump_config, commission_config)

    return jsonify(result = "ok", datas = datas, total_count = total_count)

## 合并字典
def merge_dict(d, pump, win):
    for k, v in pump.items():
        if not d["pump"].has_key(k):
            d["pump"][k] = 0
        d["pump"][k] += v

    for k, v in win.items():
        if not d["win"].has_key(k):
            d["win"][k] = 0
        d["win"][k] += v

    return d

## 返佣处理
@busi.route('/distribution_commission/do', methods=['GET'])
@login_require
def distribution_commission_do():
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

    ## 获取该玩家本次结算时间 同上次最后结算时间中是否有未结算的记录
    sql = '''
        select count(1) 
        from t_distribution_day
        where pid = %d
        and time > (select ifnull(max(date2), 0) from admin_distribution_settlement where pid = %d)
        and time < %s
    ''' % (pid, pid, begin_time)
    if LogQry(channel).qry(sql)[0][0] != 0:
        return jsonify(error_msg = u"中间还有未结算的记录, 请调整日期再结算", result = "fail")

    ## 查询该段时间该玩家的返佣记录
    sql = '''
        select pump, win
        from t_distribution_day a
        where pid = %d
        and time >= %s and time <= %s
        and time > 
            (select ifnull(max(date2) , 0)
            from admin_distribution_settlement 
            where pid = a.pid)
    ''' % (pid, begin_time, end_time)
    datas = {"pump":{}, "win":{}}
    for pump, win in LogQry(channel).qry(sql):
        datas = merge_dict(datas, json.loads(pump), json.loads(win))

    ## 查询分销配置
    sql = 'select pump_section, commission_section from admin_distribution_config limit 1'
    pump_config, commission_config = LogQry(channel).qry(sql)[0]
    pump_config = json.loads(pump_config)
    commission_config = json.loads(commission_config)

    ## 计算返佣
    datas = calc_commission(datas, pump_config, commission_config)

    ## 计算该代理真正可以拿到的钱
    real_pump = sum(datas["pump_commission"].values())
    real_win = sum(datas["win_commission"].values())

    ## 判断同客户端传上来的是否一致
    if real_pump != pump_val or real_win != win_val:
        return jsonify(result = "fail", error_msg = u'佣金统计不对')

    ## 查询结算时 下级会员数
    sql = 'select count(1) from player_agent where invite_id = %d' % pid
    count = LogQry(channel).qry(sql)[0][0]

    ## 生成本次处理记录
    sql = '''
        insert into admin_distribution_settlement
            (pid, date1, date2, pump_commission, win_commission,
            fee, other_fee, type, memo, count)
        values (%d, %s, %s, %d, %d,
            %d, %d, %d, '%s', %d)
    ''' % (pid, begin_time, end_time, real_pump, real_win,
        fee, other_fee, stype, memo, count)
    LogQry(channel).execute(sql)

    return jsonify(result = "ok")

## 查询玩家佣金发放记录
@busi.route('/distribution_commission_his', methods=['GET'])
@login_require
def distribution_commission_his():
    pid = request.args.get("pid")
    channel = session['select_channel']

    size = request.args.get('size')
    offset = request.args.get('offset')

    where = ""
    limit = ""
    if pid:
        where += "and pid = %s" % pid
    if size and offset:
        limit += "limit %s, %s" % (offset, size)

    sql = 'select count(1) from admin_distribution_settlement where 1 = 1 %s' % where
    total_count = LogQry(channel).qry(sql)[0][0]

    sql = '''
        select pid, date1, date2, pump_commission, win_commission, 
            fee, other_fee, memo, (select account_name from player where id = pid), type
        from admin_distribution_settlement
        where 1 = 1
        %s
        %s
    ''' % (where, limit)
    datas = []
    for pid, date1, date2, pump_commission, win_commission, \
        fee, other_fee, memo, name, stype in LogQry(channel).qry(sql):
        datas.append({
            "date1":date1,
            "date2":date2,
            "pid":pid,
            "name":name,
            "pump_commission":pump_commission,
            "win_commission":win_commission,
            "fee":fee,
            "stype":stype,
            "other_fee":other_fee,
            "memo":memo
            })

    return jsonify(datas = datas, total_count = total_count)
