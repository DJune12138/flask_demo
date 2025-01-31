# -*- coding:utf-8 -*-
import base_stat
import time
import json

ALARM_PLAYER_STAKE_COIN = 1  ## 玩家单局游戏押注
ALARM_PLAYER_OUTPUT_COIN = 2  ## 玩家单局游戏产出
ALARM_PLAYER_OUTPUT_COIN_TODAY = 3  ## 玩家当日游戏全部产出
ALARM_REG_SAME_IP = 4  ## 同一IP今日注册账号数
ALARM_REG_SAME_DEVICE = 5  ## 同一设备今日注册账号数
ALARM_PLAYER_OUT_STAKE_COIN_RATE = 6  ## 单局游戏中奖倍数
ALARM_PLAYER_RECHARGE = 7  ## 单次充值
ALARM_PLAYER_RECHARGE_TODAY = 8  ## 当日总共充值
ALARM_PLAYER_WITHDRAW = 9  ## 单次提现
ALARM_PLAYER_WITHDRAW_TODAY = 10  ## 当日总共提现
ALARM_PLAYER_PRESENT = 11  ## 单次赠送
ALARM_PLAYER_PRESENT_TODAY = 12  ## 当日总共赠送
STATE_UNREAD = 0
STATE_READ = 1

@base_stat.do_stats
def stat(Db, start_time, end_time, cursor=None, Host="localhost", User="root", Passwd="123456"):        
    ## 检测每个渠道告警配置
    sql = 'select config from admin_game_alarm_config where id = 1'
    try:
        print base_stat.fetchall(cursor, sql)
        config = base_stat.fetchall(cursor, sql)[0][0]
        conf = json.loads(config)
    except:
        print "no check_alarm config"
        return 

    last_check_time = start_time
    if start_time - base_stat.today0() < 30 * 60:
        last_check_time = base_stat.today0()

    ## 针对每个配置进行处理
    for alarm_type, alarm_val in conf.items():
        alarm_val = int(alarm_val)
        if int(alarm_type) == ALARM_PLAYER_STAKE_COIN:
            check_player_stake_coin(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_OUTPUT_COIN:
            check_player_output_coin(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_OUTPUT_COIN_TODAY:
            check_player_output_coin_today(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_REG_SAME_IP:
            check_reg_same_ip(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_REG_SAME_DEVICE:
            check_reg_same_device(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_OUT_STAKE_COIN_RATE:
            check_player_out_stake_coin_rate(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_RECHARGE:
            check_player_recharge(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_RECHARGE_TODAY:
            check_player_recharge_today(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_WITHDRAW:
            check_player_withdraw(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_WITHDRAW_TODAY:
            check_player_withdraw_today(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_PRESENT:
            check_player_present(cursor, alarm_val, last_check_time)
        elif int(alarm_type) == ALARM_PLAYER_PRESENT_TODAY:
            check_player_present_today(cursor, alarm_val, last_check_time)
        else:
            pass

    print "check_alarm succ: ", start_time

## 玩家单局游戏押注
def check_player_stake_coin(cursor, alarm_val, last_check_time):
    tab = base_stat.get_table_log_player_subgame(last_check_time)
    sql = '''
        select pid, gameid, time, stake_coin, (select ifnull(max(auto_id), 0) from %s)
        from %s a
        where time >= %d 
        and stake_coin >= %d
        and auto_id > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (tab, tab, last_check_time, alarm_val, ALARM_PLAYER_STAKE_COIN)
    for pid, gameid, time, stake_coin, auto_id in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, %d)
        ''' % (pid, time, ALARM_PLAYER_STAKE_COIN, join([gameid, stake_coin, alarm_val]), STATE_UNREAD, auto_id)
        cursor.execute(sql)

## 玩家单局游戏产出
def check_player_output_coin(cursor, alarm_val, last_check_time):
    tab = base_stat.get_table_log_player_subgame(last_check_time)
    sql = '''
        select pid, gameid, time, output_coin - stake_coin, (select ifnull(max(auto_id), 0) from %s)
        from %s a
        where time >= %d 
        and output_coin - stake_coin >= %d
        and auto_id > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (tab, tab, last_check_time, alarm_val, ALARM_PLAYER_OUTPUT_COIN)
    for pid, gameid, time, output_coin, auto_id in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, %d)
        ''' % (pid, time, ALARM_PLAYER_OUTPUT_COIN, join([gameid, output_coin, alarm_val]), STATE_UNREAD, auto_id)
        cursor.execute(sql)

## 玩家当日游戏全部产出
def check_player_output_coin_today(cursor, alarm_val, last_check_time):
    sql = '''
        select pid, val
        from
            (select pid, sum(output_coin - stake_coin) as val
            from %s 
            where time >= %d
            and pid not in 
                (select distinct pid from admin_game_alarm where time >= %d and stype == %d)
            group by pid) t
        where val >= %d        
    ''' % (base_stat.get_table_log_player_subgame(now_sec()), base_stat.today0(),
           base_stat.today0(), ALARM_PLAYER_OUTPUT_COIN_TODAY, alarm_val)
    for pid, win_coin in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (pid, time, ALARM_PLAYER_OUTPUT_COIN_TODAY, join([win_coin, alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

## 同一IP今日注册账号数
def check_reg_same_ip(cursor, alarm_val, last_check_time):
    sql = '''
        select reg_ip, val
        from
            (select reg_ip, count(1) as val
            from player
            where reg_time >= %d
            and reg_ip not in 
                (select distinct pid from admin_game_alarm where time >= %d and stype = %d)
            group by reg_ip) t
        where val >= %d
    ''' % (base_stat.today0(), base_stat.today0(), ALARM_REG_SAME_IP, alarm_val)
    for reg_ip, count in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (reg_ip, now_sec(), ALARM_REG_SAME_IP, join([count, alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

# 同一设备今日注册账号数
def check_reg_same_device(cursor, alarm_val, last_check_time):
    sql = '''
        select did, val
        from
            (select did, count(1) as val
            from player
            where reg_time >= %d
            and did not in 
                (select distinct pid from admin_game_alarm where time >= %d and stype = %d)
            group by did)
        where val >= %d
    ''' % (base_stat.today0(), base_stat.today0(), ALARM_REG_SAME_DEVICE, alarm_val)
    for did, count in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (did, now_sec(), ALARM_REG_SAME_DEVICE, join([count, alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

# 单局游戏中奖倍数
def check_player_out_stake_coin_rate(cursor, alarm_val, last_check_time):
    tab = get_table_log_player_subgame(now_sec())
    sql = '''
        select pid, gameid, time, format(output_coin/stake_coin, 2), (select ifnull(max(auto_id), 0) from %s)
        from %s a
        where time >= %d 
        and stake_coin > 0
        and output_coin/stake_coin >= %d
        and auto_id > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (tab, tab, last_check_time, alarm_val, ALARM_PLAYER_OUT_STAKE_COIN_RATE)
    for pid, gameid, time, count, auto_id in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, %d)
        ''' % (pid, time, ALARM_PLAYER_OUT_STAKE_COIN_RATE, join([gameid, count, alarm_val]), STATE_UNREAD, auto_id)
        cursor.execute(sql)

# 单次充值
def check_player_recharge(cursor, alarm_val, last_check_time):
    sql = '''
        select pid, cost, time, (select ifnull(max(time), 0) from admin_recharge)
        from admin_recharge
        where time >= %d
        and cost >= %d
        and state = %d
        and time > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (last_check_time, alarm_val, PAY_STATE_SUCC, ALARM_PLAYER_RECHARGE)
    for pid, cost, time, max_time in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (%d, %d, %d, '%s', %d, %d)
        ''' % (0, pid, time, ALARM_PLAYER_RECHARGE, join([int(cost/100), alarm_val]), STATE_UNREAD, max_time)
        cursor.execute(sql)

# 当日总共充值
def check_player_recharge_today(cursor, alarm_val, last_check_time):
    sql = '''
        select pid, val
        from
            (select pid, sum(cost) as val
            from admin_recharge
            where time >= %d
            and state = %d
            and pid not in 
                (select pid from admin_game_alarm where time >= %d and stype = %d)
            group by pid)
        where val >= %d
    ''' % (base_stat.today0(), PAY_STATE_SUCC, base_stat.today0(), ALARM_PLAYER_RECHARGE_TODAY, alarm_val)
    for pid, cost in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (pid, now_sec(), ALARM_PLAYER_RECHARGE_TODAY, join([int(cost/100), alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

# 单次提现
def check_player_withdraw(cursor, alarm_val, last_check_time):
    sql = '''
        select pid, withdraw_deposit_money, application_time, (select ifnull(max(id), 0) from admin_withdraw)
        from admin_withdraw
        where application_time >= %d
        and withdraw_deposit_money >= %d
        and status = 1 
        and id > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (last_check_time, alarm_val, ALARM_PLAYER_WITHDRAW)
    print sql
    for pid, money, time, max_id in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, %d)
        ''' % (pid, time, ALARM_PLAYER_WITHDRAW, join([int(money/100), alarm_val]), STATE_UNREAD, max_id)
        cursor.execute(sql)

# 当日总共提现
def check_player_withdraw_today(cursor, alarm_val, last_check_time):
    sql = '''
        select pid, val
        from
            (select pid, sum(withdraw_deposit_money) as val
            from admin_withdraw
            where application_time >= %d
            and pid not in 
                (select pid from admin_game_alarm where time >= %d and stype = %d)
            group by pid) t
        where val >= %d
    ''' % (base_stat.today0(), base_stat.today0(), ALARM_PLAYER_WITHDRAW_TODAY, alarm_val)
    print sql
    for pid, money in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (pid, now_sec(), ALARM_PLAYER_WITHDRAW_TODAY, join([int(money/100), alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

# 单次赠送
def check_player_present(cursor, alarm_val, last_check_time):
    sql = '''
        select give_id, money, time, (select ifnull(max(time), 0) from log_bank_give)
        from log_bank_give
        where time >= %d
        adn give_agent = 0
        and money >= %d
        and time > (select ifnull(max(relate_id), 0) from admin_game_alarm where stype = %d)
    ''' % (last_check_time, alarm_val, ALARM_PLAYER_PRESENT)
    for pid, money, time, max_time in base_stat.fetchall(cursor, sql):
        if not pid:
            continue
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, %d)
        ''' % (pid, time, ALARM_PLAYER_PRESENT, join([int(money/100), alarm_val]), STATE_UNREAD, max_time)
        cursor.execute(sql)

# 当日总共赠送
def check_player_present_today(cursor, alarm_val, last_check_time):
    sql = '''
        select give_id, val
        from
            (select give_id, sum(money) as val
            from log_bank_give
            where give_agent = 0
            and time >= %d
            and give_id not in 
                (select pid from admin_game_alarm where time >= %d and stype = %d)
            group by give_id)
        where val >= %d
    ''' % (base_stat.today0(), base_stat.today0(), ALARM_PLAYER_PRESENT_TODAY, alarm_val)
    for pid, money in base_stat.fetchall(cursor, sql):
        sql = '''
            insert into admin_game_alarm (id, pid, time, stype, val, state, relate_id) 
            values (0, %d, %d, %d, '%s', %d, 0)
        ''' % (pid, now_sec(), ALARM_PLAYER_PRESENT_TODAY, join([int(money/100), alarm_val]), STATE_UNREAD)
        cursor.execute(sql)

def join(l):
    return ",".join([str(i) for i in l])

def now_sec():
    return int(time.time())

if __name__ == "__main__":
    end_time = now_sec()
    start_time = end_time - 60 * 60 * 24
    import sys

    db_name = "server_1"
    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    if len(sys.argv) > 2:
        start_time = int(sys.argv[2])
        end_time = start_time + 86400
    stat(db_name, start_time, end_time)
