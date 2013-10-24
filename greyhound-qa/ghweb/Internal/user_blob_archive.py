#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from gh_api import *
from internal_api import *


class archive_blob(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret =user_blob_archive(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					for id in data["uid-list"]:
						if  ret["result"]["data"][str(id)]["error"] !=0 or ret["result"]["data"][str(id)]["archived"] is not True:
							return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth,data, err_code):
		ret = user_blob_archive(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				for zid in data['uid-list']:
					if  ret["result"]["data"][str(zid)]["error"] == err_code and ret["result"]["data"][str(zid)]["archived"] is False:
						return [True, ret]
					else:
						return [False, ret]

			elif ret["status"]["error"] == err_code:
				return [True,ret]
			
			else:
				return[False,ret]
		except:
			return [False, ret]




	"""---------------------------------Test cases-----------------------------------------------------"""

	def test_user_blob_archive_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(3)]	
		data_to_set={"cash": 100, "coins": 700, "xp": 12}
		
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
		
		data = {"version": Constants.VERSION, "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)


	def test_user_blob_archive_zids_with_no_current_blob(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code = 404 
                uidlist = [random.randint(1,200) for x in range(5)]
		new_list=[]
		blobTypes =[Constants.USER_BLOB,Constants.USER_BLOB2]
                for zid in uidlist:
                        Untrusted_zauth=  AuthSystem.getUntrustedToken(zid)
                        for blob_type in blobTypes:
                        #get the CAS value using user.blob.get API
                                ret=user_blob_get(Untrusted_zauth,blob_type)
                                if ret["blobs"][blob_type]["error"] == 404:
					new_list.append(zid)
		if not new_list:
			self.assertTrue(False, msg='Could not find zid with empty blob in given range')
		uidlist=new_list
		data = {"version": Constants.VERSION, "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)



	def test_user_blob_archive_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                err_code = 3 
		uidlist = [random.randint(1,200) for x in range(5)]
		data = {"version":Constants.VERSION + 1  , "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)


	def test_user_blob_archive_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
                err_code = 403
                uidlist = [random.randint(1,200) for x in range(5)]
                data = {"version": Constants.VERSION, "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)

	def test_user_blob_archive_empty_uidlist(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                err_code = 500
                uidlist = [random.randint(1,200) for x in range(5)]
                data = {"version": Constants.VERSION, "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg="Refer Jira defect: SEG-9277")
	

	def test_user_blob_archive_expiredToken(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, expires = 1 )
                err_code = 403
		time.sleep(2)
                uidlist = [random.randint(1,200) for x in range(5)]
                data = {"version": Constants.VERSION, "uid-list": uidlist, "interval": Constants.ARCHIVE_INTERVAL}
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)

	

"""-------------------------------MAIN------------------------------"""		

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(archive_blob)
        unittest.TextTestRunner(verbosity=99).run(suite0)
