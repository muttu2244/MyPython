#!/usr/bin/python26
import sys,os
from fraud_update import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *


class fraud_queue_update_class(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret = fraud_queue_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth,data, err_code):
		ret = fraud_queue_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_fraud_queue_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		version = 1
		gameid=12
		uidlist = [random.randint(100,200) for x in range(2)]	
		#first update the fraud-history with some data by calling fraud_update.py
		obj=fraud_update_class(methodName='check_pass')
		data = {"version": version, "uid-list": uidlist, "game-id": gameid}
		ret,result=obj.check_pass(zauth,data)
		
		
		data = {"version": version, "start-time": 1, "end-time": time.time()}
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)


	def test_fraud_queue_update_with_Untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
		version =1
		err_code = 403
		data = {"version": version, "start-time": 1, "end-time": time.time()}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)

	def test_fraud_queue_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                version = 2
		err_code =3
		data = {"version": version, "start-time": 1, "end-time": time.time()}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)

	def test_fraud_queue_update_Missing_timestamps(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                version = 1
                err_code =500
                data = {"version": version}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg="Refer Jira defect :SEG-9261" )

	def test_fraud_queue_update_with_wrong_timestamps(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                version = 1
                err_code =500
		data = {"version": version, "start-time": 1, "end-time": time.time()}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg="Refer Jira defect: SEG-9262")


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(fraud_queue_update_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
