# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils import time_util, game_util
from zs_backend.utils.channel_qry import LogQry, GameWeb
from zs_backend.utils.common import login_require
from flask import render_template, request, session, jsonify

# 代理状态映射
block_up = 0  # 停用
start_using = 1  # 启用
wait_audit = 2  # 待审
map_agent_status = {
    0: u'停用',
    1: u'启用',
    2: u'待审'
}


@busi.route('/agent/list/show', methods=['GET'])
@login_require
def agent_list_show():
    """代理列表页面"""

    # 页面内容
    content = [u'<select id="level" class="level"></select>']

    # 返回模版与数据
    return render_template('agent_list.html', content=content)


@busi.route('/agent/list/json/level', methods=['GET'])
@login_require
def agent_list_json_level():
    """代理列表新建代理时返回的玩家层级信息数据"""

    # 获取参数
    channel_id = session['select_channel']

    # 查询数据库
    retrieve_sql = """SELECT id,level_name
                      FROM admin_agent_level;"""
    data = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    data_list = list()
    for level_id, level_name in data:
        data_dict = dict()
        data_dict['level_id'] = level_id
        data_dict['level_name'] = level_name
        data_list.append(data_dict)

    # 返回数据
    return jsonify(data=data_list)


@busi.route('/agent/list/json/nick', methods=['GET'])
@login_require
def agent_list_json_nick():
    """获取玩家昵称"""

    # 获取参数
    pid = request.args.get('pid')
    channel_id = session['select_channel']

    # 校验参数
    try:
        int(pid)
    except ValueError:
        return jsonify(result=0, msg=u'玩家ID必须为整数纯数字！')

    # 查询数据库
    retrieve_sql = """SELECT nick
                      FROM player
                      WHERE id=%s;""" % pid
    data = LogQry(int(channel_id)).qry(retrieve_sql)

    # 根据数据返回数据或应答
    try:
        data = data[0][0]
    except IndexError:
        return jsonify(result=0, msg=u'没有此玩家！')
    else:
        return jsonify(result=1, data=data)


@busi.route('/agent/list/create', methods=['POST'])
@login_require
def agent_list_create():
    """代理列表新建代理"""

    # 获取参数
    pid = request.form.get('pid')
    channel_id = request.form.get('channel_id')
    level_id = request.form.get('level_id')
    pre_pid = request.form.get('pre_pid')

    # 查询数据库取出此玩家信息并判断此玩家是否存在
    retrieve_sql = """SELECT id
                      FROM player
                      WHERE id=%s;""" % pid
    data = LogQry(int(channel_id)).qry(retrieve_sql)
    if not data:
        return jsonify(result=0, msg=u'没有此玩家！')

    # 查询数据库判断此玩家是否已成为该渠道的代理
    retrieve_sql = """SELECT count(*)
                      FROM admin_agent_list
                      WHERE pid=%s;""" % pid
    data = LogQry(int(channel_id)).qry(retrieve_sql)[0][0]
    if data == 1:
        return jsonify(result=0, msg=u'此玩家已是代理！')

    # 添加玩家信息进数据库
    create_sql = """
        INSERT INTO admin_agent_list (pid, agent_level, status, pre_pid)
        VALUES (%s,%s,%d,%s)
    """ % (pid, level_id, wait_audit, pre_pid)
    LogQry(int(channel_id)).execute(create_sql)

    # 返回应答
    return jsonify(result=1, msg=u'添加代理成功！')


