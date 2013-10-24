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

DESCRIPTION: To Verify all combinations of tos (16 service levels) and Precedence (8) when outbound ACL is applied to port-interface. Repeat the test case when ACL is applied to session 
TEST PLAN :ACL Test plans
TEST CASES:ACL_FUN_023

TOPOLOGY: 

Ingress : Linux 1(17.1.1.1/24) -> 3/0 (17.1.1.2/24) SSX 
Egress : SSX 2/0 (16.1.1.2/24) -> Linux 2(16.1.1.1/24)



HOW TO RUN : python2.5 ACL_FUN_023.ACL
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



class test_ACL_FUN_023(test_case):
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


    def test_ACL_FUN_023(self):


	# Push SSX config
	#elf.ssx.config_from_string(script_var['ACL_FUN_023'])
	self.linux1.configure_ip_interface(p1_ssx_linux2[1], script_var['linux_phy_iface2_ip_mask'])
	self.linux.cmd("sudo /sbin/route add -net %s gw %s" %(script_var['client1_route'],script_var['client1_gateway']))
	self.linux1.cmd("sudo /sbin/route add -net %s gw %s" %(script_var['client2_route'],script_var['client2_gateway']))

	self.ssx.config_from_string(script_var['ACL_FUN_023'])
	

        #changing context and clear port counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        #self.ssx.cmd("clear ip access-list name subacl counters")
	#time.sleep(5)
        self.linux.cmd("sudo ping %s -c 5 "%(script_var['linux_phy_iface2_ip']))

        
	for precedence in prec_list :
		for tos in tos_list :
			self.ssx.config_from_string("context %s" %(script_var['context_name']))
			self.ssx.config_from_string("no ip access-list subacl")
			self.ssx.config_from_string("ip access-list subacl")
			self.ssx.config_from_string("permit icmp any any precedence %s tos %s"%(precedence,tos))
			self.ssx.config_from_string("exit")
			self.ssx.config_from_string("exit")
			#self.ssx.config_from_string("end")
			self.ssx.config_from_string("port ethernet %s"%(script_var['p1_ssx1_xpressvpn2']))
			self.ssx.config_from_string("bind interface to_linux2 %s"%(script_var['context_name']))
			self.ssx.config_from_string("ip access-group out name subacl")
			self.ssx.config_from_string("end")

			#self.ssx.cmd("show conf")
			time.sleep(5)
			tos_bin=int2bin(self.ssx,tos,3)
			pre_bin=int2bin(self.ssx,precedence,3)
			tos_byte=hex(int(str(pre_bin)+str(tos_bin)+"00",2))
			umatch_tos=int(tos)+3%7
			umatch_pre=int(precedence)+3%7
			ntos_bin=int2bin(self.ssx,umatch_tos,3)
			npre_bin=int2bin(self.ssx,umatch_pre,3)
			ntos_byte=hex(int(str(npre_bin)+str(ntos_bin)+"00",2))
			
			#Clearing ACL Counters
			self.ssx.cmd("clear ip access-list name subacl counters")
			time.sleep(5)
			#Sending Icmp packets with Matchin Tos Byte to pass thru 
			self.linux.cmd("sudo ping %s -c 5 -Q %s "%(script_var['linux_phy_iface2_ip'],tos_byte),timeout=40)
		        time.sleep(5)

			output = verify_access_list_counters(self.ssx, permit_out="5")
			self.failUnless(output, "TOS based permit Failed")
			"""
			result=self.ssx.cmd("show ip access-list name subacl counters")
			result=result.split('\n')
			result=result[2]
			
			result=result.split('       ')
			output=int(result[4])
		        self.failIfEqual(output,0,"Packet Filtering Based on TOS unsuccessful")
			"""
			#Clearing ACL Counters
			self.ssx.cmd("clear ip access-list name subacl counters")
		        time.sleep(5)
		        #Sending Icmp packets with NonMatching TOS Byte to be filtered thru 
			self.linux.cmd("sudo ping %s -c 5 -Q %s "%(script_var['linux_phy_iface2_ip'],ntos_byte),timeout=40)
		        time.sleep(5)

			output = verify_access_list_counters(self.ssx, deny_out="5")
                        self.failUnless(output, "TOS based deny Failed")
			"""
                        result=self.ssx.cmd("show ip access-list name subacl counters")
                        result=result.split('\n')
                        result=result[2]

                        result=result.split('       ')
                        output=int(result[5])
		        self.failIfEqual(output,0,"Packet Filtering Based on TOS Unsuccessful")

			"""
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
	#vgroup_new(vlan_cfg_acl)
	#vgroup_new(vlan_cfg_acl2)
        suite.addTest(test_ACL_FUN_023)
        test_runner(stream = sys.stdout).run(suite)

