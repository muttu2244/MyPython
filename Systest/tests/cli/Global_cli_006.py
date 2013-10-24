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

DESCRIPTION: Executes all show commands during an GLC switch-Over
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_006

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_006"
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

class test_Global_Cli_006(test_case):
    """ 
    Description: Compare Show command CLI output  all show commands during an GLC switchover and switchback
    """

    myLog = getLogger()
    def setUp(self):

        self.ssx = SSX(ssx['ipaddr'])
        #Establish a telnet session to SSX with 4.6B2
        self.ssx.telnet()

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_006(self):
        """
        Test case Id:  -  Global_Cli_006,
        Description :  -  Compare Show command CLI output  all show commands during an
                           GLC switchover and switchback
        """
        
        switch_over = False
        switch_back = True
        for cmd in cmd_list:
            #perform imc switchover 
            if not switch_over:                 
                self.ssx.cmd("reload card 2")
                switch_over = True
            
           
            if self.ssx.get_glc_status(slot = "2")[0]: 
                switch_over = False
                cmd_list.append(cmd)
                continue

            self.ssx.cmd(cmd)
            self.ssx.cmd("show syscount")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_006)
    test_runner().run(suite)


