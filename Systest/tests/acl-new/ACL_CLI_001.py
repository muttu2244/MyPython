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

DESCRIPTION:Verify all IPv4-ACL related CLI commands
TEST PLAN: ACL Test plans
TEST CASES:ACL_CLI_001

HOW TO RUN:python2.5 ACL_CLI_001.py
AUTHOR: jayanth@stoke.com
REVIEWER:

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



class test_ACL_CLI_001(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_ACL_CLI_001(self):
        
	# SSX config
        ip_cmd_arr = script_var['ACL_CLI_001'].split('\n')
        for i in range(0,len(ip_cmd_arr)):
           op_cmd = self.ssx.configcmd(ip_cmd_arr[i])
           self.failIf("ERROR" in op_cmd )

        # Store the show cofnig output in ssx_show_op
        ssx_show_op = self.ssx.configcmd("show configuration")

        # Verify each of the enterd commands with show config output present in "op_cmd_str"
        for entry in ip_cmd_arr:
           self.failUnless(entry.strip() in ssx_show_op,"Error while matching the cmd->%s with show oputput"% entry)
	
	# checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_CLI_001)
        test_runner(stream = sys.stdout).run(suite)

