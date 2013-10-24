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
SERVICE_URL = Constants.SERVICE_URL
SERVERS = SERVICE_URL.__len__()

MQS_URL = Constants.MQS_URL
MQS_SERVERS = MQS_URL.__len__()

#SECRET = "c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330"
SECRET = Constants.SECRET

XREFERER = str("http://localhost/foo/")
USER_BLOB = Constants.USER_BLOB
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
	
	pd.set_trace()	

def data_to_post(size=0):
		size_in=size*1000
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
			if len(document) >= size_in:
				break
		return document


def diff_data_post(path,oldFile,newFile):

	p = subprocess.Popen(['php %s/zcdiff-gen.php -o %s/out.zcdiff %s %s' %(path,path,oldFile,newFile)] ,shell = True)
	p.communicate()[0]

	p = subprocess.Popen(['md5sum %s > %s/checksum.txt' %(newFile,path)] ,shell = True)	
	p.communicate()[0]
	checksumFH = open('%s/checksum.txt'%path,'r')
	checksumList = checksumFH.readlines()
	checksumList = checksumList[0].split(' ')
	checksum = checksumList[0]
	subprocess.Popen(['rm %s'%oldFile],shell = True)
	subprocess.Popen(['rm %s'%newFile],shell = True)
	subprocess.Popen(['rm %s/checksum.txt'%path],shell = True)
	return checksum

def query_to_post(size):
	query= "\"{Constants.USER_QUERY: Constants.F_QUERY, \"params\":[] }\""
	length=len(query)
	while length <=2000:
		query = query + "\"{Constants.USER_QUERY: Constants.F_QUERY, \"params\":[] }\""
		length=len(query)
		if length >= 2000:
			break
	return query


def delta_max_size(maxsize, delta):
	if 'k' in maxsize:
		maxsize=int(maxsize.strip('k'))
		maxsize=maxsize * 1024

	while len(delta) <=maxsize:
		delta=delta+ "some more delta"
		if len(delta) > maxsize:
			break	

	return delta


def delta_max_count(zauth,fid,delta_type,maxcount, delta):
	count=1
	while count <= maxcount:
		ret=friend_blob_addDelta(zauth , fid , delta_type, delta )
		count =count + 1
		if count > maxcount:
			break
	return maxcount


