#!/usr/bin/python26

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
SERVICE_URL = Constants.SERVICE_URL
SERVERS = SERVICE_URL.__len__()
#SECRET = "c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330"
SECRET = Constants.SECRET

XREFERER = str("http://localhost/foo")
USER_BLOB = Constants.USER_BLOB
XOR_ENCODE = Constants.XOR_ENCODE
DISABLE_AUTH = Constants.DISABLE_AUTH

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return "cant decode the output = ",data 
	return ret


def decode_blob(blob):
	return base64.decodestring(blob)
	
	
	
def data_to_post():
	document = "\"fname\":\"{0}\"".format(''.join((random.choice(string.letters) for _ in xrange(random.randint(5, 10)))))
        document = document + ",\"lname\":\"{0}\"".format(''.join((random.choice(string.letters) for _ in xrange(random.randint(5, 10)))))
        document = document + ",\"fb_id\":\"{0}\"".format(''.join((random.choice(string.digits) for _ in xrange(random.randint(5, 10)))))
        document_1 = "\"cash\":{0}".format(random.randint(0, 1000))
        document_1 = document_1 + ",\"coins\":{0}".format(random.randint(0, 50))
        document_1 = document_1 + ",\"gold\":{0}".format(random.randint(0, 50))
        document_1 = document_1 + ",\"level\":{0}".format(random.randint(0, 50))
        document_1 = document_1 + ",\"energy\":{0}".format(random.randint(0, 50))
        document_1 = document_1 + ",\"xp\":{0}".format(random.randint(0, 1000))
        document_2 = "\"time_left\":{0},\"count\":{1}".format(random.randint(0, 1000), random.randint(0, 1000))
        document_3 = "\"time_left\":{0},\"count\":{1}".format(random.randint(0, 1000), random.randint(0, 1000))
        document = "{" "\"user\":{"+ document + "}, \"world\":{"+ document_1 + ",\"farm\":[{" + document_2 + "},{"+ document_3 +"}]}}"
	return document


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
	#user_blob = USER_BLOB
	
	#getting zid from auth token
	[zid,expire,sig] = zauth.split('.')
	if(Constants.MULTI_TENDENCY):
                [game_id,zid] = zid.split(':')
	server = SERVICE_URL
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

def curl_web_req2(zauth, url, params, addl_headers=None):
        global WEB_SERVER
        global SECRET
        global XOR_ENCODE
        global DISABLE_AUTH
        global XREFERER

        secret = SECRET
        xreferer = XREFERER
        user_blob = USER_BLOB

	[zid , expire , sig] = zauth.split('.')
	if(Constants.MULTI_TENDENCY):
		[game_id,zid] = zid.split(':')
        server = SERVICE_URL
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


def user_blob_get(zauth,blob_type):
	url = "%s/user.blob.get.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req(zauth , url , { }, add_headers)

def user_blob_set(zauth, blob_type,fields, cas):
	url = "%s/user.blob.set.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.set' , "If-Match: %s" % (cas) ]
	return curl_web_req(zauth, url, { Constants.FIELDS: fields}, add_headers)

def friend_blob_get(zauth , fid , blob_type ):
	url = "%s/friend.blob.get.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , blob_type)
	add_headers = ['X-Operation: friend.blob.get' ]
	return curl_web_req2(zauth , url , { } , add_headers)

def friend_blob_addDelta(zauth , fid , delta_type, delta):
	url = "%s/friend.blob.addDelta.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , delta_type)
	add_headers = ['X-Operation: friend.blob.addDelta']
	return curl_web_req2(zauth , url ,delta , add_headers  )

def friend_blob_queryDeltas(zauth, fid , query ):
	url = "%s/friend.blob.queryDeltas.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid)
	add_headers = ['X-Operation: friend.blob.queryDeltas']
	return curl_web_req2(zauth , url , query , add_headers)

def user_blob_queryDeltas(zauth , query):
	url = "%s/user.blob.queryDeltas.php/" % (SERVICE_URL[random.randrange(0,SERVERS)])
	add_headers = ['X-Operation: user.blob.queryDeltas']
	return curl_web_req2(zauth , url , query , add_headers)

def user_blob_deleteDeltas( zauth , delta_ids):
	url = "%s/user.blob.deleteDeltas.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , delta_ids)
	add_headers = ['X-Operation: user.blob.deleteDeltas']
	return curl_web_req2(zauth , url , { } , add_headers)


