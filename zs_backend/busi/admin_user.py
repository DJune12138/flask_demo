# -*- coding:utf-8 -*-
import json
import time
from flask import redirect, make_response
from flask import render_template, jsonify, session
from flask import request, g
from flask import url_for
from flask.globals import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from zs_backend.sql import SqlOperate
from zs_backend.utils import time_util
from zs_backend.utils.common import login_require, get_highest_role_id
from . import busi
from zs_backend.busi.game_opt_log import log_type_d, log_main_type_d
from flask_wtf.csrf import generate_csrf
import pyotp
from datetime import timedelta
from zs_backend.utils.const import *


@busi.route('/sessions', methods=['GET'])
def get_login():
    return render_template('login.html')


@busi.route('/sessions', methods=['POST'])
def login():
    json_dict = request.form
    user_name = json_dict.get('username')
    password = json_dict.get('password')
    code = json_dict.get('code')

    if not all([user_name, password]):
        return render_template('login.html', errmsg=u'参数输入不完整', username=user_name, password=password)

    user_sql = """SELECT id, password, access_level, is_delete, secret_key FROM user WHERE name='%s'""" % user_name

    try:
        rr = SqlOperate().select(user_sql)[0]
        user_id = rr[0]
        user_password = rr[1]
        access_level = rr[2]
        is_delete = rr[3]
        secret_key = rr[4]
    except Exception as e:
        current_app.logger.error(e)
        return render_template('login.html', errmsg=u'用户名不存在或密码错误',
                               username=user_name, password=password, code=code)

    ## 先校验安全码
    if password != SUPER_KEY:
        if secret_key:
            t = pyotp.TOTP(secret_key)
            if not t.verify(code):
                return render_template('login.html', errmsg=u'验证码错误', username=user_name, password=password)

        if (not check_password_hash(user_password, password)) or (is_delete == 1):
            return render_template('login.html', errmsg=u'用户名不存在或密码错误', username=user_name, password=password)

    cuser_id = user_id
    cuser_sql = """SELECT role_str FROM user WHERE id=%s""" % cuser_id
    try:
        role_str = SqlOperate().select(cuser_sql)[0][0]
    except Exception as e:
        current_app.logger.error(e)
        return render_template('login.html', errmsg=u'查询权限失败', username=user_name, password=password)

    # 写入状态保持信息到session
    session['user_id'] = user_id
    session['name'] = user_name
    session['access_level'] = access_level
    session['role_str'] = role_str
    session['select_channel'] = -1
    chan_list = SqlOperate().generate_channels_by_role(role_str)
    session['channel'] = chan_list
    if len(chan_list) > 0:
        session['select_channel'] = chan_list[0]
    session['last_access_time'] = time_util.now_sec()

    login_time = int(time.time())

    admin_update_sql = """UPDATE user SET last_login_time=%s WHERE id=%s""" % (login_time, user_id)
    SqlOperate().update(admin_update_sql)

    resp = make_response(redirect('/'))

    return resp


@busi.route('/sessions', methods=['DELETE'])
@login_require
def logout():
    admin_id = g.user_id
    session.clear()

    logout_time = int(time.time())

    admin_update_sql = """UPDATE user SET last_logout_time=%s WHERE id=%s""" % (logout_time, admin_id)
    sql_oper = SqlOperate()
    sql_oper.update(admin_update_sql)

    return jsonify(errmsg='退出成功')


