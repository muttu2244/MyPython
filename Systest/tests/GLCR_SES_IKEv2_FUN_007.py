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

DESCRIPTION:Verify that session is maintained after GLC Failover and switchback.
TEST PLAN:
TEST CASE: DoCoMo IPsec

HOW TO RUN: python2.5 GLCR_SES_IKEv2_FUN_007.py
AUTHOR: jameer@stoke.com
REVIEWER: krao@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from CISCO import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *
from glcr import *
from lanlan import *
from ike import *

#Import config and topo files
from config_docomo import *
from topo_glcr import *

class test_GLCR_SES_IKEv2_FUN_007(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
        self.ssx = SSX(ssx["ip_addr"])
        self.sst = SSX(sst["ip_addr"])
        self.cisco = CISCO(cisco["ip_addr"])
        self.radius = Linux(rad_srvr["ip_addr"])
	
	#Initiate the telnet session
	self.ssx.telnet()
	self.sst.telnet()
        self.cisco.console(cisco["ip_addr"])
        self.radius.telnet()
	
	#Clear config
        self.ssx.clear_context_all()
        self.ssx.clear_ports()
        self.ssx.clear_health_stats()
        self.sst.clear_context_all()
        self.sst.clear_ports()
	
    def tearDown(self):

	# Bring down the sessions
	self.sst.cmd("sst %s count - 1 rate 1 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot2'])
	self.sst.cmd("sst %s count - 1 rate 1 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot3'])

        # Close the telnet sessions
	self.ssx.close()
       	self.sst.close()
        self.radius.close()

    def test_GLCR_SES_IKEv2_FUN_007(self):

        self.myLog.output("\n**********starting the test**************\n")
	
        self.myLog.info("Verifying the SSX, GLC-R enabled or not")
        op = verify_glcr_status(self.ssx)
        if op == 1:
                self.myLog.output("Device is not configured for GLC Redundancy\nConfiguring the System for GLC-R, needs reboot\n")
                set_device_to_glcr(self.ssx)
	
	#Getting the GLCR Status
	self.myLog.info("Getting the GLCR Status")
	op = get_glcr_status(self.ssx)
	if int(op['standby']) != 4:
		self.myLog.error("4th card is not Standby card - reloading the Box")
		self.ssx.reload_device(timeout=200)
	
        #Push the config to SSX
        self.myLog.info("\n\nConfiguring the SSX and SST\n\n")
        self.ssx.config_from_string(ipsec_var['GLCR_SES_IKEv2_FUN_007'])
        self.sst.config_from_string(ipsec_var['SST_GLCR_SES_IKEv2_FUN_007'])

        #clear prev logs and Enable the logs
	self.ssx.cmd("no debug all")
	self.ssx.cmd("clear log debug")
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
	
	#Configuring the radius server
	self.myLog.info("Configuring the radius server")
	self.radius.configure_ip_interface(p_cisco_rad[1],ipsec_var['card2_rad_server1/mask'])
	
        #Configure Cisco
        self.myLog.info("Configuring Cisco")
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_sst_slot2_ip/mask'],intf=p_sst_cisco_slot2[1])
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_sst_slot3_ip/mask'],intf=p_sst_cisco_slot3[1])
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_card2_active_ip/mask'],intf=p_active_ssx_cisco_slot2[1])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_card2_standby_ip/mask'],intf=p_standby_ssx_cisco_slot2[1])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_to_rad_ip/mask'],intf=p_to_rad_active_ssx_cisco_slot2[1])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_card2_rad_server_ip/mask'],intf=p_cisco_rad[0])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_service_bkp_ip/mask'],intf=p_to_rad_standby_ssx_cisco_slot2[1])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_active_slot3_ip_mask'],intf=p_active_ssx_cisco_slot3[1])
        self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_standby_4slot3_ip_mask'],intf=p_standby_ssx_cisco_slot3[1])
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_rad_intf_4slot3_ip/mask'],intf=p_to_rad_active_ssx_cisco_slot3[1])
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_bkp_rad_intf_4slot3_ip/mask'],intf=p_to_rad_standby_ssx_cisco_slot3[1])
	
	#Configring the radius and adding routes
	self.myLog.info("Configring the radius and adding routes")	
	self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_route_active_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_route_backup_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_ses_route'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_sst_ixia'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_to_cisco_active_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_to_cisco_standby_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
	
	self.radius.cmd("sudo pkill radius")
	self.radius.cmd("sudo /usr/local/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius1/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius2/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius3/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius4/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius5/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius6/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius7/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius8/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius9/sbin/radiusd")
	
	self.cisco.cmd("conf t")
	self.cisco.cmd("no ip sla 100")
	self.cisco.cmd("ip sla 100")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['ssx_card2_active'],ipsec_var['cisco_card2_active_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 100 life forever start-time now")
	self.cisco.cmd("no ip sla 101")
	self.cisco.cmd("ip sla 101")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['ssx_card2_standby_ip'],ipsec_var['cisco_card2_standby_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 101 life forever start-time now")
	self.cisco.cmd("no ip sla 200")
	self.cisco.cmd("ip sla 200")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['to_rad_ip'],ipsec_var['cisco_to_rad_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 200 life forever start-time now")
	self.cisco.cmd("no ip sla 201")
	self.cisco.cmd("ip sla 201")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['service_bkp_ip'],ipsec_var['cisco_service_bkp_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 201 life forever start-time now")
	self.cisco.cmd("no ip sla 300")
	self.cisco.cmd("ip sla 300")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['active_slot3_ip'],ipsec_var['cisco_active_slot3_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 300 life forever start-time now")
	self.cisco.cmd("no ip sla 301")
	self.cisco.cmd("ip sla 301")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['standby_4slot3_ip'],ipsec_var['cisco_standby_4slot3_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 301 life forever start-time now")
	self.cisco.cmd("no ip sla 400")
	self.cisco.cmd("ip sla 400")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['rad_intf_4slot3_ip'],ipsec_var['cisco_rad_intf_4slot3_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 400 life forever start-time now")
	self.cisco.cmd("no ip sla 401")
	self.cisco.cmd("ip sla 401")
	self.cisco.cmd("icmp-echo %s source-ip %s"%(ipsec_var['bkp_rad_intf_4slot3_ip'],ipsec_var['cisco_bkp_rad_intf_4slot3_ip']))
	self.cisco.cmd("exit")
	self.cisco.cmd("ip sla schedule 401 life forever start-time now")
	self.cisco.cmd("track 11 rtr 100 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 12 rtr 101 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 13 rtr 200 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 14 rtr 201 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 15 rtr 300 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 16 rtr 301 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 17 rtr 400 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("track 18 rtr 401 reachability")
	self.cisco.cmd("exit")
	self.cisco.cmd("end")
	self.cisco.cmd("")
	self.cisco.cmd("")
	
        #Configuring the route at Cisco
        self.myLog.info("Configuring the route at Cisco")
        self.cisco.cmd("conf t")
        self.cisco.cmd("ip route %s %s track 11"%(ipsec_var['cisco_rt_card2_lpbk_ip'],ipsec_var['ssx_card2_active']))
        self.cisco.cmd("ip route %s %s track 11"%(ipsec_var['ikev2_lpbk_ip_mask'],ipsec_var['ssx_card2_active']))
        self.cisco.cmd("ip route %s %s 20 track 12"%(ipsec_var['cisco_rt_card2_lpbk_ip'],ipsec_var['ssx_card2_standby_ip']))
        self.cisco.cmd("ip route %s %s 20 track 12"%(ipsec_var['ikev2_lpbk_ip_mask'],ipsec_var['ssx_card2_standby_ip']))
        self.cisco.cmd("ip route %s %s track 13"%(ipsec_var['cisco_card2_ses_route'],ipsec_var['to_rad_ip']))
        self.cisco.cmd("ip route %s %s track 13"%(ipsec_var['cisco_card2_ses_route1'],ipsec_var['to_rad_ip']))
        self.cisco.cmd("ip route %s %s 20 track 14"%(ipsec_var['cisco_card2_ses_route'],ipsec_var['service_bkp_ip']))
        self.cisco.cmd("ip route %s %s 20 track 14"%(ipsec_var['cisco_card2_ses_route1'],ipsec_var['service_bkp_ip']))
        self.cisco.cmd("ip route %s %s track 15"%(ipsec_var['card2_lpbk_ip1_mask'],ipsec_var['active_slot3_ip']))
        self.cisco.cmd("ip route %s %s track 15"%(ipsec_var['lpbk_3rCard_ip_mask'],ipsec_var['active_slot3_ip']))
        self.cisco.cmd("ip route %s %s 20 track 16"%(ipsec_var['card2_lpbk_ip1_mask'],ipsec_var['standby_4slot3_ip']))
        self.cisco.cmd("ip route %s %s 20 track 16"%(ipsec_var['lpbk_3rCard_ip_mask'],ipsec_var['standby_4slot3_ip']))
        self.cisco.cmd("ip route %s %s track 17"%(ipsec_var['cisco_route_sst_ixia'],ipsec_var['rad_intf_4slot3_ip']))
        self.cisco.cmd("ip route %s %s 20 track 18"%(ipsec_var['cisco_route_sst_ixia'],ipsec_var['bkp_rad_intf_4slot3_ip']))
        self.cisco.cmd("ip route %s %s"%(ipsec_var['cisco_route_to_sst_ses'],ipsec_var['sst_cisco_slot2_ip']))
        self.cisco.cmd("ip route %s %s"%(ipsec_var['cisco_route_sst_slot3'],ipsec_var['sst_cisco_slot3_ip']))
        self.cisco.cmd("ip route %s %s"%(ipsec_var['route_to_card2_ses'],ipsec_var['card2_ip']))
        self.cisco.cmd("ip route %s %s"%(ipsec_var['route_to_card2_ses'],ipsec_var['card2_ip1']))
	
	#Initiate the ikev2 sessions from SST
	self.myLog.info("Initiate the ikev2 sessions from SST")
	self.sst.cmd("context local")
	op = self.sst.cmd("sst %s count - 60000 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot2'])
	if (op and (int(op.split()[-1]) != 0)):
		self.sst.cmd("sst %s count - %s ike-protocol ikev2 transport ipv4"%(ipsec_var['port_sst_slot2'],op.split()[-1]))
		time.sleep(10)

	op = self.sst.cmd("sst %s count - 60000 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot3'])
        if (op and (int(op.split()[-1]) != 0)):
                self.sst.cmd("sst %s count - %s ike-protocol ikev2 transport ipv4"%(ipsec_var['port_sst_slot3'],op.split()[-1]))
                time.sleep(10)
	
	self.sst.cmd("sst %s count 1 rate 1 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot2'])
	time.sleep(5)
	self.sst.cmd("sst %s count 1 rate 1 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot3'])

	# Moving to context
	self.ssx.cmd("context %s"%ipsec_var['context_card2'])
	time.sleep(60)

	# Verify the session
	self.myLog.info("Verifying the session parameters")
	ses_yn = self.ssx.cmd("show ike-session 2 brief")
        self.myLog.output("show ike-session 2 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
		self.fail("FAIL : ipv4 session is not establised in 2nd card")
	
	op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 2 brief") + self.ssx.cmd("show ike-session 2 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details before GLC Failover on 2nd Card GLC: %s"%op1)

	# Moving to context
	self.myLog.info("Verifying the Session on other GLC")
	self.ssx.cmd("context %s"%ipsec_var['context_name'])
	time.sleep(60)

	# Verify the session
	self.myLog.info("Verifying the session parameters")
	ses_yn = self.ssx.cmd("show ike-session 3 brief")
        self.myLog.output("show ike-session 3 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
		self.fail("FAIL : ipv4 session is not establised in 3rd card")
	
	op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 3 brief") + self.ssx.cmd("show ike-session 3 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details before GLC Failover on 3rd Card GLC: %s"%op1)


	#GLC Failover
	self.myLog.info("GLC Failover - 2nd Card ")
	self.ssx.cmd("reload card 2")
	self.cisco.cmd("conf t")
	self.cisco.cmd("int gig %s"%ipsec_var['port_cisco_active_4slot2'])
	self.cisco.cmd("shutdown")
	self.cisco.cmd("exit")
	self.cisco.cmd("int gig %s"%ipsec_var['port_cisco_rad_intf_4slot2'])
	self.cisco.cmd("shutdown")
	self.cisco.cmd("end")
	time.sleep(10)
	
	#Verifying the sessions after GLC Failover
	self.ssx.cmd("context %s"%ipsec_var['context_card2'])
	self.myLog.info("Verifying the session after GLC Failover at 4th card")
        ses_yn = self.ssx.cmd("show ike-session 4 brief")
        self.myLog.output("show ike-session 4 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session is not backed up in 4th card")

        op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 4 brief") + self.ssx.cmd("show ike-session 4 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details on 4th card: %s"%op1)

	# Verifying that session on other GLC after GLC Failover
	self.myLog.info("Verifying the session on other GLC after GLC Failover")
	self.ssx.cmd("context %s"%ipsec_var['context_name'])
        time.sleep(60)

        # Verify the session
        self.myLog.info("Verifying the session parameters")
        ses_yn = self.ssx.cmd("show ike-session 3 brief")
        self.myLog.output("show ike-session 3 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session went down after GLC Failover of 2nd card")
        
        op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 3 brief") + self.ssx.cmd("show ike-session 3 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details after 2nd card GLC Failover on 3rd Card GLC: %s"%op1)

	#Giving some delay
	self.myLog.info("Giving some delay to card 2 to come up")
	time.sleep(30)
	self.ssx.wait4cards()
	time.sleep(5)	

	#Doing GLC Switchback
	self.ssx.wait4cards()
	self.ssx.cmd("system glc-switchback")
        self.cisco.cmd("conf t")
        self.cisco.cmd("int gig %s"%ipsec_var['port_cisco_active_4slot2'])
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("exit")
        self.cisco.cmd("int gig %s"%ipsec_var['port_cisco_rad_intf_4slot2'])
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("end")
	time.sleep(10)
	self.ssx.wait4cards()

        #Verifying the sessions after glc-switchback
        self.myLog.info("Verifying the session after glc-switchback")
	self.ssx.cmd("context %s"%ipsec_var['context_card2'])
        ses_yn = self.ssx.cmd("show ike-session 2 brief")
        self.myLog.output("show ike-session 2 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session is not establised in 2nd card")

        op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 2 brief") + self.ssx.cmd("show ike-session 2 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details after glc-switchback: %s"%op1)

        # Verifying that session on other GLC after glc-switchback
        self.myLog.info("Verifying the session on other GLC after glc-switchback")
        self.ssx.cmd("context %s"%ipsec_var['context_name'])
        time.sleep(60)

        # Verify the session
        self.myLog.info("Verifying the session parameters")
        ses_yn = self.ssx.cmd("show ike-session 3 brief")
        self.myLog.output("show ike-session 3 brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session went down after glc-switchback to 2nd card")

        op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session 3 brief") + self.ssx.cmd("show ike-session 3 list") + self.ssx.cmd("show ike-session detail handle %s"%ses_yn.splitlines()[-1].split()[1])
        self.myLog.output("Session Details after 2nd card glc-switchback on 3rd Card GLC: %s"%op1)

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_GLCR_SES_IKEv2_FUN_007)
        test_runner().run(suite)

