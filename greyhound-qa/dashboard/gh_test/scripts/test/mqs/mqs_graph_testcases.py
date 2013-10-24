#!/usr/bin/python26
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import urllib
import urllib2
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
MQS_QUERY = 'select zid,field0,cash'
class mqs_graph_testcases(unittest.TestCase):
	ZID = Constants.ZID

	def setUp(self):
		return

	# Graph API testcases

	def test_graph_user_add(self):
		zid = self.ZID
		zidlist = [i+zid for i in range(10) ]
		for i in range(10):
			ret, result = check.check_pass(graph_user_add, [zid, 'app-friend', [i for i in zidlist if i != zid]])
			self.assertTrue(ret, result)
			#ret, result = check.check_pass(graph_user_add, [zid+1, 'app-friend', [zid-1,zid+1]])
			#self.assertTrue(ret, result)
			zid+=1

	def test_graph_user_remove(self):
		self.test_graph_user_add()
		zid = self.ZID
		zidlist = [i+zid for i in range(10) ]
		ret, result = check.check_pass(graph_user_remove, [zid, 'app-friend', [i for i in zidlist if i != zid]])
		self.assertTrue(ret, result)

	def test_graph_user_checkmembership(self):
		self.test_graph_user_add()
		zid = self.ZID
		zidlist = [i+zid for i in range(10) ]
		ret, result = check.check_pass(graph_user_checkmembership, [zid, ['app-friend'], [i for i in zidlist if i != zid]])
		print result
		self.assertTrue(ret, result)


	def test_graph_user_getmembers(self):
		self.test_graph_user_add()
		zid = self.ZID
		ret, result = check.check_pass(graph_user_getmembers, [zid, ['app-friend']])
		print result
		self.assertTrue(ret, result)

	def test_graph_user_getconfirmlist(self):
		zid = self.ZID
		self.test_graph_user_remove()
		ret, result = check.check_pass(graph_user_add, [zid, 'app-friend', [zid+1]])
		self.assertTrue(ret, result)
		ret, result = check.check_pass(graph_user_getconfirmlist, [zid+1, ['app-friend']])
		self.assertTrue(ret, result)

	def test_graph_user_getwaitlist(self):
		zid = self.ZID
		self.test_graph_user_remove()
		ret, result = check.check_pass(graph_user_add, [zid, 'app-friend', [zid+1]])
		self.assertTrue(ret, result)
		ret, result = check.check_pass(graph_user_getconfirmlist, [zid, ['app-friend']])
		self.assertTrue(ret, result)

	def test_graph_user_getgraphlist(self):
		zid = self.ZID
		self.test_graph_user_add()
		zidlist = [i+zid for i in range(10) ]
		ret, result = check.check_pass(graph_user_getgraphlist, [zid, [i for i in zidlist if i != zid]])
		print result
		self.assertTrue(ret, result)

	def test_query_user_graph(self):
		self.test_graph_user_add()
		zid = self.ZID
		ret, result = check.check_pass(query_user_graph, [zid, 'app-friend', MQS_QUERY])
		print result
		self.assertTrue(ret, result)

if __name__ == '__main__':
    suite0 = unittest.TestLoader().loadTestsFromTestCase(mqs_graph_testcases)
    unittest.TextTestRunner(verbosity=99).run(suite0)