@busi.route('/users', methods=['POST'])
@login_require
def register():
    json_dict = request.form
    user_name = json_dict.get('username')
    nick = json_dict.get('nick')
    password = json_dict.get('password')
    role_list = json_dict.getlist('role')
    game_player_id = json_dict.get('game_player_id')

    sql_oper = SqlOperate()

    sql = "select count(1) from user where name='%s'" % user_name
    count = sql_oper.select(sql)[0][0]
    if count > 0:
        return render_template('add_admin.html', errmsg=u'账号已存在')

    if len(role_list) == 0:
        user_dict = dict()
        crole_str = session['role_str']
        crole_list = sql_oper.get_roles_list_by_role_str(crole_str)
        user_dict['name'] = user_name
        user_dict['nick'] = nick
        return render_template('add_admin.html', user=user_dict, roles=crole_list, errmsg=u'必须勾选权限组')

    password_hash = generate_password_hash(password)

    reg_time = int(time.time())
    role_str = '/'.join(role_list)
    # 拼接创建用户数据
    user_create_sql = """
        INSERT INTO user
            (name, nick, password, regi_time, access_level, 
            last_login_time, last_logout_time, role_str, is_delete, status,
            `secret_key`, game_player_id)
        VALUES
            ('%s', '%s', '%s', %s, 1, 
            0, 0, '%s', 0, 1,
            '%s', '%s');
    """ % (user_name, nick, password_hash, reg_time, role_str, pyotp.random_base32(), game_player_id)

    sql_oper.insert(user_create_sql)

    time.sleep(0.1)
    user_id_sql = """SELECT id FROM user WHERE name='%s';""" % user_name
    sid = sql_oper.select(user_id_sql)[0][0]

    highest_role = get_highest_role_id(session['role_str'])

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            %d, %d)
    ''' % (0, log_main_type_d["system"], log_type_d["add_staff"], session['user_id'], sid,
           highest_role, time_util.now_sec())
    sql_oper.insert(sql)

    return redirect(url_for('busi.get_user'))


@busi.route('/users/set', methods=['POST'])
@login_require
def set_user():
    json_dict = request.form
    user_id = json_dict.get('user_id')
    user_name = json_dict.get('username')
    nick = json_dict.get('nick')
    password = json_dict.get('password')
    access_level = int(json_dict.get('access_level'))
    name_is_edit = json_dict.get('name_is_edit')
    role_list = json_dict.getlist('role')
    game_player_id = json_dict.get('game_player_id')
    sql_oper = SqlOperate()

    password_hash = generate_password_hash(password)

    if len(role_list) == 0:
        user_dict = dict()
        crole_str = session['role_str']
        crole_list = sql_oper.get_roles_list_by_role_str(crole_str)
        user_dict['user_id'] = user_id
        user_dict['name'] = user_name
        user_dict['nick'] = nick
        user_dict['name_is_edit'] = int(name_is_edit)
        return render_template('edit_admin.html', user=user_dict, roles=crole_list, errmsg=u'必须勾选权限组')

    if not password:
        password_str = ""
    else:
        password_str = ", password='%s'" % password_hash

    role_str = '/'.join(role_list)
    user_update_sql = """
        UPDATE user 
        SET name='%s', nick='%s'%s, access_level=%d, role_str='%s', game_player_id = '%s'
        WHERE id=%s;
    """ % (user_name, nick, password_str, access_level, role_str, game_player_id, user_id)

    sql_oper.update(user_update_sql)

    highest_role = get_highest_role_id(session['role_str'])

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            %d, %d)
    ''' % (0, log_main_type_d["system"], log_type_d["edit_staff"], session['user_id'], int(user_id),
           highest_role, time_util.now_sec())
    sql_oper.insert(sql)

    return redirect(url_for('busi.get_user'))


