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

#diff_path = os.path.dirname(os.path.abspath(__file__))
diff_path = os.path.dirname(os.path.abspath(__file__)) + "/../results"

class blob_diff(gh_unit):

        """/*****************************************************************************************
                                user.blob.patch  TCs
        ********************************************************************************************"""
        def test_user_blob_patch_existing_blob(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get(zauth)		
		if "'CAS': None" in str(result):
			cas=" "
		else:
                	cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		
		data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
		oldFile = diff_path + '/old.txt'
		f = open(oldFile,'wb+')
                f.write(data)
		f.close()
	
		result = user_blob_get(zauth)
		
		newFile = diff_path + '/new.txt'
		f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]	
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
		self.assertTrue(ret, msg='Failed to send API request')
		os.system('rm %s/out.zcdiff'%diff_path)
	def test_user_blob_patch_series_diffs(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)           
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
		
		oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

		newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()
		
		oldFile1 = diff_path + '/old1.txt'
                os.system('cp %s %s' %(newFile, oldFile1)) 
		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
		os.system('rm %s/out.zcdiff'%diff_path)

		result = user_blob_get(zauth)
		oldFile = oldFile1
		newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		checksum = diff_data_post(diff_path,oldFile,newFile)
		ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
		self.assertTrue(ret, msg='Failed to send API request')
		os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_empty_old_blob(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

		data = ''
		ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

		newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
		f.write('dfssdfio^&*^&*678687')
                f.close()		

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[500])
		self.assertTrue(ret, msg='Failed to send API request: (P3:Jira Defect: SEG-9315)')
		os.system('rm %s/out.zcdiff'%diff_path)

	'''
	def test_user_blob_patch_same_contents(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                #path = '/home/sdoddabasayya/blobDiff/php-zcdiff'
                #oldBlob = 'old.txt'
                #data = data_to_post()
		data = "werkjl3234#$#$"
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)
				
		newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(data)
                f.close()
		
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		checksum = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
		self.assertTrue(ret, msg='Manually it passes--please reverify')
		os.system('rm %s/out.zcdiff'%diff_path)
		#print "Ret: %s\n"%ret
                #print "Result: %s\n"%result
		#print "*********************************************************************\n" 
	'''

	def test_user_blob_patch_empty_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
		
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

		zauth= None
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[403])
		self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)

             

        def test_user_blob_patch_expired_token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])

		oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth) 

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                zauth= AuthSystem.getExpiredToken(Constants.ZID)
                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[403])
		self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
        def test_user_blob_patch_invalid_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])

		oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth) 

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
		cas_invalid = cas + 1
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                ret, result = self.check_pass(user_blob_patch,[zauth,Constants.USER_BLOB,"%s/out.zcdiff"%diff_path,cas_invalid,checksum ],[409])
		self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)

	def test_user_blob_patch_miss_CAS(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()
		
		checksum  = diff_data_post(diff_path,oldFile,newFile)
		cas_miss = ''
                ret, result = self.check_pass(user_blob_patch, [zauth,Constants.USER_BLOB,"%s/out.zcdiff"%diff_path,cas_miss,checksum ],[409])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_corrupted_diff(self):
		#ZID = random.randint(1,9999)
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		result = user_blob_get( zauth )
		if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

		cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
		corruptFile = diff_path + '/out.zcdiff'
		f = open(corruptFile,'r+')
		f.seek(-10,2)
                f.write(os.urandom(5)) #Edit the zcdiff file by adding some random data to corrupt it. 
                f.close()
	
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[500])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_corrupted_checksum(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get( zauth )
                if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)

                corrupted_checksum = checksum + '23487HIH&*('  #corrupt the checksum by adding some random string

                ret,result = self.check_pass(user_blob_patch,[zauth,Constants.USER_BLOB,"%s/out.zcdiff"%diff_path,cas,corrupted_checksum ],[500])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_without_base(self):
		ZID = random.randint(1,9999) #Do not take zid from api_constants for this test, as it requires a new zid alltogether
                zauth = AuthSystem.getUntrustedToken(ZID)
                result = user_blob_get( zauth )
                if "'CAS': None" in str(result):
                        cas = 0
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                data = '' #the old blob can be taken as empty string as there is no existence of old blob in the first place
                
		oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                checksum  = diff_data_post(diff_path,oldFile,newFile)

                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[500])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)

	def test_user_blob_patch_without_checksum(self):
		zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
		checksum = None
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[500])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)


	def test_user_blob_patch_Admin_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close() 

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID) #Trusted auth  token is Admin token
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_ReadOnly_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                zauth = AuthSystem.getReadonlyToken(Constants.ZID) #Read only token
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[403])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
	
	def test_user_blob_patch_Impersonated_Token(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                result = user_blob_get(zauth)
                if "'CAS': None" in str(result):
                        cas=" "
                else:
                        cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]

                data = data_to_post()
                ret, result = self.check_pass(user_blob_set, [ zauth, Constants.USER_BLOB, data, cas ],[0])
                oldFile = diff_path + '/old.txt'
                f = open(oldFile,'wb+')
                f.write(data)
                f.close()

                result = user_blob_get(zauth)

                newFile = diff_path + '/new.txt'
                f = open(newFile,'wb+')
                f.write(os.urandom(100))
                f.close()

                cas = result[ Constants.BLOBS ][ Constants.USER_BLOB ][ Constants.GH_CAS ]
                checksum  = diff_data_post(diff_path,oldFile,newFile)
                zauth = AuthSystem.getImpersonatedAuthToken(Constants.ZID) #Impersonated token
                ret, result = self.check_pass(user_blob_patch, [ zauth, Constants.USER_BLOB, "%s/out.zcdiff"%diff_path, cas,checksum ],[0])
                self.assertTrue(ret, msg='Failed to send API request')
                os.system('rm %s/out.zcdiff'%diff_path)
if __name__ == '__main__':
	#suite0 = unittest.TestLoader().loadTestsFromTestCase(blob_diff)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/blob_delta.html')

