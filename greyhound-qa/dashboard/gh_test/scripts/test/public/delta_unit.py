#!/usr/bin/python26
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from  unit_class import *
import sys
import random
from config import ConfigService
from acl import ACL

class delta_unit(gh_unit):

        """/*****************************************************************************************
                                friend.blob.addDelta  TCs
        ********************************************************************************************"""

	"""For all valid addDelta Tcs , it is adviced to delte the existing ones,
	to ensure that delta count has not exceeded max limit, else u will get 413 errors.
	Hence calling delete_prev_deltas function"""

	def test_friend_blob_addDelta(self):
        	zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.DELTATYPE)
		delta = "sample delta value"
		for element in ACL_arr:
			if (element == 'any'):
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[0])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[0])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)
			else:
				"""graph-list """
				ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID),element)
				fid_list=ret['result']['data'][element]
				fid = random.choice(fid_list)
				res=delete_prev_deltas(fid)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] ,[0])
				self.assertTrue(ret, msg=result)
			
				"""check for failure when non friend tries to add delta"""
				nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , nfid , Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)	
	

	def  test_friend_blob_addDelta_invalid_delta_type(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.INVALID_DELTA)
		delta = "sample delta value"
		for element in ACL_arr:
			if (element == 'any'):
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID+1, Constants.INVALID_DELTA, delta ] ,[413])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.INVALID_DELTA, delta ] ,[413])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.INVALID_DELTA, delta ] ,[403])
				self.assertTrue(ret, msg=result)
		
			else:
				ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID),element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                res=delete_prev_deltas(fid)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.INVALID_DELTA, delta ] ,[413])
				self.assertTrue(ret, msg=result)
				
				"""for non-friend, 403 should be returned as err code"""
				nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , nfid , Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)

	def test_friend_blob_addDelta_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		delta = "sample delta value"
		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.DELTATYPE)
		for element in ACL_arr:
			if (element == 'any'):
				delete_prev_deltas(Constants.ZID)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID+1,Constants.DELTATYPE,delta ] ,[403])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				delete_prev_deltas(Constants.ZID)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.DELTATYPE,delta ] ,[403])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				delete_prev_deltas(Constants.ZID)
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.DELTATYPE,delta ] ,[403])	
				self.assertTrue(ret, msg=result)
			else:
				delete_prev_deltas(Constants.ZID)
				ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID),element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                res=delete_prev_deltas(fid)
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.DELTATYPE,delta ] ,[403])
				self.assertTrue(ret, msg=result)

                                """for non-friend, 403 should be returned as err code"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , nfid , Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)


        def test_friend_blob_addDelta_empty_token(self):
             	zauth=None 
                delta = "sample delta value"
		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.DELTATYPE)
                for element in ACL_arr:
                        if (element == 'any'):
                                delete_prev_deltas(Constants.ZID)
				ret,result = self.check_pass(friend_blob_addDelta , [ zauth ,Constants.ZID+1,Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				delete_prev_deltas(Constants.ZID)
                                ret,result = self.check_pass(friend_blob_addDelta , [ zauth ,Constants.ZID,Constants.DELTATYPE , delta ] ,[403])	
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				delete_prev_deltas(Constants.ZID)
				ret,result = self.check_pass(friend_blob_addDelta , [ zauth ,Constants.ZID,Constants.DELTATYPE , delta ] ,[403]) 
				self.assertTrue(ret, msg=result)
			else:
				delete_prev_deltas(Constants.ZID)
				ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID),element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                res=delete_prev_deltas(fid)
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID,Constants.DELTATYPE,delta ] ,[403])
				self.assertTrue(ret, msg=result)
                                """for non-friend, 403 should be returned as err code"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , nfid , Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)


	def test_friend_blob_addDelta_Exceed_content_Limit(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		limit=ConfigService.getDeltaLimits(Constants.DELTATYPE)
		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.DELTATYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				#delete_prev_deltas(fid)
				delete_prev_deltas(Constants.ZID)
				delta=delta_max_size(limit['maxsize']+1024,Constants.DELTATYPE)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[413])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				delete_prev_deltas(Constants.ZID)
				delta=delta_max_size(limit['maxsize']+1024,Constants.DELTATYPE)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[413])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				delete_prev_deltas(Constants.ZID)
                                delta=delta_max_size(limit['maxsize']+1024,Constants.DELTATYPE)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID, Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)
			else:
				"""This is graph-list """
				delete_prev_deltas(Constants.ZID)
				ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID), element )
				fid_list=ret['result']['data'][element]
				fid = random.choice(fid_list)
				delta=delta_max_size(limit['maxsize']+1024,Constants.DELTATYPE)
                                ret , result = self.check_pass(friend_blob_addDelta , [ zauth , fid , Constants.DELTATYPE , delta ] ,[413]) 
				self.assertTrue(ret, msg=result)	
				"""for non-friends"""
				delete_prev_deltas(Constants.ZID)
				nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                delta=delta_max_size(limit['maxsize']+1024,Constants.DELTATYPE)
				ret , result = self.check_pass(friend_blob_addDelta , [ zauth , nfid, Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)
				
				
        def test_friend_blob_addDelta_Max_delta_count(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		delta="some delta"
		limit=ConfigService.getDeltaLimits(Constants.DELTATYPE)
		maxcount=limit['maxcount']
		keep=limit['keep']
		if (keep is False):
	                self.assertTrue(False,msg="Check for keep variable in storage.yaml file for the delta type") 
		

		ACL_arr=ACL.getGraphTypes('friend.blob.addDelta',Constants.DELTATYPE)
		for element in ACL_arr:
		  if (element == 'any'):
			delete_prev_deltas(Constants.ZID)
			delta_max=delta_max_count(zauth , Constants.ZID+1 , Constants.DELTATYPE,maxcount,delta)
			ret , result = self.check_pass(friend_blob_addDelta , [ zauth , Constants.ZID+1, Constants.DELTATYPE , delta ] ,[413])
			self.assertTrue(ret, msg=result)
		  elif (element == 'self'):
			delete_prev_deltas(Constants.ZID)
			delta_max=delta_max_count(zauth , Constants.ZID , Constants.DELTATYPE,maxcount,delta)
                        ret , result = self.check_pass(friend_blob_addDelta , [ zauth ,Constants.ZID , Constants.DELTATYPE , delta ] ,[413])
			self.assertTrue(ret, msg=result)
		  elif (element == 'none'):
			delete_prev_deltas(Constants.ZID)
			delta_max=delta_max_count(zauth ,Constants.ZID , Constants.DELTATYPE,maxcount,delta)
			ret , result = self.check_pass(friend_blob_addDelta , [ zauth ,Constants.ZID,Constants.DELTATYPE , delta ] ,[403])
			self.assertTrue(ret, msg=result)
		  else:
			"""This is graph-list """
                        delete_prev_deltas(Constants.ZID)
			ret =   get_friend_nofriend_id(zauth, element )
                        fid_list=ret['result']['data'][element]
                        fid = random.choice(fid_list)
			delta_max=delta_max_count(zauth , fid , Constants.DELTATYPE,maxcount,delta)
                        ret , result = self.check_pass(friend_blob_addDelta , [ zauth ,fid, Constants.DELTATYPE , delta ] ,[413])
			self.assertTrue(ret, msg=result)

                        """for non-friends"""
                        delete_prev_deltas(Constants.ZID)
			nfid=nfzid(zauth)
			delta_max=delta_max_count(zauth , fid , Constants.DELTATYPE,maxcount,delta)
                        ret , result = self.check_pass(friend_blob_addDelta , [ zauth ,nfid, Constants.DELTATYPE , delta ] ,[403])
			self.assertTrue(ret, msg=result)




        """/*****************************************************************************************
                                user.blob.deleteDeltas  TCs
        ********************************************************************************************"""



        def test_user_blob_deleteDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                delta_id = "sample:delta"
                ret,result = self.check_pass(user_blob_deleteDeltas , [zauth , delta_id],[0])
		self.assertTrue(ret, msg=result)
		
        def test_user_blob_deleteDeltas_nodeltaid(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                delta_id = ""
                ret,result = self.check_pass(user_blob_deleteDeltas , [zauth , delta_id],[404])
                self.assertTrue(ret, msg=result)
	 
        def test_user_blob_deleteDeltas_invalid_DeltaID(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass(user_blob_deleteDeltas , [zauth , Constants.INVALID_DELTAID ],[0])
		self.assertTrue(ret, msg=result)
                



        """/*****************************************************************************************
                               friend.blob.queryDeltas  api TCs
        ********************************************************************************************"""

   
	def test_friend_blob_queryDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
		ACL_arr=ACL.getGraphTypes('friend.blob.queryDeltas',Constants.DELTATYPE)
		delta="some delta"
                for element in ACL_arr:
       			if (element == 'any'):
				self.test_friend_blob_addDelta()
				#friend_blob_addDelta(zauth,Constants.ZID+1, Constants.DELTATYPE, delta)
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , Constants.ZID+1, user_query],[0])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				self.test_friend_blob_addDelta()
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query],[0])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query],[403])
				self.assertTrue(ret, msg=result)
			else:
				"""This is graph-list """
				ret =   get_friend_nofriend_id(zauth, element )
				fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
				self.test_friend_blob_addDelta()
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,fid, user_query],[0])
				self.assertTrue(ret, msg=result)

	                        """for non-friends"""
				nfid=nfzid(zauth)
                        	ret , result = self.check_pass(friend_blob_addDelta , [ zauth ,nfid, Constants.DELTATYPE , delta ] ,[403])
				self.assertTrue(ret, msg=result)
		
                




	def test_friend_blob_querydelta_Invalid_Query(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: 123, "params": {"type":Constants.DELTATYPE }}
		delta="some delta"
                ACL_arr=ACL.getGraphTypes('friend.blob.queryDeltas',Constants.DELTATYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				self.test_friend_blob_addDelta()
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , Constants.ZID+1,user_query] ,[403,404])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				self.test_friend_blob_addDelta()
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403,404])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403])
				self.assertTrue(ret, msg=result)
			else:
				"""graph-list"""
				ret =   get_friend_nofriend_id(zauth, element )
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
				self.test_friend_blob_addDelta()
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,fid,user_query] ,[403,404])
				self.assertTrue(ret, msg=result)
				"""for non-friends"""
				nfid=nfzid(zauth)
				ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,nfid,user_query] ,[403])
				self.assertTrue(ret, msg=result)



	def test_friend_blob_queryDelta_expired_token(self):
		zauth = AuthSystem.getExpiredToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
                ACL_arr=ACL.getGraphTypes('friend.blob.queryDeltas',Constants.DELTATYPE)
		delta="some delta"
                for element in ACL_arr:
			if (element == 'any'):
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , Constants.ZID+1,user_query] ,[403])
				self.assertTrue(ret, msg=result)
			elif (element == 'self'):
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403])
				self.assertTrue(ret, msg=result)
                        elif (element == 'none'):
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403])
				self.assertTrue(ret, msg=result)
			else:
				"""graph-list"""
                                ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID), element )
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,fid,user_query] ,[403])
				self.assertTrue(ret, msg=result)
                                """for non-friends"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,nfid,user_query] ,[403])
				self.assertTrue(ret, msg=result)





        def test_friend_blob_queryDeltas_empty_token(self):
                zauth=None
		user_query = {Constants.USER_QUERY: Constants.F_QUERY, "params":[] }
		ACL_arr=ACL.getGraphTypes('friend.blob.queryDeltas',Constants.DELTATYPE)
		delta="some delta"
                for element in ACL_arr:
                        if (element == 'any'):
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth , Constants.ZID+1,user_query] ,[403])
				self.assertTrue(ret, msg=result)
                        elif (element == 'self'):
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403])
				self.assertTrue(ret, msg=result)
                        elif (element == 'none'):
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,Constants.ZID, user_query] ,[403])
				self.assertTrue(ret, msg=result)
                        else:
                                """graph-list"""
                                ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID), element )
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
				self.test_friend_blob_addDelta()
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,fid,user_query] ,[403])
				self.assertTrue(ret, msg=result)
                                """for non-friends"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_queryDeltas , [zauth ,nfid,user_query] ,[403])
				self.assertTrue(ret, msg=result)




	
	"""/*****************************************************************************************
				user.blob.query  api TCs
	********************************************************************************************"""

        def test_user_blob_queryDeltas_functional(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: Constants.SELF_QUERY , "params": {"type": Constants.DELTATYPE}}
		ACL_arr = ACL.getGraphTypes('user.blob.queryDeltas',Constants.DELTATYPE)
		for element in ACL_arr:
			if (element == 'any' or element == 'self'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[0])
				self.assertTrue(ret, msg=result)
			elif (element == 'none'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[403])
				self.assertTrue(ret, msg=result)
			else:
				self.fail(msg="invalid ACL rule for the api")
	

	def test_user_blob_queryDeltas_invalid_query(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: 123, "params": {"type":Constants.DELTATYPE }}
		
		ACL_arr = ACL.getGraphTypes('user.blob.queryDeltas',Constants.DELTATYPE)
		for element in ACL_arr:
			if (element == 'any' or element == 'self'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[403])
				self.assertTrue(ret, msg=result)
			elif(element == 'none'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[403])
				self.assertTrue(ret, msg=result)
			else:
				self.fail(msg="invalid ACL rule for the api")



	def test_user_blob_queryDeltas_noquery(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query=None
		ACL_arr = ACL.getGraphTypes('user.blob.queryDeltas',Constants.DELTATYPE)
		for element in ACL_arr:
			if (element == 'any' or element == 'self' or element == 'none'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[403])
				self.assertTrue(ret, msg=result)
			else:
				self.fail(msg="invalid ACL rule for the api")

	


	def test_user_blob_queryDeltas_Mixed_case_char(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		user_query = {Constants.USER_QUERY: "select * from DeLTAs"  , "params": {"type": Constants.DELTATYPE}}
		ACL_arr = ACL.getGraphTypes('user.blob.queryDeltas',Constants.DELTATYPE)
		for element in ACL_arr:
			if (element == 'any' or element == 'self' or element == 'none'):
				ret,result = self.check_pass(user_blob_queryDeltas , [zauth , user_query],[403])
				self.assertTrue(ret, msg=result)
			else:
				self.fail(msg="invalid ACL rule for the api")
		
                


	






if __name__ == '__main__':
	#suite0 = unittest.TestLoader().loadTestsFromTestCase(delta_unit)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/delta.html')

