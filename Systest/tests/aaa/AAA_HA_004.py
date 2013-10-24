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

DESCRIPTION: Covers HA related test cases from AAA test plan
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-HA-004

TOPOLOGY DIAGRAM:

    (Linux)                              (SSX)                               (Linux)
    -------                             --------                          --------------
   |Takama | --------------------------|        |------------------------| qa-svr4      |
    -------                            |        |                         --------------
                                       |        |
                                       |Lihue-mc|
  (Netscreen)                          |        |                            (Linux)
    ------                             |        |                          --------------
   |qa-ns1 | --------------------------|        |-------------------------| qa-svr3      |
    ------                             |        |                          --------------
                                        --------


How to run: "python2.5 AAA_HA_004.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
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

class test_AAA_HA_004(test_case):

    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx2_ha['ip_addr'])
	self.ssx.telnet()
	self.ssx.clear_health_stats()

	# Clear SSX configuration 
	self.ssx.clear_config()

        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns1['ip_addr'])
	self.ns5gt.telnet()
        self.ssx.clear_health_stats()

        # Clear SSX configuration
	self.ns5gt.clear_config()	

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()

    def test_AAA_HA_004(self):

        """
        Test case Id: -  AAA-HA-004
        Description: - Verify session authentication with local database using valid credentials.
        """
        #Push the SSX configuration
        self.ssx.config_from_string(script_var['aaa_ha_004_ssx'])

        #Push the Netscreen configuration
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['aaa_ha_004_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	# Initiate IKEv1 session from a netscreen to the SSX with valid session credentials.
	# 1st ping used to get rid of any arp learnings
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	self.failUnless(ping_output,"session authentication and establishment is not successful")

	#Verify successful Phase1 authentication and  IKEv1 session establishedment
        #op_debug =  aaa_verify_authentication(self.ssx,"aggr@%s"%script_var['context'],"local")
        #self.failUnless(op_debug,"verifying in debug:session authentication and establishment is not successful")

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
    suite.addTest(test_AAA_HA_004)
    test_runner().run(suite)
    
