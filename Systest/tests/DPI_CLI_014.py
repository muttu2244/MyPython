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

DESCRIPTION: Configure DPI filters with maximum number of characters

TEST PLAN: DPI Test Plan
TEST CASES: DPI_CFG_14

TOPOLOGY DIAGRAM:
                      -NA- 

How to run: "python2.5 DPI-CLI-014.py"
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


import topo
from config import *


class test_DPI_CLI_014(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX
        self.ssx = SSX(topo.ssx["ipaddr"])
        self.ssx.telnet()
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        # Clear the SSX config
        self.ssx.clear_config()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

    def test_DPI_CLI_014 (self):

        self.myLog.output("\n**********Start the test**************\n")

	bigString = ["012345678912345", "012345678912345", "0123456789123456"]
	# Push SSX config
	self.ssx.config_from_string("context %s" % script_var['context'])
	for name in bigString:
 		outputCmd=self.ssx.config_from_string("filter dpi %s filter-protocol http" % (name))
		if name !=  bigString[2]:
			self.failUnless("ERROR" not in outputCmd, "Failed ... Unable to configure with %s" % name)
		else:
			self.failUnless("ERROR" in outputCmd, "Failed ... Able to configure with %s" % name)


	
	#for protocol in protocol_list:
 	#	self.failUnless( self.ssx.cmd("sh conf filter | grep %s" %  protocol), "Filter configuration failed for %s" % protocol )
			

	# Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_DPI_CLI_014)
    test_runner().run(suite)

