#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *


class thresholds_fetch(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret = threshold_fetch_api(zauth,data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False, "Recieved partial True, expected False"]
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, data, err_code):
		ret = threshold_fetch_api(zauth,data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_threshold_fetch_functional(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		data = {"version": Constants.VERSION, "level": Constants.LEVEL}
		ret, result = self.check_pass(zauth, data)
		self.assertTrue(ret, msg=result)

	def test_threshold_fetch_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		data = {"version": Constants.WRONG_VERSION, "level": Constants.LEVEL}
		ret, result = self.check_fail(zauth, data, err_code=3)
		self.assertTrue(ret, msg=result)

	def test_threshold_fetch_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		data = {"version": Constants.VERSION, "level": Constants.LEVEL}
		ret, result = self.check_fail(zauth, data, err_code = 403)
		self.assertTrue(ret, msg=result)


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(thresholds_fetch)
	unittest.TextTestRunner(verbosity=99).run(suite0)
