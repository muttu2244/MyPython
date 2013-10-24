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

Description: - Verify the SSX behavior when session authentication database is changed from local to Radius
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-030

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

How to run: "python2.5 AAA_FUN_030.py"
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

class test_AAA_FUN_030(test_case):

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

	"""Establish a telnet session to the Linux client box."""
        self.linux = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"]) 
	self.linux.telnet()

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
	self.ssx.close()
        self.ns5gt.close()
	self.linux.close()        

    def test_AAA_FUN_030(self):

        """
        Test case Id: -  AAA-FUN-030
	"""
        #On SSX configure an AAA profile with the session authentication set to Local and 
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['fun_030_ssx'])
        self.ssx.config_from_string(script_var['user_add_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['fun_030_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")


	# Initiate IKEv1 session from a client to the SSX with valid session credentials.
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	self.failUnless(ping_output, "Session authentication and establishment with local was not successful")

	#Verify successful Phase1 authentication and  IKEv1 session establishedment
	op_debug =  aaa_verify_authentication(self.ssx,"aggr@%s"%script_var['context'],"local")
        self.failUnless(op_debug, "Verifyiing in debugs:session local authentication and establishment is not successful")

        #Check the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(sa_output,"SA not loaded")

	#Deleting old SA
        self.ssx.cmd("context %s" %script_var['context'])
        self.ssx.cmd("clear session all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")
	
	#change the session authentication from local to Radius
        self.ssx.configcmd("context %s" %script_var['context'])
	self.ssx.config_from_string("aaa profile\nsession authentication radius\n exit\n")

	#Re-Initiate IKEv1 session from a client to the SSX with valid session credentials.
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output, "Session authentication and establishment with Radius database is not successful")

	#Verify IKEv1 session authentication 
	op_debug =  aaa_verify_authentication(self.ssx,"user1@%s"%script_var['context'],"radius")
        self.failUnless(op_debug, "Verifying in debugs:session authentication and establishment with\
				   Radius database is not successful")

        #Check the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(sa_output,"SA not loaded")
				
	############ Repeating same for user authentication ######################
	#Deleting old SA
        self.ssx.cmd("context %s" %script_var['context'])
        self.ssx.cmd("clear session all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Detach the radius server from session auth profile and attach to user authentication profile
        self.ssx.configcmd("context %s" %script_var['context'])
        self.ssx.configcmd("radius session authentication profile")
        self.ssx.configcmd("no server %s port 1812 key topsecret" %script_var['radius1_ip'])
        self.ssx.configcmd("exit")
        self.ssx.configcmd("radius user authentication profile")
        self.ssx.configcmd("server %s port 1812 key topsecret" %script_var['radius1_ip'])
        self.ssx.configcmd("exit")

	# Initiate Telnet Session from Linux client  where user has adminstrator privileages
	op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],"user3@%s"%script_var['context'],"123user3")
        self.failUnless(op_telnet,"Telnet to SSX as a user was not succeeeded")

        # Check whether SSX quiries the local database for user authentication 
	op_debug =  aaa_verify_authentication(self.ssx,"user3@%s"%script_var['context'],"local")
        self.failUnless(op_debug,"The user authentication with local was not succeeded")

        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        self.ssx.configcmd("context %s" %script_var['context'])
	self.ssx.config_from_string("aaa profile\n user authentication radius\n exit")

	#Re-Initiate Telnet Session from Linux Client  where user has adminstrator privileages
	op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],"user4@%s"%script_var['context'],"123user4")
        self.failUnless(op_telnet,"Telnet to SSX as a user was not success")

        # Check whether SSX quiries the Radius database for user authentication 
	op_debug =  aaa_verify_authentication(self.ssx,"user4@%s"%script_var['context'],"radius")
        self.failUnless(op_debug,"Verifyiing in debugs:the user authentication with radius database was not succeeded ")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_AAA_FUN_030)
    test_runner().run(suite)
    
