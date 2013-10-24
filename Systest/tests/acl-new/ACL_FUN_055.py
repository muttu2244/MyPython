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

DESCRIPTION:To Verify applying outbound access-list to a port-interface
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUN_055

TOPOLOGY : 
Linux1 (17.1.1.1/24) -> 3/0 (17.1.1.2/24) SSX
SSX (16.1.1.2/24) 2/0 -> Linux2 (16.1.1.1/24)

HOW TO RUN:python2.5 ACL_FUN_055.py
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



class test_ACL_FUN_055(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
	self.ssx.telnet()
        self.linux.telnet()
	self.linux1.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
	self.linux1.close()

    def test_ACL_FUN_055(self):


	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_055'])
	self.linux1.configure_ip_interface(p1_ssx_linux1[1], script_var['linux_phy_iface1_ip_mask'])
	self.linux1.configure_ip_interface(p1_ssx_linux2[1], script_var['linux_phy_iface2_ip_mask'])
	self.linux.cmd("sudo /sbin/route add -net %s gw %s" %(script_var['client1_route'],script_var['client1_gateway']))
        self.linux1.cmd("sudo /sbin/route add -net %s gw %s" %(script_var['client2_route'],script_var['client2_gateway']))


        #changing context and clear port counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip access-list name subacl counters")

        #applying nemesis tool for generating igmp packets
        self.linux.cmd("ping -c 5 %s"%(script_var['linux_phy_iface2_ip']),timeout=40)
     
        result=self.ssx.cmd("show ip access-list name subacl counters")

        result=result.split('\n')
        result=result[2]

        result=result.split('       ')
        output=result[5]

        output=int(output)

	self.failIfEqual(output,0,"Deny Outbound ICMP  Failed")
	
	self.ssx.cmd("clear ip access-list name subacl counters")

	self.linux.cmd("sudo /usr/local/bin/nemesis tcp -S %s -D %s -d %s"%(script_var['linux_phy_iface1_ip'],script_var['linux_phy_iface2_ip'],p1_ssx_xpressvpn[1]))

        result=self.ssx.cmd("show ip access-list name subacl counters")

        result=result.split('\n')
        result=result[2]

        result=result.split('       ')
        output=result[4]

        output=int(output)

	self.failIfEqual(output,0,"Permit Outbound TCP Failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_055)
        test_runner(stream = sys.stdout).run(suite)

