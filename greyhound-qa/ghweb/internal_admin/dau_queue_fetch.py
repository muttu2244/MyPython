#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from dau_queue_update import * 


class dau_fetch(unittest.TestCase):

	def check_pass(self, zauth,data):
		data1={"version": data['version'],"item-count": data['item-count']}
		ret =dau_queue_fetch(zauth, data1)
		try:
			if ret["status"]["error"] == 0:
				#if ret["result"]["data"] != {'dau-items': data['uid-list']}:
				if ret["result"]["partial"]:
					return [False, "Failed"]
				
				else:
					return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, data, err_code):
		data1={"version": data['version'],"item-count": data['item-count']}
		ret = dau_queue_fetch(zauth, data1)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_dau_queue_fetch_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(2)]		
		 
		obj =dau_update_class(methodName='check_pass')
		obj.check_pass(zauth,Constants.VERSION,uidlist)

		p =[]	
		for i in uidlist:
			x = '%s' %i
			p.append(x)
	
		uidlist=p
		data =  {"version":Constants.VERSION, "item-count": len(uidlist),"uid-list": uidlist}	
		ret, result = self.check_pass(zauth, data) 
		self.assertTrue(ret,msg=result)


	def test_dau_queue_fetch_TrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		uidlist = [random.randint(100,200) for x in range(10)]

                obj =dau_update_class(methodName='check_pass')
                obj.check_pass(zauth,Constants.VERSION,uidlist)

                p =[]
                for i in uidlist:
                        x = '%s' %i
                        p.append(x)

                uidlist=p

                data =  {"version": Constants.VERSION, "item-count": len(uidlist),"uid-list": uidlist}
		err_code=403
                ret, result = self.check_fail(zauth, data,err_code)
                self.assertTrue(ret,msg=result)



	def test_dau_queue_fetch_when_queue_is_empty(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                data =  {"version": Constants.VERSION, "item-count":random.randint(1,3)}
		Clean_Memsched("dau_sample")
                err_code=500
                ret, result = self.check_fail(zauth,data,err_code)



	def test_dau_queue_fetch_with_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                data =  {"version": Constants.VERSION, "item-count": random.randint(1,3)}
                err_code=3
                ret, result = self.check_fail(zauth,data,err_code)


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(dau_fetch)
        unittest.TextTestRunner(verbosity=99).run(suite0)
