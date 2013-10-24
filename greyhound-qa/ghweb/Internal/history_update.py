#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

def get_history_data(version, uidlist):
	data = {"version": version, "uid-list": {}}
	for id in uidlist:
		value = [{"operation": "harvest", "time": random.randrange(1000)}]
		data["uid-list"].update({str(id): value})
	return data

class history_update(unittest.TestCase):

	def check_pass(self, zauth, version, uidlist):
		data = get_history_data(version, uidlist)
		ret = user_history_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				for id in uidlist:
					if ret["result"]["data"][str(id)]["error"] != 0:
						return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, uidlist, err_code):
		data = get_history_data(version, uidlist)
		ret = user_history_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	"""--------------------------------Test cases-----------------------"""

	def test_history_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]		
		ret, result = self.check_pass(zauth, Constants.VERSION, uidlist)
		self.assertTrue(ret,msg=result)

	def test_history_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]
		ret, result = self.check_fail(zauth, Constants.VERSION + 1 , uidlist,3)
		self.assertTrue(ret, msg=result)

	def test_history_update_normal_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		uidlist = [random.randint(100,200) for x in range(10)]
		ret , result = self.check_fail(zauth, Constants.VERSION, uidlist, err_code = 403)
		self.assertTrue(ret, msg = result)

	def test_history_update_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, expires = 1)
		time.sleep(2)
		uidlist = [random.randint(100,200) for x in range(10)]
		ret , result = self.check_fail(zauth, Constants.VERSION, uidlist, err_code = 403)
		self.assertTrue(ret, msg = result)


"""--------------------------MAIN--------------------------------"""

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(history_update)
        unittest.TextTestRunner(verbosity=99).run(suite0)
