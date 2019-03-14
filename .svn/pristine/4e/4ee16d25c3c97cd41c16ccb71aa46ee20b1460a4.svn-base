# _*_ coding:utf-8 _*_

## 公共搜索框编写
## 开始日期 结束日期 平台 渠道(支持多选) 玩家ID

from flask.globals import session, request
from zs_backend.utils import time_util
import random
import datetime
import time

def search_bar(Action, beginDate = True, endDate = False, PT = False, SelectChannel = None,
	Channels = True, ChannelSize = 1, PlayerID = False, NickName = False, Account = False,
	QueryType = 2, OThers = [], Method = "post", PrecisionSecond = False):

	Html = u'''
	<script src="/static/js/jquery-2.1.1.min.js"></script>
	<script src="/static/js/bootstrap.min.js"></script>
	<script src="/static/js/my97date/WdatePicker.js"></script>
	<script src="/static/js/all.js?%f"></script>
	<form id="query_form" action="%s" method="%s" accept-charset="UTF-8">
		<div class='search'>
	        %s
        </div>
    </form>
'''

	QueryButtonHtml = u""
	if QueryType == 3:
		QueryButtonHtml = u'''
			<input type="button" id="query_btn" class="btn btn-primary btn-sm" value="查询"/>
		'''
	else:
		QueryButtonHtml = u'''
			<input type="submit" id="query_btn" class="btn btn-primary btn-sm" value="查询"/>
		'''


	## 日期选择
	DaterStr = u""
	if beginDate != False:
		if beginDate == True:
			beginDate = time_util.Monday0()
		elif beginDate == 7:
			beginDate = time_util.formatTimestampFormat(str(time_util.date_add(datetime.date.today().strftime('%Y%m%d'), -7)), '%Y%m%d')
		elif beginDate == 11:
			beginDate = int(time.mktime(datetime.datetime.now().date().timetuple()))
		elif beginDate == 1:
			beginDate = time_util.today0()
		if not PrecisionSecond:
			DaterStr = u'''<span>
				日期：<input class="Wdate" type="text" readonly onClick="WdatePicker({firstDayOfWeek:1, isShowClear:false, isShowOK:false, isShowToday:false, autoPickDate:true})" id="beginDate" name="beginDate" value="%s" required>
			''' % time_util.formatTimeWithDesc(beginDate, '%Y-%m-%d')
		else:
			DaterStr = u'''<span>
				日期：<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:'yyyy-MM-dd HH:mm:ss', firstDayOfWeek:1, isShowClear:false, isShowOK:false, isShowToday:false, autoPickDate:true})" id="beginDate" name="beginDate" value="%s" required>
			''' % time_util.formatTimeWithDesc(beginDate, '%Y-%m-%d %H:%M:%S')
	if endDate != False:
		if endDate == True:
			endDate = time_util.now_sec()
		elif endDate == 11:
			endDate = int(time.mktime(datetime.datetime.now().date().timetuple())) + 86400
		if not PrecisionSecond:
			DaterStr += u'''
				--<input class="Wdate" type="text" readonly onClick="WdatePicker({firstDayOfWeek:1, isShowClear:false, isShowOK:false, isShowToday:false, autoPickDate:true})" id="endDate" name="endDate" value="%s" required>
			''' % time_util.formatTimeWithDesc(endDate, '%Y-%m-%d')
		else:
			DaterStr += u'''
				--<input class="Wdate" type="text" readonly onClick="WdatePicker({dateFmt:'yyyy-MM-dd HH:mm:ss', firstDayOfWeek:1, isShowClear:false, isShowOK:false, isShowToday:false, autoPickDate:true})" id="endDate" name="endDate" value="%s" required>
			''' % time_util.formatTimeWithDesc(endDate, '%Y-%m-%d %H:%M:%S')
	if DaterStr:
		DaterStr += u'%s</span>' % QueryButtonHtml
	else:
		DaterStr = u'<span>%s</span>' % QueryButtonHtml

	## 平台选择
	PTStr = u""

	## 渠道选择
	ChannelStr = u""

	## 玩家选择
	PlayerStr = u""
	if PlayerID != False:
		PlayerStr = u'''
				<span> 玩家ID：<input type="text" id="PlayerID" name="PlayerID" value="%s" placeholder=""></span>
			''' % PlayerID
	if NickName != False:
		PlayerStr += u'''
				<span> 玩家昵称：<input type="text" id="NickName" name="NickName" value="%s" placeholder=""> </span>
			''' % NickName
	if Account != False:
		PlayerStr += u'''
				<span> 玩家账号：<input type="text" id="Account" name="Account" value="%s" placeholder=""> </span>
			''' % Account

	## 日期快速查询
	dateFast = u""
	if endDate != False:
		dateFast = u'''
	        <ul class="date_fast">
	            <li time="last_month">上月</li>
	            <li time="month">本月</li>
	            <li time="last_week">上周</li>
	            <li time="week">本周</li>
	            <li time="yesterday">昨日</li>
	            <li time="today">今日</li>
	        </ul>
			'''

	if OThers:
		SubL = [PTStr, ChannelStr] + OThers + [ PlayerStr, DaterStr , dateFast]
	else:
		SubL = [PTStr, ChannelStr, PlayerStr, DaterStr, dateFast]

	return Html % (random.random(), Action, Method, "".join(SubL))
