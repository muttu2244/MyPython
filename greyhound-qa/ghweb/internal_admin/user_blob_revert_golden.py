#!/usr/bin/python26
import sys,os
from user_golden_blob_update import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from gh_api import *


class golden_revert_class(unittest.TestCase):

	def check_pass(self, zauth, version):
		data = {"version": version }
		ret = user_blob_revert_golden(zauth,data)
		try:
			if ret["error"] != 0:
				return [False,ret]
			return [True,ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version,err_code):
		data={"version": version}
		ret = user_blob_revert_golden(zauth,data)
		try:
			if ret["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	def test_user_blob_golden_revert_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist=[Constants.ZID]
		#set the current blob for the zids
		data_to_set= '{"gold":7200, "cash": 1500, "energy": 5 }'
		blobTypes=['player', 'game-world']
		for zid in uidlist:
			Untrusted_zauth=  AuthSystem.getUntrustedToken(zid)
			for blob_type in blobTypes:
			#get the CAS value using user.blob.get API
				ret=user_blob_get(Untrusted_zauth,blob_type)
				if ret["blobs"][blob_type]["error"] == 404:
					cas = ' '
					#no blob for this user.
					ret=user_blob_set(Untrusted_zauth,blob_type,data_to_set,cas)
					if ret["error"] != 0:
						self.assertTrue(ret,"Data set failed for zid %d" %(zid))

		#making an object of golden_update , we need to have golden blobs before doing revert.
		obj = golden_update_class(methodName='check_pass')
		ret,result=obj.check_pass(zauth,Constants.VERSION,uidlist)	
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID)
		ret, result = self.check_pass(zauth,Constants.VERSION) 
		self.assertTrue(ret,msg=result)



	def test_user_blob_golden_revert_with_no_golden_blob(self):
		uidlist = [random.randint(1000,2000) for x in range(10)]
                for zid in uidlist:
                        Untrusted_zauth = AuthSystem.getUntrustedToken(zid)
                        ret = user_blob_get(Untrusted_zauth,Constants.USER_BLOB)
                        if ret["blobs"][Constants.USER_BLOB]["error"] == 404:
                                reqd_zid=zid
                                break
                        else:
                                self.assertTrue(False, msg="Didnt find empty blob zid")
                zauth = AuthSystem.getImpersonatedAuthToken(reqd_zid)
                err_code=500
                ret, result = self.check_fail(zauth,Constants.VERSION,err_code)
                self.assertTrue(ret,msg=result)
				
	


	def test_user_blob_golden_revert_with_wrong_version(self):
		zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID )
		err_code=3
		ret, result = self.check_fail(zauth,Constants.WRONG_VERSION,err_code)
                self.assertTrue(ret,msg=result)



	def test_user_blob_golden_revert_with_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
                err_code=403
                ret, result = self.check_fail(zauth,Constants.VERSION,err_code)
                self.assertTrue(ret,msg=result)


		


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(golden_revert_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
