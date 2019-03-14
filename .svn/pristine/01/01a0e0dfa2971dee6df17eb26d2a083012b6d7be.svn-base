# -*- coding:utf-8 -*-


from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.globals import current_app, session, request, g
from zs_backend.sql import SqlOperate
from zs_backend.utils.common import login_require
from . import busi


def is_sys(role_str):
    return '1' in role_str.split("/")


@busi.route('/menus', methods=['GET'])
@login_require
def get_menu():
    crole_str = session['role_str']
    sql_oper = SqlOperate()

    role_list = sql_oper.get_roles_list_by_role_str(crole_str)

    result = is_sys(crole_str)

    # 中菜单列表
    menus_list = sql_oper.get_menus_list_by_role_str(crole_str)

    return render_template('index_menu.html', menus_list=menus_list, roles=role_list, result=result)


@busi.route('/menus', methods=['POST'])
@login_require
def set_role_menu():
    json_dict = request.form
    role_id = json_dict.get('role_id')
    menu_id_list = [int(i) for i in json_dict.getlist('menus')]

    all_menu_sql = "SELECT id,role_str FROM menu"
    sql_oper = SqlOperate()
    try:
        all_menus_tup = sql_oper.select(all_menu_sql)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errmsg='数据库查询失败')

    sql = "UPDATE menu SET role_str='%s' WHERE id=%s;"
    for mid, role_str in all_menus_tup:
        role_list = role_str.split("/")
        if mid in menu_id_list:
            if role_id not in role_list:
                role_list.append(role_id)
                role_list.sort()
                new_role_str = "/".join(role_list)
                sql_oper.update(sql % (new_role_str, mid))
        else:
            if role_id in role_list:
                role_list.remove(role_id)
                role_list.sort()
                new_role_str = "/".join(role_list)
                sql_oper.update(sql % (new_role_str, mid))

    return redirect(url_for('busi.get_menu'))


@busi.route('/menus/set', methods=['POST'])
@login_require
def set_menu():
    json_dict = request.form
    menu_id = json_dict.get('menu_id')
    menu_name = json_dict.get('name')
    role_list = json_dict.getlist('role')

    role_str = '/'.join(role_list)
    menu_update_sql = """UPDATE menu SET name='%s',role_str='%s' WHERE id=%s;""" % (
        menu_name, role_str, menu_id)

    sql_oper = SqlOperate()
    try:
        sql_oper.update(menu_update_sql)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errmsg='数据库操作失败')

    return redirect(url_for('busi.get_menu'))


@busi.route('/menus', methods=['DELETE'])
@login_require
def delete_menu():
    menu_id = request.json.get('menu_id')
    del_menu_sql = """DELETE FROM menu WHERE id=%s""" % menu_id

    sql_oper = SqlOperate()
    try:
        sql_oper.delete(del_menu_sql)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno='2', errmsg='数据库操作失败')

    return jsonify(errno='0', errmsg='删除成功')


@busi.route('/menus/<re(".+"):operation>', methods=['GET'])
@login_require
def show_oper_menu(operation):
    if operation == 'add':
        crole_str = session['role_str']
        role_id = request.args.get('role_id')
        role_name = request.args.get('role_name')

        role_dict = dict()
        role_dict['id'] = role_id
        role_dict['name'] = role_name

        sql_oper = SqlOperate()
        # 中菜单列表
        menus_list = sql_oper.get_menus_list_by_role_str(crole_str)
        selected_menu = sql_oper.get_menus_list_by_role_str(role_id)

        selected_id_list = list()
        for menu_dict in selected_menu:
            for menu in menu_dict['menu_list']:
                selected_id_list.append(menu['id'])

        return render_template('add_menu.html', menus_list=menus_list, role=role_dict, selected_id=selected_id_list)

    elif operation == 'edit':
        crole_str = session['role_str']
        result = is_sys(crole_str)
        menu_id = request.args.get('menu_id')
        role_str = request.args.get('role_str')
        role_list = [int(i) for i in role_str.split('/')]

        menu_select_sql = """SELECT name,view_name FROM menu WHERE id=%s;""" % menu_id

        sql_oper = SqlOperate()
        # 查询出菜单名元组
        menu_tup = sql_oper.select(menu_select_sql)

        roles_list = sql_oper.get_roles_list_by_role_str(crole_str)

        menu_dict = dict()
        menu_dict['id'] = menu_id
        menu_dict['name'] = menu_tup[0][0]
        menu_dict['view_name'] = menu_tup[0][1]
        if result == -1:
            menu_dict['name_is_edit'] = False
        else:
            menu_dict['name_is_edit'] = True

        return render_template('edit_menu.html', menu=menu_dict,
                               roles=roles_list, select_roles=role_list)


@busi.route('/menus/manage/show', methods=['GET'])
@login_require
def menus_manage_show():
    """部门权限管理页面"""

    return render_template('jurisdiction_manage.html')


@busi.route('/menus/jurisdiction/group/', methods=['GET'])
@login_require
def menus_jurisdiction_group():
    """获取部门权限组"""

    # 获取数据
    crole_str = session['role_str']
    role_list = SqlOperate().get_roles_list_by_role_str(crole_str)
    result = is_sys(crole_str)

    # 处理数据
    data_list = list()
    for role in role_list:
        data_dict = dict()
        if role['parent_id'] != 1 or (result != -1 and role['id'] != 1):
            data_dict['id'] = role['id']
            data_dict['name'] = role['name']
            data_list.append(data_dict)

    # 返回数据
    return jsonify(result=1, data=data_list)


@busi.route('/menus/list/get', methods=['GET'])
@login_require
def menus_list_get():
    """获取菜单列表和选中菜单"""

    # 获取参数
    role_id = request.args.get('role_id')
    crole_str = session['role_str']

    # 获取菜单列表和选中菜单
    menus_list = SqlOperate().get_menus_list_by_role_str(crole_str)
    selected_menu = SqlOperate().get_menus_list_by_role_str(role_id)

    # 处理选中菜单数据
    select_list = list()
    for menu_dict in selected_menu:
        for menu in menu_dict['menu_list']:
            select_list.append(menu['id'])

    # 合并菜单列表和选中菜单
    for menu_dict in menus_list:
        for menu in menu_dict['menu_list']:
            if menu['id'] in select_list:
                menu['select'] = 1
            else:
                menu['select'] = 0

    # 返回数据
    return jsonify(result=1, data=menus_list)


@busi.route('/menus/list/update', methods=['POST'])
@login_require
def menus_list_update():
    """修改菜单列表"""

    # 获取参数
    menu_list = request.form.get('menu_list')
    role_id = request.form.get('role_id')

    # 从数据库获取数据
    retrieve_sql = """SELECT id,role_str
                      FROM menu;"""
    all_menus_tup = SqlOperate().select(retrieve_sql)

    # 更新数据
    update_sql = """UPDATE menu
                    SET role_str='{}'
                    WHERE id={};"""
    for mid, role_str in all_menus_tup:
        role_list = role_str.split("/")
        if mid in eval(menu_list):
            if role_id not in role_list:
                role_list.append(role_id)
                role_list.sort()
                new_role_str = "/".join(role_list)
                SqlOperate().update(update_sql.format(new_role_str, mid))
        else:
            if role_id in role_list:
                role_list.remove(role_id)
                role_list.sort()
                new_role_str = "/".join(role_list)
                SqlOperate().update(update_sql.format(new_role_str, mid))

    # 返回应答
    return jsonify(result=1, msg=u'修改成功！')
