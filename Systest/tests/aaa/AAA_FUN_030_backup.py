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

DESCRIPTION: Covers FUN related test cases from AAA test plan
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-030

TOPOLOGY DIAGRAM:

    (Client)                             (SSX)                             (Linux)
    -------                             --------                         -------------
   |Takama | --------------------------|Lihue-mc|-----------------------|Radius Server|
    -------                             --------                         -------------
                               Port 4/0           Port 3/0


How to run: "python2.5 AAA_FUN_030.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Ramesh - ramesh@primesoftsolutionsinc.com
REVIEWER:
"""


### Import the system libraries we need.
import sys, os

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### import the Stoke libraries we need.
from SSX import SSX
from NS import NS
from log import buildLogger
from StokeTest import test_case, test_suite, test_runner

### import topo and config files.
from config import *
from topo import *


class test_AAA_FUN_030(test_case):

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx1['ip_addr'])
        self.ssx.telnet()
        self.ssx.clear_config()

        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns1['ip_addr'])
        self.ns5gt.telnet()
        self.ns5gt.clear_config()

        """Establish a telnet session to the Xpress VPN client box."""
        linux1 = Linux(topo.linux_client["ip_addr"],topo.linux_client["user_name"],topo.linux_client["password"])
        self.linux_client.telnet()



    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()
	linux1.close()        
    def test_AAA_FUN_030(self):

        """
        Test case Id: -  AAA-FUN-030
        Description: - Verify the SSX behavior when session authentication database is changed from local to radius 
"""
        #On SSX configure an AAA profile with the session authentication set to Radius and 
	#user authentication set to query local database.
        self.ssx.config_from_string(script_var['common_ssx'])
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
	self.failUnless(ping_output, "session radius authentication and establishment with local database is not successful")

	#Verify successful Phase1 authentication and  IKEv1 session establishedment
	op_debug = self.ssx.aaa_verify_authentication("aggr@%s"%script_var['context'],"local")
        self.failUnless(op_debug, "Verifying in debugs:session radius authentication and establishment with local database\
				    is not successful")
	
	#Deleting old configuration
	self.cfg_from_str('''"context%s"script_var['context']\
			     clear session all 
				''')
	#change the session authentication from local to Radius
	self.cfg_from_str("aaa profile\ 
			session authentication radius\
	    	        service authorization radius
		     ")

	#Re-Initiate IKEv1 session from a client to the SSX with valid session credentials.
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output, "PING FAILED")

	#Verify successful Phase1 authentication and  IKEv1 session establishedment
	op_debug = self.ssx.aaa_verify_authentication("aggr@%s"%script_var['context'],"radius")
        self.failUnless(op_debug, "session Radius authentication and establishment is not successful")
				
	###################repeat this same case for user authentication also###########################################

	# Initiate Telnet Session from Xpress VPN Client  where user has adminstrator privileages
        op_telnet = self.linux1.generic_verify_telnet_2_ssx(script_var['ssx_phy_iface1_ip'],"user1@%s"%script_var['context'],"user1")
        self.failUnless(op_telnet is True,"telnet to SSX as a user was not success")

        # Check whether SSX queries the Radius database for user authentication 
	op_debug = self.ssx.aaa_verify_authentication("user1@local","local")
        self.failUnless(op_debug,"the user authentication with local database was  not successful ")
	#chage the session authentication from local to Radius
	self.cfg_from_str("context %s\
			aaa profile\
		        session authentication radius\
			service authorization radius" %script_var['context'])

	#Re-Initiate Telnet Session from Xpress VPN Client  where user has adminstrator privileages
        op_telnet = self.linux1.generic_verify_telnet_2_ssx(script_var['ssx_phy_iface1_ip'],"user1@%s"%script_var['context'],"user1")
        self.failUnless(op_telnet is True,"telnet to SSX as a user was not success")

        # Check whether SSX quiries the local database for user authentication 
	op_debug = self.ssx.aaa_verify_authentication("user1@local","radius")
        self.failUnless(op_debug,"the user authentication with Radius not success ")
	

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_AAA_FUN_030)
    test_runner().run(suite)
    