@busi.route('/agent/list/retrieve', methods=['GET'])
@login_require
def agent_list_retrieve():
    """代理列表查询"""

    # 获取参数
    channel_id = session['select_channel']
    agent_level = request.args.get('agent_level')
    PlayerID = request.args.get('PlayerID')
    NickName = request.args.get('NickName')
    Account = request.args.get('Account')
    # sort = request.args.get('sort')
    size = request.args.get('size')
    offset = request.args.get('offset')

    # 校验参数
    if (PlayerID and NickName) or (PlayerID and Account) or (NickName and Account):
        return jsonify(result=0, msg=u'玩家ID、玩家昵称、玩家账号只能输入其一！')
    if PlayerID:
        try:
            int(PlayerID)
        except ValueError:
            return jsonify(result=0, msg=u'玩家ID为整数纯数字！')

    ## 判断是否有代理 没有则添加一个顶级代理
    sql = 'select count(1) from admin_agent_list where pid <> 0'
    if LogQry(channel_id).qry(sql)[0][0] == 0:
        sql = 'insert into admin_agent_list (pid, agent_level, status, pre_pid) values (0, 1, 1, 0)'
        LogQry(channel_id).execute(sql)

    # 处理参数
    where = ''
    if agent_level and agent_level != '0':
        where += ' AND agent_level=%s' % agent_level
    if PlayerID:
        where += ' AND pid=%s' % PlayerID
    elif NickName:
        retrieve_sql = """SELECT id
                          FROM player
                          WHERE nick='%s';""" % NickName
        pid = LogQry(channel_id).qry(retrieve_sql)[0][0]
        where += ' AND pid=%s' % pid
    elif Account:
        retrieve_sql = """SELECT id
                          FROM player
                          WHERE account_name='%s';""" % Account
        pid = LogQry(channel_id).qry(retrieve_sql)[0][0]
        where += ' AND pid=%s' % pid

    # 查询数据
    retrieve_sql = """SELECT count(*) FROM admin_agent_list where 1 = 1 %s;""" % where
    total_count = LogQry(channel_id).qry(retrieve_sql)[0][0]
    retrieve_sql = """SELECT (select level_name from admin_agent_level where id=agent_level),pid,status,pre_pid,
                                (select account_id from player where id=pid),
                              (select nick from player where id=pid),(select coin from player where id=pid) as coin,
                                (select counter from player where id=pid),
                                (select reg_time from player where id=pid) as reg_time,
                                (select last_login_time from player where id=pid) as last_login_time
                      FROM admin_agent_list
                      WHERE 1 = 1
                        %s
                      ORDER BY status DESC
                      LIMIT %s,%s;""" \
                   % (where, offset, size)
    data = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    data_list = list()
    for lv, pid, status, pre_pid, account_id, \
        name, coin, counter, register_time, last_login_time in data:
        if pid == 0:
            continue
        data_dict = dict()
        data_dict['agent_level'] = lv
        data_dict['pid'] = pid
        data_dict['status'] = map_agent_status[status]
        data_dict['pre_pid'] = pre_pid
        data_dict['account_id'] = account_id
        data_dict['name'] = name
        data_dict['register_time'] = register_time
        data_dict['login_time'] = last_login_time
        data_dict['coin'] = coin
        data_dict['bank'] = game_util.get_bank_coin(counter)
        data_list.append(data_dict)

    # 返回数据
    return jsonify(result=1, data=data_list, dataLength=total_count)


@busi.route('/agent/list/lower/agent', methods=['GET'])
@login_require
def agent_list_lower_agent():
    """代理列表下级代理查询"""
    channel_id = session['select_channel']
    ## 查询所有层级
    sql = 'select id, level_name from admin_agent_level'
    agent_level = {}
    for k, v in LogQry(channel_id).qry(sql):
        agent_level[k] = v

    # 获取参数
    pid = request.args.get('pid')
    size = request.args.get('size')
    offset = request.args.get('offset')

    ## 查询总数
    sql = 'select count(1) from player_agent where invite_id = %s' % pid
    total_count = LogQry(channel_id).qry(sql)[0][0]

    ## 查询代理列表
    sql = """
        SELECT (select agent_level from admin_agent_list where pid = a.pid), pid
        FROM player_agent a
        WHERE invite_id = %s
        LIMIT %s, %s;
    """ % (pid, offset, size)
    data = LogQry(int(channel_id)).qry(sql)
    data_list = list()
    for lv, pid in data:
        data_dict = dict()
        if lv:
            data_dict['agent_level'] = agent_level[lv]
        else:
            data_dict['agent_level'] = ""
        data_dict['pid'] = pid

        sql = '''
            select nick, coin, counter, reg_time, last_login_time 
            from player 
            where id = %d
        ''' % pid
        name, coin, counter, register_time, last_login_time = LogQry(channel_id).qry(sql)[0]

        data_dict['name'] = name
        data_dict['register_time'] = register_time
        data_dict['login_time'] = last_login_time
        data_dict['coin'] = coin
        data_dict['bank'] = game_util.get_bank_coin(counter)
        data_list.append(data_dict)

    # 返回数据
    return jsonify(result=1, data=data_list, dataLength=total_count)


@busi.route('/agent/list/amend/status', methods=['PUT'])
@login_require
def agent_list_amend_status():
    """修改代理状态"""
    # 获取参数
    channel_id = session['select_channel']
    pid = request.form.get('pid')
    status = request.form.get('status')

    # 处理参数
    pid = pid.strip()
    update_sql = "UPDATE admin_agent_list SET status=%s WHERE pid=%s;" % (status, pid)
    LogQry(int(channel_id)).execute(update_sql)

    if status == '1':  ## 启用代理
        if not post_game_agent_change(int(channel_id), pid):
            return jsonify(result=0, msg=u'修改代理状态失败！')
    else:  ## 禁用代理
        if not post_game_agent_change(int(channel_id), pid):
            return jsonify(result=0, msg=u'修改代理状态失败！')

    return jsonify(result=1, msg=u'修改代理状态成功！')


def post_game_agent_change(channel, pid):
    use = []
    nouse = []
    sql = 'select pid, status from admin_agent_list'
    for pid, status in LogQry(channel).qry(sql):
        if pid == 0:
            continue
        if status == 1:
            use.append(pid)
        elif status == 0:
            nouse.append(pid)

    payload = {"use": use, "nouse": nouse, "pid": pid}
    rr = GameWeb(channel).post("/api/set_agent_list", payload)
    if rr["result"] == "succ":
        return True

    return False
