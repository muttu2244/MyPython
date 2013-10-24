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

Description: - Delete AAA profile from the SSX with sessions established. 
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-NEG-002

TOPOLOGY DIAGRAM:

    (Client)                             (SSX)                             (Linux)
    -------                             --------                         -------------
   |Takama | --------------------------|Lihue-mc|-----------------------|Radius Server|
    -------                             --------                         -------------
                               Port 4/0           Port 3/0


How to run: "python2.5 AAA_NEG_002.py"
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


class test_AAA_NEG_002(test_case):

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
	self.ns5gt.clear_config()	

        #Establish a telnet session to the linux client box.
        self.linux = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.linux.telnet()

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()

    def test_AAA_NEG_002(self):
        """
        Test case Id: -  AAA-NEG-002
        """

        #On SSX configure an AAA profile with the session authentication set to query local database.
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['user_add_ssx'])
        self.ssx.config_from_string(script_var['neg_002_ssx'])

        # Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['neg_002_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate Telnet Session from linux Client with valid user-1 credentials
        # where user is having admin privileges
        op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],
					"user3@%s"%script_var['context'],"123user3")
        self.failUnless(op_telnet is True,"telnet from client to SSX failed")

        # Checking user authentication is sucesscuful or not with valid user-1 credentials
        op_debug =  aaa_verify_authentication(self.ssx,"user3@%s"%script_var['context'],"local")
        self.failUnless(op_debug,"telnet from client to SSX failed")


	# Initiate IKEv1 session from a client to the SSX with valid session credentials.
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output, " IKEv1 session from client to SSX with valid session credentials is unsucessfull ")

        op_debug =  aaa_verify_authentication(self.ssx,"user1@%s"%script_var['context'],"radius")
        self.failUnless(op_debug,"Session authentication from client to SSX failed")


	# Deleting the AAA profile on the SSX
	self.ssx.configcmd("context %s" %script_var["context"])
	self.ssx.configcmd("no aaa profile")

	####################### Re-initiate the sessions.#########################

        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	# Flush ike sessions
	self.ssx.cmd("context %s" %script_var["context"])
	self.ssx.cmd("clear session all")

        # Initiate Telnet Session from linux Client with valid user-1 credentials
        # where user is having admin privileges
        op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],
                                        "user4@%s"%script_var['context'],"123user4")
        self.failUnless(op_telnet is True,"telnet from client to SSX failed")

        # Checking user authentication is sucesscuful or not with valid user-1 credentials
        op_debug =  aaa_verify_authentication(self.ssx,"user4@%s"%script_var['context'],"local")
        self.failUnless(op_debug,"telnet from client to SSX failed")


	# Initiate IKEv1 session
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(not ping_output,"SSX respond to the session request coming into that context ater deleting the context")

        #op_debug =  aaa_verify_authentication(self.ssx,"user1@%s"%script_var['context'],"radius")
        #self.failUnless(not op_debug,"Session authentication from client to SSX failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_AAA_NEG_002)
    test_runner().run(suite)
    
