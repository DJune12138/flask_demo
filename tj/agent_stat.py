# encoding: UTF-8

import time
import base_stat
import json


def init_player_agent(cursor, pid):
    ## 根据玩家ID去查询他的各个上级列表
    agent = {}

    ## 查询该玩家ID本身是否是代理
    sql = 'select count(1) from admin_agent_list where pid = %d' % pid
    if base_stat.fetchall(cursor, sql)[0][0] > 0:
        ## 自己是代理 则需要代理业绩
        agent[pid] = 0

    _pid = pid
    while True:
        ## 查找该玩家的上级代理
        sql_agent = "select invite_id from player_agent where pid = %d" % _pid
        Result = base_stat.fetchall(cursor, sql_agent)
        if len(Result) == 0:
            break
        else:
            _pid = Result[0][0]
            if _pid == 0:
                continue
            agent[_pid] = 0

    return {"agent":agent, "pump":0, "win":0}

@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    ## 日期	用户ID 自己抽水 1级代理抽水 2级代理抽水 3级代理抽水
    TJ_PUMP = {}

    ## 如果是传统代理模式 那就不用再跑数据了
    sql = 'select val from admin_system_parameter where name = "agent_pattern" '
    stype = base_stat.fetchall(cursor, sql)[0][0]
    if int(stype) != 1:
        return

    sql = '''
        select pid, sum(pump), sum(stake_coin - output_coin)
        from %s
        where time >= %d and time < %d
        group by pid
    ''' % (base_stat.get_table_log_player_subgame(start_time), start_time, end_time)
    Result = base_stat.fetchall(cursor, sql)
    for pid, pump, win in Result:
        if pump == 0 and win == 0:
            continue

        if not TJ_PUMP.has_key(pid):
            TJ_PUMP[pid] = init_player_agent(cursor, pid)

        ## 遍历该玩家的所有上级代理 给他的每个代理增加业绩
        for agent_id, agent_coin in TJ_PUMP[pid]["agent"].items():
            if not TJ_PUMP.has_key(agent_id):
                TJ_PUMP[agent_id] = init_player_agent(cursor, agent_id)
            TJ_PUMP[agent_id]["pump"] += pump
            TJ_PUMP[agent_id]["win"] += win

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_agent_day where time = %d" % tjdate)
    for pid, data in TJ_PUMP.items():
        sql = '''
            insert into t_agent_day
                (`time`, `pid`, `pump`, `win`)
            values
                (%d, %d, %d, %d)
        ''' % (tjdate, pid, data["pump"], data["win"])

        cursor.execute(sql)
        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"

    print "agent_stat succ：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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
