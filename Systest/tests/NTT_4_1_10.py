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

DESCRIPTION: To verify that Fast Hello can be enabled.
TEST PLAN: 
TEST CASES: NTT_4_1_10

HOW TO RUN: python2.5 NTT_4_1_10.py
AUTHOR: rajshekar@stoke.com
REIEWER: 

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
import re

#import configs file and topo..
from config_raja import *
from topo import *

class test_NTT_4_1_10(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.ssx.telnet()
        
        # Clear the SSX config
        self.ssx.clear_config()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()        
       
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

    def test_NTT_4_1_10(self):

        self.myLog.output("==================Starting The Test====================")

	# Verify the CLI case here..
	self.ssx.cmd("configuration")
	self.ssx.cmd("context %s"%script_var['context_name'])
	self.ssx.cmd("interface intf1")
	self.ssx.cmd("arp arpa")
	self.ssx.cmd("ip address %s"%script_var['intf1_ip/mask'])
	self.ssx.cmd("exit")
	self.ssx.cmd("router-id %s"%script_var['intf_lo1_ip'])
	self.ssx.cmd("router ospf")
	self.ssx.cmd("area %s"%script_var['area_id'])
	self.ssx.cmd("interface intf1")
        self.myLog.info("\n\nDO STEP 1:Confirm Fast Hello is available\n\n")
	op = self.ssx.cmd("dead-interval minimal hello-multiplier %s"%script_var['hello_mul'])
	self.failIf("ERROR:" in op.split(),"\n\nGot below Error message while enabling Fast Hello : \n\n%s"%op)
        self.myLog.info("\n\nDONE STEP 1:Confirmed Fast Hello is available\n\n")
        self.ssx.cmd("end")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_4_1_10.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_NTT_4_1_10)
        test_runner(stream=sys.stdout).run(suite)


