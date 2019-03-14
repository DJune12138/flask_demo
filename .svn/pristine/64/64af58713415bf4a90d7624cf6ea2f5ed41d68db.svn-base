# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT

from zs_backend import redis_conn
from zs_backend.utils.const import *
import json

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError:
    pass
except Exception as err:
    raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# APPID = "LTAI3knyB8CfCaQC"
# SECRET_KEY = "e0UAgw7jajDMA2xrZn1i9jlhsjswr0"

region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(channel, phone_numbers, params):
    ## 获取短息你配置
    conf = redis_conn.hget(CHANNEL_CONFIG_TABLE+channel, "sms_config")
    [appid, appkey, tpl_id, signname] = conf.split(",")
    print conf

    acs_client = AcsClient(appid, appkey, REGION)

    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(tpl_id)

    # 短信模板变量参数
    if params is not None:
        smsRequest.set_TemplateParam(params)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(uuid.uuid1())

    # 短信签名
    smsRequest.set_SignName(signname)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理

    data = smsResponse
    try:
        data = json.loads(data)
        if data["Message"] == "OK" and data["Code"] == "OK":
            return True
    except:
        pass

    print "sms err", channel, phone_numbers, params, data

    return False

if __name__ == '__main__':
    __business_id = uuid.uuid1()
    #print(__business_id)
    params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
	#params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
    print(send_sms(__business_id, "13000000000", "云通信测试", "SMS_5250008", params))
   
    
    

