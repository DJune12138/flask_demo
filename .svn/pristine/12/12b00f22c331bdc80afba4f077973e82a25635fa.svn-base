# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, jsonify, request
from zs_backend import redis_conn
from zs_backend.utils.const import *
from zs_backend.utils import erl

# 游戏参数设置类型映射
TAG_COIN_LOG = 1  # 金币日志定义
TAG_SUBGAME = 2  ## 子游戏定义
TAG_LOG_DETAIL = 3  ## 游戏对局日志定义
TAG_SUBGAME_DETAIL = 4  # 小游戏详情参数定义
TAG_ROOM_DEFINE = 5 ## 房间类型定义

def load_game_paramter():
    sql = 'SELECT type, config FROM game_parameter'
    for stype, config in SqlOperate().select(sql):
        redis_conn.hset(GAME_PARAMTER_TABLE, stype, config)

@busi.route('/game/parameter/show', methods=['GET'])
@login_require
def game_parameter_show():
    """游戏参数页面"""
    return render_template('game_parameter.html')


@busi.route('/game/parameter/retrieve', methods=['GET'])
@login_require
def game_parameter_retrieve():
    """游戏参数查询"""

    # 获取参数
    type_id = request.args.get('type', str(TAG_COIN_LOG))

    # 获取数据
    retrieve_sql = """SELECT config FROM game_parameter WHERE type=%s;""" % type_id
    data = SqlOperate().select(retrieve_sql)

    # 处理数据
    try:
        config = eval(data[0][0])
    except IndexError:
        config = []
    # 返回数据
    return jsonify(result='ok', data=config)


@busi.route('/game/parameter/update', methods=['POST'])
@login_require
def game_parameter_update():
    """游戏参数新建"""

    # 获取参数
    type_id = request.form.get('type')
    config = request.form.get('config')

    # 校验参数
    try:
        eval(config)
        redis_conn.hset(GAME_PARAMTER_TABLE, type_id, config)
    except ValueError:
        return jsonify(result='fail', msg=u'内容不合法')

    # 存进数据库
    update_sql = """replace into game_parameter (type, config) values (%s, '%s')""" % (type_id, config)
    SqlOperate().update(update_sql)

    # 返回应答
    return jsonify(result='ok', msg=u'新建成功！')


## 金币类型定义
def get_coin_log_define():
    datas = {}
    for d in eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_COIN_LOG)):
        datas[int(d["id"])] = unicode(d["name"], 'utf-8')
    return datas

## 获得对应金币日志类型名字
def get_coin_log_name(d, idx):
    try:
        return d[idx]
    except:
        return idx

## 小游戏参数定义
def detail_config():
    datas = {}
    for d in eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_SUBGAME_DETAIL)):
        gameid = int(d["gameid"])
        if not datas.has_key(gameid):
            datas[gameid] = {}
        datas[gameid][int(d["id"])] = unicode(d["detail"], 'utf-8')
    return datas

## 对局日志定义
def detail_define():
    datas = {}
    for line in eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_LOG_DETAIL)):
        seq = line["id"]
        memo = line["detail"]
        if memo[0] == "#":
            memo = memo.split("#")
            if memo[1] in ["coin", "pid", "config"]:
                datas[int(seq)] = {"type":memo[1], "txt":memo[2]}
            elif memo[1] == "desc":
                kv = {}
                for ele in memo[3].split(","):
                    k,v = ele.split(":")
                    kv[int(k)] = v 
                datas[int(seq)] = {"type":memo[1], "txt":memo[2], "kv":kv} 
        else:
            datas[int(seq)] = {"type":"normal", "txt":"".join(memo)} 

    return datas

## 小游戏定义
def get_subgame_list():
    subgame_list = eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_SUBGAME))
    subgamelist = dict([(int(ele["id"]), unicode(ele["desc"], 'utf-8')) for ele in subgame_list])

    return subgamelist

def get_subgame_by_id(d, idx):
    try:
        return d[idx]
    except:
        return idx

def get_subgame_enname(gameid):
    subgame_list = eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_SUBGAME))
    for ele in subgame_list:
        if int(ele["id"]) == gameid:
            return ele["en_name"]

    return ""

## {游戏代码:游戏名字}
def get_subgame_name_enname_d():
    subgame_list = eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_SUBGAME))
    d = {}
    for ele in subgame_list:
        d[ele["en_name"]] = unicode(ele["desc"], 'utf-8')

    return d

def get_subgame_name_by_ename(d, ename):
    try:
        return d[ename]
    except:
        ename

def get_subgame_name(SubGame):
    subgamelist = get_subgame_list()
    subgame = erl.binary_to_term(SubGame)
    if subgame[0] == "subgame_info":
        subgame = subgamelist[subgame[1]]
        return subgame

    return ""

## 房间参数定义
def room_define():
    datas = {}
    for d in eval(redis_conn.hget(GAME_PARAMTER_TABLE, TAG_ROOM_DEFINE)):
        gameid = int(d["gameid"])
        if not datas.has_key(gameid):
            datas[gameid] = {}
        datas[gameid][int(d["id"])] = unicode(d["detail"], 'utf-8')
    return datas
