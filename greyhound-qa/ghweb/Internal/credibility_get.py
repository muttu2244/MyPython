#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
import time
from reputation_update import *

"""---------------------------Functions to determine test pass/fail ------------------------"""
class credibility_get(unittest.TestCase):

	def check_pass(self, zauth, version, uidlist, cred=[]):
		data = {"version": version, "uid-list": uidlist}
		ret = user_credibility_get(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if not ret["result"]["partial"]:
					if cred:
						for i in range(len(uidlist)):
							if ret["result"]["data"][str(uidlist[i])] != cred[i]:
								print 'Credibility not equal', i, cred[i],uidlist[i]
								return [False, ret]
					return [True, ret]
			else:
				return [Fasle, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, uidlist, err_code):
		data = {"version": version, "uid-list": uidlist}
		ret = user_credibility_get(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	"""-------------------------------Test cases --------------------------------------------"""

	def test_credibility_get_functional(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uidlist = [ random.randint(1,300) for i in range(10) ]
		cred = [ random.randint(0,3) for i in range(len(uidlist)) ]  #Updates the credibility of uidlist 
		obj = reputation_update(methodName='update_credibility')
		obj.update_credibility(uidlist, cred,Constants.VERSION)
		ret, result = self.check_pass(zauth, Constants.VERSION, uidlist, cred)
		self.assertTrue(ret, msg=result)

	def test_credibility_get_Wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
                uidlist = [ random.randint(1,300) for i in range(10) ]
                cred = [ random.randint(0,3) for i in range(len(uidlist)) ]  #Updates the credibility of uidlist 
                obj = reputation_update(methodName='update_credibility')
                obj.update_credibility(uidlist, cred,Constants.VERSION)
                ret, result = self.check_fail(zauth, Constants.VERSION + 1, uidlist, 3)
                self.assertTrue(ret, msg=result)


	def test_credibility_get_untrusted_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		uidlist = [ random.randint(1,300) for i in range(10) ]
		ret, result = self.check_fail(zauth,Constants.VERSION , uidlist, 403)
		self.assertTrue(ret, msg=result)

	def test_credibility_get_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, 1)
		time.sleep(2)
		uidlist = [ random.randint(100,200) for i in range(10) ]
		ret, result = self.check_fail(zauth,Constants.VERSION, uidlist, 403)
		self.assertTrue(ret, msg=result)

	def test_credibility_get_without_uid(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uidlist = []
		ret, result = self.check_fail(zauth, Constants.VERSION, uidlist, 0)
		self.assertTrue(ret, msg=result)

	

"""---------------------------------MAIN ---------------------------------------"""
if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(credibility_get)
        unittest.TextTestRunner(verbosity=99).run(suite0)
