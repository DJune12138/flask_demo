# encoding: UTF-8

## 子游戏统计

import time
import base_stat
import json


@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    D = {}

    sql = '''
        select gameid, roomtype, count(1), sum(pump), sum(stake_coin), sum(output_coin)
        from %s
        where time >= %d and time < %d
        group by gameid, roomtype
        ''' % (base_stat.get_table_log_subgame(start_time), start_time, end_time)

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_subgame where time = %d" % tjdate)
    for gameid, roomtype, game_times, pump, stake_coin, \
        output_coin in base_stat.fetchall(cursor, sql):
        ## 查询该游戏活跃人数
        sql = '''
            select count(distinct pid)
            from %s
            where gameid = %d
            and time >= %d and time < %d
        ''' % (base_stat.get_table_log_player_subgame(start_time), gameid, start_time, end_time)
        print sql
        active_count = base_stat.fetchall(cursor, sql)[0][0]

        sql = '''
            insert into t_subgame
                (time, gameid, active_count, total_game_times, total_stake_coin, 
                total_output_coin, pump, roomtype)
            values
                (%d, %d, %d, %d, %d,
                %d, %d, %d)
        ''' % (tjdate, gameid, active_count, game_times, stake_coin, 
            output_coin, pump, roomtype)

        cursor.execute(sql)
        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"

    print "subgame_stat succ：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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
