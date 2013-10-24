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

DESCRIPTION:Verify all ACL functionalities (ICMP, IGMP,TCP,UDP) in all directions of (INBOUND, OUTBOUND) for both (PERMIT, DENY) for TUNNEL, SESSION and PORTS
TEST PLAN: ACL Test plans
TEST CASES:ACL_Func.py

HOW TO RUN:python2.5 ACL_Func
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
#from configAll import *
from config import *
from topo import *


direction = ['in','out']
operation = ['deny','permit']  
protocols = ['icmp','igmp','tcp','udp','ip']
bridges	  = ['tunnel','session','port']

#aclList = [['deny_icmp','permit_icmp'],['deny_icmp_in','permit_icmp_out'],['permit_icmp','permit_icmp_out'],['deny_icmp','deny_icmp_in']]
	
aclTunnelList = ['deny_icmp_out','permit_icmp_in','deny_icmp_in', 'permit_icmp_out',\
		'deny_igmp_in',  'permit_igmp_in','deny_igmp_out','permit_igmp_out',\
		'deny_tcp_in',   'permit_tcp_in', 'deny_tcp_out', 'permit_tcp_out', \
		'deny_udp_out',  'deny_udp_in',  'permit_udp_out', 'permit_udp_in']

aclSessList = ['permit_icmp_sess_in','deny_icmp_sess_in',   'permit_icmp_sess_out','deny_icmp_sess_out',\
		'deny_igmp_sess_out','permit_igmp_sess_out','deny_igmp_sess_in',   'permit_igmp_sess_in',\
		'deny_tcp_sess_in',  'permit_tcp_sess_in',  'deny_tcp_sess_out',   'permit_tcp_sess_out',\
		'permit_udp_sess_in','deny_udp_sess_in',    'permit_udp_sess_out', 'deny_udp_sess_out']


#aclTunnelList = ['deny_icmp_out','permit_icmp_in',\
#		'deny_icmp_in', 'permit_icmp_out']
		
#aclSessList = ['permit_icmp_sess_in','deny_icmp_sess_in',\
#		'permit_icmp_sess_out','deny_icmp_sess_out']	

aclPortList = ['permit_in_icmp_port','permit_out_icmp_port','deny_in_icmp_port','deny_out_icmp_port',\
		'deny_out_igmp_port','deny_in_igmp_port','permit_out_igmp_port','permit_in_igmp_port',\
		'permit_in_tcp_port','permit_out_tcp_port','deny_out_tcp_port','deny_in_tcp_port',\
		'deny_in_udp_port','deny_out_udp_port','permit_in_udp_port','permit_out_udp_port']

#aclPortList = ['permit_in_icmp_port','permit_out_icmp_port','deny_in_icmp_port','deny_out_icmp_port']

rx_counter = 0 
tx_counter = 0

