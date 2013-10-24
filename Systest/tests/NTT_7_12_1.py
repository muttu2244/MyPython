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

DESCRIPTION: Enable to store 2 generation of configuration 
TEST PLAN: 
TEST CASES: 7_12_1

HOW TO RUN:python2.5 7_12_1.py
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



class test_NTT_7_12_1(test_case):
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

    def test_NTT_7_12_1(self):

	# Push SSX config
        self.myLog.info("\n\n Load the Configuration to SSX \n\n")
	self.ssx.config_from_string(script_var['SSX_7_12_1_1'])

        self.ssx.cmd("del /cfint/7_12_1.cfg noconf")
        self.ssx.cmd("del /hd/7_12_1.cfg noconf")

	# Saving Config To CF
        self.myLog.info("\n\n Save the Configuration to CF \n\n")
	self.ssx.cmd("save conf /cfint/7_12_1.cfg")
	cfload_conf=self.ssx.cmd("show conf")

	#Configuring Interface with Different IP
        self.myLog.info("\n\n Changed the interface ip addredd to different one \n\n")
        self.myLog.info("\n\n Load the Configuration to SSX \n\n")
	self.ssx.config_from_string(script_var['SSX_7_12_1_2'])

	#Saving Config To DUT
        self.myLog.info("\n\n Save the Configuration \n\n")
	self.ssx.cmd("save conf /hd/7_12_1.cfg")

        # Verify saved config and the Config DUT has are same
        self.myLog.info("\n\n Verify saved config and the Config DUT has are same \n\n")
	running_conf=self.ssx.cmd("show conf")
	saved_conf=self.ssx.cmd("show file /hd/7_12_1.cfg")
	if running_conf == saved_conf :
		output = 1
	else :
		output = 0
	self.failIf(output!=1, "Confing Not Same As One On DUT")	
        self.myLog.info("\n\n Verified saved config and the Config DUT has are same \n\n")
	
        
        # Verify config in CF and Config saved to CF are same
        self.myLog.info("\n\n Verify config in CF and Config saved to CF are same \n\n")
	cf_conf= self.ssx.cmd("show file /cfint/7_12_1.cfg").strip()
	conf = "%s"%script_var['SSX_7_12_1_1'].strip()
        cf_confSplit = cf_conf.splitlines()
        confSplit = conf.splitlines()
        for index in range(0,len(cf_confSplit)) :
            if "%s"%confSplit[index] != "%s"%cf_confSplit[index] :
               output==0
        self.failIf(output==0, "Config in CF and Config saved to CF are not same")
        self.myLog.info("\n\n Verified config in CF and Config saved to CF are same \n\n")
 
        # Verify config loaded to DUT from CF and config in CF are same
        self.myLog.info("\n\n Verify config loaded to DUT from CF and config in CF are same \n\n")
	self.ssx.cmd("clear config")	
	self.ssx.cmd("load configuration /cfint/7_12_1.cfg")       
	running_conf = self.ssx.cmd("show config")
        cf_conf=self.ssx.cmd("show file /cfint/7_12_1.cfg")
        if  running_conf == cf_conf :
                output = 1
        else :
                output = 0
        self.failIf(output==0, "Config loaded to DUT from CF and config in CF are same") 
        self.myLog.info("\n\n Verified config loaded to DUT from CF and config in CF are same \n\n")
	
        self.ssx.cmd("del /cfint/7_12_1.cfg noconf")
        self.ssx.cmd("del /hd/7_12_1.cfg noconf")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
	#vgroup_new(vlan_cfg_linux)
        suite = test_suite()
        suite.addTest(test_NTT_7_12_1)
        test_runner(stream = sys.stdout).run(suite)

