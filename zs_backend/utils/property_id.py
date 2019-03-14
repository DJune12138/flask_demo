# -*- coding:utf-8 -*-
"""
游戏内邮件的附件的道具和id对应关系
"""

property_map_id = {
    10010001: u'金币',
    20010001: u'喇叭'
}

overdue_map_id = {
    1: '2028-06-20 00:00:00',
    2: '2028-06-20 00:00:00',
    3: '2028-06-20 00:00:00',
    4: '2028-06-20 00:00:00'
}


def id_map_property(mail_accessories):
    """把从数据库取出的数据，根据道具id转换成道具名称，并组织数据"""

    if mail_accessories:
        property_msg = ''
        mail_accessories_dict = eval(mail_accessories)
        for property_id, quantity in mail_accessories_dict.items():
            property_name = property_map_id[int(property_id)]
            if str(quantity).endswith('0000'):
                quantity = str(quantity)[:-4] + u'万'
            property_msg += '%s*%s ' % (property_name, quantity)
        property_msg = property_msg.strip()
        return property_msg
    else:
        return ''
