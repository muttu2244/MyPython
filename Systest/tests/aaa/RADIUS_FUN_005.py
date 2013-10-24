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

Description: - Verify that the SSX sets the NAS-IP-Address to the configured attribute value.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS_FUN_005

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


How to run: "python2.5 RADIUS_FUN_005.py"
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

### import the Stoke libraries we need.
from SSX import SSX
from NS import NS
from Linux import *
from log import buildLogger
from StokeTest import test_case, test_suite, test_runner
from helpers import is_healthy
from aaa import *
from ike import *

### import topo and config files.
from aaa_config import *
from topo import *

class test_RADIUS_FUN_005(test_case):

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
        self.ssx.clear_health_stats()

        # Estabish a telnet sessin to Radius server 1
        self.ether_linux = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_linux.telnet()

        # Clear SSX configuration
	self.ns5gt.clear_config()	

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()
	self.ether_linux.close()

    def test_RADIUS_FUN_005(self):

        """
        Test case Id: -  RADIUS_FUN_005
        """

        self.myLog.output("\n**********start the test**************\n")

        #Push the SSX configuration
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_fun_005_ssx'])

        #Push the Netscreen configuration
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_005_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	#### Ethereal cap
        self.myLog.output("Step 1 - removing the file rad_fun_005.pcap")
        self.ether_linux.cmd("sudo rm rad_fun_005.pcap -f")
        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in file ")
        #self.ether_linux.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_linux.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_005.pcap -R "radius" &'% topo.port_ssx_radius1[1])

        # Initiate IKEv1 session from a netscreen to the SSX with valid session credentials.
        ping_ot =self.ssx.ping('%s'% script_var['ns_phy_ip'])
	self.myLog.output(ping_ot)
        time.sleep(5)
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")

        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	time.sleep(10)
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output,"session authentication ")


        self.myLog.output(" Step 3 - stop tethereal by killing the tethereal application.")
	time.sleep(10)
        self.ether_linux.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        ll_output = self.ether_linux.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_005.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output(" Step 4 - read the content of the file rad_fun_005.pcap and if it has Frame then pass else fail")
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_005.pcap  -R "radius.NAS_IP_Address == %s"'%script_var['ssx_nas_ip_address'],timeout = 100)
        self.failUnless("RADIUS" in output, " Expected - packet with radius.NAS_IP_Address ")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_005)
    test_runner(stream=sys.stdout).run(suite)
    
