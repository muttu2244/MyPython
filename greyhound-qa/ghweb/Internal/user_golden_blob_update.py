#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from gh_api import *

def get_golden_data(version, uidlist):
	data = {"version": version, "uid-list": uidlist}
        #	for id in uidlist:
	#		value = [{"operation": "harvest", "time": random.randrange(1000)}]
	#		data["uid-list"].update({str(id): value})
	return data

class golden_update_class(unittest.TestCase):

	def check_pass(self, zauth, version, uidlist):
		data = get_golden_data(version, uidlist)
		ret = user_blob_golden_update(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
					return [False,ret]
				else:
					for id in uidlist:
						if  ret["result"]["data"][str(id)]["error"]!= 0:
							return [False, "Unsuccessful for zid %d"%(id)]
					return [True, ret]
				

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, version, uidlist, err_code):
		data = get_golden_data(version, uidlist)
		ret = user_blob_golden_update(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
        	        	return [True, ret]
			if ret["status"]["error"] == 0:
				for id in uidlist:
                                        if  ret["result"]["data"][str(id)]["error"]== 0:
                                	        return [False, "Unsuccessful for zid %d"%(id)]
                                return [True, ret]

                	else:
                        	return [False, ret]
			
		except:
			return [False, ret]




	"""---------------------------Test cases-----------------------------"""

	def test_golden_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(3)]		
		#set the current blob for the zids
		data_to_set = '{"gold":7200, "cash": 1500, "energy": 5 }'
		blobTypes =[Constants.USER_BLOB,Constants.USER_BLOB2]
		for zid in uidlist:
			Untrusted_zauth =  AuthSystem.getUntrustedToken(zid)
			for blob_type in blobTypes:
			#get the CAS value using user.blob.get API
				ret=user_blob_get(Untrusted_zauth,blob_type)
				if ret["blobs"][blob_type]["error"] == 404:
					cas = ' '
					#no blob for this user.
					ret=user_blob_set(Untrusted_zauth,blob_type,data_to_set,cas)
					if ret["error"] != 0:
						self.assertTrue(ret,"Data set failed for zid %d" %(zid))

		ret, result = self.check_pass(zauth,Constants.VERSION, uidlist) 
		self.assertTrue(ret,msg=result)



	def test_golden_update_for_zid_with_no_blob(self):
		uidlist = [random.randint(1000,2000) for x in range(3)]
		for zid in uidlist: 
			Untrusted_zauth =  AuthSystem.getUntrustedToken(zid)
			ret = user_blob_get(Untrusted_zauth,Constants.USER_BLOB)
			if ret["blobs"][Constants.USER_BLOB]["error"] == 404:
				reqd_zid=zid
				break
			else:
				self.assertTrue(False, msg="Didnt find empty blob zid")
		zauth = AuthSystem.getTrustedAuthToken(reqd_zid)
		err_code=500
		uidlist=[reqd_zid]
		ret, result = self.check_fail(zauth,Constants.VERSION,uidlist,err_code)
		self.assertTrue(ret,msg=result)
				

	
	def test_golden_update_with_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		err_code =3
		uidlist = [random.randint(1000,2000) for x in range(3)]
		ret, result = self.check_fail(zauth,Constants.VERSION + 1 ,uidlist,err_code)
		self.assertTrue(ret,msg=result)


	def test_golden_update_with_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
                err_code =403
                uidlist = [random.randint(1000,2000) for x in range(3)]
                ret, result = self.check_fail(zauth,Constants.VERSION,uidlist,err_code)
                self.assertTrue(ret,msg=result)
		
	
	def test_golden_update_with_ExpiredToken(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID , expires = 1 )
		err_code = 403
		time.sleep(2)
		uidlist = [random.randint(1000,2000) for x in range(3)]
		ret, result = self.check_fail(zauth,Constants.VERSION ,uidlist,err_code)
                self.assertTrue(ret,msg=result)
	


""" -----------------------------MAIN------------------------------------------"""


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(golden_update_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
