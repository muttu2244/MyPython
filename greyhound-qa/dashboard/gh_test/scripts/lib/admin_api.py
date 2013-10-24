#!/usr/bin/python26
import re
import subprocess
import pdb
import sys
import os
import urllib
import urllib2
import string
import random
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


ADMIN_URL = Constants.ADMIN_URL
SERVERS_ADMIN = ADMIN_URL.__len__()


SECRET = Constants.SECRET

XREFERER = str("http://localhost/foo/")
XOR_ENCODE = Constants.XOR_ENCODE
DISABLE_AUTH = Constants.DISABLE_AUTH

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return False
	return ret


def decode_blob(blob):
	return base64.decodestring(blob)
	





"""
Changes to this funct
	- parameters changed, it accepts zauth,url as new parameters
"""
def curl_web_req(zauth, url, params, addl_headers=None):
	global WEB_SERVER
	global SECRET
	global XOR_ENCODE
	global DISABLE_AUTH
	global XREFERER
	global USER_BLOB

	secret = SECRET
	xreferer = XREFERER
	if not zauth:
		auth_key= ' '
		auth=' '

	else:
	
		[zid,expire,sig] = zauth.split('.')
		if(Constants.MULTI_TENDENCY):
               		[game_id,zid] = zid.split(':')
	  	  	server = ADMIN_URL
		if DISABLE_AUTH:
			auth_key = Constants.HEADER_ZID
			auth = str(zid)
		else:
			auth_key = Constants.HEADER_ZAUTH
			auth = zauth

	result = StringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.WRITEFUNCTION, result.write)
	c.setopt(pycurl.URL, url)
	
	#removed X-Operation from headers and added to additional headers
	headers = [
		'Expect:',
		'Connection: Keep-Alive',
		'Keep-Alive: 300',
		"%s: %s" % (auth_key, auth),
		'Content-Type: application/json',
		"X-Referer: %s" % (xreferer)
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



def user_reputation_get(zauth,data):
	url = "%s/user.reputation.get.php"  % (ADMIN_URL[random.randrange(0,SERVERS_ADMIN)] )
	return curl_web_req(zauth, url, data)

def user_meta_threshold_get(zauth,data):
	url = "%s/user.meta.thresholds.get.php" % (ADMIN_URL[random.randrange(0,SERVERS_ADMIN)] )
	return curl_web_req(zauth, url, data)



def user_history_get(zauth,data):
	url = "%s/user.history.get.php" % (ADMIN_URL[random.randrange(0,SERVERS_ADMIN)] )
	return curl_web_req(zauth , url , data)


def user_blob_revert_golden(zauth,data):
	url = "%s/user.blob.revert.golden.php" % (ADMIN_URL[random.randrange(0,SERVERS_ADMIN)] )
        return curl_web_req(zauth,url ,data)


def user_blob_delete(zauth,blob_type):
	 url = "%s/user.blob.delete.php/%s" % (ADMIN_URL[random.randrange(0,SERVERS_ADMIN)],blob_type )
         return curl_web_req(zauth, url,{})


