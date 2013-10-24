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

DESCRIPTION: SNMP Monitor - Transmit / Transmit with max system load
TEST MATRIX: 
TEST CASE  : DoCoMo_7_6_1
TOPOLOGY   : GLC-R Setup with host connected behind Initiator.

HOW TO RUN : python2.5 DoCoMo_7_6_1.py
AUTHOR     : jameer@stoke.com
REVIEWER   : krao@stoke.com 
"""

import sys, os, commands
from string import *

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
from helpers import is_healthy, insert_char_to_string
from misc import *
from glcr import *
from lanlan import *

#Import config and topo files
from config_docomo import *
from topo import *


class test_DoCoMo_7_6_1(test_case):
    myLog = getLogger()
    global pskFlag
    pskFlag = 1

    def setUp(self):
        #Establish a telnet session
        self.myLog.info(__doc__)
	self.myLog.info("Establish a telnet session to Console")
	self.ssx = SSX(ssx["ip_addr"])
	self.ssx.telnet()
        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux1["ip_addr"])
        self.xpress_vpn.telnet()

	# Telnet session to radisu server
	self.rad = Linux(topo.radius1["ip_addr"])
	self.rad.telnet()

	# Sniffer.
        self.sniffer = Linux(topo.linux1["ip_addr"])
        self.sniffer.telnet()

	# Enable the debug logs
	self.ssx.cmd("debug module aaad all")	
	self.ssx.cmd("debug module iked all")	
	self.ssx.cmd("debug module tunmgr all")	

    def tearDown(self):

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	self.ssx.close()

        # Close the telnet sessions
	if pskFlag:
		self.xpress_vpn.cmd("ike reset")
	        time.sleep(10)
 	        self.xpress_vpn.cmd("quit")	
	self.xpress_vpn.close()
	self.rad.close()

    def test_DoCoMo_7_6_1(self):

        self.myLog.output("\n**********starting the test**************\n")

        # Push SSX config
        self.ssx.config_from_string(docomo_var['DoCoMo_6_2_5'])
	
	#configuring tunnel on linux machine
        self.xpress_vpn.configure_ip_interface(port_ssx_linux1[1], docomo_var['xpress_phy_iface1_ip_mask'])
        self.rad.configure_ip_interface(port_ssx_radius1[1], docomo_var['radius1_ip_mask'])
	self.rad.cmd("sudo /sbin/route add -host %s gw %s"%(docomo_var['ip_pool_mask'],docomo_var['ssx_rad1_ip']))
	
	# start the radius, if not started
	self.myLog.output("Start the radius, if not started")
	radOp = self.rad.cmd("sudo /sbin/service radiusd status")
	if ("stop" or "dead" or "not running" in radOp):
		self.rad.cmd("sudo /sbin/service radiusd start")

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(docomo_var['xpm_autoexec'],"autoexec.cfg","/xpm/")


        # Enable debug logs for iked
        self.ssx.cmd("context %s" % docomo_var['context_name'])
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate IKE Session from Xpress VPN Client (takama)
	self.xpress_vpn.cmd("sudo /sbin/ip addr add dev %s %s/16 brd +"%(port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(docomo_var['ses_lo_ip'],docomo_var['ssx_clnt_ip'],port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(docomo_var['radius1_route'],docomo_var['ssx_clnt_ip'],port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ifconfig %s:1 %s netmask 255.255.0.0"%(port_ssx_linux1[1],docomo_var['xpress_phy_iface1_ip']))
	time.sleep(3)
	self.xpress_vpn.cmd("cd /xpm")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
	time.sleep(30)

        ses_yn = self.ssx.cmd("show ike-session brief")
        self.myLog.output("show ike-session brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session is not establised")

	op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session brief") + self.ssx.cmd("show ike-session list") + self.ssx.cmd("show ike-session detail remote %s"%docomo_var['xpress_phy_iface1_ip'])
        self.myLog.output("Session Details: %s"%op1)
        time.sleep(4)

        # Initiate Ping through tunnel
	self.myLog.output("Initiate Ping through tunnel")
        op_ping = self.xpress_vpn.ping_xpress_vpn(docomo_var['ip_pool'],docomo_var['radius1_ip'],"500","4")
        self.failUnless(op_ping,"Ping through tunnel to radius server failed")
        self.myLog.output("\n***************\n Ping through tunnel is success\n****************\n")

	self.myLog.info("Calling the shell process for loading the bulk config,\n so that we can access console while loading")
        
	#run this command on shell prompt 'on  -R3 -p6f cpuhog -n 1000 -f 0 -t 2 &'
        out = self.ssx.shellcmd("on  -R3 -p6f cpuhog -n 1000 -f 0 -t 2 &")
        self.myLog.info("%s" %out)
	# Verifying the console access while cpu usage is max.
	self.myLog.info("\n\nVerifying the console access while cpu usage is maximum\n\n")
	cnt = 0
	while(cnt < 15):
		self.myLog.output("CPU Utilization: %s"%self.ssx.cmd("show process cpu non-zero"))
		cpuUtil = self.ssx.cmd('show process cpu non-zero | grep "CPU0 Utilization"')
		fiveSec = re.search("CPU0\s+Utilization\s+for\s+5\s+seconds:\s+(\d+\.\d+)", cpuUtil, re.I)
		oneMin = re.search("\s+1\s+Minute:\s+(\d+\.\d+)", cpuUtil, re.I)
		self.myLog.output("CPU Utilization:\n")
		self.myLog.output("5 Seconds : %s Percentage"%fiveSec.group(1))
		self.myLog.output("1 minute  : %s Percentage"%oneMin.group(1))

		if ((float(oneMin.group(1)) >= float(80.00)) and (float(fiveSec.group(1)) >= float(80.00))):
			self.myLog.output("CPU Usage is more than or equal to 80 Precentage")
			self.myLog.output("CPU Usage is more than 80 Precentage")
	                self.myLog.output("Current CPU Utilization: %s"%self.ssx.cmd("show process cpu non-zero"))
        	        self.myLog.info("\n\n\n able to operate on console when CPU load is 60 ~ 99 Percentage\n\n\n")
			break

		cnt = cnt + 1
		time.sleep(15)


	self.myLog.info("Verifying the SNMP when cpu load is high")
	# Start the pkt captur at client
	self.myLog.info("Start the pkt capture at the client")
	self.sniffer.cmd("sudo ls")
	self.sniffer.cmd("sudo /usr/sbin/tethereal -i %s -R isakmp -q -w isakmp.pcap &"% port_ssx_linux1[1])
	self.ssx.cmd("ping %s repeat 5"%docomo_var['xpress_phy_iface1_ip'])
	time.sleep(60)
	output = self.sniffer.cmd("sudo /usr/sbin/tethereal -r isakmp.pcap -R 'ip.dsfield == 0x00 && ip.src == %s' -V | grep Diff"%(docomo_var['xpress_phy_iface1_ip']),timeout=100)
	self.failUnless("0x00" in output, "Dscp Value Mismatch")
		
	#Kill the process
        pid = out.split()[-1].strip()
        out = self.ssx.shellcmd("kill -9 %s" %pid)
        self.myLog.info("%s" %out)


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_7_6_1)
        test_runner().run(suite)

