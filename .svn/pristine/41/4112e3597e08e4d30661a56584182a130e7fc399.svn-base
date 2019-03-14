# _*_ coding:utf-8 _*_
from zs_backend.busi import busi
from zs_backend.utils.common import login_require
from flask import render_template


@busi.route('/player/game/detail/show', methods=['GET'])
@login_require
def player_game_detail_show():
    """玩家游戏详情页面"""

    return render_template('player_game_detail.html')
