# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, request, jsonify, session
from zs_backend.utils.channel_qry import *


@busi.route('/member/level/retrieve', methods=['GET'])
@login_require
def member_level_details():
    """玩家层级页面（查询）"""

    # 获取参数
    channel_id = session['select_channel']

    ## 查询层级数量 如果没有 则默认生成一条
    sql= 'select count(1) from admin_member_level'
    count = LogQry(channel_id).qry(sql)[0][0]
    if count == 0:
        sql = '''
            insert into admin_member_level 
                (id, member_level_name, number_withdrawals, over_operation_id, fee_charging,
                min_withdrawals, max_withdrawals, inspect_id, inspect_tips, channel_id,
                is_delete) 
            values (1, "默认层级", 1, 1, 0,
            100, 1000, 1, "", %d,
            0)
        ''' % channel_id
        LogQry(channel_id).execute(sql)

    retrieve_sql = """
        SELECT member_level_name,number_withdrawals,min_withdrawals,max_withdrawals,id,
            channel_id 
        FROM admin_member_level 
        WHERE is_delete=0 
        AND channel_id=%s;
    """ % channel_id
    datas = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    datas_list = list()
    for member_level_name, number_withdrawals, min_withdrawals, max_withdrawals, level_id, \
        channel_id in datas:
        data_dict = dict()
        data_dict['member_level_name'] = member_level_name
        data_dict['number_withdrawals'] = number_withdrawals
        data_dict['min_withdrawals'] = min_withdrawals
        data_dict['max_withdrawals'] = max_withdrawals
        data_dict['level_id'] = level_id
        data_dict['channel_id'] = channel_id
        datas_list.append(data_dict)

    # 返回模版与数据
    return render_template('member_level.html', datas=datas_list, SelectChannel=int(channel_id))


@busi.route('/member/level/json/update', methods=['GET'])
@login_require
def member_level_json_update():
    """返回修改页面用的旧数据"""

    # 获取参数
    level_id = request.args.get('level_id')

    # 从数据库获取数据
    retrieve_sql = """
        SELECT member_level_name,number_withdrawals,over_operation_id,fee_charging,min_withdrawals,
            max_withdrawals,inspect_id,inspect_tips 
        FROM admin_member_level 
        WHERE id=%s;""" % level_id
    datas = LogQry(session['select_channel']).qry(retrieve_sql)[0]

    # 处理数据
    data_dict = dict()
    data_dict['member_level_name'] = datas[0]
    data_dict['number_withdrawals'] = datas[1]
    data_dict['over_operation_id'] = datas[2]
    data_dict['fee_charging'] = datas[3]
    data_dict['min_withdrawals'] = datas[4]
    data_dict['max_withdrawals'] = datas[5]
    data_dict['inspect_id'] = datas[6]
    data_dict['inspect_tips'] = datas[7]

    # 返回数据
    return jsonify(datas=data_dict)


