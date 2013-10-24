#!/usr/bin/python26
import os
import pdb
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from  unit_class import *
import sys
import pdb
class scoreboard_unit(gh_unit):

        """/*****************************************************************************************
				user.scoreboard.create TCs
        ********************************************************************************************"""	
	
	def test_user_scoreboard_create_Untrusted_bits(self):
		zauth= AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
       		max =int(max)
	        ret,result = self.check_pass( user_scoreboard_create, [zauth,max,Constants.SCOREBOARD_TYPE], ['0'])
		self.assertTrue(ret, msg = 'Failed to send API request')        

	'''
	def test_user_scoreboard_create_read_only_auth(self):
		zauth= AuthSystem.getReadonlyToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                ret,result = self.check_fail( user_scoreboard_create, [zauth, max, Constants.SCOREBOARD_TYPE], [403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''
        def test_user_scoreboard_create_no_scoreboard_type(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                ret,result = self.check_fail( user_scoreboard_create, [zauth, max],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''
        def test_user_scoreboard_create_non_integer_initial_val(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ival='abc'
                ret,result = self.check_fail( user_scoreboard_create, [zauth, ival,Constants.SCOREBOARD_TYPE],[403])
		self.assertTrue(ret, msg = 'Please refer Jira defect: SEG-6803')
	'''
        def test_user_scoreboard_create_different_scoreboard_type(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                ret,result = self.check_pass( user_scoreboard_create, [zauth, max,'different_score'],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_scoreboard_create_no_post_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail( user_scoreboard_create,[zauth,Constants.SCOREBOARD_TYPE, ' '],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_scoreboard_create_meta_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                meta_data={"level": 5, "xp": 9}
                ret,result = self.check_pass(user_scoreboard_meta_create,[zauth,meta_data,Constants.SCOREBOARD_TYPE,max],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')





        """/*****************************************************************************************
                                user.scoreboard.get TCs
        ********************************************************************************************"""


        def test_user_scoreboard_get_untrusted_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)

                result = user_scoreboard_create(zauth, max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass( user_scoreboard_get, [zauth,scoreboard_key],[0] )
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''
        def test_user_scoreboard_get_readonly_auth(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
	        result = user_scoreboard_create(zauth,max, Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_pass( user_scoreboard_get, [zauth,scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Please referJira defect: SEG-6874 ')
	'''
        def test_user_scoreboard_get_invalid_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key= 'test:1:scoreboard:viral:0000000'
                ret,result = self.check_fail( user_scoreboard_get, [zauth,scoreboard_key], [404,403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_user_scoreboar_get_no_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail( user_scoreboard_get, [zauth],[403, 500] )
		self.assertTrue(ret, msg = 'Failed to send API request')

	'''
        def test_user_scoreboard_get_key_exceed_max_url_len(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                size=4000
                #Constants.SCOREBOARD_TYPE=max_key(size)
		scoreboard_type=max_key(size)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)

                result =  user_scoreboard_create (zauth, max,Constants.SCOREBOARD_TYPE )
                scoreboard_key=result['id']
                ret,result = self.check_fail( user_scoreboard_get, [zauth, scoreboard_key],[413])
		self.assertTrue(ret, msg = 'Pleaes refer Jira defect: SEG-6531')
	'''


        """/*****************************************************************************************
                              		friend.scoreboard.get TCs
        ********************************************************************************************"""
	
	def test_friend_scoreboard_get_Untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result =  user_scoreboard_create (zauth, max,Constants.SCOREBOARD_TYPE )
                scoreboard_key=result['id']
                ret,result = self.check_pass(friend_scoreboard_get, [fzauth,scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''
        def test_friend_scoreboard_get_readonly_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getReadonlyToken(fid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result =  user_scoreboard_create (zauth, max,Constants.SCOREBOARD_TYPE )
                scoreboard_key=result['id']
                ret,result = self.check_pass(friend_scoreboard_get, [fzauth,scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Please refer Jira defect: SEG 6874')
	'''
        def test_friend_scoreboard_get_nonfriend(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                nfid=nfzid(zauth)
                nfzauth=AuthSystem.getUntrustedToken(nfid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result =  user_scoreboard_create (zauth, max,Constants.SCOREBOARD_TYPE )
                scoreboard_key=result['id']
                ret,result = self.check_fail(friend_scoreboard_get, [nfzauth,scoreboard_key],[0,403])
		self.assertTrue(ret, msg = 'Failed to send API request')

        def test_friend_scoreboard_get_no_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
	
                ret,result = self.check_fail(friend_scoreboard_get, [fzauth],[500,403])
		self.assertTrue(ret, msg = 'Failed to send API request')

	def test_friend_scoreboard_get_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)

                scoreboard_key='abcd'
                ret,result = self.check_fail(friend_scoreboard_get, [fzauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_friend_scoreboard_get_invalid_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                scoreboard_key='test:1:scoreboard:viral:0000'
                ret,result = self.check_fail(friend_scoreboard_get, [fzauth, scoreboard_key],[404,403])
		self.assertTrue(ret, msg = 'Failed to send API request')


        """/*****************************************************************************************
				friend.scoreboard.increment
        ********************************************************************************************"""

        def test_friend_scoreboard_increment_Untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
		min,host_ip,file,flag=remote_connect('min', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                min=int(min)
                result = user_scoreboard_create (zauth,min,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass( friend_scoreboard_increment, [fzauth, scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')

	'''
        def test_friend_scoreboard_increment_readonly_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getReadonlyToken(fid)
		min,host_ip,file,flag=remote_connect('min', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                min=int(min)
                result =  user_scoreboard_create(zauth, min,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_fail(friend_scoreboard_increment, [fzauth, scoreboard_key],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''

        def test_friend_scoreboard_increment_no_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                ret,result = self.check_fail(friend_scoreboard_increment, [fzauth ],[403,500])
		self.assertTrue(ret, msg = 'Failed to send API request')


	def test_friend_scoreboard_increment_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                scoreboard_key=0000
                ret,result = self.check_fail(friend_scoreboard_increment, [fzauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


	def test_friend_scoreboard_increment_increment_val_morethan_once(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
		min,host_ip,file,flag=remote_connect('min', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                min=int(min)
                result= user_scoreboard_create(zauth, min,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret2=friend_scoreboard_increment(fzauth, scoreboard_key)
                ret,result = self.check_fail(friend_scoreboard_increment, [fzauth, scoreboard_key],[412])
		self.assertTrue(ret, msg = 'Failed to send API request')



	def test_friend_scoreboard_increment_val_greater_than_max(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                result =user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_fail(friend_scoreboard_increment, [fzauth, scoreboard_key],[416])
		self.assertTrue(ret, msg = 'Failed to send API request')


        """/*****************************************************************************************
					freind.scoreboard.decrement Tcs
        ********************************************************************************************"""

	def test_friend_scoreboard_decrement_untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create( zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass( friend_scoreboard_decrement,[fzauth, scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')

	'''
        def test_friend_scoreboard_decrement_read_only(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getReadonlyToken(fid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result =user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_fail(friend_scoreboard_decrement,[fzauth, scoreboard_key],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''

        def test_friend_scoreboard_decrement_no_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                ret,result = self.check_fail(friend_scoreboard_decrement,[fzauth],[403,500])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_friend_scoreboard_decrement_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                scoreboard_key=000
                ret,result = self.check_fail(friend_scoreboard_decrement,[fzauth,scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_friend_scoreboard_decrement_val_morethan_once(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret=friend_scoreboard_decrement(fzauth,scoreboard_key)
                ret,result = self.check_fail(friend_scoreboard_decrement,[fzauth, scoreboard_key],[412])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_friend_scoreboard_decrement_invalid_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                scoreboard_key='test:1:scoreboard:viral:0000'
                ret=friend_scoreboard_decrement(fzauth,scoreboard_key)
                ret,result = self.check_fail(friend_scoreboard_decrement,[fzauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_friend_scoreboard_decrement_val_less_than_min(self):
		zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		min,host_ip,file,flag=remote_connect('min', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                min=int(min)
                fid=fzid(zauth)
                fzauth=AuthSystem.getUntrustedToken(fid)
                result = user_scoreboard_create(zauth,min,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_fail(friend_scoreboard_decrement, [fzauth, scoreboard_key],[416])
		self.assertTrue(ret, msg = 'Failed to send API request')



        """/*****************************************************************************************
					user.scoreboard.setmeta TCs
        ********************************************************************************************"""
       

	def test_user_scoreboard_setmeta_untrusted_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                ret,result =self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')


	'''
        def test_user_scorebopard_setmeta_readonly_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_fail(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''

        def test_user_setmeta_no_meta_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                meta_data={"meta" : []}
                ret,result = self.check_pass( user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')


	def test_user_setmeta_wrong_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key=0000
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                ret,result = self.check_fail(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[404,403])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_scoreboard_wrong_meta_dta_format(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                meta_data={"meta123":{"level": 1, "coin" : 1000}}
                ret,result = self.check_fail(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_setmeta_invalid_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='test:1:scoreboard:viral:000000'
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                ret,result = self.check_fail(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_scoreboard_setmeta_multiple_updates(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                count=1
                while count <= 5:
                        ret=user_scoreboard_setmeta(zauth,scoreboard_key,meta_data)
                        count= count + 1

                ret,result = self.check_pass( user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')
		

        """/*****************************************************************************************
					user.scoreboard.delete TCs
        ********************************************************************************************"""


	def test_user_scoreboard_delete_untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth, scoreboard_key],[0])
		self.assertTrue(ret, msg = 'Failed to send API request')

	'''
        def test_user_scoreboard_delete_readonly_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		max,host_ip,file,flag=remote_connect('max', 'Scoreboard' , Constants.SCOREBOARD_TYPE)
                max=int(max)
                result = user_scoreboard_create(zauth,max,Constants.SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_fail(user_scoreboard_delete,[ zauth, scoreboard_key],[403])
		self.assertTrue(ret, msg = 'Failed to send API request')
	'''

        def test_user_scoreboard_delete_invalid_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='test:1:scoreboard:viral:0000'
                ret,result = self.check_fail(user_scoreboard_delete,[ zauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_scoreboard_delete_no_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_fail(user_scoreboard_delete,[ zauth ],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


        def test_user_scoreboard_delete_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='00000'
                ret,result = self.check_fail(user_scoreboard_delete,[ zauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = 'Failed to send API request')


		
if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(scoreboard_unit)
        unittest.TextTestRunner(verbosity=99).run(suite0)


	
		
