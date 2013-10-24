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

DESCRIPTION: Configure legacy QoS class using single DPI filter 

TEST PLAN: DPI Test Plan
TEST CASES: DPI_CFG_09	 

TOPOLOGY DIAGRAM:
                      -NA- 

How to run: "python2.5 DPI-CLI-009.py"
AUTHOR: Venkat - krao@stoke.com
REVIEWER:
"""
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import SSX
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

from dpi import *

import topo
from config import *


class test_DPI_CLI_009(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX
        self.ssx = SSX(topo.ssx["ipaddr"])
        self.ssx.telnet()
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        # Clear the SSX config
        #self.ssx.clear_config()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

    def test_DPI_CLI_009 (self):

        #self.myLog.info("\n**********Start the test**************\n")

	# Push SSX config
	self.ssx.config_from_string(script_var['DPI_CLI_009'])
	
	inputConfig = script_var['DPI_CLI_009']
        outputConfig = self.ssx.cmd("show configuration context %s" % script_var['context'])
	result = compareMultiStr(self.ssx, inputConfig, outputConfig)
        self.failUnless(result, "InputConfiguration is not matched with outputConfiguration")

	# Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_DPI_CLI_009)
    test_runner().run(suite)

