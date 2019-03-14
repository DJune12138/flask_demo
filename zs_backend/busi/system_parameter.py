# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, request, jsonify, session
from zs_backend.utils.channel_qry import LogQry, GameWeb


@busi.route('/system/parameter/show', methods=['GET'])
@login_require
def system_parameter_show():
    """系统参数页面"""

    return render_template('system_parameter.html')

@busi.route('/system/parameter/retrieve', methods=['GET'])
@login_require
def system_parameter_retrieve():
    """系统参数查询"""

    # 获取参数
    channel_id = session['select_channel']

    # 从数据库获取数据
    retrieve_sql = '''SELECT * FROM admin_system_parameter'''
    data = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    data_dict = dict()
    for name, val in data:
        data_dict[name] = val

    # 返回数据
    return jsonify(data=data_dict)

@busi.route('/system/parameter/create/update', methods=['POST'])
@login_require
def system_parameter_create_update():
    """系统参数新建/修改"""

    # 获取参数
    channel_id = session['select_channel']
    agent_pattern = request.form.get('agent_pattern')
    default_level = request.form.get('default_level')
    phone_service_url = request.form.get('phone_service_url')

    data = []
    for k, v in request.form.items():
        data.append("('%s','%s')" % (k, v))

    # 在数据库新建或修改数据
    sql = '''
        REPLACE INTO admin_system_parameter 
            (`name`, `val`)
        VALUES %s
    ''' % (",".join(data))
    LogQry(channel_id).execute(sql)

    payload = {"data":request.form.items()}
    GameWeb(channel_id).post("/api/set_system_parameter", payload)

    # 返回应答
    return jsonify(msg=u'保存成功！')
