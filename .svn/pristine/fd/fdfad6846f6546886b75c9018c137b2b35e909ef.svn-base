# -*- coding:utf-8 -*-
from zs_backend import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template, session, request, jsonify, g
from zs_backend.utils import time_util
from zs_backend.utils.channel_qry import *
from zs_backend.utils.const import *
import json

# 活动类型映射
activity_type_map = {
    6: u'固定金额赠送',
    7: u'充值金额的百分比赠送'
}

participation_member_map = {
    1: u'所有玩家',
    2: u'新玩家',
    3: u'老玩家'
}

# 状态映射
TAKE_EFFECT = 1  # 生效
LOSE_EFFICACY = 0  # 失效
status_map = {
    1: u'生效',
    0: u'失效'
}


@busi.route('/recharge/discounts/show', methods=['GET'])
@login_require
def recharge_discounts_show():
    """充值优惠设置页面"""

    # 其他信息
    other_msg = dict()
    other_msg['beginDate'] = 11
    other_msg['endDate'] = 11
    other_msg['OThers'] = [u'<td> 活动描述：<input type="text" id="activity_title_retrieve" '
                           u'name="activity_title" value=""> </td>',
                           u'<td> 后台账号：<input type="text" id="user_id_retrieve" '
                           u'name="user_id" value=""> </td>']

    # 返回模版与数据
    return render_template('recharge_discounts.html', other_msg=other_msg)


@busi.route('/recharge/discounts/retrieve', methods=['GET'])
@login_require
def recharge_discounts_retrieve():
    """充值优惠设置查询"""

    # 获取参数
    channel_id = session['select_channel']
    activity_content = request.args.get('activity_title')
    user_id = request.args.get('user_id')
    begin_time = request.args.get('beginDate')
    end_time = request.args.get('endDate')

    # 处理时间
    begin_time = time_util.start(begin_time)
    end_time = time_util.end(end_time)

    # 校验并处理参数
    if begin_time >= end_time:
        return jsonify(result='fail', msg=u'结束时间不能小于开始时间！')
    where = ''
    if user_id:
        where += " AND user_id='%s'" % user_id
    if activity_content:
        where += " AND activity_content like '%%%s%%'" % activity_content

    # 从数据库获取数据
    retrieve_sql = """SELECT priority,id,user_id,activity_content,activity_type,
                              participation_member,request_times,max_add_recharge,journal_require,begin_time,
                              end_time,status
                      FROM admin_recharge_discounts
                      WHERE ((begin_time>=%s AND begin_time<=%s)
                      OR (end_time>=%s AND end_time<=%s))
                        %s
                      ORDER BY status DESC;""" \
                   % (begin_time, end_time, begin_time, end_time, where)
    data = LogQry(channel_id).qry(retrieve_sql)

    # 处理数据
    data_list = list()
    for priority, activity_id, user_id, activity_content, activity_type, \
        participation_member, request_times, max_add_recharge, journal_require, begin_time, \
        end_time, status in data:
        data_dict = dict()
        data_dict['priority'] = priority
        data_dict['activity_id'] = activity_id
        data_dict['user_id'] = user_id
        data_dict['activity_content'] = activity_content.replace('\n', '<br>')
        data_dict['activity_type'] = activity_type_map[activity_type]
        data_dict['participation_member'] = participation_member_map[participation_member]
        data_dict['request_times'] = request_times
        data_dict['max_add_recharge'] = max_add_recharge if max_add_recharge else ''
        data_dict['journal_require'] = journal_require
        data_dict['begin_time'] = time_util.formatDateTime(begin_time)
        data_dict['end_time'] = time_util.formatDateTime(end_time)
        if status == TAKE_EFFECT:  # 如果状态为生效，再判断一下当前时间与活动实际时间是否生效，若失效则修改状态
            if not begin_time < time_util.now_sec() < end_time:
                status = LOSE_EFFICACY
                update_sql = """UPDATE admin_recharge_discounts
                                SET status=%s
                                WHERE id=%s;""" \
                             % (status, activity_id)
                LogQry(channel_id).execute(update_sql)
        data_dict['status'] = status_map[status]
        data_dict['status_num'] = status  # 用于调字体颜色
        data_list.append(data_dict)

    # 返回模版与数据
    return jsonify(result='ok', data=data_list)


