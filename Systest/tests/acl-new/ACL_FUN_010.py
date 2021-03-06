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

DESCRIPTION:To Test to check that SSX allows sessions to be established when empty ACL is applied to a session name. Test to check that data traffic is not allowed through the session
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUN_010

HOW TO RUN:python2.5 ACL_FUN_010.py
AUTHOR: jayanth@stoke.com

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
from acl import *
from helpers import is_healthy
from misc import *

#import config and topo file
from config import *
from topo import *



class test_ACL_FUN_010(test_case):
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

    def test_ACL_FUN_010(self):

	# Push SSX config
	self.ssx.cmd("clear session all")
	self.ssx.config_from_string(script_var['ACL_FUN_010'])
	#self.linux.write_to_file(script_var['FUN_032_XPM'],"autoexec.cfg","/xpm/")

        self.ssx.cmd("context %s" %(script_var['context_name']))

	self.linux.write_to_file(script_var['ACL_FUN_XPM_common'],"autoexec.cfg","/xpm/")

	self.linux.cmd("cd /xpm")
	self.linux.cmd("sudo ./start_ike")

	time.sleep(10)

	output=self.ssx.cmd("show session counters")
	
	
        self.failUnless(output,"Failed to Establish Session When Empty ACL is applied to a session")


	self.linux.cmd("exit")

	# Checking SSX Health 
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_010)
        test_runner(stream = sys.stdout).run(suite)

