#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *


class archive_update(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret = archive_update_API(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False,ret]
				for id in data["uid-list"]:
					if  ret["result"]["data"][str(id)] is not True:
						return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth,data, err_code):
		ret = archive_update_API(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_archive_queue_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]		
		data = {"version": Constants.VERSION, "uid-list": uidlist}
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)


	def test_archive_queue_update_with_Untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
		err_code = 403
                uidlist = [random.randint(100,200) for x in range(10)]
                data = {"version": Constants.VERSION, "uid-list": uidlist}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)

	def test_archive_queue_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code =3
                uidlist = [random.randint(100,200) for x in range(10)]
		data = {"version": Constants.WRONG_VERSION, "uid-list": uidlist}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)


	def test_archive_queue_empty_uidlist(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = []
		data = {"version": Constants.VERSION, "uid-list": uidlist}
		ret, result = self.check_fail(zauth, data,500)
		self.assertTrue(ret,msg="Refer Jira defect: SEG_9277")

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(archive_update)
        unittest.TextTestRunner(verbosity=99).run(suite0)
