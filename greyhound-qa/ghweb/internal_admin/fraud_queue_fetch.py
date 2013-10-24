#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from fraud_queue_update import * 


class fraud_queue_fetch_class(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret = fraud_queue_fetch(zauth, data)
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
		ret = fraud_queue_fetch(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]
	'''
	def test_fraud_queue_fetch_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		version = 1
		itemcount=2

		data = {"version": version, "start-time": 1 , "end-time": time.time()}
			        
		obj = fraud_queue_update_class(methodName='check_pass')
		ret,result=obj.check_pass(zauth,data)

		data =  {"version": version, "item-count": itemcount}
		ret, result = self.check_pass(zauth, data) 
		self.assertTrue(ret,msg=result)
	'''

	def test_archive_queue_fetch_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		version=1
		itemcount=3

		data = {"version": version, "start-time": 1 , "end-time": time.time()}

                obj = fraud_queue_update_class(methodName='check_pass')
                obj.check_pass(zauth,data)

                data =  {"version": version, "item-count": itemcount}

		err_code=403
		ret, result = self.check_fail(zauth,data,err_code)
		self.assertTrue(ret,msg=result)



	def test_archive_queue_fetch_when_queue_is_empty(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                version=1
		itemcount=3	
		
                data =  {"version": version, "item-count": itemcount}
		GH_MSCHED='10.32.233.230'
		PORT='11213'
		#Empty the memsched queue
		process=subprocess.Popen('echo  "flush_all fraud_sample" |  nc %s %s' %( GH_MSCHED, PORT), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output,stderr=process.communicate()
                if output.rstrip() != 'OK':
                        self.assertTrue(False, msg="Memsched queue could not be emptied")

		err_code=500
		ret, result = self.check_fail(zauth,data,err_code)
		self.assertTrue(ret,msg=result)
		
		

	def test_fraud_queue_fetch_with_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                version = 21
                itemcount=1
		
		data =  {"version": version, "item-count": itemcount}
		err_code=3
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)


	



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(fraud_queue_fetch_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
