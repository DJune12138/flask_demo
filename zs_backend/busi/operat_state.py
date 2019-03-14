# -*- coding:utf-8 -*-
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, session, jsonify
from zs_backend.utils.const import *
from zs_backend import redis_conn

@busi.route('/operat/state', methods=['GET'])
@login_require
def show_operat_state():
    """财务汇总报表页面"""

    return render_template('operat_state.html')


@busi.route('/retrieve/all/channel', methods=['GET'])
@login_require
def retrieve_all_channel():
    """获取所有渠道名称和ID"""

    channel_list = list()
    for one in session.get('channel'):
        channel_dict = dict()
        channel_dict['name'] = redis_conn.hget(CHANNEL_CONFIG_TABLE+str(one), "name")
        channel_dict['id'] = one
        channel_list.append(channel_dict)
    return jsonify(data=channel_list)
