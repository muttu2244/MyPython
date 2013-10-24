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

Description: - Verify that session authentication credentials are sent 
          to secondary RADIUS server when the primary server is Not-responding.
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-012

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
How to run: "python2.5 RADIUS_FUN_012.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Raja Rathnam - rathnam@primesoftsolutionsinc.com
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
from Linux import *
from SSX import SSX
from NS import NS 
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *
from misc import *

# import configs file
from aaa_config import *
from topo import *

# python libraries
import time 

class test_RADIUS_FUN_012(test_case):
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

 
        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
        self.ns5gt.telnet()
        self.ns5gt.clear_config()

	# Establish a telnet session to the radius servers 
        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()

        self.ether_radius2 = Linux(radius2['ip_addr'],radius2['user_name'],radius2['password'])
        self.ether_radius2.telnet()


    def tearDown(self):

        # Start The (stopped) radius process
        self.ether_radius1.cmd("sudo /etc/init.d/radiusd start")
        self.ether_radius1.cmd("sudo pkill tethereal")
        self.ether_radius2.cmd("sudo pkill tethereal")
        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of ns5gt client .
        self.ns5gt.close()
	# Close the telnet session of Radius (tethereal capture machine)
	self.ether_radius1.close()
	self.ether_radius2.close()



    def test_RADIUS_FUN_012(self):
        """
        Test case Id: -  RADIUS_FUN_012
	"""

        self.myLog.output("\n**********start the test**************\n")

        #Configure SSX to forward session authentication credentials to radius server for authentication.
	#Configure two radius servers primary & secondary in the session authentication profile.
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_fun_012_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_012_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	# Stop the radius process
        self.ether_radius1.cmd("sudo /etc/init.d/radiusd stop")

        #### Start Ethereal capture on both the Radius servers
        self.myLog.output(" Step 1 - removing the file rad_fun_012.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_012.pcap -f")
        self.ether_radius2.cmd("sudo rm rad_fun_012.pcap -f")
        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal   -h')
        #self.ether_radius2.cmd('sudo /usr/sbin/tethereal   -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_012.pcap -R "radius" & '% topo.port_ssx_radius1[1])
        self.ether_radius2.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_012.pcap -R "radius" & '% topo.port_ssx_radius2[1])

        # Initiate IKEv1 session from a Netscreen to the SSX
        self.ssx.ping('%s'% script_var['ns_phy_ip'])
        self.ssx.ping('%s'% script_var['ns_phy_ip'])
        time.sleep(5)
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")

        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	time.sleep(45)
        #self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output, "session authentication with Radius is not\
                        successed even with valid session credentials")


        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        self.ether_radius1.cmd("sudo pkill tethereal")
        self.ether_radius2.cmd("sudo pkill tethereal")
        time.sleep(5)


        # Check whether the pcap file is created
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_012.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")
        ll_output = self.ether_radius2.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_012.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_fun_012.pcap ")
        output=self.ether_radius2.cmd('sudo /usr/sbin/tethereal -r rad_fun_012.pcap -R "radius.code == 2 " ',timeout = 30)
        self.failUnless("RADIUS" in output, """ Expected - packet with radius.code == 2,  Actual = %s"""% output)
        
        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        self.failUnless(sa_output,"SA not loaded")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_012)
    test_runner(stream=sys.stdout).run(suite)
    
