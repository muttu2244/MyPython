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

DESCRIPTION: Route delete and recovery behavior due to OSPF Hello unreachable.
TEST PLAN: DoCoMo regression
TEST CASES: DoCoMo_5_2_1

HOW TO RUN: python2.5 DoCoMo_5_2_1.py
AUTHOR: jameer@stoke.com
REIEWER: kra@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from CISCO import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from vlan import *
from misc import *
from ospf_ikev2 import *
from helpers import is_healthy
import re, commands

#Import Config and topo file
from config_docomo import *
from topo import *

class test_DoCoMo_5_2_1(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx1 = SSX(ssx1["ip_addr"])
        self.ssx1.telnet()
        
	# Clear the SSX config
        self.ssx1.clear_config()

        # wait for card to come up
        self.ssx1.wait4cards()
        self.ssx1.clear_health_stats()
    
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx1.close()

    def test_DoCoMo_5_2_1(self):

        self.myLog.output("==================Starting The Test====================")

	# Getting the management IP and Gateway
	self.myLog.output("Getting the management IP and Gateway")
	ipOp = commands.getoutput("nslookup %s"%ssx1["hostname"]).split()[-1]
	gw = ipOp.split('.')
	gw = "".join([gw[0],'.',gw[1],'.',gw[2],'.','1'])

        # Push SSX config
        self.ssx1.config_from_string(security_var['DoCoMo_5_2_1'] %(security_var['username'],security_var['passwd'],ipOp,gw))

	# Verify the login authentication via console
	self.myLog.info("Verifying the login authentication via console")
	self.ssx1.cmd("context local")
	loginOp = self.ssx1.verify_console_login()
	print "testing"
	#self.failUnless(loginOp, "Accepted wrong login credentials")
	loginOp = self.ssx1.verify_console_login("%s@local"%security_var['username'],security_var['passwd'])
	self.failIf(loginOp, "Not accepted the right login credentials")

	self.ssx1.cmd("terminal length infinite")
	self.ssx1.cmd("terminal width infinite")
	self.myLog.output("Configuration after login:%s"%self.ssx1.cmd("show configuration"))

        # Checking SSX Health
        hs1 = self.ssx1.get_health_stats()
        self.failUnless(is_healthy( hs1), "Platform is not healthy at SSX1")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("DoCoMo_5_2_1.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_5_2_1)
        test_runner().run(suite)

