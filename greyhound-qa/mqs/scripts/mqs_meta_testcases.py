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
from mqs_apis import *
from mqs_check import mqs_check as check
class mqs_meta_testcases(unittest.TestCase):
	ZID = Constants.ZID
	def setUp(self):
		return
		
	#
	# TestCases for the MQS meta APIs with different types of Auth Token
	#
	# META_USER_GET API..
	
	def test_meta_get_normal_functionality(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_get, [zid])
			self.assertTrue(ret, result)
			zid += 1


	def test_meta_user_aupdate_normal_functionality(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_get, [zid])
			self.assertTrue(ret, result)
			cas = result['result']['cas']
			fields = result['result']['data']
			fields['xp'] += 1
			ret, result = check.check_pass(meta_user_update, [zid, fields, cas])
			self.assertTrue(ret, result)

		print fields
	def test_meta_user_update_invalid_cas(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_get, [zid])
			self.assertTrue(ret, result)
			cas = result['result']['cas']
			fields = result['result']['data']
			ret, result = check.check_pass(meta_user_update, [zid, fields, cas])
			self.assertTrue(ret, result)
			ret, result = check.check_fail(meta_user_update, [zid, fields, cas])
			self.assertTrue(ret, result)
			zid += 1

	def test_meta_user_update_without_cas(self):
		zid = self.ZID
		for i in range(10):
			ret,result = check.check_pass(meta_user_get, [zid])
			self.assertTrue(ret, result)
			cas = ' '
			fields = result['result']['data']
			ret, result = check.check_fail(meta_user_update, [zid, fields, cas])
			zid += 1

	def test_meta_user_update_without_postfields(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_get, [zid])
			self.assertTrue(ret, result)
			cas = result['result']['cas']
			fields = ' '
			ret, result = check.check_fail(meta_user_update, [zid, fields, cas])
			zid += 1

	# credibility apis

	def test_meta_user_credibility_get(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_credibility_get, [zid, [zid,zid+1]])
			print result
			self.assertTrue(ret, result)
			zid+=2

	
	def test_meta_user_credibility_get_without_input(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_fail(meta_user_credibility_get, [zid, [ ]])
			self.assertTrue(ret, result)
			zid+=1

	def test_meta_user_credibility_set(self):
		zid = self.ZID
		for i in range(10):
			credibility = {zid: "1",zid+1: "2"} 
			ret, result = check.check_pass(meta_user_credibility_set, [zid, credibility ])
			self.assertTrue(ret, result)
			zid+=2

	def test_meta_user_credibility_upgrade(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_credibility_upgrade, [zid, [zid,zid+1]])
			self.assertTrue(ret, result)
			zid+=2

	def test_meta_user_credibility_downgrade(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_credibility_downgrade, [zid, [zid,zid+1]])
			self.assertTrue(ret, result)
			zid+=2

	def test_meta_user_trio_get(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_trio_get, [zid, [zid,zid+1]])
			self.assertTrue(ret, result)
			zid+=2

	def test_meta_user_bulk_update(self):
		zid = self.ZID
		for i in range(10):
			ret, result = check.check_pass(meta_user_trio_get, [zid, [zid,zid+1]])
			self.assertTrue(ret, result)
			fields = result['result']['data']
			for key, value in fields.items():
				fields[key] = value['current']
			ret, result = check.check_pass(meta_user_bulk_update, [zid, Constants.META_TYPE_CURRENT, fields])
			self.assertTrue(ret, result)
			zid += 2



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(mqs_meta_testcases)
	unittest.TextTestRunner(verbosity=99).run(suite0)

	
