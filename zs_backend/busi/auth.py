# -*- coding:utf-8 -*-
from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, request, g, session
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from . import busi


def is_sys(role_str):
    return '1' in role_str.split("/")


@busi.route('/roles', methods=['GET'])
@login_require
def get_role():
    return render_template('index_auth.html')


@busi.route('/roles/retrieve', methods=['GET'])
@login_require
def role_retrieve():
    sql_oper = SqlOperate()

    cuser_id = g.user_id
    crole_sql = """SELECT role_str FROM user WHERE id=%s""" % cuser_id
    crole_str_tup = sql_oper.select(crole_sql)[0]

    crole_tup_str = '(' + crole_str_tup[0].replace('/', ',') + ')'

    if is_sys(crole_str_tup[0]):
        parent_role_sql = """SELECT id FROM role;"""
        roles_sql = """SELECT id, name, parent_id FROM role;"""
    else:
        parent_role_sql = """SELECT id
                            FROM role 
                            WHERE (id IN %s AND parent_id=1);""" \
                          % crole_tup_str

        roles_sql = """SELECT id, name, parent_id 
                    FROM role 
                    WHERE id!=1 
                    AND (id IN %s OR parent_id IN %s);""" % (crole_tup_str, crole_tup_str)

    parent_roles_tup = sql_oper.select(parent_role_sql)
    roles_tup = sql_oper.select(roles_sql)

    role_list = []
    for role in roles_tup:
        role_dict = dict()
        role_dict['id'] = role[0]
        role_dict['name'] = role[1]
        role_dict['parent_id'] = role[2]
        role_dict['parent_name'] = sql_oper.get_parent_role_name(role[2])
        role_list.append(role_dict)

    parent_list = []
    for parent_role in parent_roles_tup:
        parent_role_dict = dict()
        parent_role_dict['id'] = parent_role[0]
        parent_role_dict['name'] = sql_oper.get_parent_role_name(parent_role[0])
        parent_list.append(parent_role_dict)

    return jsonify(result='ok', roles=role_list, parents=parent_list)


@busi.route('/roles', methods=['POST'])
@login_require
def add_role():
    json_dict = request.form
    role_name = json_dict.get('name')
    parent_role = int(json_dict.get('parent'))

    sql_oper = SqlOperate()
    try:
        sql = 'select ifnull(max(id), 2) from role'
        idx = int(sql_oper.select(sql)[0][0]) + 1
        role_add_sql = """INSERT INTO role VALUES (%d, '%s', %d);""" % (idx, role_name, parent_role)
        sql_oper.insert(role_add_sql)
    except Exception as e:
        print e
        current_app.logger.error(e)
        return jsonify(errmsg='数据库查询失败')

    # 如果不是管理员 则还需要把该角色加入到当前渠道的可操作角色中去
    crole_list = session['role_str'].split('/')
    admin = '1' in crole_list
    print "admin:", admin
    if not admin:
        sql = '''
            update channel 
            set role_str = concat_ws("/", role_str, "%d") 
            where id = %d
        ''' % (idx, session['select_channel'])
        sql_oper.update(sql)
        print sql

    return redirect(url_for('busi.get_role'))


@busi.route('/roles/set', methods=['POST'])
@login_require
def set_role():
    json_dict = request.form
    role_id = json_dict.get('role_id')
    role_name = json_dict.get('name')
    parent_id = json_dict.get('parent')

    role_update_sql = """UPDATE role SET name='%s', parent_id=%s WHERE id=%s;""" % (
        role_name, parent_id, role_id)

    print role_update_sql
    sql_oper = SqlOperate()
    sql_oper.update(role_update_sql)

    return redirect(url_for('busi.get_role'))


@busi.route('/roles', methods=['DELETE'])
@login_require
def delete_role():
    role_id = request.json.get('role_id')
    del_role_sql = """DELETE FROM role WHERE id=%s""" % role_id

    sql_oper = SqlOperate()
    try:
        sql_oper.delete(del_role_sql)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errmsg='数据库操作失败')

    return jsonify(errmsg='删除成功')


@busi.route('/roles/edit', methods=['GET'])
@login_require
def show_oper_role():
    role_id = request.args.get('role_id')
    parent_id = int(request.args.get('parent_id'))

    sql_oper = SqlOperate()
    cuser_id = g.user_id
    crole_sql = """SELECT role_str FROM user WHERE id=%s""" % cuser_id
    crole_str_tup = sql_oper.select(crole_sql)[0]

    crole_tup_str = '(' + crole_str_tup[0].replace('/', ',') + ')'

    if is_sys(crole_str_tup[0]):
        parent_role_sql = """SELECT id FROM role;"""

    else:
        parent_role_sql = """SELECT parent_id 
                            FROM role 
                            WHERE parent_id IN %s;""" % \
                          crole_tup_str

    role_sql = """SELECT name, parent_id FROM role WHERE id=%s""" % role_id

    role_tup = sql_oper.select(role_sql)
    parent_roles_tup = sql_oper.select(parent_role_sql)

    role_dict = dict()
    role_dict['id'] = role_id
    role_dict['name'] = role_tup[0][0]
    role_dict['parent'] = role_tup[0][1]
    role_dict['parent_id'] = parent_id

    parent_list = []
    for parent_role in parent_roles_tup:
        parent_role_dict = dict()
        parent_role_dict['id'] = parent_role[0]
        parent_role_dict['name'] = sql_oper.get_parent_role_name(parent_role[0])
        parent_list.append(parent_role_dict)

    return render_template('edit_auth.html', role=role_dict, parents=parent_list)
