#!/usr/bin/python26
import sys
import os 
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import urllib
import urllib2
from api_constants import Constants
import random 
import time
from multiprocessing import Pool
import StringIO
import pycurl
import traceback
import select 
import unittest
from mqs_auth_api import *
from mqs_check import mqs_check as check
from mqs_auth import *
class mqs_auth(unittest.TestCase):
	ZID = Constants.ZID
	def setUp(self):
		return
		
	#
	# TestCases for the MQS meta APIs with different types of Auth Token
	#
	# META_USER_GET API..
	def test_meta_get_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)

	def test_meta_get_invalid_auth(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)

	def test_meta_get_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)

	def test_meta_get_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret,msg=result)

	def test_meta_get_without_token(self):
		zauth = ' '
		ret, result = check.check_fail(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)

	def test_meta_get_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)

	# META_USER_UPDATE

	def test_meta_update_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		fields["xp"] = 100
		fields["cash"] = 200 
		ret, result = check.check_pass(meta_user_update, [zauth, fields, cas])
		self.assertTrue(ret, msg=result)	
	
	def test_meta_update_invalid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		fields["cash"] = 200
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_update, [zauth, fields, cas])
		self.assertTrue(ret, msg=result)
	
	def test_meta_update_expired_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		fields["cash"] = 200
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_update, [zauth, fields, cas])
		self.assertTrue(ret, msg=result)

	def test_meta_update_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_update, [zauth, fields, cas])
		self.assertTrue(ret, msg=result)

	def test_meta_update_without_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		zauth = ' '
		ret, result = check.check_fail(meta_user_update,  [zauth, fields, cas])
		self.assertTrue(ret, msg=result)

	def test_meta_update_admin_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret,result = check.check_pass(meta_user_get, [zauth])
		self.assertTrue(ret, msg=result)
		cas = result['result']['cas']
		fields = result['result']['data']
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_update, [zauth, fields, cas])
		self.assertTrue(ret, msg=result)


	# CREDIBILITY GET


	def test_meta_credibility_get_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_get_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_get_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_get_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
	
	def test_meta_credibility_get_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_get_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(meta_user_credibility_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
	
	#CREDIBILITY SET

	def test_meta_credibility_set_trusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		credibility =  { Constants.ZID: "1" }
		ret, result = check.check_pass(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)	

	def test_meta_credibility_set_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		credibility =  { self.ZID: "1", self.ZID+1: 2 }
		ret, result = check.check_fail(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)

	def test_meta_credibility_set_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		credibility =  { self.ZID: "1", self.ZID+1: 2 }
		ret, result = check.check_fail(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)

	def test_meta_credibility_set_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, 0)
		time.sleep(2)
		credibility =  { self.ZID: "1", self.ZID+1: 2 }
		ret, result = check.check_fail(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)

	def test_meta_credibility_set_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		credibility =  { self.ZID: "1", self.ZID+1: 2 }
		ret, result = check.check_fail(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)

	def test_meta_credibility_set_empty_token(self):
		zauth = ' '
		credibility =  { self.ZID: "1", self.ZID+1: 2 }
		ret, result = check.check_fail(meta_user_credibility_set, [zauth, credibility])
		self.assertTrue(ret, result)
	
	# CREDIBILITY UPGRADE
	
	def test_meta_credibility_upgrade_trusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
	

	def test_meta_credibility_upgrade_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_upgrade_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_upgrade_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, 0)
		time.sleep(2)
		ret, result = check.check_fail(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_upgrade_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_upgrade_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(meta_user_credibility_upgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	# CREDIBILITY DOWNGRADE

	def test_meta_credibility_downgrade_trusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_downgrade_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_downgrade_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_downgrade_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, 0)
		time.sleep(2)
		ret, result = check.check_fail(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_downgrade_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_credibility_downgrade_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(meta_user_credibility_downgrade, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	# TRIO GET
	
	def test_meta_trio_get_trusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_trio_get_untrusted_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_trio_get_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_trio_get_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID, 0)
		time.sleep(2)
		ret, result = check.check_fail(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_trio_get_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	def test_meta_trio_get_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)

	# BULK UPDATE

	def test_meta_user_bulk_update_trusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
		fields = result['result']['data']
		for key, value in fields.items():
			fields[key] = value['current']

		ret, result = check.check_pass(meta_user_bulk_update, [zauth, Constants.META_TYPE_CURRENT, fields])
		self.assertTrue(ret, result)

	def test_meta_user_bulk_update_untrusted_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
		fields = result['result']['data']
		for key, value in fields.items():
			fields[key] = value['current']
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_bulk_update, [zauth, Constants.META_TYPE_CURRENT, fields])
		self.assertTrue(ret, result)

	def test_meta_user_bulk_update_readonly_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
		self.assertTrue(ret, result)
		fields = result['result']['data']
		for key, value in fields.items():
			fields[key] = value['current']
		
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_fail(meta_user_bulk_update, [zauth, Constants.META_TYPE_CURRENT, fields])
		self.assertTrue(ret, result)


	def test_meta_user_bulk_update_expired_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
        	ret, result = check.check_pass(meta_user_trio_get, [zauth, [self.ZID,self.ZID+1]])
        	self.assertTrue(ret, result)
		fields = result['result']['data']
 	        for key, value in fields.items():
               		fields[key] = value['current']

		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID,0)
		time.sleep(2)
		ret, result = check.check_fail(meta_user_bulk_update, [zauth, Constants.META_TYPE_CURRENT, fields])
		self.assertTrue(ret, result)
		
		
if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(mqs_auth)
	unittest.TextTestRunner(verbosity=99).run(suite0)

	
