# _*_ coding:utf-8 _*_

from zs_backend import get_app
from zs_backend import system_init
from config import configs

config_name = configs.get('develop')

# 生成app对象
app = get_app(config_name)
system_init.init(config_name.SERVER_TYPE)

# @app.before_first_request
# def init():
#     pass

if __name__ == '__main__':
    # print app.url_map
    app.run(host=config_name.HOST, port=config_name.PORT)
