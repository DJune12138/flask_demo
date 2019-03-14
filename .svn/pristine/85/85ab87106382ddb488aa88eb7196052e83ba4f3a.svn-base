# -*- coding:utf-8 -*-
# 使用蓝图按照接口版本划分模块

from flask import Blueprint

# 创建版本1.0的蓝图 http://www.example.com/api/1.0/info
api = Blueprint('api', __name__)	

from . import h5_api, pay_cb, api_route, wx, first, sms, pre_pay, api_jobs, pay_channel_api, distribution_api, \
	recharge_api, withdraw_api

API_JOBS = [
	# {
	# 	"func":api_jobs.get_channel_data,
	# 	"id":"1",
	# 	"args":(),
	# 	"trigger":"interval",
	# 	"seconds":10,
	# },
]
