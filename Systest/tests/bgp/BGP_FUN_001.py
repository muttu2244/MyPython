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

DESCRIPTION: To verify that OSPF NBMA can be configured.
TEST PLAN: OSPF NBMA Test Plans
TEST CASES: BGP_FUN_001

HOW TO RUN: python2.5 BGP_FUN_001.py
AUTHOR: jameer@stoke.com
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
from misc import *
from helpers import is_healthy
import re


#import configs file and topo..
from bgp_config import *
from topo import *


class test_BGP_FUN_001(test_case):
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

    def test_BGP_FUN_001(self):

        self.myLog.output("==================Starting The Test====================")

        # Push SSX config
        self.ssx.config_from_string(script_var['BGP_FUN_001'])

        #Changing context from local
        self.ssx.cmd("context %s"%script_var['context_name'])
	
	# Verifying the BGP Summary and Neighbor information.
	self.myLog.output("Delay is given for summarization and rip messages exchange")
 	time.sleep(200)
	bgp = self.ssx.cmd("show ip bgp summary")
	self.myLog.output("BGP Summary on context1 \n %s \n"%bgp)
	neighbor = self.ssx.cmd("show ip bgp neighbor")
	self.myLog.output("BGP neighbors on context1 \n %s \n"%neighbor)
	neighbor_state = self.ssx.cmd("show ip bgp neighbors | grep -i \"bgp state\"")
	self.failIf(int(bgp.splitlines()[5].split()[3]) == 0 , "BGP message is not recieved from other end router")
	self.failIf(neighbor_state.split()[-1] != 'Idle' , "Test Failed")

	# Verifying the BGP Summary and Neighbor information on other end.
	self.myLog.output("Verifying the BGP Summary and Neighbor information on other router")
        bgp1 = self.ssx.cmd("show ip bgp summary")
        self.myLog.output("BGP Summary on context1 \n %s \n"%bgp1)
        neighbor1 = self.ssx.cmd("show ip bgp neighbor")
        self.myLog.output("BGP neighbors on context1 \n %s \n"%neighbor1)
        neighbor_state1 = self.ssx.cmd("show ip bgp neighbors | grep -i \"bgp state\"")
        self.failIf(int(bgp.splitlines()[5].split()[3]) == 0 , "BGP message is not recieved from other end router")
        self.failIf(neighbor_state1.split()[-1] != 'Idle' , "Test Failed")


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("BGP_FUN_001.log", debug=True,console=True)
    	vgrp_str = "%s %s"%(topo1[0],topo1[1])
   	vgroup_new(vgrp_str)
        suite = test_suite()
        suite.addTest(test_BGP_FUN_001)
        test_runner(stream=sys.stdout).run(suite)


