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

DESCRIPTION: To verify Permit/deny rules for all options
TEST PLAN: System Test
TEST CASES:ACL_SYS_001

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |     
       |                 ETH1                                    Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  jayanth@stoke.com
        
REVIEWER:

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

from misc import vgroup_new

#import configs file
from config_sys import *
from topo_sys import *
#import private libraries
from ike import *
from nemesis import *


class test_ACL_SYS_001(test_case):
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

    def test_ACL_SYS_001(self):
	
	# Push SSX config
        self.ssx.config_from_string(script_var['ACL_SYS_001'])

	#Configure Ip Interface on Linux
	self.linux.cmd("sudo /sbin/ifconfig %s %s"%(script_var['linux_iface'], script_var['linux_phy_iface_ip_mask']))

	for feature in featureList :
		# Checking permit conditions
		self.myLog.output("Checking Permit Condition For %s"%feature)
		self.ssx.config_from_string("context %s"%script_var['context_name'])
		self.ssx.config_from_string("no ip access-list subacl")
		self.ssx.config_from_string("ip access-list subacl")
		self.ssx.config_from_string("permit %s any any"%feature)	
		self.ssx.config_from_string("exit")
		self.ssx.config_from_string("exit")
		self.ssx.config_from_string("port ethernet %s"%script_var['ssx_port'])
		self.ssx.config_from_string("bind interface to_host %s"%script_var['context_name'])
		self.ssx.config_from_string("ip access-group in name subacl")
		self.ssx.config_from_string("exit")
		self.ssx.config_from_string("service ipsec")
		self.ssx.config_from_string("enable")
		self.ssx.config_from_string("end")
		
		#Changing Context and Clearing Counters	
		self.ssx.cmd("context %s"%script_var['context_name'])
		self.ssx.cmd("clear ip counters")
		self.ssx.cmd("clear ip access-list name subacl counters")
		self.ssx.cmd("show ip access-list name subacl counters")
		
		if feature == 'udp' :
			#generate UDP Packets from Linux
			output = send_udp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
			self.failUnless(output, "Nemesis Should Be Installed To Test")
			output = verify_access_list_counters(self.ssx, permit_in="5")
			self.failUnless(output, "Permit Counters For UDP Did Not Increment")
			self.myLog.output("Permit Condition For UDP Passed")
		elif feature == 'icmp' :
			#generate ICMP Packets from Linux
                        output = send_icmp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, permit_in="5")
                        self.failUnless(output, "Permit Counters For ICMP Did Not Increment")
			self.myLog.output("Permit Condition For ICMP passed")
	
		elif feature == 'tcp' :
			 #generate TCP packets from Linux
                        output = send_tcp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, permit_in="5")
                        self.failUnless(output, "Permit Counters For TCP Did Not Increment")
			self.myLog.output("Permit Condition For TCP passed")
		else :
			#generate IGMP Packets from Linux
			output = send_igmp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
			self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, permit_in="5")
                        self.failUnless(output, "Permit Counters For IGMP Did Not Increment")
			self.myLog.output("Permit Condition For IGMP passed")

		#Checking Deny Conditions
		self.myLog.output("Checking Deny Condition For %s"%feature)
		self.ssx.config_from_string("context %s"%script_var['context_name'])
                self.ssx.config_from_string("no ip access-list subacl")
                self.ssx.config_from_string("ip access-list subacl")
                self.ssx.config_from_string("deny %s any any"%feature)
                self.ssx.config_from_string("exit")
                self.ssx.config_from_string("exit")
                self.ssx.config_from_string("port ethernet %s"%script_var['ssx_port'])
                self.ssx.config_from_string("bind interface to_host %s"%script_var['context_name'])
                self.ssx.config_from_string("ip access-group in name subacl")
                self.ssx.config_from_string("exit")
                self.ssx.config_from_string("service ipsec")
                self.ssx.config_from_string("enable")
                self.ssx.config_from_string("end")

                #Changing Context and Clearing Counters 
                self.ssx.cmd("context %s"%script_var['context_name'])
                self.ssx.cmd("clear ip counters")
                self.ssx.cmd("clear ip access-list name subacl counters")
                self.ssx.cmd("show ip access-list name subacl counters")

                if feature == 'udp' :
                        #generate UDP Packets from Linux
                        output = send_udp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, deny_in="5")
                        self.failUnless(output, "Deny Counters For UDP Did Not Increment")
			self.myLog.output("Deny Condition For UDP passed")
                elif feature == 'icmp' :
                        #generate ICMP Packets from Linux
                        output = send_icmp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, deny_in="5")
                        self.failUnless(output, "Deny Counters For ICMP Did Not Increment")
			self.myLog.output("Deny Condition For ICMP passed")

                elif feature == 'tcp' :
                         #generate TCP packets from Linux
                        output = send_tcp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx, deny_in="5")
                        self.failUnless(output, "Deny Counters For TCP Did Not Increment")
			self.myLog.output("Deny Condition For TCP passed")
                else :
                        #generate IGMP Packets from Linux
                        output = send_igmp_nemesis(self.linux, src=script_var['linux_phy_iface_ip'], dst=script_var['ssx_phy_iface_ip'], send_pkts="5", dev=script_var['linux_iface'])
                        self.failUnless(output, "Nemesis Should Be Installed To Test")
                        output = verify_access_list_counters(self.ssx,deny_in="5")
                        self.failUnless(output, "Deny Counters For IGMP Did Not Increment")
			self.myLog.output("Deny Condition For IGMP passed")



        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    vgroup_new(vlan_cfg_acl)
    suite = test_suite()
    suite.addTest(test_ACL_SYS_001)
    test_runner(stream = sys.stdout).run(suite)

	
