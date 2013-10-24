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

DESCRIPTION: Confirm COST is definable and changeable.
TEST PLAN:
TEST CASES: NTT_4-1-9

HOW TO RUN: python2.5 NTT_4_1_9.py
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
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from misc import *
from helpers import is_healthy
import re

#import configs file and topo..
from config_raja import *
from topo import *


class test_NTT_4_1_9(test_case):
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

    def test_NTT_4_1_9(self):

        self.myLog.output("==================Starting The Test====================")

	# Adding a Static route in rtr B
	self.ssx.cmd("config")
	self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("router-id %s"%script_var['intf_lo1_ip'])
	self.ssx.cmd("router ospf")
        self.myLog.info("\n\nDO STEP 1:Confirm COST is definable\n\n")
	out = self.ssx.cmd("neighbor %s cost 100"%script_var['intf1_ip'])
        self.failIf("ERROR:" in out,"\n\nGot below Error message while defining Cost : \n\n%s"%out)
        self.myLog.info("\n\nDONE STEP 1:Confirmed COST is definable\n\n")
        self.myLog.info("\n\nDO STEP 2:Confirm COST is changeable")
	out = self.ssx.cmd("neighbor %s cost 50"%script_var['intf1_ip'])
        self.failIf("ERROR:" in out,"\n\nGot below Error message while Changing Cost : \n\n%s"%out)
        self.myLog.info("\n\nDONE STEP 2:Confirmed COST is changeable\n\n")
	self.ssx.cmd("end")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_4_1_9.log", debug=True,console=True)
    	#vgrp_str = "%s %s"%(topo1[0],topo1[1])
   	#vgroup_new(vgrp_str)
        suite = test_suite()
        suite.addTest(test_NTT_4_1_9)
        test_runner(stream=sys.stdout).run(suite)


