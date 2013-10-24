#!/usr/bin/env python2.2
"""
#######################################################################
#
# Copyright (c) Stoke Networks Pvt Ltd.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke Networks. and may 
#only be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: Verify CLI is available to
  	     1.Create logical slot (100/101)
	     2.Bind loopback to logical slot 
	     3.bind ipsec policies

Test Topo : Remote prest and neutron
TEST PLAN: Guava_4_5_Integration_Matrix.xls
TEST CASE: GLCR_FUN_NEW_001
HOW TO RUN: python2.5 GLCR_FUN_NEW_001.py
AUTHOR: Jameer Basha - jameer@stoke.com
REVIEW: 

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from ixia import *
from CISCO import *
from log import *
from glcr import *
from lanlan import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
import pexpect
from logging import getLogger
from helpers import is_healthy
import re, time

#import config and topo file
from config import *
from topo import *

class test_GLCR_FUN_NEW_001(test_case):
    myLog = getLogger()

    def setUp(self):
        #Establish a telnet sessions to SSX, Linux servers.
        self.ssx = SSX(ssx["ip_addr"])
	self.sst = SSX(sst["ip_addr"])
	self.cisco = CISCO(cisco["ip_addr"])

        #Initiate Telnet session to SSX and IXIA..
        self.ssx.telnet()
#	self.ssx.clear_config()
        self.sst.telnet()
#	self.sst.clear_config()
	self.cisco.console(cisco["ip_addr"])

	#Initail check..
	#self.ssx.clear_context_all()
	#self.ssx.clear_ports()
        self.ssx.wait4cards()
        self.sst.wait4cards()

    def tearDown(self):
        # Close the telnet session of SSX and Linux servers
        self.ssx.close()
        self.sst.close()


    def test_GLCR_FUN_NEW_001(self):

        self.myLog.info("-" *50)
        self.myLog.output("Starting Test")
        self.myLog.info("-" *50)
	self.myLog.info("Verifying the GLC-R image, if not configure the system")
	#set_device_to_glcr(self.ssx)
	
	op = verify_glcr_status(self.ssx)
	#self.failIf(1 in op ,"Device is not configured for GLC-R")
	if op == 1:
		self.myLog.output("Device is not configured for GLC Redundancy\nConfiguring the System for GLC-R, needs reboot\n")
	'''
	self.ssx.cmd("configuration")	
	slot_op = self.ssx.cmd("slot %s"%script_var1['logical_slot_100'])
	if "ERROR" in slot_op:
		self.fail("ERROR while configuring the Logical slot - 100")
	self.ssx.cmd("exit")
	slot_op = self.ssx.cmd("slot %s"%script_var1['logical_slot_101'])
	self.failIf("ERROR" in slot_op , "Error while configuring the Logical slot - 101")
	self.myLog.output("\n\nCLI option for creating the Logical Slot is verified\n\n")
	self.ssx.cmd("exit")
	self.ssx.cmd("no slot %s"%script_var1['logical_slot_100'])
	self.ssx.cmd("no slot %s"%script_var1['logical_slot_101'])
	self.ssx.cmd("end")
	'''
	#Push the Configuration to SSX and SST
#	self.ssx.config_from_string(script_var1['GLCR_FUN_NEW_001'])
	self.myLog.info("SSX is configured successfully")
#	self.sst.config_from_string(script_var1['GLCR_FUN_NEW_SST_001'])
	self.myLog.info("SST is configured successfully")
	#Moving into context
	self.ssx.cmd("context %s"%script_var1['context_name'])	
	self.sst.cmd("context local")
	
	print cisco
	## Configure cisco
	configure_cisco(self,cisco)
	## Establish Session
	self.sst.cmd("sst 2/1 count - 1 ike-protocol ikev2 transport ipv4")
	self.sst.cmd("sst 2/1 count 1 ike-protocol ikev2 transport ipv4")
	
	#Clear the ike counters
	self.myLog.output("Clearing the ike counters before triggering from SST")
	self.ssx.cmd("clear ike count")
	self.myLog.output("ike conters detail after clearing: %s\n"%self.ssx.cmd("show ike counters"))
	self.myLog.info("Triggering the 2K sessiions from SST")
	self.sst.cmd("sst %s count %s rate 50 ike-protocol ikev2 transport ipv4"%(p2_ssx_clntCisco[0],script_var1['no_of_sessions1']))
	self.myLog.output("Given delay to sessions to come up")
	time.sleep(20)
	self.myLog.info("verifying the number of sessions")
	index = 0
	while(1):
		op = verify_ike_session_counters(self.ssx,count=int(script_var1['no_of_sessions1'])-10)
		print "%d"%op
		if int(op) == 1:
			self.myLog.output("%s sessions are up at SSX"%script_var1['no_of_sessions1'])
			break 
		else:
			index = index + 1
			time.sleep(10)
		if index >= 9:
			self.myLog.output("%s session did not come up in expected time"%script_var1['no_of_sessions1'])
			break

        hs1 = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs1), "Platform is not healthy")
        hs2 = self.sst.get_health_stats()
        self.failUnless(is_healthy(hs2), "Platform is not healthy")
	

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("GLCR_FUN_NEW_001.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_GLCR_FUN_NEW_001)
        test_runner(stream=sys.stdout).run(suite)