@busi.route('/member/level/update/create', methods=['POST'])
@login_require
def member_level_update_create():
    """修改/新建玩家层级"""

    # 获取参数
    member_level_name = request.form.get('member_level_name')
    number_withdrawals = request.form.get('number_withdrawals')
    over_operation_id = request.form.get('over_operation_id')
    fee_charging = request.form.get('fee_charging')
    min_withdrawals = request.form.get('min_withdrawals')
    max_withdrawals = request.form.get('max_withdrawals')
    inspect_id = request.form.get('inspect_id')
    inspect_tips = request.form.get('inspect_tips')
    level_id = request.form.get('level_id')
    channel_id = session['select_channel']
    old_name = request.form.get('old_name')
    old_channel = request.form.get('old_channel')

    # 校验并组织参数
    if not all([member_level_name, min_withdrawals, max_withdrawals]):
        return jsonify(result=0, msg=u'请输入完整参数！')
    try:
        int(min_withdrawals)
        int(max_withdrawals)
    except ValueError as e:
        return jsonify(result=0, msg=u'单笔最低和单笔最高为整数纯数字！')
    if over_operation_id == '2' or over_operation_id == '3':
        try:
            int(fee_charging)
        except ValueError as e:
            return jsonify(result=0, msg=u'手续费为整数纯数字！')
    if not fee_charging:
        fee_charging = 'null'

    # 修改玩家层级
    if level_id:
        if member_level_name != old_name:
            # 查找玩家层级名称是否重复
            retrieve_sql = """
                SELECT member_level_name 
                FROM admin_member_level 
                WHERE is_delete=0 
                AND channel_id=%s;""" % old_channel
            names = LogQry(session['select_channel']).qry(retrieve_sql)
            for name in names:
                if name[0] == member_level_name:
                    return jsonify(result=0, msg=u'玩家层级名称已被使用！')
        # 存进数据库并返回应答
        create_sql = """
            UPDATE admin_member_level 
            SET member_level_name='%s',number_withdrawals=%s,over_operation_id=%s,fee_charging=%s,
                min_withdrawals=%s,max_withdrawals=%s,inspect_id=%s,inspect_tips='%s' 
            WHERE id=%s;
        """ % (member_level_name, number_withdrawals, over_operation_id, fee_charging, min_withdrawals,
            max_withdrawals, inspect_id, inspect_tips, level_id)
        LogQry(session['select_channel']).execute(create_sql)

        if not sync_config_to_game(session['select_channel']):
            return jsonify(result = 0, msg=u'同步数据到游戏失败,请重新保存')

        return jsonify(result=1, msg=u'修改玩家层级成功！')

    # 新建玩家层级
    else:
        # 查找玩家层级名称是否重复
        retrieve_sql = """
            SELECT member_level_name 
            FROM admin_member_level 
            WHERE is_delete=0 
            AND channel_id=%s;""" % channel_id
        names = LogQry(session['select_channel']).qry(retrieve_sql)
        for name in names:
            if name[0] == member_level_name:
                return jsonify(result=0, msg=u'玩家层级名称已被使用！')
        # 存进数据库并返回应答
        create_sql = """
            INSERT INTO admin_member_level
                (member_level_name,number_withdrawals,over_operation_id,fee_charging, min_withdrawals,
                max_withdrawals,inspect_id,inspect_tips,channel_id) 
            VALUES('%s',%s,%s,%s,%s,
                %s,%s,'%s',%s);
        """ % (member_level_name, number_withdrawals, over_operation_id, fee_charging, min_withdrawals,
            max_withdrawals, inspect_id, inspect_tips, channel_id)
        LogQry(session['select_channel']).execute(create_sql)

        if not sync_config_to_game(session['select_channel']):
            return jsonify(result = 0, msg=u'同步数据到游戏失败,请重新保存')

        return jsonify(result=1, msg=u'新建玩家层级成功！')

@busi.route('/member/level/delete', methods=['PUT'])
@login_require
def member_level_delete():
    """删除玩家层级"""

    # 获取参数
    level_id = request.form.get('level_id')

    # 存进数据库
    update_sql = """UPDATE admin_member_level SET is_delete=1 WHERE id=%s;""" % level_id
    LogQry(session['select_channel']).execute(update_sql)

    if not sync_config_to_game(session['select_channel']):
        return jsonify(result = 0, msg=u'同步数据到游戏失败,请重新保存')

    # 返回应答
    return jsonify(msg=u'删除玩家层级成功！')


@busi.route('/member/level/json/name', methods=['GET'])
@login_require
def member_level_json_name():
    """返回对应渠道玩家层级所有名称"""

    # 获取参数
    channel_id = session['select_channel']

    # 从数据库获取数据
    retrieve_sql = """
        SELECT id,member_level_name 
        FROM admin_member_level 
        WHERE channel_id=%s 
        AND is_delete=0;""" % channel_id
    datas = LogQry(channel_id).qry(retrieve_sql)

    # 组织数据
    datas_list = list()
    for level_id, member_level_name in datas:
        data_dict = dict()
        data_dict['id'] = level_id
        data_dict['name'] = member_level_name
        datas_list.append(data_dict)

    # 返回数据
    return jsonify(datas=datas_list)

def sync_config_to_game(channel):
    sql = '''
        select id, number_withdrawals, over_operation_id, min_withdrawals, max_withdrawals
        from admin_member_level
        where is_delete=0
    '''
    data = {}
    for vip, number_withdrawals, over_operation_id, min_withdrawals, max_withdrawals in LogQry(channel).qry(sql):
        data[vip] = {
            "number_withdrawals":number_withdrawals,
            "over_operation_id":over_operation_id,
            "min_withdrawals":min_withdrawals,
            "max_withdrawals":max_withdrawals,
            }

    if GameWeb(channel).post("/api/set_cash_params", data)["result"] == "succ":
        return True
    else:
        return False
