import time
import base64
import hmac
import hashlib
import struct
import socket
from api_constants import Constants
from time import time as now

#TBD configuration of ZLIVE SECRET
#ZLIVE_SECRET = "8a930dce0245c6e9b53c3fd153347d5c3ffa8457"
SECRET = Constants.SECRET

class AuthSystem(object):
	READ_ONLY = 4
	USER = 3
	IMPERSONATED_USER = 1
	INTERNAL =2

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
		zid = str(zid)
		if (Constants.MULTI_TENDENCY):
                        zid = "%d:%s" % (Constants.GAME_ID , zid)
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
                return AuthSystem.getAuthTokenOnCondition(zid,SECRET,expires,AuthSystem.USER)

        @staticmethod
        def getReadonlyToken(zid , expires = 3600):
                return AuthSystem.getAuthTokenOnCondition(zid,SECRET,expires,AuthSystem.READ_ONLY)


        @staticmethod
        def getExpiredToken(zid , expires = 0):
		t = AuthSystem.getAuthTokenOnCondition(zid,SECRET,expires,AuthSystem.USER)
		time.sleep(2)
                return t

        @staticmethod
        def getInvalidToken(zid , expires = 3600):
                secret = SECRET+"tmp"
                return AuthSystem.getAuthTokenOnCondition(zid,secret,expires,AuthSystem.USER)

	@staticmethod
	def getImpersonatedAuthToken(zid, expires = 3600):
		return AuthSystem.getAuthTokenOnCondition(zid, SECRET, expires,	AuthSystem.IMPERSONATED_USER)
	@staticmethod
	def getTrustedAuthToken(zid, expires = 3600):
		return AuthSystem.getAuthTokenOnCondition(zid, SECRET, expires,	AuthSystem.INTERNAL)

	@staticmethod
	def checkAuthToken(auth_token, secret = SECRET):
		(token, sig) = auth_token.split('|', 1)
		(zid, expires, authbits) = token.split('.', 2)

		ret = struct.unpack("I", base64.decodestring(authbits))
		authbits = socket.ntohl(ret[0])
		
		if (authbits & AuthSystem.TRUSTED_FLAG == AuthSystem.TRUSTED_FLAG):
			secret = secret[::-1]

		expected_sig = base64.encodestring(hmac.new(secret, msg=token, digestmod=hashlib.sha256).digest()).strip()

		if (expected_sig != sig):
			return [ False, None, 0, "Incorrect signature" ]

		if (int(expires) < now()):
			return [ False, None, 0, "Auth expired" ]
		
		return [ True, str(zid), authbits, "Success" ]

#Adding test code
def test():
	a =  AuthSystem.getUntrustedToken(12345)
	b = AuthSystem.checkAuthToken(a)
	print a
	print b

if __name__ == "__main__":
	test()
