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
MQS_QUERY = 'select zid,field3,cash where cash>0 order by field10'
class mqs_graph_auth(unittest.TestCase):
	ZID = Constants.ZID
	def setUp(self):
		return
	
	# GRAPH ADD
	def test_graph_add_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_add, [zauth, 'app-friend', [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_add_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret,result = check.check_fail(graph_user_add,  [zauth, 'app-friend', [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)
			
	def test_graph_add_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_add, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_add_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_add, [zauth, 'app-friend', [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_add_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_add, [zauth, 'app-friend', [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_add_without_token(self):
		zauth = ' '
		ret, result = check.check_fail(graph_user_add, [zauth, 'app-friend', [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	# GRAPH REMOVE

	def test_graph_remove_valid_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_remove_invalid_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_remove_expired_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_remove_readonly_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_remove_admin_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_remove_empty_token(self):
		self.test_graph_add_valid_token()
		zauth = ' '
		ret, result = check.check_fail(graph_user_remove, [zauth, 'app-friend',[self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)


	# GRAPH CHECKMEMBERSHIP
	
	def test_graph_checkmembership_valid_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)	

	def test_graph_checkmembership_invalid_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_checkmembership_expired_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg=result)

	def test_graph_checkmembership_readonly_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg= result)

	def test_graph_checkmembership_admin_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg= result)

	def test_graph_checkmembership_empty_token(self):
		self.test_graph_add_valid_token()
		zauth = ' '
		ret, result = check.check_fail(graph_user_checkmembership, [zauth, ['app-friend'], [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret, msg= result)

	# GRAPH GET MEMBERS

	def test_graph_getmembers_valid_token(self):
		self.test_graph_add_valid_token()
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getmembers_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getmembers_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getmembers_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getmembers_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getmembers_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(graph_user_getmembers, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	# GRAPH GET CONFIRMLIST

	def test_graph_getconfirmlist_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getconfirmlist_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getconfirmlist_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getconfirmlist_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getconfirmlist_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getconfirmlist_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(graph_user_getconfirmlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	# GRAPH GET WAITLIST

	def test_graph_getwaitlist_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getwaitlist_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getwaitlist_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getwaitlist_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getwaitlist_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	def test_graph_getwaitlist_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(graph_user_getwaitlist, [zauth, ['app-friend']])
		self.assertTrue(ret,result)

	# GRAPH GET GRAPHLIST

	def test_graph_getgraphlist_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	def test_graph_getgraphlist_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	def test_graph_getgraphlist_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	def test_graph_getgraphlist_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	def test_graph_getgraphlist_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	def test_graph_getgraphlist_empty_token(self):
		zauth = ' ' 
		ret, result = check.check_fail(graph_user_getgraphlist, [zauth, [self.ZID+1,self.ZID+2]])
		self.assertTrue(ret,result)

	#QUERY USER GRAPH
	
	def test_graph_queryusergraph_valid_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = check.check_pass(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)

	def test_graph_queryusergraph_invalid_token(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret, result = check.check_fail(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)

	def test_graph_queryusergraph_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret, result = check.check_fail(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)

	def test_graph_queryusergraph_readonly_token(self):
		zauth = AuthSystem.getReadonlyToken(Constants.ZID)
		ret, result = check.check_pass(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)

	def test_graph_queryusergraph_admin_token(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID)
		ret, result = check.check_pass(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)

	def test_graph_queryusergraph_empty_token(self):
		zauth = ' '
		ret, result = check.check_fail(query_user_graph, [zauth, 'app-friend', MQS_QUERY])
		self.assertTrue(ret,result)


if __name__ == '__main__':
	suite1 = unittest.TestLoader().loadTestsFromTestCase(mqs_graph_auth)
	unittest.TextTestRunner(verbosity=99).run(suite1)


