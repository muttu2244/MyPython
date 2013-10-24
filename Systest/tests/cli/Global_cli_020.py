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

DESCRIPTION: Executes all show commands during an IMC switch-Over
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_020

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_020"
AUTHOR: Ganapathi 
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

class test_Global_Cli_020(test_case):
    """ 
    Description: Executes all show commands
    """

    myLog = getLogger()
    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
        


    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_020(self):
        """
        Test case Id: -  Global_Cli_020,
        Description:  -  Executes all show commands 
        """
        switch_over = True
        for cmd in cmd_list:
           #perform imc switchover 
           self.ssx.cmd(cmd)
           self.ssx.cmd("show syscount",timeout = 10000)

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_020)
    test_runner().run(suite)


