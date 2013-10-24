#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

class reputation_update(unittest.TestCase):

	def update_credibility(self, uidlist, cred, version=1):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		reputation = [{"zid": uidlist[i],"fraud-score": 3, "credibility": cred[i], "updated-golden-state":True, "escalate": True} for i in range(len(uidlist))]
                ret, result = self.check_pass(zauth, version, reputation)
                self.assertTrue(ret, msg=result)
		return True


	def check_pass(self, zauth, version, reputation):
		data = {"version": version, "reputation-list": reputation}
		ret = user_reputation_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False, "Partial recieved is True"]
				else:
					for i in reputation:
						if not ret["result"]["data"][str(i["zid"])]:
							return [False, "Recieved True for "+str(i["zid"])]
					return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	def check_fail(self, zauth, version, reputation, err_code):
		data = {"version": version, "reputation-list": reputation}
		ret = user_reputation_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_reputation_update_functional(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = [{"zid": uid[i],"fraud-score": 3, "credibility": 0, "updated-golden-state": True, "escalate": True} for i in range(10)]
		ret, result = self.check_pass(zauth, Constants.VERSION, reputation)
		self.assertTrue(ret, msg=result)


	def test_reputation_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = [{"zid": uid[i], "fraud-score": 1,"credibility": 0, "updated-golden-state": True, "escalate": True} for i in range(10)]
		ret, result = self.check_fail(zauth, Constants.VERSION +1,reputation,3)
		self.assertTrue(ret, msg=result)

	def test_reputation_update_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = [{"zid": uid[i], "fraud-score": 1, "credibility": 0, "updated-golden-state": True, "escalate": True} for i in range(10)]
		ret, result = self.check_fail(zauth, Constants.VERSION, reputation,403)
		self.assertTrue(ret, msg=result)

	def test_reputation_update_credibility_greater(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = [{"zid": uid[i], "credibility": 75, "fraud-score": 1, "updated-golden-state": True, "escalate": True} for i in range(10)]
		ret, result = self.check_fail(zauth, Constants.VERSION, reputation,403)
		self.assertTrue(ret, msg='Refer jira bug SEG-9260')

	def test_reputation_update_empty_reputation(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = []
		ret, result = self.check_fail(zauth, Constants.VERSION, reputation,400)
		self.assertTrue(ret, msg= "Refer Jira defect: SEG-9277")
	
	def test_reputation_update_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, expires =1 )
		time.sleep(2)
		uid = [random.randint(100,200) for x in range(10)]
		reputation = [{"zid": uid[i],"fraud-score": 3, "credibility": 0, "updated-golden-state": True, "escalate": True} for i in range(10)]
		ret, result = self.check_fail(zauth, Constants.VERSION, reputation,403)
                self.assertTrue(ret, msg=result)



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(reputation_update)
        unittest.TextTestRunner(verbosity=99).run(suite0)	
	 
