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


DESCRIPTION:To verify igmp  traffic after applying deny rule to acl context.
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_007
TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |              eth1                                       Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  jayanths@stoke.com
        
REVIEWER:

HOW TO RUN : python ACL_FUN_007.py
"""

import sys, os, getopt

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
import re


#import configs file
from config import *
from topo import *



class test_ACL_FUN_007(test_case):
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
    def test_ACL_FUN_007(self):
	
	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn[1], script_var['xpress_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_007'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("clear port counters")
	
	#nemesis tool for generating igmp packets on linux

	self.linux.cmd("sudo nemesis igmp -i 224.0.0.5")
	#verifying  coreespondig port counters
        cmd_op=self.ssx.cmd("show  port %s counters "%(p1_ssx_xpressvpn1[0]))
#	output=verify_port_counters(self.ssx,cmd_op,1)
	output = verify_port_counters(self.ssx,cmd_op,1)

        self.failIfEqual(output,1,"igmp through interface passed when acl applied")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ACL_FUN_007)
    test_runner(stream = sys.stdout).run(suite)

