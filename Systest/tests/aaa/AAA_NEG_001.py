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

Description: - Delete context including the AAA profile from the SSX with sessions established .
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-NEG-001

TOPOLOGY DIAGRAM:

    (Client)                             (SSX)                             (Linux)
    -------                             --------                         -------------
   |Takama | --------------------------|Lihue-mc|-----------------------|Radius Server|
    -------                             --------                         -------------
                               Port 4/0           Port 3/0


How to run: "python2.5 AAA_NEG_001.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com	
	Raja rathnam - rathnam@primesoftsolutionsinc.com
REVIEWER:
"""

# Import the system libraries we need.
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

class test_AAA_NEG_001(test_case):

    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx1['ip_addr'])
        self.ssx1 = SSX(ssx1['ip_addr'])
	self.ssx.telnet()
	self.ssx1.telnet()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        # Clear SSX configuration
	self.ssx.clear_config()

        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
	self.ns5gt.telnet()
	self.ns5gt.clear_config()	

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ssx1.close()
        self.ns5gt.close()

    def test_AAA_NEG_001(self):
        """
        Test case Id: -  AAA-NEG-001
        """

        #On SSX configure an AAA profile with the session authentication set to query local database..
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['neg_001_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['neg_001_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate IKEv1 session from a client to the SSX with valid session credentials.
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output, "PING FAILED")

        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(sa_output,"SA established successfully")

        op_debug = aaa_verify_authentication(self.ssx,"aggr@%s"%script_var['context'],"local")
        self.failUnless(op_debug, "session is not successful")

	#Delete the context along with the AAA profile from SSX.
	self.ssx.configcmd("no context %s" %script_var['context'])

        # Re-initiate IKEv1 session from a client to the SSX with valid session credentials.
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(not ping_output, "Session authentication occurred even after deleting the context")
	
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")
	

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True,console=True)

    suite = test_suite()
    suite.addTest(test_AAA_NEG_001)
    test_runner().run(suite)
    
