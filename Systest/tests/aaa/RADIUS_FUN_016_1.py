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

Description: - Verify that the SSX drops all the session requests 
	when the configured RADIUS server reaches Maximum outstanding threshold.
	(repeating testcase for accounting profile)
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-016_1

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
How to run: "python2.5 RADIUS_FUN_016_1.py"
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

class test_RADIUS_FUN_016_1(test_case):
    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(topo.ssx1['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

        # CLear SSX configuration
	self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.xpress_vpn.telnet()

        # Establish a telnet session to the radius servers
        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()

    def tearDown(self):

        # Start The (stopped) radius process
        self.ether_radius1.cmd("sudo /etc/init.d/radiusd start")
        self.ether_radius1.cmd("sudo pkill tethereal")

	# close the telnet session of the  radius server
        self.ether_radius1.telnet()

        # Close the telnet session of SSX
        self.ssx.close()

        # Close the telnet session of Xpress VPN Client
        self.xpress_vpn.close()


    def test_RADIUS_FUN_016_1(self):
        """
        Test case Id: -  RADIUS_FUN_016_1
	"""

        self.myLog.output("\n**********start the test**************\n")

        #### Start Ethereal capture on both the Radius servers
        self.myLog.output(" Step 1 - removing the file rad_fun_016_1.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_016_1.pcap -f")
        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_016_1.pcap -R "radius" & '% topo.port_ssx_radius1[1])

        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['rad_fun_016_1_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['rad_fun_016_1_xpressvpn'],"autoexec.cfg","/xpm/")

        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Stop the radius process
        self.ether_radius1.cmd("sudo /etc/init.d/radiusd stop")


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")


        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        time.sleep(15)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_016_1.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_fun_016_1.pcap ")
        ether_op = self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_016_1.pcap -R "radius.code == 4  && ! icmp"',timeout = 30)
        self.failUnless("RADIUS" in ether_op, 'Expected - radius_accout_request for 2 sessions,but not recived')


        
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_016_1)
    test_runner().run(suite)
    
