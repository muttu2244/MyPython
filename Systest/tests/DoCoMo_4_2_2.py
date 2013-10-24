#!/volume/labtools/bin/python
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

DESCRIPTION: Route delete and recovery behavior due to OSPF Hello unreachable.
TEST PLAN: DoCoMo regression
TEST CASES: DoCoMo_4_2_2

HOW TO RUN: python2.5 DoCoMo_4_2_2.py
AUTHOR: jameer@stoke.com
REIEWER: kra@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from CISCO import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from vlan import *
from misc import *
from ospf_ikev2 import *
from helpers import is_healthy
import re

#Import Config and topo file
from config_docomo import *
from topo import *

class test_DoCoMo_4_2_2(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx1 = SSX(ssx1["ip_addr"])
	self.cisco = CISCO(cisco["ip_addr"])
        self.ssx1.telnet()
	self.cisco.console(cisco["ip_addr"])
	
        # Clear the SSX config
        self.ssx1.clear_config()

        # wait for card to come up
        self.ssx1.wait4cards()
        self.ssx1.clear_health_stats()
	
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx1.close()

    def test_DoCoMo_4_2_2(self):

        self.myLog.output("==================Starting The Test====================")
	
        # Push SSX config
	self.ssx1.config_from_string(route_var['DoCoMo_4_2_2'])
	self.myLog.info("Configured the OSPF, \nConfiguring in the Cisco")
	
	
	self.cisco.clear_interface_config(intf=p_ssx1_cisco[1])
	self.myLog.info("Adding required vlans to database")
	self.cisco.cmd("vlan database")
	self.cisco.cmd("vlan %s"%route_var['ospf_vlan1'])
	self.cisco.cmd("exit")
	self.cisco.cmd("conf t")
	self.cisco.cmd("no interface vlan %s"%route_var['ospf_vlan1'])
	self.cisco.cmd("interface vlan %s"%route_var['ospf_vlan1'])
	self.cisco.cmd("no ip address")
	self.cisco.cmd("no shutdown")
	self.cisco.cmd("ip address %s"%route_var['cisco_ospf_intf1_ip/mask'])
	self.cisco.cmd("exit")
	self.cisco.cmd("interface giga %s"%p_ssx1_cisco[1])
	self.cisco.cmd("switchport")
	self.cisco.cmd("switchport access vlan %s"%route_var['ospf_vlan1'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
	self.cisco.cmd("switchport trunk allowed vlan %s"%route_var['ospf_vlan1'])
	self.cisco.cmd("switchport mode trunk")
	self.cisco.cmd("no ip address")
	self.cisco.cmd("exit")
	self.cisco.cmd("no router ospf 123")
	self.cisco.cmd("router ospf 123")
	self.cisco.cmd("router-id 56.1.2.2")
	self.cisco.cmd("log-adjacency-changes")
	self.cisco.cmd("redistribute connected subnets")
	self.cisco.cmd("redistribute static subnets")
	self.cisco.cmd("network %s area 0"%route_var['ospf_route1'])
	self.cisco.cmd("exit")

	# Adding null routes to verify the routes delete/recovery
	self.myLog.info("Adding null routes at Cisco to verify the routes delete/recovery")
        self.cisco.cmd("ip route %s null0"%route_var['static_route1'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route2'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route3'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route4'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route5'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route6'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route7'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route8'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route9'])
        self.cisco.cmd("ip route %s null0"%route_var['static_route10'])
        self.cisco.cmd("end")
	time.sleep(10)

	#Moving to context
	self.ssx1.cmd("context %s"%route_var['context_name1'])
	self.myLog.info("Given delay to OSPF come up")
	time.sleep(100)
	
	#Verify the all ospf's are up with the neighbor
	self.myLog.info("Verifying the ospf states at router - %s"%route_var['context_name1'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%route_var['ospf_intf1_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%route_var['cisco_ospf_intf1_ip'])

	# Verify the routes before OSPF Hello Unreachable
	self.myLog.info("Verify the routes before OSPF Hello Unreachable")
	for i in xrange(1,11):
		op1, op2 = chk_ip_route_proto(self.ssx1,route=route_var["static_route%s"%i],proto="ospf")
		self.failIf(len(op2) > 0, "check ip route failed for these parameters for route %s:%s"%(route_var["static_route%s"%i],op2))


	self.myLog.info("Make OSPF Hello Unreachable")
	self.cisco.cmd("config ter")
	self.cisco.cmd("interface giga %s"%p_ssx1_cisco[1])
	self.cisco.cmd("shutdown")
	self.cisco.cmd("end")
	self.myLog.info("Given delay to OSPF to sync")
	time.sleep(80)

	self.myLog.info("\n\nVerifying that routes are dleted after OSPF Hello Unreachable\n\n")
	for i in xrange(1,11):
                op1, op2 = chk_ip_route_proto(self.ssx1,route=route_var["static_route%s"%i])
		self.failIf(op2[0] != "Wrong input","Route is not deleted from the routing table after OSPF Hello Unreachable for the route %s"%route_var["static_route%s"%i])

	# Make OSPF Hello reachable
        self.myLog.info("Make OSPF Hello reachable")
        self.cisco.cmd("config ter")
        self.cisco.cmd("interface giga %s"%p_ssx1_cisco[1])
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("end")
	self.myLog.info("Given delay to OSPF come up")
        time.sleep(100)

        self.myLog.info("\n\nVerifying that routes are recovered properly after OSPF Hello reachable\n\n")
        for i in xrange(1,11):
                op1, op2 = chk_ip_route_proto(self.ssx1,route=route_var["static_route%s"%i],proto="ospf")
                self.failIf(len(op2) > 0, "route %s is not recovered"%route_var["static_route%s"%i])

        # Checking SSX Health
        hs1 = self.ssx1.get_health_stats()
        self.failUnless(is_healthy( hs1), "Platform is not healthy at SSX1")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("DoCoMo_4_2_2.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_4_2_2)
        test_runner().run(suite)
