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

Description: - Verify SSX limits the number of sessions to the Max-sessions configured 
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-007

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
How to run: "python2.5 AAA_FUN_007.py"
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

class test_AAA_FUN_007(test_case):
    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(topo.ssx1['ip_addr'])
	self.ssx.telnet()

        # CLear SSX configuration
	self.ssx.clear_config()

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.xpress_vpn.telnet()

        # wait for card to come up
        self.ssx.wait4cards()

        self.ssx.clear_health_stats()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

        # Close the telnet session of Xpress VPN Client
        self.xpress_vpn.close()

    def test_AAA_FUN_007(self):
        """
        Test case Id: -  AAA_FUN_007
	"""

        self.myLog.output("\n**********start the test**************\n")

        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['fun_007_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['fun_007_xpressvpn_multi'],"autoexec.cfg","/xpm/")
        self.xpress_vpn.write_to_file(script_var['add_ip_takama'],"add_ip_takama","/xpm/")


        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        self.xpress_vpn.cmd("sudo chmod 777 add_ip_takama")
        self.xpress_vpn.cmd("sudo ./add_ip_takama")
	time.sleep(3)
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
	time.sleep(10)


        #Consider 9 client
        op_ssx_sa = self.ssx.configcmd("show ike-session brief")
        i=0
        count=0
        ssx_max_ses=5
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count=count+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count)
        self.failUnless(count==ssx_max_ses,"Mismatch with the number of sessions and Max sessions configured")


        # Check the "authentication fail" notify message when more than Max sessions are initiated
        op_debug =  verify_in_debug(self.ssx,"AUTHEN_FAIL")
        self.failUnless(op_debug,"the AUTHENTICATION_FAILED notify message is not sent by SSX")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_AAA_FUN_007)
    test_runner(stream=sys.stdout).run(suite)
    
