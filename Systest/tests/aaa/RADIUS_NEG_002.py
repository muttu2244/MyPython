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

DESCRIPTION: Covers NEG related test cases from RADIUS test plan
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-NEG-002

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
How to run: "python2.5 RADIUS_NEG_002.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Raja Rathnam -rathnam@primesoftsolutionsinc.com
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
from Linux import Linux
from SSX import SSX
from aaa import *
from ike import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

# import configs file
from aaa_config import *
from topo import *

# python libraries
import time 

class test_RADIUS_NEG_002(test_case):
    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(topo.ssx1['ip_addr'])
	self.ssx.telnet()

        # CLear SSX configuration
	self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.xpress_vpn.telnet()

        # Establish a telnet session to the radius servers
        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.xpress_vpn.close()
	self.ether_radius1.close()
    def test_RADIUS_NEG_002(self):

        """
        Test case Id: -  RADIUS_NEG_002
        Description: - With continuous session requests in the background,
		delete the existing Radius session authentication profile.
	"""

        self.myLog.output("\n**********start the test**************\n")

        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_neg_002_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['rad_neg_002_xpressvpn'],"autoexec.cfg","/xpm/")

        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        self.xpress_vpn.cmd("sudo cat /etc/sudoers")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike &")

        time.sleep(9)
        self.myLog.output("List of sessions eastablished before deleting the session authentication profile")
        #Consider 9 client
        op_ssx_sa = self.ssx.configcmd("show ike-session brief")
        i=0
        count1 =0
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count1 = count1+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count1)

        #Delete the session authentication profile
        self.ssx.configcmd("context %s" % script_var['context'])
        self.ssx.configcmd("no radius session authentication profile")

	time.sleep(2)
        self.myLog.output("List of sessions eastablished after deleting the session authentication profile")
        #Checking wheather sessions are establishing even after deleting  the profile
	op_ssx_sa = self.ssx.configcmd("show ike-session brief")
        i=0
        count1 =0
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count1 = count1+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count1)

        self.myLog.output("\nGoing to sleep for 20sec after deleting the session auth profile\n")
	time.sleep(20)
        op_ssx_sa = self.ssx.configcmd("show ike-session brief")
        i=0
        count2 =0
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count2 = count2+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count2)
	self.failUnless(count1 == count2,"Sessions established even afterdeleting the session")


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_NEG_002)
    test_runner().run(suite)
    
