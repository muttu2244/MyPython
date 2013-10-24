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

HOW TO RUN: python2.5 DoCoMo_PERF_GLCR_SESS_003.py
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
from ixia import *
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

global ixia_path,cardID, portID
ixia_path = "D:/DoCoMo"
#op = topo.p1_ssx2_ixia[1].split('/')
#cardID = op[0]
#portID = op[1]

class test_DoCoMo_PERF_GLCR_SESS_003(test_case):
    myLog = getLogger()
    global ixia_path, cardID, portID

    def setUp(self):

        #Establish a telnet session
        self.ssx = SSX(ssx["ip_addr"])
        self.sst = SSX(sst["ip_addr"])
        self.cisco = CISCO(cisco["ip_addr"])
	self.ixia = IXIA(ixia["ip_addr"])
        self.radius = Linux(rad_srvr["ip_addr"])
	
	#Initiate the telnet session
	self.ssx.telnet()
	self.sst.telnet()
        self.cisco.console(cisco["ip_addr"])
	self.ixia.telnet()
        self.radius.telnet()
	'''
	#Clear config
	self.ssx.wait4cards()
        self.ssx.clear_config()
        self.ssx.clear_health_stats()
	self.sst.wait4cards()
        self.sst.clear_config()
	'''
    def tearDown(self):

        # Close the telnet sessions
	self.ixia.cmd("ixLogout")
        self.ixia.cmd("cleanUp")
	self.ixia.close()
	self.ssx.close()
       	self.sst.close()
        self.radius.close()

    def test_DoCoMo_PERF_GLCR_SESS_003(self):

        self.myLog.output("\n**********starting the test**************\n")
	'''
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
        self.ssx.config_from_string(ipsec_var['DoCoMo_PERF_GLCR_SESS_003'])
        self.sst.config_from_string(ipsec_var['SST_DoCoMo_PERF_GLCR_SESS_003'])

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
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_slot2_ip/mask'],intf=topo_glcr.p1_cisco_ixia[0])
	self.cisco.configure_ipv4_interface(ip_addr=ipsec_var['cisco_slot3_ip/mask'],intf=topo_glcr.p2_cisco_ixia[0])
	
	#Configring the radius and adding routes
	self.myLog.info("Configring the radius and adding routes")	
	self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_route_active_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_route_backup_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['card2_ses_route'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_sst_ixia'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_to_cisco_active_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
        self.radius.cmd("sudo /sbin/route add -net %s gw %s dev %s"%(ipsec_var['route_to_cisco_standby_rad'],ipsec_var['cisco_card2_rad_server_ip'],p_cisco_rad[1]))
	
	self.radius.cmd("sudo pkill radius")
	#self.radius.cmd("sudo /usr/local/sbin/radiusd")
	self.radius.cmd("sudo /a/radius1/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius2/sbin/radiusd")
	self.radius.cmd("sudo /a/radius3/sbin/radiusd")
	self.radius.cmd("sudo /a/radius4/sbin/radiusd")
	self.radius.cmd("sudo /a/radius5/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius6/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius7/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius8/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius9/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius10/sbin/radiusd")
	#self.radius.cmd("sudo /a/radius11/sbin/radiusd")
        #self.radius.cmd("sudo /a/radius12/sbin/radiusd")
        #self.radius.cmd("sudo /a/radius13/sbin/radiusd")
        #self.radius.cmd("sudo /a/radius14/sbin/radiusd")
        #self.radius.cmd("sudo /a/radius15/sbin/radiusd")
        #self.radius.cmd("sudo /a/radius16/sbin/radiusd")

	
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
	self.cisco.cmd("ip route %s %s"%(ipsec_var['cisco_ssx_ses_traffic_route'],ipsec_var['ixia_cisco_slot2_ip']))
	self.cisco.cmd("ip route %s %s"%(ipsec_var['cisco_ssx_slot3_ses_traffic_route'],ipsec_var['ixia_cisco_slot3_ip']))

	#Initiate the ikev2 sessions from SST
	self.myLog.info("Initiate the ikev2 sessions from SST")
	self.sst.cmd("context local")
	op = self.sst.cmd("sst %s count - 60000 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot2'])
	if (op and (int(op.split()[-1]) != 0)):
		self.sst.cmd("sst %s count - %s ike-protocol ikev2 transport ipv4"%(ipsec_var['port_sst_slot2'],op.split()[-1]))
                time.sleep(5)

	op = self.sst.cmd("sst %s count - 60000 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot3'])
        if (op and (int(op.split()[-1]) != 0)):
                self.sst.cmd("sst %s count - %s ike-protocol ikev2 transport ipv4"%(ipsec_var['port_sst_slot3'],op.split()[-1]))
                time.sleep(5)
	
	self.sst.cmd("sst %s count 60000 rate 100 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot2'])
	time.sleep(20)
	self.sst.cmd("sst %s count 60000 rate 100 ike-protocol ikev2 transport ipv4"%ipsec_var['port_sst_slot3'])
	time.sleep(20)
	'''
	# Moving to context
	self.ssx.cmd("context %s"%ipsec_var['context_name'])

        # Pull required TCL and IXIA packages to our test topo
        self.ixia.cmd("package require IxTclHal")
        self.ixia.cmd("package require IxTclExplorer")

        # Login with your username
        login = self.ixia.cmd("ixLogin %s"%ixia_owner)
        if not int(login):
           self.myLog.output("User %s has logged in Successfully"%ixia_owner)

	# Gave delay to 120K sessions comes up
	#time.sleep(300)
	ikeCnt = 0
	repeatIndex = 0
	bytesTuple = (128,512)

	def sourceMe(byte):
		self.ixia.cmd('source "%s/DoCoMo_Perf_Glcr_2ndCardSST%sBytes.tcl"'%(ixia_path,byte))
                self.ixia.cmd("ixTransmitPortArpRequest %s"%p_sst_ixia[1])
                self.ixia.cmd('source "%s/DoCoMo_Perf_Glcr_3rdCardSST%sBytes.tcl"'%(ixia_path,byte))
		self.ixia.cmd("ixTransmitPortArpRequest %s"%p_sst_slot3_ixia[1])
		time.sleep(10)
		self.ixia.cmd('source "%s/DoCoMo_Perf_Glcr_2ndCardCisco%sBytes.tcl"'%(ixia_path,byte))
		self.ixia.cmd("ixTransmitPortArpRequest %s"%p1_cisco_ixia[1])
		self.ixia.cmd('source "%s/DoCoMo_Perf_Glcr_3rdCardCisco%sBytes.tcl"'%(ixia_path,byte))
		self.ixia.cmd("ixTransmitPortArpRequest %s"%p2_cisco_ixia[1])


	def ixTransmit():
		self.ixia.cmd("ixStartPortTransmit %s"%p_sst_ixia[1])
		time.sleep(5)
		self.ixia.cmd("ixStartPortTransmit %s"%p_sst_slot3_ixia[1])
		time.sleep(5)
		self.ixia.cmd("ixStartPortTransmit %s"%p1_cisco_ixia[1])
		time.sleep(5)
		self.ixia.cmd("ixStartPortTransmit %s"%p2_cisco_ixia[1])

	def ixStop():
                self.ixia.cmd("ixStopPortTransmit %s"%p_sst_ixia[1])
                time.sleep(5)
                self.ixia.cmd("ixStopPortTransmit %s"%p_sst_slot3_ixia[1])
                time.sleep(5)
                self.ixia.cmd("ixStopPortTransmit %s"%p1_cisco_ixia[1])
                time.sleep(5)
                self.ixia.cmd("ixStopPortTransmit %s"%p2_cisco_ixia[1])
	'''
	# Verify the 120K sessions
	sesFlag = 0
	while(1):
		self.myLog.info("repeatIndex: %s"%repeatIndex)
		cnt = self.ssx.cmd('show ike-session counters | grep "Active Sessions"')
		self.myLog.output("show ike-session counters:%s"%self.ssx.cmd('show ike-session counters'))
		cnt = int(cnt.split()[2].strip())
		repeatIndex = repeatIndex + 1
		if cnt >= 1190000:
			self.myLog.output("120K sessions established successfully")
			sesFlag = 1
			break
		self.myLog.output("Number of sessions established as of now: %s"%cnt)
		self.myLog.info("Going for sleep for some time")
		time.sleep(40)
		if repeatIndex >= 50:
			self.myLog.error("Not able to establish 120K sessions in a expected time")
			self.myLog.output("Number of sessions established as of now: %s"%cnt)
			break

	sourceMe(bytesTuple[0])
	ixTransmit()
	self.myLog.info("Given delay after transmit")
	time.sleep(300)
	tmp = 0

	self.myLog.info("Verifying the total sessions after starting the traffic:")
	while((tmp < 10) or (sesFlag)):
		self.myLog.info("tmp and sesFlag: %s and %s "%(tmp, sesFlag))
		if sesFlag == 0:
			cnt = self.ssx.cmd('show ike-session counters | grep "Active Sessions"')
			self.myLog.output("show ike-session counters:%s"%self.ssx.cmd('show ike-session counters'))
			cnt = int(cnt.split()[2].strip())
			if cnt >= 119000:
				self.myLog.output("120K sessions established successfully")
				sesFlag = 1
			self.myLog.output("Number of sessions established as of now: %s"%cnt)
			self.myLog.info("Going for sleep for some time")
	                time.sleep(30)
	# Verify that all sessions are up
	self.failIf(sesFlag == 0 , "Not all 120K sessions are up")

	'''
	# Verifying the session counters
	self.myLog.info("Verifying the session counters")
	self.ssx.cmd("context %s"%ipsec_var['context_name'])
	myDict = {}
	ipList = ["3.2.0.98", "3.2.31.86", "3.2.188.215", "3.2.70.146", "3.2.144.162"]
	for remoteIp in ipList:
		ssxOp = parse_show_ike_session_detail(self.ssx,remote_ip=remoteIp)
		if ssxOp['session_handle']:
			sesCnt = self.ssx.cmd("show session counter handle %s"%ssxOp['session_handle'])
			sesCnt = sesCnt.splitlines()[-1]
			self.failIf(((int(sesCnt.split()[2]) == 0) and (int(sesCnt.split()[3]) == 0)),"Traffic is not flowing in the session with handle: %s"%ssxOp['session_handle'])
			myDict[ssxOp['session_handle']] = "%s %s"%(sesCnt.split()[2],sesCnt.split()[3])

	# Moving to other context
	self.ssx.cmd("context %s"%ipsec_var['context_card2'])
	ipList = ["2.2.98.58", "2.2.130.176", "2.2.0.167", "2.2.3.157", "2.2.163.43"]
	for remoteIp in ipList:
                ssxOp = parse_show_ike_session_detail(self.ssx,remote_ip=remoteIp)
                if ssxOp['session_handle']:
                        sesCnt = self.ssx.cmd("show session counter handle %s"%ssxOp['session_handle'])
                        sesCnt = sesCnt.splitlines()[-1]
                        self.failIf(((int(sesCnt.split()[2]) == 0) and (int(sesCnt.split()[3]) == 0)),"Traffic is not flowing in the session with handle: %s"%ssxOp['session_handle'])

        # Checking SSX Health
	self.myLog.info("Checking SSX Health after 128 byte traffic")
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")
	
	ixStop()

	# Verifying the sessions for 512 bytes of UDP traffic
	self.myLog.info("\n\nVerifying the sessions for 512 bytes of UDP traffic\n\n")
        sourceMe(bytesTuple[1])
        ixTransmit()
        self.myLog.info("Given delay after transmit")
        time.sleep(300)
        tmp = 0

        # Verifying the session counters
        self.myLog.info("Verifying the session counters")
        self.ssx.cmd("context %s"%ipsec_var['context_name'])
        ipList = ["3.2.0.98", "3.2.31.86", "3.2.188.215", "3.2.70.146", "3.2.144.162"]
        for remoteIp in ipList:
                ssxOp = parse_show_ike_session_detail(self.ssx,remote_ip=remoteIp)
                if not ssxOp['session_handle']:
                        sesCnt = self.ssx.cmd("show session counter handle %s"%ssxOp['session_handle'])
                        sesCnt = sesCnt.splitlines()[-1]
                        self.failIf(((int(sesCnt.split()[2]) == 0) and (int(sesCnt.split()[3]) == 0)),"Traffic is not flowing in the session with handle: %s"%ssxOp['session_handle'])

        # Moving to other context
        self.ssx.cmd("context %s"%ipsec_var['context_card2'])
        ipList = ["2.2.98.58", "2.2.130.176", "2.2.0.167", "2.2.3.157", "2.2.163.43"]
        for remoteIp in ipList:
                ssxOp = parse_show_ike_session_detail(self.ssx,remote_ip=remoteIp)
                if not ssxOp['session_handle']:
                        sesCnt = self.ssx.cmd("show session counter handle %s"%ssxOp['session_handle'])
                        sesCnt = sesCnt.splitlines()[-1]
                        self.failIf(((int(sesCnt.split()[2]) == 0) and (int(sesCnt.split()[3]) == 0)),"Traffic is not flowing in the session with handle: %s"%ssxOp['session_handle'])

	ixStop()

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
        suite.addTest(test_DoCoMo_PERF_GLCR_SESS_003)
        test_runner().run(suite)

