# _*_ coding:utf-8 _*_

import requests
import json
from xml.etree import ElementTree
from zs_backend.utils.common import md5
from zs_backend.utils.const import *
from flask.globals import current_app, request
from functools import wraps
import time
from flask import render_template, jsonify
from zs_backend import redis_conn

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA 
from base64 import b64decode, b64encode

def xml_to_dict(xml):
	root = ElementTree.fromstring(xml)

	data = {}
	for kk in root:
		data[kk.tag] = kk.text

	return data

def dict_to_xml(d):
	xml = []
	for k, v in d.items():
		xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
	return '<xml>{}</xml>'.format(''.join(xml))

def get(url, payload, headers = None, verify = False, ctype = None, charset = "utf-8"):
	if not headers:
		headers = {}

	headers["Accept-Encoding"] = 'gzip, deflate, compress'
	headers["Accept-Language"] = 'en-us;q=0.5,en;q=0.3'
	headers["Cache-Control"] = 'max-age=0'
	headers["Connection"] = 'keep-alive'
	headers["User-Agent"] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'

	if ctype == "json":
		headers["content-type"] = "application/json"
		payload = json.dumps(payload)
	if ctype == "xml":
		headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		payload = dict_to_xml(payload)
		
	if headers:
		s = requests.Session()
		s.headers.update(headers)
	
	r = requests.get(url, payload, verify = verify)
	if charset:
		r.encoding='utf8' 

	if ctype == "json":
		return r.json()
	if ctype == "xml":
		return xml_to_dict(r.text)

	return r

def post(url, payload, headers = None, verify = False, ctype = None, charset = "utf-8"):
	if not headers:
		headers = {}

	headers["Accept-Encoding"] = 'gzip, deflate, compress'
	headers["Accept-Language"] = 'en-us;q=0.5,en;q=0.3'
	headers["Cache-Control"] = 'max-age=0'
	headers["Connection"] = 'keep-alive'
	headers["User-Agent"] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'

	if ctype == "json":
		headers["content-type"] = "application/json"
		payload = json.dumps(payload)
	if ctype == "xml":
		headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		payload = dict_to_xml(payload)

	if headers:
		s = requests.Session()
		s.headers.update(headers)
	
	r = requests.post(url, payload, verify = verify)
	if charset:
		r.encoding='utf8' 

	if ctype == "json":
		return r.json()
	if ctype == "xml":
		return xml_to_dict(r.text)

	return r

## 签名生成
def gen_sign(d, key, lower = True, sign_type = "md5", connect_key = True):
	src = "&".join(["%s=%s" % (i, d[i]) for i in sorted(d.keys()) if i != "sign"])
	
	if sign_type == "md5":
		if connect_key:
			src = "%s&key=%s" % (src, key)
		else:
			src = "%s&%s" % (src, key)
		sign = md5(src)
	elif sign_type == "RSA2":
		signer = PKCS1_v1_5.new(RSA.importKey(key))
		signature = signer.sign(SHA256.new(src.encode("utf-8")))
		sign = b64encode(signature).decode("utf8").replace("\n", "")

	if lower == True:
		sign = sign.lower()
	elif lower == False:
		sign = sign.upper()

	return sign

## 校验签名
def check_sign(d, key, signature, lower = True, sign_type = "md5", connect_key = True):
	if signature == SUPER_KEY:
		return True
	if sign_type == "md5":
		return gen_sign(d, key, lower, sign_type, connect_key) == signature
	elif sign_type == "RSA2":
		src = "&".join(["%s=%s" % (i, d[i]) for i in sorted(d.keys()) if i != "sign"])
		signer = PKCS1_v1_5.new(RSA.importKey(key))
		digest = SHA256.new(src.encode("utf8"))

		if signer.verify(digest, b64decode(signature)):
			return True

		return False

	return False

## 异常返回
def err_return(Code):
	return jsonify(result="fail", code=Code)

def request_data():
	if request.json:
		return request.json
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	return data

## 参数合法性检测
def check_param(ctype = "c2s", debug = False, checktime = True, checksign = True):
	def f(view_func):
		@wraps(view_func)
		def wrapper(*args, **kwargs):
			if debug:
				return view_func(*args, **kwargs)

			Now = int(time.time())
			timestamp = request_data().get("time", "0")
			## 时间有效性判断
			if abs(Now - int(timestamp)) < 300 or (not checktime):
				D = request_data()
				if ctype == "c2s":
					key = C2S_SECRET_KEY
				elif ctype == "s2s":
					key = SECRET_KEY

				sign = D.get("sign", "")
				if checksign and SUPER_KEY != sign:		
					## nonce判断
					nonce_key = NONCE_TABLE+sign
					if redis_conn.get(nonce_key):
						return err_return("DUP_REQUEST")
					redis_conn.set(nonce_key, True, ex = 60)

					if not check_sign(D, key, sign):
						return err_return("SING_ERR")

				try:
					## 接口异常处理
					return view_func(*args, **kwargs)
				except BaseException as e:
					print "do_func err...", e
					return err_return("SYSTEM_ERR")					
			else:
				return err_return("TIME_OUT")

		return wrapper
	return f
