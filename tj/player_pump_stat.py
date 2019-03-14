# encoding: UTF-8

import time
import base_stat
import json


def init_player_data(cursor, pid, commission_len):
    ## 根据玩家ID去查询他的各个上级列表
    agent = {0:pid}

    _i = 0
    _pid = pid
    while _i < commission_len - 1:
        ## 查找该玩家的上级代理
        sql_agent = "select invite_id from player_agent where pid = %d"
        Result = base_stat.fetchall(cursor, sql_agent % _pid)
        if len(Result) == 0:
            break
        else:
            _i += 1
            agent[_i] = Result[0][0]
            _pid = Result[0][0]

    ## 根据长度生成他的各个下级代理
    pump = {}
    pump_detail = {}
    win = {}
    win_detail = {}
    _i = 0
    while _i < commission_len:
        pump_detail[_i] = {}
        win_detail[_i] = {}
        pump[_i] = 0
        win[_i] = 0
        _i += 1

    return {"pump": pump, "agent":agent, "win":win, "pump_detail":pump_detail, "win_detail":win_detail}

@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    ## 日期	用户ID 自己抽水 1级代理抽水 2级代理抽水 3级代理抽水
    TJ_PUMP = {}

    ## 如果是传统代理模式 那就不用再跑数据了
    sql = 'select val from admin_system_parameter where name = "agent_pattern" '
    stype = base_stat.fetchall(cursor, sql)[0][0]
    if int(stype) != 2:
        return

    ## 查询有多少级返利
    sql = 'select commission_section from admin_distribution_config'
    commission_len = len(json.loads(base_stat.fetchall(cursor, sql)[0][0]))

    sql = '''
        select pid, sum(pump), sum(stake_coin - output_coin)
        from %s
        where time >= %d and time < %d
        group by pid
    ''' % (base_stat.get_table_log_player_subgame(start_time), start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for pid, pump, win in Result:
        pump = int(pump)
        win = int(win)
        if pump == 0 and win == 0:
            continue

        if not TJ_PUMP.has_key(pid):
            TJ_PUMP[pid] = init_player_data(cursor, pid, commission_len)

        ## 遍历该玩家可以享受分佣的上级代理 给该玩家的各个上级加上该玩家的业绩
        for k, pre_pid in TJ_PUMP[pid]["agent"].items():
            ## 判断是否已经有该玩家上线的数据 如果没有则初始化该上线玩家的数据
            if not TJ_PUMP.has_key(pre_pid):
                TJ_PUMP[pre_pid] = init_player_data(cursor, pre_pid, commission_len)

            ## 给该上线玩家加上该玩家的贡献度
            TJ_PUMP[pre_pid]["pump_detail"][k][pid] = pump
            TJ_PUMP[pre_pid]["win_detail"][k][pid] = win

            TJ_PUMP[pre_pid]["pump"][k] += pump
            TJ_PUMP[pre_pid]["win"][k] += win

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_distribution_day where time = %d" % tjdate)
    for pid, data in TJ_PUMP.items():
        if pid == 0:
            continue
        sql = '''
            insert into t_distribution_day
                (`time`, `pid`, `pump`, `pump_detail`, `win`, 
                `win_detail`)
            values
                (%d, %d, '%s', '%s', '%s', '%s')
        ''' % (tjdate, pid, json.dumps(data["pump"]), json.dumps(data["pump_detail"]), json.dumps(data["win"]), 
            json.dumps(data["win_detail"]))

        cursor.execute(sql)
        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"

    print "player_pump_stat succ：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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
