#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION:To Verify permit (out) and Deny (out) counters when inbound filter is applied to a port. Repeat the test case with ACL applied to session name.
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUN_015

HOW TO RUN:python2.5 ACL_FUN_015.py
AUTHOR: jayanth@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from acl import *
from helpers import is_healthy
from misc import *

#import config and topo file
from config import *
from topo import *



class test_ACL_FUN_015(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
	self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
        self.ssx.telnet()
        self.linux.telnet()
	self.linux1.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
	self.linux1.close()

    def test_ACL_FUN_015(self):


	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_015'])


        #changing context and clear port counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip counters")
	
	self.ssx.cmd("clear ip access-list name subacl counters")
        time.sleep(5)
	self.linux.cmd("ping 16.1.1.1 -c 5",timeout=60)
	time.sleep(5)
	output=self.ssx.cmd("show ip access-list name subacl counters")
	
	output=output.split("\n")
	output=output[2]

	output=output.split("       ")
	output=output[5]
	
	self.failUnless(output , "Deny Counters Increment Failed")

	self.ssx.config_from_string(script_var['ACL_FUN_015_MOD'])


        #changing context and clear port counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip counters")

        self.ssx.cmd("clear ip access-list name subacl counters")
        time.sleep(5)
        self.linux.cmd("ping 16.1.1.1 -c 5",timeout=60)
        time.sleep(5)
        output=self.ssx.cmd("show ip access-list name subacl counters")

        output=output.split("\n")
        output=output[2]

        output=output.split("       ")
        output=output[4]

        self.failUnless(output , "Permit Counters Increment Failed")


	# Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_015)
        test_runner(stream = sys.stdout).run(suite)

