#/usr/bin/env python
# encoding: UTF-8
"This module is used for game log persisting into mysql"

import os, sys, getopt, re, time, shutil, commands
import pymysql
import traceback
import time
from warnings import filterwarnings

filterwarnings('error', category = pymysql.Warning)

interval = 210 ## 处理210秒前的文件
game_log_dir = "./logs/game/" ## 游戏日志根路径

game_config = "../../config/server_common.config"
## 出错的日志目录
errPath = "../errlog"
## 完成的日志目录
compPath = "../complog"

## 查找早于interval之前的时间的所有日志
def findLogFiles():
    files = os.listdir(os.getcwd())
    afile = []
    r = re.compile("^log_.+?_\d{14}\.log$") ##文件名：log_subgame_20180612144042.log
    t = time.time() - interval
    for fname in files:
        if r.match(fname) == None:
            continue
        else:
            fileDate = fname[-18:-4]
            ftime = time.mktime(time.strptime(fileDate, "%Y%m%d%H%M%S"))
            if ftime <= t:
                ## 早于这个时间的要处理
                afile.append(fname)
    return afile

def persisLogFile(cursor, files):
    if not os.path.isdir(errPath):
        os.makedirs(errPath)
    if not os.path.isdir(compPath):
        os.makedirs(compPath)

    sql = "LOAD DATA LOCAL INFILE '%s' \
INTO TABLE `%s` \
FIELDS TERMINATED BY '|' \
LINES TERMINATED BY '\\n' "
    for f in files:
        table = translate_table_name(cursor, f[:-19], f[-18:-10])
        if table == "log_player_subgame_json":
            continue
        try:
            newSql = sql % (f, table)
            cursor.execute(newSql)
            shutil.move(f, compPath)
        except Exception, e:
            print "persislog err:...............", f , e
            shutil.move(f, errPath)

def get_log_db():
    Cmd = ''' grep game_log_db %s | tail -n 1 |sed 's/{game_log_db, \"//g'|sed 's/\"}.//g' ''' % game_config
    LOG_DB_STR = commands.getoutput(Cmd).strip()
    LOG_DB = {}
    for v in LOG_DB_STR.split(","):
        vv = v.split("=")
        LOG_DB[vv[0].strip()] = vv[1].strip()

    return LOG_DB

def main():
    global interval
    if len(sys.argv) >= 2:
        game_log_dir = sys.argv[1]

    try:
        ## 日志目录
        os.chdir(game_log_dir)
        allFiles = findLogFiles()

        LOG_DB = get_log_db()

        ## 链接数据库
        conn = pymysql.connect(host=LOG_DB["host"], 
            user=LOG_DB["user"], passwd=LOG_DB["passwd"], 
            db=LOG_DB["db"], charset='utf8',
            local_infile=1)
        cursor = conn.cursor()
        ## 入库
        persisLogFile(cursor, allFiles)

        ## 提交
        cursor.execute("commit;")
        cursor.close()
        conn.close()
    except Exception,e:
        print traceback.format_exc()

def translate_table_name(cursor, name, datestr):
    if name=="log_coin" or name=="log_subgame" or name=="log_player_subgame":
        YYYY_WEEK = time.strftime("%Y_%W", time.localtime(time.mktime(time.strptime(datestr, "%Y%m%d"))))
        TableName = "%s_%s" % (name, YYYY_WEEK)

        ## 判断表是否存在 不存在则创建
        try:
            cursor.execute("show create table %s" % name)
            DML = cursor.fetchall()[0][1]
            DML_HEAD = u"CREATE TABLE "
            sql = u"%s if not exists `%s` %s" % (DML_HEAD, TableName, DML[len(DML_HEAD) + len(name) + 2:])
            cursor.execute(sql)
        except pymysql.Warning, w:
            pass
        finally:
            return TableName
    else:
        return name

if __name__ == "__main__":
    main()
