#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from archive_queue_update import * 


class archive_fetch(unittest.TestCase):

	def check_pass(self, zauth, data):
		data1={"version": data['version'],"item-count": data['item-count']}
		ret = archive_queue_fetch(zauth, data1)
		try:
			if ret["status"]["error"] == 0:
				if ret["result"]["partial"]:
				#if ret["result"]["data"] != {'archive-items': data['uid-list']}:
					return [False, "Failed"]
				
				else:
					return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, data, err_code):
		data1={"version": data['version'],"item-count": data['item-count']}
		ret = archive_queue_fetch(zauth, data1)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_archive_queue_fetch_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(2)]		
		data = {"version": Constants.VERSION, "uid-list": uidlist}
		obj = archive_update(methodName='check_pass')
		obj.check_pass(zauth,data)

		#p =[]	
		#for i in uidlist:
			#x = '%s' %i
			#p.append(x)
	
		#uidlist=p
		uidlist = " " .join(str(x) for x in uidlist).split()
		data =  {"version": Constants.VERSION, "item-count":len(uidlist) ,"uid-list": uidlist}	
		ret, result = self.check_pass(zauth, data) 
		self.assertTrue(ret,msg=result)


	def test_archive_queue_fetch_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		uidlist = [random.randint(100,200) for x in range(10)]
                data = {"version": Constants.VERSION, "uid-list": uidlist}

                obj = archive_update(methodName='check_pass')
                obj.check_pass(zauth,data)

		uidlist = " " .join(str(x) for x in uidlist).split()
		data =  {"version": Constants.VERSION, "item-count": len(uidlist) ,"uid-list": uidlist}
		err_code=403
		ret, result = self.check_fail(zauth,data,err_code)
		self.assertTrue(ret,msg=result)



	def test_archive_queue_fetch_when_queue_is_empty(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                data =  {"version": Constants.VERSION, "item-count": random.randint(1,3)}
		#Empty the memsched queue
		Clean_Memsched("archive_sample")
		err_code=500
		ret, result = self.check_fail(zauth,data,err_code)
		self.assertTrue(ret,msg=result)
		
		

	def test_archive_queue_fetch_with_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		data =  {"version": Constants.VERSION + 1 , "item-count":random.randint(1,3) }
		err_code=3
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)


	



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(archive_fetch)
        unittest.TextTestRunner(verbosity=99).run(suite0)
