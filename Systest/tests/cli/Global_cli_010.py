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

DESCRIPTION: Executes all show commands and verify the nitrox keyword in the output
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_010

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_010"
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

class test_Global_Cli_010(test_case):
    """ 
    Description: Executes all show commands and verify the nitrox keyword in the output
    """

    myLog = getLogger()
    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
        
    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_010(self):
        """
        Test case Id: -  Global_Cli_010,
        Description:  -  Executes all show commands and verify the nitrox keyword in the output
        """
        switch_over = True
        status = True
        for cmd in cmd_list:
            ret = self.ssx.cmd(cmd)
            for line in ret.split():
                obj = re.compile("nitrox",re.I)
                m = obj.search(line)
                if m:
                    self.myLog.output("Error: Nitrox present in command \'%s\'" %cmd)
                    status = False
                    break
            
        self.failUnless(status,"Failed testcase Global_cli_010.py")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_010)
    test_runner().run(suite)


