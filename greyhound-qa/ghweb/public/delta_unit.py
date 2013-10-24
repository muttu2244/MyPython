#!/usr/bin/python26
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from  unit_class import *
import sys
import random

class delta_unit(gh_unit):

        """/*****************************************************************************************
                                user.blob.addDelta  TCs
        ********************************************************************************************"""

	"""For all valid addDelta Tcs , it is adviced to delte the existing ones,
	to ensure that delta count has not exceeded max limit, else u will get 413 errors.
	Hence calling delete_prev_deltas function"""
	def test_friend_blob_addDelta(self):
        	zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                delta = "sample delta value"
		res=delete_prev_deltas(fid)
                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] ,[0])
		self.assertTrue(ret, msg='Failed to send API request')

	def test_friend_blob_addDelta_nonfriend(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =  get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
		nfid=nfzid(zauth)
                delta = "sample delta value"
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , nfid, Constants.DELTATYPE , delta ],[0,403] )
		self.assertTrue(ret, msg='Failed to send API request')


	def  test_friend_blob_addDelta_invalid_delta(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                delta = "sample delta value"
		#delete_prev_deltas(fid)
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid, Constants.INVALID_DELTA, delta ],[403])
		self.assertTrue(ret, msg='Failed to send API request')

	def test_friend_blob_addDelta_expired_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                delta = "some dataa"
		delete_prev_deltas(fid)
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] ,[403])
		
                self.assertTrue(ret, msg='Failed to send API request')



        def test_friend_blob_addDelta_empty_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                delta = "sample delta value"
                zauth=None
		delete_prev_deltas(fid)
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid, Constants.DELTATYPE , delta ] ,[403])
		
                self.assertTrue(ret, msg='Failed to send API request')


	def test_friend_blob_addDelta_Exceed_content_Limit(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
		maxsize,host_ip,file,flag=remote_connect('maxsize','Deltas' ,Constants.DELTATYPE)
		maxsize=maxsize.rstrip('\n')
		delete_prev_deltas(fid)
		delta=delta_max_size(maxsize,Constants.DELTATYPE)
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid, Constants.DELTATYPE , delta ] ,[413])
		
                self.assertTrue(ret, msg='Failed to send API request')


        def test_friend_blob_addDelta_Max_delta_count(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                delta="Some Delta"
		delete_prev_deltas(fid)
		maxcount,host_ip,file,flag=remote_connect('maxcount', 'Deltas', Constants.DELTATYPE)
		maxcount=int(maxcount)
		if 'newest' in flag:
			self.assertFalse(True, msg='Change the value of variable -keep to oldest to run this TC')

                delta_max=delta_max_count(zauth , fid , Constants.DELTATYPE,maxcount,delta)
                ret , result = self.check_fail(friend_blob_addDelta , [ zauth , fid, Constants.DELTATYPE , delta ] ,[413])
		
                self.assertTrue(ret, msg='Failed to send API request')



        """/*****************************************************************************************
                                user.blob.deleteDeltas  TCs
        ********************************************************************************************"""



        def test_user_blob_deleteDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                delta = "sample delta value"
                result=delete_prev_deltas(fid)
                result = friend_blob_addDelta (zauth , fid , Constants.DELTATYPE , delta )
                delta_id = result["id"]
                zauth=AuthSystem.getUntrustedToken(fid)
                ret,result = self.check_pass(user_blob_deleteDeltas , [zauth , delta_id],[0])
		
                self.assertTrue(ret, msg='Failed to send API request')





        def test_user_blob_deleteDeltas_Empty_DeltaID(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                delta_id = []
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , delta_id],['False'])
		
                self.assertTrue(ret, msg='Failed to send API request')


        def test_user_blob_deleteDeltas_Empty_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                delta = "sample delta value"
		result=delete_prev_deltas(fid)
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                delta_id = result['id']
                zauth = None
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , delta_id],[403])
		
                self.assertTrue(ret, msg='Failed to send API request')


        def test_user_blob_deleteDeltas_invalid_DeltaID(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_deleteDeltas , [zauth , Constants.INVALID_DELTAID ],['False'])
		
                self.assertTrue(ret, msg='Failed to send API request')



        """/*****************************************************************************************
                               friend.blob.queryDeltas  api TCs
        ********************************************************************************************"""

   
	def test_friend_blob_queryDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
		"""Add delta and query the same """
		delta = "sample delta value"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , fid , user_query],[0])
		
                self.assertTrue(ret, msg='Failed to send API request')


	
        def test_friend_blob_queryDeltas_nonfriends(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
		nfid=nfzid(zauth)
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , nfid , user_query],[0,403])
                self.assertTrue(ret, msg='Failed to send API request')

	def test_friend_blob_querydelta_Invalid_Query(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
		"""Add delta and query the same """
                delta = "sample delta value"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                user_query = {Constants.USER_QUERY: 123 , "params":[] }
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid,  user_query] ,[403])
		
                self.assertTrue(ret, msg='Failed to send API request')




        def test_friend_blob_queryDeltas_without_query(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
		delta="some delta"
		result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                user_query = None
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid,  user_query],[403] )
		
                self.assertTrue(ret, msg='Failed to send API request')


	def test_friend_blob_queryDelta_expired_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
		delta="some delta"
		result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid , user_query] ,[403])
		
                self.assertTrue(ret, msg='Failed to send API request')




        def test_friend_blob_queryDeltas_empty_token(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                zauth=None
		delta="some delta"
                user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
		result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid,  user_query] ,[403])
		
                self.assertTrue(ret, msg='Failed to send API request')



        def test_friend_blob_queryDeltas_Mixed_case_char(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                user_query = {Constants.USER_QUERY:"select * from DeLTas" , "Parms":[] }
		delta="some delta"
                ret , result = self.check_fail(friend_blob_queryDeltas , [zauth , fid,  user_query],[403] )
		
                self.assertTrue(ret, msg='Failed to send API request')



	
	"""/*****************************************************************************************
				user.blob.query  api TCs
	********************************************************************************************"""

        def test_user_blob_queryDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
		fzauth=AuthSystem.getUntrustedToken(109)
		res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
                ret,result = self.check_pass(user_blob_queryDeltas , [fzauth, user_query],[0])
		
                self.assertTrue(ret, msg='Failed to send API request')



	def test_user_blob_queryDeltas_invalid_query(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                fzauth=AuthSystem.getUntrustedToken(fid)
		res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                user_query = {Constants.USER_QUERY: 123, "params": {"type":Constants.DELTATYPE }}
                ret,result = self.check_pass(user_blob_queryDeltas , [fzauth , user_query],[403])
                
                self.assertTrue(ret, msg='Failed to send API request')

	def test_user_blob_queryDeltas_noquery(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                fzauth=AuthSystem.getUntrustedToken(fid)
                res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
		user_query=None
                ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query],[403])
		
                self.assertTrue(ret, msg='Failed to send API request')

	
	def test_user_blob_queryDeltas_with_Expired_Token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                fzauth=AuthSystem.getUntrustedToken(fid)
                res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
		user_query = {Constants.USER_QUERY:Constants.SELF_QUERY , "params": {"type":Constants.DELTATYPE }}
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query],[403])
		
                self.assertTrue(ret, msg='Failed to send API request')

	def test_user_blob_queryDeltas_empty_token(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                fzauth=AuthSystem.getUntrustedToken(fid)
                res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
		user_query = {Constants.USER_QUERY:Constants.SELF_QUERY , "params": {"type":Constants.DELTATYPE }}
		zauth=None
		ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query],[403])
		
                self.assertTrue(ret, msg='Failed to send API request')


	def test_user_blob_queryDeltas_Mixed_case_char(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                fzauth=AuthSystem.getUntrustedToken(fid)
                res=delete_prev_deltas(fid)
                delta="some delta"
                result =friend_blob_addDelta ( zauth , fid , Constants.DELTATYPE , delta )
                user_query = {Constants.USER_QUERY: "select * from DeLTAs"  , "params": {"type": Constants.DELTATYPE}}
		ret,result = self.check_fail(user_blob_queryDeltas , [zauth , user_query],[403])
		
                self.assertTrue(ret, msg='Failed to send API request')



if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(delta_unit)
        unittest.TextTestRunner(verbosity=99).run(suite0)

