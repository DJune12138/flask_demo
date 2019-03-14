# -*- coding:utf-8 -*-
from flask import render_template, jsonify
from flask.globals import current_app, session, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from . import busi


@busi.route('/', methods=['GET'])
@login_require
def show_base():
    name = session['name']
    role_str = session['role_str']
    sql_oper = SqlOperate()
    try:
        role_text = sql_oper.get_role_text(role_str)
    except Exception as e:
        print e
    # 前端需求，加上menus_list
    user_id = g.user_id
    role_sql = """SELECT role_str FROM user WHERE id=%s""" % user_id
    sql_oper = SqlOperate()
    crole_str = sql_oper.select(role_sql)[0][0]
    menus_list = sql_oper.get_menus_list_by_role_str(crole_str)
    return render_template('base.html', menus_list=menus_list, username=name, role_text=role_text)

@busi.route('/top', methods=['GET'])
@login_require
def show_top():
    name = session['name']
    role_str = session['role_str']
    sql_oper = SqlOperate()
    try:
        role_text = sql_oper.get_role_text(role_str)
    except Exception as e:
        print e

    # 前端需求，加上menus_list
    user_id = g.user_id
    role_sql = """SELECT role_str FROM user WHERE id=%s""" % user_id
    sql_oper = SqlOperate()
    crole_str = sql_oper.select(role_sql)[0][0]
    menus_list = sql_oper.get_menus_list_by_role_str(crole_str)

    return render_template('top.html', username=name, role_text=role_text, menus_list=menus_list)


@busi.route('/left', methods=['GET'])
@login_require
def show_left():
    user_id = g.user_id
    role_sql = """SELECT role_str FROM user WHERE id=%s""" % user_id

    sql_oper = SqlOperate()
    crole_str = sql_oper.select(role_sql)[0][0]
    menus_list = sql_oper.get_menus_list_by_role_str(crole_str)

    return render_template('left.html', menus_list=menus_list)


@busi.route('/index', methods=['GET'])
def show_index():
    return render_template('index.html', content='dasdasdasdasdasdasdasdasd')