@busi.route('/recharge/discounts/create/update', methods=['POST'])
@login_require
def recharge_discounts_create_update():
    """充值优惠设置新建/修改"""

    # 获取参数
    channel_id = session['select_channel']
    user_id = g.user_id
    activity_title = request.form.get('activity_title')
    show_picture_url = request.form.get('show_picture_url')
    tab1_url = request.form.get('tab1_url')
    tab2_url = request.form.get('tab2_url')
    activity_type = request.form.get('activity_type')
    participation_member = request.form.get('participation_member')
    participation_level = request.form.get('participation_level')
    activity_content = request.form.get('activity_content')
    recharge_detail = request.form.get('recharge_detail')
    journal_require = request.form.get('journal_require')
    request_times = request.form.get('request_times')
    max_add_recharge = request.form.get('max_add_recharge')
    begin_time = request.form.get('begin_time')
    end_time = request.form.get('end_time')
    priority = request.form.get('priority')
    activity_id = request.form.get('activity_id')

    # 校验并处理参数
    if not all([begin_time, end_time, priority, activity_content]):
        return jsonify(result=0, msg=u'请输入所有必填项！')
    try:
        int(priority)
        int(journal_require)
        int(request_times)
        max_add_recharge = int(max_add_recharge) * 100
    except ValueError:
        return jsonify(result=0, msg=u'流水要求、申请次数、最高赠送、优先级为整数纯数字！')
    try:
        recharge_detail = eval(recharge_detail)
    except Exception:
        return jsonify(result=0, msg=u'所有充值梯度里的项都是必填项，且为整数纯数字！')
    for one in recharge_detail:
        i = 0
        for one_in_one in one:
            try:
                one[i] = int(one_in_one) * 100
            except ValueError:
                return jsonify(result=0, msg=u'所有充值梯度里的项都是必填项，且为整数纯数字！')
            i += 1
    if participation_level == ']':
        participation_level = ''
    begin_time = time_util.formatTimestamp(begin_time)
    end_time = time_util.formatTimestamp(end_time)
    if begin_time > end_time:
        return jsonify(result=0, msg=u'开始时间不能大于结束时间！')

    # 向游戏服发送请求
    times = [begin_time] + [end_time]
    game_status = GameWeb(channel_id).post('/api/up_activity',
                                           {'id': int(activity_type), 'icon1': tab1_url, 'icon2': tab2_url,
                                            'mark': activity_title, 'ord': int(priority), 'detail': show_picture_url,
                                            'times': times, 'rules': activity_content})
    if game_status['result'] != 'ok':
        return jsonify(result=0, msg='创建失败！')

    # 根据当前时间判定新建的活动的状态
    if begin_time < time_util.now_sec() < end_time:
        status = TAKE_EFFECT
    else:
        status = LOSE_EFFICACY

    # 查询账号名
    retrieve_sql = """SELECT name
                      FROM user
                      WHERE id=%s;""" % user_id
    user_id = SqlOperate().select(retrieve_sql)[0][0]

    # 新建充值优惠
    if not activity_id:
        # 先把同活动类型为生效状态的活动改状态为失效
        update_sql = """UPDATE admin_recharge_discounts
                        SET status=%s
                        WHERE status=%s
                        AND activity_type=%s;""" \
                     % (LOSE_EFFICACY, TAKE_EFFECT, activity_type)
        LogQry(channel_id).execute(update_sql)
        # 再新建新的活动
        create_sql = """INSERT INTO admin_recharge_discounts
                        VALUES (0,'%s',%s,'%s','%s',%s,
                                %s,'%s','%s','%s',%s,
                                %s,'%s','%s',%s,%s,
                                %s,%s);""" \
                     % (user_id, priority, activity_title, activity_content, activity_type,
                        participation_member, show_picture_url, tab1_url, tab2_url, begin_time,
                        end_time, participation_level, recharge_detail, request_times, max_add_recharge,
                        journal_require, status)
        LogQry(channel_id).execute(create_sql)
        return jsonify(result=1, msg=u'新建成功！')

    # 修改充值优惠
    else:
        # 先把同活动类型为生效状态的活动改状态为失效
        update_sql = """UPDATE admin_recharge_discounts
                        SET status=%s
                        WHERE status=%s
                        AND activity_type=%s;""" \
                     % (LOSE_EFFICACY, TAKE_EFFECT, activity_type)
        LogQry(channel_id).execute(update_sql)
        # 再修改活动
        update_sql = """UPDATE admin_recharge_discounts
                        SET priority=%s,activity_title='%s',activity_content='%s',activity_type=%s,participation_member=%s,
                            show_picture_url='%s',tab1_url='%s',tab2_url='%s',begin_time=%s,end_time=%s,
                            participation_level='%s',recharge_detail='%s',request_times=%s,max_add_recharge=%s,journal_require=%s,
                            status=%s,user_id='%s'
                        WHERE id=%s;""" \
                     % (priority, activity_title, activity_content, activity_type, participation_member,
                        show_picture_url, tab1_url, tab2_url, begin_time, end_time,
                        participation_level, recharge_detail, request_times, max_add_recharge, journal_require,
                        status, user_id, activity_id)
        LogQry(channel_id).execute(update_sql)
        return jsonify(result=1, msg=u'修改成功！')


@busi.route('/recharge/discounts/json', methods=['GET'])
@login_require
def recharge_discounts_json():
    """返回修改充值优惠设置的json数据"""

    # 获取参数
    activity_id = request.args.get('activity_id')

    # 从数据库获取数据
    retrieve_sql = """SELECT activity_type,activity_title,show_picture_url,tab1_url,tab2_url,
                              activity_content,participation_member,participation_level,journal_require,request_times,
                              max_add_recharge,recharge_detail,begin_time,end_time,priority
                      FROM admin_recharge_discounts
                      WHERE id=%s;""" % activity_id
    data = LogQry(session['select_channel']).qry(retrieve_sql)

    # 处理数据
    data = data[0]
    data_dict = dict()
    data_dict['activity_type'] = data[0]
    data_dict['activity_title'] = data[1]
    data_dict['show_picture_url'] = data[2]
    data_dict['tab1_url'] = data[3]
    data_dict['tab2_url'] = data[4]
    data_dict['activity_content'] = data[5]
    data_dict['participation_member'] = data[6]
    data_dict['participation_level'] = data[7]
    data_dict['journal_require'] = data[8]
    data_dict['request_times'] = data[9]
    data_dict['max_add_recharge'] = data[10] / 100
    new_detail = eval(data[11])
    for one in new_detail:
        i = 0
        for one_in_one in one:
            one[i] = one_in_one / 100
            i += 1
    data_dict['recharge_detail'] = new_detail
    data_dict['begin_time'] = time_util.formatDateTime(data[12])
    data_dict['end_time'] = time_util.formatDateTime(data[13])
    data_dict['priority'] = data[14]
    data_dict['activity_id'] = activity_id

    # 返回数据
    return jsonify(data=data_dict)
