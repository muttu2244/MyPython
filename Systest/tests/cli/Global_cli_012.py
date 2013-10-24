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

DESCRIPTION: Verifies that GLC processes pppd and pppoe,and IMC processes pppdmc and pppoedmc do not appear in output from show process command
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_012

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_012"
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

class test_Global_Cli_012(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
       

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_012(self):
        switch_over = True
        status = True

        for i in range(0,5):
            ret1 = self.ssx.cmd("show process slot %s | grep pppd" %i)
	    ret2 = self.ssx.cmd("show process slot %s | grep pppoe" %i)
	    ret3 = self.ssx.cmd("show process slot %s | grep pppdmc" %i)
	    ret4 = self.ssx.cmd("show process slot %s | grep pppoedmc" %i)

            for line in ret1.split("\n"):
                if "pppd" in line:
                      self.myLog.output("Error: GLC process pppd appeared")
                      status = False
            for line in ret2.split("\n"):
                if "pppoe" in line:
                      self.myLog.output("Error: GLC process pppoe appeared")
                      status = False
            for line in ret3.split("\n"):
                if "pppdmc" in line:
                      self.myLog.output("Error: IMC process pppdmc appeared")
                      status = False
            for line in ret4.split("\n"):
                if "pppoedmc" in line:
                      self.myLog.output("Error: IMC process pppoedmc appeared")
                      status = False
	    
        self.failUnless(status,"Failed testcase Global_cli_012.py")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_012)
    test_runner().run(suite)
