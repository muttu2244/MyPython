#!/usr/bin/env python2.5

#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : tests cli of 'rtr' rlated commands
AUTHOR                  : venkat 'krao@stoke.com'
"""


### Importing system libraries
import sys, os, re
import time
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### Importing libraries from the python framework
from log import buildLogger
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner
from SSX import SSX
from helpers import is_healthy

### Importing topo file and Config file

import pexpect
import topo

class cli_conf_rtr(test_case):

    myLog = getLogger()

    def setUp(self):

        #Establish telnet session for connecting to SSX and checking its status
        self.myLog.output("Trying to connect to SSX ")
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        self.ssx.clear_health_stats()

    def tearDown(self):
        #Closing down the telnet sessions
        self.ssx.close()

    def test_rtr(self):

	self.myLog.info("Test Started .........")
	self.myLog.info("Executing the command \"cli-driver.pl  -C rtr -i context_local -z -2 -c %s\" ......" %topo.ssx_con['ip_addr'])
	cliOutput = pexpect.run("cli-driver.pl  -C rtr -i context_local -z  -2 -c %s" %topo.ssx_con['ip_addr'])

	try:
		self.myLog.info("Press <ctrl-c> if script hang more than 20 seconds)")
	        # Checking SSX Health
	        hs = self.ssx.get_health_stats()
	        self.failUnless(is_healthy(hs, Warn_logs=100), "Platform is not healthy")
	except:
	        self.failUnless(0, "SSX CRASH/HANG observed.....")
		self.myLog.info("cliOutput %s" %cliOutput)

	#self.myLog.info("cliOutput %s" %cliOutput)

if __name__ == '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True,console=True)
    #log = buildLogger(filename, debug=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_conf_rtr)
    test_runner(stream=sys.stdout).run(suite)