def max_count_storage(zauth,max,scoreboard_type,maxcount):
	count=1
	while count <= maxcount:
		ret=user_scoreboard_create(zauth,max,scoreboard_type)
                count =count + 1
                if count > maxcount:
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
Following code required for getting friend id and non-friend id
"""
def fzid(zauth):
	
	ret = get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
	fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
	fid = random.choice(fid_list)
	
	return fid

def nfzid(zauth):
	ret = get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
        fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
        fid = random.choice(fid_list)


	x=random.randint(1,100000)
	while 1:
       		if x not in fid_list:
                	break
        	x=random.randint(1,1000000)

	nfid=x

	return nfid



def max_key(size):
	doc="abcdefgh"
	while len(doc) <= size: 
                        doc = doc + "abc" 
                        if len(doc) >size :
                                break

	return doc



def remote_connect(var, default, type):
	""" get the IP of the GH web server """
        fh=open('/etc/hosts')
        for line in fh.readlines():
        	if re.search( Constants.APP_NAMESPACE, line):
               		 host_ip=line.split()[0]
                         break;


	file='/apps/%s/current/Storage.yaml' %(Constants.APP_NAMESPACE)
        """subprocess.Popen is run to get the variable maxcount/maxsize/max/min etc value from the remote
        greyhound web server """

	flag='true'
	if 'maxcount' in var:
		""" If var is maxcount we need to check variable keep, it needs to be set to oldest for maxcount TCs"""
		chk='keep'
		process = subprocess.Popen('ssh \"%s\" cat \"%s\" | sed -n /%s/,/type:.*/p | sed -n \'/%s/p\' | \
                cut -d: -f 2'  %(host_ip, file, Constants.DELTATYPE,chk), shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output,stderr = process.communicate()
                status = process.poll()
                #verify_var=output.rstrip('\n')

                if not output:
                        """ This implies keep is not defined in the delta type used, chck in default Deltas"""
                        process = subprocess.Popen('ssh \"%s\" cat \"%s\" | sed -n /Deltas:/,/%s/p | sed -n \'/%s/p\' | \
                        cut -d: -f 2'  %(host_ip, file,chk), shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        output,stderr = process.communicate()
                        status = process.poll()

		flag=output.strip('\n')

	"""For other variables like max, min, maxsize etc """
	process = subprocess.Popen('ssh \"%s\" cat \"%s\"  | sed -n /\"%s\"/,/type:.*/p  | sed -n \'/\\b%s\\b/p\'  | cut -d: -f 2' \
	%(host_ip, file, type, var), shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output,stderr = process.communicate()
        status = process.poll()
        val=output
     
        if not val:
    	 	"""This implies the specified delta\scoreboard type has no  max  value set for var, hence pick it from default 'Deltas' """
        	process = subprocess.Popen('ssh \"%s\" cat \"%s\" | sed -n /%s\:/,/maxcount/p | sed -n  \'/\\b%s\\b/p\'  | \
                cut -d: -f 2' %(host_ip, file, default, var), shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output,stderr = process.communicate()
                status = process.poll()
                val=output.rstrip('\n')

	
        return (val,host_ip,file,flag)






"""The below function is written to delete all the previous deltas"""
def delete_prev_deltas(fid):
	user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
        fzauth=AuthSystem.getUntrustedToken(fid)
        result = user_blob_queryDeltas (fzauth , user_query)
	if "'deltas': []" in str(result):
		"""no deltas available"""
		return None
        delta_id = []
        for item in result['deltas']:
        	delta_id = (item['delta_id'])
                result = user_blob_deleteDeltas ( fzauth , delta_id)

	return result







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



def curl_web_req2(url, params, addl_headers=None):
        global WEB_SERVER
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



def curl_web_req3(zauth, url, file, addl_headers=None):
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
                        server = SERVICE_URL
                if DISABLE_AUTH:
                        auth_key = Constants.HEADER_ZID
                        auth = str(zid)
                else:
                        auth_key = Constants.HEADER_ZAUTH
                        auth = zauth
	
	f = open(file, "rb")
	fs = os.path.getsize(file)

        result = StringIO.StringIO()
        c = pycurl.Curl()
	c.setopt(pycurl.PUT, 1)
	c.setopt(pycurl.WRITEFUNCTION, result.write)
        c.setopt(pycurl.URL, url)
	headers = [
                'Expect:',
                'Connection: Keep-Alive',
                'Keep-Alive: 300',
                "%s: %s" % (auth_key, auth),
                'Content-Type: text/html'
        ]
        if addl_headers:
                headers += addl_headers
	
        c.setopt(pycurl.HTTPHEADER, headers)
	c.setopt(pycurl.READDATA, f)
        c.setopt(pycurl.INFILESIZE, int(fs))
        c.setopt(pycurl.NOSIGNAL, 1)
        #c.setopt(pycurl.VERBOSE, 1)
        c.perform()
	ret = result.getvalue()
	if XOR_ENCODE:
                ret = xor_encode(ret, auth)
        if ret:
                ret = decode_post(ret)
        result.close()
        c.close()
	f.close()
	#print "Ret: %s\n"%ret
        return ret
                                                                                                                                                                          


"""
Changes -- 
	function parameters changed. Function accepts zauth and blob type as parameters
	url is created in these functions
