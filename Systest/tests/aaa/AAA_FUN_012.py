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

Description: - Verify that SSX DOES NOT consult other databases in the method list 
		when authentication fails with the primary database (RADIUS) .
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-012

TOPOLOGY DIAGRAM:

    (Linux)                              (SSX)                               (Linux)
    -------                             --------                          --------------
   |Takama | --------------------------|        |------------------------| qa-svr4      |
    -------                            |        |                         --------------
                                       |        |
                                       |Lihue-mc|
  (Netscreen)                          |        |                            (Linux)
    ------                             |        |                          --------------
   |qa-ns1 | --------------------------|        |-------------------------| qa-svr3      |
    ------                             |        |                          --------------
                                        --------

How to run: "python2.5 AAA_FUN_012.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
        Raja rathnam - rathnam@primesoftsolutionsinc.com
REVIEWER:
"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import *
from SSX import SSX
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *

#import configs file
from aaa_config import *
from topo import *

class test_AAA_FUN_012(test_case):

    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        #Establish a telnet session to the linux client box.
        self.linux = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.linux.telnet()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()
    
    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of linux Client
	self.linux.close()             

    def test_AAA_FUN_012(self):
        """
        Test case Id: -  AAA-FUN-012
        """

	self.myLog.output("\n**********start the test**************\n")

        #Push the SSX configuration
	self.ssx.config_from_string(script_var['common_ssx1'])
	self.ssx.config_from_string(script_var['fun_012_ssx'])
	
        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
	# Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate Telnet Session from linux Client with in-valid user credentials 
	# which are not configured in radius server  
        op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],
					username="user3@%s"%script_var['context'],password="invalidpasswd")
        self.failUnless(not op_telnet,"Telnet happened even with the user which is not present in the Radius db")

        # Verify that SSX should initially relay the authentication information to the RADIUS.
        op_debug =  aaa_verify_authentication(self.ssx,"user3@%s"% script_var['context'],"radius","FAIL")
        self.failUnless(op_debug,"Expected user authentication FAIL but not occurred")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_AAA_FUN_012)
    test_runner(stream=sys.stdout).run(suite)

