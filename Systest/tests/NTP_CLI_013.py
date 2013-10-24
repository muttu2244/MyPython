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

DESCRIPTION: Verify that configured NTP profile can be disabled
TEST PLAN:NTP CLI Test plans
TEST CASES: NTP_CLI_013

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            17.1.1.1/24  ---------------->     17.1.1.10/24                     |
       |                                                                                |
       |              e3                                         Port 3/1               |
         --------------------------------------------------------------------------------


HOW TO RUN: python2.5 NTP_CLI_013.py
AUTHOR: nkasera@stoke.com
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
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy,diff_in_time_ssx
import re
from misc import *

#import configs file and topo file
from ntp_config import *
from topo import *



class test_NTP_CLI_013(test_case):
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

    def test_NTP_CLI_013(self):

	 #vgroup b/w NTP client and NTP server
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring interface on linux machine

	self.myLog.output("==================Starting The Test====================")

	self.ssx.cmd("config")
        self.ssx.cmd("context %s"%var_dict['context_name'])
        self.ssx.cmd("ntp profile")
        self.ssx.cmd("exit")
        self.ssx.cmd("end")

        #Changing context from local
        op = self.ssx.cmd("sh config")
	print op.splitlines()

        if "ntp profile" in op:
                self.myLog.output("NTP profile configured")
        else:
                self.failIf(True, "NTP profile not configured")
	time.sleep(3)
	self.myLog.output("==================Disabling ntp profile====================")

        self.ssx.cmd("config")
        self.ssx.cmd("context %s"%var_dict['context_name'])
        self.ssx.cmd("no ntp profile")
        self.ssx.cmd("exit")
        self.ssx.cmd("end")

        #Changing context from local
        op = self.ssx.cmd("sh config")

	if "ntp profile" not in op:
                self.myLog.output("NTP profile disabled")
        else:
                self.failIf(True, "NTP profile not disabled")

	
	# Push NTP configuration on NTP client 
	#self.ssx.config_from_string(script_var['common_ssx'])
	#self.ssx.cmd("end")
	
	# Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_NTP_CLI_013)
	test_runner(stream=sys.stdout).run(suite)

