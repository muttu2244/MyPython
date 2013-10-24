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

Description: -  Verify that SSX consults databases as per the method list
                when the primary database in the method list is non-responsive.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-025

TOPOLOGY DIAGRAM:

    (Linux)                              (SSX)                               (Linux)
    -------                             --------                          --------------
   |Takama | --------------------------|        |------------------------| qa-svr4      |
    -------                            |        |                         --------------
                                       |        |
                                       |Lihue-mc|
  (Netscreen)                          |        |                            (Linux)
    ------                             |        |                          --------------
   |qa-ns | --------------------------|        |-------------------------| qa-svr3      |
    ------                             |        |                          --------------
                                        --------

How to run: "python2.5 AAA_FUN_025.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Ramesh - ramesh@primesoftsolutionsinc.com
REVIEWER:
"""


### Import the system libraries we need.
import sys, os

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import *
from SSX import SSX
from NS import NS
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *

#import configs file
from aaa_config import *
from topo import *

class test_AAA_FUN_025(test_case):

    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx1['ip_addr'])
        self.ssx.telnet()

        # Clear SSX configuration
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
        self.ns5gt.telnet()

        # Clear SSX configuration
        self.ns5gt.clear_config()

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()

    def test_AAA_FUN_025(self):

        """
	Test case Id: -  AAA-FUN-025
	"""

        #On SSX configure an AAA profile with the session authentication set to query local database
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['fun_025_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['fun_025_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")


	# Initiate IKEv1 session from a client to the SSX with valid session credentials.

        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")

        op_debug =  aaa_verify_authentication(self.ssx,"aggr@%s" %script_var['context'],"local")
        self.failUnless(op_debug, "phase-1 session authentication and establishment is not successful")

	time.sleep(19)

        #Verify successful Phase1 authentication and  IKEv1 session establishedment
        op_debug =  aaa_verify_authentication(self.ssx,"aggr@%s" %script_var['context'],"local")
        self.failUnless(op_debug, "phase-1 session authentication and establishment is not successful")
        op_debug =  aaa_verify_authentication(self.ssx,"user1@%s" %script_var['context'],"local")
        self.failUnless(op_debug, "X-auth not successful")

        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(sa_output,"SA not loaded")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")
						
if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_AAA_FUN_025)
    test_runner(stream=sys.stdout).run(suite)
    
