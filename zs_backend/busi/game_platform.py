# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.busi import game_parameter
from zs_backend.utils.common import login_require
from flask import render_template, request, session, jsonify
from zs_backend.utils.channel_qry import LogQry, GameWeb

# 功能开关名称映射
function_map = {-1: u'充值按钮', -2: u'提现按钮', -11: u'排序类型'}


@busi.route('/game/platform/show', methods=['GET'])
@login_require
def game_platform_show():
    """游戏平台管理页面"""

    return render_template('game_platform.html')


@busi.route('/game/platform/retrieve', methods=['GET'])
@login_require
def game_platform_retrieve():
    """游戏平台管理查询"""

    # 获取参数
    channel_id = session['select_channel']

    # 从数据库获取游戏开关状态数据
    retrieve_sql = """SELECT game_function_id,status,sort
                      FROM admin_platform
                      WHERE game_function_id>0;"""
    datas = LogQry(channel_id).qry(retrieve_sql)

    # 处理游戏开关的数据
    game_status_dict = dict()
    for game_id, status, sort in datas:
        game_status_dict[game_id] = [status] + [sort]
    all_game_dict = game_parameter.get_subgame_list()
    datas_list_game = list()
    for game_id, game_name in all_game_dict.items():
        game_dict = dict()
        game_dict['game_id'] = game_id
        game_dict['name'] = game_name
        try:
            game_dict['status'] = game_status_dict.get(game_id)[0]
        except TypeError:
            game_dict['status'] = -1
        try:
            game_dict['sort'] = game_status_dict.get(game_id)[1]
        except TypeError:
            game_dict['sort'] = ''
        datas_list_game.append(game_dict)

    # 游戏开关根据sort排序
    datas_list_game.sort(key=lambda x: x['sort'])

    # 从数据库获取功能开关状态数据
    retrieve_sql = """SELECT game_function_id,status
                      FROM admin_platform
                      WHERE game_function_id<0;"""
    datas = LogQry(channel_id).qry(retrieve_sql)

    # 处理游戏功能开关的数据
    function_status_dict = dict()
    for function_id, status in datas:
        function_status_dict[function_id] = status
    datas_list_function = list()
    for function_id, function_name in function_map.items():
        function_dict = dict()
        function_dict['function_id'] = function_id
        function_dict['name'] = function_name
        function_dict['status'] = function_status_dict.get(function_id, -1)
        datas_list_function.append(function_dict)

    # 返回模板与数据
    return jsonify(data_function=datas_list_function, data_game=datas_list_game)


@busi.route('/game/platform/update', methods=['POST'])
@login_require
def game_platform_update():
    """修改游戏平台管理"""

    # 获取参数
    update_list = request.form.get('update_list')
    channel_id = session['select_channel']

    up = eval(update_list)

    ## 给游戏web发送的数据
    payload = list()

    ## 本次修改插入的数据
    sql0 = "insert into admin_platform (game_function_id, status, sort) values "
    sql_v = []

    ## 遍历参数
    for ele in up:
        payload_list = list()
        func_id = ele["primary_id"]
        status = int(ele["status"])
        sort = ele.get('sort', 'null')
        sql_v.append("(%s, %d, %s)" % (func_id, status, sort))
        if status >= 0 or func_id == '-11':
            payload_list.append(int(func_id))
            payload_list.append(status)
            payload.append(payload_list)

    ## 生成要插入的sql语句
    sql = "%s %s" % (sql0, ",".join(sql_v))

    ## 先删除原有数据
    LogQry(channel_id).execute("delete from admin_platform")
    LogQry(channel_id).execute(sql)

    print GameWeb(int(channel_id)).post("/api/game_open", {'ui_list': payload})

    # 返回应答
    return jsonify(result=1, msg=u'发布成功！')
