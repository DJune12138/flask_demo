# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, session, jsonify, request
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.busi.agent_list import post_game_agent_change

@busi.route('/agent/add/show', methods=['GET'])
@login_require
def agent_add_show():
    return render_template('agent_add.html')

@busi.route('/agent/list_simple', methods=['GET'])
@login_require
def agent_list_simple():
    sql = '''
        select pid, if(pid = 0, "系统顶级代理", (select nick from player where id = pid))
        from admin_agent_list 
        where status = 1
    '''
    from zs_backend.utils.channel_qry import LogQry, GameWeb

    data = {}
    for pid, name in LogQry(session['select_channel']).qry(sql):
        data[pid] = name

    return jsonify(data = data)

@busi.route('/agent/add/do', methods=['GET'])
@login_require
def agent_add_do():
    # 获取参数
    pid = int(request.args.get('pid'))
    level_id = int(request.args.get('level_id'))
    pre_pid = int(request.args.get('pre_pid'))
    channel = session['select_channel']

    ## 判断该玩家当前是不是代理
    sql = '''
        select sum(if(pid = %d, 1, 0)), sum(if(pid = %d, 1, 0)) 
        from admin_agent_list 
        where pid = %d or pid = %d
    ''' % (pid, pre_pid, pid, pre_pid)
    count, pre_count = LogQry(channel).qry(sql)[0]
    if count != 0:
        return jsonify(result = "fail", msg = u"该玩家已经是代理")
    if pre_count == 0:
        return jsonify(result = "fail", msg = u"找不到该上级代理ID")

    ## 判断是否存该代理层级
    sql = 'select count(1) from admin_agent_level where id = %d' % level_id
    if LogQry(channel).qry(sql)[0][0] != 1:
        return jsonify(result = "fail", msg = u"找不到该代理层级")

    payload = {"pid":pid, "agent_id":pre_pid}
    rr = GameWeb(channel).post("/api/bind_agent", payload)
    if rr["result"] != 0:
        return jsonify(result = "fail", msg = u"同步绑定代理失败")

    ## 插入该代理信息
    sql = '''
        insert into admin_agent_list (pid, agent_level, status, pre_pid)
        values (%d, %d, %d, %d)
    ''' % (pid, level_id, 2, pre_pid)
    LogQry(channel).execute(sql)

    return jsonify(result = "ok")
