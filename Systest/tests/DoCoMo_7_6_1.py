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


## Threading the processes
from threading import Thread

class testIt(Thread):
   threadLog = getLogger()
   def __init__ (self,myHandle):
	Thread.__init__(self)
	self.ssxHandle = myHandle
	self.status = -1

   def run(self):
	# Let me run the thread, so I no need to 
	# wait till it loads the configuration.
	self.threadLog.info("Loading the bulk configuration")
	self.ssxHandle.cmd("load configuration /hd/DoCoMo_7_6_1.cfg", timeout=12000)
	self.status = 1


global ssxfdList, getPath, scriptServer
getPath = sys.path[0]
ssxfdList = []
hostName = commands.getoutput("hostname")
scriptServer = commands.getoutput("host %s"% hostName)
scriptServer = scriptServer.split()[-1]

class test_DoCoMo_7_6_1(test_case):
    myLog = getLogger()
    global pskFlag
    pskFlag = 1

    def setUp(self):
	global ssxfdList, getPath, scriptServer
        #Establish a telnet session
        self.myLog.info(__doc__)
	self.myLog.info("Establish a telnet session to Console")
	self.ssx_con = SSX(ssx["ip_addr"])
	ssxfdList.append(self.ssx_con)
	for i in xrange(2):
		self.ssx = SSX(ssx["hostname"])
		ssxfdList.append(self.ssx)
	ssxfdList = tuple(ssxfdList)

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux1["ip_addr"])
        self.xpress_vpn.telnet()

	# Telnet session to radisu server
	self.rad = Linux(topo.radius1["ip_addr"])
	self.rad.telnet()

	# Sniffer.
        self.sniffer = Linux(topo.linux1["ip_addr"])
        self.sniffer.telnet()

	ssxfdList[0].telnet()
	# Clear the running config
	ssxfdList[0].wait4cards()
	ssxfdList[0].clear_config()

	# Load minimum configuration
	ssxfdList[0].load_min_config(ssx["hostname"])
	ssxfdList[0].cmd("end")
	ssxfdList[0].cmd("context local")
	ssxfdList[0].ftppasswd ("copy sftp://regress@%s:%s/DoCoMo_7_6_1.cfg /hd/DoCoMo_7_6_1.cfg noconfirm"%(scriptServer,getPath),Pword="gleep7")


	# Enable the debug logs
	ssxfdList[0].cmd("debug module aaad all")	
	ssxfdList[0].cmd("debug module iked all")	
	ssxfdList[0].cmd("debug module tunmgr all")	

	# Establish a telnet session.
	for fdIndex in xrange(1,3):
		ssxfdList[fdIndex].telnet()


    def tearDown(self):

        # Checking SSX Health
        hs = ssxfdList[0].get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

        # Close the telnet sessions
	for ssxfd in ssxfdList:
                ssxfd.close()
	if pskFlag:
		self.xpress_vpn.cmd("ike reset")
	        time.sleep(10)
 	        self.xpress_vpn.cmd("quit")	
	self.xpress_vpn.close()
	self.rad.close()

    def test_DoCoMo_7_6_1(self):

        self.myLog.output("\n**********starting the test**************\n")

	# Configuring the ikev2 session
	self.myLog.info("Configuring the ikev2 session")
	self.myLog.info("Running vgroup")
	ssx_name= ssx["ip_addr"].split("-mc")[0]
        vportssx1 = port_ssx_linux1[0].replace('/',':')
        vportssx2 = port_ssx_radius1[0].replace('/',':')
	vportl1   = port_ssx_linux1[1].replace('eth','e')
	vportl2   = port_ssx_radius1[1].replace('eth','e')

	vgroup_new("%s:%s %s:%s"%(ssx_name,vportssx1,linux1['ip_addr'],vportl1))
	vgroup_new("%s:%s %s:%s"%(ssx_name,vportssx2,radius1['ip_addr'],vportl2))
	
        # Push SSX config
        ssxfdList[0].config_from_string(docomo_var['DoCoMo_6_2_5'])
	
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
        ssxfdList[0].cmd("context %s" % docomo_var['context_name'])
        ssxfdList[0].cmd("debug module iked all")
        ssxfdList[0].cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        ssxfdList[0].cmd("clear log debug")

        # Initiate IKE Session from Xpress VPN Client (takama)
	self.xpress_vpn.cmd("sudo /sbin/ip addr add dev %s %s/16 brd +"%(port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(docomo_var['ses_lo_ip'],docomo_var['ssx_clnt_ip'],port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(docomo_var['radius1_route'],docomo_var['ssx_clnt_ip'],port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ifconfig %s:1 %s netmask 255.255.0.0"%(port_ssx_linux1[1],docomo_var['xpress_phy_iface1_ip']))
	time.sleep(3)
	self.xpress_vpn.cmd("cd /xpm")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
	time.sleep(10)

        ses_yn = ssxfdList[0].cmd("show ike-session brief")
        self.myLog.output("show ike-session brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session is not establised")

	op1 = ssxfdList[0].cmd("show session") + ssxfdList[0].cmd("show ike-session brief") + ssxfdList[0].cmd("show ike-session list") + ssxfdList[0].cmd("show ike-session detail remote %s"%docomo_var['xpress_phy_iface1_ip'])
        self.myLog.output("Session Details: %s"%op1)
        time.sleep(4)

        # Initiate Ping through tunnel
	self.myLog.output("Initiate Ping through tunnel")
        op_ping = self.xpress_vpn.ping_xpress_vpn(docomo_var['ip_pool'],docomo_var['radius1_ip'],"500","4")
        self.failUnless(op_ping,"Ping through tunnel to radius server failed")
        self.myLog.output("\n***************\n Ping through tunnel is success\n****************\n")

	self.myLog.info("Calling the thread process for loading the bulk config,\n so that we can access console while loading")
	loadBulk = testIt(ssxfdList[1]) # Loading the bulk config from management.
	loadBulk.start()

	# Verifying the console access while cpu usage is max.
	self.myLog.info("\n\nVerifying the console access while cpu usage is maximum\n\n")
	cnt = 0
	while(cnt < 15):
		self.myLog.output("CPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))
		cpuUtil = ssxfdList[0].cmd('show process cpu non-zero | grep "CPU0 Utilization"')
		fiveSec = re.search("CPU0\s+Utilization\s+for\s+5\s+seconds:\s+(\d+\.\d+)", cpuUtil, re.I)
		oneMin = re.search("\s+1\s+Minute:\s+(\d+\.\d+)", cpuUtil, re.I)
		self.myLog.output("CPU Utilization:\n")
		self.myLog.output("5 Seconds : %s Percentage"%fiveSec.group(1))
		self.myLog.output("1 minute  : %s Percentage"%oneMin.group(1))

		if ((float(oneMin.group(1)) >= float(80.00)) and (float(fiveSec.group(1)) >= float(80.00))):
			self.myLog.output("CPU Usage is more than or equal to 80 Precentage")
			self.myLog.output("CPU Usage is more than 80 Precentage")
	                self.myLog.output("Current CPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))
        	        self.myLog.info("\n\n\n able to operate on console when CPU load is 60 ~ 99 Percentage\n\n\n")
			break

		cnt = cnt + 1
		time.sleep(15)


	self.myLog.info("Verifying the SNMP when cpu load is high")
	# Start the pkt captur at client
	self.myLog.info("Start the pkt capture at the client")
	self.sniffer.cmd("sudo ls")
	self.sniffer.cmd("sudo /usr/sbin/tethereal -i %s -R isakmp -q -w isakmp.pcap &"% port_ssx_linux1[1])
	ssxfdList[0].cmd("ping %s repeat 1"%docomo_var['xpress_phy_iface1_ip'])
	time.sleep(5)
	output = self.sniffer.cmd("sudo /usr/sbin/tethereal -r isakmp.pcap -R 'ip.dsfield == 0x00 && ip.src == %s' -V | grep Diff"%(script_var['xpress_phy_iface1_ip']),timeout=100)
	self.failUnless("0x00" in output, "Dscp Value Mismatch")
		
	loadBulk.join()



if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_7_6_1)
        test_runner().run(suite)

