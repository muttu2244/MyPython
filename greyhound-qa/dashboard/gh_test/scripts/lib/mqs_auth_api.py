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


def encode_post(data):
	return json.dumps(data)


def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return data
	return ret

def curl_web_req(zauth, params = { }, addl_headers=None):
  
	""" Sends the http request and return the result as python object"""
	
	xreferer = Constants.XREFERER
	auth_key = Constants.HEADER_ZAUTH
	result = StringIO.StringIO()
	url = Constants.MQS_URL
	c = pycurl.Curl()
	
	headers =  ['Expect: ','Connection: Keep-Alive','Keep-Alive: 300',
							"%s: %s" % (auth_key,zauth),
							'Content-Type: application/json',
							"X-Referer: %s" % (xreferer)
							]

	if addl_headers:
		headers += addl_headers
	
	c.setopt(pycurl.WRITEFUNCTION, result.write)
	c.setopt(pycurl.URL, url[0])
	c.setopt(pycurl.HTTPHEADER, headers)
	c.setopt(pycurl.POST, 1)
	if params != { }:
	  	params = encode_post(params)
		if Constants.XOR_ENCODE:
			post_body = xor_encode(params, zauth)
		else:
			post_body = params
	else:
		post_body = '{"version": 1}'
	
	c.setopt(pycurl.POSTFIELDS, post_body)
	c.perform()

	ret = result.getvalue()
	print ret
	if Constants.XOR_ENCODE:
		ret = xor_encode(ret, zauth)
	
	if ret:
		ret = decode_post(ret)
	
	result.close()
	c.close()
	return ret 	

# Meta user APIs 

def meta_user_get(zauth):
	headers = ['X-Operation: meta.user.get']
	return curl_web_req(zauth, { }, headers)

def meta_user_update(zauth, fields, cas):
	headers = ['X-Operation: meta.user.update', "If-Match: %s" % (cas) ]
	return curl_web_req(zauth,{ Constants.FIELDS: fields }, headers)


# Graph user APIs

def graph_user_add(zauth, graph, zid_list):
	headers = ['X-Operation: graph.user.add']
	return curl_web_req(zauth, { "graph-type": graph, Constants.ZID_LIST: zid_list}, headers )


def graph_user_remove(zauth, graph, zid_list):
	headers = ['X-Operation: graph.user.remove']
	return curl_web_req(zauth, { "graph-type": graph, Constants.ZID_LIST: zid_list}, headers)

def graph_user_checkmembership(zauth, graph_list, zid_list):
	headers = ['X-Operation: graph.user.checkmembership']
	return curl_web_req(zauth, { "graph-type": graph_list, Constants.ZID_LIST: zid_list}, headers)


def graph_user_getmembers(zauth, graph_list):
	headers = ['X-Operation: graph.user.getmembers']
	return curl_web_req(zauth, { "graph-type": graph_list}, headers)

def graph_user_getconfirmlist(zauth, graph_list):
	headers = ['X-Operation: graph.user.getconfirmlist']
	return curl_web_req(zauth, { "graph-type": graph_list}, headers)

def graph_user_getwaitlist(zauth, graph_list):
	headers = ['X-Operation: graph.user.getwaitlist']
  	return curl_web_req(zauth, { "graph-type": graph_list}, headers)

def graph_user_getgraphlist(zauth,zid_list):
	headers = ['X-Operation: graph.user.getgraphlist']
	return curl_web_req(zauth, { Constants.ZID_LIST: zid_list}, headers)


def query_user_graph(zauth, graph, query):
	headers = ['X-Operation: query.user.graph']
	return curl_web_req(zauth, { "graph-type": graph, Constants.STMT: query }, headers)


# APIs that requires admin token (credibility APIs)

	
def meta_user_credibility_get(zauth, zid_list):
	headers = ['X-Operation: meta.user.credibility.get']
	return curl_web_req(zauth, { Constants.ZID_LIST: zid_list }, headers)

def meta_user_credibility_set(zauth, credibility):
	headers = ['X-Operation: meta.user.credibility.set']
	return curl_web_req(zauth, { "credibility":  credibility }, headers)

def meta_user_credibility_upgrade(zauth, zid_list):
	headers = ['X-Operation: meta.user.credibility.upgrade']
	return curl_web_req(zauth, { Constants.ZID_LIST: zid_list }, headers)

def meta_user_credibility_downgrade(zauth, zid_list):
	headers = ['X-Operation: meta.user.credibility.downgrade']
	return curl_web_req(zauth, { Constants.ZID_LIST: zid_list }, headers)

def meta_user_trio_get(zauth, zid_list):
	headers = ['X-Operation: meta.user.trio.get']
	return curl_web_req(zauth, { Constants.ZID_LIST: zid_list }, headers)

def meta_user_bulk_update(zauth, metatype, fields):
	headers = ['X-Operation: meta.user.bulk.update']
	return curl_web_req(zauth, { 'type': metatype, 'fields': fields}, headers)



