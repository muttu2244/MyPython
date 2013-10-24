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

DESCRIPTION: Verify ACL functionality for IGMP traffic through port when inbound and outbound ACLs applied to port [Deny for inbound and Deny for outbound]
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUNC_099.py

HOW TO RUN:python2.5 ACL_FUNC_099
AUTHOR: smath@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
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
from glcr import *
from CISCO import *
from vlan import *
from tunnel import *
from lanlan import *
from ike import *

#import config and topo file
from config import *
from topo import *


class test_ACL_FUNC_099(test_case):
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
	#self.ssx.configcmd("no context %s"%script_var['context_name'])
       

	# Connection To CISCO
        self.myLog.info("Connecting to the cisco ")
        self.myLog.debug("has the IP of: %s" % cisco["ip_addr"])
        self.cisco = CISCO(cisco["ip_addr"])
        self.cisco.console(cisco["ip_addr"],username="stoke", password="stoke")


	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

    def tearDown(self):
	'''	
	# Stop the client
        self.linux.cmd("ike reset")
        time.sleep(10)
        self.linux.cmd("exit")	
	'''
        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
        self.linux1.close()

	
    def cisco_linux_config(self):

        self.myLog.output("\n**********start the test**************\n")

        ########################################################################
        #  SSX  - RESPONDER
        ########################################################################
        Card_Reset = 0
        Card_Restart = 0
        #self.myLog.info("Verify the GLC-R enabled or not on SSX")
        status = verify_glcr_status(self.ssx)
        if status == 1:
            self.myLog.output("Device is not configured for GLC Redundancy\nConfigure the System for GLC-R, needs reboot\n")
            set_device_to_glcr(self.ssx)
        #Get the GLCR Status
        self.myLog.info("Get the GLCR Status")
        op = get_glcr_status(self.ssx)
        if int(op['standby']) != 4:
            self.myLog.error("4th card is not Standby card - Switching Back")
            #self.ssx.reload_device(timeout=200)
	    self.ssx.cmd("system glc-switchback")
            Card_Reset = Card_Reset + 1

        #clear prev logs and Enable the logs
        self.myLog.info("***************** Clear and Enable Logs ***********************")
        self.ssx.cmd("no debug all")
        self.ssx.cmd("clear log debug")
        self.ssx.cmd("debug module countd all")
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        self.ssx.cmd("debug module tunmgr all")
        self.ssx.cmd("end")

        self.myLog.output("\n********** Configuring SSX Responder **************\n")
        # Push SSX Common config
        self.ssx.config_from_string(script_var['test_ACL_Func_Main'])

		# Clearing CISCO interface configurations
        self.myLog.info("\n Clearing CISCO interface configurations \n")

        self.cisco.clear_interface_config(intf=topo.p_cisco_linux[0])
        self.cisco.clear_interface_config(intf=topo.p_cisco_linux1[0])
        self.cisco.clear_interface_config(intf=topo.p_tr_active2_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=topo.p_tr_stdby2_ssx_cisco_slot4[1])
        self.cisco.clear_interface_config(intf=topo.p_sr_active2_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=topo.p_sr_stdby2_ssx_cisco_slot4[1])
        self.cisco.clear_interface_config(intf=topo.p_tr_active1_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=topo.p_tr_stdby1_ssx_cisco_slot4[1])
        self.cisco.clear_interface_config(intf=topo.p_sr_active1_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=topo.p_sr_stdby1_ssx_cisco_slot4[1])

        self.myLog.info("Configuring Cisco Ports which are On DUT Slot2&4 side")
        self.cisco.configure_ipv4_vlan_interface(ip_addr=script_var['cisco_active_slot2_ip_mask'],
                  intf=script_var['p_tr_active1_ssx_cisco_slot2'],vlan=script_var['tr_Active1_vlan'])

        self.cisco.configure_ipv4_vlan_interface(ip_addr=script_var['cisco_standby_slot4_ip_mask'],
                  intf=script_var['p_tr_stdby1_ssx_cisco_slot4'],vlan=script_var['tr_Stdby1_vlan'])


        self.cisco.configure_ipv4_interface(ip_addr=script_var['cisco_service_slot2_ip_mask'],
                  intf=script_var['p_sr_active1_ssx_cisco_slot3'],vrf="service")

        self.cisco.configure_ipv4_interface(ip_addr=script_var['cisco_active_standby_slot2_ip_mask'],
                  intf=script_var['p_sr_stdby1_ssx_cisco_slot4'],vrf="service")

        self.cisco.configure_ipv4_interface(ip_addr=script_var['ciscoxpVpnHstIpMsk'],
                  intf=p_cisco_linux[0])

        self.cisco.configure_ipv4_interface(ip_addr=script_var['cisco_intf_ipmask'],
                  intf=p_cisco_linux1[0],vrf="service")

	self.myLog.output("\n**********Configuring Linux Interfaces***********\n")
        self.linux.cmd("sudo /sbin/ifconfig %s %s"%(topo.p_cisco_linux[1],
                                    script_var['xpVpnHstIpMsk']))

        self.myLog.output("\n**********Adding Routes On Linux***********\n")
        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['tnLpNw'],script_var['ciscoxpVpnHstIp']))
        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['tnIfNw'],script_var['ciscoxpVpnHstIp']))

        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['active_slot2__mask'],script_var['ciscoxpVpnHstIp']))

        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['active_slot4_mask'],script_var['ciscoxpVpnHstIp']))

        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['linux1_route_mask'],script_var['ciscoxpVpnHstIp']))


        self.linux1.cmd("sudo /sbin/ifconfig %s %s"%(topo.p_cisco_linux1[1],
                                    script_var['linux1_intf_ip_mask']))

        self.myLog.output("\n**********Adding Routes On Linux***********\n")
        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['linux_nw'],script_var['linux1_nexthop_ip']))

        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['serv_slot2_mask'],script_var['linux1_nexthop_ip']))

        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['serv_slot4_mask'],script_var['linux1_nexthop_ip']))

        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['ip_pool_mask'],script_var['linux1_nexthop_ip']))

        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['tnLpNw'],script_var['linux1_nexthop_ip']))


        self.myLog.info("**************** End Of Linux configuration **********")

	# Add routes on CISCO
        self.myLog.info("Configuring Cisco with routes")
        self.cisco.cmd("vlan database")
        self.cisco.cmd("vlan 1000")
        self.cisco.cmd("vlan 1001")
        self.cisco.cmd("exit")
        self.cisco.cmd("config ter")
        self.cisco.cmd("ip vrf service")
        self.cisco.cmd("exit")
        self.cisco.cmd("ip route %s %s 10"%(script_var['tnLpBkIpMsk1'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route %s %s 20"%(script_var['tnLpBkIpMsk1'],script_var['standby_slot4_ip']))
        self.cisco.cmd("ip route %s %s 10"%(script_var['tnIFIpMsk1'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route %s %s 20"%(script_var['tnIFIpMsk1'],script_var['standby_slot4_ip']))
        self.cisco.cmd("ip route %s %s %s"%(script_var['sess_loopback1'],script_var['ip_netmask'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['xpIfMsk'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['xpIfMsk'],script_var['service_standby_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['lanIp_mask'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['lanIp_mask'],script_var['standby_slot4_ip']))
        self.cisco.cmd("ip route vrf service %s %s 100"%(script_var['tnLpBkIpMsk1'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 200"%(script_var['tnLpBkIpMsk1'],script_var['service_standby_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 100"%(script_var['ip_pool_ipmask'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 200"%(script_var['ip_pool_ipmask'],script_var['service_standby_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['linux1Msk'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['linux1Msk'],script_var['standby_slot4_ip']))

        self.myLog.info("**************** End Of CISCO configuration*************")

	
    def tunnelUp(self):
        # Push xpress vpn config
        self.linux.write_to_file(script_var['fun_001_xpressvpn'],"autoexec.cfg","/xpm/")

        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo /sbin/rmmod xpressvpn.ko")
        self.linux.cmd("sudo /sbin/insmod xpressvpn.ko")
        op_client_cmd = self.linux.cmd("sudo ./start_ike")
        time.sleep(10)

        # Check SA in SSX with the remote (11.11.11.11)
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpVpnHstIp'])
        self.failIf("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")


        # send traffic through session
        # Initiate Ping through tunnel from xpressent
        # Get the IP Assined to Client
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['tnLpBkIp'],"500","4")
        self.failIfEqual(op_ping,False,"Ping through tunnel failed")


        #step1 is for checking tunnel state and ping traffic after bringup tunnel
        self.myLog.info("\nStep1: Checking tunnel state and ping traffic after bringup tunnel\n")
        #Check Tunnel State
	output_dut = check_tunnel_state(self.ssx ,tunnel = script_var['tunnel_name'])
        self.failIfEqual(output_dut,False , "Tunnels are Down")

    
    def befNAftSwitchOver(self):
	#clear the acl counters before the traffic is sent
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
	
	
	self.ssx.config_from_string(script_var['deny_in_igmp_port'])

        #op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['linux1'],"500","4")
	op_ping = self.linux.ping(script_var['active_slot2_ip'])
        self.failIfEqual(op_ping,True,"Ping through tunnel must fail after acl applied")

        acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","5","0","0","0")
        self.failIf(acl_cntrs!=True , "Deny Acl counters are not incrementing ")

	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	#Removing the Acl applied
        self.ssx.cmd("config")
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("no ip access-list %s"%(script_var['acl_name']))
        self.ssx.cmd("end")


	self.ssx.config_from_string(script_var['deny_out_igmp_port'])

        #op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['linux1'],"500","4")
        self.failIfEqual(op_ping,True,"Ping through tunnel must fail after acl applied")

        acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","0","5")
        self.failIf(acl_cntrs!=True , "Permit Acl counters are not incrementing ")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	
	#Removing the Acl applied
	self.ssx.cmd("config")
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("no ip access-list %s"%(script_var['acl_name']))
        self.ssx.cmd("end")



    def test_ACL_FUNC_099(self):
	
	Card_Reset = 0
        Card_Restart = 0

	#calling the function to configure the cisco and linux
        self.cisco_linux_config()
	
	#calling the tunnelUp function
	#self.tunnelUp()	

	#changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear tunnel counters")
        time.sleep(5)
	
	
	#calling the function before the switchover
	self.befNAftSwitchOver()

	# Reload the card
        self.myLog.info("********** Reload Card *****************")
        reload_card(self.ssx, port=topo.p_tr_active1_ssx_cisco_slot2[0])
        time.sleep(20)
        #ping operation after acl applied
        #op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['linux1'],"500","25")
	op_ping = self.linux.ping(script_var['standby_slot4_ip'])
        self.failIfEqual(op_ping,False,"Ping through tunnel during reload")
        #Wait for Card To Come Back Up
        self.ssx.wait4cards()
        Card_Reset = Card_Reset + 1
        time.sleep(10)

        #calling the function after switch over
        self.befNAftSwitchOver()

        #Executing the switchback command
        self.myLog.info("********* execute system glc-switchback command *************")
        self.ssx.cmd("system glc-switchback")
        time.sleep(20)
        #ping operation after acl applied
        #op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['linux1'],"500","25")
	op_ping = self.linux.ping(script_var['active_slot2_ip'])
        self.failIfEqual(op_ping,False,"Ping through tunnel failed during switchback")

        Card_Restart = Card_Restart + 1
        #Wait for Card To Come Back Up
        self.ssx.wait4cards()
        # Wait for the card 4 to compleate the synchronization
        time.sleep(40)

        #calling the function after switch back
        self.befNAftSwitchOver()

	# Checking SSX Health 
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs,Card_Reset=2,Card_Restart=1), "Platform is not healthy")

if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUNC_099)
        test_runner().run(suite)
