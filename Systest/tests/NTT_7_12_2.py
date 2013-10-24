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

DESCRIPTION: Recover to Backup configuration
TEST PLAN: 
TEST CASES: NTT_7_12_2

HOW TO RUN:python2.5 NTT_7_12_2.py
AUTHOR: rajshekar@stoke.com
REVIEWER:

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from aaa import *
from acl import *
from helpers import is_healthy
from misc import *

#import config and topo file
from config_raja import *
from topo import *



class test_NTT_7_12_2(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

    def test_NTT_NTT_7_12_2(self):

	# Push SSX config
        self.myLog.info("\n\n Load the Configuration to SSX \n\n")
	self.ssx.config_from_string(script_var['SSX_7_12_1_1'])

        self.ssx.cmd("del /cfint/NTT_7_12_2.cfg noconf")
        self.ssx.cmd("del /hd/NTT_7_12_2.cfg noconf")

	# Saving Config To CF
        self.myLog.info("\n\n Save the Configuration to CF \n\n")
	self.ssx.cmd("save conf /cfint/NTT_7_12_2.cfg")
	cfload_conf=self.ssx.cmd("show conf")

        # Verify config loaded to DUT from CF and config in CF are same
        self.myLog.info("\n\n Verify config loaded to DUT from CF and config in CF are same \n\n")
	self.ssx.cmd("clear config")	
	self.ssx.cmd("load configuration /cfint/NTT_7_12_2.cfg")       
	running_conf = self.ssx.cmd("show config")
        cf_conf=self.ssx.cmd("show file /cfint/NTT_7_12_2.cfg")
        if  running_conf == cf_conf :
                output = 1
        else :
                output = 0
        self.failIf(output==0, "Config loaded to DUT from CF and config in CF are same") 
        self.myLog.info("\n\n Verified config loaded to DUT from CF and config in CF are same \n\n")
	
        self.ssx.cmd("del /cfint/NTT_7_12_2.cfg noconf")
        self.ssx.cmd("del /hd/NTT_7_12_2.cfg noconf")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
	#vgroup_new(vlan_cfg_linux)
        suite = test_suite()
        suite.addTest(test_NTT_7_12_2)
        test_runner(stream = sys.stdout).run(suite)

