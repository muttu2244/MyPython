#!/usr/bin/python26
import sys,os
from user_blob_archive import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from gh_api import *
from internal_api import *


class revert_blob(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret =user_blob_revert(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					for id in data["uid-list"]:
						if  ret["result"]["data"][str(id)]["error"] !=0:
							return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth,data, err_code):
		ret = user_blob_revert(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				for zid in data['uid-list']:
					if  ret["result"]["data"][str(zid)]["error"] == err_code and ret["result"]["data"][str(zid)]["archived"] is False:
						return [True, ret]
					else:
						return [False, ret]
			elif ret["status"]["error"] == err_code:
				return [True, ret]

			else:
				return[False,ret]
		except:
			return [False, ret]

	def test_user_blob_revert_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(3)]	
		data_to_set={"cash": 100, "coins": 700, "xp": 12}
		blobTypes =[Constants.USER_BLOB,Constants.USER_BLOB2]	
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
		
		data = {"version": Constants.VERSION, "uid-list": uidlist, "interval":Constants.ARCHIVE_INTERVAL }
		#First archive the blob at an interval of 6, before reverting
		obj=archive_blob(methodName='check_pass')
		ret,result=obj.check_pass(zauth,data)
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)



	def test_user_blob_revert_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code=3
		uidlist = [random.randint(100,200) for x in range(3)]
		data = {"version": Constants.VERSION + 1 , "uid-list": uidlist, "interval":Constants.ARCHIVE_INTERVAL }
		ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)


	

	def test_user_blob_revert_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                err_code= 403
                uidlist = [random.randint(100,200) for x in range(3)]
                data = {"version": Constants.VERSION, "uid-list": uidlist, "interval":Constants.ARCHIVE_INTERVAL }
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(revert_blob)
        unittest.TextTestRunner(verbosity=99).run(suite0)
