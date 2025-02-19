# encoding: UTF-8

import time
import base_stat
import json
from copy import deepcopy
import requests

api_url="https://ghiag.cn/sdk/reset_click_tj"

BIGGER_RECHARGE = 500

give_data = json.dumps(
    {
        "give_times":0, 
        "give_coin":0, 
        "give_pump":0, 
        "give_player_num":0, 
        "recv_coin_player_num":0
    }
)

tj_key = {
    "reg_count":0, 
    "active_count":0, 
    "login_count":0, 
    "recharge_count":0, 
    "bigger_recharge_count":0,

    "recharge_player_count":0, 
    "new_recharge_count":0, 
    "total_recharge":0, 
    "bigger_recharge":0, 
    "recharge_coin":0,

    "withdraw":0, 
    "bankrupt_player_count":0, 
    "bankrupt_count":0, 
    "game_win":0, 
    "pump":0, 

    "total_online_time":0, 
    "max_online_num":0, 
    "give_coin_p2p":give_data, 
    "give_coin_p2a":give_data, 
    "give_coin_a2p":give_data,

    "give_coin_a2a":give_data, 
    "day2":0, 
    "day3":0, 
    "day7":0, 
    "day15":0, 

    "day30":0,
    "give_pump":0,
    "game_active_count":0, ## 游戏活跃人数
    "new_device":0, ## 新增设备数
    "url_click":0,

    "withdraw_count":0,
    'recharge_count_reg':0,
    'total_recharge_reg':0,
    'recharge_count2_reg':0,
}


## 数据更新
def up_data(d, key, subkey, v):
    if d.has_key(key):
        dd = d[key]
        dd[subkey] = v
    else:
        dd = deepcopy(tj_key)
        dd[subkey] = v
        d[key] = dd


