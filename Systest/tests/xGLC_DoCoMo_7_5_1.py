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

DESCRIPTION: snmp trap - Transmit / Transmit with max system load
TEST MATRIX: 
TEST CASE  : DoCoMo_7_5_1
TOPOLOGY   : GLC-R Setup with host connected behind Initiator.

HOW TO RUN : python2.5 DoCoMo_7_5_1.py
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
from SSX import *
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


class test_DoCoMo_7_5_1(test_case):
    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session
        self.myLog.info(__doc__)
	self.myLog.info("Establish a telnet session to Console")
	self.ssx = SSX(ssx["ip_addr"])
	self.ssx.telnet()
	self.linux1=self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.linux.telnet()
	self.linux1.telnet()

	# Enable the debug logs
	self.ssx.cmd("debug module aaad all")	
	self.ssx.cmd("debug module iked all")	
	self.ssx.cmd("debug module tunmgr all")	

    def tearDown(self):

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

        self.ssx.close()

	self.linux.close()
	self.linux1.close()

    def test_DoCoMo_7_5_1(self):

        self.myLog.output("\n**********starting the test**************\n")
	self.myLog.info("Configuring the snmp before loading bulk config")
	self.ssx.config_from_string(basic_var['DoCoMo_7_5_1'])

	#Configuring Linux Interface
	self.linux.cmd("sudo /sbin/ifconfig %s %s up"%(port_ssx_linux1[1],basic_var['snmp_server_ip_mask']))

	self.ssx.cmd("ping %s repeat 20"%basic_var['snmp_server_ip'])

	self.myLog.info("Calling the shell process for loading the bulk config,\n so that we can access console while loading")
        
	#run this command on shell prompt 'on  -R3 -p6f cpuhog -n 1000 -f 0 -t 2 &'
        out = self.ssx.shellcmd("on  -R3 -p6f cpuhog -n 1000 -f 0 -t 2 &")
	self.myLog.info("%s" %out)
	# Verifying the console access while cpu usage is max.
	self.myLog.info("\n\nVerifying the SNMP Trap while cpu usage is maximum\n\n")
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

	#Setup Packet Capture
	self.linux.cmd("sudo /usr/sbin/tethereal -i %s -q -w DoCoMo.pcap &"%(port_ssx_linux1[1]))

	self.linux1.cmd("snmpget -V2C -c snmp_com1 ip %s SysName.0"%basic_var['ssx_phy_iface_ip'])
	time.sleep(60)	
	
	self.linux.cmd("sudo pkill tethereal")
	time.sleep(5)
	output = self.linux.cmd("sudo /usr/sbin/tethereal -r DoCoMo.pcap -R 'ip.dsfield == 0x00 && snmp && ip.src == %s' -V | grep Diff"%(basic_var['ssx_phy_iface_ip']),timeout=100)	
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
        suite.addTest(test_DoCoMo_7_5_1)
        test_runner().run(suite)

