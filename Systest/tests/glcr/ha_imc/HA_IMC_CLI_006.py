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

DESCRIPTION: To check if the imc switchover  doesn.t affect the Context Created
TEST MATRIX: 4.6B2_HA-IMC.xls
TEST CASE  : HA_IMC_CLI_006
TOPOLOGY   : GLC-R Setup 

HOW TO RUN : python2.5 HA_IMC_CLI_006.py
AUTHOR     : rajshekar@stoke.com
REVIEWER   : 

"""

import sys, os, commands
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from CISCO import *
from Linux import *
from ixia import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import *
from misc import *
from glcr import *
from lanlan import *

#Import config and topo files
from config import *
from topo import *
from cleanUpCisco import test_cleanUpCisco

## Threading the processes
from threading import Thread

class testIt(Thread):
   threadLog = getLogger()
   def __init__ (self,myHandle, file):
        Thread.__init__(self)
        self.ssxHandle = myHandle
	self.file = file
        self.status = -1

   def run(self):
        # Let me run the thread, so I no need to
        # wait till it loads the configuration.
        self.threadLog.info("Loading the bulk configuration for the file %s"%self.file)
        self.ssxHandle.cmd("load configuration %s"%self.file, timeout=30000)
        self.status = 1

class test_HA_IMC_CLI_006(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
	self.myLog.info(__doc__)
        self.Resp = SSX(ssx_resp["ip_addr"])

	#Initiate the telnet session
	self.Resp.telnet()
        
	# Load minimum configuration 
        self.Resp.load_min_config(ssx_resp["hostname"])
	
        #Clear config and health stats
        self.Resp.clear_ports()
        self.Resp.clear_context_all()
        self.Resp.clear_health_stats()
	self.Resp.wait4cards()
	
    def tearDown(self):

        # Close the telnet sessions
	self.Resp.close()

    def test_HA_IMC_CLI_006(self):

        self.myLog.output("\n**********starting the test**************\n")
        IMC_Switch = 0
        Card_Reset = 0
        Card_Restart= 0
                
        self.myLog.info("\n\n######## Creating new context before IMC-switchover####### \n\n")
        self.Resp.cmd("end")
        self.Resp.cmd("conf")
        self.Resp.cmd("cont DelMe") 

        #================== Do imc-switchover
        self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
        self.Resp.imc_switchover_mgmt("system imc-switchover")
        IMC_Switch = IMC_Switch + 1
        Card_Reset = Card_Reset + 1

        self.myLog.info("\n\n######## Verify context creation not effected after IMC-switchover ##### \n")
        out = self.Resp.cmd("show context all")
        if "DelMe" not in out :
           self.fail("Context \"DelMe\" is deleted after IMC-switchover")

        # Verify the IMC0 is Active
        cardSta = self.Resp.cmd('show card 0 | grep  "Running\(Active\)"')
        if len(cardSta) == 0 :
           self.Resp.imc_switchover_mgmt("system imc-switchover")
           IMC_Switch = IMC_Switch + 1
           Card_Reset = Card_Reset + 1
           self.Resp.wait4cards()

        # Verify the GLCR status
        glcrOp = get_glcr_status(self.Resp)
        if int(glcrOp['standby']) != 4:
                self.Resp.cmd("system glc-switchback")
                Card_Restart = Card_Restart + 1
                time.sleep(10)
                self.Resp.wait4cards()

        # Checking SSX Health
        hs1 = self.Resp.get_health_stats()
        self.failUnless(is_healthy(hs1,Card_Reset=Card_Reset,Card_Restart=Card_Restart,IMC_Switch=IMC_Switch), "Platform is not healthy -Responder")
        hs2 = self.Ini.get_health_stats()
        self.failUnless(is_healthy( hs2), "Platform is not healthy at Initiator - Remote peer")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_HA_IMC_CLI_006)
        test_runner().run(suite)

