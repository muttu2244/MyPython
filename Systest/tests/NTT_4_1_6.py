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

DESCRIPTION: Confirm neighbor is established, and confirm it shows adjency status. (9/21/11 NOS Review - Ponit to Point Network).
TEST PLAN: 
TEST CASES: NTT_4_1_6

HOW TO RUN: python2.5 NTT_4_1_6.py
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

class test_NTT_4_1_6(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx1 = SSX(ssx1["ip_addr"])
	self.cisco = CISCO(cisco["ip_addr"])
        self.ssx1.telnet()
	self.cisco.console(cisco["ip_addr"])
        
        self.ssx1.clear_ports()
        self.ssx1.clear_context_all()
	
        # wait for card to come up
        self.ssx1.wait4cards()
        self.ssx1.clear_health_stats()
	
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx1.close()

    def test_NTT_4_1_6(self):

        self.myLog.output("==================Starting The Test====================")
	
        # Push SSX config
	self.ssx1.config_from_string(route_var['NTT_4_1_6'])
	self.myLog.info("Configured the OSPF, \nConfiguring in the Cisco")
	self.cisco.clear_interface_config(intf=p_ssx1_cisco[1])
	self.cisco.cmd("conf t")
	self.cisco.cmd("interface giga %s"%p_ssx1_cisco[1])
        self.cisco.cmd("no ip address")
        self.cisco.cmd("no switchport")
	self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%route_var['cisco_ospf_intf1_ip/mask'])
        self.cisco.cmd(" ip ospf mtu-ignore")
        self.cisco.cmd("no keepalive")
        self.cisco.cmd("no cdp enable")

	self.cisco.cmd("exit")
        self.cisco.cmd("exit")

        #Moving to context
        self.ssx1.cmd("context %s"%route_var['context_name1'])
        self.ssx1.cmd("clear ip ospf proc")
        #self.cisco.cmd("clear ip ospf proc")
	self.myLog.info("Given delay to OSPF come up")
	time.sleep(100)
	
	#Verify the all ospf's are up with the neighbor
	self.myLog.info("Verifying the ospf states at router - %s"%route_var['context_name1'])
	ospf_op1 = self.ssx1.cmd('show ip ospf neighbor | grep "%s"'%route_var['ospf_intf1_ip'])
        if not "Full" in ospf_op1:
		self.fail("OSPF Router is not established with the adjacent interface %s"%route_var['cisco_ospf_intf1_ip'])

       
        ospf_op1 = self.ssx1.cmd("show ip ospf interface vr1")
        if "POINTOPOINT" not in ospf_op1 :
           self.fail("Network Type POINTOPOINT is not there is output , actual output returned by command is %s"%ospf_op1)

        # Checking SSX Health
        hs1 = self.ssx1.get_health_stats()
        self.failUnless(is_healthy( hs1), "Platform is not healthy at SSX1")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_4_1_6.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_NTT_4_1_6)
        test_runner().run(suite)
