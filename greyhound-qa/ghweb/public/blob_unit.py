#!/usr/bin/python26
import os
#import pdb
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from  unit_class import *
import sys
import random

class blob_unit(gh_unit):
	"""/*****************************************************************************************
                                user.blob.get TCs
        ********************************************************************************************"""

	def test_user_blob_get_new_user(self):
                zauth = AuthSystem.getUntrustedToken(Constants.NZID )
                ret, result = self.check_pass(user_blob_get, [ zauth ], [404])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_blob_get_normal_user(self):
		#pdb.set_trace()
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result =user_blob_get( zauth )
                ret, result = self.check_pass(user_blob_get, [ zauth],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')

	def test_user_blob_get_expired_token(self):
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_get, [ zauth],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_blob_get_invalid_blob(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_get_invalid, [ zauth, Constants.INVALID_BLOB],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')                


        def test_user_blob_get_empty_blob(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_get, [ zauth, Constants.EMPTY_BLOB ],[[],403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_blob_get_empty_zauth(self):
                zauth=None
                ret,result = self.check_fail(user_blob_get, [ zauth],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_blob_get_no_zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail(user_blob_get_no_Zauth_head, [Constants.USER_BLOB],[403])
                self.assertTrue(ret, msg = 'Failed to send API request') 

	

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
		self.assertTrue(ret, msg='Failed to send API request')


        def test_user_blob_set_empty_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth= None
                ret, result = self.check_fail(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[403])
		self.assertTrue(ret, msg='Failed to send API request')                

        def test_user_blob_set_expired_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret, result = self.check_fail(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[403])
		self.assertTrue(ret, msg='Failed to send API request')

        def test_user_blob_set_invalid_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                cas_invalid= cas + 1
                ret, result = self.check_fail(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas_invalid ],[409])
		self.assertTrue(ret, msg='Failed to send API request')

        def test_user_blob_set_miss_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                #result = user_blob_get( zauth )
               # cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                cas_miss=' '
                ret, result = self.check_fail(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas_miss ],[409])
                self.assertTrue(ret, msg='Failed to send API request')

        def test_user_blob_set_size_less_than_maxsize_defined_for_blobtype(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(1)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                self.assertTrue(ret, msg='Failed to send API request')

	def test_user_blob_set_size_10K(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(10)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                self.assertTrue(ret, msg='Failed to send API request')

        def test_user_blob_set_size_50K(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(50)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                self.assertTrue(ret, msg='Failed to send API request')

	def test_user_blob_set_100k(self):
		#pdb.set_trace()
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )

		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(100)
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                self.assertTrue(ret, msg='Failed to send API request')

        def test_user_blob_set_500K(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post(500)
                ret, result = self.check_fail(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[413])
                self.assertTrue(ret, msg='Failed to send API request')
        def test_user_blob_set_no_Zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()

                ret, result = self.check_fail(user_blob_set_no_Zauth_head, [ Constants.USER_BLOB, data, cas ],[403])
                
                self.assertTrue(ret, msg='Failed to send API request')


        """/*****************************************************************************************
				freind.blob.get TCs
        ********************************************************************************************"""


	def test_friend_blob_get(self):
		#pdb.set_trace()
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
		"""If  froend blob is empty, update some value and then fetch the blob, through friend.blob.get api"""
		fzauth=AuthSystem.getUntrustedToken(fid)
		result = user_blob_get( fzauth )
                if "'CAS': None" in str(result):
			cas= " "
			data = data_to_post()
	                result = user_blob_set( fzauth, Constants.USER_BLOB, data, cas)
		else:
               		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                ret , result = self.check_pass(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB],[0])
		self.assertTrue(ret, msg='Failed to send API request')


        def test_friend_blob_get_expired_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                zauth = AuthSystem.getExpiredToken(Constants.ZID)
                ret , result = self.check_fail(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB],[403])
		self.assertTrue(ret, msg='Failed to send API request')


        def test_friend_blob_get_empty_Zauth_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                zauth=None 
                ret , result = self.check_fail(friend_blob_get , [ zauth ,fid, Constants.USER_BLOB],[403])
		self.assertTrue(ret, msg='Failed to send API request')

        def test_friend_blob_get_no_zauth_header(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
                fid = random.choice(fid_list)
                ret,result = self.check_fail(friend_blob_get_no_Zauth_head, [fid, Constants.USER_BLOB],[403])
		self.assertTrue(ret, msg='Failed to send API request')

        def test_friend_blob_get_nonfriend(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret =   get_friend_nofriend_id(zauth, Constants.GRAPH_TYPE)
                fid_list=ret['result']['data'][Constants.GRAPH_TYPE]
		nfid=nfzid(zauth)
                ret , result = self.check_fail(friend_blob_get , [ zauth ,nfid, Constants.USER_BLOB],[403,404])
		self.assertTrue(ret, msg='Failed to send API request')
	


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(blob_unit)
        unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='istorage.html', xml='istorage.xml')
