-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: zs_backend_develop
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `user_id` int(10) unsigned NOT NULL COMMENT '生成者账号id',
  `activity_title` varchar(100) DEFAULT NULL COMMENT '活动标题图片链接',
  `activity_content` varchar(5000) DEFAULT NULL COMMENT '活动描述',
  `activity_award` varchar(1000) DEFAULT NULL COMMENT '活动奖励',
  `picture_url` varchar(500) DEFAULT NULL COMMENT '活动描述图片链接',
  `begin_time` int(10) unsigned DEFAULT NULL COMMENT '开始日期',
  `end_time` int(10) unsigned DEFAULT NULL COMMENT '结束日期',
  `push_time_begin` int(10) unsigned DEFAULT NULL COMMENT '开始推送时间',
  `push_time_end` int(10) unsigned DEFAULT NULL COMMENT '结束推送时间',
  `entry_fee` int(10) unsigned DEFAULT NULL COMMENT '报名费',
  `feast_gold` int(10) unsigned DEFAULT NULL COMMENT '彩金盛宴金币',
  `push_times` tinyint(3) unsigned DEFAULT NULL COMMENT '每日推送次数',
  `priority` int(10) unsigned DEFAULT NULL COMMENT '优先级',
  `son_task_id` int(10) unsigned DEFAULT NULL COMMENT '子任务id',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `activity_title` (`activity_title`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `begin_time` (`begin_time`) USING BTREE,
  KEY `end_time` (`end_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='活动系统';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity`
--

LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (1,1,1,'标题','<p>描述<br/></p>','{10010001: 11, 20010001: 22}','',1533177977,1533955579,1534473981,1535165182,NULL,NULL,3,23,0,2),(2,1,1,'','<p>时间节点发</p>','{10010001: \"100000\", }','',1533833723,1535820926,1534524930,1535216131,NULL,NULL,19,2,0,2),(3,7,1,'biaoti1','<p>dawawd</p>','{10010001: 12, 20010001: 123}','e',1538609647,1538868850,1538609654,1539387255,11,12,1,23,12,3);
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agent_distribution_config`
--

DROP TABLE IF EXISTS `agent_distribution_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent_distribution_config` (
  `channel` int(10) unsigned NOT NULL COMMENT '渠道',
  `pump_section` varchar(1000) DEFAULT '' COMMENT '税收系数',
  `commission_section` varchar(1000) DEFAULT '' COMMENT '佣金系数',
  PRIMARY KEY (`channel`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent_distribution_config`
--

LOCK TABLES `agent_distribution_config` WRITE;
/*!40000 ALTER TABLE `agent_distribution_config` DISABLE KEYS */;
INSERT INTO `agent_distribution_config` VALUES (1,'{\"2-3\": 4, \"1-2\": 1, \"11-22\": 3}','[55, 2, 3, 4]');
/*!40000 ALTER TABLE `agent_distribution_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agent_level`
--

DROP TABLE IF EXISTS `agent_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent_level` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `level_name` varchar(50) DEFAULT NULL COMMENT '代理层级名称',
  `grant_brokerage` tinyint(4) DEFAULT NULL COMMENT '是否发放佣金',
  `first_ladder` varchar(3000) DEFAULT NULL COMMENT '第一阶梯',
  `second_ladder` varchar(3000) DEFAULT NULL COMMENT '第二阶梯',
  `third_ladder` varchar(3000) DEFAULT NULL COMMENT '第三阶梯',
  `fourth_ladder` varchar(3000) DEFAULT NULL COMMENT '第四阶梯',
  `fifth_ladder` varchar(3000) DEFAULT NULL COMMENT '第五阶梯',
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8 COMMENT='代理层级';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent_level`
--

LOCK TABLES `agent_level` WRITE;
/*!40000 ALTER TABLE `agent_level` DISABLE KEYS */;
INSERT INTO `agent_level` VALUES (24,1,'默认层级',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(25,1,'test2',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(26,7,'本级代理',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(27,7,'一级代理',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(28,7,'二级代理',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(29,7,'三级代理',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}'),(30,1,'test1',1,'{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}','{\"win_lose\":\"0\",\"bet\":\"0\",\"detail\":[{\"id\":\"96\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"97\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"98\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"99\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"80\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"81\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"82\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"83\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"84\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"85\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"86\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"87\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"88\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"90\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"91\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"92\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"93\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"94\",\"rebate\":\"0\",\"backwater\":\"0\"},{\"id\":\"95\",\"rebate\":\"0\",\"backwater\":\"0\"}]}');
/*!40000 ALTER TABLE `agent_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agent_list`
--

DROP TABLE IF EXISTS `agent_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agent_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `pid` int(10) unsigned DEFAULT NULL COMMENT '代理玩家id',
  `agent_level` int(10) unsigned DEFAULT NULL COMMENT '代理层级',
  `nick` varchar(20) DEFAULT NULL COMMENT '玩家昵称',
  `name` varchar(10) DEFAULT NULL COMMENT '玩家姓名',
  `coin_bank` varchar(50) DEFAULT NULL COMMENT '携带金币与保险柜金币',
  `register_time` int(10) unsigned DEFAULT NULL COMMENT '注册时间',
  `login_time` int(10) unsigned DEFAULT NULL COMMENT '登录时间',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `nick` (`nick`) USING BTREE,
  KEY `pid` (`pid`) USING BTREE,
  KEY `agent_level` (`agent_level`) USING BTREE,
  KEY `name` (`name`) USING BTREE,
  KEY `register_time` (`register_time`) USING BTREE,
  KEY `login_time` (`login_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='代理列表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agent_list`
--

LOCK TABLES `agent_list` WRITE;
/*!40000 ALTER TABLE `agent_list` DISABLE KEYS */;
INSERT INTO `agent_list` VALUES (5,1,90001,24,'孤独、','','null',1532712068,1532749386,2),(9,1,1000001,24,'导演','','1.00000212259e+11',1532606681,1538022191,2),(11,1,1025925,24,'＆鱼雷77','','null',1537953042,1538012629,2),(12,1,1025939,24,'、偏执','','null',1538100468,1538103795,2);
/*!40000 ALTER TABLE `agent_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backend_agent`
--

DROP TABLE IF EXISTS `backend_agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backend_agent` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `agent_id` bigint(20) unsigned NOT NULL COMMENT '代理ID',
  `channel` varchar(20) NOT NULL DEFAULT '' COMMENT '渠道名称',
  `duty` varchar(20) NOT NULL DEFAULT '' COMMENT '代理职务',
  `is_active` tinyint(5) NOT NULL DEFAULT '1' COMMENT '代理状态',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backend_agent`
--

LOCK TABLES `backend_agent` WRITE;
/*!40000 ALTER TABLE `backend_agent` DISABLE KEYS */;
INSERT INTO `backend_agent` VALUES (3,1000001,'1','5',1),(4,1000002,'1','x',1),(5,1000180,'1','1',0),(6,90001,'1','11',0);
/*!40000 ALTER TABLE `backend_agent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `black_list`
--

DROP TABLE IF EXISTS `black_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `black_list` (
  `pid` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `channel` varchar(20) NOT NULL DEFAULT '' COMMENT '渠道',
  `nick` varchar(50) NOT NULL DEFAULT '' COMMENT '玩家名',
  `game_count` int(5) NOT NULL COMMENT '游戏局数',
  `coin` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '金币',
  `counter` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '保险柜金币',
  `total_recharge_rmb` bigint(22) NOT NULL DEFAULT '0' COMMENT '累计充值RMB数量(分)',
  `total_withdraw` bigint(20) DEFAULT '0' COMMENT '总共提现',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `black_list`
--

LOCK TABLES `black_list` WRITE;
/*!40000 ALTER TABLE `black_list` DISABLE KEYS */;
INSERT INTO `black_list` VALUES (90001,'1','孤独、',0,0,0,0,0,'多久啊我不急啊'),(90001,'1','孤独、',0,0,0,0,0,'而神秘访客'),(90001,'1','孤独、',0,0,0,0,0,'而神秘访客'),(90001,'1','孤独、',0,0,0,0,0,'人坦克流看'),(90001,'1','孤独、',0,0,0,0,0,'发神经'),(1000008,'1','^乔木',0,0,310436,0,397,'11'),(1000008,'1','^乔木',0,0,310436,0,397,'1'),(1000008,'1','^乔木',0,0,310436,0,397,'1'),(1000008,'1','^乔木',0,0,310436,0,397,'1'),(1000001,'1','导演',0,0,202621,16082816,2,''),(1000001,'1','导演',0,0,202621,16082816,2,'');
/*!40000 ALTER TABLE `black_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `game_log_db` varchar(150) NOT NULL,
  `web_url` varchar(150) NOT NULL,
  `other_msg` blob COMMENT '渠道其他信息',
  `role_str` varchar(100) NOT NULL,
  `is_delete` tinyint(5) DEFAULT '0' COMMENT '渠道是否被删除',
  `status` tinyint(5) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
INSERT INTO `channel` VALUES (1,'小周专版','host=192.168.0.11,user=root,passwd=123456,db=server_juhao','http://192.168.0.101:8000/','{\"coin_rate\": \"100\", \"h5_wx_appid\": \"\", \"sms_type\": \"1\", \"h5_wx_token\": \"\", \"h5_api_key\": \"\", \"h5_link\": \"https://1234.com/juhao\", \"wx_appid\": \"\", \"api\": \"http://192.168.0.101:8000/\", \"wx_token\": \"\", \"sms_config\": \"\", \"hotup_url\": \"1\"}','1/2',0,1),(24,'guiyang_gongban_114','host=192.168.0.114,user=root,passwd=123456,db=server_9000','host=192.168.0.114,user=root,passwd=123456,db=server_9000','{\"coin_rate\": \"1\", \"h5_wx_appid\": \"\", \"h5_wx_token\": \"\", \"h5_api_key\": \"1\", \"h5_link\": \"host=192.168.0.114,user=root,passwd=123456,db=server_9000\", \"wx_appid\": \"\", \"api\": \"1\", \"wx_token\": \"\"}','1/2/5',0,1),(8,'0_11','host=192.168.0.127,user=root,passwd=123456,db=server_1','http://192.168.0.127:8080/','{\"coin_rate\": \"100\", \"h5_link\": \"https://1234.com/juhao\"}','1/2',1,1),(7,'juhao','host=192.168.0.11, user=root, passwd=123456, db=server_gongban','http://192.168.0.11:8001/','{\"coin_rate\": \"10000\", \"h5_wx_appid\": \"\", \"h5_wx_token\": \"\", \"h5_api_key\": \"\", \"h5_link\": \"https://1234.com/juhao\", \"wx_appid\": \"\", \"api\": \"0\", \"wx_token\": \"\"}','1',0,1),(10,'37','host=192.168.0.126,user=root,passwd=123456,db=server_1','http://192.168.0.126:8080/','{\"coin_rate\": \"100\", \"h5_link\": \"https://1234.com/juhao\"}','1/7',0,1),(14,'4399','host=192.168.0.126,user=root,passwd=123456,db=server_1','http://192.168.0.11:8080/','{\"h5_link\": \"<a href=https://1234.com/juhao target=\\\"_blank\\\">https://1234.com/juhao\", \"coin_rate\": 100} ','1/2',1,1),(15,'test','大萨达所大声道a            ','http://192.168.0.11:8080/','{\"h5_link\": \"<a href=https://1234.com/juhao target=\\\"_blank\\\">https://1234.com/juhao\", \"coin_rate\": 100} ','1',1,1),(16,'121232','232123123 ','http://192.168.0.11:8080/','{\"coin_rate\": \"100\", \"h5_link\": \"https://1234.com/juhao\"}','1/2',1,1),(17,'321','{\"h5_link\": \"<a href=https://1234.com/juhao target=\"_blank\">https://1234.com/juhao\", \"coin_rate\": 100} ','http://192.168.0.126:8080/','{\"coin_rate\": \"100\", \"h5_link\": \"weqeqe\"}','1',0,1),(25,'shuhui_gongban','host=192.168.0.101,user=root,passwd=123456,db=server_gongban','http://192.168.0.101:8000','{\"coin_rate\": \"1:10000\", \"h5_wx_appid\": \"\", \"h5_wx_token\": \"\", \"h5_api_key\": \"\", \"h5_link\": \"\", \"wx_appid\": \"\", \"api\": \"11\", \"wx_token\": \"\"}','1/2/5/6/7/8',1,1),(26,'1','2','1','{\"coin_rate\": \"1\", \"h5_wx_appid\": \"1\", \"h5_wx_token\": \"1\", \"h5_api_key\": \"1\", \"h5_link\": \"1\", \"wx_appid\": \"1\", \"api\": \"1\", \"wx_token\": \"1\"}','1',1,1),(27,'聚豪','host=192.168.0.11,user=root,passwd=123456,db=server_juhao	','http://192.168.0.11:8001/','{\"coin_rate\": \"1:1\", \"h5_wx_appid\": \"\", \"h5_wx_token\": \"\", \"h5_api_key\": \"\", \"h5_link\": \"\", \"wx_appid\": \"\", \"api\": \"1\", \"wx_token\": \"\"}','1',0,1),(28,'tt','123456','123456',NULL,'',0,1);
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_announcement`
--

DROP TABLE IF EXISTS `game_announcement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_announcement` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `channel` bigint(20) unsigned NOT NULL COMMENT '渠道ID',
  `priority` bigint(20) NOT NULL COMMENT '优先级',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '公告标题',
  `content_image_url` varchar(1000) NOT NULL DEFAULT '' COMMENT '内容图片链接',
  `title_image_url` varchar(20) NOT NULL DEFAULT '' COMMENT '标题图片链接',
  `push_times` varchar(20) NOT NULL DEFAULT '' COMMENT '每日推送次数',
  `start_date` int(30) NOT NULL COMMENT '开始日期',
  `end_date` int(30) NOT NULL COMMENT '结束日期',
  `status` tinyint(5) NOT NULL DEFAULT '1' COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `title` (`title`) USING BTREE,
  KEY `channel` (`channel`) USING BTREE
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='游戏内报告';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_announcement`
--

LOCK TABLES `game_announcement` WRITE;
/*!40000 ALTER TABLE `game_announcement` DISABLE KEYS */;
INSERT INTO `game_announcement` VALUES (1,1,2,'大叔大婶','阿萨德asd','阿萨大声道','1',1533042167,1535547769,1),(2,1,2,'大多数','大多数阿萨德','阿萨德大傻d','2',1534856631,1533647032,1),(3,1,1,'于洋洋','1','1','3',1533074621,1535148223,1),(4,1,1,'1','1','11','1',1534889040,1535148242,1);
/*!40000 ALTER TABLE `game_announcement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_parameter`
--

DROP TABLE IF EXISTS `game_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_parameter` (
  `type` int(10) unsigned NOT NULL COMMENT '类型ID',
  `config` text COMMENT '参数设置',
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏参数设置';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_parameter`
--

LOCK TABLES `game_parameter` WRITE;
/*!40000 ALTER TABLE `game_parameter` DISABLE KEYS */;
INSERT INTO `game_parameter` VALUES (1,'[{\"id\":\"11000\",\"name\":\"领取救济金\"},{\"id\":\"11001\",\"name\":\"金库存取\"},{\"id\":\"11002\",\"name\":\"周卡初次获得\"},{\"id\":\"11003\",\"name\":\"周卡每日领取获得\"},{\"id\":\"11004\",\"name\":\"玩家经验\"},{\"id\":\"11005\",\"name\":\"ios充值\"},{\"id\":\"11006\",\"name\":\"转账进来\"},{\"id\":\"11007\",\"name\":\"转账出去\"},{\"id\":\"12000\",\"name\":\"使用物品\"},{\"id\":\"12001\",\"name\":\"赠送物品\"},{\"id\":\"12003\",\"name\":\"砍掉物品（例如寄售到交易行）\"},{\"id\":\"12004\",\"name\":\"GM\"},{\"id\":\"13000\",\"name\":\"邮件领取附件\"},{\"id\":\"14000\",\"name\":\"金库存款\"},{\"id\":\"14001\",\"name\":\"金库取款\"},{\"id\":\"14002\",\"name\":\"赠送金币\"},{\"id\":\"15000\",\"name\":\"活动奖励\"},{\"id\":\"15001\",\"name\":\"瓜分现金押注\"},{\"id\":\"15002\",\"name\":\"兑换码获得物品\"},{\"id\":\"15003\",\"name\":\"新用户进入游戏后获得赠送金币\"},{\"id\":\"22000\",\"name\":\"gm加钱\"},{\"id\":\"80000\",\"name\":\"结算\"},{\"id\":\"80001\",\"name\":\"押注\"},{\"id\":\"81000\",\"name\":\"百人牛牛结算\"},{\"id\":\"81001\",\"name\":\"百人牛押注\"},{\"id\":\"82000\",\"name\":\"9线水果机下注\"},{\"id\":\"82001\",\"name\":\"赢分\"},{\"id\":\"83000\",\"name\":\"水浒传下注\"},{\"id\":\"83001\",\"name\":\"水浒传赢分\"},{\"id\":\"84000\",\"name\":\"德州押注\"},{\"id\":\"84001\",\"name\":\"德州赢钱\"},{\"id\":\"85000\",\"name\":\"结算\"},{\"id\":\"85001\",\"name\":\"押注\"},{\"id\":\"85002\",\"name\":\"取消押注\"},{\"id\":\"86000\",\"name\":\"结算\"},{\"id\":\"86001\",\"name\":\"押注\"},{\"id\":\"87000\",\"name\":\"吃鸡老虎机下注\"},{\"id\":\"87001\",\"name\":\"吃鸡老虎机赢分\"},{\"id\":\"88000\",\"name\":\"结算\"},{\"id\":\"88001\",\"name\":\"寻宝\"},{\"id\":\"90000\",\"name\":\"押注\"},{\"id\":\"90001\",\"name\":\"赢钱\"},{\"id\":\"90002\",\"name\":\"抽水\"},{\"id\":\"90003\",\"name\":\"底注\"},{\"id\":\"90004\",\"name\":\"输钱\"},{\"id\":\"92000\",\"name\":\"押注\"},{\"id\":\"92001\",\"name\":\"比牌\"},{\"id\":\"92002\",\"name\":\"allin下注\"},{\"id\":\"92003\",\"name\":\"底注\"},{\"id\":\"92004\",\"name\":\"孤注一掷返还\"},{\"id\":\"92005\",\"name\":\"赢钱\"},{\"id\":\"92006\",\"name\":\"抽水\"},{\"id\":\"93000\",\"name\":\"子弹返还\"},{\"id\":\"93001\",\"name\":\"开炮消耗\"},{\"id\":\"93002\",\"name\":\"鱼死亡，掉落\"},{\"id\":\"94000\",\"name\":\"三国老虎机下注\"},{\"id\":\"94001\",\"name\":\"三国老虎机赢分\"},{\"id\":\"94002\",\"name\":\"三国老虎机草船借箭小游戏赢分\"},{\"id\":\"95000\",\"name\":\"经典走灯水果机下注\"},{\"id\":\"95001\",\"name\":\"经典走灯水果机赢分\"},{\"id\":\"95002\",\"name\":\"经典走灯水果机比大小下注\"},{\"id\":\"96000\",\"name\":\"传奇老虎机下注\"},{\"id\":\"96001\",\"name\":\"传奇老虎机赢分\"},{\"id\":\"97000\",\"name\":\"王者荣耀老虎机下注\"},{\"id\":\"97001\",\"name\":\"王者荣耀老虎机赢分\"},{\"id\":\"98000\",\"name\":\"极速金花下注\"},{\"id\":\"98001\",\"name\":\"极速金花结算\"},{\"id\":\"99000\",\"name\":\"金币结算\"},{\"id\":\"100000\",\"name\":\"金币结算\"},{\"id\":\"26731\",\"name\":\"满件大事\"}]'),(2,'[{\"desc\":\"红黑大战\",\"en_name\":\"game_redblack\",\"id\":80},{\"desc\":\"百人牛牛\",\"en_name\":\"game_hundred_niu\",\"id\":81},{\"desc\":\"九线水果机\",\"en_name\":\"game_jackpot\",\"id\":82},{\"desc\":\"水浒传\",\"en_name\":\"game_water_margin\",\"id\":83},{\"desc\":\"百人德州\",\"en_name\":\"game_hundred_texas\",\"id\":84},{\"desc\":\"森林舞会\",\"en_name\":\"game_forest\",\"id\":85},{\"desc\":\"龙虎斗\",\"en_name\":\"game_dragon\",\"id\":86},{\"desc\":\"绝地求生\",\"en_name\":\"game_pubg\",\"id\":87},{\"desc\":\"连环夺宝\",\"en_name\":\"game_treasure_hunt\",\"id\":88},{\"desc\":\"5人牛\",\"en_name\":\"game_nn_5\",\"id\":90},{\"desc\":\"2人牛\",\"en_name\":\"game_nn_2\",\"id\":91},{\"desc\":\"炸金花\",\"en_name\":\"game_jinhua\",\"id\":92},{\"desc\":\"金蟾捕鱼\",\"en_name\":\"game_by\",\"id\":93},{\"desc\":\"三国老虎机\",\"en_name\":\"game_three_countries\",\"id\":94},{\"desc\":\"经典水果机\",\"en_name\":\"game_classcal_fruit\",\"id\":95},{\"desc\":\"传奇老虎机\",\"en_name\":\"game_legend\",\"id\":96},{\"desc\":\"王者荣耀老虎机\",\"en_name\":\"game_king\",\"id\":97},{\"desc\":\"极速炸金花\",\"en_name\":\"game_jinhua_js\",\"id\":98},{\"desc\":\"二八杠\",\"en_name\":\"game_mahjong_28\",\"id\":99},{\"desc\":\"三公\",\"en_name\":\"game_sangong\",\"id\":100}]'),(3,'[{\"desc\":\"\",\"detail\":\"#coin#携带金币\",\"en_name\":\"\",\"gameid\":\"100\",\"id\":\"100\",\"name\":\"\"},{\"detail\":\"#coin#下注\",\"id\":\"101\"},{\"detail\":\"开奖id\",\"id\":\"102\"},{\"detail\":\"赠送次数\",\"id\":\"103\"},{\"detail\":\"压线数\",\"id\":\"104\"},{\"detail\":\"#coin#单注金额\",\"id\":\"105\"},{\"detail\":\"赠送次数\",\"id\":\"106\"},{\"detail\":\"总倍率\",\"id\":\"107\"},{\"detail\":\"#desc#免费状态#0:收费,1:免费\",\"id\":\"108\"},{\"detail\":\"#coin#结算\",\"id\":\"109\"},{\"detail\":\"#coin#jackpot结算\",\"id\":\"110\"},{\"detail\":\"#config#压中的线\",\"id\":\"111\"},{\"detail\":\"几连\",\"id\":\"112\"},{\"detail\":\"#config#压中的基础id\",\"id\":\"113\"},{\"detail\":\"#coin#本局输赢分\",\"id\":\"114\"},{\"detail\":\"#coin#本局抽水\",\"id\":\"115\"},{\"detail\":\"#coin#本局总产分\",\"id\":\"116\"},{\"detail\":\"#config#下注基础id\",\"id\":\"117\"},{\"detail\":\"下注数量\",\"id\":\"118\"},{\"detail\":\"#desc#奖励类型#0:正常,1:银lucky送灯,2:金lucky送灯,3:大三元,4:大四喜,5:大满贯\",\"id\":\"119\"},{\"detail\":\"#config#开牌情况[基础id...]\",\"id\":\"120\"},{\"detail\":\"#config#中奖基础id\",\"id\":\"121\"},{\"detail\":\"中奖数量\",\"id\":\"122\"},{\"detail\":\"#config#jackpot基础id\",\"id\":\"123\"},{\"detail\":\"jackpot当前数量\",\"id\":\"124\"},{\"detail\":\"#coin#走灯当前赢分\",\"id\":\"125\"},{\"detail\":\"#desc#买大小#1:小,2:大\",\"id\":\"126\"},{\"detail\":\"#desc#开出大小#1:小,2:大\",\"id\":\"127\"},{\"detail\":\"点数1\",\"id\":\"128\"},{\"detail\":\"点数2\",\"id\":\"129\"},{\"detail\":\"#coin#过关小游戏获得金币数\",\"id\":\"130\"},{\"detail\":\"打通关卡\",\"id\":\"131\"},{\"detail\":\"开奖位置\",\"id\":\"132\"},{\"detail\":\"开奖倍率\",\"id\":\"133\"},{\"detail\":\"第几次消除\",\"id\":\"134\"},{\"detail\":\"击杀人数\",\"id\":\"135\"},{\"detail\":\"瞄准镜位置\",\"id\":\"136\"},{\"detail\":\"#coin#大逃杀获得金币数\",\"id\":\"137\"},{\"detail\":\"大逃杀击杀人数\",\"id\":\"138\"},{\"detail\":\"大逃杀第几轮\",\"id\":\"139\"},{\"detail\":\"大逃杀剩余血量\",\"id\":\"140\"},{\"detail\":\"第几局大逃杀\",\"id\":\"141\"},{\"detail\":\"被反击次数\",\"id\":\"142\"},{\"detail\":\"掉血\",\"id\":\"143\"},{\"detail\":\"加血\",\"id\":\"144\"},{\"detail\":\"#coin#大逃杀本局抽水\",\"id\":\"145\"},{\"detail\":\"#coin#大逃杀本局总产分\",\"id\":\"146\"},{\"detail\":\"#coin#普通输赢分\",\"id\":\"147\"},{\"detail\":\"#coin#普通抽水\",\"id\":\"148\"},{\"detail\":\"#coin#普通总产分\",\"id\":\"149\"},{\"detail\":\"#coin#三国过关斩将赢分\",\"id\":\"150\"},{\"detail\":\"#coin#草船借箭最高可赢的分\",\"id\":\"151\"},{\"detail\":\"#coin#草船借箭输赢分\",\"id\":\"152\"},{\"detail\":\"#coin#草船借箭赢分抽水\",\"id\":\"153\"},{\"detail\":\"#coin#草船借箭总赢分\",\"id\":\"154\"},{\"detail\":\"#coin#连环夺宝身上积分\",\"id\":\"155\"},{\"detail\":\"连环夺宝钥匙数\",\"id\":\"156\"},{\"detail\":\"#config#消除列表(消除id)\",\"id\":\"157\"},{\"detail\":\"消除列表(消除数量)\",\"id\":\"158\"},{\"detail\":\"#coin#消除列表(获得金币)\",\"id\":\"159\"},{\"detail\":\"#coin#携带积分\",\"id\":\"160\"},{\"detail\":\"#coin#连环夺宝赢得的积分\",\"id\":\"161\"},{\"detail\":\"#coin#连环夺宝bouns赢得的积分\",\"id\":\"162\"},{\"detail\":\"连环夺宝获得钥匙数量\",\"id\":\"163\"},{\"detail\":\"#coin#连环夺宝龙珠夺宝输赢分\",\"id\":\"164\"},{\"detail\":\"#coin#连环夺宝龙珠夺宝获得金币抽水\",\"id\":\"165\"},{\"detail\":\"#coin#连环夺宝龙珠夺宝产出总分\",\"id\":\"166\"},{\"detail\":\"#coin#龙珠夺宝箱子产出分\",\"id\":\"167\"},{\"detail\":\"龙珠夺宝箱子产出概率\",\"id\":\"168\"},{\"detail\":\"#desc#水浒传奖励类型#3:3连,4:4连,5:5连线,6:全盘武器,7:全盘人物,8:全盘一致\",\"id\":\"169\"},{\"detail\":\"水浒传小玛丽次数\",\"id\":\"170\"},{\"detail\":\"#coin#水浒传小玛丽获得金币\",\"id\":\"171\"},{\"detail\":\"#config#水浒传小玛丽外圈位置\",\"id\":\"172\"},{\"detail\":\"#config#水浒传小玛丽内圈信息\",\"id\":\"173\"},{\"detail\":\"#coin#水浒传小玛丽获得金币\",\"id\":\"174\"},{\"detail\":\"水浒传摇色子获得倍率\",\"id\":\"175\"},{\"detail\":\"#pid#玩家id\",\"id\":\"176\"},{\"detail\":\"#coin#总下注\",\"id\":\"177\"},{\"detail\":\"弃牌\",\"id\":\"178\"},{\"detail\":\"#coin#下底注\",\"id\":\"179\"},{\"detail\":\"#pid#庄家id\",\"id\":\"180\"},{\"detail\":\"第几轮\",\"id\":\"181\"},{\"detail\":\"看牌\",\"id\":\"182\"},{\"detail\":\"#config#牌信息\",\"id\":\"183\"},{\"detail\":\"亮牌\",\"id\":\"184\"},{\"detail\":\"比牌\",\"id\":\"185\"},{\"detail\":\"比牌结果是否赢\",\"id\":\"186\"},{\"detail\":\"#coin#比牌金币\",\"id\":\"187\"},{\"detail\":\"#coin#金花孤注一掷\",\"id\":\"188\"},{\"detail\":\"#coin#allin金币\",\"id\":\"189\"},{\"detail\":\"#coin#赢分\",\"id\":\"190\"},{\"detail\":\"是否赢\",\"id\":\"191\"},{\"detail\":\"位置\",\"id\":\"192\"},{\"detail\":\"抢庄\",\"id\":\"193\"},{\"detail\":\"被踢\",\"id\":\"194\"},{\"detail\":\"开始游戏\",\"id\":\"195\"},{\"detail\":\"抢庄倍率\",\"id\":\"196\"},{\"detail\":\"是否庄家\",\"id\":\"197\"},{\"detail\":\"是否准备\",\"id\":\"198\"},{\"detail\":\"#desc#龙虎下注区域#1:龙,2:虎,3:和,4:龙黑,5:龙红,6:龙梅,7:龙方,8:虎黑,9:虎红,10:虎梅,11:虎方\",\"id\":\"199\"},{\"detail\":\"#coin#龙虎下注金币\",\"id\":\"200\"},{\"detail\":\"龙虎坐下\",\"id\":\"201\"},{\"detail\":\"龙虎坐起来\",\"id\":\"202\"},{\"detail\":\"#desc#龙虎产出区域#1:龙,2:虎,3:和,4:龙黑,5:龙红,6:龙梅,7:龙方,8:虎黑,9:虎红,10:虎梅,11:虎方\",\"id\":\"203\"},{\"detail\":\"#coin#区域输赢分\",\"id\":\"204\"},{\"detail\":\"#coin#区域抽水\",\"id\":\"205\"},{\"detail\":\"#coin#区域总产分\",\"id\":\"206\"},{\"detail\":\"#desc#龙虎中奖区域#1:龙,2:虎,3:和,4:龙黑,5:龙红,6:龙梅,7:龙方,8:虎黑,9:虎红,10:虎梅,11:虎方\",\"id\":\"207\"},{\"detail\":\"#config#龙牌\",\"id\":\"208\"},{\"detail\":\"#config#虎牌\",\"id\":\"209\"},{\"detail\":\"#config#森林舞会下注动物id\",\"id\":\"210\"},{\"detail\":\"#coin#森林舞会下注金币\",\"id\":\"211\"},{\"detail\":\"#coin#重置下注\",\"id\":\"212\"},{\"detail\":\"进入房间\",\"id\":\"213\"},{\"detail\":\"离开房间\",\"id\":\"214\"},{\"detail\":\"#desc#庄闲和#501:庄,601:闲,701:和\",\"id\":\"215\"},{\"detail\":\"#desc#开奖类型#1:大三元,2:大四喜,3:送灯,4:普通\",\"id\":\"216\"},{\"detail\":\"是否霹雳连环\",\"id\":\"217\"},{\"detail\":\"#coin#森林舞会输赢分\",\"id\":\"218\"},{\"detail\":\"#coin#森林舞会抽水\",\"id\":\"219\"},{\"detail\":\"#coin#森林舞会总产分\",\"id\":\"220\"},{\"detail\":\"#coin#森林舞会bonus产出金币\",\"id\":\"221\"},{\"detail\":\"#desc#百人牛下注区域#1:庄家,2:天,3:地,4:玄,5:黄\",\"id\":\"222\"},{\"detail\":\"#coin#下注金币\",\"id\":\"223\"},{\"detail\":\"#pid#坐下\",\"id\":\"224\"},{\"detail\":\"#pid#坐起来\",\"id\":\"225\"},{\"detail\":\"#pid#上庄\",\"id\":\"226\"},{\"detail\":\"#pid#等待上庄\",\"id\":\"227\"},{\"detail\":\"#pid#下庄\",\"id\":\"228\"},{\"detail\":\"#desc#区域#1:庄家,2:天,3:地,4:玄,5:黄\",\"id\":\"229\"},{\"detail\":\"#config#牌\",\"id\":\"230\"},{\"detail\":\"#desc#赢状态#1:赢,2:输\",\"id\":\"231\"},{\"detail\":\"#desc#牛类型#0:无牛,1:牛1,2:牛2,3:牛3,4:牛4,5:牛5,6:牛6,7:牛7,8:牛8,9:牛9,10:牛牛,11:5花牛,12:炸弹,13:5小牛\",\"id\":\"232\"},{\"detail\":\"#config#牛列表\",\"id\":\"233\"},{\"detail\":\"#config#下注区域\",\"id\":\"234\"},{\"detail\":\"#coin#下注金币\",\"id\":\"235\"},{\"detail\":\"#config#红黑红方牌型\",\"id\":\"236\"},{\"detail\":\"#config#红黑黑方牌型\",\"id\":\"237\"},{\"detail\":\"#config#红黑红方牌信息\",\"id\":\"238\"},{\"detail\":\"#config#红黑黑方牌信息\",\"id\":\"239\"},{\"detail\":\"#config#产出区域\",\"id\":\"240\"},{\"detail\":\"#config#中奖区域\",\"id\":\"241\"},{\"detail\":\"#config#赢的牌\",\"id\":\"242\"},{\"detail\":\"#config#公牌型\",\"id\":\"243\"},{\"detail\":\"#config#百人德州红方牌信息\",\"id\":\"244\"},{\"detail\":\"#config#百人德州蓝方牌信息\",\"id\":\"245\"},{\"detail\":\"#config#百人德州公牌信息\",\"id\":\"246\"},{\"detail\":\"是否赢\",\"id\":\"247\"},{\"detail\":\"#pid#玩家准备\",\"id\":\"248\"},{\"detail\":\"#config#牌类型\",\"id\":\"249\"},{\"detail\":\"抢庄倍数\",\"id\":\"250\"},{\"detail\":\"#desc#下注区域#1:蓝,2:红,3:和,4:一对,5:2对,6:顺子/3条,7:同花/葫芦,8:金刚/同花顺\",\"id\":\"251\"},{\"detail\":\"#coin#返还子弹金币\",\"id\":\"252\"},{\"detail\":\"#coin#子弹价格\",\"id\":\"253\"},{\"detail\":\"#coin#获得金币\",\"id\":\"254\"},{\"detail\":\"#coin#抽水\",\"id\":\"255\"},{\"detail\":\"#config#鱼类型ID\",\"id\":\"256\"},{\"detail\":\"倍率\",\"id\":\"257\"},{\"detail\":\"的反馈了计算机东方时空\",\"id\":\"21332\"}]'),(4,'[{\"detail\":\"方2\",\"gameid\":80,\"id\":21},{\"detail\":\"梅2\",\"gameid\":80,\"id\":22},{\"detail\":\"红2\",\"gameid\":80,\"id\":23},{\"detail\":\"黑2\",\"gameid\":80,\"id\":24},{\"detail\":\"方3\",\"gameid\":80,\"id\":31},{\"detail\":\"梅3\",\"gameid\":80,\"id\":32},{\"detail\":\"红3\",\"gameid\":80,\"id\":33},{\"detail\":\"黑3\",\"gameid\":80,\"id\":34},{\"detail\":\"方4\",\"gameid\":80,\"id\":41},{\"detail\":\"梅4\",\"gameid\":80,\"id\":42},{\"detail\":\"红4\",\"gameid\":80,\"id\":43},{\"detail\":\"黑4\",\"gameid\":80,\"id\":44},{\"detail\":\"方5\",\"gameid\":80,\"id\":51},{\"detail\":\"梅5\",\"gameid\":80,\"id\":52},{\"detail\":\"红5\",\"gameid\":80,\"id\":53},{\"detail\":\"黑5\",\"gameid\":80,\"id\":54},{\"detail\":\"方6\",\"gameid\":80,\"id\":61},{\"detail\":\"梅6\",\"gameid\":80,\"id\":62},{\"detail\":\"红6\",\"gameid\":80,\"id\":63},{\"detail\":\"黑6\",\"gameid\":80,\"id\":64},{\"detail\":\"方7\",\"gameid\":80,\"id\":71},{\"detail\":\"梅7\",\"gameid\":80,\"id\":72},{\"detail\":\"红7\",\"gameid\":80,\"id\":73},{\"detail\":\"黑7\",\"gameid\":80,\"id\":74},{\"detail\":\"方8\",\"gameid\":80,\"id\":81},{\"detail\":\"梅8\",\"gameid\":80,\"id\":82},{\"detail\":\"红8\",\"gameid\":80,\"id\":83},{\"detail\":\"黑8\",\"gameid\":80,\"id\":84},{\"detail\":\"方9\",\"gameid\":80,\"id\":91},{\"detail\":\"梅9\",\"gameid\":80,\"id\":92},{\"detail\":\"红9\",\"gameid\":80,\"id\":93},{\"detail\":\"黑9\",\"gameid\":80,\"id\":94},{\"detail\":\"方10\",\"gameid\":80,\"id\":101},{\"detail\":\"梅10\",\"gameid\":80,\"id\":102},{\"detail\":\"红10\",\"gameid\":80,\"id\":103},{\"detail\":\"黑10\",\"gameid\":80,\"id\":104},{\"detail\":\"方J\",\"gameid\":80,\"id\":111},{\"detail\":\"梅J\",\"gameid\":80,\"id\":112},{\"detail\":\"红J\",\"gameid\":80,\"id\":113},{\"detail\":\"黑J\",\"gameid\":80,\"id\":114},{\"detail\":\"方Q\",\"gameid\":80,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":80,\"id\":122},{\"detail\":\"红Q\",\"gameid\":80,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":80,\"id\":124},{\"detail\":\"方K\",\"gameid\":80,\"id\":131},{\"detail\":\"梅K\",\"gameid\":80,\"id\":132},{\"detail\":\"红K\",\"gameid\":80,\"id\":133},{\"detail\":\"黑K\",\"gameid\":80,\"id\":134},{\"detail\":\"方A\",\"gameid\":80,\"id\":141},{\"detail\":\"梅A\",\"gameid\":80,\"id\":142},{\"detail\":\"红A\",\"gameid\":80,\"id\":143},{\"detail\":\"黑A\",\"gameid\":80,\"id\":144},{\"detail\":\"方A\",\"gameid\":81,\"id\":11},{\"detail\":\"梅A\",\"gameid\":81,\"id\":12},{\"detail\":\"红A\",\"gameid\":81,\"id\":13},{\"detail\":\"黑A\",\"gameid\":81,\"id\":14},{\"detail\":\"方2\",\"gameid\":81,\"id\":21},{\"detail\":\"梅2\",\"gameid\":81,\"id\":22},{\"detail\":\"红2\",\"gameid\":81,\"id\":23},{\"detail\":\"黑2\",\"gameid\":81,\"id\":24},{\"detail\":\"方3\",\"gameid\":81,\"id\":31},{\"detail\":\"梅3\",\"gameid\":81,\"id\":32},{\"detail\":\"红3\",\"gameid\":81,\"id\":33},{\"detail\":\"黑3\",\"gameid\":81,\"id\":34},{\"detail\":\"方4\",\"gameid\":81,\"id\":41},{\"detail\":\"梅4\",\"gameid\":81,\"id\":42},{\"detail\":\"红4\",\"gameid\":81,\"id\":43},{\"detail\":\"黑4\",\"gameid\":81,\"id\":44},{\"detail\":\"方5\",\"gameid\":81,\"id\":51},{\"detail\":\"梅5\",\"gameid\":81,\"id\":52},{\"detail\":\"红5\",\"gameid\":81,\"id\":53},{\"detail\":\"黑5\",\"gameid\":81,\"id\":54},{\"detail\":\"方6\",\"gameid\":81,\"id\":61},{\"detail\":\"梅6\",\"gameid\":81,\"id\":62},{\"detail\":\"红6\",\"gameid\":81,\"id\":63},{\"detail\":\"黑6\",\"gameid\":81,\"id\":64},{\"detail\":\"方7\",\"gameid\":81,\"id\":71},{\"detail\":\"梅7\",\"gameid\":81,\"id\":72},{\"detail\":\"红7\",\"gameid\":81,\"id\":73},{\"detail\":\"黑7\",\"gameid\":81,\"id\":74},{\"detail\":\"方8\",\"gameid\":81,\"id\":81},{\"detail\":\"梅8\",\"gameid\":81,\"id\":82},{\"detail\":\"红8\",\"gameid\":81,\"id\":83},{\"detail\":\"黑8\",\"gameid\":81,\"id\":84},{\"detail\":\"方9\",\"gameid\":81,\"id\":91},{\"detail\":\"梅9\",\"gameid\":81,\"id\":92},{\"detail\":\"红9\",\"gameid\":81,\"id\":93},{\"detail\":\"黑9\",\"gameid\":81,\"id\":94},{\"detail\":\"方10\",\"gameid\":81,\"id\":101},{\"detail\":\"梅10\",\"gameid\":81,\"id\":102},{\"detail\":\"红10\",\"gameid\":81,\"id\":103},{\"detail\":\"黑10\",\"gameid\":81,\"id\":104},{\"detail\":\"方J\",\"gameid\":81,\"id\":111},{\"detail\":\"梅J\",\"gameid\":81,\"id\":112},{\"detail\":\"红J\",\"gameid\":81,\"id\":113},{\"detail\":\"黑J\",\"gameid\":81,\"id\":114},{\"detail\":\"方Q\",\"gameid\":81,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":81,\"id\":122},{\"detail\":\"红Q\",\"gameid\":81,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":81,\"id\":124},{\"detail\":\"方K\",\"gameid\":81,\"id\":131},{\"detail\":\"梅K\",\"gameid\":81,\"id\":132},{\"detail\":\"红K\",\"gameid\":81,\"id\":133},{\"detail\":\"黑K\",\"gameid\":81,\"id\":134},{\"detail\":\"橙子\",\"gameid\":82,\"id\":101},{\"detail\":\"葡萄\",\"gameid\":82,\"id\":102},{\"detail\":\"西瓜\",\"gameid\":82,\"id\":103},{\"detail\":\"苹果\",\"gameid\":82,\"id\":104},{\"detail\":\"柠檬\",\"gameid\":82,\"id\":105},{\"detail\":\"荔枝\",\"gameid\":82,\"id\":106},{\"detail\":\"樱桃\",\"gameid\":82,\"id\":107},{\"detail\":\"BAR\",\"gameid\":82,\"id\":108},{\"detail\":\"WILD（癞子）\",\"gameid\":82,\"id\":109},{\"detail\":\"SCATTER（777）\",\"gameid\":82,\"id\":110},{\"detail\":\"JACKPOT（四叶草）\",\"gameid\":82,\"id\":111},{\"detail\":\"铁斧\",\"gameid\":83,\"id\":101},{\"detail\":\"银枪\",\"gameid\":83,\"id\":102},{\"detail\":\"金刀\",\"gameid\":83,\"id\":103},{\"detail\":\"鲁智深\",\"gameid\":83,\"id\":104},{\"detail\":\"林冲\",\"gameid\":83,\"id\":105},{\"detail\":\"宋江\",\"gameid\":83,\"id\":106},{\"detail\":\"替天行道\",\"gameid\":83,\"id\":107},{\"detail\":\"忠义堂\",\"gameid\":83,\"id\":108},{\"detail\":\"水浒传\",\"gameid\":83,\"id\":109},{\"detail\":\"全盘武器\",\"gameid\":83,\"id\":110},{\"detail\":\"全盘人物\",\"gameid\":83,\"id\":111},{\"detail\":\"小玛丽内连线倍率\",\"gameid\":83,\"id\":112},{\"detail\":\"退出\",\"gameid\":83,\"id\":1},{\"detail\":\"鲁智深\",\"gameid\":83,\"id\":2},{\"detail\":\"银枪\",\"gameid\":83,\"id\":3},{\"detail\":\"忠义堂\",\"gameid\":83,\"id\":4},{\"detail\":\"铁斧\",\"gameid\":83,\"id\":5},{\"detail\":\"金刀\",\"gameid\":83,\"id\":6},{\"detail\":\"退出\",\"gameid\":83,\"id\":7},{\"detail\":\"宋江\",\"gameid\":83,\"id\":8},{\"detail\":\"鲁智深\",\"gameid\":83,\"id\":9},{\"detail\":\"银枪\",\"gameid\":83,\"id\":10},{\"detail\":\"铁斧\",\"gameid\":83,\"id\":11},{\"detail\":\"替天行道\",\"gameid\":83,\"id\":12},{\"detail\":\"退出\",\"gameid\":83,\"id\":13},{\"detail\":\"林冲\",\"gameid\":83,\"id\":14},{\"detail\":\"金刀\",\"gameid\":83,\"id\":15},{\"detail\":\"铁斧\",\"gameid\":83,\"id\":16},{\"detail\":\"鲁智深\",\"gameid\":83,\"id\":17},{\"detail\":\"宋江\",\"gameid\":83,\"id\":18},{\"detail\":\"退出\",\"gameid\":83,\"id\":19},{\"detail\":\"林冲\",\"gameid\":83,\"id\":20},{\"detail\":\"银枪\",\"gameid\":83,\"id\":21},{\"detail\":\"铁斧\",\"gameid\":83,\"id\":22},{\"detail\":\"金刀\",\"gameid\":83,\"id\":23},{\"detail\":\"替天行道\",\"gameid\":83,\"id\":24},{\"detail\":\"方2\",\"gameid\":84,\"id\":21},{\"detail\":\"梅2\",\"gameid\":84,\"id\":22},{\"detail\":\"红2\",\"gameid\":84,\"id\":23},{\"detail\":\"黑2\",\"gameid\":84,\"id\":24},{\"detail\":\"方3\",\"gameid\":84,\"id\":31},{\"detail\":\"梅3\",\"gameid\":84,\"id\":32},{\"detail\":\"红3\",\"gameid\":84,\"id\":33},{\"detail\":\"黑3\",\"gameid\":84,\"id\":34},{\"detail\":\"方4\",\"gameid\":84,\"id\":41},{\"detail\":\"梅4\",\"gameid\":84,\"id\":42},{\"detail\":\"红4\",\"gameid\":84,\"id\":43},{\"detail\":\"黑4\",\"gameid\":84,\"id\":44},{\"detail\":\"方5\",\"gameid\":84,\"id\":51},{\"detail\":\"梅5\",\"gameid\":84,\"id\":52},{\"detail\":\"红5\",\"gameid\":84,\"id\":53},{\"detail\":\"黑5\",\"gameid\":84,\"id\":54},{\"detail\":\"方6\",\"gameid\":84,\"id\":61},{\"detail\":\"梅6\",\"gameid\":84,\"id\":62},{\"detail\":\"红6\",\"gameid\":84,\"id\":63},{\"detail\":\"黑6\",\"gameid\":84,\"id\":64},{\"detail\":\"方7\",\"gameid\":84,\"id\":71},{\"detail\":\"梅7\",\"gameid\":84,\"id\":72},{\"detail\":\"红7\",\"gameid\":84,\"id\":73},{\"detail\":\"黑7\",\"gameid\":84,\"id\":74},{\"detail\":\"方8\",\"gameid\":84,\"id\":81},{\"detail\":\"梅8\",\"gameid\":84,\"id\":82},{\"detail\":\"红8\",\"gameid\":84,\"id\":83},{\"detail\":\"黑8\",\"gameid\":84,\"id\":84},{\"detail\":\"方9\",\"gameid\":84,\"id\":91},{\"detail\":\"梅9\",\"gameid\":84,\"id\":92},{\"detail\":\"红9\",\"gameid\":84,\"id\":93},{\"detail\":\"黑9\",\"gameid\":84,\"id\":94},{\"detail\":\"方10\",\"gameid\":84,\"id\":101},{\"detail\":\"梅10\",\"gameid\":84,\"id\":102},{\"detail\":\"红10\",\"gameid\":84,\"id\":103},{\"detail\":\"黑10\",\"gameid\":84,\"id\":104},{\"detail\":\"方J\",\"gameid\":84,\"id\":111},{\"detail\":\"梅J\",\"gameid\":84,\"id\":112},{\"detail\":\"红J\",\"gameid\":84,\"id\":113},{\"detail\":\"黑J\",\"gameid\":84,\"id\":114},{\"detail\":\"方Q\",\"gameid\":84,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":84,\"id\":122},{\"detail\":\"红Q\",\"gameid\":84,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":84,\"id\":124},{\"detail\":\"方K\",\"gameid\":84,\"id\":131},{\"detail\":\"梅K\",\"gameid\":84,\"id\":132},{\"detail\":\"红K\",\"gameid\":84,\"id\":133},{\"detail\":\"黑K\",\"gameid\":84,\"id\":134},{\"detail\":\"方A\",\"gameid\":84,\"id\":141},{\"detail\":\"梅A\",\"gameid\":84,\"id\":142},{\"detail\":\"红A\",\"gameid\":84,\"id\":143},{\"detail\":\"黑A\",\"gameid\":84,\"id\":144},{\"detail\":\"红狮子\",\"gameid\":85,\"id\":101},{\"detail\":\"绿狮子\",\"gameid\":85,\"id\":102},{\"detail\":\"黄狮子\",\"gameid\":85,\"id\":103},{\"detail\":\"红熊猫\",\"gameid\":85,\"id\":201},{\"detail\":\"绿熊猫\",\"gameid\":85,\"id\":202},{\"detail\":\"黄熊猫\",\"gameid\":85,\"id\":203},{\"detail\":\"红猴子\",\"gameid\":85,\"id\":301},{\"detail\":\"绿猴子\",\"gameid\":85,\"id\":302},{\"detail\":\"黄猴子\",\"gameid\":85,\"id\":303},{\"detail\":\"红兔子\",\"gameid\":85,\"id\":401},{\"detail\":\"绿兔子\",\"gameid\":85,\"id\":402},{\"detail\":\"黄兔子\",\"gameid\":85,\"id\":403},{\"detail\":\"庄\",\"gameid\":85,\"id\":501},{\"detail\":\"闲\",\"gameid\":85,\"id\":601},{\"detail\":\"和\",\"gameid\":85,\"id\":701},{\"detail\":\"方A\",\"gameid\":86,\"id\":11},{\"detail\":\"梅A\",\"gameid\":86,\"id\":12},{\"detail\":\"红A\",\"gameid\":86,\"id\":13},{\"detail\":\"黑A\",\"gameid\":86,\"id\":14},{\"detail\":\"方2\",\"gameid\":86,\"id\":21},{\"detail\":\"梅2\",\"gameid\":86,\"id\":22},{\"detail\":\"红2\",\"gameid\":86,\"id\":23},{\"detail\":\"黑2\",\"gameid\":86,\"id\":24},{\"detail\":\"方3\",\"gameid\":86,\"id\":31},{\"detail\":\"梅3\",\"gameid\":86,\"id\":32},{\"detail\":\"红3\",\"gameid\":86,\"id\":33},{\"detail\":\"黑3\",\"gameid\":86,\"id\":34},{\"detail\":\"方4\",\"gameid\":86,\"id\":41},{\"detail\":\"梅4\",\"gameid\":86,\"id\":42},{\"detail\":\"红4\",\"gameid\":86,\"id\":43},{\"detail\":\"黑4\",\"gameid\":86,\"id\":44},{\"detail\":\"方5\",\"gameid\":86,\"id\":51},{\"detail\":\"梅5\",\"gameid\":86,\"id\":52},{\"detail\":\"红5\",\"gameid\":86,\"id\":53},{\"detail\":\"黑5\",\"gameid\":86,\"id\":54},{\"detail\":\"方6\",\"gameid\":86,\"id\":61},{\"detail\":\"梅6\",\"gameid\":86,\"id\":62},{\"detail\":\"红6\",\"gameid\":86,\"id\":63},{\"detail\":\"黑6\",\"gameid\":86,\"id\":64},{\"detail\":\"方7\",\"gameid\":86,\"id\":71},{\"detail\":\"梅7\",\"gameid\":86,\"id\":72},{\"detail\":\"红7\",\"gameid\":86,\"id\":73},{\"detail\":\"黑7\",\"gameid\":86,\"id\":74},{\"detail\":\"方8\",\"gameid\":86,\"id\":81},{\"detail\":\"梅8\",\"gameid\":86,\"id\":82},{\"detail\":\"红8\",\"gameid\":86,\"id\":83},{\"detail\":\"黑8\",\"gameid\":86,\"id\":84},{\"detail\":\"方9\",\"gameid\":86,\"id\":91},{\"detail\":\"梅9\",\"gameid\":86,\"id\":92},{\"detail\":\"红9\",\"gameid\":86,\"id\":93},{\"detail\":\"黑9\",\"gameid\":86,\"id\":94},{\"detail\":\"方10\",\"gameid\":86,\"id\":101},{\"detail\":\"梅10\",\"gameid\":86,\"id\":102},{\"detail\":\"红10\",\"gameid\":86,\"id\":103},{\"detail\":\"黑10\",\"gameid\":86,\"id\":104},{\"detail\":\"方J\",\"gameid\":86,\"id\":111},{\"detail\":\"梅J\",\"gameid\":86,\"id\":112},{\"detail\":\"红J\",\"gameid\":86,\"id\":113},{\"detail\":\"黑J\",\"gameid\":86,\"id\":114},{\"detail\":\"方Q\",\"gameid\":86,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":86,\"id\":122},{\"detail\":\"红Q\",\"gameid\":86,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":86,\"id\":124},{\"detail\":\"方K\",\"gameid\":86,\"id\":131},{\"detail\":\"梅K\",\"gameid\":86,\"id\":132},{\"detail\":\"红K\",\"gameid\":86,\"id\":133},{\"detail\":\"黑K\",\"gameid\":86,\"id\":134},{\"detail\":\"绷带\",\"gameid\":87,\"id\":101},{\"detail\":\"止痛药\",\"gameid\":87,\"id\":102},{\"detail\":\"肾上腺素\",\"gameid\":87,\"id\":103},{\"detail\":\"药包\",\"gameid\":87,\"id\":104},{\"detail\":\"平底锅\",\"gameid\":87,\"id\":105},{\"detail\":\"背包\",\"gameid\":87,\"id\":106},{\"detail\":\"手雷（消除）\",\"gameid\":87,\"id\":107},{\"detail\":\"头盔\",\"gameid\":87,\"id\":108},{\"detail\":\"步枪\",\"gameid\":87,\"id\":109},{\"detail\":\"WILD（癞子）\",\"gameid\":87,\"id\":110},{\"detail\":\"JACKPOT\",\"gameid\":87,\"id\":111},{\"detail\":\"白玉\",\"gameid\":88,\"id\":101},{\"detail\":\"碧玉\",\"gameid\":88,\"id\":102},{\"detail\":\"墨玉\",\"gameid\":88,\"id\":103},{\"detail\":\"玛瑙\",\"gameid\":88,\"id\":104},{\"detail\":\"琥珀\",\"gameid\":88,\"id\":105},{\"detail\":\"祖母绿\",\"gameid\":88,\"id\":201},{\"detail\":\"猫眼石\",\"gameid\":88,\"id\":202},{\"detail\":\"紫水晶\",\"gameid\":88,\"id\":203},{\"detail\":\"翡翠\",\"gameid\":88,\"id\":204},{\"detail\":\"珍珠\",\"gameid\":88,\"id\":205},{\"detail\":\"红宝石\",\"gameid\":88,\"id\":301},{\"detail\":\"绿宝石\",\"gameid\":88,\"id\":302},{\"detail\":\"黄宝石\",\"gameid\":88,\"id\":303},{\"detail\":\"蓝宝石\",\"gameid\":88,\"id\":304},{\"detail\":\"钻石\",\"gameid\":88,\"id\":305},{\"detail\":\"钥匙\",\"gameid\":88,\"id\":401},{\"detail\":\"方A\",\"gameid\":90,\"id\":11},{\"detail\":\"梅A\",\"gameid\":90,\"id\":12},{\"detail\":\"红A\",\"gameid\":90,\"id\":13},{\"detail\":\"黑A\",\"gameid\":90,\"id\":14},{\"detail\":\"方2\",\"gameid\":90,\"id\":21},{\"detail\":\"梅2\",\"gameid\":90,\"id\":22},{\"detail\":\"红2\",\"gameid\":90,\"id\":23},{\"detail\":\"黑2\",\"gameid\":90,\"id\":24},{\"detail\":\"方3\",\"gameid\":90,\"id\":31},{\"detail\":\"梅3\",\"gameid\":90,\"id\":32},{\"detail\":\"红3\",\"gameid\":90,\"id\":33},{\"detail\":\"黑3\",\"gameid\":90,\"id\":34},{\"detail\":\"方4\",\"gameid\":90,\"id\":41},{\"detail\":\"梅4\",\"gameid\":90,\"id\":42},{\"detail\":\"红4\",\"gameid\":90,\"id\":43},{\"detail\":\"黑4\",\"gameid\":90,\"id\":44},{\"detail\":\"方5\",\"gameid\":90,\"id\":51},{\"detail\":\"梅5\",\"gameid\":90,\"id\":52},{\"detail\":\"红5\",\"gameid\":90,\"id\":53},{\"detail\":\"黑5\",\"gameid\":90,\"id\":54},{\"detail\":\"方6\",\"gameid\":90,\"id\":61},{\"detail\":\"梅6\",\"gameid\":90,\"id\":62},{\"detail\":\"红6\",\"gameid\":90,\"id\":63},{\"detail\":\"黑6\",\"gameid\":90,\"id\":64},{\"detail\":\"方7\",\"gameid\":90,\"id\":71},{\"detail\":\"梅7\",\"gameid\":90,\"id\":72},{\"detail\":\"红7\",\"gameid\":90,\"id\":73},{\"detail\":\"黑7\",\"gameid\":90,\"id\":74},{\"detail\":\"方8\",\"gameid\":90,\"id\":81},{\"detail\":\"梅8\",\"gameid\":90,\"id\":82},{\"detail\":\"红8\",\"gameid\":90,\"id\":83},{\"detail\":\"黑8\",\"gameid\":90,\"id\":84},{\"detail\":\"方9\",\"gameid\":90,\"id\":91},{\"detail\":\"梅9\",\"gameid\":90,\"id\":92},{\"detail\":\"红9\",\"gameid\":90,\"id\":93},{\"detail\":\"黑9\",\"gameid\":90,\"id\":94},{\"detail\":\"方10\",\"gameid\":90,\"id\":101},{\"detail\":\"梅10\",\"gameid\":90,\"id\":102},{\"detail\":\"红10\",\"gameid\":90,\"id\":103},{\"detail\":\"黑10\",\"gameid\":90,\"id\":104},{\"detail\":\"方J\",\"gameid\":90,\"id\":111},{\"detail\":\"梅J\",\"gameid\":90,\"id\":112},{\"detail\":\"红J\",\"gameid\":90,\"id\":113},{\"detail\":\"黑J\",\"gameid\":90,\"id\":114},{\"detail\":\"方Q\",\"gameid\":90,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":90,\"id\":122},{\"detail\":\"红Q\",\"gameid\":90,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":90,\"id\":124},{\"detail\":\"方K\",\"gameid\":90,\"id\":131},{\"detail\":\"梅K\",\"gameid\":90,\"id\":132},{\"detail\":\"红K\",\"gameid\":90,\"id\":133},{\"detail\":\"黑K\",\"gameid\":90,\"id\":134},{\"detail\":\"方A\",\"gameid\":91,\"id\":11},{\"detail\":\"梅A\",\"gameid\":91,\"id\":12},{\"detail\":\"红A\",\"gameid\":91,\"id\":13},{\"detail\":\"黑A\",\"gameid\":91,\"id\":14},{\"detail\":\"方2\",\"gameid\":91,\"id\":21},{\"detail\":\"梅2\",\"gameid\":91,\"id\":22},{\"detail\":\"红2\",\"gameid\":91,\"id\":23},{\"detail\":\"黑2\",\"gameid\":91,\"id\":24},{\"detail\":\"方3\",\"gameid\":91,\"id\":31},{\"detail\":\"梅3\",\"gameid\":91,\"id\":32},{\"detail\":\"红3\",\"gameid\":91,\"id\":33},{\"detail\":\"黑3\",\"gameid\":91,\"id\":34},{\"detail\":\"方4\",\"gameid\":91,\"id\":41},{\"detail\":\"梅4\",\"gameid\":91,\"id\":42},{\"detail\":\"红4\",\"gameid\":91,\"id\":43},{\"detail\":\"黑4\",\"gameid\":91,\"id\":44},{\"detail\":\"方5\",\"gameid\":91,\"id\":51},{\"detail\":\"梅5\",\"gameid\":91,\"id\":52},{\"detail\":\"红5\",\"gameid\":91,\"id\":53},{\"detail\":\"黑5\",\"gameid\":91,\"id\":54},{\"detail\":\"方6\",\"gameid\":91,\"id\":61},{\"detail\":\"梅6\",\"gameid\":91,\"id\":62},{\"detail\":\"红6\",\"gameid\":91,\"id\":63},{\"detail\":\"黑6\",\"gameid\":91,\"id\":64},{\"detail\":\"方7\",\"gameid\":91,\"id\":71},{\"detail\":\"梅7\",\"gameid\":91,\"id\":72},{\"detail\":\"红7\",\"gameid\":91,\"id\":73},{\"detail\":\"黑7\",\"gameid\":91,\"id\":74},{\"detail\":\"方8\",\"gameid\":91,\"id\":81},{\"detail\":\"梅8\",\"gameid\":91,\"id\":82},{\"detail\":\"红8\",\"gameid\":91,\"id\":83},{\"detail\":\"黑8\",\"gameid\":91,\"id\":84},{\"detail\":\"方9\",\"gameid\":91,\"id\":91},{\"detail\":\"梅9\",\"gameid\":91,\"id\":92},{\"detail\":\"红9\",\"gameid\":91,\"id\":93},{\"detail\":\"黑9\",\"gameid\":91,\"id\":94},{\"detail\":\"方10\",\"gameid\":91,\"id\":101},{\"detail\":\"梅10\",\"gameid\":91,\"id\":102},{\"detail\":\"红10\",\"gameid\":91,\"id\":103},{\"detail\":\"黑10\",\"gameid\":91,\"id\":104},{\"detail\":\"方J\",\"gameid\":91,\"id\":111},{\"detail\":\"梅J\",\"gameid\":91,\"id\":112},{\"detail\":\"红J\",\"gameid\":91,\"id\":113},{\"detail\":\"黑J\",\"gameid\":91,\"id\":114},{\"detail\":\"方Q\",\"gameid\":91,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":91,\"id\":122},{\"detail\":\"红Q\",\"gameid\":91,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":91,\"id\":124},{\"detail\":\"方K\",\"gameid\":91,\"id\":131},{\"detail\":\"梅K\",\"gameid\":91,\"id\":132},{\"detail\":\"红K\",\"gameid\":91,\"id\":133},{\"detail\":\"黑K\",\"gameid\":91,\"id\":134},{\"detail\":\"方2\",\"gameid\":92,\"id\":21},{\"detail\":\"梅2\",\"gameid\":92,\"id\":22},{\"detail\":\"红2\",\"gameid\":92,\"id\":23},{\"detail\":\"黑2\",\"gameid\":92,\"id\":24},{\"detail\":\"方3\",\"gameid\":92,\"id\":31},{\"detail\":\"梅3\",\"gameid\":92,\"id\":32},{\"detail\":\"红3\",\"gameid\":92,\"id\":33},{\"detail\":\"黑3\",\"gameid\":92,\"id\":34},{\"detail\":\"方4\",\"gameid\":92,\"id\":41},{\"detail\":\"梅4\",\"gameid\":92,\"id\":42},{\"detail\":\"红4\",\"gameid\":92,\"id\":43},{\"detail\":\"黑4\",\"gameid\":92,\"id\":44},{\"detail\":\"方5\",\"gameid\":92,\"id\":51},{\"detail\":\"梅5\",\"gameid\":92,\"id\":52},{\"detail\":\"红5\",\"gameid\":92,\"id\":53},{\"detail\":\"黑5\",\"gameid\":92,\"id\":54},{\"detail\":\"方6\",\"gameid\":92,\"id\":61},{\"detail\":\"梅6\",\"gameid\":92,\"id\":62},{\"detail\":\"红6\",\"gameid\":92,\"id\":63},{\"detail\":\"黑6\",\"gameid\":92,\"id\":64},{\"detail\":\"方7\",\"gameid\":92,\"id\":71},{\"detail\":\"梅7\",\"gameid\":92,\"id\":72},{\"detail\":\"红7\",\"gameid\":92,\"id\":73},{\"detail\":\"黑7\",\"gameid\":92,\"id\":74},{\"detail\":\"方8\",\"gameid\":92,\"id\":81},{\"detail\":\"梅8\",\"gameid\":92,\"id\":82},{\"detail\":\"红8\",\"gameid\":92,\"id\":83},{\"detail\":\"黑8\",\"gameid\":92,\"id\":84},{\"detail\":\"方9\",\"gameid\":92,\"id\":91},{\"detail\":\"梅9\",\"gameid\":92,\"id\":92},{\"detail\":\"红9\",\"gameid\":92,\"id\":93},{\"detail\":\"黑9\",\"gameid\":92,\"id\":94},{\"detail\":\"方10\",\"gameid\":92,\"id\":101},{\"detail\":\"梅10\",\"gameid\":92,\"id\":102},{\"detail\":\"红10\",\"gameid\":92,\"id\":103},{\"detail\":\"黑10\",\"gameid\":92,\"id\":104},{\"detail\":\"方J\",\"gameid\":92,\"id\":111},{\"detail\":\"梅J\",\"gameid\":92,\"id\":112},{\"detail\":\"红J\",\"gameid\":92,\"id\":113},{\"detail\":\"黑J\",\"gameid\":92,\"id\":114},{\"detail\":\"方Q\",\"gameid\":92,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":92,\"id\":122},{\"detail\":\"红Q\",\"gameid\":92,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":92,\"id\":124},{\"detail\":\"方K\",\"gameid\":92,\"id\":131},{\"detail\":\"梅K\",\"gameid\":92,\"id\":132},{\"detail\":\"红K\",\"gameid\":92,\"id\":133},{\"detail\":\"黑K\",\"gameid\":92,\"id\":134},{\"detail\":\"方A\",\"gameid\":92,\"id\":141},{\"detail\":\"梅A\",\"gameid\":92,\"id\":142},{\"detail\":\"红A\",\"gameid\":92,\"id\":143},{\"detail\":\"黑A\",\"gameid\":92,\"id\":144},{\"detail\":\"小不点\",\"gameid\":93,\"id\":1001},{\"detail\":\"小绿鱼\",\"gameid\":93,\"id\":1002},{\"detail\":\"小黄鱼\",\"gameid\":93,\"id\":1003},{\"detail\":\"苍蝇鱼\",\"gameid\":93,\"id\":1004},{\"detail\":\"热带鱼\",\"gameid\":93,\"id\":1005},{\"detail\":\"小丑鱼\",\"gameid\":93,\"id\":1006},{\"detail\":\"河豚\",\"gameid\":93,\"id\":1007},{\"detail\":\"小蓝鱼\",\"gameid\":93,\"id\":1008},{\"detail\":\"灯笼鱼\",\"gameid\":93,\"id\":1009},{\"detail\":\"小海龟\",\"gameid\":93,\"id\":1010},{\"detail\":\"天使鱼\",\"gameid\":93,\"id\":1011},{\"detail\":\"蝴蝶鱼\",\"gameid\":93,\"id\":1012},{\"detail\":\"蓝尾鱼\",\"gameid\":93,\"id\":1013},{\"detail\":\"剑鱼\",\"gameid\":93,\"id\":1014},{\"detail\":\"魔鬼鱼\",\"gameid\":93,\"id\":1015},{\"detail\":\"海藻\",\"gameid\":93,\"id\":1016},{\"detail\":\"海豚\",\"gameid\":93,\"id\":1017},{\"detail\":\"银鲨\",\"gameid\":93,\"id\":1018},{\"detail\":\"金鲨\",\"gameid\":93,\"id\":1019},{\"detail\":\"双头企鹅\",\"gameid\":93,\"id\":1020},{\"detail\":\"大章鱼\",\"gameid\":93,\"id\":1021},{\"detail\":\"银龙\",\"gameid\":93,\"id\":1022},{\"detail\":\"金龙\",\"gameid\":93,\"id\":1023},{\"detail\":\"胖头金鲨\",\"gameid\":93,\"id\":1024},{\"detail\":\"美人鱼\",\"gameid\":93,\"id\":1025},{\"detail\":\"宝藏船\",\"gameid\":93,\"id\":1026},{\"detail\":\"金蟾BOSS\",\"gameid\":93,\"id\":2001},{\"detail\":\"炼丹炉\",\"gameid\":93,\"id\":3001},{\"detail\":\"全屏炸弹\",\"gameid\":93,\"id\":3002},{\"detail\":\"出奇制胜\",\"gameid\":93,\"id\":3003},{\"detail\":\"一箭双雕\",\"gameid\":93,\"id\":3004},{\"detail\":\"一石三鸟\",\"gameid\":93,\"id\":3005},{\"detail\":\"金玉满堂\",\"gameid\":93,\"id\":3006},{\"detail\":\"连锁闪电1\",\"gameid\":93,\"id\":3007},{\"detail\":\"连锁闪电2\",\"gameid\":93,\"id\":3008},{\"detail\":\"连锁闪电3\",\"gameid\":93,\"id\":3009},{\"detail\":\"连锁闪电4\",\"gameid\":93,\"id\":3010},{\"detail\":\"连锁闪电5\",\"gameid\":93,\"id\":3011},{\"detail\":\"连续-小绿\",\"gameid\":93,\"id\":4001},{\"detail\":\"连续-小黄\",\"gameid\":93,\"id\":4002},{\"detail\":\"连续-圆形灯笼\",\"gameid\":93,\"id\":4010},{\"detail\":\"连续-圆形海龟\",\"gameid\":93,\"id\":4030},{\"detail\":\"偏移-小丑\",\"gameid\":93,\"id\":5001},{\"detail\":\"偏移-热带\",\"gameid\":93,\"id\":5002},{\"detail\":\"双股剑\",\"gameid\":94,\"id\":101},{\"detail\":\"丈八蛇矛\",\"gameid\":94,\"id\":102},{\"detail\":\"青龙偃月刀\",\"gameid\":94,\"id\":103},{\"detail\":\"方天画戟\",\"gameid\":94,\"id\":104},{\"detail\":\"朱雀羽扇\",\"gameid\":94,\"id\":105},{\"detail\":\"八卦阵\",\"gameid\":94,\"id\":106},{\"detail\":\"赤兔马\",\"gameid\":94,\"id\":107},{\"detail\":\"紫金冠\",\"gameid\":94,\"id\":108},{\"detail\":\"太平要术\",\"gameid\":94,\"id\":109},{\"detail\":\"传国玉玺\",\"gameid\":94,\"id\":110},{\"detail\":\"WILD-癞子\",\"gameid\":94,\"id\":111},{\"detail\":\"BONUS-过关斩将\",\"gameid\":94,\"id\":201},{\"detail\":\"SCATTER-草船借箭\",\"gameid\":94,\"id\":202},{\"detail\":\"苹果\",\"gameid\":95,\"id\":101},{\"detail\":\"橙子\",\"gameid\":95,\"id\":102},{\"detail\":\"柠檬\",\"gameid\":95,\"id\":103},{\"detail\":\"铃铛\",\"gameid\":95,\"id\":104},{\"detail\":\"西瓜\",\"gameid\":95,\"id\":105},{\"detail\":\"星星\",\"gameid\":95,\"id\":106},{\"detail\":\"77\",\"gameid\":95,\"id\":107},{\"detail\":\"BAR\",\"gameid\":95,\"id\":108},{\"detail\":\"银lucky\",\"gameid\":95,\"id\":109},{\"detail\":\"金lucky\",\"gameid\":95,\"id\":110},{\"detail\":\"(小)苹果\",\"gameid\":95,\"id\":201},{\"detail\":\"(小)橙子\",\"gameid\":95,\"id\":202},{\"detail\":\"(小)柠檬\",\"gameid\":95,\"id\":203},{\"detail\":\"(小)铃铛\",\"gameid\":95,\"id\":204},{\"detail\":\"(小)西瓜\",\"gameid\":95,\"id\":205},{\"detail\":\"(小)星星\",\"gameid\":95,\"id\":206},{\"detail\":\"(小)77\",\"gameid\":95,\"id\":207},{\"detail\":\"(小)BAR\",\"gameid\":95,\"id\":208},{\"detail\":\"大三元\",\"gameid\":95,\"id\":301},{\"detail\":\"大四喜\",\"gameid\":95,\"id\":302},{\"detail\":\"大满贯\",\"gameid\":95,\"id\":303},{\"detail\":\"肉\",\"gameid\":96,\"id\":101},{\"detail\":\"金疮药\",\"gameid\":96,\"id\":102},{\"detail\":\"火把\",\"gameid\":96,\"id\":103},{\"detail\":\"回城卷轴\",\"gameid\":96,\"id\":104},{\"detail\":\"噬魂\",\"gameid\":96,\"id\":105},{\"detail\":\"裁决\",\"gameid\":96,\"id\":106},{\"detail\":\"屠龙\",\"gameid\":96,\"id\":107},{\"detail\":\"逍遥扇\",\"gameid\":96,\"id\":108},{\"detail\":\"麻痹戒指\",\"gameid\":96,\"id\":109},{\"detail\":\"烈火剑法\",\"gameid\":96,\"id\":110},{\"detail\":\"WILD-癞子\",\"gameid\":96,\"id\":111},{\"detail\":\"BONUS-保卫玛法\",\"gameid\":96,\"id\":201},{\"detail\":\"SCATTER-流星火雨\",\"gameid\":96,\"id\":202},{\"detail\":\"10\",\"gameid\":97,\"id\":101},{\"detail\":\"J\",\"gameid\":97,\"id\":102},{\"detail\":\"Q\",\"gameid\":97,\"id\":103},{\"detail\":\"K\",\"gameid\":97,\"id\":104},{\"detail\":\"A\",\"gameid\":97,\"id\":105},{\"detail\":\"妲己\",\"gameid\":97,\"id\":106},{\"detail\":\"亚瑟\",\"gameid\":97,\"id\":107},{\"detail\":\"庄周\",\"gameid\":97,\"id\":108},{\"detail\":\"后羿\",\"gameid\":97,\"id\":109},{\"detail\":\"香香\",\"gameid\":97,\"id\":110},{\"detail\":\"WILD-癞子水晶\",\"gameid\":97,\"id\":111},{\"detail\":\"SCATTER-李白\",\"gameid\":97,\"id\":201},{\"detail\":\"JACKPOT-武则天\",\"gameid\":97,\"id\":202},{\"desc\":\"\",\"detail\":\"方2\",\"en_name\":\"\",\"gameid\":\"80\",\"id\":\"21\",\"name\":\"\"},{\"detail\":\"梅2\",\"gameid\":98,\"id\":22},{\"detail\":\"红2\",\"gameid\":98,\"id\":23},{\"detail\":\"黑2\",\"gameid\":98,\"id\":24},{\"detail\":\"方3\",\"gameid\":98,\"id\":31},{\"detail\":\"梅3\",\"gameid\":98,\"id\":32},{\"detail\":\"红3\",\"gameid\":98,\"id\":33},{\"detail\":\"黑3\",\"gameid\":98,\"id\":34},{\"detail\":\"方4\",\"gameid\":98,\"id\":41},{\"detail\":\"梅4\",\"gameid\":98,\"id\":42},{\"detail\":\"红4\",\"gameid\":98,\"id\":43},{\"detail\":\"黑4\",\"gameid\":98,\"id\":44},{\"detail\":\"方5\",\"gameid\":98,\"id\":51},{\"detail\":\"梅5\",\"gameid\":98,\"id\":52},{\"desc\":\"\",\"detail\":\"红5\",\"en_name\":\"\",\"gameid\":\"81\",\"id\":\"53\",\"name\":\"\"},{\"detail\":\"黑5\",\"gameid\":98,\"id\":54},{\"detail\":\"方6\",\"gameid\":98,\"id\":61},{\"detail\":\"梅6\",\"gameid\":98,\"id\":62},{\"detail\":\"红6\",\"gameid\":98,\"id\":63},{\"detail\":\"黑6\",\"gameid\":98,\"id\":64},{\"detail\":\"方7\",\"gameid\":98,\"id\":71},{\"detail\":\"梅7\",\"gameid\":98,\"id\":72},{\"detail\":\"红7\",\"gameid\":98,\"id\":73},{\"detail\":\"黑7\",\"gameid\":98,\"id\":74},{\"detail\":\"方8\",\"gameid\":98,\"id\":81},{\"detail\":\"梅8\",\"gameid\":98,\"id\":82},{\"detail\":\"红8\",\"gameid\":98,\"id\":83},{\"detail\":\"黑8\",\"gameid\":98,\"id\":84},{\"detail\":\"方9\",\"gameid\":98,\"id\":91},{\"detail\":\"梅9\",\"gameid\":98,\"id\":92},{\"detail\":\"红9\",\"gameid\":98,\"id\":93},{\"detail\":\"黑9\",\"gameid\":98,\"id\":94},{\"detail\":\"方10\",\"gameid\":98,\"id\":101},{\"detail\":\"梅10\",\"gameid\":98,\"id\":102},{\"detail\":\"红10\",\"gameid\":98,\"id\":103},{\"detail\":\"黑10\",\"gameid\":98,\"id\":104},{\"detail\":\"方J\",\"gameid\":98,\"id\":111},{\"detail\":\"梅J\",\"gameid\":98,\"id\":112},{\"detail\":\"红J\",\"gameid\":98,\"id\":113},{\"detail\":\"黑J\",\"gameid\":98,\"id\":114},{\"detail\":\"方Q\",\"gameid\":98,\"id\":121},{\"detail\":\"梅Q\",\"gameid\":98,\"id\":122},{\"detail\":\"红Q\",\"gameid\":98,\"id\":123},{\"detail\":\"黑Q\",\"gameid\":98,\"id\":124},{\"detail\":\"方K\",\"gameid\":98,\"id\":131},{\"detail\":\"梅K\",\"gameid\":98,\"id\":132},{\"detail\":\"红K\",\"gameid\":98,\"id\":133},{\"detail\":\"黑K\",\"gameid\":98,\"id\":134},{\"detail\":\"方A\",\"gameid\":98,\"id\":141},{\"detail\":\"梅A\",\"gameid\":98,\"id\":142},{\"detail\":\"红A\",\"gameid\":98,\"id\":143},{\"detail\":\"黑A\",\"gameid\":98,\"id\":144},{\"detail\":\"1筒\",\"gameid\":99,\"id\":10},{\"detail\":\"2筒\",\"gameid\":99,\"id\":20},{\"detail\":\"3筒\",\"gameid\":99,\"id\":30},{\"detail\":\"4筒\",\"gameid\":99,\"id\":40},{\"detail\":\"5筒\",\"gameid\":99,\"id\":50},{\"detail\":\"6筒\",\"gameid\":99,\"id\":60},{\"detail\":\"7筒\",\"gameid\":99,\"id\":70},{\"detail\":\"8筒\",\"gameid\":99,\"id\":80},{\"detail\":\"9筒\",\"gameid\":99,\"id\":90},{\"detail\":\"10筒\",\"gameid\":99,\"id\":105}]'),(5,'[{\"detail\":\"详情\",\"gameid\":\"85\",\"id\":\"5001\"}]');
/*!40000 ALTER TABLE `game_parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_platform`
--

DROP TABLE IF EXISTS `game_platform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_platform` (
  `game_function_id` int(11) DEFAULT NULL COMMENT '游戏和功能id',
  `channel_id` int(10) unsigned DEFAULT NULL COMMENT '渠道id',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `game_function_id` (`game_function_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='游戏平台管理';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_platform`
--

LOCK TABLES `game_platform` WRITE;
/*!40000 ALTER TABLE `game_platform` DISABLE KEYS */;
INSERT INTO `game_platform` VALUES (-2,24,1),(-1,24,1),(80,24,0),(81,24,0),(82,24,1),(83,24,1),(84,24,-1),(85,24,-1),(86,24,-1),(87,24,-1),(88,24,-1),(90,24,-1),(91,24,-1),(92,24,-1),(93,24,-1),(94,24,-1),(95,24,-1),(-2,7,1),(-1,7,1),(80,7,1),(81,7,1),(83,7,0),(84,7,0),(85,7,1),(86,7,1),(90,7,1),(91,7,1),(92,7,1),(93,7,1),(-2,27,1),(96,27,1),(97,27,1),(98,27,1),(99,27,1),(80,27,1),(81,27,1),(82,27,1),(83,27,1),(84,27,1),(85,27,1),(86,27,1),(87,27,1),(88,27,1),(90,27,1),(91,27,1),(92,27,1),(93,27,1),(94,27,1),(95,27,1),(-2,1,1),(80,1,1),(81,1,0),(82,1,0),(83,1,1),(84,1,1),(86,1,0),(87,1,0),(90,1,1),(91,1,1),(92,1,1),(93,1,0),(94,1,1),(95,1,1);
/*!40000 ALTER TABLE `game_platform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ip_black_white_list`
--

DROP TABLE IF EXISTS `ip_black_white_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ip_black_white_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` tinyint(4) DEFAULT NULL COMMENT '黑名单（1）还是白名单（2）',
  `country_area_ip` varchar(500) DEFAULT NULL COMMENT '国家/地区/IP',
  `channel_id` int(10) unsigned DEFAULT NULL COMMENT '渠道id',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  KEY `type` (`type`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='IP黑白名单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ip_black_white_list`
--

LOCK TABLES `ip_black_white_list` WRITE;
/*!40000 ALTER TABLE `ip_black_white_list` DISABLE KEYS */;
INSERT INTO `ip_black_white_list` VALUES (5,1,'菲律宾',24,'法尔胜'),(6,1,'菲律宾',7,'挺可怜的他'),(7,1,'111',7,'挂号费'),(8,1,'喝可乐太疯狂了',7,'通纪念馆'),(9,2,'菲律宾',7,''),(10,2,'菲律宾',1,'荣哥'),(11,1,'热开了间 藕粉色颇丰 欧拉法搜房 8.8.8.5',1,'揉了揉'),(12,1,'111',1,'吃的那家酒店如果你'),(13,1,'hfesfs',1,'艾斯比方法分'),(14,2,'菲律宾',1,'阿瓦达达娃');
/*!40000 ALTER TABLE `ip_black_white_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail`
--

DROP TABLE IF EXISTS `mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `user_id` int(10) unsigned NOT NULL COMMENT '生成者账号id',
  `mail_title` varchar(100) DEFAULT NULL COMMENT '邮件标题',
  `mail_content` varchar(5000) DEFAULT NULL COMMENT '邮件内容',
  `mail_accessories` varchar(500) DEFAULT NULL COMMENT '邮件附件',
  `push_time` int(10) unsigned DEFAULT NULL COMMENT '推送时间',
  `failure_time` int(10) unsigned DEFAULT NULL COMMENT '失效时间',
  `push_player_id` mediumtext COMMENT '推送用户id',
  `status` tinyint(4) DEFAULT '0' COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `mail_title` (`mail_title`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `push_time` (`push_time`) USING BTREE,
  KEY `failure_time` (`failure_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COMMENT='游戏内邮件';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail`
--

LOCK TABLES `mail` WRITE;
/*!40000 ALTER TABLE `mail` DISABLE KEYS */;
INSERT INTO `mail` VALUES (1,1,16,'阿达瓦多多多多','<p>rff<span style=\"color: rgb(217, 150, 148);\">s</span>ds<span style=\"font-size: 18px; color: rgb(84, 141, 212);\">fsad呀</span>呀<span style=\"color: rgb(149, 55, 52);\">呀</span></p>','{20010001: 10000}',1534957200,1536515129,'11232,5841202,22353',0),(2,1,16,'玉玲会更好','<p>基恩方法名机动车那么快23</p>','',1534960110,1535132912,'全服推送',0),(3,1,1,'要好好','<p><span style=\"font-size: 10px; color: rgb(250, 192, 143);\">啊</span><span style=\"color: rgb(31, 73, 125); font-size: 10px;\">较</span><span style=\"font-family: 微软雅黑, &quot;Microsoft YaHei&quot;;\"><span style=\"color: rgb(31, 73, 125); font-size: 10px;\">大</span><em><span style=\"color: rgb(31, 73, 125); font-size: 10px;\">面</span></em></span><span style=\"font-family: &quot;arial black&quot;, &quot;avant garde&quot;;\"><em><span style=\"color: rgb(147, 137, 83); font-size: 14px;\">积<span style=\"color: rgb(147, 137, 83); font-size: 20px;\">我</span></span></em><em><span style=\"color: rgb(147, 137, 83); font-size: 20px;\"></span><span style=\"font-size: 16px;\">等</span></em></span><em><span style=\"font-size: 16px;\"></span><span style=\"font-size: 14px;\"></span><span style=\"font-size: 20px; border: 1px solid rgb(0, 0, 0);\">你</span></em><span style=\"color: rgb(227, 108, 9); font-size: 20px;\">忙</span><span style=\"font-family: 黑体, SimHei; color: rgb(227, 108, 9); font-size: 20px;\">完</span><span style=\"font-family: 微软雅黑, &quot;Microsoft YaHei&quot;;\"><span style=\"font-size: 20px;\">顺</span><strong><span style=\"color: rgb(196, 189, 151); font-size: 20px;\"><em><span style=\"font-size: 24px;\">丰</span></em></span></strong></span><span style=\"font-family: 黑体, SimHei;\"><span style=\"color: rgb(227, 108, 9); font-size: 24px;\">动</span><span style=\"font-size: 20px;\"><strong>漫</strong></span></span><span style=\"font-size: 20px;\"><span style=\"font-size: 11px;\">网</span></span><strong><span style=\"font-size: 20px;\"><span style=\"color: rgb(196, 189, 151); font-size: 24px;\">说</span><span style=\"color: rgb(178, 162, 199);\"><span style=\"font-size: 24px;\"></span><span style=\"font-family: &quot;arial black&quot;, &quot;avant garde&quot;;\"><span style=\"border: 1px solid rgb(0, 0, 0);\">如</span>果</span><span style=\"font-size: 14px; color: rgb(31, 73, 125);\">的</span></span></span><em><span style=\"color: rgb(178, 162, 199); font-size: 14px;\">是</span></em></strong><em><span style=\"color: rgb(178, 162, 199); font-family: 黑体, SimHei; font-size: 20px;\">十</span></em><span style=\"border: 1px solid rgb(0, 0, 0);\"><span style=\"color: rgb(178, 162, 199); font-family: 黑体, SimHei; font-size: 14px;\">分</span><span style=\"font-family: 隶书, SimLi; font-size: 20px; color: rgb(227, 108, 9);\">色</span><span style=\"color: rgb(178, 162, 199); font-family: 隶书, SimLi; font-size: 20px;\">粉</span><strong><em><span style=\"border: 1px solid rgb(0, 0, 0); font-size: 20px; color: rgb(227, 108, 9);\">粉</span></em></strong></span><span style=\"color: rgb(178, 162, 199); font-family: 隶书, SimLi; font-size: 20px;\">色</span></p>','{20010001: 10}',1534982166,1535154977,'486465',0),(4,1,1,'yhjy','<p>的方式v但是</p>','{10010001: 10000, 20010001: 12}',1534896981,1535242584,'全服推送',2),(5,1,1,'adwwda','<p>yhthbtd</p>','{10010001: 2000000, 20010001: 121}',1533860810,1535243212,'12543',0),(6,1,1,'wawa','<p>删附件</p>','',1533774723,1535329928,'2131,53',0),(7,7,1,'人发顺丰','<p>给你吃的地方</p>','{10010001: 1020000}',1534997405,1535343010,'全服推送',0),(8,7,1,'而是','<p>嘎嘎嘎v下</p>','',1534997497,1535775099,'54546,748654',0),(9,1,1,'的撒按时','<p>啊哇哇哇</p>','{20010001: 1200000}',1534889353,1535753356,'全服推送',1),(10,7,1,'发送到','<p>若个人同国歌</p>','',1533161903,1535062705,'123',0),(11,1,1,'rthrf','<p>啊哇哇哇hnbgh</p>','{20010001: 1200000, 10010001: 10000}',1534889353,1535753356,'全服推送',0),(12,7,1,'wr','<p>fsdefeswfew</p>','{20010001: 12}',1538436774,1538695977,'全服推送',1);
/*!40000 ALTER TABLE `mail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `marquee`
--

DROP TABLE IF EXISTS `marquee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marquee` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL COMMENT '渠道id',
  `user_id` int(11) NOT NULL COMMENT '生成者账号id',
  `marquee_content` varchar(5000) DEFAULT NULL COMMENT '跑马灯内容',
  `interval_time` smallint(5) unsigned DEFAULT NULL COMMENT '间隔时间',
  `push_times` smallint(6) DEFAULT NULL COMMENT '推送次数',
  `begin_time` int(10) unsigned DEFAULT NULL COMMENT '开始时间',
  `end_time` int(10) unsigned DEFAULT NULL COMMENT '结束时间',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `begin_time` (`begin_time`) USING BTREE,
  KEY `end_time` (`end_time`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `marquee_content` (`marquee_content`(255)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='跑马灯（小喇叭）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marquee`
--

LOCK TABLES `marquee` WRITE;
/*!40000 ALTER TABLE `marquee` DISABLE KEYS */;
INSERT INTO `marquee` VALUES (1,1,13,'<p>奥术大师嗯嗯翁额</p>',15,-1,1535158800,1535852491,3),(2,7,1,'<p>按时打算打是大所多</p>',63,123,1534499995,1534540812,1),(3,1,1,'<p>银河帝国胡椒粉啊速度快打手拉手的阿萨德了卡死了拉屎的克拉克说对啦开始懂了快递费代课老师跟难对付卡机男距无法马克思佛拉斯暗少肯德基啊山东矿机爱上大口径的哈萨克居安思危哦你个头啦</p>',555,66,1533813003,1536491408,1),(4,1,1,'<p><span style=\"font-size: 24px;\">554<span style=\"font-size: 24px; color: rgb(227, 108, 9);\"><strong><span style=\"font-size: 10px; font-family: 隶书, SimLi;\">dfsdf<span style=\"font-size: 10px; font-family: 隶书, SimLi; color: rgb(128, 100, 162);\"><em><span style=\"font-family: 隶书, SimLi; font-size: 20px;\">大娃娃无</span></em></span></span></strong><strong><span style=\"font-size: 10px; font-family: 隶书, SimLi;\"></span></strong></span></span></p>',23,-1,1534592509,1534678913,2),(5,1,1,'<p><span style=\"font-size: 16px;\">突<span style=\"color: rgb(149, 55, 52);\">然有</span></span><span style=\"color: rgb(149, 55, 52);\">人</span><span style=\"color: rgb(49, 133, 155);\">同<span style=\"font-size: 24px;\">意</span></span><span style=\"font-size: 24px;\">让他</span>有<span style=\"font-size: 10px; color: rgb(227, 108, 9);\">人讨</span>厌过期的啊啊</p>',203,8896,1534889084,1535234686,3),(6,7,1,'<p>6<span style=\"color: rgb(192, 80, 77);\">552山</span>东<span style=\"font-size: 12px; color: rgb(79, 129, 189);\">矿机</span><span style=\"font-size: 20px;\"><span style=\"color: rgb(79, 129, 189);\">附</span>加费nasdm</span>kas</p>',0,-1,1534889084,1535234686,1),(7,7,1,'<p><span style=\"font-size: 24px;\">asdas1<span style=\"font-size: 10px;\">225</span>4<span style=\"font-size: 24px; color: rgb(227, 108, 9);\"><strong><span style=\"font-size: 10px; font-family: 隶书, SimLi;\">dfsdf</span></strong></span><span style=\"font-size: 24px; color: rgb(84, 141, 212);\"><strong><span style=\"font-family: 微软雅黑, &quot;Microsoft YaHei&quot;; font-size: 16px;\">暗少的</span></strong></span></span></p>',230,5865,1533382909,1534678913,0),(8,1,1,'<p>一个复件好高级改成生效的</p>',168,-1,1535223647,1535828454,3),(9,1,1,'<p>未生效的啊啊啊</p>',14,12,1535925895,1536530771,0),(10,7,1,'<p>daasdasd</p>',14,-1,1539214235,1539387037,2);
/*!40000 ALTER TABLE `marquee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_level`
--

DROP TABLE IF EXISTS `member_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_level` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_level_name` varchar(20) DEFAULT NULL COMMENT '会员层级名称',
  `number_withdrawals` tinyint(4) DEFAULT NULL COMMENT '提款次数',
  `over_operation_id` tinyint(4) DEFAULT NULL COMMENT '超过次数后续操作id',
  `fee_charging` int(10) unsigned DEFAULT NULL COMMENT '收取费用',
  `min_withdrawals` int(10) unsigned DEFAULT NULL COMMENT '最小提款',
  `max_withdrawals` int(10) unsigned DEFAULT NULL COMMENT '最大提款',
  `inspect_id` tinyint(4) DEFAULT NULL COMMENT '稽查类型id',
  `inspect_tips` varchar(100) DEFAULT NULL COMMENT '稽查提示文字',
  `channel_id` int(10) unsigned DEFAULT NULL COMMENT '渠道id',
  `is_delete` tinyint(4) DEFAULT '0' COMMENT '逻辑删除',
  PRIMARY KEY (`id`),
  KEY `member_level_name` (`member_level_name`) USING BTREE,
  KEY `is_delete` (`is_delete`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='会员层级';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_level`
--

LOCK TABLES `member_level` WRITE;
/*!40000 ALTER TABLE `member_level` DISABLE KEYS */;
INSERT INTO `member_level` VALUES (1,'11',-1,1,NULL,11,1,1,'',7,0),(2,'1',-1,1,NULL,11,1,1,'',1,1),(3,'和我符文111',-1,1,NULL,1,1,1,'',1,0),(4,'哈哈哈哈',-1,1,NULL,1,1,1,'',1,0),(5,'哈哈1',-1,1,NULL,1,1,1,'',1,0),(6,'哈哈2',-1,1,NULL,1,2,1,'',1,0),(7,'管理员组',-1,1,NULL,1,1,1,'',1,0),(8,'wechat',-1,1,NULL,1,1,1,'',1,0),(9,'管理员组1',-1,1,NULL,11,1,1,'',1,0),(10,'管理员组11',-1,1,NULL,1,1,1,'',1,0),(11,'管理员组88',-1,1,NULL,1,1,1,'',1,0),(12,'1',-1,1,NULL,1,1,1,'',7,0),(13,'11',-1,1,NULL,1,1,1,'',17,0),(14,'wechat',2,3,999,10,10000,2,'救死扶伤可交换机',7,0);
/*!40000 ALTER TABLE `member_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `role_str` varchar(100) NOT NULL,
  `view_name` varchar(50) NOT NULL,
  `menu_group` varchar(20) NOT NULL,
  `weight` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1009 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (701,'调控操作日志','1/2','show_manipulate_log','强控输赢',7),(702,'单控玩家输赢','1/2','maniplate_single_player','强控输赢',7),(703,'调控全盘输赢','1/2','maniplate_full_handicaper','强控输赢',7),(401,'数据走势概括','1/2','get_game_data','运营分析',12),(402,'游戏盈利报表','1/2','get_sub_data','数据报表',3),(403,'数据分时对比','1/2','get_daily_data_detail','数据报表',3),(404,'游戏数据对比','1/2','game_data_compare','游戏数据',0),(8,'游戏参数设置','1','game_parameter_show','系统管理',1010),(803,'代理赠送数据','1/2','show_agent_presentation','数据报表',3),(507,'玩家游戏报表','1','player_game_detail_show','玩家管理',1),(904,'分销佣金结算','1/2','distribution_commission_init','代理管理',4),(501,'玩家操作日志','1','show_manage_log','玩家管理',1),(502,'玩家列表查看','1/2','manage_game_user','玩家管理',1),(503,'玩家信息详情','1','get_game_user_detail','玩家管理',1),(504,'访客权限管理','1','show_users_list','系统管理',11),(201,'赠送统计报表','1','get_daily_presentation','数据报表',3),(202,'赠送订单详情','1/2','get_detail_presentation','游戏数据',0),(203,'赠送参数设置','1','presented_config_init','系统管理',11),(1,'员工账号管理','1','get_user','系统管理',11),(2,'后台渠道管理','1','get_channel','系统管理',11),(3,'部门权限管理','1/2','menus_manage_show','系统管理',11),(4,'部门列表查看','1/2','get_role','系统管理',11),(601,'盈利亏损排行','1/2','show_profit_rank','游戏排行',6),(602,'金币买卖排行','1/2','show_point_rank','游戏排行',6),(603,'充值提现排行','1','show_withdraw_rank','游戏排行',6),(604,'玩家金币排行','1/2','show_gold_rank','游戏排行',6),(101,'充值提现报表','1/2','get_daily_topup','数据报表',3),(102,'充值订单详情','1/2','get_topup_order_detail','财务管理',2),(901,'分销参数设置','1/2','agent_distribution_init','系统管理',11),(405,'道具变更详情','1/2','get_item_change_data','游戏数据',0),(406,'账变记录详情','1/2','get_coin_change_data','游戏数据',0),(103,'钱包转账查询','1','transfer_coin','财务管理',2),(1002,'平台滚动公告','1/2','show_marquee','运营工具',10),(1001,'平台登录公告','1/2','show_annouce_game','运营工具',10),(1003,'平台内部邮件','1/2','show_mail_in_game','运营工具',10),(5,'系统操作日志','1','show_users_manage_log','系统管理',11),(505,'代理靓号设置','1','luck_page_init','代理管理',4),(1006,'平台活动管理','1/2','show_activity','运营工具',10),(1004,'平台状态管理','1','show_server_state','运营工具',10),(1005,'H5模拟登陆','1/2','h5_moni_login','运营工具',10),(104,'人工加款扣款','1/2','show_player_money_details','财务管理',2),(506,'玩家层级管理','1/2','member_level_details','玩家管理',1),(6,'游戏开关管理','1','game_platform_show','系统管理',11),(105,'商城代理管理','1','show_wx_agent','财务管理',2),(106,'收款通道管理','1','show_pay_channel','财务管理',2),(407,'卡号使用查询','1/2','show_card_data','游戏数据',0),(107,'提现订单管理','1/2','withdrawal_order_details','财务管理',2),(408,'对局日志详情','1/2','show_game_detail','游戏数据',0),(108,'运营状况概括','1/2','show_operat_state','运营分析',12),(1007,'充值优惠设置','1/2','recharge_discounts_show','运营工具',10),(801,'代理层级管理','1/2','agent_level_show','代理管理',4),(804,'代理列表查看','1/2','agent_list_show','代理管理',4),(805,'代理佣金结算','1','agent_commission_init','代理管理',4),(806,'代理添加管理','1/2','agent_add_show','代理管理',4),(7,'系统参数设置','1','system_parameter_show','系统管理',11),(1008,'游戏预警设置','1','alarm_config_show','运营工具',908);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `online_payment`
--

DROP TABLE IF EXISTS `online_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `online_payment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned DEFAULT NULL COMMENT 'æ¸ é“id',
  `pay_type` tinyint(4) DEFAULT NULL COMMENT 'æ”¯ä»˜ç±»åž‹',
  `api_name` varchar(50) DEFAULT NULL COMMENT 'æŽ¥å£åç§°',
  `api_id` varchar(50) DEFAULT NULL COMMENT 'æŽ¥å£ID',
  `api_url` varchar(1000) DEFAULT NULL COMMENT 'æŽ¥å£åŸŸå',
  `api_code` varchar(50) DEFAULT NULL COMMENT 'æŽ¥å£ä»£ç ',
  `merchant_code` varchar(1000) DEFAULT NULL COMMENT 'å•†æˆ·å·',
  `md5_key` varchar(1000) DEFAULT NULL COMMENT 'MD5 KEY',
  `public_key` varchar(5000) DEFAULT NULL COMMENT 'å…¬é’¥',
  `private_key` varchar(5000) DEFAULT NULL COMMENT 'ç§é’¥',
  `single_minimum` int(10) unsigned DEFAULT NULL COMMENT 'å•ç¬”æœ€ä½Ž',
  `single_highest` int(10) unsigned DEFAULT NULL COMMENT 'å•ç¬”æœ€é«˜',
  `stop_using_limit` int(10) unsigned DEFAULT NULL COMMENT 'å•æ—¥åœç”¨ä¸Šé™',
  `status` tinyint(4) DEFAULT NULL COMMENT 'çŠ¶æ€',
  `apply_level` varchar(1000) DEFAULT NULL COMMENT 'ä½¿ç”¨å±‚çº§',
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `pay_type` (`pay_type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='åœ¨çº¿æ”¯ä»˜';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `online_payment`
--

LOCK TABLES `online_payment` WRITE;
/*!40000 ALTER TABLE `online_payment` DISABLE KEYS */;
INSERT INTO `online_payment` VALUES (1,1,1,'11','22','33','55','66','','','7700',8800,9900,1,4,'44'),(2,1,1,'1','2','3','5','6','','','700',800,900,1,3,'4'),(3,1,1,'11111111111111111111111111111111111111111111111111','11111111111111111111111111111111111111111111111111','1','1','1','','','100',100,100,1,0,'1'),(4,1,1,'','id','url','','','','','0',0,0,1,0,''),(5,1,3,'1','3','2','4','','','5','6',700,800,900,1,'3'),(6,1,1,'','','','','','','','',0,0,0,1,''),(7,1,1,'','','','','','','','',0,0,0,0,''),(8,1,1,'','','','','','','','',0,0,0,0,''),(9,1,1,'','','','','','','','',0,0,0,0,''),(10,1,1,'','','','','','','','',0,0,0,1,''),(11,1,1,'','','','','','','','',0,0,0,0,''),(12,1,1,'','','','','','','','',0,0,0,1,''),(13,1,1,'','','','','','','','',0,0,0,1,''),(14,1,1,'','','','','','','','',0,0,0,0,'');
/*!40000 ALTER TABLE `online_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opt_log`
--

DROP TABLE IF EXISTS `opt_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opt_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel` int(10) unsigned NOT NULL COMMENT '渠道',
  `log_type` int(11) DEFAULT NULL COMMENT '日志类型 0单控玩家  1全盘操控',
  `operator` int(11) DEFAULT NULL COMMENT '操作员ID',
  `obj` int(11) DEFAULT NULL COMMENT '操作对象',
  `val` varchar(500) DEFAULT NULL COMMENT '操作数据',
  `timestamp` int(11) DEFAULT NULL COMMENT '操作时间',
  `maintype` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '大类 0输赢控制  1系统配置 2玩家相关  3财务相关',
  PRIMARY KEY (`id`),
  KEY `timestamp` (`timestamp`)
) ENGINE=MyISAM AUTO_INCREMENT=426 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opt_log`
--

LOCK TABLES `opt_log` WRITE;
/*!40000 ALTER TABLE `opt_log` DISABLE KEYS */;
INSERT INTO `opt_log` VALUES (31,1,2,1,1000042,'100000',1532351905,0),(32,1,2,1,1000042,'-1000000',1532351922,0),(33,1,3,1,1000042,'100000',1532351938,0),(34,1,3,1,1000042,'-100000',1532351956,0),(35,1,3,1,1000001,'1000000',1532413605,0),(36,1,3,1,1000001,'-1000000',1532413614,0),(37,1,3,1,1000001,'-600000',1532413626,0),(38,1,3,1,1000001,'-500000',1532413667,0),(39,1,2,1,1000001,'1000',1532413690,0),(40,1,2,1,1000001,'-1000',1532413709,0),(41,1,0,1,1000001,'1000000',1532415970,0),(42,1,0,1,1000001,'1000000',1532415995,0),(43,1,0,1,1000001,'1000000',1532416148,0),(44,1,0,1,1000001,'2000000',1532416415,0),(45,1,0,1,1000001,'1000000',1532416455,0),(46,1,0,1,1000001,'-5000000',1532416473,0),(47,1,0,1,1000001,'-1000000',1532418291,0),(48,1,1,1,82,'普通场_1000000',1532424462,0),(49,1,1,1,82,'普通场_1000000',1532424511,0),(50,2,1,1,82,'普通场--1000_1000000',1532428731,0),(51,2,1,1,82,'普通场--1000_1000000',1532428856,0),(52,2,1,1,82,'普通场--5000_1000000',1532428856,0),(53,2,1,1,91,'贫民场--2001_110000',1532428944,0),(54,2,1,1,82,'普通场--5000_100',1532429231,0),(55,2,1,1,82,'普通场--1000_100',1532429231,0),(56,2,1,1,82,'普通场--1000_1',1532429269,0),(57,2,1,1,82,'普通场--5000_1',1532429269,0),(58,1,1,1,82,'普通场--1000_1',1532429926,0),(59,1,1,1,82,'普通场--5000_1000000',1532430966,0),(60,1,1,1,82,'普通场--50000_-10000000',1532431008,0),(61,1,1,1,80,'普通场--1001_-44554881',1532487012,0),(62,1,1,1,80,'普通场--1001_500000',1532487070,0),(63,0,14,1,9,'1',1532487079,0),(64,2,1,1,85,'初级场--1001_-76846465',1532487091,0),(65,2,1,1,85,'初级场--1001_-500000',1532487262,0),(66,2,1,1,85,'初级场--1001_500000',1532487568,0),(67,2,1,1,87,'普通场--10000_-77463550',1532487751,0),(68,2,1,1,88,'普通场--1000_-1990520',1532488359,0),(69,2,1,1,88,'普通场--5000_-5976520',1532488448,0),(70,2,1,1,81,'4倍场--1001_-199896000',1532488564,0),(71,1,1,1,80,'普通场--1001_-11489999',1532488960,0),(72,1,1,1,80,'普通场--1001_20000000',1532488989,0),(73,1,1,1,80,'普通场--1001_23',1532489019,0),(74,1,1,1,80,'普通场--1001_-5505',1532489034,0),(75,1,1,1,82,'普通场--500000_500',1532489039,0),(76,2,1,1,80,'普通场--1001_-59198470',1532489064,0),(77,2,1,1,80,'普通场--1001_453645354354',1532489084,0),(78,2,1,1,80,'普通场--1001_-553635354354',1532489091,0),(79,1,1,1,80,'普通场--1001_-10994318',1532489126,0),(80,2,1,1,91,'老板场--2003_-108556458',1532489334,0),(81,2,1,1,82,'普通场--1000_-112498962',1532489488,0),(207,0,19,1,16,'1',1533700052,0),(83,1,1,1,80,'普通场--1001_9999800',1532499540,0),(84,2,1,1,80,'普通场--1001_999999982220',1532499554,0),(85,2,1,1,81,'4倍场--1001_-5143677400',1532499568,0),(86,2,1,1,80,'普通场--1001_-900000000000',1532499824,0),(87,2,1,1,80,'普通场--1001_-10000000',1532499830,0),(88,2,1,1,84,'普通场--1001_-50269000',1532499870,0),(89,2,1,1,84,'普通场--1001_-10000000',1532499968,0),(90,2,1,1,84,'普通场--1001_99989110',1532500401,0),(91,2,1,1,86,'初级房--1001_-98376800',1532500420,0),(92,2,1,1,80,'普通场--1001_110000000',1532500694,0),(93,2,1,1,85,'初级场--1001_1000000',1532500891,0),(94,2,1,1,85,'初级场--1001_-51025689',1532500933,0),(95,2,1,1,85,'初级场--1001_559978220',1532501396,0),(96,2,1,1,86,'初级房--1001_999411000',1532501413,0),(97,2,1,1,91,'贫民场--2001_-197032023',1532501440,0),(98,2,1,1,92,'普通场--1001_-12521039',1532501708,0),(99,2,1,1,90,'贫民场--3001_-100014660',1532504633,0),(100,2,1,1,90,'小资场--3002_-100201760',1532504720,0),(101,2,1,1,90,'小资场--3002_50000000',1532504726,0),(102,2,1,1,81,'4倍场--1001_4999988400',1532507217,0),(103,2,1,1,81,'4倍场--1001_50000000',1532507228,0),(104,1,1,1,82,'普通场--5000_1742929',1532514261,0),(105,1,1,1,82,'普通场--50000_10560750',1532514337,0),(106,1,1,1,82,'普通场--1000000_48961660000',1532514355,0),(107,1,1,1,82,'普通场--1000000_500000000',1532514371,0),(108,1,3,1,1000025,'500000',1532567318,0),(221,0,17,1,19,'1',1533726177,0),(110,0,15,1,1,'1',1532607132,0),(111,0,15,1,1,'1',1532607205,0),(112,0,15,7,1,'1',1532672175,0),(206,0,18,1,16,'1',1533700035,0),(205,0,17,1,15,'1',1533699800,0),(204,0,18,1,15,'1',1533697921,0),(203,0,17,1,14,'1',1533645885,0),(202,0,19,1,7,'1',1533645809,0),(201,0,17,1,14,'1',1533645781,0),(120,0,15,1,1,'1',1532677678,0),(121,0,15,1,4,'1',1532677704,0),(122,0,15,1,7,'1',1532677708,0),(123,0,15,1,12,'1',1532678308,0),(124,0,15,1,13,'1',1532679267,0),(125,0,15,1,7,'1',1532679081,0),(126,0,15,1,13,'1',1532680008,0),(127,0,15,1,1,'1',1532680027,0),(128,0,15,1,1,'1',1532680203,0),(129,0,15,7,7,'1',1532681137,0),(220,0,17,1,20,'1',1533726174,0),(219,0,19,1,17,'1',1533726172,0),(218,0,17,1,21,'1',1533711548,0),(217,0,17,1,22,'1',1533711546,0),(134,0,15,1,7,'1',1532690802,0),(135,0,15,1,11,'1',1532690981,0),(136,0,15,1,11,'1',1532690986,0),(137,2,1,1,92,'小资场--1002_-25005700',1532693085,0),(138,2,1,1,92,'小资场--1002_-9999999999',1532693097,0),(139,2,1,1,92,'普通场--1001_-110000480',1532693107,0),(140,2,1,1,92,'小资场--1002_9999997999',1532693175,0),(141,2,1,1,92,'小资场--1002_-10000064879',1532693244,0),(142,2,1,1,92,'小资场--1002_10000057919',1532693374,0),(143,2,1,1,92,'小资场--1002_-9999779879',1532693415,0),(144,2,1,1,92,'小资场--1002_-328000',1532693427,0),(145,2,1,1,92,'小资场--1002_188280',1532693492,0),(146,2,1,1,92,'小资场--1002_5720',1532693566,0),(147,2,1,1,92,'小资场--1002_109128084',1532695210,0),(148,2,1,1,92,'小资场--1002_109128084',1532695217,0),(149,0,15,1,11,'1',1532917764,0),(150,0,14,1,4,'1',1532917766,0),(151,1,3,1,1000219,'100000',1532954623,0),(152,1,3,1,1000221,'100000',1532955105,0),(153,1,3,1,1000222,'100000',1532955319,0),(154,1,3,1,1000224,'1000000000',1532955395,0),(155,7,3,1,1000001,'1000000',1533126421,0),(156,7,3,1,1000001,'1000000',1533127468,0),(157,1,3,1,1000001,'1000000',1533128313,0),(158,7,3,1,1000001,'1000000',1533128337,0),(159,1,13,1,1000003,'',1533178432,0),(160,1,13,1,1000005,'',1533192753,0),(161,1,13,1,1000005,'',1533192763,0),(200,0,19,1,14,'1',1533645620,0),(196,0,16,17,7,'2',1533642706,0),(195,0,16,1,13,'1',1533642575,0),(194,0,15,1,13,'1',1533642497,0),(193,0,14,1,11,'1',1533642471,0),(168,1,12,1,1000024,'',1533203781,0),(169,7,3,1,1000024,'-200000',1533568679,0),(170,7,3,1,1000024,'-100000',1533568716,0),(171,7,3,1,1000024,'-200000',1533569086,0),(172,7,3,1,1000024,'-200000',1533569124,0),(173,7,3,1,1000024,'-200000',1533569184,0),(216,0,17,1,23,'1',1533711543,0),(215,0,18,1,17,'1',1533711528,0),(214,0,18,1,17,'1',1533711528,0),(213,0,18,1,17,'1',1533711527,0),(212,0,18,1,17,'1',1533711527,0),(211,0,18,1,17,'1',1533711527,0),(210,0,18,1,17,'1',1533711527,0),(209,0,18,1,17,'1',1533711527,0),(208,0,19,1,8,'1',1533700282,0),(191,0,15,1,7,'1',1533641417,0),(184,0,15,1,13,'1',1533611776,0),(185,0,15,1,13,'1',1533612886,0),(186,0,15,1,13,'1',1533612926,0),(187,0,15,1,16,'1',1533612450,0),(188,0,15,1,16,'1',1533612482,0),(192,0,15,1,17,'1',1533642302,0),(190,0,14,1,16,'1',1533632952,0),(222,0,17,1,18,'1',1533726179,0),(223,0,19,1,17,'1',1533785368,0),(224,0,19,1,17,'1',1533785376,0),(225,0,19,1,17,'1',1533785379,0),(226,0,19,1,16,'1',1533785405,0),(227,0,19,1,16,'1',1533785428,0),(228,0,19,1,16,'1',1533786480,0),(229,0,19,1,10,'1',1533786487,0),(230,0,19,1,7,'1',1533786491,0),(231,0,19,1,8,'1',1533786495,0),(232,0,19,1,1,'1',1533786499,0),(233,0,19,1,8,'1',1533797400,0),(234,0,19,1,8,'1',1533867900,0),(235,0,19,1,8,'1',1533867942,0),(236,0,19,1,8,'1',1533868157,0),(237,0,19,1,8,'1',1533868763,0),(238,0,19,1,8,'1',1533868770,0),(239,7,6,1,1000002,'',1533887055,0),(240,7,7,1,1000002,'',1533887057,0),(241,7,8,1,1000002,'',1533887059,0),(242,7,9,1,1000002,'',1533887062,0),(243,7,9,1,1000002,'',1533887070,0),(244,7,8,1,1000002,'',1533887080,0),(245,7,9,1,1000002,'',1533887081,0),(246,7,7,1,1000002,'',1533887081,0),(247,7,9,1,1000068,'',1533887126,0),(248,7,7,1,1000068,'',1533887128,0),(249,7,1,1,82,'普通场--1000_163243890',1533890813,0),(250,0,16,1,7,'1',1533901240,0),(251,0,16,1,7,'1',1533901244,0),(252,0,16,1,17,'1',1533901252,0),(253,1,7,17,1000000,'',1533902365,0),(254,1,6,17,1000000,'',1533902369,0),(255,1,7,17,1000000,'',1533902373,0),(256,1,13,17,1000000,'',1533902379,0),(257,0,19,1,10,'1',1534247616,0),(258,0,16,1,7,'1',1534247637,0),(259,7,1,1,82,'普通场--5000_1000000',1534326156,0),(260,7,1,1,82,'普通场--1000_1000000',1534326212,0),(261,7,1,1,82,'普通场--1000_6345260',1534326230,0),(262,7,1,1,82,'普通场--1000_2200000',1534327957,0),(263,0,18,1,24,'1',1534389771,0),(264,0,16,1,16,'1',1534767167,0),(265,0,19,1,10,'1',1535082354,0),(266,0,16,1,16,'1',1535103876,0),(267,0,18,1,25,'1',1535618942,0),(268,0,16,1,7,'1',1535620792,0),(269,0,16,1,7,'1',1535620971,0),(270,0,16,1,7,'1',1535620988,0),(271,0,19,1,24,'1',1535621986,0),(272,0,18,1,26,'1',1535622519,0),(273,7,3,1,313131,'1',1535704731,0),(274,7,3,1,313131,'1',1535704787,0),(275,7,3,1,313131,'1',1535704794,0),(276,7,3,1,313131,'1',1535704813,0),(277,7,3,1,313131,'1111',1535704831,0),(278,10,3,1,1000008,'21',1535705078,0),(279,10,3,1,1000008,'1000',1535705251,0),(280,10,3,1,1000008,'1',1535706547,0),(281,10,2,1,1000008,'2',1535706551,0),(282,10,12,1,1000008,'',1535706604,0),(283,10,12,1,1000008,'',1535706607,0),(284,10,3,1,1000008,'1,10,阿斗',1535706796,0),(285,10,2,1,1000008,'13',1535707077,0),(286,10,3,1,1000008,'2--8888--efhfsbh',1535707721,0),(287,10,2,1,1000008,'1--34',1535708954,0),(288,10,2,1,1000008,'2--2222',1535708988,0),(289,10,12,1,1000008,'',1535709082,0),(290,10,3,1,1000008,'1--11--11',1535709339,0),(291,10,3,1,1000008,'1--100--kgfk',1535711983,0),(292,10,3,1,1000008,'1---100--hjgh',1535712719,0),(293,10,3,1,1000008,'1---100--刚刚好',1535712889,0),(294,10,3,1,1000008,'1--100--gg',1535712960,0),(295,10,3,1,1000008,'1--100--gg',1535713097,0),(296,10,3,1,1000008,'1--1000--utth',1535713454,0),(297,10,3,1,1000008,'1--1000--yjuj',1535713596,0),(298,10,3,1,1000008,'1--1000--yjuj',1535714000,0),(299,10,3,1,1000008,'3---100--trfh',1535714284,0),(300,7,3,1,1000008,'1--100--tr',1535714610,0),(301,10,3,1,1000008,'1--11--2121',1535714638,0),(302,7,3,1,1000008,'1--2000--ghhgf',1535714642,0),(303,7,3,1,1000008,'1--11--212',1535714682,0),(304,7,3,1,1000008,'3---100--qwgd',1535714697,0),(305,7,3,1,1000008,'1--1--人太多',1535714738,0),(306,7,3,1,1000008,'1--1000--刚刚好',1535714832,0),(307,7,3,1,1000008,'4---80--rjh',1535714855,0),(308,7,3,1,1000008,'1--88--ksdj',1535714907,0),(309,7,3,1,1000008,'1--111--fsdf',1535715200,0),(310,7,3,1,1000008,'1--100--ghrth',1535715216,0),(311,7,3,1,1000008,'1--10000--fsdfs',1535715330,0),(312,10,3,1,1000008,'1--100--sf',1535716048,0),(313,7,3,1,1000008,'1--100--dfgdgf',1535716065,0),(314,7,3,1,1000008,'3---100--safsf',1535716170,0),(315,7,3,1,1000008,'1--21--ddfds',1535716398,0),(316,7,3,1,1000008,'1--1111--23',1535716473,0),(317,7,3,1,1000008,'1--111111--dfsdf',1535716477,0),(318,7,3,1,1000008,'1--1000--gfdgd',1535716486,0),(319,7,3,1,1000008,'1--12--  1',1535716532,0),(320,7,3,1,1000008,'1--53453-- 13',1535716537,0),(321,7,3,1,1000008,'1--31--ds',1535716549,0),(322,7,3,1,1000008,'1--3131--sdfs',1535716570,0),(323,7,3,1,1000008,'3---2131--ad',1535716577,0),(324,7,3,1,1000008,'1--2121--fdsf',1535716618,0),(325,7,3,1,1000008,'1--3131314--ewqe',1535716640,0),(326,7,3,1,1000008,'1---103131--ew',1535716646,0),(327,7,3,1,1000008,'4---11--1',1535716752,0),(328,7,3,1,1000008,'1--1000--rgr',1535720400,0),(329,7,3,1,1000008,'2--1--dgf',1535720418,0),(330,7,3,1,1000008,'3---1--dfsg',1535720431,0),(331,7,3,1,1000008,'4---1--fg',1535720438,0),(332,7,3,1,1000008,'1--1--dfgs',1535720448,0),(333,7,3,1,1000008,'3---1--rgerh',1535720455,0),(334,7,3,1,1000008,'4---100--gfd',1535720464,0),(335,1,5,1,90001,'',1536147252,2),(336,1,10,1,90001,'',1536148032,2),(337,1,5,1,90001,'',1536148034,2),(338,1,4,1,90001,'',1536148070,2),(339,1,10,1,90001,'',1536148247,2),(340,1,5,1,90001,'',1536148257,2),(341,1,4,1,90001,'',1536148265,2),(342,1,10,1,90001,'',1536148273,2),(343,1,11,1,90001,'',1536148293,2),(344,1,5,1,90001,'',1536148830,2),(345,1,4,1,90001,'',1536148840,2),(346,1,10,1,90001,'',1536148849,2),(347,1,11,1,90001,'',1536148856,2),(348,1,5,1,90001,'',1536149020,2),(349,1,4,1,90001,'',1536149165,2),(350,0,17,1,25,'1',1536149167,1),(351,1,10,1,90001,'',1536149168,2),(352,1,11,1,90001,'',1536149171,2),(353,1,4,1,90001,'',1536149174,2),(354,1,11,1,90001,'',1536149176,2),(355,0,19,1,1,'1',1536149231,1),(356,1,5,1,90001,'',1536149235,2),(357,1,10,1,90001,'',1536150255,2),(358,1,5,1,90001,'',1536195791,2),(359,1,10,1,90001,'',1536195795,2),(360,1,5,1,90001,'',1536196077,2),(361,1,5,1,90001,'',1536196255,2),(362,1,10,1,90001,'',1536196259,2),(363,1,5,1,90001,'',1536196263,2),(364,1,5,1,90001,'',1536196265,2),(365,1,10,1,90001,'',1536196286,2),(366,1,5,1,90001,'',1536196290,2),(367,1,4,1,90001,'',1536196915,2),(368,1,4,1,90001,'',1536197078,2),(369,1,11,1,90001,'',1536197089,2),(370,1,4,1,90001,'',1536197212,2),(371,1,4,1,90001,'',1536199637,2),(372,1,11,1,90001,'',1536199640,2),(373,1,4,1,90001,'',1536199642,2),(374,1,10,1,90001,'',1536200503,2),(375,1,5,1,90001,'',1536200900,2),(376,1,5,1,90001,'',1536200936,2),(377,1,5,1,90001,'',1536200963,2),(378,1,10,1,90001,'',1536200969,2),(379,1,11,1,90001,'',1536200973,2),(380,1,5,1,90001,'',1536201456,2),(381,1,5,1,90001,'',1536201996,2),(382,1,4,1,90001,'',1536201996,2),(383,1,4,1,90001,'',1536202113,2),(384,1,4,1,90001,'',1536202145,2),(385,1,5,1,90001,'',1536202161,2),(386,0,19,1,7,'1',1536218409,0),(387,7,1,1,94,'普通场--100_520',1536218763,0),(388,7,1,1,94,'普通场--100_5200000',1536218775,0),(389,0,19,1,7,'1',1536247449,1),(390,1,10,1,90001,'',1536283526,2),(391,1,11,1,90001,'',1536283528,2),(392,0,19,1,1,'1',1536287185,1),(393,0,18,1,27,'1',1536288813,1),(394,0,17,1,26,'1',1536288881,1),(395,0,19,1,27,'1',1536288922,1),(396,1,5,1,90001,'',1536307809,2),(397,1,4,1,90001,'',1536313824,2),(398,1,10,1,90001,'',1536313830,2),(399,1,5,1,90001,'',1536313838,2),(400,0,19,1,1,'1',1537862426,1),(401,0,19,1,1,'1',1537864552,1),(402,0,19,1,7,'1',1537929652,1),(403,0,19,1,7,'1',1537930134,1),(404,1,5,1,90001,'',1537945578,2),(405,1,5,1,90001,'',1537945613,2),(406,1,5,1,90001,'',1537945623,2),(407,1,5,1,90001,'',1537945786,2),(408,1,5,1,1000008,'',1537946183,2),(409,1,5,1,1000008,'',1537946232,2),(410,1,5,1,1000008,'',1537946251,2),(411,1,5,1,1000008,'',1537946277,2),(412,1,5,1,1000001,'',1537946283,2),(413,1,5,1,1000001,'',1537946291,2),(414,7,13,1,1000001,'MM11',1538021694,2),(415,7,2,1,1000001,'1--1',1538022149,2),(416,0,19,1,1,'1',1538960909,1),(417,0,19,1,1,'1',1538961190,1),(418,0,19,1,1,'1',1538974592,1),(419,0,19,1,7,'1',1539259116,1),(420,0,19,1,7,'1',1539259157,1),(421,0,19,1,1,'1',1539743605,1),(422,0,19,1,1,'1',1539759914,1),(423,0,19,1,1,'1',1539845271,1),(424,0,19,1,1,'1',1539845588,1),(425,0,19,1,1,'1',1539867220,1);
/*!40000 ALTER TABLE `opt_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pay_channel`
--

DROP TABLE IF EXISTS `pay_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pay_channel` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel` int(10) unsigned DEFAULT NULL COMMENT '渠道',
  `name` varchar(50) DEFAULT NULL COMMENT '通道名字',
  `player_lv` varchar(100) DEFAULT NULL COMMENT '匹配玩家等级',
  `min_recharge` int(11) DEFAULT NULL COMMENT '最小充值',
  `max_recharge` int(11) DEFAULT NULL COMMENT '最大充值',
  `pay_type` int(11) DEFAULT NULL COMMENT '支付方式 0银行卡转账  1支付宝支付  2微信支付 3qq支付',
  `receipt_type` int(11) DEFAULT NULL COMMENT '收款方式 0银行卡收款  1支付宝二维码 2支付宝账号 3微信二维码 4qq二维码',
  `config` varchar(300) DEFAULT NULL COMMENT '收款方式详情 json格式 ',
  `commission` int(11) DEFAULT NULL COMMENT '手续费 百分比',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  `decimal_open` tinyint(4) DEFAULT NULL COMMENT '小数点开启',
  `memo` varchar(100) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `player_lv` (`player_lv`) USING BTREE,
  KEY `channel` (`channel`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COMMENT='支付通道';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_channel`
--

LOCK TABLES `pay_channel` WRITE;
/*!40000 ALTER TABLE `pay_channel` DISABLE KEYS */;
INSERT INTO `pay_channel` VALUES (8,1,'1','3,4,6,7',11,22,-1,3,'{\"receipt_bank\":\"微信\",\"receipt_name\":\"212\",\"receipt_account\":\"321312\",\"file_name\":\"\"}',NULL,0,0,'111222'),(9,1,'通道名称','8',22,33,1,2,'{\"receipt_bank\":\"支付宝\",\"receipt_name\":\"收款户名\",\"receipt_account\":\"收款账号\"}',NULL,0,0,''),(10,1,'2131','3,4',11,22,0,0,'{\"receipt_bank\":\"农业银行\",\"receipt_address\":\"地址\",\"receipt_name\":\"户名\",\"receipt_account\":\"账号\"}',88888,1,1,''),(11,7,'通道名称','None',22,33,1,2,'{\"receipt_bank\":\"支付宝\",\"receipt_name\":\"户名\",\"receipt_account\":\"账号\"}',11,0,1,''),(12,1,'313','3,4',1,1,2,3,'{\"receipt_bank\":\"微信\",\"receipt_name\":\"户名\",\"receipt_account\":\"讽德诵功\"}',NULL,0,0,''),(13,1,'name','3,4',11,22,0,0,'{\"receipt_bank\":\"建设银行\",\"receipt_address\":\"dizhi\",\"receipt_name\":\"huming\",\"receipt_account\":\"42342\"}',NULL,0,0,''),(19,1,'啊我觉得和环境','3,4',10,20,0,2,'{\"receipt_bank\":\"支付宝\",\"receipt_name\":\"awdaw\",\"receipt_account\":\"\"}',NULL,0,1,''),(21,1,'打哈哈','4,5',10,10,-1,2,'{\"receipt_bank\":\"支付宝\",\"receipt_name\":\"awd\",\"receipt_account\":\"\"}',NULL,0,1,''),(22,1,'哈登哈登','2,3',10,10,-1,2,'{\"receipt_bank\":\"支付宝\",\"receipt_name\":\"awd\",\"receipt_account\":\"\"}',NULL,0,1,''),(23,1,'i热帖即热','3,4',10,10,-1,3,'{\"receipt_bank\":\"微信\",\"receipt_name\":\"rgerg\",\"receipt_account\":\"\",\"file_name\":\"\"}',NULL,0,0,''),(24,1,'ajsd','2,3,4',21,13,-1,0,'{\"receipt_bank\":\"广发银行\",\"receipt_address\":\"123\",\"receipt_name\":\"123\",\"receipt_account\":\"123\",\"file_name\":\"\"}',NULL,0,1,'');
/*!40000 ALTER TABLE `pay_channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presented_config`
--

DROP TABLE IF EXISTS `presented_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `presented_config` (
  `channel` int(10) unsigned NOT NULL COMMENT '渠道',
  `config` blob COMMENT '配置',
  PRIMARY KEY (`channel`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presented_config`
--

LOCK TABLES `presented_config` WRITE;
/*!40000 ALTER TABLE `presented_config` DISABLE KEYS */;
INSERT INTO `presented_config` VALUES (1,'{\"a2p\": 1, \"p2a_min_coin\": 1, \"p2a_tax\": 0, \"p2a\": 1, \"a2p_min_coin\": 1, \"p2p_tax\": 100, \"a2a_min_coin\": 1, \"p2a_max_coin\": 10000000, \"a2a\": 1, \"p2p_max_coin\": 10000000, \"a2p_max_coin\": 10000000, \"p2p\": 1, \"a2p_tax\": 100, \"a2a_max_coin\": 10000000, \"p_coin\": 0, \"a2a_tax\": 0, \"p2p_min_coin\": 1, \"max_presented_times\": 999}'),(7,'{\"a2p\": 0, \"p2a\": 1, \"a2a\": 1, \"p2p\": 1, \"min_coin\": 10000, \"p_coin\": 0, \"a2a_tax\": 0, \"p2a_tax\": 100, \"p2p_tax\": 100, \"max_coin\": 9999999999, \"a2p_tax\": 100, \"max_presented_times\": 999}'),(10,'{\"a2p\": 1, \"p2a\": 1, \"a2a\": 1, \"p2p\": 1, \"min_coin\": 2, \"p_coin\": 22, \"a2a_tax\": 1, \"p2a_tax\": 1, \"p2p_tax\": 1, \"max_coin\": 2222, \"a2p_tax\": 111, \"max_presented_times\": 11}'),(24,'{\"a2p\": 1, \"p2a_min_coin\": 1, \"p2a_tax\": 0, \"p2a\": 1, \"a2p_min_coin\": 1, \"p2p_tax\": 100, \"a2a_min_coin\": 1, \"p2a_max_coin\": 10000000, \"a2a\": 1, \"p2p_max_coin\": 10000000, \"a2p_max_coin\": 10000000, \"p2p\": 1, \"a2p_tax\": 100, \"a2a_max_coin\": 10000000, \"p_coin\": 0, \"a2a_tax\": 0, \"p2p_min_coin\": 1, \"max_presented_times\": 999}');
/*!40000 ALTER TABLE `presented_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recharge_discounts`
--

DROP TABLE IF EXISTS `recharge_discounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recharge_discounts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `user_id` int(10) unsigned NOT NULL COMMENT '生成者账号id',
  `priority` tinyint(3) unsigned DEFAULT NULL COMMENT '优先级',
  `activity_title` varchar(100) DEFAULT NULL COMMENT '活动标题',
  `activity_content` varchar(5000) DEFAULT NULL COMMENT '活动内容描述',
  `activity_type` tinyint(4) DEFAULT NULL COMMENT '活动类型',
  `participation_member` tinyint(4) DEFAULT NULL COMMENT '参与会员',
  `title_picture_url` varchar(500) DEFAULT NULL COMMENT '活动标题图片链接',
  `show_picture_url` varchar(500) DEFAULT NULL COMMENT '展示图片链接',
  `begin_time` int(10) unsigned DEFAULT NULL COMMENT '开始时间',
  `end_time` int(10) unsigned DEFAULT NULL COMMENT '结束时间',
  `push_time_begin` int(10) unsigned DEFAULT NULL COMMENT '开始推送时间',
  `push_time_end` int(10) unsigned DEFAULT NULL COMMENT '结束推送时间',
  `participation_level` varchar(500) DEFAULT NULL COMMENT '参与层级',
  `recharge_detail` varchar(1000) DEFAULT NULL COMMENT '充值详情',
  `push_times` int(10) unsigned DEFAULT NULL COMMENT '推送次数',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  PRIMARY KEY (`id`),
  KEY `channel_id` (`channel_id`) USING BTREE,
  KEY `begin_time` (`begin_time`) USING BTREE,
  KEY `end_time` (`end_time`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `activity_title` (`activity_title`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='充值优惠';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recharge_discounts`
--

LOCK TABLES `recharge_discounts` WRITE;
/*!40000 ALTER TABLE `recharge_discounts` DISABLE KEYS */;
INSERT INTO `recharge_discounts` VALUES (4,7,1,2,'标题111','<p>内容描述111</p>',2,2,'biaoti_lianjie111','zhanshi_lianjie111',1535848272,1535934675,1536021077,1536107478,'1','[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]',1,0),(5,7,1,2,'标题','<p>内容描述</p>',2,2,'标题链接','展示链接',1538020267,1538365870,1538193076,1538279477,'1,12,14','[[35, 44, 456, 768, 0], [78, 54, 876, 78, 7]]',36,2),(6,7,1,1,'标题','<p>1</p>',1,1,'biaoti_lianjie','zhanshi_lianjie',1535602402,1536898403,1538280810,1538367212,'12,14','[[1, 1, 1, 1, 1]]',3,2),(7,7,1,1,'额外的','<p>dawadw</p>',1,2,'标题链接','展示链接',1538609743,1538868946,1538609750,1538868951,'1,12','[[12, 12, 12, 12, 12]]',3,0);
/*!40000 ALTER TABLE `recharge_discounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `parent_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (2,'聚豪管理员',1),(5,'爆豪开发组',2),(6,'聚豪代理',2),(7,'wechat',1),(11,'2121',1),(12,'管理员组',6),(13,'2121',6),(14,'11111',6);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_parameter`
--

DROP TABLE IF EXISTS `system_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_parameter` (
  `channel_id` int(10) unsigned NOT NULL COMMENT '渠道id',
  `agent_pattern` tinyint(4) DEFAULT NULL COMMENT '代理模式',
  `default_level` int(10) unsigned DEFAULT NULL COMMENT '默认层级',
  `phone_service_url` varchar(500) DEFAULT NULL COMMENT '手机客服链接',
  PRIMARY KEY (`channel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系统参数';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_parameter`
--

LOCK TABLES `system_parameter` WRITE;
/*!40000 ALTER TABLE `system_parameter` DISABLE KEYS */;
INSERT INTO `system_parameter` VALUES (1,1,2,'却无法前端我'),(7,2,1,''),(8,3,0,'');
/*!40000 ALTER TABLE `system_parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT '',
  `nick` varchar(20) NOT NULL DEFAULT '' COMMENT '员工昵称',
  `password` varchar(100) NOT NULL,
  `regi_time` int(20) DEFAULT '0',
  `access_level` tinyint(5) DEFAULT '1' COMMENT '账号权限等级',
  `last_login_time` int(20) DEFAULT '0',
  `last_logout_time` int(20) DEFAULT '0',
  `role_str` varchar(100) NOT NULL,
  `is_delete` tinyint(5) DEFAULT '0' COMMENT '账号是否被删除',
  `status` tinyint(5) DEFAULT '1',
  `secret_key` varchar(100) DEFAULT NULL COMMENT 'secret key',
  `game_player_id` varchar(100) DEFAULT NULL COMMENT 'ç»‘å®šæ¸¸æˆè´¦å·ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','初始管理员','pbkdf2:sha256:50000$h02TSIsv$6cc775b8d8f8bdd8569eb15dfe8be1ca13ae8e1dbfba10172f38319a27f7b8a8',1538128531,1,1542766048,1542700737,'1',0,0,'',NULL),(5,'test02','都是sd','pbkdf2:sha256:50000$J1BEWd8w$b57e6e69385dcf9485ab46611dcbed40bb7f50afb61254d3e99db3c7874cdbf1',1532487109,0,1534250792,1542701932,'1/5/7',0,1,'',NULL),(17,'asd','都是sd','pbkdf2:sha256:50000$Y0N686n8$d7180424fdaa522973a20446930d778ea23eba2dd8110d536a75058efc78c7f7',1533642302,0,1536658635,1536658637,'2',0,1,NULL,NULL),(11,'juhao_test','都是sd','pbkdf2:sha256:50000$d9GcfKFA$ea421865eb3853a930c6c4ebffdf7973bac17422ce19b2ddd4896165571c4d50',1532601002,0,1532672568,1532672575,'2',0,1,NULL,NULL),(13,'juhao_operator','都是sd','pbkdf2:sha256:50000$4U4XGqQ0$5faa2d12ba95cd304219301344ce4a56345c8a1772df669de9e9d5378ee5713b',1532679267,1,1534729205,1534737139,'1',0,1,NULL,NULL),(16,'123','123','pbkdf2:sha256:50000$DmXcD3VX$10b9b99c6df2bad17e6186a80536e039523b277991b693cee1d7952ef7f14d3f',1533612450,0,1537878405,1537878419,'1',0,1,'',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `white_list`
--

DROP TABLE IF EXISTS `white_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `white_list` (
  `pid` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `channel` varchar(20) NOT NULL DEFAULT '' COMMENT '渠道',
  `nick` varchar(50) NOT NULL DEFAULT '' COMMENT '玩家名',
  `game_count` int(5) NOT NULL COMMENT '游戏局数',
  `coin` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '金币',
  `counter` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '保险柜金币',
  `total_recharge_rmb` bigint(22) NOT NULL DEFAULT '0' COMMENT '累计充值RMB数量(分)',
  `total_withdraw` bigint(20) DEFAULT '0' COMMENT '总共提现',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `white_list`
--

LOCK TABLES `white_list` WRITE;
/*!40000 ALTER TABLE `white_list` DISABLE KEYS */;
INSERT INTO `white_list` VALUES (90001,'1','孤独、',0,0,0,0,0,'他天后方可');
/*!40000 ALTER TABLE `white_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `withdraw_deposit_order_form`
--

DROP TABLE IF EXISTS `withdraw_deposit_order_form`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `withdraw_deposit_order_form` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(10) unsigned DEFAULT NULL COMMENT '会员账号',
  `member_level` int(10) unsigned DEFAULT NULL COMMENT '会员层级',
  `withdraw_deposit_id` bigint(20) unsigned DEFAULT NULL COMMENT '提现单号',
  `withdraw_deposit_type` tinyint(4) DEFAULT NULL COMMENT '提现类型',
  `withdraw_deposit_money` int(10) unsigned DEFAULT NULL COMMENT '提现金额',
  `application_time` int(10) unsigned DEFAULT NULL COMMENT '申请时间',
  `service_charge` int(10) unsigned DEFAULT NULL COMMENT '手续费',
  `platform_withhold` int(10) unsigned DEFAULT NULL COMMENT '平台扣款',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  `dispose_time` int(10) unsigned DEFAULT NULL COMMENT '处理时间',
  `dispose_user` int(10) unsigned DEFAULT NULL COMMENT '处理人',
  `remark` varchar(100) DEFAULT NULL COMMENT '备注',
  `payee` varchar(10) DEFAULT NULL COMMENT '收款人',
  `due_bank` varchar(15) DEFAULT NULL COMMENT '收款银行',
  `gathering_account` bigint(20) unsigned DEFAULT NULL COMMENT '收款账号',
  `open_account_address` varchar(100) DEFAULT NULL COMMENT '开户地址',
  `failed_reason` varchar(100) DEFAULT NULL COMMENT '失败原因',
  `channel_id` int(10) unsigned DEFAULT NULL COMMENT '渠道id',
  PRIMARY KEY (`id`),
  KEY `withdraw_deposit_type` (`withdraw_deposit_type`) USING BTREE,
  KEY `status` (`status`) USING BTREE,
  KEY `application_time` (`application_time`) USING BTREE,
  KEY `pid` (`pid`) USING BTREE,
  KEY `channel_id` (`channel_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='提现订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `withdraw_deposit_order_form`
--

LOCK TABLES `withdraw_deposit_order_form` WRITE;
/*!40000 ALTER TABLE `withdraw_deposit_order_form` DISABLE KEYS */;
INSERT INTO `withdraw_deposit_order_form` VALUES (1,90001,1,1809051000000,1,8888888,1537932867,1000,54200,1,1536743191,1,'划分开来','诸葛亮','浦发银行',6632450810000,'地球村','',1),(2,90001,1,1809051000000,1,8888888,1537932864,NULL,NULL,2,1536743244,1,'热热','诸葛亮','浦发银行',6632450810000,'地球村','割让给',1),(3,90001,1,1809051000000,1,8888888,1537932861,5400,2500,1,1536922165,16,'','诸葛亮','浦发银行',6632450810000,'地球村','',1),(4,90001,1,1809051000000,1,8888888,1537932866,NULL,NULL,3,NULL,NULL,'','诸葛亮','浦发银行',6632450810000,'地球村','',1),(5,90001,1,1809051000000,1,8888888,1537932862,NULL,NULL,3,NULL,NULL,'','诸葛亮','浦发银行',6632450810000,'地球村','',1),(6,90001,1,1809051000000,1,8888888,1537932869,NULL,NULL,3,NULL,NULL,'','诸葛亮','浦发银行',6632450810000,'地球村','',1),(7,90001,1,1809051000000,1,8888888,4294967295,NULL,NULL,3,NULL,NULL,'','诸葛亮','浦发银行',6632450810000,'地球村','',1),(8,90001,1,1809051000000,1,8888888,1537932863,1000,54200,3,NULL,1,'划分开来','诸葛亮','浦发银行',6632450810000,'地球村','',1);
/*!40000 ALTER TABLE `withdraw_deposit_order_form` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wx_agent`
--

DROP TABLE IF EXISTS `wx_agent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wx_agent` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `wx` varchar(50) DEFAULT NULL COMMENT '微信号',
  `seq` int(11) DEFAULT NULL COMMENT '顺序号',
  `status` tinyint(4) DEFAULT NULL COMMENT '状态',
  `channel` int(10) unsigned DEFAULT NULL COMMENT '渠道',
  `memo` varchar(100) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `wx` (`wx`) USING BTREE,
  KEY `channel` (`channel`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='微信代理';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wx_agent`
--

LOCK TABLES `wx_agent` WRITE;
/*!40000 ALTER TABLE `wx_agent` DISABLE KEYS */;
INSERT INTO `wx_agent` VALUES (1,'11',22,1,1,'33'),(2,'11111',11122,0,1,'23'),(3,'aaa',1,0,1,''),(4,'1',2,0,1,'3'),(5,'3',3,0,1,'3'),(6,'111',222,0,1,'333'),(7,'31313',75675757,0,1,'3'),(8,'1534535',12,1,1,'1'),(9,'9',8,0,1,'7'),(10,'111222',22,1,1,'3'),(11,'88',88,0,1,'88'),(12,'99',99,1,1,'99'),(13,'77',77,0,1,'77'),(14,'66',66,1,1,'66'),(15,'55',55,0,1,'55'),(16,'44',44,1,1,'44'),(17,'133',1,0,10,'1'),(18,'ferf',2131,0,1,'3131'),(19,'3131',3131,0,1,'3131');
/*!40000 ALTER TABLE `wx_agent` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-21 11:44:57
