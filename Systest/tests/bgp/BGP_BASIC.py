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

DESCRIPTION: To verify BGP basic functionality.
TEST PLAN: BGP
TEST CASES: 

HOW TO RUN: python2.5 BGP_BASIC.py
AUTHOR: rajshekar@stoke.com
REIEWER: 
TOPODIAGRAM :
ssx          ----------> cisco
2/x or 3/x
for 4.6 :                1/3
x=0 or 1 or 2 or 3
for laurel :
x=0 or 1
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
from CISCO import *
from helpers import is_healthy
import re


#import configs file and topo..
from bgp_config import *
from topo import *


class test_BGP_BASIC(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.ssx.telnet()

        # Connection To CISCO
        self.myLog.info("Connecting to the cisco ")
        self.myLog.debug("has the IP of: %s" % topo.cisco["ip_addr"])
        self.cisco = CISCO(topo.cisco["ip_addr"])
        self.cisco.console(topo.cisco["ip_addr"])

        # Clear the SSX config
        #self.ssx.clear_config()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

    def test_BGP_BASIC(self):

        self.myLog.output("==================Starting The Test====================")
        
        testStepsList = ["NormalPort","Dot1qPort" , "untaggedPort"]
        testStepsList = ["NormalPort"]
        # Push SSX config
        self.ssx.config_from_string(script_var['BGP_BASIC-DutCfg'])
        self.myLog.info("\n Clearing CISCO interface configurations \n")
        self.cisco.cmd("vlan database")
        self.cisco.cmd("vlan %s"%script_var['vlan1'])
        self.cisco.cmd("exit")
        self.cisco.cmd("config t")
        self.cisco.cmd("no interface vlan %s"%script_var['vlan1'])
        self.cisco.cmd("no interface vlan 1")
        self.cisco.cmd("end")

        for testStep in testStepsList :
            if testStep=="NormalPort" :      
                self.myLog.info("\n\n #*50")
                self.myLog.info("\n\n Repeating Test with NORMAL Port \n\n")
                self.myLog.info("#*50\n\n")

                # Push SSX config
                self.ssx.cmd("end")
                self.ssx.cmd("conf")
                self.ssx.cmd("no port ethernet %s"%script_var['intf1_port'])
                self.ssx.cmd("port ethernet %s"%script_var['intf1_port'])
                self.ssx.cmd(" bind interface intf1 %s"%script_var['context_name'])
                self.ssx.cmd("exit")
                self.ssx.cmd("enable")
                self.ssx.cmd("exit")
                # Clearing CISCO interface configurations
                self.myLog.info("\n Clearing CISCO interface configurations \n")
                self.cisco.clear_interface_config(intf=script_var['slot2port_cisco'])
                self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")
                self.cisco.configure_ipv4_interface(ip_addr=script_var['intf2_ip_mask'],
                intf=script_var['slot2port_cisco'])
            if testStep=="Dot1qPort" :
                self.myLog.info("\n\n #*50")
                self.myLog.info("\n\n Repeating Test with DOT1Q Port \n\n")
                self.myLog.info("#*50\n\n")
                # Clearing CISCO interface configurations
                self.myLog.info("\n Clearing CISCO interface configurations \n")
                self.cisco.cmd("vlan database")
                self.cisco.cmd("vlan %s"%script_var['vlan1'])
                self.cisco.cmd("exit")
                self.cisco.cmd("config t")
                self.cisco.cmd("no interface vlan %s"%script_var['vlan1'])
                self.cisco.cmd("end")

                self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")

                self.cisco.clear_interface_config(intf=script_var['slot2port_cisco'])
                self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")
                self.cisco.configure_ipv4_vlan_interface(ip_addr=script_var['intf2_ip_mask'],
                  intf=script_var['slot2port_cisco'],vlan=script_var['vlan1'])
                self.ssx.cmd("end")
                self.ssx.cmd("conf")
                self.ssx.cmd("no port eth %s"%script_var['intf1_port'])
                self.ssx.cmd("port ethernet %s dot1q"%script_var['intf1_port'])
                self.ssx.cmd("vlan %s"%script_var['vlan1'])
                self.ssx.cmd("bind interface intf1 %s"%script_var['context_name'])
                self.ssx.cmd("exit")
                self.ssx.cmd("exit")
                self.ssx.cmd("enable")
                self.ssx.cmd("end")

            if testStep=="untaggedPort" :
                self.myLog.info("\n\n #*50")
                self.myLog.info("\n\n Repeating Test with untagged Port \n\n")
                self.myLog.info("#*50\n\n")
                self.myLog.info("BY DEFAULT VLAN 1 IS UNTAGGED ON CISCO SO USING THE SAME ID AS UNTAGGED VLAN ID")
                # Clearing CISCO interface configurations
                self.myLog.info("\n Clearing CISCO interface configurations \n")
                self.cisco.cmd("no interface vlan %s"%script_var['vlan1'])
                self.cisco.cmd("end")

                self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")

                self.cisco.clear_interface_config(intf=script_var['slot2port_cisco'])
                self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")
                self.cisco.configure_ipv4_vlan_interface(ip_addr=script_var['intf2_ip_mask'],
                  intf=script_var['slot2port_cisco'],vlan=1)
                self.ssx.cmd("end")
                self.ssx.cmd("conf")
                self.ssx.cmd("no port eth %s"%script_var['intf1_port'])
                self.ssx.cmd("port ethernet %s dot1q"%script_var['intf1_port'])
                self.ssx.cmd("vlan 1 untag")
                self.ssx.cmd("bind interface intf1 %s"%script_var['context_name'])
                self.ssx.cmd("exit")
                self.ssx.cmd("exit")
                self.ssx.cmd("enable")
                self.ssx.cmd("end")

            self.cisco.cmd("conf t")
            self.cisco.cmd("router bgp %s"%script_var['auto_no2'])
            self.cisco.cmd("no synchronization")
            self.cisco.cmd("bgp log-neighbor-changes")
            self.cisco.cmd("neighbor %s remote-as %s"%(script_var['intf1_ip'],script_var['auto_no1']))
            self.cisco.cmd("neighbor %s activate "%script_var['intf1_ip'])
            self.cisco.cmd("no auto-summary")
            self.cisco.cmd("end")
            self.ssx.cmd("end")
            #Changing context from local
            self.ssx.cmd("context %s"%script_var['context_name'])
	
    	    # Verifying the BGP Summary and Neighbor information.
   	    self.myLog.output("Delay is given for summarization and bgp messages exchange")
 	    time.sleep(60)
	    bgp = self.ssx.cmd("show ip bgp summary")
	    self.myLog.output("BGP Summary on context1 \n %s \n"%bgp)
	    neighbor = self.ssx.cmd("show ip bgp neighbor")
	    self.myLog.output("BGP neighbors on context1 \n %s \n"%neighbor)
	    neighbor_state = self.ssx.cmd("show ip bgp neighbors | grep -i \"bgp state\"")
	    self.failIf(int(bgp.splitlines()[5].split()[3]) == 0 , "BGP message is not recieved from other end router")
	    self.failIf("Established" not in "%s"%neighbor_state,"Test Failed FOR %s"%testStep)
       
        # Verifying the BGP is not Flapping.
        self.myLog.output("Verifying the BGP neighbourship is not Flapping.")
        neighbor = self.ssx.cmd("show ip bgp neighbor | grep -i \"bgp state\"")
        upTimeBefWait = int(neighbor.split()[-1].split(":")[1][:2])           
        self.myLog.output("Wait for 10 mins")
        timeToWait = 2
        time.sleep(timeToWait*60)
        upTimeAftWait = upTimeBefWait + timeToWait
        neighbor = self.ssx.cmd("show ip bgp neighbor | grep -i \"bgp state\"")
        self.failIf("Established" not in "%s"%neighbor_state,"Test Failed after sometime due to BGP neighbourship is Flapping")
        uptime = neighbor.split()[-1].split(":")[1][:2]
        self.failIf(uptime < upTimeAftWait , "Test Failed : OBSERVED BGP neighbourship Falpped")

        self.myLog.info("\n Clearing CISCO/SSX interface configurations at the end of test case\n")
        self.cisco.cmd("end")
        self.cisco.cmd("config t")
        self.cisco.cmd("no interface vlan %s"%script_var['vlan1'])
        self.cisco.cmd("no interface vlan 1")
        self.cisco.cmd("end")
        self.ssx.cmd("end")
        self.ssx.cmd("conf")
        self.ssx.cmd("no port eth %s"%script_var['intf1_port'])
        self.ssx.cmd("no context %s"%script_var['context_name'])
        self.ssx.cmd("exit")
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("BGP_BASIC.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_BGP_BASIC)
        test_runner(stream=sys.stdout).run(suite)


