#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *


class fraud_update_class(unittest.TestCase):

	def check_pass(self, zauth,data):
		ret = fraud_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, data,err_code):
		ret = fraud_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_fraud_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]		
		data={"version": Constants.VERSION, "uid-list": uidlist, "game-id":Constants.GAME_ID }
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)

	
	def test_fraud_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code=3
                uidlist = [random.randint(100,200) for x in range(10)]
                data={"version": Constants.VERSION + 1 , "uid-list": uidlist, "game-id": Constants.GAME_ID }
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)


	def test_fraud_update_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
                err_code= 403
                uidlist = [random.randint(100,200) for x in range(10)]
                data={"version": Constants.VERSION, "uid-list": uidlist, "game-id":Constants.GAME_ID }
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)

	
	def test_fraud_update_empty_uidlist(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                err_code= 400
		uidlist=[]
                data={"version": Constants.VERSION, "uid-list": uidlist, "game-id":Constants.GAME_ID }
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)

	


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(fraud_update_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
