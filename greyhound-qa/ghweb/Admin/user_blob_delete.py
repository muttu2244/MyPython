#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from api_constants import *
from gh_api import *
from admin_api import *


class blob_delete_class(unittest.TestCase):

	def check_pass(self, zauth):
		ret = user_blob_delete(zauth,Constants.USER_BLOB)
		try:
			if ret["blobs"][Constants.USER_BLOB]["error"] != 0 and ret["blobs"]["status"] is not True:
				return [False, "Delete was Unsuccessful"]
			else:
				return [True, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, err_code):
		ret = user_blob_delete(zauth,Constants.USER_BLOB) 
		try:
			if ret["blobs"][Constants.USER_BLOB]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_user_blob_delete_functional(self):
                zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID )
		data_to_set='{"cash":100, "gold": 200, "xp": 5}'
		Untrusted_zauth=  AuthSystem.getUntrustedToken(Constants.ZID)
		#get the CAS value using user.blob.get API
		ret=user_blob_get(Untrusted_zauth,Constants.USER_BLOB)
		if ret["blobs"][Constants.USER_BLOB]["error"] == 404:
			cas = ' '
			#no blob for this user. Set the blob of type Constansts.USER_BLOB
			ret=user_blob_set(Untrusted_zauth,Constants.USER_BLOB,data_to_set,cas)
			if ret["error"] != 0:
				self.assertTrue(ret,"Data set failed for zid %d" %(zid))

		ret, result = self.check_pass(zauth) 
		self.assertTrue(ret,msg=result)


	def test_user_blob_delete_for_zid_with_no_blob(self):
		uidlist = [random.randint(1,200) for x in range(10)]
		for zid in uidlist:
			Untrusted_zauth=  AuthSystem.getUntrustedToken(zid)
			ret=user_blob_get(Untrusted_zauth,Constants.USER_BLOB)
			if  ret["blobs"][Constants.USER_BLOB]["error"] == 404:
				zid_req=zid
				break
		
		zauth = AuthSystem.getImpersonatedAuthToken(zid_req)
		err_code=404
		ret,result=self.check_fail(zauth,err_code)
		self.assertTrue(ret,msg=result)					

				
				
				

	

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(blob_delete_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
