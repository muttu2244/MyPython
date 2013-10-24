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

Description: - Verify that the SSX sends a session Accounting-request
	 (stop) when session authentication fails on RADIUS server.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-024

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

How to run: "python2.5 RADIUS_FUN_024.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Raja Rathnam - rathnam@primesoftsolutionsinc.com
	
REVIEWER:
"""

import sys, os

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

class test_RADIUS_FUN_024(test_case):

    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1['ip_addr'])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
        self.ns5gt.telnet()
        self.ns5gt.clear_config()

        """Establish a telnet session to Linux machine ."""
        self.linux = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.linux.telnet()

        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()


    def tearDown(self):
        """Clear the config and Close down the telnet session."""

        self.ssx.close()
        self.ns5gt.close()
        self.linux.close()
	self.ether_radius1.close()

    def test_RADIUS_FUN_024(self):

        """
        Test case Id: -  RADIUS-FUN-022
        """

	self.myLog.output("\n**********start the test**************\n")

        self.myLog.output(" Step 1 - removing the file rad_fun_024.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_024.pcap -f")

        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_024.pcap & '% topo.port_ssx_radius1[1])

	# Configure SSX to forward session authentication credentials to 
	# local database and acct info to radius server  .
	self.ssx.config_from_string(script_var['common_ssx1'])
	self.ssx.config_from_string(script_var['rad_fun_024_ssx'])

	# Configure the IKEv1 Phase1 & Phase2 Polices on the SSX. 
	# Ensure that the client is also configured with matching policies.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_024_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
	# Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug") 


        # Initiate IKEv1 session from a Netscreen to the SSX (with invalid X-Auth user)
        # ping ikev1 clent from ssx
        self.ssx.ping('%s'% script_var['ns_phy_ip'])
        time.sleep(5)
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")

        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(not ping_output, "session established even with in-valid X-Auth user")
       
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
	time.sleep(5)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless("rad_fun_024.pcap" in ll_output,"Testcase FAILED because pcap file has not created")

        self.myLog.output (" Step 4 - read the content of the file rad_fun_024.pcap")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_024.pcap  -R "radius.Acct_Status_Type"',timeout = 30)
        self.failUnless("RADIUS" in output, " Expected - packet with radius.Acct.Status_Type == 4 ")


        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(not sa_output,"SA loaded even with invalid X-auth user")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_024)
    test_runner(stream=sys.stdout).run(suite)

