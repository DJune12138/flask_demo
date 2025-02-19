# -*- coding:utf-8 -*-
from zs_backend.utils import game_util
from zs_backend.busi import busi, game_parameter
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require
from flask import render_template, jsonify, request, session


@busi.route('/agent/level/show', methods=['GET'])
@login_require
def agent_level_show():
    """代理层级页面"""

    return render_template('agent_level.html')


@busi.route('/agent/level/retrieve', methods=['GET'])
@login_require
def agent_level_retrieve():
    """代理层级查询"""

    # 获取参数
    channel_id = session['select_channel']

    ## 如果没有代理层级 则插入一条顶级代理
    sql = 'select count(1) from admin_agent_level'
    if LogQry(channel_id).qry(sql)[0][0] == 0:
        sql = 'insert into admin_agent_level (id, level_name) values (1, "顶级代理")'
        LogQry(channel_id).execute(sql)

    # 从数据库获取数据
    retrieve_sql = """SELECT id,level_name,grant_brokerage,first_ladder,second_ladder,
                              third_ladder,fourth_ladder,fifth_ladder
                      FROM admin_agent_level;"""
    data = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    data_list = list()
    for level_id, level_name, grant_brokerage, first_ladder, second_ladder, \
        third_ladder, fourth_ladder, fifth_ladder in data:
        data_dict = dict()
        data_dict['level_id'] = level_id
        data_dict['level_name'] = level_name
        data_dict['grant_brokerage'] = grant_brokerage
        data_dict['first_ladder'] = first_ladder
        data_dict['second_ladder'] = second_ladder
        data_dict['third_ladder'] = third_ladder
        data_dict['fourth_ladder'] = fourth_ladder
        data_dict['fifth_ladder'] = fifth_ladder
        data_list.append(data_dict)

    # 返回数据
    return jsonify(data=data_list)


@busi.route('/agent/level/create/update', methods=['POST'])
@login_require
def agent_level_create_update():
    """代理层级新建/修改"""

    # 获取参数
    channel_id = session['select_channel']
    level_name = request.form.get('level_name')
    grant_brokerage = request.form.get('grant_brokerage')
    first_ladder = request.form.get('first_ladder')
    second_ladder = request.form.get('second_ladder')
    third_ladder = request.form.get('third_ladder')
    fourth_ladder = request.form.get('fourth_ladder')
    fifth_ladder = request.form.get('fifth_ladder')
    old_name = request.form.get('old_name')
    level_id = request.form.get('level_id')

    # 校验参数
    if not level_name:
        return jsonify(result=0, msg=u'代理层级名称不能为空！')
    if not level_id or (level_id and level_name != old_name):
        retrieve_sql = """SELECT level_name
                          FROM admin_agent_level;"""
        data = LogQry(int(channel_id)).qry(retrieve_sql)
        for one in data:
            if one[0] == level_name:
                return jsonify(result=0, msg=u'代理层级名称已存在！')
    try:
        int(eval(first_ladder)['win_lose_max'])
        int(eval(first_ladder)['win_lose_min'])
        int(eval(first_ladder)['bet_max'])
        int(eval(first_ladder)['bet_min'])
        int(eval(first_ladder)['rebate'])
        int(eval(first_ladder)['backwater'])
        int(eval(second_ladder)['win_lose_max'])
        int(eval(second_ladder)['win_lose_min'])
        int(eval(second_ladder)['bet_max'])
        int(eval(second_ladder)['bet_min'])
        int(eval(second_ladder)['rebate'])
        int(eval(second_ladder)['backwater'])
        int(eval(third_ladder)['win_lose_max'])
        int(eval(third_ladder)['win_lose_min'])
        int(eval(third_ladder)['bet_max'])
        int(eval(third_ladder)['bet_min'])
        int(eval(third_ladder)['rebate'])
        int(eval(third_ladder)['backwater'])
        int(eval(fourth_ladder)['win_lose_max'])
        int(eval(fourth_ladder)['win_lose_min'])
        int(eval(fourth_ladder)['bet_max'])
        int(eval(fourth_ladder)['bet_min'])
        int(eval(fourth_ladder)['rebate'])
        int(eval(fourth_ladder)['backwater'])
        int(eval(fifth_ladder)['win_lose_max'])
        int(eval(fifth_ladder)['win_lose_min'])
        int(eval(fifth_ladder)['bet_max'])
        int(eval(fifth_ladder)['bet_min'])
        int(eval(fifth_ladder)['rebate'])
        int(eval(fifth_ladder)['backwater'])
    except ValueError:
        return jsonify(result=0, msg=u'输赢金额与押注金额为数字，且最多两位小数！返佣比例与反水比例为整数纯数字！')

    # 新建代理层级
    if not level_id:
        create_sql = """INSERT INTO admin_agent_level
                        VALUES (0,'%s',%s,'%s','%s','%s',
                        '%s','%s');""" \
                     % (level_name, grant_brokerage, first_ladder, second_ladder, third_ladder,
                        fourth_ladder, fifth_ladder)
        LogQry(int(channel_id)).execute(create_sql)
        return jsonify(result=1, msg=u'新建成功！')

    # 修改代理层级
    else:
        update_sql = """UPDATE admin_agent_level
                        SET level_name='%s',grant_brokerage=%s,first_ladder='%s',second_ladder='%s',third_ladder='%s',
                            fourth_ladder='%s',fifth_ladder='%s'
                        WHERE id=%s;""" \
                     % (level_name, grant_brokerage, first_ladder, second_ladder, third_ladder,
                        fourth_ladder, fifth_ladder, level_id)
        LogQry(int(channel_id)).execute(update_sql)
        return jsonify(result=1, msg=u'修改成功！')