class test_ACL_Func(test_case):
    myLog = getLogger()
    def setUp(self):
	'''
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
	self.linux2=Linux(linux2['ip_addr'],linux2['user_name'],linux2['password'])
        self.ssx.telnet()
        self.linux.telnet()
        self.linux1.telnet()
	self.linux2.telnet()

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
	'''

    def tearDown(self):
	
	'''
	# Stop the client
        self.linux.cmd("ike reset")
        time.sleep(10)
        self.linux.cmd("exit")	

	self.linux1.cmd("sudo pkill radiusd")
	time.sleep(10)

	self.linux2.cmd("ike reset")
        time.sleep(10)
        self.linux2.cmd("exit")

	

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
        self.linux1.close()
	self.linux2.close()
	'''

    def setUpTunnel(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
        self.linux2=Linux(linux2['ip_addr'],linux2['user_name'],linux2['password'])
        self.ssx.telnet()
        self.linux.telnet()
        self.linux1.telnet()
        self.linux2.telnet()

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


    def setUpSession(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
        self.linux2=Linux(linux2['ip_addr'],linux2['user_name'],linux2['password'])
        self.ssx.telnet()
        self.linux.telnet()
        self.linux1.telnet()
        self.linux2.telnet()

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

	
    def tearDownTunnel(self):

        # Stop the client
        self.linux.cmd("ike reset")
        time.sleep(10)
        self.linux.cmd("exit")

        # Close the telnet session of SSX
        self.ssx.close()
        self.linux.close()
        self.linux1.close() 

    def tearDownSession(self):

        #self.linux1.cmd("sudo pkill radiusd")
        #time.sleep(10)

        #self.linux2.cmd("ike reset")
        #time.sleep(10)
        #self.linux2.cmd("exit")

        # Close the telnet session of SSX
        self.ssx.close()
        self.linux1.close()
        self.linux2.close()

	
    def cisco_linux_config(self):

        self.myLog.output("\n**********start the test**************\n")

        ########################################################################
        #  SSX  - RESPONDER
        ########################################################################
        #Card_Reset = 0
        #Card_Restart = 0
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

	'''
        self.myLog.output("\n********** Configuring SSX Responder **************\n")
        # Push SSX Common config
        self.ssx.config_from_string(script_var['test_ACL_Func_Main'])
	'''


	# Clearing CISCO interface configurations
        self.myLog.info("\n Clearing CISCO interface configurations \n")

        self.cisco.clear_interface_config(intf=topo.p_cisco_linux[0])
        self.cisco.clear_interface_config(intf=topo.p_cisco_linux1[0])
	self.cisco.clear_interface_config(intf=topo.p_cisco_linux2[0])
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

	self.cisco.configure_ipv4_interface(ip_addr=script_var['ciscoxpVpnSesHstIpMsk'],
                  intf=p_cisco_linux2[0])

        self.myLog.output("\n**********Configuring Linux Interfaces***********\n")
        self.linux.cmd("sudo /sbin/ifconfig %s %s"%(topo.p_cisco_linux[1],script_var['xpVpnHstIpMsk']))
	self.linux2.cmd("sudo /sbin/ifconfig %s %s"%(topo.p_cisco_linux2[1],script_var['xpVpnSesHstIpMsk']))

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

        self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['cisco_service_slot2_ip'],script_var['ciscoxpVpnHstIp']))

	self.linux2.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['tnLpNw'],script_var['ciscoxpVpnSesHstIp']))
        self.linux2.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['tnIfNw'],script_var['ciscoxpVpnSesHstIp']))
	
	self.linux2.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['loopbackMsk'],script_var['ciscoxpVpnSesHstIp']))
	
	self.linux2.cmd("sudo /sbin/route add -net %s gw %s"%(
          script_var['linux1_route_mask'],script_var['ciscoxpVpnSesHstIp']))	

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


	self.linux2.cmd("sudo /sbin/route add -net %s gw %s"%(
                script_var['linux2_route_mask'],script_var['linux1_nexthop_ip']))

        self.myLog.info("**************** End Of Linux configuration **********")

	self.myLog.output("\n**********Session Specific Routes***********\n")

        self.linux2.cmd("sudo /sbin/ip addr add dev %s %s/16 brd +"%(p_cisco_linux2[1],script_var['ip_pool']))
        self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(script_var['ip_pool_mask'],script_var['linux1_nexthop_ip']))
        self.cisco.cmd("ip route vrf service %s %s 10"%(script_var['ip_pool_ipmask'],script_var['service_slot2_ip']))
        self.cisco.cmd("ip route vrf service %s %s 20"%(script_var['ip_pool_ipmask'],script_var['service_standby_slot2_ip']))

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
        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")


        # send traffic through session
        # Initiate Ping through tunnel from xpressent
        # Get the IP Assined to Client
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['tnLpBkIp'],"500","4")
        self.failUnless(op_ping,"Ping through tunnel failed")


        #step1 is for checking tunnel state and ping traffic after bringup tunnel
        self.myLog.info("\nStep1: Checking tunnel state and ping traffic after bringup tunnel\n")
        #Check Tunnel State
        #output_dut = check_mytunnel_state(self.ssx ,script_var['tunnel_name'])
	output_dut = check_tunnel_state(self.ssx ,tunnel = script_var['tunnel_name'])
        self.failIfEqual(output_dut,False , "Tunnels Have Gone Down")
        
    def sessionUp(self):
        # Push xpress vpn config
	self.linux2.write_to_file(script_var['fun_011_xpressvpn'],"autoexec.cfg","/xpm/")
	#self.linux1.write_to_file(script_var['rad_users_acl_out'],"users","/a/radius1/etc/raddb/")
	self.linux1.cmd("cd %s" %script_var['radiusLoc'])
	op_client_cmd3 = self.linux1.cmd("sudo ./radiusd ")
	time.sleep(10)

	self.linux2.cmd("cd /xpm")
        self.linux2.cmd("sudo /sbin/rmmod xpressvpn.ko")
        self.linux2.cmd("sudo /sbin/insmod xpressvpn.ko")
        op_client_cmd2 = self.linux2.cmd("sudo ./start_ike")
        time.sleep(10)	


	# Check SA in SSX with the remote (33.33.33.33)
        ssx_show_op2 = parse_show_ike_session_detail(self.ssx,script_var['xpVpnSesHstIp'])
        self.failUnless("ESTABLISHED" in ssx_show_op2["session_state"],"failed to find SA in Session")


	self.myLog.info("\nStep1: Checking session state\n")
        #output_dut2 = check_ike_session_brief(self.ssx)
        #self.failUnless(output_dut2 , "Sessions Have Gone Down")
	ses_yn = self.ssx.cmd("show ike-session brief")
        self.myLog.output("show ike-session brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("Ikev2 Session is not established")
                
        
    def tun_icmp_cntrs(self,rule):
	#clear the ACL counters before sending the traffic
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

        #ping operation after acl applied
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['cisco_service_slot2_ip'],"500","4")
        if 'permit_icmp' in rule:
            self.failIfEqual(op_ping,False,"Ping through tunnel failed after permit acl is applied!!")
	    if op_ping == False:
		self.myLog.output("\n\n\n######################################################################\n")
		self.myLog.output("Ping through tunnel failed after permit acl is applied!!")
	    	self.myLog.output("\n\n\n######################################################################\n")
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"4","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
		    self.myLog.output("Tunnel: permit_icmp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","4","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: permit_icmp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
        else:
            self.failIfEqual(op_ping,True,"Ping through tunnel must fail!!")
	    if op_ping == True:
		self.myLog.output("\n\n\n######################################################################\n")
		self.myLog.output("Ping through tunnel must fail after deny acl is applied!!")
		self.myLog.output("\n\n\n######################################################################\n")
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","4","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_icmp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","0","4")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_icmp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

    def tun_igmp_cntrs(self,rule):

	self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
	#nemesis tool for generating igmp packets on linux
        self.linux.cmd("!sudo /usr/local/bin/nemesis igmp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['linux1']))
        time.sleep(5)

	cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	if 'permit' in rule:
	    output = verify_port_counters(self.ssx,cmd_op,1)
	    if 'in' in rule:
		self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
	    	if output == 0:
		    self.myLog.output("\n\n\n######################################################################\n")
		    self.myLog.output("Tunnel: permit_igmp_in: igmp did not pass through when permitted ")
		    self.myLog.output("\n\n\n######################################################################\n")
	    if 'out' in rule:
		if output == 0:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: permit_igmp_out: igmp did not pass through when permitted ")
		    self.myLog.output("\n\n\n######################################################################\n")
	elif 'deny' in rule:
	    output = verify_port_counters(self.ssx,cmd_op,1)
	    if 'in' in rule:
		self.failIfEqual(output,1,"igmp through interface passed through when denied") 
		if output == 1:
		    self.myLog.output("\n\n\n######################################################################\n")
		    self.myLog.output("Tunnel: deny_igmp_in: igmp passed through when denied ")
		    self.myLog.output("\n\n\n######################################################################\n")
	    if 'out' in rule:
		if output == 1:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_igmp_out: igmp passed through when denied ")
		    self.myLog.output("\n\n\n######################################################################\n")
	
    def tun_tcp_cntrs(self,rule):
	self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
        #nemesis tool for generating igmp packets on linux
        self.linux.cmd("!sudo /usr/local/bin/nemesis tcp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['linux1']))
        time.sleep(5)

	if 'permit_tcp' in rule:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"1","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
		    self.myLog.output("Tunnel: permit_tcp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","1","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: permit_tcp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
        else:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","1","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_tcp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","0","1")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_tcp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	'''
        cmd_op = self.ssx.cmd("show  port %s counters "%(active_slot2_ip))
        if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,1,"igmp through interface passed through when denied")
	'''

    def tun_udp_cntrs(self,rule):
	self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
        #nemesis tool for generating igmp packets on linux
        self.linux.cmd("!sudo /usr/local/bin/nemesis udp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['linux1']))
        time.sleep(5)
	
	if 'permit_udp' in rule:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"1","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: permit_udp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","1","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: permit_udp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
        else:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","1","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_udp_in: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name'],"0","0","0","0","1")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
		    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Tunnel: deny_udp_out: Acl counters are failing ")
		    self.myLog.output("\n\n\n######################################################################\n")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])


	'''
        cmd_op = self.ssx.cmd("show  port %s counters "%(active_slot2_ip))
        if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,1,"igmp through interface passed through when denied")
       '''

    def ses_icmp_cntrs(self,rule):
	#clear the acl counters before the traffic is sent
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])

        op_ping = self.linux2.ping_xpress_vpn(script_var['ip_pool'],script_var['linux1'],"500","4")

        if 'permit_icmp' in rule:
            self.failIfEqual(op_ping,False,"Ping through Session failed after permit acl is applied!!")
	    if op_ping == False:
                self.myLog.output("\n\n\n######################################################################\n")
                self.myLog.output("Ping through Session failed after permit acl is applied!!")
                self.myLog.output("\n\n\n######################################################################\n") 
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"4","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_icmp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","4","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_icmp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
        else:
            self.failIfEqual(op_ping,True,"Ping through Session must fail!!")
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","4","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_icmp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","0","4")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_icmp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])
	

    def ses_igmp_cntrs(self,rule):

        self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])
        #nemesis tool for generating igmp packets on linux
	self.linux2.cmd("!sudo /usr/local/bin/nemesis igmp -S %s -D %s"%( script_var['ip_pool'], script_var['linux1']))
        time.sleep(5)	

	cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])	

	if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_igmp_sess_in : igmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_igmp_sess_out : igmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                self.failIfEqual(output,1,"igmp through interface passed through when denied")
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_igmp_sess_in : igmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_igmp_sess_out : igmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")

    def ses_tcp_cntrs(self,rule):
        self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])
        #nemesis tool for generating igmp packets on linux
	self.linux2.cmd("!sudo /usr/local/bin/nemesis tcp -S %s -D %s"%( script_var['ip_pool'], script_var['linux1']))
        time.sleep(5)
	
	if 'permit_tcp' in rule:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"1","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_tcp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")	
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","1","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_tcp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
        else:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","1","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_tcp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","0","1")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_tcp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])

	
	'''
        cmd_op = self.ssx.cmd("show  port %s counters "%(active_slot2_ip))
        if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,1,"igmp through interface passed through when denied")
	'''

    def ses_udp_cntrs(self,rule):
        self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])
        #nemesis tool for generating igmp packets on linux
	self.linux2.cmd("!sudo /usr/local/bin/nemesis udp -S %s -D %s"%( script_var['ip_pool'], script_var['linux1']))
        time.sleep(5)	
	
	if 'permit_udp' in rule:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"1","0","0","0","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_udp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","1","0")
                self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: permit_udp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
        else:
            if 'in' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","1","0","0","0")
                #self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_udp_sess_in : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")
            elif 'out' in rule:
                acl_cntrs = verify_access_list_counters(self.ssx,script_var['acl_name1'],"0","0","0","0","1")
                #self.failIf(acl_cntrs != True , "Acl counters are failing ")
		if acl_cntrs != True:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Session: deny_udp_sess_out : Acl counters are failing ")
                    self.myLog.output("\n\n\n######################################################################\n")

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name1'])
	'''
	cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))
        if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            self.failIfEqual(output,1,"igmp through interface passed through when denied")
	'''
    def port_icmp_cntrs(self,rule):
	#clear the ACL counters before sending the traffic
	self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
	self.ssx.cmd("clear port counters")
        #ping operation after acl applied
        #op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['tnLpBkIp'],"500","4")
	op_ping = self.linux.cmd("ping -I %s %s -s 500 -c 4"%(script_var['xpVpnHstIp'],script_var['tnLpBkIp']))
	cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,4)
            if 'in' in rule:
                #self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_in_icmp_port : icmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_out_icmp_port : icmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,4)
            if 'in' in rule:
                #self.failIfEqual(output,1,"igmp through interface passed through when denied")
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_in_icmp_port : icmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_out_icmp_port : icmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")

    def port_igmp_cntrs(self,rule):
        self.ssx.cmd("clear port counters")
        #nemesis tool for generating igmp packets on linux
        self.linux.cmd("sudo /usr/local/bin/nemesis igmp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['tnLpBkIp']))
        time.sleep(5)
	self.ssx.cmd("context %s" %(script_var['context_name']))
        cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))
    
	if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_in_igmp_port : igmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_out_igmp_port : igmp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,1,"igmp through interface passed through when denied")
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_in_igmp_port : igmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_out_igmp_port : igmp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")


    def port_tcp_cntrs(self,rule):
        self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
        #nemesis tool for generating igmp packets on linux
	self.linux.cmd("sudo /usr/local/bin/nemesis tcp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['tnLpBkIp']))
        time.sleep(5)
	self.ssx.cmd("context %s" %(script_var['context_name']))
        cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))
        
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
    
	if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_in_tcp_port : tcp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_out_tcp_port : tcp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,1,"igmp through interface passed through when denied")
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_in_tcp_port : tcp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_out_tcp_port : tcp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")

    def port_udp_cntrs(self,rule):
        self.ssx.cmd("clear port counters")
	self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])
        #nemesis tool for generating igmp packets on linux
	self.linux.cmd("sudo /usr/local/bin/nemesis udp -S %s -D %s"%( script_var['xpVpnHstIp'], script_var['tnLpBkIp']))
	time.sleep(5)
	self.ssx.cmd("context %s" %(script_var['context_name']))
        cmd_op = self.ssx.cmd("show  port %s counters "%(script_var['tr_Active1_port']))

        self.ssx.cmd("clear ip access-list name %s counters"%script_var['acl_name'])

	if 'permit' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,0,"igmp through interface did not pass through when permited")
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_in_udp_port : udp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 0:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: permit_out_udp_port : udp did not pass through when permitted ")
                    self.myLog.output("\n\n\n######################################################################\n")
        elif 'deny' in rule:
            output = verify_port_counters(self.ssx,cmd_op,1)
            if 'in' in rule:
                #self.failIfEqual(output,1,"igmp through interface passed through when denied")
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_in_udp_port : udp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")
            if 'out' in rule:
                if output == 1:
                    self.myLog.output("\n\n\n######################################################################\n")
                    self.myLog.output("Port: deny_out_udp_port : udp passed through when denied ")
                    self.myLog.output("\n\n\n######################################################################\n")

    def mainTunnel(self,rule):
	
	#ping before acl applied
        op_ping = self.linux.ping_xpress_vpn(script_var['xpVpnHstIp'],script_var['cisco_service_slot2_ip'],"500","4")
        self.failIfEqual(op_ping,False,"Ping through tunnel failed before acl applied")

        tun_cntrs = verify_tunnel_counters_with_name(self.ssx,script_var['tunnel_name']) #lanlan api
        self.failIf(tun_cntrs != 0 , "Traffic is not via tunnel!!No tunnel counters")

        #changing context and clearing ip counters
        self.ssx.cmd("clear tunnel counters")
        time.sleep(5)

        # Push ACL config
        self.ssx.config_from_string(script_var[rule])
	
	if 'icmp' in rule:
	    self.tun_icmp_cntrs(rule)
	elif 'igmp' in rule:
	    self.tun_igmp_cntrs(rule)
	elif 'tcp' in rule:
	    self.tun_tcp_cntrs(rule)
	elif 'udp' in rule:
	    self.tun_udp_cntrs(rule)
	
	
        #Removing the Acl applied
        self.ssx.cmd("config")
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("no ip access-list %s"%(script_var['acl_name']))
        self.ssx.cmd("no session name %s"%(script_var['sess_name']))
        self.ssx.cmd("end")
        	
	#Confirming the Acl removal
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("show ip access-list name %s"%(script_var['acl_name']))
        self.ssx.cmd("end")
        
    def mainSession(self,rule):
        
	if 'icmp' in rule:
            self.ses_icmp_cntrs(rule)
        elif 'igmp' in rule:
            self.ses_igmp_cntrs(rule)
        elif 'tcp' in rule:
            self.ses_tcp_cntrs(rule)
        elif 'udp' in rule:
            self.ses_udp_cntrs(rule)
 
	'''
        tunCnt = self.ssx.cmd("show session counters")
        self.myLog.output("Session counters:%s"%tunCnt)
        rx_count  = tunCnt.splitlines()[-1].split()[2]
        tx_count = tunCnt.splitlines()[-1].split()[3]
        if 'deny' in rule:
	    rx_counter = rx_counter + '5'
	    tx_counter = tx_counter + '4'
            if not (rx_count == '1' and tx_count == '0'):
                self.fail("Session counters are not matching Rx Count = %s Tx Count = %s"%(rx_count,tx_count))
        if 'permit' in rule:
	    if not (rx_count == '1' and tx_count == '1'):
                self.fail("Session counters are not matching Rx Count = %s Tx Count = %s"%(rx_count,tx_count))	
        '''
        #Removing the Acl applied
	self.ssx.cmd("config")
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("no ip access-list %s"%(script_var['acl_name1']))
	self.ssx.cmd("no session name %s"%(script_var['sess_name']))
	self.ssx.cmd("end")

	#Confirming the Acl removal
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("show ip access-list name %s"%(script_var['acl_name1']))
        self.ssx.cmd("end")
       
    def mainPort(self,rule):

	self.ssx.config_from_string(script_var[rule])

	if 'icmp' in rule:
            self.port_icmp_cntrs(rule)
        elif 'igmp' in rule:
            self.port_igmp_cntrs(rule)
        elif 'tcp' in rule:
            self.port_tcp_cntrs(rule)
        elif 'udp' in rule:
            self.port_udp_cntrs(rule)
	#Removing the Acl applied
        self.ssx.cmd("config")
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("no ip access-list %s"%(script_var['acl_name']))
	self.ssx.cmd("end")

	#Confirming the Acl removal
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("show ip access-list name %s"%(script_var['acl_name']))
        self.ssx.cmd("end")
 
    def test_ACL_Func(self):

	Card_Reset = 0
        Card_Restart = 0

	#calling the function to configure the cisco and linux
        #self.cisco_linux_config()
	
	for bridge in bridges:
	    if bridge == 'tunnel':
		self.setUpTunnel()
		self.cisco_linux_config()
		self.myLog.output("\n********** Configuring SSX Responder **************\n")
        	# Push SSX Common config
        	self.ssx.config_from_string(script_var['test_ACL_Func_Main'])
	        #calling the function to bring up the tunnel
	        self.tunnelUp()	
	        #changing context and clearing ip counters
		self.ssx.cmd("context %s" %(script_var['context_name']))
		self.ssx.cmd("clear tunnel counters")
		time.sleep(5)
		
		for rule in aclTunnelList:
		    #calling the main function 
		    self.mainTunnel(rule)
		    # Checking SSX Health 
		    hs = self.ssx.get_health_stats()
	            self.failUnless(is_healthy( hs,Card_Reset=1,Card_Restart=1), "Platform is not healthy")
		    #####Put the result code here############
		
		
		self.tearDownTunnel()


	    elif bridge == 'session':
		self.setUpSession()
                self.cisco_linux_config()	
		self.myLog.output("\n********** Configuring SSX Responder **************\n")
                # Push SSX Common config
                self.ssx.config_from_string(script_var['test_ACL_Func_Sess'])

	    	for rule in aclSessList:
	    	    if 'in' in rule:
	    	    	self.linux1.write_to_file(script_var['rad_users_acl_in'],"users","/a/radius1/etc/raddb/")
	    	    elif 'out' in rule:
	    	    	self.linux1.write_to_file(script_var['rad_users_acl_out'],"users","/a/radius1/etc/raddb/")
	    	    self.ssx.config_from_string(script_var[rule])
	            #calling the function to bring up the session
	            self.sessionUp()
	            #calling the main function
	     	    self.mainSession(rule)	       
	     	    hs = self.ssx.get_health_stats()
	            self.failUnless(is_healthy( hs,Card_Reset=1,Card_Restart=1), "Platform is not healthy")
	    
	            #####Put the result code here############
		    self.linux1.cmd("sudo pkill radiusd")
		    time.sleep(10)

		    self.linux2.cmd("ike reset")
        	    time.sleep(10)
	            self.linux2.cmd("exit")
	    
	        self.tearDownSession()

	    elif bridge == 'port':
		self.setUpTunnel()
	        self.cisco_linux_config()
		self.myLog.output("\n********** Configuring SSX Responder **************\n")
                # Push SSX Common config
                self.ssx.config_from_string(script_var['test_ACL_Func_Main'])
		for rule in aclPortList:
		    self.mainPort(rule)
		    hs = self.ssx.get_health_stats()
                    self.failUnless(is_healthy( hs,Card_Reset=1,Card_Restart=1), "Platform is not healthy")
		
		self.ssx.close()
        	self.linux.close()
        	self.linux1.close()     		


		#self.tearDownTunnel()
 
if __name__ == '__main__':
	#filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger('aclAll.log', debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_ACL_Func)
	test_runner().run(suite)
	    
