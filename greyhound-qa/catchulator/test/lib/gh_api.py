#!/usr/bin/python26
import pdb
import sys
import os
import urllib
import urllib2
import string
import random
#from api_constants import Constants
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

SERVICE_URL = "sample.greyhound.zynga.com/services"
#GH_INT_URL = "internal.sample.greyhound.zynga.com/services"
GH_INT_URL = "internal.sample.greyhound.zynga.com/services"

#SERVICE_URL = Constants.SERVICE_URL
SERVERS = SERVICE_URL.__len__()

MQS_URL = "sample.greyhound.zynga.com/services" 
#MQS_URL = Constants.MQS_URL
MQS_SERVERS = MQS_URL.__len__()

SECRET = "c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330"
#SECRET = Constants.SECRET

XREFERER = str("http://localhost/foo/")
USER_BLOB = "game-world"
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


def decode_blob(blob):
	return base64.decodestring(blob)
	
	pd.set_trace()	

def data_to_post(size=0):
		size_in=size*1024
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

		while len(document) <= size_in:
			document = document + ",\"lname\":\"{0}\"".format(''.join((random.choice(string.letters) for _ in xrange(random.randint(5, 10)))))
			if len(document) > size_in:
				break

		return document


def query_to_post(size):
	query= "\"{Constants.USER_QUERY: Constants.F_QUERY, \"params\":[] }\""
	
	length=len(query)
	while length <=2000:
		query = query + "\"{Constants.USER_QUERY: Constants.F_QUERY, \"params\":[] }\""
		length=len(query)
		if length >= 2000:
			break
	return query


def delta_to_post(delta_type):
	if delta_type == 'visit':
		size=5000
	elif delta_type == 'gift':
		size=2500
	else:
		size=1500
	
	delta="some delta"
	while len(delta) <= size:
		delta=delta+ "some more delta"
		if len(delta) > size:
			break	

	return delta


def delta_max_count(zauth,fid,delta_type,delta):
	count=1
	while count <= 11:
		ret=friend_blob_addDelta(zauth , fid , delta_type, delta)
		count =count + 1
		if count >= 11:
			break
		
	return ret



def find_errcode(dicts, error=None):
	for key,value in dicts.items():
		if key == 'error':
			return value	
		else:
			val=find_errcode(value,error)	
			return val

"""
Changes to this funct
	- parameters changed, it accepts zauth,url as new parameters
"""
def curl_web_req(zauth, url, params=None, addl_headers=None):
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
		if(MULTI_TENDENCY):
               		[game_id,zid] = zid.split(':')
	  	  	server = SERVICE_URL
		if DISABLE_AUTH:
			auth_key = 'X-ZID'
			auth = str(zid)
		else:
			auth_key = 'Z-Authorization'
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
	#params = encode_post(params)
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

	#pdb.set_trace()
	if not zauth:
                auth_key= ' '
                auth=' '
        else:

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



def curl_web_req3(url, params, addl_headers=None):
        #global WEB_SERVER
        global SECRET
        global XOR_ENCODE
        global DISABLE_AUTH
        global XREFERER

        secret = SECRET
        xreferer = XREFERER
        user_blob = USER_BLOB


        result = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(pycurl.WRITEFUNCTION, result.write)
        c.setopt(pycurl.URL, url)
        headers = [
                'Expect:',
                'Connection: Keep-Alive', 
                'Keep-Alive: 300',
                'Content-Type: application/json',
                "X-Referer: %s" % (xreferer)
	
        ]
	if addl_headers:
                headers += addl_headers
        c.setopt(pycurl.HTTPHEADER, headers)
        c.setopt(pycurl.POST, 1)
        params = encode_post(params)
	if XOR_ENCODE:
                p1 = xor_encode(params)
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

                                                                                                                                                                          


"""
Changes -- 
	function parameters changed. Function accepts zauth and blob type as parameters
	url is created in these functions
"""

def user_blob_get(zauth,blob_type):
	#pdb.set_trace()
	url = "http://%s/user.blob.get.php/%s" % (SERVICE_URL, blob_type)
	print url
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req(zauth , url, add_headers)

def user_blob_get_invalid(zauth,blob_type):
	url = "http://%s/user.blob.get.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req(zauth , url , { }, add_headers)


def user_blob_set(zauth, blob_type,fields, cas):
	global SERVICE_URL
	#url = "http://%s/user.blob.set.php/%s" % (SERVICE_URL, blob_type)
	#add_headers = ['X-Operation: user.blob.set' , "If-Match: %s" % (cas) ]
	url_int="http://%s/user.token.issue.php" %(GH_INT_URL)
	zid=zauth
	zauth=" " 
	add_headers = ['X-Operation: user.token.issue']
	#curl_web_req(zauth,url_int,{"uid": zid, "version": 1} , add_headers)	

	res = curl_web_req3( url_int,{"uid": zid, "version": 1} , add_headers)
	zauth= res['result']['userToken']
	url = "http://%s/user.blob.set.php/%s" % (SERVICE_URL, blob_type)
        add_headers = ['X-Operation: user.blob.set' , "If-Match: %s" % (cas) ]
        return curl_web_req(zauth, url, fields, add_headers)


