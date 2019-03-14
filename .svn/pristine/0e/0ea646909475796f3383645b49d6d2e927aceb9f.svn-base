# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from werkzeug.security import generate_password_hash
import fcntl
from zs_backend import scheduler

def init(admin_type):
    try:
        f = file("admin.lock", "w")
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        init1(admin_type)
        cron(admin_type)
    except:
        pass

def init1(admin_type):
    if admin_type == "API":
        return
    from zs_backend.busi.channel import load_channel
    from zs_backend.busi.game_parameter import load_game_paramter
    print "system init"
    ## 初始化系统账号
    user_count = SqlOperate().select('select count(1) from user')[0][0]
    if user_count == 0:
        sql = '''
            insert into user (name, nick, password, role_str) values ('admin', 'admin', '%s', '1')
        ''' % generate_password_hash('123456')
        SqlOperate().insert(sql)

    role_count = SqlOperate().select('select count(1) from role')[0][0]
    if role_count == 0:
        sql = '''
            insert into role (id, name, parent_id) values (1, '管理员组', 1)
        '''
        SqlOperate().insert(sql)

    ## 加载渠道配置到redis
    try:
        load_channel()
    except BaseException as e:
        print "load_channel:", e
    ## 加载游戏参数
    load_game_paramter()

def cron(admin_type):
    if admin_type == "API":
        from zs_backend.api import API_JOBS
        for item in API_JOBS:
            try:
                scheduler.add_job(func=item["func"], id=item["id"], args=item["args"], trigger=item["trigger"], 
                    seconds=item["seconds"], replace_existing=True)
            except Exception as e:
                print "add scheduler............", e
