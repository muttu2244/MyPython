import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

class reputation_get(unittest.TestCase):

	def check_pass(self, zauth, version):
		data = {"version": version}
		ret = user_reputation_get(zauth, data)
		try:
			if ret["blobs"]["reputation"]["error"] == 0:
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, err_code):
		data = {"version": version}
		ret = user_reputation_get(zauth, data)
		try:
			if ret["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	def test_reputation_get_functional(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		ret,result = self.check_pass(zauth, Constants.VERSION)
		self.assertTrue(ret, msg=result)

	def test_reputation_get_invalid_version(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		ret, result = self.check_fail(zauth, Constants.WRONG_VERSION, 3)
		self.assertTrue(ret, msg=result)

	def test_reputation_get_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = self.check_fail(zauth, Constants.VERSION, 403)
		self.assertTrue(ret, msg=result)

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(reputation_get)
        unittest.TextTestRunner(verbosity=99).run(suite0)
