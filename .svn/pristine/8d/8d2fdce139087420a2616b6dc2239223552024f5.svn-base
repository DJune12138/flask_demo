# _*_ coding:utf-8 _*_

from flask import Flask
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
import redis
from zs_backend.utils.common import RegexConverter, rounding_off
from zs_backend.utils.time_util import formatDateTime, formatDate
from zs_backend.utils.search_bar import search_bar
from zs_backend.utils.erl import binary_to_term
from config import Config
import logging
from logging.handlers import RotatingFileHandler
from sql import SqlOperate
from zs_backend.utils.html_translate import pt
from flask_apscheduler import APScheduler

# 生成redis数据库操作对象
redis_pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, 
    db=Config.REDIS_DATABASE, password=Config.REDIS_PASSWD)
redis_conn = redis.Redis(connection_pool = redis_pool)

app = Flask(__name__)
scheduler = APScheduler()

def setUpLogging(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/admin.log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def get_app(config_name):
    # 调用setUpLogging设置logging配置
    setUpLogging(config_name.LOGGING_LEVEL)
    # 将配置项配置到app中
    app.config.from_object(config_name)
    
    scheduler.init_app(app=app)
    scheduler.start()
    # 开启CSRF保护
    # CSRFProtect(app)
    # 将session数据保存到redis数据库中
    Session(app)

    # 注册自定义管理器
    app.url_map.converters['re'] = RegexConverter

    if Config.SERVER_TYPE == "ADMIN":
        from zs_backend.busi import busi
        # 注册busi中的蓝图
        app.register_blueprint(busi)
    elif Config.SERVER_TYPE == "API":
        # 注册api中的蓝图
        from zs_backend.api import api
        app.register_blueprint(api)
    elif Config.SERVER_TYPE == "ALL":
        from zs_backend.busi import busi
        # 注册busi中的蓝图
        app.register_blueprint(busi)

        # 注册api中的蓝图
        from zs_backend.api import api
        app.register_blueprint(api)

    ## 跨域处理
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

    ## 添加全局函数
    app.add_template_global(search_bar, 'search_bar')
    app.add_template_global(binary_to_term, 'parse_erl')
    app.add_template_global(formatDateTime, 'formatDateTime')
    app.add_template_global(formatDate, 'formatDate')
    app.add_template_global(pt, 'pt')
    app.add_template_global(rounding_off, 'rounding_off')

    return app
