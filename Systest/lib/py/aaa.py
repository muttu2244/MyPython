#!/usr/bin/env python2.5
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : This Script contains following AAA  APIs which has 
			  been used in the AAA/RADIUS Testcases
			   1.	generic_verify_telnet_2_ssx
			   2.	aaa_verify_authentication	
			   3.	generic_verify_config			   
	
TEST PLAN               : AAA/RADIUS Test plan V0.2
AUTHOR                  : Mahesh Kumar; email :  mahesh@primesoftsolutionsinc.com
			  Raja Rathnam; email :  rathnam@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import pexpect
import time
import string
import sys
import re

from logging import getLogger
log = getLogger()
from ike import verify_in_debug

def generic_verify_telnet_2_ssx(self, ssx_ip="10.1.1.2", username="user1@local", password="user1",timeout=None):
        '''Connect to SSX via telnet from a Linux mahcine, username defaults to "user1@local",
        password defaults to "user1" '''

        self.ses.sendline("telnet %s" %ssx_ip)
        log.debug("Tryig to connect to SSX port: %s with the user as: %s" %(ssx_ip,username))
        if not self.ses.expect("sername: ", 100):
                self.ses.sendline(username)
        if not self.ses.expect("assword:", 100):
                self.ses.sendline(password)
        expect_output = self.ses.expect(["[#,>]","sername: "],100)
        if expect_output == 1:
                log.debug("Invalid user / password")
                return False
        log.debug("Login to SSX port %s --> success" %ssx_ip)
        if timeout:
                log.debug("going to be idle for %s secs" %timeout)
                time.sleep(int(timeout))
                self.ses.expect(["closed"],100)
                log.debug(" SSX Terminated the telnet session of the user: %s " %username)
                return True

        elif timeout == None:
                log.debug("exiting from telnet session.........")
                command = "exit"
                self.ses.sendline(command)
                return True
        else :
                return False




#def aaa_verify_authentication(self,user_name,auth_method="None"):
def aaa_verify_authentication(self,user_name,auth_method="None", result="PASS"):
        if auth_method=="local":
	    #op1=verify_in_debug(self,user_name,"SUCCEEDED")
            #op2=verify_in_debug(self,user_name,"PASS")
            op2=verify_in_debug(self,user_name,result)
	    #if op1 and op2:
            if op2:
                return True
            else:
                return False
        elif auth_method=='radius':
	    #op1=verify_in_debug(self,user_name,"Radius")
            #op2=verify_in_debug(self,user_name,"PASS")
            op2=verify_in_debug(self,user_name,result)
	    #if op1 and op2:
            if op2 :
                return True
            else :
                return False


#defining verify_rda_counters_disconnect for rda disconnect counters
def verify_rda_counters_disconnect(self,rda_attr,accept="None",removed="None",reject="None"):

        if rda_attr:
                #verify in RDA counters 
                rda_lines = rda_attr.split('\n')

                result_request = rda_lines[10].split(' ')
                result_accept = rda_lines[11].split(' ')
                result_reject = rda_lines[12].split(' ')
                result_removed = rda_lines[22].split(' ')

                request_val = result_request[55].strip()
                accept_val  = result_accept[56].strip()
                removed_val = result_removed[41].strip()
                reject_val  = result_reject[56].strip()

                if request_val  and accept_val == accept and removed_val == removed and reject_val == reject:
                        return True
                else :
                        return False


#defining verify_rda_counters_coa for rda coa counters
def verify_rda_counters_coa(self,rda_attr,accept="None",removed="None",reject="None"):

        if rda_attr:
                #verify in RDA counters 
                rda_lines = rda_attr.split('\n')

                result_request = rda_lines[10].split(' ')
                result_accept = rda_lines[11].split(' ')
                result_reject = rda_lines[12].split(' ')
                result_removed = rda_lines[22].split(' ')

                request_val = result_request[38].strip()
                accept_val  = result_accept[39].strip()
                reject_val  = result_reject[39].strip()
                removed_val = result_removed[24].strip()

                if request_val  and accept_val == accept and removed_val == removed and reject_val == reject:
                        return True
                else :
                        return False


def generic_verify_config(self,context="none",config_file_loaded="none"):

        """
        Description: - This API verify the show config output with the config file loded test pass when
                        the match else false the testcase .
        CLI Used- CLI.s that are used for the API  <show configuration>.
        Input: - List of Inputs to the API, mandatory are[context,config_file_loaded].
        Output: - List of values that this API returns to the calling function e.i Pass or Fail .
        Author: - Raja rathnam , rathnam@primesoftsolutionsinc.com .
        Reviewer: -                        """

        """ verify the 'show config' output with the  given config_file """
        if context=="none":
            cli="show configuration"
        else:
            cli="show configuration context %s"% context

        # Store the show config output in ssx_show_op
        show_output = self.cmd(cli)

        #split config_file based on the new line and stroe
        #the list of commands in a list "config_file_command_list"
        config_file_command_list=config_file_loaded.split('\n')

        #Verfying the commands in show_output and config_file
	# Return a tuple true or false and reason for false
        for command in config_file_command_list:
                if command.strip() in show_output :
			pass
		else:
			return False,(""" TestFailed because of missmatch in
                         expected and actual output
                         CLI Used - <"%s">
                         Expected in output of < %s > - %s
                         Actual output of < %s command is>  - %s"""% (cli,cli,command,cli,show_output))

	return True,1


