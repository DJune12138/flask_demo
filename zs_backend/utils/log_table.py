# -*- coding:utf-8 -*-

import time

def get_table_log_coin(Time):
	return "log_coin_%s" % time.strftime("%Y_%W", time.localtime(Time))

def get_table_log_subgame(Time):
	return "log_subgame_%s" % time.strftime("%Y_%W", time.localtime(Time))

def get_table_log_player_subgame(Time):
	return "log_player_subgame_%s" % time.strftime("%Y_%W", time.localtime(Time))
