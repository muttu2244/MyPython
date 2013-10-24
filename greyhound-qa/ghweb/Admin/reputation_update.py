import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from admin_api import *

class admin_reputation_update(unittest.TestCase):

	def check_pass(self, zauth, version,cred):
		data = {"version": version, "credibility": cred}
		ret = user_reputation_update(zauth, data)
		try:
			if ret["blobs"]["reputation"]["error"] == 0:
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version,cred, err_code):
		data = {"version": version, "credibility": cred}
		ret = user_reputation_update(zauth, data)
		try:
			if ret["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	"""--------------------------------Test cases------------------------------"""


	def test_reputation_update_functional(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		cred = random.randint(0,2)
		ret,result = self.check_pass(zauth, Constants.VERSION,cred)
		self.assertTrue(ret, msg=result)

	def test_reputation_update_wrong_version(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		cred = random.randint(0,2)
		ret, result = self.check_fail(zauth, Constants.VERSION + 1 , cred, 3 )
		self.assertTrue(ret, msg=result)

	def test_reputation_update_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		cred = random.randint(0,2)
		ret, result = self.check_fail(zauth, Constants.VERSION,cred, 403)
		self.assertTrue(ret, msg=result)

	def test_reputation_update_ExpiredToken(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID, expires =1)
		time.sleep(2)
                cred = random.randint(0,2)
                ret,result = self.check_fail(zauth, Constants.VERSION,cred, 403)
                self.assertTrue(ret, msg=result)

	def test_reputation_update_without_credibility(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		cred = random.randint(0,2)
                ret,result = self.check_fail(zauth, Constants.VERSION,cred,500)
                self.assertTrue(ret, msg="Refer  Jira defect: SEG-9277")



"""-----------------------------------MAIN-----------------------------------------------"""
if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(admin_reputation_update)
        unittest.TextTestRunner(verbosity=99).run(suite0)
