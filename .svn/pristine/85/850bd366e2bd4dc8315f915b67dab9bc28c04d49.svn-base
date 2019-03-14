# -*- coding:utf-8 -*-
import json
from flask import render_template, session, request, jsonify
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require

## 获取抽水返利比例
def get_pump_rate(pump_config, pump):
    pump = int(pump)
    for l in pump_config:
        if l[4] >= pump and l[3] <= pump:
            return float(l[5]) / 10000
    else:
        return float(l[5]) / 10000

## 计算输赢返利比例
def get_win_rate(win_config, win):
    win = int(win)
    for l in win_config:
        if l[1] >= win and l[0] <= win:
            return float(l[2]) / 10000
    else:
        return float(l[2]) / 10000

## 计算返佣
def calc_commission(d, pump_config, commission_config):
    ## 计算各级下线给该玩家带来的返利
    pump_commission = {}
    for k, v in d["pump"].items():
        k = int(k)
        pump_commission[k] = int(v * get_pump_rate(pump_config, v) * int(commission_config[k]) / 10000)

    win_commission = {}
    for k, v in d["win"].items():
        k = int(k)
        win_commission[k] = int(v * get_win_rate(pump_config, v) * int(commission_config[k]) / 10000)

    d["win_commission"] = win_commission
    d["pump_commission"] = pump_commission

    return d
