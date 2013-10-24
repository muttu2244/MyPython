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

DESCRIPTION: Route delete and recovery behavior due to OSPF Hello unreachable.
TEST PLAN: DoCoMo regression
TEST CASES: DoCoMo_4_3_1

HOW TO RUN: python2.5 DoCoMo_4_3_1.py
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

class test_DoCoMo_4_3_1(test_case):
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

    def test_DoCoMo_4_3_1(self):

        self.myLog.output("==================Starting The Test====================")
	
        # Push SSX config
	self.ssx1.config_from_string(route_var['DoCoMo_4_3_1'])
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
	self.myLog.info("\n\n Verifying the route behavior with respect the routes\n\n")
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%route_var['ospf_intf1_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%route_var['cisco_ospf_intf1_ip'])

	# Verify the routes before OSPF Hello Unreachable
	self.myLog.info("Verify the routes before OSPF Hello Unreachable")
	for i in xrange(1,11):
		op1, op2 = chk_ip_route_proto(self.ssx1,route=route_var["static_route%s"%i],proto="ospf")
		self.failIf(len(op2) > 0, "check ip route failed for these parameters for route %s:%s"%(route_var["static_route%s"%i],op2))


	# Movomg to other context
	self.myLog.info(" Moving to other context")
	self.ssx1.cmd("context local")
	self.myLog.info("\n\nVerifying that routes are specific to context\n\n")
	for i in xrange(1,11):
                op1, op2 = chk_ip_route_proto(self.ssx1,route=route_var["static_route%s"%i])
		self.failIf(op2[0] != "Wrong input","Route is not deleted from the routing table after OSPF Hello Unreachable for the route %s"%route_var["static_route%s"%i])

	# Verfi the context parameters
	self.myLog.info("Verify the context parameters")
	contOp = self.ssx1.cmd("show context")
	self.failIf(contOp.splitlines()[-1].split()[0] == route_var['context_name1'] , "Context name is %s instead of local"% route_var['context_name1'])
	contOp = self.ssx1.cmd("show context %s"%route_var['context_name1'])
	self.failIf(contOp.splitlines()[-1].split()[0] != route_var['context_name1'] , "Context name is local instead of %s"% route_var['context_name1'])
	contOp = self.ssx1.cmd("show context local")
	self.failIf(contOp.splitlines()[-1].split()[0] == route_var['context_name1'] , "Context name is %s instead of local"% route_var['context_name1'])
	contOp = self.ssx1.cmd("show context all")
	self.failIf(route_var['context_name1'] not in contOp , "Context name %s is not found in 'show cont all'"% route_var['context_name1'])
	self.failIf("local" not in contOp , "Context name 'local' is not found in 'show cont all'")
	contOp = self.ssx1.cmd("show context summary")
	self.failIf(int(contOp.split()[-1]) != 2 , "Number of context shows more/less than configured")
	self.ssx1.cmd("config")
	self.ssx1.cmd("context test")
	self.ssx1.cmd("end")
	contOp = self.ssx1.cmd("show context summary")
        self.failIf(int(contOp.split()[-1]) != 3 , "Number of context shows more/less than configured")

        #Moving to context
	self.myLog.info(" Moving to context")
        self.ssx1.cmd("context %s"%route_var['context_name1'])
        self.myLog.info("Verify the context parameters @ context %s"% route_var['context_name1'])
        contOp = self.ssx1.cmd("show context")
        self.failIf(contOp.splitlines()[-1].split()[0] != route_var['context_name1'] , "Context name is %s instead of local"% route_var['context_name1'])
        contOp = self.ssx1.cmd("show context %s"%route_var['context_name1'])
        self.failIf(contOp.splitlines()[-1].split()[0] != route_var['context_name1'] , "Context name is local instead of %s"% route_var['context_name1'])
        contOp = self.ssx1.cmd("show context local")
        self.failIf(contOp.splitlines()[-1].split()[0] == route_var['context_name1'] , "Context name is %s instead of local"% route_var['context_name1'])
        contOp = self.ssx1.cmd("show context all")
        self.failIf(route_var['context_name1'] not in contOp , "Context name %s is not found in 'show cont all'"% route_var['context_name1'])
        self.failIf("local" not in contOp , "Context name 'local' is not found in 'show cont all'")
	contOp = self.ssx1.cmd("show context summary")
        self.failIf(int(contOp.split()[-1]) != 3 , "Number of context shows more/less than configured")
        self.ssx1.cmd("config")
        self.ssx1.cmd("context test")
        self.ssx1.cmd("end")
        contOp = self.ssx1.cmd("show context summary")
        self.failIf(int(contOp.split()[-1]) != 3 , "Number of context shows more/less than configured")
	
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
        log = buildLogger("DoCoMo_4_3_1.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_4_3_1)
        test_runner().run(suite)
