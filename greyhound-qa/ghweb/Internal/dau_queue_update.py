#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

def get_dau_data(version, uidlist):
	data = {"version": version, "uid-list": uidlist}
	return data

class dau_update_class(unittest.TestCase):

	def check_pass(self, zauth, version, uidlist):
		data = get_dau_data(version, uidlist)
		ret =dau_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False, ret]
				for id in uidlist:
					if  ret["result"]["data"][str(id)] is not True:
							return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, uidlist, err_code):
		data = get_dau_data(version, uidlist)
		ret =dau_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_dau_queue_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]		
		ret, result = self.check_pass(zauth,Constants.VERSION, uidlist) 
		self.assertTrue(ret,msg=result)


	def test_dau_queue_update_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                err_code =403
                uidlist = [random.randint(100,200) for x in range(10)]
                ret, result = self.check_fail(zauth,Constants.VERSION, uidlist,err_code)
                self.assertTrue(ret,msg=result)

	def test_dau_queue_update_expired_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID,expires = 1)
		time.sleep(2)
                err_code =403
                uidlist = [random.randint(100,200) for x in range(10)]
                ret, result = self.check_fail(zauth,Constants.VERSION, uidlist,err_code)
                self.assertTrue(ret,msg=result)


	def test_dau_queue_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code =3
                uidlist = [random.randint(100,200) for x in range(10)]
                ret, result = self.check_fail(zauth,Constants.VERSION + 1 , uidlist,err_code)
                self.assertTrue(ret,msg=result)


	def test_dau_queue_empty_uidlist(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                uidlist = []
                ret, result = self.check_fail(zauth, Constants.VERSION,uidlist,500)
                self.assertTrue(ret,msg="Refer Jira defect: SEG_9277")



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(dau_update_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