@busi.route('/agent/level/game/json', methods=['GET'])
@login_require
def agent_level_game_json():
    """返回代理层级页面用的游戏json数据"""

    # 获取游戏数据
    all_game_dict = game_parameter.get_subgame_list()

    # 处理数据
    game_list = list()
    for game_id, game_name in all_game_dict.items():
        game_dict = dict()
        game_dict['id'] = game_id
        game_dict['name'] = game_name
        game_list.append(game_dict)

    # 返回数据
    return jsonify(data=game_list)


@busi.route('/agent/level/delete', methods=['DELETE'])
@login_require
def agent_level_delete():
    """代理层级删除"""

    # 获取参数
    level_id = request.form.get('level_id')
    channel_id = session['select_channel']

    # 判断是否顶级代理，若是顶级代理，则不予删除
    if level_id == '1':
        return jsonify(msg=u'顶级代理不能删除！')

    # 从数据库删除数据
    delete_sql = """DELETE FROM admin_agent_level
                    WHERE id=%s;""" % level_id
    LogQry(int(channel_id)).execute(delete_sql)

    # 返回应答
    return jsonify(msg=u'删除成功')


@busi.route('/agent/level/default', methods=['POST'])
@login_require
def agent_level_default():
    """每个渠道的默认层级"""

    # 获取参数
    channel_id = session['select_channel']
    agent_pattern_id = request.form.get('agent_pattern_id')
    first_ladder = request.form.get('first_ladder')
    second_ladder = request.form.get('second_ladder')
    third_ladder = request.form.get('third_ladder')
    fourth_ladder = request.form.get('fourth_ladder')
    fifth_ladder = request.form.get('fifth_ladder')

    # 如果是传统代理模式，先从数据库查出是否没有代理层级，没有就新建一个默认层级
    if agent_pattern_id == '1':
        retrieve_sql = """SELECT count(*)
                          FROM admin_agent_level;"""
        data = LogQry(channel_id).qry(retrieve_sql)[0][0]
        if data == 0:
            create_sql = """INSERT INTO admin_agent_level
                            VALUES (0,'默认层级',1,'%s','%s','%s','%s','%s');""" \
                         % (first_ladder, second_ladder, third_ladder, fourth_ladder, fifth_ladder)
            LogQry(channel_id).execute(create_sql)
        return jsonify(result=1)

    # 如果是分销代理模式，先从数据库查出是否没有代理层级，没有就新建四个默认层级
    elif agent_pattern_id == '2':
        retrieve_sql = """SELECT count(*)
                          FROM admin_agent_level;"""
        data = LogQry(channel_id).qry(retrieve_sql)[0][0]
        if data == 0:
            create_sql = """INSERT INTO agent_level
                            VALUES (0,'本级代理',1,'%s','%s','%s','%s','%s'),
                                    (0,'一级代理',1,'%s','%s','%s','%s','%s'),
                                    (0,'二级代理',1,'%s','%s','%s','%s','%s'),
                                    (0,'三级代理',1,'%s','%s','%s','%s','%s');""" \
                         % (first_ladder, second_ladder, third_ladder, fourth_ladder, fifth_ladder,
                            first_ladder, second_ladder, third_ladder, fourth_ladder, fifth_ladder,
                            first_ladder, second_ladder, third_ladder, fourth_ladder, fifth_ladder,
                            first_ladder, second_ladder, third_ladder, fourth_ladder, fifth_ladder)
            LogQry(channel_id).execute(create_sql)
        return jsonify(result=1)

    # 都不是，直接返回应答
    else:
        return jsonify(result=1)


@busi.route('/agent/level/player/update', methods=['PUT'])
@login_require
def agent_level_player_update():
    """玩家代理层级修改"""

    # 获取参数
    pid = request.form.get('pid')
    level = request.form.get('level')
    channel_id = session['select_channel']

    # 修改数据
    update_sql = """UPDATE admin_agent_list
                    SET agent_level=%s
                    WHERE pid=%s;""" \
                 % (level, pid)
    LogQry(channel_id).execute(update_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'修改成功！')
