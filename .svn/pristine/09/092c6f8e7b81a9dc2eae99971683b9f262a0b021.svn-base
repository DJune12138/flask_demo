# encoding: UTF-8

## 玩家常规统计

import time
import base_stat
import json

def init_player_data(DPlayer, PID):
    DPlayer[PID] = {
        "os":1,
        "today_recharge":0,
        "today_withdraw":0,
        "today_up_coin":0,
        "today_down_coin":0,
        "online_time":0, 
        "bankrupt_count":0,
    }

@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    DPlayer = {}

    ## 统计所有今天在线的玩家
    online_sql = '''
        select distinct pid
        from log_account_login
        where time >= %d and time < %d
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, online_sql)
    for pid, in Result:
        init_player_data(DPlayer, pid)

    ## 玩家在线时长统计
    timeLongSql = '''
        select pid, sum(online_time)
        from log_account_login
        where time >= %d and time < %d
        and opt = "account_logout"
        group by pid
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, timeLongSql)
    for pid, online_time in Result:
        if not DPlayer.has_key(pid):
            init_player_data(DPlayer, pid)
        DPlayer[pid]["online_time"] = online_time

    ## todo 充值 提现

    ## todo 玩家破产次数

    ## 今日充值
    sql = '''
        select pid, sum(cost)
        from admin_recharge
        where time >= %d and time < %d
        and state = 1
        group by pid
    ''' % (start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for pid, recharge in Result:
        if not DPlayer.has_key(pid):
            init_player_data(DPlayer, pid)
        DPlayer[pid]["today_recharge"] = recharge

    ## 今日上分
    sql = '''
        select give_id, sum(money)
        from log_bank_give
        where time >= %d and time < %d
        and give_agent = 1 
        and recv_agent = 0
        group by give_id
    ''' % (start_time, end_time)
    for pid, coin in base_stat.fetchall(cursor, sql):
        if not DPlayer.has_key(pid):
            init_player_data(DPlayer, pid)
        DPlayer[pid]["today_up_coin"] = coin

    ## 今日下分
    sql = '''
        select recv_id, sum(money)
        from log_bank_give
        where time >= %d and time < %d
        and give_agent = 0 
        and recv_agent = 1
        group by recv_id
    ''' % (start_time, end_time)
    for pid, coin in base_stat.fetchall(cursor, sql):
        if not DPlayer.has_key(pid):
            init_player_data(DPlayer, pid)
        DPlayer[pid]["today_down_coin"] = coin

    ## 查询玩家的平台信息
    DPlayer_pt = {}
    if DPlayer:
        sql = '''
            select id, if(device = "ios", 2, 1)
            from player
            where id in (%s) 
        ''' % (",".join([str(I) for I in DPlayer.keys()]))
        for pid, pt in base_stat.fetchall(cursor, sql):
            DPlayer_pt[pid] = pt

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_player_general where time = %d" % tjdate)
    for pid, v in DPlayer.items():
        PT = 1
        if DPlayer_pt.has_key(pid):
            PT = DPlayer_pt[pid]
        sql = '''
            insert into t_player_general
                (time, pid, os, today_recharge, today_withdraw,
                today_up_coin, today_down_coin, bankrupt_times, timelong)
            values
                (%d, %d, %d, %d, %d,
                %d, %d, %d, %d)
        ''' % (tjdate, pid, PT, v["today_recharge"], v["today_withdraw"],
            v["today_up_coin"], v["today_down_coin"], v["bankrupt_count"], v["online_time"])

        cursor.execute(sql)
        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"

    print "player_stat succ：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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
