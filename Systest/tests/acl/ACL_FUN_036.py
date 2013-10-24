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

DESCRIPTION:To verify IPV6 acl (icmp traffic) 
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_036

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24  ------------->  TransIP = 2.2.2.45/24          |
       |         									|
       |              ETH1                                       Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_036.py
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



class test_SAN_ACL_036(test_case):
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

    def test_SAN_ACL_036(self):


	   #vgroup b/w SSX and linux.
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring interface and tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_linux1[1],script_var['linux_phy_iface1_ipv6_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['SAN_ACL_036'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))

	#Minimum time taken for changing context.
	time.sleep(5)

	#ping operation   
	time.sleep(5)
	ping_op=self.ssx.ping(dest=script_var['linux_phy_iface1_ipv6'])
        self.failUnless(ping_op == 1,"Ping through interface failed when acl applied")


	# this api will check whether the icmp counts are getting incremented or not
        self.myLog.output("icmpCounters exists in SSX after sending traffic:%s" %self.ssx.cmd("show ipv6 counters icmp"))

	output=ip_verify_ipv6_counters_icmp(self.ssx,total_tx='5',echo_request='5',echo_reply='5')
	self.failUnless(output == 0,"ip_counters_icmp failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
		os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_SAN_ACL_036)
	test_runner(stream = sys.stdout).run(suite)

