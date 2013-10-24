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

DESCRIPTION: To Verify that SSX allows/drops packets based on the ICMP message type and message code options
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUN_017


HOW TO RUN:python2.5 ACL_FUN_017.py
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



class test_ACL_FUN_017(test_case):
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

    def test_ACL_FUN_017(self):


	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_017'])


        #changing context and clear counters
        self.ssx.cmd("context %s" %(script_var['context_name']))

	#Resolving ARP
	self.ssx.cmd("ping %s repeat 1"%script_var['xpress_phy_iface1_ip'])


        self.ssx.cmd("clear ip access-list name subacl counters")
	time.sleep(5)
        #applying nemesis tool for generating icmp packets of TYPE-8(Packets should be allowed)
        self.linux.cmd("sudo /usr/local/bin/nemesis icmp -S %s -D %s -d %s -c 0 -i 8 "%( script_var['xpress_phy_iface1_ip'], script_var['ssx_phy_iface1_ip'],p1_ssx_xpressvpn[1]))
        time.sleep(5)

	output = verify_access_list_counters(self.ssx,permit_in="1")

        self.failUnless(output,"Icmp Permit for Type 8 Failed")
	
	self.ssx.cmd("clear ip access-list name subacl counters")
        time.sleep(5)
        
	#applying nemesis tool for generating icmp packets of not TYPE-8
        self.linux.cmd("sudo /usr/local/bin/nemesis icmp -S %s -D %s -d %s -c 8 -i 0"%( script_var['xpress_phy_iface1_ip'], script_var['ssx_phy_iface1_ip'],p1_ssx_xpressvpn[1]))
        time.sleep(5)
	
	output = verify_access_list_counters(self.ssx,deny_in="1")


        self.failUnless(output,"Icmp Deny for Non Type 8 Failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
	vgroup_new(vlan_cfg_acl)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_017)
        test_runner(stream = sys.stdout).run(suite)

