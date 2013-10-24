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
TEST CASES: RADIUS-NEG-006

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
How to run: "python2.5 RADIUS_NEG_006.py"
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

class test_RADIUS_NEG_006(test_case):
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
        self.ether_linux = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_linux.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.xpress_vpn.close()
        # Close the telnet session of Radius (tethereal capture machine)
        self.ether_linux.close()

    def test_RADIUS_NEG_006(self):

        """
        Test case Id: -  RADIUS_NEG_006
        Description: - With continuous session requests in the background, 
	Reload the GLC card that is being used to process the session-requests.

	"""

        self.myLog.output("\n**********start the test**************\n")
        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_neg_006_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['rad_neg_006_xpressvpn'],"autoexec.cfg","/xpm/")

        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
        time.sleep(10)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")
        self.xpress_vpn.cmd("quit")

        #Saving the cofiguration
        self.ssx.boot_config("/cfint/stoke.cfg")
        self.ssx.save_config(location='/cfint/stoke.cfg')
        # Reload the SSX
	card = topo.port_ssx_linux[0]
	card_reload = card.split('/')
        self.ssx.cmd("reload card %s"%card_reload[0])
        self.ssx.wait4cards(maxtime=150, wait_interval=10)

        #### Start Ethereal capture the Radius-1
        self.myLog.output(" Step 1 - removing the file rad_neg_006.pcap")
        self.ether_linux.cmd("sudo rm rad_neg_006.pcap -f")
        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        #self.ether_linux.cmd('sudo /usr/sbin/tethereal   -h')
        self.ether_linux.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_neg_006.pcap -R "radius" & '% topo.port_ssx_radius1[1])

        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
        time.sleep(10)

        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        self.myLog.output (" \n going for sleep 60sec to catch session requests after card reload '4'")
        self.ether_linux.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created
        ll_output = self.ether_linux.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_neg_006.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_neg_006.pcap ")
        output = self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_neg_006.pcap -R "radius.code == 2" ',timeout = 30)
        self.failUnless("RADIUS" in output, " Expected - packet with radius.code == 2 ")
        #Consider 9 client
        op_ssx_sa = self.ssx.configcmd("show ike-session brief")
	'''
        i=0
        count=0
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count = count+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count)
        self.failUnless(count in (3,4,5),"expected  sessions after card reload")
	'''

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,Card_Reset=1), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_NEG_006)
    test_runner().run(suite)
    
