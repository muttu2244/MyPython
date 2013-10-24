#!/usr/bin/python26
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from  unit_class import *
from config import ConfigService
from acl import ACL
import sys
import pdb

Constants.SCOREBOARD_TYPES = ConfigService.getScoreboardTypes()
SCOREBOARD_TYPE = Constants.SCOREBOARD_TYPES[0]
class scoreboard_unit(gh_unit):



        """/*****************************************************************************************
				user.scoreboard.create TCs
        ********************************************************************************************"""	
	
	def test_user_scoreboard_create_Untrusted_bits(self):
		zauth= AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
		max=arr['max']
	        ret,result = self.check_pass( user_scoreboard_create, [zauth,max,SCOREBOARD_TYPE], ['0'])
		self.assertTrue(ret, msg = result)        


	def test_user_scoreboard_create_read_only_auth(self):
		zauth= AuthSystem.getReadonlyToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                ret,result = self.check_pass( user_scoreboard_create, [zauth, max, SCOREBOARD_TYPE], [403])
		self.assertTrue(ret, msg = result)

        def test_user_scoreboard_create_no_scoreboard_type(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                ret,result = self.check_pass( user_scoreboard_create, [zauth, max],[403])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_create_different_scoreboard_type(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
		ret,result = self.check_pass( user_scoreboard_create, [zauth, max,'different_score'],[403])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_create_no_post_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass( user_scoreboard_create,[zauth,SCOREBOARD_TYPE, ' '],[403])
		self.assertTrue(ret, msg = result)

        def test_user_scoreboard_create_meta_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                meta_data={"level": 5, "xp": 9}
                ret,result = self.check_pass(user_scoreboard_meta_create,[zauth,meta_data,SCOREBOARD_TYPE,max],[0])
		self.assertTrue(ret, msg = result)


	def test_user_scoreboard_create_exceed_max_storage_pool_count(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']

		maxcount=arr['maxcount']
		ret=max_count_storage(zauth,max,SCOREBOARD_TYPE,maxcount)
                ret,result = self.check_pass( user_scoreboard_create,[zauth,max, SCOREBOARD_TYPE],[413])
		self.assertTrue(ret, msg = result)
		
		"""delete all the scoreboards created from membase """
		for key in result['id']:
			user_scoreboard_delete(zauth, key)

					



        """/*****************************************************************************************
                                user.scoreboard.get TCs
        ********************************************************************************************"""


        def test_user_scoreboard_get_untrusted_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass( user_scoreboard_get, [zauth,scoreboard_key],[0] )
		self.assertTrue(ret, msg = result)

        def test_user_scoreboard_get_readonly_auth(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max, SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_pass( user_scoreboard_get, [zauth,scoreboard_key],[0])
		self.assertTrue(ret, msg = result)

        def test_user_scoreboard_get_invalid_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key= 'test:1:scoreboard:viral:0000000'
                ret,result = self.check_pass( user_scoreboard_get, [zauth,scoreboard_key], [404,403])
		self.assertTrue(ret, msg = result)

        def test_user_scoreboar_get_no_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass( user_scoreboard_get, [zauth],[403, 500] )
		self.assertTrue(ret, msg = result)


        """/*****************************************************************************************
                              		friend.scoreboard.get TCs
        ********************************************************************************************"""
	
	def test_friend_scoreboard_get_Untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		limit=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
		max=limit['max']				
		"""create a scoreboard and get the scoreboard key"""
		result = user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']

		ACL_arr=ACL.getGraphTypes('friend.scoreboard.get', SCOREBOARD_TYPE)
		for element in ACL_arr:
			if (element == 'any'):
				ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
				ret =   get_friend_nofriend_id(zauth,element)
                        	fid_list=ret['result']['data'][element]
	                        fid = random.choice(fid_list)
				fzauth=AuthSystem.getUntrustedToken(fid)
				ret,result = self.check_pass(friend_scoreboard_get, [fzauth ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
		
				""" for non-friends"""
				nfid=nfzid(zauth)
				nfzauth=AuthSystem.getUntrustedToken(nfid)
				ret,result = self.check_pass(friend_scoreboard_get, [nfzauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)




        def test_friend_scoreboard_get_readonly_bits(self):
		zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		limit=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=limit['max']           
		"""create a scoreboard and get the scoreboard key"""
                result = user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
		zauth=AuthSystem.getReadonlyToken(Constants.ZID)

                ACL_arr=ACL.getGraphTypes('friend.scoreboard.get', SCOREBOARD_TYPE)
                for element in ACL_arr:
	                if (element == 'any'):
				zauth_any=AuthSystem.getReadonlyToken(Constants.ZID+1)
        	                ret,result = self.check_pass(friend_scoreboard_get, [zauth_any ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
                	elif (element == 'self'):
                        	ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
	                elif (element == 'none'):
        	                ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
                	else:
                        	"""graph list is specified """
	                        ret =   get_friend_nofriend_id(zauth,element)
        	                fid_list=ret['result']['data'][element]
                	        fid = random.choice(fid_list)
                        	fzauth=AuthSystem.getReadonlyToken(fid)
	                        ret,result = self.check_pass(friend_scoreboard_get, [fzauth ,scoreboard_key],[0])
				self.assertTrue(ret, msg = result)

	                        """ for non-friends"""
                	        nfid=nfzid(zauth)
                        	nfzauth=AuthSystem.getReadonlyToken(nfid)
	                        ret,result = self.check_pass(friend_scoreboard_get, [nfzauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)


		

	def test_friend_scoreboard_get_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		limit=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
		scoreboard_key='abcd'
                max=limit['max']
		ACL_arr=ACL.getGraphTypes('friend.scoreboard.get', SCOREBOARD_TYPE)
		for element in ACL_arr:
       	  		if (element == 'any'):
                        	ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
	                elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
        	                ret,result = self.check_pass(friend_scoreboard_get, [zauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
                	        """graph list is specified """
                        	ret =   get_friend_nofriend_id(zauth,element)
                  	      	fid_list=ret['result']['data'][element]
                        	fid = random.choice(fid_list)
               	        	fzauth=AuthSystem.getUntrustedToken(fid)
                	        ret,result = self.check_pass(friend_scoreboard_get, [fzauth ,scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)

	                        """ for non-friends"""
        	                nfid=nfzid(zauth)
                	        nfzauth=AuthSystem.getUntrustedToken(nfid)
                        	ret,result = self.check_pass(friend_scoreboard_get, [nfzauth ,scoreboard_key],[403])
				self.assertTrue(ret, msg = result)





        """/*****************************************************************************************
				friend.scoreboard.increment
        ********************************************************************************************"""

        def test_friend_scoreboard_increment_Untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                min=arr['min']
		"""get scoreboard key by adding one"""
		result = user_scoreboard_create (zauth,min,SCOREBOARD_TYPE)
	        scoreboard_key=result['id']
		
		ACL_arr=ACL.getGraphTypes('friend.scoreboard.increment', SCOREBOARD_TYPE)
                for element in ACL_arr:
               		if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
                        	ret,result = self.check_pass(friend_scoreboard_increment, [zauth_any, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
               		elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
            		else:
                        	"""graph list is specified """
                	        ret =   get_friend_nofriend_id(zauth,element)
                        	fid_list=ret['result']['data'][element]
	                        fid = random.choice(fid_list)
        	                fzauth=AuthSystem.getUntrustedToken(fid)
				ret,result = self.check_pass(friend_scoreboard_increment, [fzauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
	
        	                """ for non-friends"""
                	        nfid=nfzid(zauth)
                        	nfzauth=AuthSystem.getUntrustedToken(nfid)
				ret,result = self.check_pass(friend_scoreboard_increment, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)



        def test_friend_scoreboard_increment_readonly_bits(self):
		zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                min=arr['min']
		"""get scoreboard key by adding one"""
                result = user_scoreboard_create (zauth,min,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
		zauth=AuthSystem.getReadonlyToken(Constants.ZID)
                ACL_arr=ACL.getGraphTypes('friend.scoreboard.increment', SCOREBOARD_TYPE)
                for element in ACL_arr:
        	        if (element == 'any'):
				zauth_any = AuthSystem.getReadonlyToken(Constants.ZID+1)
                	        ret,result = self.check_pass(friend_scoreboard_increment, [zauth_any, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
	                elif (element == 'self'):
        	                ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
               		elif (element == 'none'):
                        	ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
               		else:
                        	"""graph list is specified """
                    		ret =   get_friend_nofriend_id(zauth,element)
                       		fid_list=ret['result']['data'][element]
                   		fid = random.choice(fid_list)
                  		fzauth=AuthSystem.getReadonlyToken(fid)
                       		ret,result = self.check_pass(friend_scoreboard_increment, [fzauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)

                       		""" for non-friends"""
                   		nfid=nfzid(zauth)
          	                nfzauth=AuthSystem.getReadonlyToken(nfid)
                  	        ret,result = self.check_pass(friend_scoreboard_increment, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
	


	def test_friend_scoreboard_increment_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                min=arr['min']
		scoreboard_key=0000
		ACL_arr=ACL.getGraphTypes('friend.scoreboard.increment', SCOREBOARD_TYPE)
                for element in ACL_arr:
	                if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth_any, scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
	                        ret =   get_friend_nofriend_id(zauth,element)
        	                fid_list=ret['result']['data'][element]
                	        fid = random.choice(fid_list)
                        	fzauth=AuthSystem.getUntrustedToken(fid)
	                        ret,result = self.check_pass(friend_scoreboard_increment, [fzauth, scoreboard_key],[403,404])
				self.assertTrue(ret, msg = result)
	
        	                """ for non-friends"""
                	        nfid=nfzid(zauth)
                        	nfzauth=AuthSystem.getUntrustedToken(nfid)
	                        ret,result = self.check_pass(friend_scoreboard_increment, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)


		

	def test_friend_scoreboard_increment_increment_val_morethan_once(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                min=arr['min']
		"""get the scoreboard key by creating one"""
		result= user_scoreboard_create(zauth, min,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
		ACL_arr=ACL.getGraphTypes('friend.scoreboard.increment', SCOREBOARD_TYPE)
		for element in ACL_arr:
                        if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				friend_scoreboard_increment(zauth_any, scoreboard_key)
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth_any,scoreboard_key],[412])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				friend_scoreboard_increment(zauth, scoreboard_key)	
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[412])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                fzauth=AuthSystem.getUntrustedToken(fid)
				friend_scoreboard_increment(fzauth, scoreboard_key)
                                ret,result = self.check_pass(friend_scoreboard_increment, [fzauth, scoreboard_key],[412])
				self.assertTrue(ret, msg = result)

                                """ for non-friends"""
                                nfid=nfzid(zauth)
                                nfzauth=AuthSystem.getUntrustedToken(nfid)
                                ret,result = self.check_pass(friend_scoreboard_increment, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)

	

	def test_friend_scoreboard_increment_val_greater_than_max(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
		"""get the scoreboard key by creating one"""
                result= user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ACL_arr=ACL.getGraphTypes('friend.scoreboard.increment', SCOREBOARD_TYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth_any, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_increment, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                fzauth=AuthSystem.getUntrustedToken(fid)
                                ret,result = self.check_pass(friend_scoreboard_increment, [fzauth, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)

                                """ for non-friends"""
                                nfid=nfzid(zauth)
                                nfzauth=AuthSystem.getUntrustedToken(nfid)
                                ret,result = self.check_pass(friend_scoreboard_increment, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)



				


        """/*****************************************************************************************
					freind.scoreboard.decrement Tcs
        ********************************************************************************************"""

	def test_friend_scoreboard_decrement_untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
		"""get the scoreboard key by creating one"""
                result= user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
		ACL_arr=ACL.getGraphTypes('friend.scoreboard.decrement',SCOREBOARD_TYPE)
		for element in ACL_arr:
			if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth_any, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                fzauth=AuthSystem.getUntrustedToken(fid)
				ret,result = self.check_pass(friend_scoreboard_decrement, [fzauth, scoreboard_key],[0])
				self.assertTrue(ret, msg = result)
			        """ for non-friends"""
                                nfid=nfzid(zauth)
                                nfzauth=AuthSystem.getUntrustedToken(nfid)
				ret,result = self.check_pass(friend_scoreboard_decrement, [nfzauth, scoreboard_key],[403])	
				self.assertTrue(ret, msg = result)
		


        def test_friend_scoreboard_decrement_read_only(self):
		zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                """get the scoreboard key by creating one"""
                result= user_scoreboard_create(zauth,max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
		zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ACL_arr=ACL.getGraphTypes('friend.scoreboard.decrement',SCOREBOARD_TYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				zauth_any = AuthSystem.getReadonlyToken(Constants.ZID+1)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [zauth_any, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
                        elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
				fzauth=AuthSystem.getReadonlyToken(fid)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [fzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
                                """ for non-friends"""
                                nfid=nfzid(zauth)
				nfzauth=AuthSystem.getReadonlyToken(nfid)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)





        def test_friend_scoreboard_decrement_val_morethan_once(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                """get the scoreboard key by creating one"""
                result= user_scoreboard_create(zauth, max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ACL_arr=ACL.getGraphTypes('friend.scoreboard.decrement',SCOREBOARD_TYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				friend_scoreboard_decrement(zauth_any, scoreboard_key)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [zauth_any, scoreboard_key],[412])
				self.assertTrue(ret, msg = result)
                        elif (element == 'self'):
				friend_scoreboard_decrement(zauth, scoreboard_key)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[412])
				self.assertTrue(ret, msg = result)
                        elif (element == 'none'):
                                ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
                        else:
                                """graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                fzauth=AuthSystem.getUntrustedToken(fid)
				friend_scoreboard_decrement(fzauth, scoreboard_key)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [fzauth, scoreboard_key],[412])
				self.assertTrue(ret, msg = result)
                                """ for non-friends"""
                                nfid=nfzid(zauth)
                                nfzauth=AuthSystem.getUntrustedToken(nfid)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)




        def test_friend_scoreboard_decrement_val_less_than_min(self):
		zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                min=arr['min']

		"""get the scoreboard key by creating one"""
                result= user_scoreboard_create(zauth, min,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ACL_arr=ACL.getGraphTypes('friend.scoreboard.decrement',SCOREBOARD_TYPE)
                for element in ACL_arr:
                        if (element == 'any'):
				zauth_any = AuthSystem.getUntrustedToken(Constants.ZID+1)
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth_any, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)
			elif (element == 'self'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)
			elif (element == 'none'):
				ret,result = self.check_pass(friend_scoreboard_decrement, [zauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)
			else:
				"""graph list is specified """
                                ret =   get_friend_nofriend_id(zauth,element)
                                fid_list=ret['result']['data'][element]
                                fid = random.choice(fid_list)
                                fzauth=AuthSystem.getUntrustedToken(fid)
                                friend_scoreboard_decrement(zauth, scoreboard_key)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [fzauth, scoreboard_key],[416])
				self.assertTrue(ret, msg = result)
                                """ for non-friends"""
                                nfid=nfzid(zauth)
                                nfzauth=AuthSystem.getUntrustedToken(nfid)
                                ret,result = self.check_pass(friend_scoreboard_decrement, [nfzauth, scoreboard_key],[403])
				self.assertTrue(ret, msg = result)






        """/*****************************************************************************************
					user.scoreboard.setmeta TCs
        ********************************************************************************************"""
       

	def test_user_scoreboard_setmeta_untrusted_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                ret,result =self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data],[0])
		self.assertTrue(ret, msg = result)



        def test_user_scorebopard_setmeta_readonly_bits(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403])
		self.assertTrue(ret, msg = result)

        def test_user_setmeta_no_meta_data(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE) 
                scoreboard_key=result['id']
                meta_data={"meta" : []}
                ret,result = self.check_pass( user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[0])
		self.assertTrue(ret, msg = result)


	def test_user_setmeta_wrong_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key=0000
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                ret,result = self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[404,403])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_wrong_meta_dta_format(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                meta_data={"meta123":{"level": 1, "coin" : 1000}}
                ret,result = self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403,404])
		self.assertTrue(ret, msg = result)


        def test_user_setmeta_invalid_scoreboard_key(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='test:1:scoreboard:viral:000000'
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                ret,result = self.check_pass(user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[403,404])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_setmeta_multiple_updates(self):
                zauth = AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                meta_data={"meta":{"level" : 10, "coin" : 10000, "point" : 23400, "xp" : 32}}
                count=1
                while count <= 5:
                        ret=user_scoreboard_setmeta(zauth,scoreboard_key,meta_data)
                        count= count + 1

                ret,result = self.check_pass( user_scoreboard_setmeta,[zauth, scoreboard_key,meta_data ],[0])
		self.assertTrue(ret, msg = result)
		

        """/*****************************************************************************************
					user.scoreboard.delete TCs
        ********************************************************************************************"""


	def test_user_scoreboard_delete_untrusted_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth, scoreboard_key],[0])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_delete_readonly_bits(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
		arr=ConfigService.getScoreBoardLimits(SCOREBOARD_TYPE)
                max=arr['max']
                result = user_scoreboard_create(zauth,max,SCOREBOARD_TYPE)
                scoreboard_key=result['id']
                zauth= AuthSystem.getReadonlyToken(Constants.ZID)
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth, scoreboard_key],[403])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_delete_invalid_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='test:1:scoreboard:viral:0000'
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_delete_no_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth ],[403,404])
		self.assertTrue(ret, msg = result)


        def test_user_scoreboard_delete_wrong_scoreboard_key(self):
                zauth=AuthSystem.getUntrustedToken(Constants.ZID)
                scoreboard_key='00000'
                ret,result = self.check_pass(user_scoreboard_delete,[ zauth, scoreboard_key],[403,404])
		self.assertTrue(ret, msg = result)


		
if __name__ == '__main__':
	#suite0 = unittest.TestLoader().loadTestsFromTestCase(scoreboard_unit)
	#unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='/opt/zynga/greyhound/current/gh_test/scripts/test/results/scoreboard.html')


	
		