def friend_blob_get(zauth , fid , blob_type ):
	url = "http://%s/friend.blob.get.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , blob_type)
	add_headers = ['X-Operation: friend.blob.get' ]
	return curl_web_req2(zauth , url , { } , add_headers)

def friend_blob_addDelta(zauth , fid , delta_type, delta):
	url = "http://%s/friend.blob.addDelta.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , delta_type)
	add_headers = ['X-Operation: friend.blob.addDelta']
	return curl_web_req2(zauth , url ,delta, add_headers  )

def friend_blob_queryDeltas(zauth, fid , query ):
	url = "http://%s/friend.blob.queryDeltas.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid)
	add_headers = ['X-Operation: friend.blob.queryDeltas']
	return curl_web_req2(zauth , url , query , add_headers)

def user_blob_queryDeltas(zauth , query):
	url = "http://%s/user.blob.queryDeltas.php/" % (SERVICE_URL[random.randrange(0,SERVERS)])
	add_headers = ['X-Operation: user.blob.queryDeltas']
	return curl_web_req2(zauth , url , query , add_headers)

def user_blob_deleteDeltas( zauth , delta_ids):
	url = "http://%s/user.blob.deleteDeltas.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , delta_ids)
	add_headers = ['X-Operation: user.blob.deleteDeltas']
	return curl_web_req2(zauth , url , { } , add_headers)

def user_blob_get_no_Zauth_head(blob_type):
	url="http://%s/user.blob.get.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req3(url,{},add_headers)

def user_blob_set_no_Zauth_head( blob_type, data, cas):
	url="http://%s/user.blob.get.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.set']
	return curl_web_req3(url,{},add_headers)

def friend_blob_get_no_Zauth_head(fid, blob_type ):
	url = "http://%s/friend.blob.get.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , blob_type)
        add_headers = ['X-Operation: friend.blob.get' ]
        return curl_web_req3(url , { } , add_headers)


"""
mqs query to get friend and non-friend IDs for friend.blobs and deltas.
Check is made to verify the user has friend list, if not graph.user.add API is called and then the list is taken
"""



def get_friend_nofriend_id(zauth, graph_type):
	url = "http://%s/graph.user.getmembers" %(MQS_URL[random.randrange(0,MQS_SERVERS)] )
	add_headers = ['X-Operation: graph.user.getmembers']
	ret = curl_web_req(zauth , url , {"version": 1 ,"graph-type": [Constants.GRAPH_TYPE]} , add_headers)
	if ret['status']['message'] != 'success':
		add_headers = ['X-Operation: graph.user.add']
		print "zauth is : %r" %zauth
		ret=curl_web_req(zauth, url, {"version" : 1, "graph-type": [Constants.GRAPH_TYPE], "uid-list": [101]},add_headers)	
		add_headers = ['X-Operation: graph.user.getmembers']
		ret = curl_web_req(zauth , url , {"version": 1 ,"graph-type": [Constants.GRAPH_TYPE]} , add_headers)
	
	if ret is None:
		print " Please, check for MQS host's availibility"
	return ret

def user_blob_golden_update(zauth, uid_list):
	global GH_INT_URL
	document = "\"version\": 1, \"uid-list\": [{0}]".format(uid_list)
	fields = "{" + document + "}"
	url = "http://%s/user.blob.golden.update.php" %(GH_INT_URL)
	add_headers = ['X-Operation: user.blob.golden.update']
	return curl_web_req(zauth , url, fields, add_headers)
	
def payment_meta_append(zauth, fields, cas):
	global GH_INT_URL
	url = "http://%s/user.payments.meta.append.php" % (GH_INT_URL)
	add_headers = ['X-Operation: user.payments.meta.append' , "If-Match: %s" % (cas) ]
	return curl_web_req(zauth, url, fields, add_headers)

def dau_queue_update(zauth, fields):
	global GH_INT_URL
	url = "http://%s/dau.queue.update.php" % (GH_INT_URL)
	add_headers = ['X-Operation: dau.queue.update']
	return curl_web_req(zauth, url, fields, add_headers)


#if __name__ == "__main__":
	#user_blob_set(AuthSystem.getUntrustedToken(sys.argv[1]), USER_BLOB, sys.argv[2], cas = " ")
	#dau_queue_update(AuthSystem.getTrustedAuthToken(16), '{"uid-list": ["880", "881", "882", "883", "884", "885", "886", "887", "888", "889"], "version": 1}')
	#payment_meta_append(AuthSystem.getImpersonatedAuthToken(sys.argv[1]), sys.argv[2], cas = " ")
	#user_blob_golden_update(AuthSystem.getTrustedAuthToken(sys.argv[1]), sys.argv[3])