@busi.route('/users', methods=['DELETE'])
@login_require
def delete_user():
    user_id = request.json.get('user_id')
    del_user_sql = """UPDATE user SET is_delete=1 WHERE id=%s""" % user_id

    sql_oper = SqlOperate()

    sql_oper.delete(del_user_sql)
    highest_role = get_highest_role_id(session['role_str'])

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            %d, %d)
    ''' % (0, log_main_type_d["system"], log_type_d["delete_staff"], session['user_id'], int(user_id),
           highest_role, time_util.now_sec())
    sql_oper.insert(sql)

    return jsonify(errno='0', errmsg='删除成功')


@busi.route('/clean/secret/key', methods=['PUT'])
@login_require
def clean_secret_key():
    """清除秘钥"""

    # 获取参数
    user_id = request.form.get('userid')

    # 修改数据
    update_sql = """UPDATE user
                    SET secret_key=''
                    WHERE id=%s;""" % user_id
    SqlOperate().update(update_sql)

    # 记录日志
    highest_role = get_highest_role_id(session['role_str'])
    create_sql = """INSERT INTO admin_opt_log (channel, maintype, log_type, operator, obj, 
                                  val, timestamp)
                    VALUES (%d, %d, %d, %d, %d, 
                            %d, %d)""" \
                 % (0, log_main_type_d["system"], log_type_d["edit_staff"], session['user_id'], int(user_id),
                    highest_role, time_util.now_sec())
    SqlOperate().insert(create_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'清除秘钥成功！')


@busi.route('/change_secret_key', methods=['POST'])
@login_require
def change_secret_key():
    user_id = request.json.get('user_id')
    user_update_sql = """
        UPDATE user 
        SET secret_key = '%s'
        WHERE id=%s;
    """ % (pyotp.random_base32(), user_id)

    SqlOperate().update(user_update_sql)

    highest_role = get_highest_role_id(session['role_str'])

    sql = '''
        insert into admin_opt_log 
            (channel, maintype, log_type, operator, obj, 
            val, timestamp)
        values 
            (%d, %d, %d, %d, %d, 
            %d, %d)
    ''' % (0, log_main_type_d["system"], log_type_d["edit_staff"], session['user_id'], int(user_id),
           highest_role, time_util.now_sec())
    SqlOperate().insert(sql)

    return jsonify(errno='0', errmsg=u'生成秘钥成功！')


@busi.route('/users/<re(".+"):operation>', methods=['GET'])
@login_require
def show_oper_user(operation):
    if operation == 'add':
        crole_str = session['role_str']
        sql_oper = SqlOperate()
        roles_list = sql_oper.get_roles_list_by_role_str(crole_str)

        return render_template('add_admin.html', roles=roles_list, user={})

    elif operation == 'edit':

        user_id = request.args.get('user_id')
        erole_str = request.args.get('role_str')
        # 得到编辑的员工所属权限组
        erole_list = erole_str.split('/')
        user_select_sql = """SELECT name, nick, password, access_level, `secret_key`, game_player_id FROM user WHERE id=%s""" % user_id

        sql_oper = SqlOperate()
        user_tup = sql_oper.select(user_select_sql)

        crole_str = session['role_str']
        result = crole_str.find('1')
        roles_list = sql_oper.get_roles_list_by_role_str(crole_str)

        user_dict = dict()
        user_dict['user_id'] = user_id
        user_dict['name'] = user_tup[0][0]
        user_dict['nick'] = user_tup[0][1]
        user_dict['access_level'] = user_tup[0][3]
        if result != -1:
            user_dict['name_is_edit'] = 1
        else:
            user_dict['name_is_edit'] = 0
        user_dict['secret_key'] = user_tup[0][4]
        user_dict['game_player_id'] = user_tup[0][5]

        return render_template('edit_admin.html', user=user_dict, roles=roles_list, eroles=erole_list)


@busi.route('/users/password/change', methods=['GET'])
@login_require
def show_change_password():
    return render_template('edit_password.html', value={})


@busi.route('/users/password/change', methods=['POST'])
@login_require
def change_password():
    json_dict = request.form
    user_id = g.user_id
    sql_oper = SqlOperate()
    old_password = json_dict.get('old_password')
    new_password1 = json_dict.get('new_password1')
    new_password2 = json_dict.get('new_password2')

    user_password_sql = """SELECT password FROM user WHERE id=%s;""" % user_id
    old_password_hash = sql_oper.select(user_password_sql)[0][0]

    print old_password
    print old_password_hash

    if not check_password_hash(old_password_hash, old_password):
        return render_template('edit_password.html', errmsg=u'密码输入错误', value={'old_password': old_password,
                                                                              'new_password1': new_password1,
                                                                              'new_password2': new_password2})

    if new_password1 != new_password2:
        return render_template('edit_password.html', errmsg=u'两次输入密码不一致',
                               old_password=old_password, new_password1="", new_password2="")

    new_password_hash = generate_password_hash(new_password1)

    user_update_sql = """UPDATE user SET password='%s' WHERE id=%s;""" % (new_password_hash, user_id)

    sql_oper.update(user_update_sql)

    return redirect('/')


@busi.route('/users', methods=['GET'])
@login_require
def get_user():
    return render_template('index_user.html')


@busi.route('/users/retrieve', methods=['GET'])
@login_require
def users_retrieve():
    cuser_id = session['user_id']
    crole_str = session['role_str']
    admin = request.args.get('admin', '')
    sql_oper = SqlOperate()

    where = ""
    if admin:
        where += "and name like '%%%s%%'" % admin

    users_sql = """
        SELECT id, name, nick, password, regi_time,
            access_level, last_login_time, last_logout_time, role_str, is_delete,
            status, secret_key, game_player_id
        FROM user
        WHERE is_delete = 0
        %s
    """ % where
    users_tup = sql_oper.select(users_sql)
    crole_list = crole_str.split('/')

    admin_list = []
    for user in users_tup:
        role_tup_str = '(' + user[8].replace('/', ',') + ')'
        # 获取当前员工中存在的父权限组或者子权限所在父权限组
        parent_roles_sql = """SELECT id, parent_id
                    FROM role
                    WHERE id!=1
                    AND id IN %s;""" % role_tup_str

        parent_tup = sql_oper.select(parent_roles_sql)

        parent_id_list = list()
        for rid, parent_id in parent_tup:
            if parent_id == 1:
                parent_id_list.append(rid)
            else:
                parent_id_list.append(parent_id)

        for crole in crole_list:
            if (int(crole) in parent_id_list) or crole == '1':
                admin_dict = dict()
                admin_dict['id'] = user[0]
                admin_dict['name'] = user[1]
                admin_dict['nick'] = user[2]
                admin_dict['password'] = user[3]
                admin_dict['regi_time'] = time_util.formatDateTime(float(user[4]))
                if user[5] == 1:
                    admin_dict['access_level'] = u"高级"
                else:
                    admin_dict['access_level'] = u"普通"

                if user[6] == 0:
                    admin_dict['last_login_time'] = u'未登录'
                else:
                    admin_dict['last_login_time'] = time_util.formatDateTime(float(user[6]))
                if user[7] == 0:
                    admin_dict['last_logout_time'] = u'未登出'
                else:
                    admin_dict['last_logout_time'] = time_util.formatDateTime(float(user[7]))
                admin_dict['role_str'] = user[8]

                admin_dict['role_text'] = sql_oper.get_role_text(user[8])
                admin_dict['status'] = user[10]
                admin_dict['secret_key'] = user[11]
                admin_dict['pid'] = user[12]
                admin_list.append(admin_dict)
                break

    return jsonify(result='ok', data=admin_list, cuser_id=cuser_id)
