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

DESCRIPTION: Verifies the output changes as mentioned in the SFS for following commands
TEST PLAN:   Global_Cli_TestPlan
TEST CASES:  Global_Cli_001

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_Cli_001"
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

class test_Global_Cli_001(test_case):
    """ 
    Description: Verifies the output changes as mentioned in the SFS for following commands
    .	Show card
    .	Show hardware
    .	Show port
    .	Show port with redundancy option
    .	Show port details
    .	Show port details with redundancy option
    .	show port counters drop
    .	show fast-path counters
    .	show process
    .	show process cpu
    .	show environmental detail

    """

    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX(ssx['ipaddr'])
        self.ssx.telnet()
       

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_Global_Cli_001(self):
        """
        Test case Id: -  Global_Cli_001,
        Description:  -  Verifies the output changes as mentioned in the SFS for following commands
        """
        switch_over = True
        status = True
	
        for i in range(2,5):
            ret = self.ssx.cmd("show card %s" %i)
            for line in ret.split("\n"):
                if "GLC" in line:
                    obj = re.compile("XGLC")
                    m = obj.search(line)
                    if not m:
                      self.myLog.output("Error: XGLC is not present in \'show card\' output")
                      status = False
                    obj = re.compile("4x10GBase-R")
                    m = obj.search(line)
                    if not m:
                      self.myLog.output("Error: 4x10GBase-R is not present in \'show card\' output")
                      status = False

        ret = self.ssx.cmd("show hardware")
        for line in ret.split("\n"):
            if "4x" in line:
                modelName = line.split("Model Name:")[1].split()[0].strip()
                print modelName
                if '4x10GBase-R' not in modelName:
                    self.myLog.output("Error: 4x10GBase-R is not present in \'show hardware\' output")
                    status = False

        portList = ["2/0","2/1","2/2","2/3","3/0","3/1","3/2","3/3","4/0","4/1","4/2","4/3"]

        for port in portList:
            ret = self.ssx.cmd("show port | grep %s" %port)
            for line in ret.split("\n"):
                if port in line:
                    outList = line.split()
                    if "10G" not in outList[4]:
                        self.myLog.output("Error: 10G not present in speed for port %s" %port)
                        status = False
                    if "SFP+" not in outList[6]:
                        self.myLog.output("Error: SFP+ not present in speed for port %s" %port) 
                        status = False
                    if "SR" not in outList[7]:
                        self.myLog.output("Error: SR not present in speed for port %s" %port) 
                        status = False
	portList = ["2/0","2/1","3/0","3/1","4/0","4/1"]
        for port in portList:
            ret = self.ssx.cmd("show port %s redundancy" %port)
            for line in ret.split("\n"):
                if port in line:
                    outList = line.split()
                    if "10G" not in outList[4]:
                        self.myLog.output("Error: 10G not present in speed for port %s" %port)
                        status = False
                    if "SFP+" not in outList[6]:
                        self.myLog.output("Error: SFP+ not present in speed for port %s" %port) 
                        status = False
                    if "SR" not in outList[7]:
                        self.myLog.output("Error: SR not present in speed for port %s" %port) 
                        status = False        
	
	portList = ["2/0","2/1","3/0","3/1","4/0","4/1"]
	for port in portList:
            ret = self.ssx.cmd("show port %s detail" %port)
	    sep = ret.split("\n")
            if "Up" not in sep[3]:
	    	if "Down" not in sep[3]:
			self.myLog.output("Error: Link state is not present in speed for port %s" %port)
                   	status = False

            if "SFP+" not in sep[5]:
 	           self.myLog.output("Error: SFP+ not present in speed for port %s" %port)
                   status = False

            if "10GBASE-SR" not in sep[9]:
 	           self.myLog.output("Error: SR not present in speed for port %s" %port)
                   status = False
		
        portList = ["2/0","2/1","3/0","3/1","4/0","4/1"]
        for port in portList:
            ret = self.ssx.cmd("show port %s detail redundancy" %port)
            sep = ret.split("\n")
            if "Up" not in sep[3]:
                if "Down" not in sep[3]:
                        self.myLog.output("Error: Link state is not present in speed for port %s" %port)
                        status = False

            if "SFP+" not in sep[5]:
                   self.myLog.output("Error: SFP+ not present in speed for port %s" %port)
                   status = False

            if "10GBASE-SR" not in sep[9]:
                   self.myLog.output("Error: 10GBASE-SR not present in speed for port %s" %port)
                   status = False
	
        for i in range(2,5):
            ret = self.ssx.cmd("show process internal slot %s" %i)
            sep = ret.split("\n")
            if "Io-pkt" not in sep[3]:
		self.myLog.output("Error: Io-pkt is not present for port %s" %port)
            	status = False
            if "NSM" not in sep[9]:
                self.myLog.output("Error: NSM is not present for port %s" %port)
                status = False
            if "Iked" not in sep[12]:
                self.myLog.output("Error: Iked is not present for port %s" %port)
                status = False
	  
        for i in range(2,5):
            ret = self.ssx.cmd("show environmental %s" %i)
            sep = ret.split("\n")
            if "Data polling interval is 60 second(s)" not in sep[2]:
                self.myLog.output("Error: Data polling interval not present for port %s" %port)
                status = False
            if "Voltage readings" not in sep[4]:
                self.myLog.output("Error: Voltage readings not present for port %s" %port)
                status = False
            if "Temperature readings" not in sep[35]:
                self.myLog.output("Error: Temperature readings not present for port %s" %port)
                status = False


        self.failUnless(status,"Failed testcase Global_cli_001.py")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_Cli_001)
    test_runner().run(suite)


