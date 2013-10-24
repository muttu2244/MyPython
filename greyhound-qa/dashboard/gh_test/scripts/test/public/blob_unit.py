#!/usr/bin/python26
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from acl import ACL
from  unit_class import *
import sys
import random
from config import ConfigService

class blob_unit(gh_unit):
	"""/*****************************************************************************************
                                user.blob.get TCs
        ********************************************************************************************"""

	def test_user_blob_get_new_user(self):
                zauth = AuthSystem.getUntrustedToken(Constants.NZID )
                ret, result = self.check_pass(user_blob_get, [ zauth ], [404])
		self.assertTrue(ret, msg = result)

        def test_user_blob_get_normal_user(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result =user_blob_get( zauth )
                ret, result = self.check_pass(user_blob_get, [ zauth],[0])
		self.assertTrue(ret, msg = result)

	def test_user_blob_get_expired_token(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret,result = self.check_pass(user_blob_get, [ zauth],[403])
		self.assertTrue(ret, msg = result)

        
	def test_user_blob_get_invalid_blob(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass(user_blob_get_invalid, [ zauth, Constants.INVALID_BLOB],[403])
		self.assertTrue(ret, msg = result)                


        def test_user_blob_get_empty_zauth(self):
                zauth=None
                ret,result = self.check_pass(user_blob_get, [ zauth],[403])
		self.assertTrue(ret, msg = result)

        def test_user_blob_get_no_zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass(user_blob_get_no_Zauth_head, [Constants.USER_BLOB],[403])
                self.assertTrue(ret, msg = result) 

	

        """/*****************************************************************************************
                                user.blob.set  TCs
        ********************************************************************************************"""
	
	

        def test_user_blob_set_normal_functionality(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get(zauth)		
		if "'CAS': None" in str(result):
			cas=" "
		else:
                	cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
		self.assertTrue(ret, msg = result)		


        
	def test_user_blob_set_empty_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth= None
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[403])
		self.assertTrue(ret, msg = result)

        def test_user_blob_set_expired_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[403])
		self.assertTrue(ret, msg = result)
	
        def test_user_blob_set_invalid_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                cas_invalid= cas + 1
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas_invalid ],[409])
		self.assertTrue(ret, msg = result)

	
        def test_user_blob_set_miss_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                #result = user_blob_get( zauth )
               # cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                cas_miss=' '
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas_miss ],[409])
                self.assertTrue(ret, msg = result)

        def test_user_blob_set_size_less_than_maxsize_defined_for_blobtype(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(1)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                self.assertTrue(ret, msg = result)


	def test_user_blob_set_size_greater_than_limit(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                limit = ConfigService.getBlobLimits(Constants.USER_BLOB)
		data = data_to_post(limit['maxsize']+10)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[413])
                self.assertTrue(ret, msg = result)


        def test_user_blob_set_no_Zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
		ret, result = self.check_pass(user_blob_set_no_Zauth_head, [ Constants.USER_BLOB, data, cas ],[403])
                self.assertTrue(ret, msg = result)

	def test_user_blob_set_empty_data(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
			cas=" "
		else:
			cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		data = None
		ret, result = self.check_pass(user_blob_set_empty, [ zauth, Constants.USER_BLOB, data, cas ],[400])
		self.assertTrue(ret, msg = result)
                

	

        """/*****************************************************************************************
				freind.blob.get TCs
        ********************************************************************************************"""


	def test_friend_blob_get(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		ACL_arr=ACL.getGraphTypes('friend.blob.get', Constants.USER_BLOB)
		for element in ACL_arr:
			if (element == 'any'):
				ret , result = self.check_pass(friend_blob_get , [ zauth ,Constants.ZID, Constants.USER_BLOB],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret , result = self.check_pass(friend_blob_get , [ zauth ,Constants.ZID, Constants.USER_BLOB],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret , result = self.check_pass(friend_blob_get , [ zauth ,Constants.ZID, Constants.USER_BLOB],[403])
				self.assertTrue(ret, msg = result)
			else:
				"In this case it is a graphlist"
				ret =   get_friend_nofriend_id(zauth, element )
   			        fid_list=ret['result']['data'][element]
                	        fid = random.choice(fid_list)
      		                """If  friend blob is empty, update some value and then fetch the blob, through friend.blob.get api"""
	                        fzauth=AuthSystem.getUntrustedToken(fid)
                                result = user_blob_get( fzauth )
          		        if "'CAS': None" in str(result):
                      		  	cas= " "
                       			data = data_to_post()
                     			result = user_blob_set( fzauth, Constants.USER_BLOB, data, cas)
        		        else:
                       			cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
				"""Checking for friend"""
				ret , result = self.check_pass(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB],[0])
				self.assertTrue(ret, msg = result)
				"""cheking for non-friend"""	
				nfid=nfzid(zauth)	
 				ret , result = self.check_pass(friend_blob_get , [ zauth ,nfid, Constants.USER_BLOB],[403])	
				self.assertTrue(ret, msg = result)
		


        def test_friend_blob_get_expired_Token(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)

		ACL_arr=ACL.getGraphTypes('friend.blob.get', Constants.USER_BLOB)
                for element in ACL_arr:
                        if (element == 'any') or (element == 'self') or (element == 'none'):
                                ret , result = self.check_pass(friend_blob_get , [ zauth ,Constants.ZID, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                        else:
                                "In this case it is a graphlist"
                                ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID), element )
                                fid_list = ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                """If  friend blob is empty, update some value and then fetch the blob, through friend.blob.get api"""
                                fzauth=AuthSystem.getUntrustedToken(fid)
                                result = user_blob_get( fzauth )
                                if "'CAS': None" in str(result):
                                        cas= " "
                                        data = data_to_post()
                                        result = user_blob_set( fzauth, Constants.USER_BLOB, data, cas)
                                else:
                                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                                """Checking for friend"""
                                ret , result = self.check_pass(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                                """cheking for non-friend"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_get , [ zauth ,nfid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)


	
        def test_friend_blob_get_empty_Zauth_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		
		ACL_arr=ACL.getGraphTypes('friend.blob.get', Constants.USER_BLOB)
                for element in ACL_arr:
                        if (element == 'any') or (element == 'self') or (element == 'none'):
                                ret , result = self.check_pass(friend_blob_get , [ None, Constants.ZID, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                        else:
                                "In this case it is a graphlist"
                                ret =   get_friend_nofriend_id(AuthSystem.getUntrustedToken(Constants.ZID), element )
                                fid_list = ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                """If  friend blob is empty, update some value and then fetch the blob, through friend.blob.get api"""
                                fzauth=AuthSystem.getUntrustedToken(fid)
                                result = user_blob_get( fzauth )
                                if "'CAS': None" in str(result):
                                        cas= " "
                                        data = data_to_post()
                                        result = user_blob_set( fzauth, Constants.USER_BLOB, data, cas)
                                else:
                                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                                """Checking for friend"""
                                ret , result = self.check_pass(friend_blob_get , [ None, fid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                                """cheking for non-friend"""
                                nfid=nfzid(AuthSystem.getUntrustedToken(Constants.ZID))
                                ret , result = self.check_pass(friend_blob_get , [ None, nfid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)


        def test_friend_blob_get_no_zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)

		ACL_arr=ACL.getGraphTypes('friend.blob.get', Constants.USER_BLOB)
                for element in ACL_arr:
                        if (element == 'any') or (element == 'self') or (element == 'none'):
                                ret , result = self.check_pass(friend_blob_get_no_Zauth_head , [ Constants.ZID, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                        else:
                                "In this case it is a graphlist"
                                ret =   get_friend_nofriend_id(zauth, element )
                                fid_list = ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                """If  friend blob is empty, update some value and then fetch the blob, through friend.blob.get api"""
                                fzauth=AuthSystem.getUntrustedToken(fid)
                                result = user_blob_get( fzauth )
                                if "'CAS': None" in str(result):
                                        cas= " "
                                        data = data_to_post()
                                        result = user_blob_set( fzauth, Constants.USER_BLOB, data, cas)
                                else:
                                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                                """Checking for friend"""
                                ret , result = self.check_pass(friend_blob_get_no_Zauth_head , [ fid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)
                                """cheking for non-friend"""
                                nfid=nfzid(zauth)
                                ret , result = self.check_pass(friend_blob_get_no_Zauth_head , [ nfid, Constants.USER_BLOB],[403])
                                self.assertTrue(ret, msg = result)









if __name__ == '__main__':
	#suite0 = unittest.TestLoader().loadTestsFromTestCase(blob_unit)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/blob_unit.html')

