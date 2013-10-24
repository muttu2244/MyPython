#!/sr/bin/env python2.5
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

DESCRIPTION: Verifies that CLI should not allow to configure the ports 2/2,2/3,3/2,3/3,4/2,4/3
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_015

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_015"
AUTHOR: npatel
REVIEWER: 
"""

import sys, os
import  time


mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries 
from SSX import * 
from log import *
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner  
from helpers import is_healthy
from ShowCmdList import *
from topo import *
#from config import *
import pexpect
import re

class test_Global_Cli_015(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
       

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_015(self):
        switch_over = True
        status = True
	
	#port configuration	

        self.ssx.cmd("conf")
        self.ssx.cmd("cont porttest")
        self.ssx.cmd("int p1")
        self.ssx.cmd("arp arpa")
        self.ssx.cmd("ip address 57.1.1.2/24")
        self.ssx.cmd("exit")
	self.ssx.cmd("exit")
	 op1 = self.ssx.cmd("port ethernet 2/2")
        if "ERROR" in op1:
                self.myLog.output("Error: port 2/2 can not be configured")
                status = False
        self.ssx.cmd("bind interface p1 porttest")
        self.ssx.cmd("exit")
        self.ssx.cmd("enable")
        self.ssx.cmd("exit")

        self.ssx.cmd("conf")
        self.ssx.cmd("cont porttest")
        self.ssx.cmd("int p2")
        self.ssx.cmd("arp arpa")
        self.ssx.cmd("ip address 67.1.1.1/24")
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")
        self.ssx.cmd("port ethernet 2/3")
        self.ssx.cmd("bind interface p2 porttest")
        self.ssx.cmd("exit")
        self.ssx.cmd("enable")
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")


	self.ssx.cmd("conf")
	self.ssx.cmd("cont porttest2")
	self.ssx.cmd("int p3")
	self.ssx.cmd("arp arpa")
	self.ssx.cmd("ip address 57.1.1.3/24")
	self.ssx.cmd("exit")
		self.ssx.cmd("exit")
		self.ssx.cmd("port ethernet 3/2")
	self.ssx.cmd("bind interface p3 porttest2")
	self.ssx.cmd("exit")
	self.ssx.cmd("enable")
	self.ssx.cmd("exit")

	        self.ssx.cmd("conf")
        self.ssx.cmd("cont porttest")

	self.ssx.cmd("int p4")
	self.ssx.cmd("arp arpa")
	self.ssx.cmd("ip address 67.1.1.4/24")
	self.ssx.cmd("exit")
	self.ssx.cmd("exit")
	self.ssx.cmd("port ethernet 3/3")
	self.ssx.cmd("bind interface p4 porttest2")
	self.ssx.cmd("exit")
	self.ssx.cmd("enable")
	self.ssx.cmd("exit")
	self.ssx.cmd("exit")
	
        self.ssx.cmd("conf")
        self.ssx.cmd("cont porttest3")
        self.ssx.cmd("int p5")
        self.ssx.cmd("arp arpa")
        self.ssx.cmd("ip address 57.1.1.5/24")
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")
		        self.ssx.cmd("port ethernet 4/2")
        self.ssx.cmd("bind interface p5 porttest3")
        self.ssx.cmd("exit")
        self.ssx.cmd("enable")
        self.ssx.cmd("exit")

		
		
		        self.ssx.cmd("conf")
        self.ssx.cmd("cont porttest")

        self.ssx.cmd("int p6")
        self.ssx.cmd("arp arpa")
        self.ssx.cmd("ip address 67.1.1.6/24")
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")
        self.ssx.cmd("port ethernet 4/3")
        self.ssx.cmd("bind interface p6 porttest3")
        self.ssx.cmd("exit")
        self.ssx.cmd("enable")
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")

        self.failUnless(status,"Failed testcase Global_cli_015.py")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_015)
    test_runner().run(suite)
