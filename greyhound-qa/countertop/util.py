import os
import sys
import random
import time
import base64
import hmac
import hashlib
import struct
import socket
from time import time as now
import simplejson as json
import pycurl
import StringIO
import string

#APP_SECRET = "c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330"
APP_SECRET = "2244"
GID = 2244
#URL = "http://gh-mt-sample.greyhound.zynga.com/services/"
URL = "http://api.greyhound.zynga.com/services/"
#URL = "http://service.gh-mt-web.zynga.com/public/services/"
BLOB_TYPE = "game-world"
ZID = 10000

class bcolors:
    HEADER = '\033[35m'
    OKBLUE = '\033[34m'
    OKGREEN = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[31m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class Results:
	
	STATS = {}

	@staticmethod
	def printResults():
		def printCode(value):
                        if value == 200 or value == 0:
                                return bcolors.OKGREEN+str(value)+bcolors.ENDC
                        else:
                                return bcolors.FAIL + str(value) + bcolors.ENDC

		print bcolors.OKBLUE + "   API  \t\t    HTTP code  \t\tJSON code \n" + bcolors.ENDC
		for key,value in Results.STATS.items():
			t = key + "\t\t\t"
			httperr = value[0]
			jsonerr = value[1]
			print t + printCode(httperr)+"\t\t" + printCode(jsonerr)
	
	@staticmethod
	def Update(api, err, result):
		if result:
			try:
				jerr = result["blobs"][BLOB_TYPE]["error"]
			except KeyError:
				jerr = result["error"]
			except TypeError:
				jerr = "Memcache timeout, recieved empty blob"
		else:
			jerr = None
		Results.STATS.update({api: [err, jerr]})

class AuthSystem(object):
	READ_ONLY = 4
	USER = 3
	IMPERSONATED_USER = 1
	INTERNAL =2
	SECRET = APP_SECRET
	PREMIUM_FLAG = 0x00000001
	SUSPECT_FLAG = 0x00000002
	IMPERSONATE_FLAG = 0x00000004
	TRUSTED_FLAG = 0x00000008

	#signToken is a function that is used to sign the token with a secret
	@staticmethod
	def signToken(token, secret, trusted = False):
		if (trusted):
			secret =  secret[::-1]

		sig = base64.encodestring(hmac.new(secret, msg=token, digestmod=hashlib.sha256).digest()).strip()
		return "%s|%s"%(token, sig)


	#gen_auth creates a trusted auth token to be generated.
	@staticmethod
	def getAuthTokenOnCondition(zid, secret, expires = 3600, condition = -1):
		trusted = False
		t = now() + expires
		authbits  = 0
                zid = "%d:%s" % (GID , str(zid))
		if (condition == AuthSystem.USER):
			#This is not implemented
			pass
		elif (condition == AuthSystem.IMPERSONATED_USER):
			authbits |= AuthSystem.IMPERSONATE_FLAG
		elif (condition == AuthSystem.INTERNAL):
			authbits |= AuthSystem.TRUSTED_FLAG
			trusted = True
		elif (condition == AuthSystem.READ_ONLY):
                        authbits = 16
		else :
			raise Exception("Undefined condition for getting Auth Token")

		authbits_str = base64.encodestring(struct.pack("I", socket.htonl(authbits)))
		token = "%s.%d.%s"%(zid, t, authbits_str.strip())
		return AuthSystem.signToken(token, secret, trusted)


	@staticmethod
        def getUntrustedToken(zid , expires = 2000):
                return AuthSystem.getAuthTokenOnCondition(zid,AuthSystem.SECRET,expires,AuthSystem.USER)


def send_request(zauth, url, data=None, headers=[]):

        c = pycurl.Curl()
        c.setopt(pycurl.URL,url)
        headers = headers + [ 'Expect: ',"Z-Authorization: %s"%zauth ]
        c.setopt(pycurl.HTTPHEADER, headers)
        result = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, result.write)
	data = encode_post(data)
	c.setopt(pycurl.POSTFIELDS, data)
        try:
                c.perform()
        except:
                return 404,'Couldnt resolve host'
        ret = result.getvalue()
        result.close()
	ret = decode_post(ret)
        err_code = c.getinfo(pycurl.HTTP_CODE)
        c.close()
        return err_code, ret

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		return json.loads(data)
	except:
		return False



#                 Add Test Functions
#
def test_gh_web():
      	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/user.blob.get.php/" + BLOB_TYPE
        err , result = send_request(zauth,url)
	
	Results.Update("UserBlobGet",err,result)

def blob_set():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/user.blob.set.php/" + BLOB_TYPE
	data = "Blob data"
	headers = ["If-Match: "]
	err, result = send_request(zauth, url, data, headers)
	Results.Update("UserBlobSet", err, result)

def friend_blob_get():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/friend.blob.get.php/100/" + BLOB_TYPE
	err, result = send_request(zauth, url)
	Results.Update("FriendBlobGet", err, result)

def friend_add_delta():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/friend.blob.addDelta.php/100/visit"
	delta = "some delta"
	err, result = send_request(zauth, url, delta)
	Results.Update("FriendDeltaAdd", err, result)

def friend_query_delta():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/friend.blob.queryDeltas.php/200"
	query = {"query": "select * from deltas", "params":[]}
	err, result = send_request(zauth, url, query)
	Results.Update("FriendDeltas", err, result)

def user_query_delta():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL+"/user.blob.queryDeltas.php"
	query = {"query": "select * from deltas","params":[]}
	err, result = send_request(zauth, url, query)
	Results.Update("UserQueryDeltas", err, result)

def scoreboard_create():
	zauth = AuthSystem.getUntrustedToken(ZID)
	url = URL + "/user.scoreboard.create.php/viral"
	data = {"initial": 5}
	err, result = send_request(zauth, url, data)
	Results.Update("ScorebrdCreate", err, result)

if __name__ == "__main__":
	test_gh_web()
	blob_set()
	friend_blob_get()
	friend_add_delta()
	friend_query_delta()
	user_query_delta()
	scoreboard_create()
	Results.printResults()
