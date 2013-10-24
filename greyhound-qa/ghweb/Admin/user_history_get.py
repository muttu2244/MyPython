#!/usr/bin/python26
import sys,os
from time import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from admin_api import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../Internal")
from history_update import *


class history_get_class(unittest.TestCase):

	def check_pass(self, zauth, version,start,end):
		data = {"version": version,"start": start, "end": end}
		ret = user_history_get(zauth, data)
		try:
			if ret["blobs"]["history"]["error"] == 0:
					return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, err_code,start,end):
		data = {"version": version, "start": start, "end": end}
		ret = user_history_get(zauth, data)
		try:
				if ret["error"] == err_code:
					return [True, ret]

				else:
					return [False, ret]
	
		except:
			return [False, ret]


	def test_history_get_functional(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		#update the history before fetch
		#create an object of class history_update
		obj = history_update(methodName='check_pass')
		zauth2= AuthSystem.getTrustedAuthToken(Constants.ZID )
		obj.check_pass(zauth2, Constants.VERSION,[Constants.ZID])		

		ret,result = self.check_pass(zauth,Constants.VERSION ,1,time.time())
		self.assertTrue(ret, msg=result)

	def test_history_get_invalid_version(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		err_code=3
		#update the history before fetch
                #create an object of class history_update
                obj = history_update(methodName='check_pass')
                zauth2= AuthSystem.getTrustedAuthToken(Constants.ZID )
                obj.check_pass(zauth2, Constants.VERSION,[Constants.ZID])
		ret, result = self.check_fail(zauth, Constants.VERSION + 1 ,err_code,1,time.time())
		self.assertTrue(ret, msg=result)

	def test_history_get_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		err_code=403
		#update the history before fetch
                #create an object of class history_update
                obj = history_update(methodName='check_pass')
                zauth2= AuthSystem.getTrustedAuthToken(Constants.ZID )
                obj.check_pass(zauth2, Constants.VERSION,[Constants.ZID])
		ret, result = self.check_fail(zauth, Constants.VERSION,err_code,1,time.time()) 
		self.assertTrue(ret, msg=result)


	def test_history_get_wrong_time_stamps(self):
		#when start time is gretaer than end time
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
                ret,result = self.check_pass(zauth, Constants.VERSION,time.time(),1)
                self.assertTrue(ret, msg=result)
		

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(history_get_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
