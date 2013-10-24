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

#SERVICE_URL = "zgreyhound.greyhound-staging.zynga.com/public/services"
INTERNAL_URL = Constants.INTERNAL_URL
SERVERS = INTERNAL_URL.__len__()


#PUBLIC_URL = Constants.SERVICE_URL
#SERVERS_PUBLIC = SERVICE_URL.__len__()

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
		return data
	return ret


def decode_blob(blob):
	return base64.decodestring(blob)
	



def Clean_Memsched(item):
	GH_MEMSCHED = Constants.GH_MEMSCHED
	PORT = Constants.PORT
	process = subprocess.Popen('echo "flush_all %s" | nc %s %s' %(item,GH_MEMSCHED,PORT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output,stderr=process.communicate()
	if output.rstrip()!= 'OK':
		print "error in Cleaning up memsched table"
	


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
	  	  	server = INTERNAL_URL
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


def threshold_fetch_api(zauth, data):
	url = "%s/thresholds.fetch.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	return curl_web_req(zauth, url, data)

def threshold_update_api(zauth,data):
	url = "%s/thresholds.update.php" % (INTERNAL_URL[random.randrange(0,SERVERS)]) 
	return curl_web_req(zauth, url, data)

def user_credibility_get(zauth, data):
	url = "%s/user.credibility.get.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	time.sleep(1)
	return curl_web_req(zauth, url, data)

def user_reputation_update(zauth, data):
	url = "%s/user.reputation.update.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	time.sleep(1)
	return curl_web_req(zauth, url, data)



def user_blob_golden_update(zauth,data):
	url = "%s/user.blob.golden.update.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	return curl_web_req(zauth, url, data)


def user_history_update(zauth, data):
	url = "%s/user.history.update.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	return curl_web_req(zauth , url , data)


def fraud_update(zauth,data):
	url = "%s/fraud.update.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
        return curl_web_req(zauth , url , data)


def archive_update_API(zauth, data):
	url = "%s/archive.queue.update.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	return curl_web_req(zauth , url ,data)

def dau_update(zauth,data):
	url = "%s/dau.queue.update.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
        return curl_web_req(zauth , url ,data)


def archive_queue_fetch(zauth,data):
	 url = "%s/archive.queue.fetch.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	 time.sleep(1)
	 return curl_web_req(zauth, url,data)

def dau_queue_fetch(zauth,data):
	 url = "%s/dau.queue.fetch.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
         time.sleep(1)
         return curl_web_req(zauth, url,data)


def user_blob_archive(zauth,data):
	 url = "%s/user.blob.archive.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
         return curl_web_req(zauth, url,data)


def payments_append(zauth,data):
	url = "%s/user.payments.meta.append.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	return curl_web_req(zauth, url,data)

def  user_payments_meta_get(zauth,data):
	url = "%s/user.payments.meta.get.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
        return curl_web_req(zauth, url,data)

def user_blob_revert(zauth,data):
	 url = "%s/user.blob.revert.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
         return curl_web_req(zauth, url,data)

def fraud_queue_update(zauth,data):
	url = "%s/fraud.queue.update.php" % (INTERNAL_URL[random.randrange(0,SERVERS)] )
        return curl_web_req(zauth, url,data)

def fraud_queue_fetch(zauth,data):
	url = "%s/fraud.queue.fetch.php"  % (INTERNAL_URL[random.randrange(0,SERVERS)] )
	time.sleep(1)
        return curl_web_req(zauth, url,data)

#def user_blob_get(zauth):
#url = "http://%s/services/user.blob.get.php" %(PUBLIC_URL[random.randrange(0,SERVERS_PUBLIC)] )
#return curl_web_req(zauth,url)
