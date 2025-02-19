CREATE TABLE IF NOT EXISTS admin_withdraw (
    id int unsigned PRIMARY KEY auto_increment,
    pid int unsigned comment '会员账号',
    member_level int unsigned comment '会员层级',
    withdraw_deposit_id varchar(100) not null comment '提现单号',
    withdraw_deposit_type tinyint comment '提现类型',
    withdraw_deposit_money int unsigned comment '提现金额',
    application_time int unsigned comment '申请时间',
    service_charge int unsigned comment '手续费',
    platform_withhold int unsigned comment '平台扣款',
    status tinyint comment '状态',
    dispose_time int unsigned comment '处理时间',
    dispose_user int unsigned comment '处理人',
    remark varchar(100) comment '备注',
    payee varchar(10) comment '收款人',
    due_bank varchar(15) comment '收款银行',
    gathering_account varchar(100) comment '收款账号',
    open_account_address varchar(100) comment '开户地址',
    failed_reason varchar(100) comment '失败原因',
    channel_id int unsigned comment '渠道id',
    KEY withdraw_deposit_type (withdraw_deposit_type) USING BTREE,
    KEY status (status) USING BTREE,
    KEY application_time (application_time) USING BTREE,
    KEY pid (pid) USING BTREE,
    KEY channel_id (channel_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='提现订单';

create table `admin_recharge` (
  `time` bigint(20) unsigned not null COMMENT '时间',
  `pid` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `os` SMALLINT(1) unsigned not null COMMENT '操作系统 ios 2  其他 1',
  `channel` VARCHAR(20) not null COMMENT '渠道',
  `vip` SMALLINT(5) not null COMMENT 'vip等级',
  `lv` SMALLINT(5) not null COMMENT '等级',
  `orderno` varchar(50) not null COMMENT '订单号',
  `platformno` VARCHAR(50) not null COMMENT '平台订单号',
  `coin` bigint(10) not null COMMENT '获得金币',
  `cost` int(5) not null COMMENT '消耗金额 单位分',
  `rechargeid` int(5) not null COMMENT '计费点id',
  `state` SMALLINT(5) not null COMMENT '状态 0发起付费  1付费成功 2付费失败 3待审核',
  `add_recharge` int(5) default 0 comment '赠送金额',
  `type` int(5) not null COMMENT '充值类型 1公司入款 2客服充值',
  `pay_type` int(5) not null COMMENT '支付类型 1公司入款 2客服充值',
  `pay_channel` int(5) not null COMMENT '支付通道ID',
  `request_pid` int(5) not null COMMENT '申请人ID',
  `review_time` int(5) not null COMMENT '审核时间',
  `review_pid` int(5) not null COMMENT '审核人',
  `pay_name` VARCHAR(100) COMMENT '转账姓名',
  `memo` VARCHAR(100) not null COMMENT '备注',
  KEY `time` (`time`) USING BTREE,
  KEY `pid` (`pid`) USING BTREE,
  UNIQUE KEY `orderno` (`orderno`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='充值日志';

CREATE TABLE IF NOT EXISTS admin_presented_config (
    channel int unsigned not null comment "渠道",
    config blob comment "配置",
    primary key `channel` (`channel`)
);

CREATE TABLE IF NOT EXISTS admin_opt_log (
    id int unsigned primary key auto_increment,
    channel int unsigned not null comment "渠道",
    maintype int unsigned not null default 0 comment "大类 0输赢控制  1系统配置 2玩家相关  3财务相关",
    log_type int comment "日志类型 0单控玩家  1全盘操控",
    operator int comment "操作员ID",
    obj int comment "操作对象",
    val varchar(500) comment "操作数据",
    `timestamp` int comment "操作时间",
    key `timestamp`(`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS admin_announcement(
    `id` int unsigned primary key auto_increment COMMENT '公告ID',
    `channel` bigint(20) unsigned NOT NULL COMMENT '渠道ID',
    `priority` bigint(20) NOT NULL COMMENT '优先级',
    `title` varchar(100) NOT NULL DEFAULT '' COMMENT '公告标题',
    `content_image_url` varchar(1000) NOT NULL DEFAULT '' COMMENT '内容图片链接',
    `push_times` int(20) NOT NULL DEFAULT 0 COMMENT '每日推送次数',
    `start_date` int(30) NOT NULL COMMENT '开始日期',
    `end_date` int(30) NOT NULL COMMENT '结束日期',
    `status` tinyint(5) NOT NULL DEFAULT 1 COMMENT '状态',
    KEY `title` (`title`) USING BTREE,
    KEY `channel` (`channel`) USING BTREE,
    key `status` (`status`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='游戏内报告';

CREATE TABLE IF NOT EXISTS admin_marquee (
    id bigint unsigned primary key,
    user_id varchar(100) comment '生成者账号',
    marquee_content varchar(1000) comment '跑马灯内容',
    push_times smallint signed comment '每日展示次数',
    begin_time int unsigned comment '开始时间',
    end_time int unsigned comment '结束时间',
    status tinyint signed comment '状态',
    UNIQUE KEY id (id) USING BTREE,
    KEY begin_time (begin_time) USING BTREE,
    KEY end_time (end_time) USING BTREE,
    KEY user_id (user_id) USING BTREE,
    KEY marquee_content (marquee_content) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='跑马灯（小喇叭）';

CREATE TABLE IF NOT EXISTS admin_mail (
    id int unsigned PRIMARY KEY auto_increment,
    user_id varchar(100) comment '生成者账号',
    mail_title varchar(100) comment '邮件标题',
    mail_content varchar(5000) comment '邮件内容',
    mail_accessories varchar(500) comment '邮件附件',
    push_time int unsigned DEFAULT 0 comment '发送时间',
    push_player_id text comment '推送用户id',
    expire tinyint unsigned comment '有效时间',
    status tinyint DEFAULT 0 comment '状态',
    UNIQUE KEY id (id) USING BTREE,
    KEY mail_title (mail_title) USING BTREE,
    KEY user_id (user_id) USING BTREE,
    KEY push_time (push_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏内邮件';

CREATE TABLE IF NOT EXISTS admin_activity (
    id int unsigned PRIMARY KEY auto_increment,
    user_id varchar(100) comment '生成者账号',
    activity_title varchar(500) comment '活动页签角标图片',
    activity_content varchar(1000) comment '活动规则描述',
    picture_url varchar(500) comment '活动内容图片',
    tab1_url varchar(500) comment '活动页签图片1',
    tab2_url varchar(500) comment '活动页签图片2',
    begin_time int unsigned comment '开始日期',
    end_time int unsigned comment '结束日期',
    entry_fee int unsigned comment '报名费',
    priority int unsigned comment '优先级',
    activity_type int unsigned comment '活动类型',
    status tinyint comment '状态',
    UNIQUE KEY id (id) USING BTREE,
    KEY activity_content (activity_content) USING BTREE,
    KEY user_id (user_id) USING BTREE,
    KEY begin_time (begin_time) USING BTREE,
    KEY end_time (end_time) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='活动系统';

CREATE TABLE IF NOT EXISTS admin_member_level (
    id int unsigned PRIMARY KEY auto_increment,
    member_level_name varchar(20) comment '玩家层级名称',
    number_withdrawals tinyint comment '提款次数',
    over_operation_id tinyint comment '超过次数后续操作id',
    fee_charging int unsigned comment '收取费用',
    min_withdrawals int unsigned comment '最小提款',
    max_withdrawals int unsigned comment '最大提款',
    inspect_id tinyint comment '稽查类型id',
    inspect_tips varchar(100) comment '稽查提示文字',
    channel_id int unsigned comment '渠道id',
    is_delete tinyint DEFAULT '0' comment '逻辑删除',
    KEY member_level_name (member_level_name) USING BTREE,
    KEY is_delete (is_delete) USING BTREE,
    KEY channel_id (channel_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='玩家层级';

CREATE TABLE IF NOT EXISTS admin_wx_agent (
    id int unsigned PRIMARY KEY auto_increment,
    wx varchar(50) comment '微信号',
    seq int comment '顺序号',
    status tinyint comment '状态',
    channel int unsigned comment '渠道',
    memo varchar(100) comment '备注',
    UNIQUE KEY id (id) USING BTREE,
    KEY wx (wx) USING BTREE,
    KEY channel (channel) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微信代理';

CREATE TABLE IF NOT EXISTS admin_pay_channel (
    id int unsigned PRIMARY KEY auto_increment,
    channel int unsigned comment '渠道',
    name varchar(50) comment '通道名字',
    player_lv varchar(100) comment '匹配玩家等级',
    min_recharge int comment '最小充值',
    max_recharge int comment '最大充值',
    pay_type int comment '支付方式 0银行卡转账  1支付宝支付  2微信支付 3qq支付',
    receipt_type int comment '收款方式 0银行卡收款  1支付宝二维码 2支付宝账号 3微信二维码 4qq二维码',
    config varchar(300) comment '收款方式详情 json格式 ',
    status tinyint comment '状态',
    decimal_open tinyint comment '小数点开启',
    memo varchar(100) comment '备注',
    UNIQUE KEY id (id) USING BTREE,
    KEY player_lv (player_lv) USING BTREE,
    KEY channel (channel) USING BTREE
) ENGINE=InnoDB auto_increment=80000000 DEFAULT CHARSET=utf8 COMMENT='支付通道';

CREATE TABLE IF NOT EXISTS admin_online_payment (
    id int unsigned PRIMARY KEY auto_increment,
    channel_id int unsigned comment '渠道id',
    pay_type tinyint comment '支付类型',
    api_name varchar(50) comment '接口名称',
    api_id varchar(50) comment '接口ID',
    api_url varchar(1000) comment '接口域名',
    api_code varchar(50) comment '接口代码',
    merchant_code varchar(1000) comment '商户号',
    md5_key varchar(1000) comment 'MD5 KEY',
    public_key varchar(5000) comment '公钥',
    private_key varchar(5000) comment '私钥',
    single_minimum int unsigned comment '单笔最低',
    single_highest int unsigned comment '单笔最高',
    stop_using_limit int unsigned comment '单日停用上限',
    status tinyint comment '状态',
    apply_level varchar(1000) comment '使用层级',
    KEY channel_id (channel_id) USING BTREE,
    KEY pay_type (pay_type) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='在线支付';

CREATE TABLE IF NOT EXISTS admin_platform (
    game_function_id int PRIMARY KEY comment '游戏和功能id',
    status tinyint comment '状态',
    sort int unsigned comment '排序'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏平台管理';

CREATE TABLE IF NOT EXISTS admin_ip_black_white_list (
    id int unsigned PRIMARY KEY auto_increment,
    type tinyint comment '黑名单（1）还是白名单（2）',
    country_area_ip varchar(500) comment '国家/地区/IP',
    channel_id int unsigned comment '渠道id',
    remark varchar(100) COMMENT '备注',
    KEY type (type) USING BTREE,
    KEY channel_id (channel_id) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='IP黑白名单';

CREATE TABLE IF NOT EXISTS admin_recharge_discounts (
    id int unsigned PRIMARY KEY auto_increment,
    user_id varchar(100) comment '生成者账号',
    priority int unsigned comment '优先级',
    activity_title varchar(500) comment '活动页签角标图片',
    activity_content varchar(1000) comment '活动规则描述',
    activity_type int comment '活动类型',
    participation_member tinyint comment '参与玩家',
    show_picture_url varchar(500) comment '活动内容图片',
    tab1_url varchar(500) comment '活动页签图片1',
    tab2_url varchar(500) comment '活动页签图片2',
    begin_time int unsigned comment '开始时间',
    end_time int unsigned comment '结束时间',
    participation_level varchar(500) comment '参与层级',
    recharge_detail varchar(1000) comment '充值详情',
    request_times int unsigned default 1 comment '申请次数',
    max_add_recharge int unsigned comment '最大赠送金额',
    journal_require int unsigned comment '流水要求',
    status tinyint unsigned comment '状态',
    KEY begin_time (begin_time) USING BTREE,
    KEY end_time (end_time) USING BTREE,
    KEY user_id (user_id) USING BTREE,
    KEY activity_content (activity_content) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='充值优惠';

CREATE TABLE IF NOT EXISTS admin_agent_level (
    id int unsigned PRIMARY KEY auto_increment,
    level_name varchar(50) comment '代理层级名称',
    grant_brokerage tinyint comment '是否发放佣金',
    first_ladder varchar(3000) comment '第一阶梯',
    second_ladder varchar(3000) comment '第二阶梯',
    third_ladder varchar(3000) comment '第三阶梯',
    fourth_ladder varchar(3000) comment '第四阶梯',
    fifth_ladder varchar(3000) comment '第五阶梯'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='代理层级';

CREATE TABLE IF NOT EXISTS admin_agent_list (
    pid int unsigned PRIMARY KEY comment '代理玩家id',
    agent_level int unsigned comment '代理层级',
    status tinyint comment '状态',
    pre_pid int unsigned comment '上级代理',
    KEY pid (pid) USING BTREE,
    KEY agent_level (agent_level) USING BTREE,
    KEY pre_pid (pre_pid) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='代理列表';

CREATE TABLE IF NOT EXISTS admin_black_list(
    `pid` bigint(20) unsigned NOT NULL COMMENT '用户ID',
    `game_count` int(5) not null COMMENT '游戏局数',
    `coin` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '金币',
    `counter`  bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '保险柜金币',
    `total_recharge_rmb` bigint(22) NOT NULL DEFAULT '0' COMMENT '累计充值RMB数量(分)',
    `total_withdraw`  bigint DEFAULT 0 COMMENT '总共提现',
    `remark` varchar(100) COMMENT '备注'
);

CREATE TABLE IF NOT EXISTS admin_white_list(
    `pid` bigint(20) unsigned NOT NULL COMMENT '用户ID',
    `game_count` int(5) not null COMMENT '游戏局数',
    `coin` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '金币',
    `counter`  bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '保险柜金币',
    `total_recharge_rmb` bigint(22) NOT NULL DEFAULT '0' COMMENT '累计充值RMB数量(分)',
    `total_withdraw` bigint DEFAULT 0 COMMENT '总共提现',
    `remark` varchar(100) COMMENT '备注'
);

CREATE TABLE IF NOT EXISTS admin_distribution_config (
    id int unsigned PRIMARY KEY auto_increment,
    pump_section varchar(1000) default "" comment "税收系数",
    commission_section varchar(1000) default "" comment "佣金系数"
);

CREATE TABLE IF NOT EXISTS admin_system_parameter (
    name varchar(100) PRIMARY KEY comment "参数名字",
    val varchar(1000) comment "参数值"
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统参数';

CREATE TABLE IF NOT EXISTS  admin_agent_settlement (
    pid int unsigned comment "代理id",
    date1 int unsigned comment "结算开始日期",
    date2 int unsigned comment "结算结束日期",
    count int unsigned comment "会员数",
    pump_commission int comment "抽水佣金",
    win_commission int comment "押注佣金",
    fee int unsigned comment "手续费",
    other_fee int unsigned comment "其他费用",
    type int unsigned comment "1 发放到银行卡  2发放到钱包  3累计到下一期",
    memo varchar(300) comment "备注",
    KEY pid (pid) USING BTREE,
    KEY date1 (date1) USING BTREE,
    KEY date2 (date2) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='代理结算';

CREATE TABLE IF NOT EXISTS  admin_distribution_settlement (
    pid int unsigned comment "代理id",
    date1 int unsigned comment "结算开始日期",
    date2 int unsigned comment "结算结束日期",
    count int unsigned comment "会员数",
    pump_commission int comment "抽水佣金",
    win_commission int comment "押注佣金",
    fee int unsigned comment "手续费",
    other_fee int unsigned comment "其他费用",
    type int unsigned comment "1 发放到银行卡  2发放到钱包  3累计到下一期",
    memo varchar(300) comment "备注",
    KEY pid (pid) USING BTREE,
    KEY date1 (date1) USING BTREE,
    KEY date2 (date2) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='分销结算';

CREATE TABLE IF NOT EXISTS admin_game_alarm_config (
    id int unsigned PRIMARY KEY comment "id",
    config varchar(1000) default "" comment "配置"
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏告警配置';


CREATE TABLE IF NOT EXISTS admin_game_alarm (
    id int unsigned PRIMARY KEY comment "编号" auto_increment,
    pid varchar(100) comment "玩家ID/IP/设备号",
    time int unsigned comment "时间戳",
    stype int unsigned comment "告警类型",
    val varchar(300) default "" comment "配置",
    state int unsigned comment "状态 0待处理 1已处理",
    relate_id int unsigned comment "关联ID",
    KEY pid (pid) USING BTREE,
    KEY time (time) USING BTREE,
    KEY stype (stype) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏告警';
