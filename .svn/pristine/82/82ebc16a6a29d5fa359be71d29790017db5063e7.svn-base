# encoding: UTF-8

## 玩家游戏统计

import time
import base_stat
import json


@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):
    D = {}

    sql = '''
    	select pid, gameid, roomtype, sum(stake_coin), sum(output_coin),
    		sum(pump), count(1)
    	from %s
    	where time >= %d and time < %d
    	group by pid, gameid, roomtype
    ''' % (base_stat.get_table_log_player_subgame(start_time), start_time, end_time)

    tjdate = int(time.strftime("%Y%m%d", time.localtime(start_time)))
    cursor.execute("delete from t_player_subgame where time = %d" % tjdate)
    for pid, gameid, roomtype, total_stake_coin, total_output_coin, \
    	pump, game_count in base_stat.fetchall(cursor, sql):
    	sql = '''
    		insert into t_player_subgame 
    			(time, pid, gameid, roomtype, game_count, 
    			stake_coin, output_coin, pump)
    		values 
    			(%d, %d, %d, %d, %d,
    			%d, %d, %d)
    	''' % (tjdate, pid, gameid, roomtype, game_count,
    		total_stake_coin, total_output_coin, pump)
    	cursor.execute(sql)
        if cursor._result.warning_count > 0:
            print "sql err...", sql
            raise "sql err"

    print "player_subgame_stat succ：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

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