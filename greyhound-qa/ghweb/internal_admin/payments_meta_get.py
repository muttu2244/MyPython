#!/usr/bin/python26
import sys,os
from time import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

def  payment_append(uidlist):
	for id in uidlist:
		pay_data = json.dumps({"version": 1, "payment": { "gold": 100}})
		ret= payments_append(AuthSystem.getImpersonatedAuthToken(id), pay_data)

def get_payment_data(version, uidlist):
        data = {"version": version, "zidinfo-list": [] }
        for id in uidlist:
                value = {"zid": str(id), "start-time": 1, "end-time": time.time()}
		data["zidinfo-list"].append(value)
                #data["zidinfo-list"].update( value)
        return data

class payments_get_class(unittest.TestCase):

	def check_pass(self, zauth, data):
		ret1=get_payment_data(data["version"],data["uid-list"])
		value={"fields": ["gold"]}
		ret1.update(value)
	#	ret1=json.dumps(ret1)
		
		ret = user_payments_meta_get(zauth,ret1)
		try:
			if ret["status"]["error"] == 0: 
				if ret["result"]["partial"]:
					return [False, "Unsuccessful for zid %d"%(id)]
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth,data, err_code):
		ret1=get_payment_data(data["version"],data["uid-list"])
                value={"fields": ["gold"]}
                ret1.update(value)

		ret = user_payments_meta_get(zauth ,ret1)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_payments_meta_get_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]
		for id in uidlist:
			payment_append(str(id))

		#data = {"version": version, "zidinfo-list": ["zid": id], "fields" : ["cash","gold"] }
		data = {"version": Constants.VERSION,"uid-list": uidlist}		
		ret, result = self.check_pass(zauth, data)
		self.assertTrue(ret,msg=result)


	
	def test_payments_meta_get_UntrustedToken(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID )
		err_code= 403
                uidlist = [random.randint(100,200) for x in range(10)]
                data = {"version": Constants.VERSION,"uid-list": uidlist}
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)



	def test_payments_meta_get_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                err_code= 3
                uidlist = [random.randint(100,200) for x in range(10)]
                data ={ "version": Constants.WRONG_VERSION,"uid-list": uidlist}
                ret, result = self.check_fail(zauth,data,err_code)
                self.assertTrue(ret,msg=result)


	

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(payments_get_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
