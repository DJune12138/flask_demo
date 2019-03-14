# -*- coding:utf-8 -*-
import time
from zs_backend.sql import SqlOperate
from zs_backend.busi import busi
from zs_backend.utils.channel_qry import LogQry
from zs_backend.utils.common import login_require
from flask import render_template, request, jsonify, session
from zs_backend.utils import time_util
from zs_backend.utils import httpc_util

import os,sys
import urllib, urllib2, zipfile
import subprocess
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
import traceback
from copy import deepcopy

# 初始化
language = 'CH'
endpoint = 'oss-cn-shenzhen.aliyuncs.com'
access_key_id = 'LTAI59gZRaI225ly'
access_key_secret = 'mvEtfXL6PC6zjnqEMBsqzPQbtV5Rlj'
cdn_server_address = 'https://cdn.aliyuncs.com'
bucket = "zslm-source"

user_params = {}
user_params['action'] = 'RefreshObjectCaches'
user_params['ObjectType'] = 'Directory'
user_params['ObjectPath'] = "https://admin.ffc427.cn/%s/"

class Refresh:
    def __init__(self,access_key_id,access_key_secret):

        self.__secretid = access_key_id
        self.__secretkey = access_key_secret

    def percent_encode(self,str):
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    #计算签名
    def compute_signature(self, parameters, access_key_secret):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])

        h = hmac.new(access_key_secret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def compose_url(self,user_params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2014-11-11', \
            'AccessKeyId'   : self.__secretid, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'TimeStamp'         : timestamp, \
        }

        for key in user_params.keys():
            parameters[key] = user_params[key]

        signature = self.compute_signature(parameters, self.__secretkey)
        parameters['Signature'] = signature
        url = cdn_server_address + "/?" + urllib.urlencode(parameters)
        return url

    def make_request(self, user_params, quiet=False):
        url = self.compose_url(user_params)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        print(response.read())

def addOSS(channel, uploadpath, base_url, dest_path):
    config=subprocess.call("/usr/bin/ossutil config -L %s -e %s -i %s -k %s --output-dir=/root/" \
    	% (language, endpoint, access_key_id, access_key_secret), shell=True)

    ## 提交配置
    cmd = "/usr/bin/ossutil cp -rf %s oss://%s%s" % (uploadpath, bucket, dest_path)
    result=subprocess.call(cmd, shell=True)
    print(uploadpath, cmd, result)

    recdn = Refresh(access_key_id, access_key_secret)
    dd = deepcopy(user_params)
    refresh_url = base_url + dest_path
    dd["ObjectPath"] = refresh_url
    print "refresh_url:", refresh_url
    try:
        recdn.make_request(dd)
    except:
        pass

    return dd["ObjectPath"]