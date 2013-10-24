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

Description: - Verify that SSX forwards the User accounting information
	 to radius when user accounting radius is configured in AAA profile.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-FUN-013

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

How to run: "python2.5 AAA_FUN_013.py"
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
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *

#import configs file
from aaa_config import *
from topo import *


class test_AAA_FUN_013(test_case):

    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        #Establish a telnet session to the linux client box.
        self.linux = Linux(topo.linux["ip_addr"],topo.linux["user_name"],
				topo.linux["password"])
        self.linux.telnet()

        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],
					radius1['password'])
        self.ether_radius1.telnet()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

   
    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of linux Client
	self.linux.close()             
        self.ether_radius1.close()

    def test_AAA_FUN_013(self):
        """
        Test case Id: -  AAA-FUN-013
        """

	self.myLog.output("\n**********start the test**************\n")

        #Push the SSX configuration
	self.ssx.config_from_string(script_var['user_add_ssx'])
	self.ssx.config_from_string(script_var['common_ssx1'])
	self.ssx.config_from_string(script_var['fun_013_ssx'])
	
        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
	# Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        self.myLog.output(" Step 1 - removing the file aaa_fun_013.pcap")
        self.ether_radius1.cmd("pwd")
        self.ether_radius1.cmd("sudo rm aaa_fun_013.pcap ")

        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in file ")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w aaa_fun_013.pcap -R "radius" & '% topo.port_ssx_radius1[1])

        # Initiate Telnet Session from client to SSX  with valid user credentials
        # which are configured in radius server
        op_telnet = generic_verify_telnet_2_ssx(self.linux,script_var['ssx_phy_ip2'],
                username="user3@%s"%script_var['context'],password="123user3")
        self.failUnless(op_telnet,"telnet failed from client to SSX")

        self.myLog.output(" Step 3 - stop tethereal by killing the tethereal application.")
	time.sleep(5)
        self.ether_radius1.cmd("sudo pkill tethereal")

	# Check whether the pcap file is created or not 
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless( "aaa_fun_013.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")
	
        self.myLog.output (" Step 4 - read the content of the file aaa_fun_013.pcap and if it has Frame then pass else fail")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r aaa_fun_013.pcap -R "radius.Acct_Status_Type == 1"',timeout = 30)
        self.failUnless(output, " Expected - packet with radius.Acct.Status_Type == 1 ")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r aaa_fun_013.pcap -R "radius.Acct_Status_Type == 2"',timeout = 30)
        self.failUnless(output, " Expected - packet with radius.Acct.Status_Type == 2 ")

        # Verify that SSX should initially relay the authentication information to the RADIUS.
        op_debug =  aaa_verify_authentication(self.ssx,"user3@%s"% script_var['context'],"radius")
        self.failUnless(op_debug,"Telnet Authentication not succes")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_AAA_FUN_013)
    test_runner(stream=sys.stdout).run(suite)