"""

def user_blob_get(zauth,blob_type= Constants.USER_BLOB):
	#pdb.set_trace()
	url = "http://%s/user.blob.get.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req(zauth , url , { }, add_headers)

def user_blob_get_invalid(zauth,blob_type):
	url = "http://%s/user.blob.get.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req(zauth , url , { }, add_headers)


def user_blob_set(zauth, blob_type,fields, cas):
	url = "http://%s/user.blob.set.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.set' , "If-Match: %s" % (cas) ]
	return curl_web_req(zauth, url, { Constants.FIELDS: fields}, add_headers)


def user_blob_patch(zauth, blob_type,file, cas,checksum):
        url = "http://%s/user.blob.patch.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
        add_headers = ['X-Operation: user.blob.patch' , "If-Match: %s" % (cas),"X-Blob-Checksum: %s" %(checksum) ]
        return curl_web_req3(zauth, url, file, add_headers)



def friend_blob_get(zauth , fid , blob_type ):
	url = "http://%s/friend.blob.get.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , blob_type)
	add_headers = ['X-Operation: friend.blob.get' ]
	return curl_web_req(zauth , url , { } , add_headers)

def friend_blob_addDelta(zauth , fid , delta_type, delta):
	url = "http://%s/friend.blob.addDelta.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , delta_type)
	add_headers = ['X-Operation: friend.blob.addDelta']
	return curl_web_req(zauth , url ,delta, add_headers  )

def friend_blob_queryDeltas(zauth, fid , query ):
	url = "http://%s/friend.blob.queryDeltas.php/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid)
	add_headers = ['X-Operation: friend.blob.queryDeltas']
	return curl_web_req(zauth , url , query , add_headers)

def user_blob_queryDeltas(zauth , query):
	url = "http://%s/user.blob.queryDeltas.php/" % (SERVICE_URL[random.randrange(0,SERVERS)])
	add_headers = ['X-Operation: user.blob.queryDeltas']
	return curl_web_req(zauth , url , query , add_headers)

def user_blob_deleteDeltas( zauth , delta_ids):
	url = "http://%s/user.blob.deleteDeltas.php" % (SERVICE_URL[random.randrange(0,SERVERS)] )
	add_headers = ['X-Operation: user.blob.deleteDeltas']
	return curl_web_req(zauth , url , {"deltas" : [str(delta_ids)]} , add_headers)

def user_blob_get_no_Zauth_head(blob_type):
	url="http://%s/user.blob.get.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.get']
	return curl_web_req2(url,{},add_headers)

def user_blob_set_no_Zauth_head( blob_type, data, cas):
	url="http://%s/user.blob.get.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] , blob_type)
	add_headers = ['X-Operation: user.blob.set']
	return curl_web_req2(url,{},add_headers)

def friend_blob_get_no_Zauth_head(fid, blob_type ):
	url = "http://%s/friend.blob.get.php/%s/%s" % (SERVICE_URL[random.randrange(0,SERVERS)] , fid , blob_type)
        add_headers = ['X-Operation: friend.blob.get' ]
        return curl_web_req2(url , { } , add_headers)

def user_scoreboard_create(zauth,ival,scoreboard_type=''):
        url = "http://%s/user.scoreboard.create.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_type)
        add_headers = ['X-Operation: user.scoreboard.create']
	if ' ' in str(ival):
		return curl_web_req(zauth, url, {}, add_headers)
	else:	
		return curl_web_req(zauth, url, {"initial" :ival} ,add_headers)

def user_scoreboard_get(zauth,scoreboard_key=' '):
	url = "http://%s/user.scoreboard.get.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: user.scoreboard.get']
	return curl_web_req(zauth,url,{}, add_headers)

def friend_scoreboard_get(fzauth,scoreboard_key=' ' ):
	url = "http://%s/friend.scoreboard.get.php/%s"  %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: friend.scoreboard.get']
	return curl_web_req(fzauth, url , {} , add_headers)

def friend_scoreboard_increment(fzauth, scoreboard_key= ' '):
	url = "http://%s/friend.scoreboard.increment.php/%s"  %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: friend.scoreboard.increment']
	return curl_web_req(fzauth, url , {} , add_headers)

def friend_scoreboard_decrement(fzauth, scoreboard_key= ' '):
	url = "http://%s/friend.scoreboard.decrement.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: friend.scoreboard.decrement']
	return curl_web_req(fzauth, url , {} , add_headers)

def user_scoreboard_setmeta(zauth, scoreboard_key, meta_data):
	url = "http://%s/user.scoreboard.setmeta.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: user.scoreboard.setmeta']
	return curl_web_req(zauth, url ,meta_data, add_headers)

def user_scoreboard_delete(zauth,scoreboard_key= ' '):
	url = "http://%s/user.scoreboard.delete.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_key)
	add_headers = ['X-Operation: user.scoreboard.delete']
	return curl_web_req(zauth, url, {}, add_headers)

def user_scoreboard_meta_create(zauth,meta_data,scoreboard_type, ival ):
	url = "http://%s/user.scoreboard.create.php/%s" %(SERVICE_URL[random.randrange(0,SERVERS)] ,scoreboard_type)
	add_headers = ['X-Operation: user.scoreboard.create']
	return curl_web_req(zauth, url,{ "initial" : ival, "meta": meta_data} ,add_headers)




"""
mqs query to get friend and non-friend IDs for friend.blobs and deltas.
Check is made to verify the user has friend list, if not graph.user.add API is called and then the list is taken
"""



def get_friend_nofriend_id(zauth, graph_type):
	url = "http://%s/graph.user.getmembers" %(MQS_URL[random.randrange(0,MQS_SERVERS)] )
	add_headers = ['X-Operation: graph.user.getmembers']
	ret = curl_web_req(zauth , url , {"version": 1 ,"graph-type": [Constants.GRAPH_TYPE]} , add_headers)
	if ret['result']['data'][Constants.GRAPH_TYPE] == []:
		add_headers = ['X-Operation: graph.user.add']
		ret1=curl_web_req(zauth, url, {"version" : 1, "graph-type": Constants.GRAPH_TYPE, "uid-list": [101]},add_headers)	
		"""also add zauth in fid's list, else fid will be in wait state """
		[zid,expire,sig] = zauth.split('.')
                if(Constants.MULTI_TENDENCY):
                        [game_id,zid] = zid.split(':')
		add_headers = ['X-Operation: graph.user.add']
		zauth = AuthSystem.getUntrustedToken(101)
		ret2=curl_web_req(zauth, url, {"version" : 1, "graph-type": Constants.GRAPH_TYPE, "uid-list": [zid]}, add_headers)

		add_headers = ['X-Operation: graph.user.getmembers']
		ret = curl_web_req(zauth , url , {"version": 1 ,"graph-type": [Constants.GRAPH_TYPE]} , add_headers)
		#print "ret from  MQS get graph members: %s" %ret
	
	if ret is None:
		print " Please, check for MQS host's availibility"
	return ret
