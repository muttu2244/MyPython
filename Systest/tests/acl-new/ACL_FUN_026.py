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

DESCRIPTION:Verify that SSX doesn't allow to apply a non-existing ACL to port-interface
TEST PLAN: ACL Test plans
TEST CASES: ACL_FUN_026

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24  ------------->  TransIP = 2.2.2.45/24          |
       |         									|
       |              ETH1                                       Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_026.py
AUTHOR:rajshekar@primesoftsolutionsinc.com  
REVIEWER:suresh@primesoftsolutionsinc.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from acl import *
from helpers import is_healthy
from misc import *

#import configs file
from config import *
from topo import *

class test_ACL_FUN_026(test_case):
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

    def test_ACL_FUN_026(self):


        self.myLog.output("==================Starting The Test====================")
		
	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_026'])
	self.linux.write_to_file(script_var['ACL_FUN_XPM_common'],"autoexec.cfg","/xpm/")
	self.ssx.cmd("context %s" %(script_var['context_name']))

	self.linux.cmd("cd /xpm")
	self.linux.cmd("sudo ./add_ip_route")
	self.linux.cmd("sudo ./start_ike")
	
	output=self.ssx.cmd("show session")

	self.failUnless(output=="", "Session Established When Inexistant ACL was applied to session")
	# Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_ACL_FUN_026)
	test_runner(stream = sys.stdout).run(suite)

