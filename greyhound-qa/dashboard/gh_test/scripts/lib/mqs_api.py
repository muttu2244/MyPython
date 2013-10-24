import sys
import os
import urllib
import urllib2
from api_constants import Constants
import random
import time
from multiprocessing import Pool
import StringIO
import pycurl
import traceback
import select
import base64
import hmac
import hashlib
from time import time as now
from auth import *
import simplejson as json

DB_SERVER = "10.32.193.85:22122"
WEB_SERVER = "10.32.232.238:80"

SECRET = "sekret"
XOR_ENCODE = 0
DISABLE_AUTH = 0

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return False
	return ret

def curl_web_req(api, zid, params, addl_headers=None, server_role=False):
	global WEB_SERVER
	global SECRET
	global XOR_ENCODE
	global DISABLE_AUTH

	secret = SECRET

	if not isinstance(zid, int):
		zid = int(zid)

	server = WEB_SERVER
	if DISABLE_AUTH:
		auth_key = Constants.HEADER_ZID
		auth = str(zid)
	else:
		auth_key = Constants.HEADER_ZAUTH
		if server_role:
			auth = AuthSystem.getAuthTokenOnCondition(zid, SECRET, 3600, AuthSystem.INTERNAL)
		else:
			auth = AuthSystem.getAuthTokenOnCondition(zid, SECRET, 3600, AuthSystem.USER)

	url = "http://%s/services/%s" % (server, api)

	params['version'] = 1
	result = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.WRITEFUNCTION, result.write)
	c.setopt(pycurl.URL, url)
	headers = [
		'Expect:',
		'Connection: Keep-Alive',
		'Keep-Alive: 300',
		"%s: %s" % (auth_key, auth),
		"%s: %s" % (Constants.HEADER_X_OPERATION, api),
		'Content-Type: application/octet-stream',
		'X-Referer: http://localhost/foo'
	]
	if addl_headers:
		headers += addl_headers
	c.setopt(pycurl.HTTPHEADER, headers)
	c.setopt(pycurl.POST, 1)
	params = encode_post(params)
	if XOR_ENCODE:
		p1 = xor_encode(params, auth)
	else:
		p1 = params
	c.setopt(pycurl.POSTFIELDS, p1)
	c.perform()
	ret = result.getvalue()
	if XOR_ENCODE:
		ret = xor_encode(ret, auth)
	if ret:
		ret = decode_post(ret)
	result.close()
	c.close()
	return ret

def curl_db_req(api, zid, params):
	global DB_SERVER

	url = "http://%s/services/%s" % (DB_SERVER, api)

	params['version'] = 1
	result = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.WRITEFUNCTION, result.write)
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, [
		'Expect:',
		'Connection: Keep-Alive',
		'Keep-Alive: 300',
		"%s: %d" % (Constants.HEADER_ZID, int(zid)),
		"%s: %s" % (Constants.HEADER_X_OPERATION, api),
		'Content-Type: application/json',
	])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, encode_post(params))
	c.perform()
	ret = decode_post(result.getvalue())
	result.close()
	c.close()
	return ret

def graph_user_add(zid, type, zid_list):
	return curl_web_req('graph.user.add', zid, { Constants.GRAPH_TYPE: type, Constants.ZID_LIST: zid_list})

def graph_user_remove(zid, type, zid_list):
	return curl_web_req('graph.user.remove', zid, { Constants.GRAPH_TYPE: type, Constants.ZID_LIST: zid_list})

def graph_user_get(zid, type):
	return curl_web_req('graph.user.getmembers', zid, { Constants.GRAPH_TYPE: type })

def graph_user_checkmembership(zid, types, zid_list):
	return curl_web_req('graph.user.checkmembership', zid, { Constants.GRAPH_TYPE: types, Constants.ZID_LIST: zid_list })

def graph_user_getgraphlist(zid, zid_list):
	return curl_web_req('graph.user.getgraphlist', zid, { Constants.ZID_LIST: zid_list })

def graph_user_getmembers(zid, graph_type_list):
	return curl_web_req('graph.user.getmembers', zid, { Constants.GRAPH_TYPE: graph_type_list })

def graph_user_getconfirmlist(zid, graph_type_list):
	return curl_web_req('graph.user.getconfirmlist', zid, { Constants.GRAPH_TYPE: graph_type_list })

def graph_user_getwaitlist(zid, graph_type_list):
	return curl_web_req('graph.user.getwaitlist', zid, { Constants.GRAPH_TYPE: graph_type_list })

def meta_user_get(zid):
	return curl_web_req('meta.user.get', zid, { })

def meta_user_update(zid, fields, cas):
	return curl_web_req('meta.user.update', zid, { Constants.FIELDS: fields }, [ "If-Match: %s" % (cas) ])

def meta_user_delete(zid):
	return curl_db_req('meta.user.delete', zid, { })

def meta_user_getbulk(zid_list):
	columns = [ "zid", "level", "xp", "gold", "cash", "coins", "commodity_1", "commodity_2" ]
	return curl_db_req('meta.user.getbulk', 0, { Constants.ZID_LIST: zid_list, Constants.COLUMNS: columns })

def meta_user_credibility_upgrade(zid_list, server_role=True):
	return curl_web_req('meta.user.credibility.upgrade', 0, { Constants.ZID_LIST: zid_list }, None, server_role)

def meta_user_credibility_downgrade(zid_list, server_role=True):
	return curl_web_req('meta.user.credibility.downgrade', 0, { Constants.ZID_LIST: zid_list }, None, server_role)

def meta_user_credibility_get(zid_list, server_role=True):
	return curl_web_req('meta.user.credibility.get', 0, { Constants.ZID_LIST: zid_list }, None, server_role)

def meta_user_credibility_set(cred, server_role=True):
	return curl_web_req('meta.user.credibility.set', 0, { Constants.CRED: cred }, None, server_role)

def meta_user_trio_get(zid_list, server_role=True):
	return curl_web_req('meta.user.trio.get', 0, { Constants.ZID_LIST: zid_list }, None, server_role)

def meta_user_bulk_update(type, fields, server_role=True):
	return curl_web_req('meta.user.bulk.update', 0, { Constants.META_TYPE: type, Constants.FIELDS: fields }, None, server_role)

def query_user_graph(zid, type, stmt):
	return curl_web_req('query.user.graph', zid, { Constants.GRAPH_TYPE: type, Constants.STMT: stmt })
