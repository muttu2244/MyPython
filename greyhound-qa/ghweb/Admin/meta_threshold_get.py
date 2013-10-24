#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random, time
from auth import *
from internal_api import *
from admin_api import *
from thresholds_update import *

class meta_threshold_get(unittest.TestCase):
	
	def check_pass(self, zauth, data):
		ret = user_meta_threshold_get(zauth, data)
		try:
			if ret["error"] == 0:
				return [True, ret]
			else:
				return [False, ret]
		except:	
			return [False, ret]

	def check_fail(self, zauth, data, err_code):
		ret = user_meta_threshold_get(zauth, data)
		try:
			if ret["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [Fasle, ret]

	def test_meta_threshold_get(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		data = get_threshold_data(Constants.VERSION,Constants.LEVEL,[int(Constants.ZID)])
		th = thresholds_update(methodName = 'check_pass')
		ret, result = th.check_pass(zauth,data)
		time.sleep(3)
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		data = {"version":Constants.VERSION, "level": Constants.LEVEL }
		ret, result = self.check_pass(zauth, data)
		self.assertTrue(ret, msg=result)
		
	def test_meta_threshold_get_invalid_version(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		data = {"version": Constants.VERSION+1, "level" : Constants.LEVEL}
		ret, result = self.check_fail(zauth, data, err_code = 3)
		self.assertTrue(ret, msg=result)

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(meta_threshold_get)
	unittest.TextTestRunner(verbosity=99).run(suite0)