@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    # 日期	平台 
    # 注册人数	活跃人数	登陆次数	充值人数 大额充值次数
    # 日充值人数 新增充值人数 今日总充值 大额充值总额 充值产出金币
    # 今日提现 破产人数  破产次数 游戏总盈利 游戏总抽水 
    # 日人均线时长    最高在线人数 赠送次数 赠送总金币 赠送总抽水 
    # 赠送人数  收到赠送人数 2日留存 3日留存    7日留存
    # 15日留存	30日留存	

    D = {}

    ##点击数统计
    # d_click = get_click_num(Db)
    # up_data(D, 1, "url_click", d_click["android"])
    # up_data(D, 2, "url_click", d_click["ios"])
    up_data(D, 1, "url_click", 0)
    up_data(D, 2, "url_click", 0)

    # 注册人数
    regCountSql = '''
        select os, count(1)
        from log_role_reg
        where time >= %d and time < %d
        group by os
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, regCountSql)
    for os, num in Result:
        up_data(D, os, "reg_count", num)

    ## 新增设备数
    sql = '''
        select ifnull(sum(if(device = "ios", 1, 0)), 0), ifnull(sum(if(device = "ios", 0, 1)), 0)
        from player
        where reg_time >= %d and reg_time < %d
        and did not in 
        (select distinct did from player where reg_time < %d)
    ''' % (start_time, end_time, start_time)
    ios, android = base_stat.fetchall(cursor, sql)[0]
    up_data(D, 2, "new_device", ios)
    up_data(D, 1, "new_device", android)

    # 活跃人数 登录次数统计
    activeCountSql = '''
        select os, count(distinct pid), count(pid)
        from log_account_login
        where time >= %d and time < %d
        group by os
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, activeCountSql)
    for os, activenum, loginnum in Result:
        up_data(D, os, "active_count", activenum)
        up_data(D, os, "login_count", loginnum)

    ## 游戏活跃人数统计
    sql = '''
        select count(distinct pid)
        from %s
        where time >= %d and time < %d
    ''' % (base_stat.get_table_log_player_subgame(start_time), start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for count, in Result:
        up_data(D, 1, "game_active_count", int(count))
        up_data(D, 2, "game_active_count", 0)

    # todo	日破产人数	日破产次数	

    ## 提现总额
    sql = '''
        select ifnull(sum(withdraw_deposit_money), 0), count(distinct pid)
        from admin_withdraw
        where application_time >= %d and application_time < %d
        and status = 1
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for total, count in Result:
        up_data(D, 1, "withdraw_count", int(count))
        up_data(D, 1, "withdraw", int(total))
        up_data(D, 2, "withdraw_count", 0)
        up_data(D, 2, "withdraw", 0)

    ## 赠送
    sql = '''
        select if(give_agent = 0, 'p', 'a'), if(recv_agent = 0, 'p', 'a'), count(1), 
                ifnull(sum(money), 0), ifnull(sum(pump), 0), 
            count(distinct give_id), count(distinct recv_id)
        from log_bank_give
        where time >= %d and time < %d
        group by give_agent, recv_agent
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for give_agent, recv_agent, give_times, give_coin, give_pump, \
        give_player_num, recv_coin_player_num in Result:
        Data = {
            "give_times":int(give_times), "give_coin":int(give_coin), 
            "give_pump":int(give_pump), "give_player_num":int(give_player_num), 
            "recv_coin_player_num":int(recv_coin_player_num)
            }
        up_data(D, 1, "give_coin_%s2%s" % (give_agent, recv_agent), json.dumps(Data))

    # 游戏抽水
    gameWinSql = '''
        select ifnull(sum(pump), 0)
        from %s
        where time >= %d and time < %d
    ''' % (base_stat.get_table_log_subgame(start_time), start_time, end_time)
    Result = base_stat.fetchall(cursor, gameWinSql)
    for count, in Result:
        up_data(D, 1, "pump", int(count))
        up_data(D, 2, "pump", 0)

    ## 赠送抽水
    sql = '''
        select ifnull(sum(pump), 0)
        from log_bank_give
        where time >= %d and time < %d
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for count, in Result:
        up_data(D, 1, "give_pump", int(count))

    ## 新增充值人数
    newRechargeSql = '''
        select os, count(distinct pid)
        from admin_recharge
        where time >= %d and time < %d
        and state = 1
        and pid not in
            (
            select distinct pid
            from admin_recharge
            where time < %d
            and state = 1
            )
        group by os
    ''' % (start_time, end_time, start_time)
    Result = base_stat.fetchall(cursor, regCountSql)
    for os, num in Result:
        up_data(D, os, "new_recharge_count", num)

    # 大额充值金额
    rechargeSql = '''
        select os, count(1), sum(cost), sum(coin), count(distinct pid), 
            sum(if(cost > %d, 1, 0)), sum(if(cost > %d, cost, 0))
        from admin_recharge
        where time >= %d and time < %d
        and state = 1
        group by os
    ''' % (BIGGER_RECHARGE, BIGGER_RECHARGE, start_time, end_time)
    Result = base_stat.fetchall(cursor, rechargeSql)
    for os, rechargenum, rechargemoney, rechargecoin, recharge_player_num, \
        bigger_times, bigger_recharge in Result:
        up_data(D, os, "recharge_count", rechargenum)
        up_data(D, os, "total_recharge", rechargemoney)
        up_data(D, os, "recharge_coin", rechargecoin)
        up_data(D, os, "recharge_player_count", recharge_player_num)
        up_data(D, os, "bigger_recharge_count", bigger_times)
        up_data(D, os, "bigger_recharge", bigger_recharge)

    ## 当日注册充值情况统计
    recharge_count_reg = 0
    total_recharge_reg = 0
    recharge_count2_reg = 0
    sql = '''
        select pid, sum(cost), count(1)
        from admin_recharge a, player p
        where time >= %d and time < %d
        and state = 1
        and a.pid = p.id
        and p.reg_time >= %d
    ''' % (start_time, end_time, start_time)
    for pid, cost, num in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        recharge_count_reg += 1
        total_recharge_reg += cost
        if num > 1:
            recharge_count2_reg += 1
    up_data(D, 1, "recharge_count_reg", recharge_count_reg)
    up_data(D, 1, "total_recharge_reg", total_recharge_reg)
    up_data(D, 1, "recharge_count2_reg", recharge_count2_reg)
    up_data(D, 2, "recharge_count_reg", 0)
    up_data(D, 2, "total_recharge_reg", 0)
    up_data(D, 2, "recharge_count2_reg", 0)

    # 游戏总盈亏
    gameWinSql = '''
        select os, -sum(val)
        from %s
        where time >= %d and time < %d
        and log_type >= 80000
        group by os
    ''' % (base_stat.get_table_log_coin(start_time), start_time, end_time)
    Result = base_stat.fetchall(cursor, gameWinSql)
    for os, count in Result:
        up_data(D, os, "game_win", int(count))

    # 2日留存	3日留存	7日留存	15日留存	30日留存
    Day2Sql = '''
        select os, count(distinct pid)
        from log_account_login
        where time >= %d and time < %d
        and pid in
            (select distinct pid
            from log_role_reg
            where time >= %d and time < %d)
        group by os
    ''' % (start_time, end_time, start_time - 86400, start_time)
    Result = base_stat.fetchall(cursor, Day2Sql)
    for os, count in Result:
        up_data(D, os, "day2", count)

    Day3Sql = '''
        select os, count(distinct pid)
        from log_account_login
        where time >= %d and time < %d
        and pid in
            (select distinct pid
            from log_role_reg
            where time >= %d and time < %d)
        group by os
    ''' % (start_time, end_time, start_time - 2 * 86400, start_time - 86400)
    Result = base_stat.fetchall(cursor, Day3Sql)
    for os, count in Result:
        up_data(D, os, "day3", count)

    Day7Sql = '''
        select os, count(distinct pid)
        from log_account_login
        where time >= %d and time < %d
        and pid in
            (select distinct pid
            from log_role_reg
            where time >= %d and time < %d)
        group by os
    ''' % (start_time, end_time, start_time - 6 * 86400, start_time - 86400 * 5)
    Result = base_stat.fetchall(cursor, Day7Sql)
    for os, count in Result:
        up_data(D, os, "day7", count)

    Day15Sql = '''
        select os, count(distinct pid)
        from log_account_login
        where time >= %d and time < %d
        and pid in
            (select distinct pid
            from log_role_reg
            where time >= %d and time < %d)
        group by os
    ''' % (start_time, end_time, start_time - 14 * 86400, start_time - 86400 * 13)
    Result = base_stat.fetchall(cursor, Day15Sql)
    for os, count in Result:
        up_data(D, os, "day15", count)

    Day30Sql = '''
        select os, count(distinct pid)
        from log_account_login
        where time >= %d and time < %d
        and pid in
            (select distinct pid
            from log_role_reg
            where time >= %d and time < %d)
        group by os
    ''' % (start_time, end_time, start_time - 29 * 86400, start_time - 86400 * 28)
    Result = base_stat.fetchall(cursor, Day30Sql)
    for os, count in Result:
        up_data(D, os, "day30", count)

    #日人均线时长
    onlineTimeSql = '''
        select os, sum(online_time)
        from log_account_login
        where time >= %d and time < %d
        and opt = "account_logout"
        group by os
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, onlineTimeSql)
    for os, totaltime in Result:
        up_data(D, os, "total_online_time", int(totaltime))

    # 最高在线人数
    onlineMaxSql = '''
        select os, max(num)
        from log_online
        where time >= %d and time < %d
        group by os
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, onlineMaxSql)
    for os, max_player_num in Result:
        up_data(D, os, "max_online_num", max_player_num)

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_system where time = %d" % tjdate)
    for os, v in D.items():
        v["time"] = tjdate
        v["os"] = os

        sql = '''
            replace into t_system
                (`time`, `os`, `reg_count`, `active_count`, `login_count`, 
                `recharge_count`, `bigger_recharge_count`, `recharge_player_count`, 
                    `new_recharge_count`, `total_recharge`, 
                `bigger_recharge`, `recharge_coin`, `withdraw`, `bankrupt_player_count`, `bankrupt_count`, 
                `game_win`, `pump`, `total_online_time`, `max_online_num`, `give_coin_a2a`, 
                `give_coin_a2p`, `give_coin_p2a`, `give_coin_p2p`, `day2`, `day3`, 
                `day7`, `day15`, `day30`, `give_pump`, `game_active_count`,
                `new_device`, `url_click`, `withdraw_count`, `recharge_count_reg`,`total_recharge_reg`,
                `recharge_count2_reg`)
            values
                (%(time)d, %(os)d, %(reg_count)d, %(active_count)d, %(login_count)d, 
                %(recharge_count)d, %(bigger_recharge_count)d, %(recharge_player_count)d,
                    %(new_recharge_count)d, %(total_recharge)d, 
                %(bigger_recharge)d, %(recharge_coin)d, %(withdraw)d, 
                    %(bankrupt_player_count)d, %(bankrupt_count)d, 
                %(game_win)d, %(pump)d, %(total_online_time)d, %(max_online_num)d, '%(give_coin_a2a)s', 
                '%(give_coin_a2p)s', '%(give_coin_p2a)s', '%(give_coin_p2p)s', %(day2)d, %(day3)d, 
                %(day7)d, %(day15)d, %(day30)d, %(give_pump)d, %(game_active_count)d,
                %(new_device)d, %(url_click)d, %(withdraw_count)d, %(recharge_count_reg)d, %(total_recharge_reg)d,
                %(recharge_count2_reg)d)
            ''' % v
        print sql
        cursor.execute(sql)

        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"
        
    print "game_system succ:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

## 获取点击下载链接数
def get_click_num(DbName):
    ## 此处比较恶心 通过数据库名字去获取渠道
    channel = "_".join(DbName.split("_")[:-1])
    ## 点击数判断
    r = requests.get(api_url, {"channel":channel})
    return r.json()

if __name__ == "__main__":
    end_time = base_stat.today0()
    start_time = end_time - 86400
    import sys

    db_name = "server_1"
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    if len(sys.argv) > 2:
        start_time = int(sys.argv[2])
        end_time = start_time + 86400
    stat(db_name, start_time, end_time)
