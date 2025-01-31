# -*- coding:utf-8 -*-

from zs_backend.utils import erl
from zs_backend.utils.channel_qry import *
from zs_backend import SqlOperate
from zs_backend import redis_conn
from zs_backend.utils.const import *
import json

def get_bank_coin(Counter):
    Counter = erl.binary_to_term(Counter)
    for k, v in Counter:
        if k == 14001:
            for kk, vv in v:
                if kk == "deposit":
                    return vv
    return 0

def get_bank_info(Counter):
    acc = ""
    name = ""
    bank = ""
    addr = ""
    Counter = erl.binary_to_term(Counter)
    for k, v in Counter:
        if k == 11010:
            for kk, vv in v:
                if kk == "bank_reg_name":
                    name = vv
                elif kk == "bank_acc":
                    acc = vv
                elif kk == 'bank_name':
                    bank = vv
                elif kk == "bank_detail":
                    addr = vv
    return bank, acc, name, addr

def set_bank_info(channel, pid, acc, name, bank, addr):
    payload = {
        "pid":pid,
        "bank_reg_name":name,
        "bank_acc":acc,
        "bank_name":bank,
        "bank_detail":addr
    }
    if GameWeb(channel).post("/api/update_bound_cash_info", payload)["result"] == "succ":
        return True

    return False

def get_zfb_info(Counter):
    acc = ""
    name = ""
    Counter = erl.binary_to_term(Counter)
    for k, v in Counter:
        if k == 11010:
            for kk, vv in v:
                if kk == "zfb_reg_name":
                    name = vv
                elif kk == "zfb_acc":
                    acc = vv
    return acc, name

def set_zfb_info(channel, pid, acc, name):
    payload = {
        "pid":pid,
        "zfb_reg_name":name,
        "zfb_acc":acc,
    }
    if GameWeb(channel).post("/api/update_bound_cash_info", payload)["result"] == "succ":
        return True

    return False

def coin_translate(channel, coin):
    ## 查询该渠道配置
    try:
        rate = int(redis_conn.hget(CHANNEL_CONFIG_TABLE+str(channel), "coin_rate"))
    except:
        rate = 1

    if rate != 1:
        ## 保留两位小数
        return int(int(coin) * 100 / rate) / 100.0

    return coin

