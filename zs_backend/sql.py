# -*- coding:utf-8 -*-
import json

from flask import current_app, jsonify
from pymysql import *
from config import Config


class SqlOperate(object):
    def __init__(self):
        self.host = Config.DB_HOST
        self.port = Config.DB_PORT
        self.user = Config.DB_USER
        self.password = Config.DB_PASSWORD
        self.database = Config.DB_DATABASE

    def insert(self, insert_sql):
        # 创建Connection连接
        conn = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database,
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        count = cs1.execute(insert_sql)
        # 打印受影响的行数
        print("插入%d条数据:" % count)
        conn.commit()
        # 关闭Cursor对象
        cs1.close()
        conn.close()

    def delete(self, delete_sql):
        # 创建Connection连接
        conn = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database,
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        count = cs1.execute(delete_sql)
        # 打印受影响的行数
        print("删除%d条数据:" % count)
        conn.commit()
        # 关闭Cursor对象
        cs1.close()
        conn.close()

    def update(self, update_sql):
        # 创建Connection连接
        conn = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database,
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        count = cs1.execute(update_sql)
        # 打印受影响的行数
        print("更新%d条数据:" % count)
        conn.commit()
        # 关闭Cursor对象
        cs1.close()
        conn.close()

    def select(self, select_sql):
        # 创建Connection连接
        conn = connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database,
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()
        count = cs1.execute(select_sql)
        result = cs1.fetchall()
        # 关闭Cursor对象
        cs1.close()
        conn.close()
        return result

    def get_role_text(self, role_str):
        role_text_sql = "SELECT name FROM role WHERE id IN (%s);" % ",".join(role_str.split('/'))
        role_tuple = self.select(role_text_sql)

        role_name_list = []
        for role_name in role_tuple:
            role_name_list.append(role_name[0])
        role_name_str = '/'.join(role_name_list)

        return role_name_str

    def generate_channels_by_role(self, role_str):
        role_list = role_str.split('/')
        # 模糊查询渠道信息
        channel_sql = '''
            SELECT id, role_str
            FROM channel 
            WHERE is_delete=0 
        '''

        try:
            # 获取用户权限对应的渠道元组
            chan_tup = self.select(channel_sql)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errmsg='数据库查询失败')

        # 创建渠道字典
        chan_list = []
        for channel_id, role_str in chan_tup:
            tmp_role_list = role_str.split('/')
            if not [i for i in role_list if i in tmp_role_list]:
                continue
            chan_list.append(channel_id)
        return chan_list
    
    def get_parent_role_name(self, parent_id):
        channel_text_sql = """SELECT name FROM role WHERE id=%s;""" % parent_id
        role_name_tuple = self.select(channel_text_sql)
        role_name = role_name_tuple[0][0]
        return role_name

    def get_roles_list_by_role_str(self, role_str):
        crole_tup_str = '(' + role_str.replace('/', ',') + ')'
        if '1' in role_str.split("/"):
            roles_sql = """SELECT id, name, parent_id FROM role;"""
        else:
            roles_sql = """SELECT id, name, parent_id 
                        FROM role 
                        WHERE id!=1
                        AND (id IN %s OR parent_id IN %s);""" % (crole_tup_str, crole_tup_str)

        roles_tup = self.select(roles_sql)

        role_list = []
        for role in roles_tup:
            role_dict = dict()
            role_dict['id'] = role[0]
            role_dict['name'] = role[1]
            role_dict['parent_id'] = role[2]
            role_dict['parent'] = self.get_parent_role_name(role[2])
            role_list.append(role_dict)

        return role_list

    def get_menus_list_by_role_str(self, crole_str):
        crole_list = crole_str.split('/')
        admin = '1' in crole_list
        role_text = self.get_role_text(crole_str)

        menus_sql = """
            SELECT menu_group,group_concat(id ORDER BY weight, id),group_concat(name ORDER BY weight, id),
                    group_concat(view_name ORDER BY weight, id),group_concat(role_str ORDER BY weight, id) 
            FROM menu 
            GROUP BY menu_group
            ORDER BY weight;
        """

        menus_tup = self.select(menus_sql)

        # 中菜单列表
        menus_list = list()
        menus_dict = dict()
        menu_list = list()
        for menu_tup in menus_tup:
            # 子菜单列表
            menu_group = menu_tup[0]
            menu_id_list = menu_tup[1].split(',')
            menu_name_list = menu_tup[2].split(',')
            menu_view_list = menu_tup[3].split(',')
            menu_role_list = menu_tup[4].split(',')

            for index in range(len(menu_name_list)):
                menu_dict = dict()
                for crole in crole_list:
                    # 如果当前用户所属权限组中具有此菜单操作权限，result不为-1
                    result = crole in menu_role_list[index].split("/")
                    if result:
                        menu_dict['id'] = menu_id_list[index]
                        menu_dict['name'] = menu_name_list[index]
                        menu_dict['view_name'] = menu_view_list[index]
                        menu_dict['role_str'] = menu_role_list[index]
                        menu_dict['role_text'] = role_text if admin else self.get_role_text(menu_role_list[index])
                        menu_list.append(menu_dict)
                        break
                    else:
                        continue
                if (index == len(menu_name_list) - 1) and (len(menu_list) >= 1):
                    menus_dict['group'] = menu_group
                    menus_dict['menu_list'] = menu_list
                    menus_list.append(menus_dict)
                    menus_dict = dict()
                    menu_list = list()

        return menus_list

# 测试
if __name__ == '__main__':
    sql_oper = SqlOperate()
    sql_oper.get_role_text('1,2')
