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

Description: - Verify that the SSX sends a session Accounting-off 
		request when it is reloaded . 
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-028

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

How to run: "python2.5 RADIUS_FUN_028.py"
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

class test_RADIUS_FUN_028(test_case):

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


	# telnet used for tethereal to capture messages
        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],
                                        radius1['password'])
        self.ether_radius1.telnet()


    def tearDown(self):
        """Clear the config and Close down the telnet session."""

        self.ssx.close()
	self.ether_radius1.close()

    def test_RADIUS_FUN_028(self):

        """
        Test case Id: -  RADIUS-FUN-028
        """

	self.myLog.output("\n**********start the test**************\n")
	
	# Configure SSX to forward session accounting-requests 
	# to radius server for accounting .
	self.ssx.config_from_string(script_var['common_ssx1'])
	self.ssx.config_from_string(script_var['rad_fun_028_ssx'])
        
        self.myLog.output(" Step 1 - removing the file rad_fun_028.pcap")
        self.ether_radius1.cmd("rm rad_fun_028.pcap -f")

        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in file x")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_028.pcap -R "radius" & '% topo.port_ssx_radius1[1])

        # Reload the SSX
        self.ssx.reload_device()

	#### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
	time.sleep(5)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_028.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output (" Step 4 - read the content of the file rad_fun_028.pcap")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_028.pcap -R "radius.Acct_Status_Type == 8"',timeout = 30)
        self.failUnless("RADIUS" in  output, " Expected - packet with (off)radius.Acct_Status_Type == 8")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_028)
    test_runner().run(suite)

