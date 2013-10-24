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

DESCRIPTION:To verify SSX (relay agent) clears relay counters for a particular server. 
TEST PLAN: DHCP Test plans
TEST CASE ID: DHCP-FUN-REL-021

TOPOLOGY DIAGRAM:

	--------------------------------------------------------------------------------
       |		LINUX	                         SSX	 			|
       |         Trans  IP = 2.1.1.1/24			 TransIP = 2.1.1.2/24		|
       |                               -------------->                           	|
       |                     ETH1                                   Port 3/0		|
         --------------------------------------------------------------------------------

HOW TO RUN:python2.5 DHCP-FUN-REL-021.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:himanshu@primesoftsolutionsinc.com

"""
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from Linux import *
from dhcp import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *

#import dhcp_config and topo file
from dhcp_config import *
from  topo import *

class test_DHCP_FUN_021(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1 = Linux(linux1["ip_addr"])
	self.linux2 = Linux(linux2["ip_addr"])
	self.linux1.telnet()
	self.linux2.telnet()
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.linux1.close()
	self.linux2.close()

    def test_DHCP_FUN_021(self):

        self.myLog.output("\n**********start the test**************\n")

	             #vgroup b/w SSX and linux.
        #vg_output1 = vgroup_new(topo1[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

	# Push SSX config
        self.ssx.config_from_string(script_var['DHCP_FUN_021'])

        #configure ip interface on linux machine
        self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['infc_server1_ip_addr/mask'])

        #adding route 
        self.linux1.add_route(script_var['ssx_client_ip_mask'],script_var['ssx_server1_ip_addr'],p1_ssx_linux1[1])

        #moving to DHCP server directory and writing configuration into configuration file. 
        self.linux1.cmd("cd /dhcp-4.0.0b3/server/")
        self.linux1.cmd("sudo rm -f  dhcpd.conf")
        self.linux1.write_to_file(script_var['fun_004_dhcpserver1'],"dhcpd.conf","/dhcp-4.0.0b3/server/")
		
	#killing jobs on server regarding dhcp 
        self.linux1.cmd("sudo pkill dhcpd")
        self.linux1.cmd("sudo pkill dhclient")
		
	#initiating dhcp server 
        op_client_cmd = self.linux1.cmd("sudo ./dhcpd -cf dhcpd.conf -lf le %s"%p1_ssx_linux1[1])

	#killing jobs on client regarding dhcp
        self.linux2.cmd("sudo pkill dhclient")
        self.linux2.cmd("sudo pkill dhcpd")
        self.linux2.cmd("sudo pkill dhclient")
        self.linux2.cmd("cd /dhcp-4.0.0b3/")
        self.linux2.cmd("sudo chmod 777 client")
        self.linux2.cmd("cd client")

	#changing context on SSX and clearing and displating counters on SSX. 
	self.ssx.cmd("context %s"%script_var['context_name'])
	self.myLog.output("\n DHCP counters before relaying a message to DHCP server:\n%s\n"%self.ssx.cmd("show dhcp counters"))

	#Initiate dhcp client inorder to get ip address from address pool.
	self.linux2.cmd("sudo ./dhclient %s"%p1_ssx_linux2[1],timeout = 100)
	
	self.myLog.output("\nDHCP counters after relaying a message to DHCP server:\n%s\n"%self.ssx.cmd("show dhcp counters")	)
	self.ssx.cmd("clear dhcp counters")
	self.myLog.output("\n DHCP counters after clearing counters of dhcp:\n%s\n"%self.ssx.cmd("show dhcp counters") )

	#Capturing the incremented dhcp counters of server,after clearing.
	Server_out = self.ssx.cmd("show dhcp counters | grep server1")
	self.failUnless((int(Server_out.split()[3]) == 0)& (int(Server_out.split()[5]) ==0),"TEST FAILED")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


	      	   
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_DHCP_FUN_021)
    test_runner().run(suite)

