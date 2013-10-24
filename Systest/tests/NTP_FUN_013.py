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

DESCRIPTION: Configure the SSX with NTP server. Manually change the Configure the SSX with NTP server. Manually change the SSX. clock and reload SSX. restart time same  as we set manually clock.
TEST PLAN: NTP Test plans
TEST CASES: NTP_FUN_013

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------
       |                                                                                |
       |                LINUX                            SSX                            |
       |          2.2.2.3/24     ------------>      2.2.2.45/24                         |
       |                                                                                |
       |              e1                              Port 2/1                          |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_013.py
AUTHOR:rajshekar@primesoftsolutionsinc.com  
REVIEWER:sudama@primesoftsolutionsinc.com

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
from misc import *

#import config and topo file
from ntp_config import *
from topo import *



class test_NTP_FUN_013(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_NTP_FUN_013(self):

	# Push NTP configuration on NTP client 
	self.ssx.config_from_string(script_var['NTP_FUN_012'])

	#Setting time on SSX (YYYY:MM:DD:HH:MIN:SS).
	Clock_out = self.ssx.cmd("show clock ")

	Clock_out=  Clock_out.split()[4].split(":")[0]
	Clock_out = int(Clock_out) +1

	self.ssx.cmd("clock set 2008:01:21:%s:50:34"%Clock_out)
	self.ssx.cmd("show clock")
	
	#Reload SSX
	self.ssx.cmd("reload")
	self.ssx.cmd("yes")
	Clock_out_reload = self.ssx.cmd("show version")
	Clock_out_in_hour =int(Clock_out_reload.split("\n")[9].split()[6].split(":")[0])
	Clock_out_in_minu =int(Clock_out_reload.split("\n")[9].split()[6].split(":")[1])

	if Clock_out_in_minu in range(57,60):
		Clock_out_in_hour = Clock_out_in_hour +1

	self.failUnless(Clock_out == Clock_out_in_hour , "TEST FAILED")
 
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
	suite.addTest(test_NTP_FUN_013)
	test_runner(stream=sys.stdout).run(suite)

