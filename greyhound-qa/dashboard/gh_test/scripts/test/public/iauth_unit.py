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
import simplejson as json
from iauth_api import *
from auth import *
# vim: ai ts=4 sts=4 et sw=4 ft=python

class iauth_unit(unittest.TestCase):  
        """ TODO : 
     	        * setUp() - will set test env
	        * tearDown() - will clean up test env
        """
	def setUp(self):
                return
		
        def validate_in_list(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val in tmp:
		        return True
		val = 1
		self.assertEqual(val, 2,msg='val is not in list')
	        return False

        def validate_not_in_list(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val not in tmp:
		        return True
		val = 1
		self.assertEqual(val, 2, msg='val is in list')
	        return False

        def validate_obj_val(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val == tmp:
		        return True

	        print "Value ", tmp, " is not same as expected value ", val, " in obj path ", list_path, " in data ", data
	        return False

        def run_validation_fn(self, validation_fn_list, data):
	        for fn in validation_fn_list:
		        if len(fn) == 1:
			        ret = fn[0](ret)
		        elif len(fn) == 2:
			        ret = fn[0](fn[1], data)
		        elif len(fn) == 3:
			        ret = fn[0](fn[1], fn[2], data)
		        elif len(fn) == 4:
			        ret = fn[0](fn[1], fn[2], fn[3], data)
		        else:
			        raise Exception("No validator defined")
		        if not ret:
			        return ret
	        return True

        def check_pass(self, fun, args, validation_fn_list = None):
	        ret = fun(*args)
	        if not ret:
			set_ret = 1
		        self.assertEqual(set_ret, 1, msg = ret)
            		return [ False, ret ]
		if Constants.BLOBS not in ret:
			if ret[ Constants.GH_ERROR ] == 403:
				if not ret[ Constants.GH_ERROR_MESSAGE ]:
					self.assertEqual(ret[ Constants.GH_ERROR ], 403, msg = 'Error in delta adding')
				else:
					self.assertEqual(ret[ Constants.GH_ERROR ], 403, msg = ret[ Constants.GH_ERROR_MESSAGE ])
				return [ False, ret ]
			if ret[ Constants.GH_ERROR ] == 409:
				self.assertEqual(ret[ Constants.GH_ERROR ], 409, msg = ret[ Constants.GH_CAS ])	
				return [ False, ret ]
			if ret[ Constants.GH_ERROR ] == 0:
				return [True , ret ]
		elif ret[ Constants.BLOBS ] == []:
			""" temp fix for istorage bug
			 (SEG-5787) [iStorage] user.blob.get should return error code 500 when memcached service is down
			"""
			set_ret = 2
			self.assertEqual( set_ret, 1, msg = ret[ Constants.BLOBS ])
			return [ False, ret ] 
		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 404:  
                        self.assertEqual(ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ], 404, msg = ret[ Constants.BLOBS ])
                        return [ False, ret ]
		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 500:  
                        self.assertEqual(ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ], 404, msg = ret[ Constants.BLOBS ])
			return [ False, ret ]
		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 0:
                        return [ True, ret ]
		else:
			val = 2
			self.assertTrue(val, 1, msg = "API filed due to unknow reason %s" %(ret))
			return [ False, ret ]
        def check_fail(self, fun, args):
	        ret = fun(*args)
	        if not ret:
			set_ret = 1
		        self.assertEqual(set_ret, 1, msg= ret)
	   	        return [ False, ret ]
	
		if Constants.BLOBS not in ret:
			if ret[ Constants.GH_ERROR ] == 403:
				if Constants.GH_ERROR_MESSAGE not in ret:
                                        self.assertEqual(ret[ Constants.GH_ERROR ], 403, msg = 'Error in delta adding')
					return [ False, ret ]
                                else:
                                        self.assertEqual(ret[ Constants.GH_ERROR ], 403, msg = ret[ Constants.GH_ERROR_MESSAGE ])
                                	return [ False, ret ]

			if ret[ Constants.GH_ERROR ] == 409:
				self.assertEqual(ret[ Constants.GH_ERROR ], 409, msg = ret[ Constants.GH_CAS ])	
				return [ True, ret ]
		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 404:  
                        self.assertEqual(ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ], 404, msg = ret[ Constants.BLOBS ])
			return [ True, ret ]

		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 500:  
                        self.assertEqual(ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ], 404, msg = ret[ Constants.BLOBS ])
			return [ True, ret ]
	       
		elif ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ] == 413:  
                        self.assertEqual(ret[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_ERROR ], 404, msg = ret[ Constants.BLOBS ])
			return [ True, ret ]
		 
	        else:
			self.assertFalse(ret, msg= ret[ Constants.BLOBS ])
		        return [ False, ret ]




	"""
	/---------   All TestCases for valid Auth Token -------------\  """


	def test_user_blob_get_valid_auth(self):
        	zauth = AuthSystem.getUntrustedToken(Constants.ZID)
	        ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])
		
		if not ret:
			self.assertFalse(ret, msg = 'Failed to send API request')
		#cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
	        #data = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_BLOB64 ] 
		#v = decode_blob(data)
		#data = data_to_post()
	        #ret , result = self.check_pass(user_blob_set, [ zauth,'game-world',data,cas ])
   
	def test_user_blob_set_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		data = data_to_post()
		if cas == None:
			cas = " "
		ret , result = self.check_pass(user_blob_set, [ zauth,Constants.USER_BLOB, data, cas ])
	def test_friend_blob_get_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		fid = Constants.ZID + 1
		ret , result = self.check_pass(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB])
		if not ret:
			self.assertFalse(ret, msg = 'Failed to send API request')
		
	def test_friend_blob_addDelta_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		fid = Constants.ZID 
		delta = "some data"
		ret , result = self.check_pass(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] )
		if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
	
	def test_friend_blob_queryDeltas_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		fid = Constants.ZID + 1
		user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] } 
		ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , fid , user_query] )


	def test_user_blob_queryDeltas_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
		ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])


	"""
		/----------    All TestCases For Invalid Auth Token ---------------\
	"""


	def test_user_blob_get_invalid_auth(self):
                zauth = AuthSystem.getInvalidToken(Constants.ZID)
                ret, result = self.check_fail(user_blob_get, [ zauth , Constants.USER_BLOB ])

                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

	def test_user_blob_set_invalid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		data = data_to_post()
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		ret , result = self.check_fail(user_blob_set, [ zauth,Constants.USER_BLOB, data, cas ])
	

	def test_friend_blob_get_invalid_auth(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		fid = Constants.ZID + 1
		ret , result = self.check_fail(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB])
		if not ret:
			self.assertFalse(ret, msg = 'Failed to send API request')
		
	def test_friend_blob_addDelta_invalid_auth(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		fid = Constants.ZID + 1
		delta = "some data"
		ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] )
		if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
	
	def test_friend_blob_queryDeltas_invalid_auth(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		fid = Constants.ZID + 1
		user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] } 
		ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid , user_query] )


	def test_user_blob_queryDeltas_invalid_auth(self):
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
		ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query])



	"""
	/------------ All TestCases For ReadOnly Auth Token -----------\
	"""	




	def test_user_blob_get_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])

                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

        def test_user_blob_set_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth = AuthSystem.getInvalidToken(Constants.ZID)
                ret , result = self.check_fail(user_blob_set, [ zauth,Constants.USER_BLOB, data, cas ])


        def test_friend_blob_get_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                fid = Constants.ZID + 1
                ret , result = self.check_pass(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

	def test_friend_blob_addDelta_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                fid = Constants.ZID + 1
                delta = "some data"
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] )
		if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

        def test_friend_blob_queryDelta_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                fid = Constants.ZID + 1
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , fid , user_query] )


        def test_user_blob_queryDeltas_readonly_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])



	"""
	/--------------   All TestCases For Expired Auth token  -----------------\
	"""


	def test_user_blob_get_expired_auth(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret, result = self.check_fail(user_blob_get, [ zauth , Constants.USER_BLOB ])

                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')


	def test_user_blob_set_expired_auth(self):
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                ret, result = self.check_pass(user_blob_get, [ zauth , Constants.USER_BLOB ])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret , result = self.check_fail(user_blob_set, [ zauth,Constants.USER_BLOB, data, cas ])


        def test_friend_blob_get_expired_auth(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                fid = Constants.ZID + 1
                ret , result = self.check_fail(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB])
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

        def test_friend_blob_addDelta_expired_auth(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                fid = Constants.ZID + 1
                delta = "some data"
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] )
                if not ret:
                        self.assertFalse(ret, msg = 'Failed to send API request')

        def test_friend_blob_queryDelta_expired_auth(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                fid = Constants.ZID + 1
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid , user_query] )


        def test_user_blob_queryDeltas_expired_auth(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query])



	"""
	/------------ TEST CASES FOR USER BLOB DELETE DELTAS API  -----------------\
	"""



	def test_user_blob_deleteDeltas_valid_auth(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])
		delta_id = []
		for item in result['deltas']:
			delta_id.append(item['delta_id'])
		ids = ",".join(delta_id)
		ret,result = self.check_pass(user_blob_deleteDeltas , [zauth , ids])

	def test_user_blob_deleteDeltas_invalid_auth(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])
                delta_id = []
                for item in result['deltas']:
                        delta_id.append(item['delta_id'])
                ids = ",".join(delta_id)
		zauth = AuthSystem.getInvalidToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , ids])

	def test_user_blob_deleteDeltas_readonly_auth(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])
                delta_id = []
                for item in result['deltas']:
                        delta_id.append(item['delta_id'])
                ids = ",".join(delta_id)
                zauth = AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , ids])


	def test_user_blob_deleteDeltas_expired_auth(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query])
                delta_id = []
                for item in result['deltas']:
                        delta_id.append(item['delta_id'])
                ids = ",".join(delta_id)
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , ids])

						
if __name__ == '__main__':
        #suite0 = unittest.TestLoader().loadTestsFromTestCase(iauth_unit)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/iauth.html')

