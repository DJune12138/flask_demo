# _*_ coding:utf-8 _*_
# 定义公共的工具文件
from flask import g, request
from flask import redirect
from flask import session, jsonify
from werkzeug.routing import BaseConverter
from functools import wraps
import random
import traceback
from decimal import Decimal
from zs_backend.utils import time_util


def rand_list(L):
    if not L:
        return ""
    Len = len(L)
    return L[int(round(random.uniform(0, Len - 1)))]


def rand(Min, Max):
    return int(random.uniform(Min, Max))


# 自定义正则匹配转换器
class RegexConverter(BaseConverter):
    # 重写init方法
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]


def iframe_reload():
    return '''
<html>
<body onload="load()">
<script type="text/javascript">
function load() { 
    parent.location.reload(); 
}
</script>
</body>
</html>
    '''


def login_require(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/sessions')
        else:
            try:
                if not session.has_key('last_access_time'):
                    session['last_access_time'] = time_util.now_sec()
                Now = time_util.now_sec()

                # 一小时没有操作 则退出
                if Now - session['last_access_time'] >= 60 * 60:
                    session.clear()
                    return iframe_reload()

                if str(request.url_rule) not in ["/withdrawal/order/count", "/recharge/order/waiting/count"]:
                    session['last_access_time'] = time_util.now_sec()

                g.user_id = user_id
                return view_func(*args, **kwargs)
            except BaseException as e:
                print traceback.format_exc()
                return jsonify(error="system_err")

    return wrapper


def md5(Str):
    import hashlib
    return hashlib.md5(Str).hexdigest()


def get_highest_role_id(role_str):
    highest_role = 0
    for role_id in role_str.split('/'):
        if int(role_id) == 1:
            highest_role = 1
            break
        if highest_role == 0 or (highest_role < int(role_id)):
            highest_role = int(role_id)

    return highest_role


def rounding_off(num1, num2, n):
    """四舍五入保留n位小数"""

    d = Decimal(num1) / Decimal(num2)
    return round(d, n)
