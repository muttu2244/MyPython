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

Description: -  Verify  session authentication with RADIUS database using in-valid X-auth credentials
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-024

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

How to run: "python2.5 AAA_FUN_024.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Ramesh - ramesh@primesoftsolutionsinc.com
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

class test_AAA_FUN_024(test_case):

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

        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()
	self.ether_radius1.close()
    def test_AAA_FUN_024(self):
        """
        Test case Id: -  AAA-FUN-024
        """

        #Push the SSX configuration        
	self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['fun_024_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['fun_024_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        #### Ethereal cap
        self.myLog.output(" Step 1 - removing the file aaa_fun_024.pcap")
        self.ether_radius1.cmd("sudo rm aaa_fun_024.pcap -f")

        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in file ")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w  aaa_fun_024.pcap -R "radius" & '% topo.port_ssx_radius1[1])
        self.ether_radius1.cmd(' sudo ls -lrt *.pcap')
	
	# Initiate IKEv1 session from a client to the SSX with invalid X-auth credentials.
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	self.failUnless(not ping_output, "Session established even with invalid X-auth credentials")
        
	self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")

	time.sleep(8)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        #ll_output = self.ether_radius1.cmd("ll")
        #self.failUnless( 'aaa_fun_024.pcap' in  ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file aaa_fun_024.pcap ")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r aaa_fun_024.pcap -R "radius.code == 3" ',timeout = 30)
        self.failUnless(output, """ Expected - packet with radius.code == 3  Actual = %s"""% output)

        #In debug messages verify whether the X-auth authentication is succeeded or not.
	# With in-valid X-auth credentials
        op_debug =  aaa_verify_authentication(self.ssx,"invalidxauthuser@%s" %script_var['context'],"radius")
        self.failUnless(not op_debug, "X-auth passed even with invalid credentials")


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_AAA_FUN_024)
    test_runner(stream=sys.stdout).run(suite)
    
