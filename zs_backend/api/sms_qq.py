# -*- coding:utf-8 -*-
import hashlib
from zs_backend.utils.common import rand
from zs_backend.utils import time_util, httpc_util
from zs_backend import redis_conn
from zs_backend.utils.const import *

URL = "https://yun.tim.qq.com/v5/tlssmssvr/sendsms" 

def calculate_signature(appkey, rand, time, phone_numbers=None):
    """Calculate a request signature according to parameters.

    :param appkey: sdk appkey
    :param random: random string
    :param time: unix timestamp time
    :param phone_numbers: phone number array
    """
    raw_text = "appkey={}&random={}&time={}".format(appkey, rand, time)
    if phone_numbers:
        raw_text += "&mobile={}".format(
            ",".join(map(str, phone_numbers)))
    return hashlib.sha256(raw_text.encode("utf8")).hexdigest()

def send_sms(channel, phone_number, params, time, nationcode = 86):
    ## 获取短息你配置
    conf = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "sms_config")
    [appid, appkey, tpl_id] = conf.split(",")

    now = time
    rand_v = rand(100000, 999999)
    url = "{}?sdkappid={}&random={}".format(URL, appid, rand_v)
    paylaod = {
        "tel": {
            "nationcode": str(nationcode),
            "mobile": str(phone_number)
        },
        "tpl_id": tpl_id,
        "sig": calculate_signature(appkey, rand_v, now, [phone_number]),
        "time": now,
        "params": params,
    }

    try:
        r = None
        r = httpc_util.post(url, paylaod, ctype ="json")
        if r["result"] == 0:
            return True
    except:
        pass

    print "sms_err", r, channel, paylaod
    return False
