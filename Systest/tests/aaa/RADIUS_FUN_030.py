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

Description: - Verify that the correct terminate cause type is reflected 
	 in the Accounting-request (stop) when the session is terminated.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-030

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

How to run: "python2.5 RADIUS_FUN_030.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Raja rathnam - rathnam@primesoftsolutionsinc.com
	
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

class test_RADIUS_FUN_030(test_case):

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

    def test_RADIUS_FUN_030(self):

        """
        Test case Id: -  RADIUS-FUN-030
        Description: - Verify that the correct terminate cause type is reflected 
		 in the Accounting-request (stop) when the session is terminated.
        """

	self.myLog.output("\n**********start the test**************\n")
	
	# Configure SSX to forward session authentication & session accounting 
	# credentials to radius server for authentication.
	self.ssx.config_from_string(script_var['common_ssx1'])
	self.ssx.config_from_string(script_var['rad_fun_030_ssx'])

	# Configure the IKEv1 Phase1 & Phase2 Polices on the SSX. 
	# Ensure that the client is also configured with matching policies.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_030_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
	# Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug") 


        self.myLog.output(" Step 1 - removing the file rad_fun_030.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_030.pcap -f")

        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_030.pcap  & '% topo.port_ssx_radius1[1])

        # Initiate IKEv1 session from a Netscreen to the SSX
        # ping ikev1 clent from ssx
        self.ssx.ping('%s'% script_var['ns_phy_ip'])
        time.sleep(5)
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        time.sleep(5)

        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output,"session authentication with Radius is not\
                        successed even with valid session credentials")
       
        #Clear the sessions
        self.ssx.cmd("context %s" %script_var['context'])
        self.ssx.cmd("clear session all")

        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
	time.sleep(10)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless("rad_fun_030.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

	# Read the contents of the pcap file 
        self.myLog.output (" Step 4 - read the content of the file rad_fun_030.pcap")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_030.pcap -R "radius.Acct_Terminate_Cause  == 6"',timeout = 30)

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_030)
    test_runner(stream=sys.stdout).run(suite)

