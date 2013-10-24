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

DESCRIPTION:To verify that SSX allows all  protocol traffic when applied ACL is removed from interface configuration
 
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_024

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24 ----------->     TransIP = 2.2.2.45/24          |
       |     
       |                 ETH1                                    Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_008.py
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



class test_ACL_FUN_024(test_case):
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

    def test_ACL_FUN_024(self):

	 #vgroup b/w SSX and LINUX.
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_linux1[1], script_var['linux_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_024'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))

	#ping operation   
	ping_op=self.ssx.ping(dest=script_var['linux_phy_iface1_ip'])
	self.ssx.cmd("clear ip counters")
	ping_op=self.ssx.ping(dest=script_var['linux_phy_iface1_ip'])
        self.failUnless(ping_op == 0,"Ping through interface failed when acl applied")

	# this api will check whether the icmp stats are getting incremented or not
	self.myLog.output("icmpCounters exists in SSX after sending traffic:%s" %self.ssx.cmd("show ip counters icmp"))
        output=ip_verify_ip_counters_icmp(self.ssx,total_tx='5',total='0',echo_request='5', echo_reply='0', unreachable='0', mask_request='0', mask_reply='0', source_quench= '0' , param_problem='0', timestamp='0', redirects='0', info_reply='0', ttl_expired='0', other='0')
	self.failUnless(output == 1,"ip counters not incremented according to send traffic")


	self.myLog.output("====sending traffic when applied acl removed from interface configuration=====")

	# Push SSX config
        self.ssx.config_from_string(script_var['ACL_FUN_024_1'])

	#changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
	time.sleep(5)

	#Ping opeartion.
	self.ssx.cmd("clear ip counters")
	ping_op=self.ssx.ping(dest=script_var['linux_phy_iface1_ip'])
	self.failUnless(ping_op == 1,"Ping through interface failed when acl applied")
	self.myLog.output("icmpCounters exists in SSX after sending traffic :%s" %self.ssx.cmd("show ip counters icmp"))
	
	#This api check whether counters incremented or not.	
	output=ip_verify_ip_counters_icmp(self.ssx,total_tx='5',total='5',echo_request='5', echo_reply='5', unreachable='0', \
        mask_request='0', mask_reply='0', source_quench= '0' , param_problem='0', timestamp='0',\
        redirects='0', info_reply='0', ttl_expired='0', other='0')

        self.failUnless(output == 0,"counters not incremented according to sending traffic")

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
	suite.addTest(test_ACL_FUN_024)
	test_runner(stream=sys.stdout).run(suite)

