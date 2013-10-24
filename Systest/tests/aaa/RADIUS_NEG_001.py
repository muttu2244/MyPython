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
TEST CASES: RADIUS-NEG-001

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
How to run: "python2.5 RADIUS_NEG_001.py"
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

class test_RADIUS_NEG_001(test_case):
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
        self.ether_radius2 = Linux(radius2['ip_addr'],radius2['user_name'],radius2['password'])
        self.ether_radius2.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.xpress_vpn.close()
        # Close the telnet session of Radius (tethereal capture machine)
        self.ether_radius1.close()
        self.ether_radius2.close()

    def test_RADIUS_NEG_001(self):
        """
        Test case Id: -  RADIUS_NEG_001
        Description: - Continuously flap the interface on the SSX ,
			that has the primary RADIUS server configured
	"""

        #### Start Ethereal capture the Radius-1
        self.myLog.output(" Step 1 - removing the file rad_neg_001.pcap")
        self.ether_radius1.cmd("sudo rm rad_neg_001.pcap -f")
        self.ether_radius2.cmd("sudo rm rad_neg_001.pcap -f")
        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
	# before starting kill tethereal
        self.ether_radius1.cmd("sudo pkill tethereal")
        self.ether_radius2.cmd("sudo pkill tethereal")
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_neg_001.pcap -R "radius" & '% topo.port_ssx_radius1[1])
        self.ether_radius2.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_neg_001.pcap -R "radius" & '% topo.port_ssx_radius2[1])

        self.myLog.output("\n**********start the test**************\n")

        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_neg_001_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['rad_neg_001_xpressvpn'],"autoexec.cfg","/xpm/")

        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")



        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
	# For entering password 
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
        time.sleep(1)

        self.ssx.configcmd("port ethernet %(port_ssx_radius2)s" %script_var)

	# flap the port which is connected to primary server
        count = 0
        while count<15 :
          self.ssx.configcmd("no enable")
          time.sleep(0.5)
          self.ssx.configcmd("enable")
          # Initiate Ping
          count=count+1

        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        time.sleep(30)
        self.ether_radius1.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created
        ll_output = self.ether_radius1.cmd("ls")
        self.failUnless( "rad_neg_001.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_neg_001.pcap ")
        output1 = self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_neg_001.pcap -R "radius.code == 2" ',timeout = 30)
        self.failUnless("RADIUS" in output1, " Expected - packet with radius.code == 2 ")
        ether_op = output1.split('\n')
        count1 = 0
        for line in ether_op:
            if "RADIUS" in line:
                count1 = count1+1
	##### terminate tethereal & read the pcap file contents captured on secondry server
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        time.sleep(10)
        self.ether_radius1.cmd("sudo pkill tethereal")
        self.ether_radius2.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created
        ll_output = self.ether_radius2.cmd("ls")
        self.failUnless( "rad_neg_001.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_neg_001.pcap ")
        output2 = self.ether_radius2.cmd('sudo /usr/sbin/tethereal -r rad_neg_001.pcap -R "radius.code == 2" ',timeout = 30)
        self.failUnless("RADIUS" in output2, " Expected - packet with radius.code == 2 ")
        ether_op = output2.split('\n')
        count2 = 0
        for line in ether_op:
            if "RADIUS" in line:
                count2 = count2+1

        self.myLog.output("Number of ike sessions Radius-2 Authenticated : %s  rad2 is %s" %(count1,count2))        
	#self.failUnless(count1 + count2 == 9, """ Expected -No packet with radius.code == 2;  Actual = %s"""% count)

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_NEG_001)
    test_runner().run(suite)
    
