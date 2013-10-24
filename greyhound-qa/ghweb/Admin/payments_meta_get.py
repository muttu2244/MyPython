#!/usr/bin/python26
import sys,os
from time import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *
from admin_api import *



def  payment_append(uid):
		pay_data = {"version": 1, "payment": { "gold": 100}}
		ret= payments_append(AuthSystem.getTrustedAuthToken(uid), pay_data)




"""-----------------------Functions to evaluate test pass/fail ---------------------"""

class admin_payments_get_class(unittest.TestCase):

	def check_pass(self, zauth, data):
		

		ret = user_admin_payments_meta_get(zauth, data)
		try:
			if ret["blobs"]["payments"]["error"] == 0: 
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]



	def check_fail(self, zauth,data, err_code):
		ret = user_admin_payments_meta_get(zauth , data)
		try:
			if ret["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]


	
	"""--------------------------------Test cases ---------------------------------------"""


	def test_payments_meta_get_functional(self):
		uid = random.randint(100,200 )
		zauth = AuthSystem.getImpersonatedAuthToken(uid)
		payment_append(str(uid))

		data = {"version": Constants.VERSION }
		ret, result = self.check_pass(zauth, data)
		self.assertTrue(ret,msg=result)


	
	def test_payments_meta_get_UntrustedToken(self):
		uid = random.randint(100,200 )
                zauth = AuthSystem.getUntrustedToken(uid)
                payment_append(str(uid))

                data = {"version": Constants.VERSION }
                ret, result = self.check_fail(zauth, data, 403)
                self.assertTrue(ret,msg=result)

	def test_payments_meta_get_ExpiredToken(self):
		uid = random.randint(100,200 )
                zauth = AuthSystem.getImpersonatedAuthToken(uid, expires = 1)
		time.sleep(2)
                payment_append(str(uid))

                data = {"version": Constants.VERSION }
                ret, result = self.check_fail(zauth, data, 403)
                self.assertTrue(ret,msg=result)

	def test_payments_meta_get_Wrong_version(self):
		uid = random.randint(100,200 )
		zauth = AuthSystem.getImpersonatedAuthToken(uid)
                payment_append(str(uid))

                data = {"version": Constants.VERSION + 1 }
                ret, result = self.check_fail(zauth, data, 3)
                self.assertTrue(ret,msg=result)


"""----------------------------------MAIN----------------------------------"""	

if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(admin_payments_get_class)
        unittest.TextTestRunner(verbosity=99).run(suite0)
