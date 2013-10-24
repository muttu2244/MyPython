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

DESCRIPTION:To Verify SSX performs phase 1 rekeys successfully when PERMIT UDP is applied to port  
TEST PLAN: ACL Test plans
TEST CASES:GRED_ACL_TUN_FUN_009.py

HOW TO RUN:python2.5 GRED_ACL_TUN_FUN_009
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


class test_GRED_ACL_TUN_FUN_009(test_case):
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
	
	# Stop the client
        self.linux.cmd("ike reset")
        time.sleep(10)
        self.linux.cmd("exit")	

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
        self.ssx.config_from_string(script_var['test_GRED_ACL_TUN_FUN_001'])

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

        self.linux1.cmd("sudo /sbin/ifconfig %s %s"%(topo.p_cisco_linux1[1],
                                    script_var['linux1_intf_ip_mask']))

	self.myLog.output("\n**********Adding Routes On Linux***********\n")
        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['linux_nw'],script_var['linux1_nexthop_ip']))
        self.myLog.info("**************** End Of Linux configuration **********")

         # Add routes on CISCO
        self.myLog.info("Configuring Cisco with routes")
        self.cisco.cmd("config ter")
        self.cisco.cmd("ip route %s %s 10"%(script_var['tnLpBkIpMsk1'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route %s %s 20"%(script_var['tnLpBkIpMsk1'],script_var['standby_slot4_ip']))
        self.cisco.cmd("ip route %s %s 10"%(script_var['tnIFIpMsk1'],script_var['active_slot2_ip']))
        self.cisco.cmd("ip route %s %s 20"%(script_var['tnIFIpMsk1'],script_var['standby_slot4_ip']))

        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['xpVpnHstIFMsk'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['xpVpnHstIFMsk'],script_var['service_standby_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['lanIp_mask'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['lanIp_mask'],script_var['service_standby_slot2_ip']))



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
        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")


        # send traffic through session
        # Initiate Ping through tunnel from xpressent
        # Get the IP Assined to Client
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['tnLpBkIp'],"500","4")
        self.failUnless(op_ping,"Ping through tunnel failed")


        #step1 is for checking tunnel state and ping traffic after bringup tunnel
        self.myLog.info("\nStep1: Checking tunnel state and ping traffic after bringup tunnel\n")
        #Check Tunnel State
        #output_dut = check_tunnel_state(self.ssx , count="1")
	output_dut = check_tunnel_state(self.ssx ,tunnel = script_var['tunnel_name'])
        self.failUnless(output_dut , "Tunnels Have Gone Down")

    def phase1Rekey(self):
	# Get the ph1 negotiation initial count
        self.failUnless(sa_check(self.ssx,script_var['xpVpnHstIp']))
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpVpnHstIp'])
        initial_neg_count = int(ssx_show_op['ike_sa_negotiation_count'])

        self.myLog.output("\n\n******going to sleep for %s***\n\n"%ssx_show_op['ike_sa_time_remaining'])
        time.sleep(int(ssx_show_op['ike_sa_time_remaining']))

        #time.sleep(10)

        # Check delete sa  notify msg in logs
        op_debug = verify_in_debug(self.ssx,"SA_DELETE")
        self.failUnless(op_debug, "deletion of old sa Failed")

        # Get the ph1 negotiation final count
        self.failUnless(sa_check(self.ssx,script_var['xpVpnHstIp']))
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpVpnHstIp'])
        final_neg_count = int(ssx_show_op['ike_sa_negotiation_count'])

        # Check the negotiation happened after ph1 ssx_lifetime
        self.failUnless((final_neg_count - initial_neg_count) == 1,"Negotiation count not increased")

    def phase2Rekey(self):
	ssx_ph2_sa_lifetime = 60
	# Get the ph1 negotiation initial count
        self.failUnless(sa_check(self.ssx,script_var['xpVpnHstIp']))
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpVpnHstIp'])
        initial_neg_count = int(ssx_show_op['child_sa_negotiation_count'])

        self.myLog.output("\n\n******Sleeping for 60(sa life) + 5 seconds*******\n\n")
        #time.sleep(int(ssx_show_op['ssx_ph2_sa_lifetime'])+5)  # +5 Delay issue
        time.sleep(ssx_ph2_sa_lifetime+5)  # +5 Delay issue

        # Check delete sa  notify msg in logs
        op_debug = verify_in_debug(self.ssx,"SA_DELETE")
        self.failUnless(op_debug, "deletion of old sa Failed")

        # Check Rekey notify msg in logs
        op_debug = verify_in_debug(self.ssx,"REKEY_SA")
        self.failUnless(op_debug, "Rekey Failed")

        # Get the ph1 negotiation final count
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpVpnHstIp'])
        final_neg_count = int(ssx_show_op['child_sa_negotiation_count'])

        # Check the negotiation happened after ph1 ssx_lifetime
        self.failUnless((final_neg_count - initial_neg_count) == 1,"Negotiation count not increased")



    def dpdTrans(self):
	
	#Kill existing session
        #self.linux.cmd("exit")

        self.myLog.output("\n Sleep Until DPD Interval\n")
        #Sleep until DPD interval
        time.sleep(65)

        #justFun = self.ssx.cmd("show tunnel | grep down | count")
        #print "$$$$$$$$$$$$$$JUSTFUN %s$$$$$$$$$$$$$$$$$$" %justFun

        #Check for first DPD messages in debug
        op_log_debug = self.ssx.cmd("show log debug | grep DPD")
        print "*******************************op_log_debug %s &&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n" %(op_log_debug)
        self.failUnless(op_log_debug, "DPD Message No Sent At Interval defined")

        #clear log for second message
        self.ssx.cmd("clear log debug")

        self.myLog.output("\n Sleep Until DPD Interval\n")

        #Sleep until DPD interval
        time.sleep(30)

        #Check for second DPD messages in debug
        op_log_debug=self.ssx.cmd("show log debug | grep DPD")
        self.failUnless(op_log_debug, "DPD Message No Sent At Interval defined")

        #check if session is killed
        output=self.ssx.cmd("show session")
        if output :
                output='0'
        else :
                output='1'

        self.failUnless(output,"Session Not Killed After DPD")


    def befNAftSwitchOver(self):
	#ping after acl applied
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['linux1'],"500","4")
        self.failIfEqual(op_ping,True,"Ping through tunnel must fail after acl applied")

        tun_cntrs = verify_tunnel_counters_with_name(self.ssx,script_var['tunnel_name']) 
        self.failIf(tun_cntrs != 0 , "Traffic is not via tunnel!!No tunnel counters")
	
	#calling the phase1 Rekey function
	self.phase1Rekey()	

	#Removing the Acl applied
        self.ssx.cmd("config")
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("no ip access-list %s"%(script_var['acl_name']))
        self.ssx.cmd("end")
	
	# Stop the client
        self.linux.cmd("ike reset")
        time.sleep(10)
        self.linux.cmd("exit")



    def test_GRED_ACL_TUN_FUN_009(self):
	
	Card_Reset = 0
        Card_Restart = 0

	#calling the function to configure the cisco and linux
        self.cisco_linux_config()

	
	# Push permitUdp config
        self.ssx.config_from_string(script_var['deny_udp'])
	
	#calling the function to bring up the tunnel
	self.tunnelUp()

	#calling the function before switch over
	self.befNAftSwitchOver()
	
	#calling the function to bring up the tunnel
        self.tunnelUp()
	
	#calling the phase2 Rekey function
        self.phase2Rekey()

	#calling the DPD transactions
	#self.dpdTrans()	

	# Reload the card
	self.myLog.info("********** Reload Card *****************")
        reload_card(self.ssx, port=topo.p_tr_active1_ssx_cisco_slot2[0])
        #Wait for Card To Come Back Up
        self.ssx.wait4cards()
        Card_Reset = Card_Reset + 1
        time.sleep(10)
	
	# Push permitUdp config
        self.ssx.config_from_string(script_var['deny_udp'])	

	#calling the function after switch over
	self.befNAftSwitchOver()

	#calling the function to bring up the tunnel
        self.tunnelUp()

        #calling the phase2 Rekey function
        self.phase2Rekey()

        #calling the DPD transactions
        #self.dpdTrans()

	
	#Executing the switchback command
	self.myLog.info("********* execute system glc-switchback command *************")
        self.ssx.cmd("system glc-switchback")
        Card_Restart = Card_Restart + 1
        #Wait for Card To Come Back Up
        self.ssx.wait4cards()
        # Wait for the card 4 to compleate the synchronization
        time.sleep(40)
	
	# Push permitUdp config
        self.ssx.config_from_string(script_var['deny_udp'])

	#calling the function after switch back
	self.befNAftSwitchOver()
	
	#calling the function to bring up the tunnel
        self.tunnelUp()

        #calling the phase2 Rekey function
        self.phase2Rekey()

        #calling the DPD transactions
        #self.dpdTrans()

	# Checking SSX Health 
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs,Card_Reset=1,Card_Restart=1), "Platform is not healthy")

if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_GRED_ACL_TUN_FUN_009)
        test_runner().run(suite)

