# _*_ coding:utf-8 _*_
import logging
import redis


class Config(object):
    # 服务类型  ALL全部功能  API只有api功能
    SERVER_TYPE = "ADMIN" 
    ## API网关地址
    API_WEB_SITE = "https://apith.jl45f.cn"
    ADMIN_WEB_SITE = "https://win.jl45f.cn"
    # 配置参数
    HOST = '192.168.0.116'
    PORT = 8899
    # 配置mysql连接信息
    DB_HOST = '192.168.0.126'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASSWORD = '123456'
    DB_DATABASE = 'zs_backend_develop'
    # 配置秘钥
    SECRET_KEY = 'Rl9jNLq+W/3+f7YAgC4a3d7t317LLVeUZW7xVOJhb/E1NTrBR4T8K3xxceJCrM7a'
    # 配置redis连接信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWD= ""
    REDIS_DATABASE = 5
    # 配置session保存保存方式
    SESSION_TYPE = 'redis'
    # # 配置session连接redis数据库地址
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE, password=REDIS_PASSWD)
    # 是否使用secret_key签名session_data
    SESSION_USE_SIGNER = True
    # 配置session过期时间
    PERMANENT_SESSION_LIFETIME = 3600 * 24


class Development(Config):
    LOGGING_LEVEL = logging.DEBUG
    DEBUG = True


class Prodution(Config):
    # 产品上线关闭DEBUG模式
    DEBUG = False
    # 配置session过期时间
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 6
    LOGGING_LEVEL = logging.WARNING


configs = {
    'develop': Development,
    'production': Prodution,
}
