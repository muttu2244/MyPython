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

Description: - Verify the ikev2 session for incorrect psk
TEST PLAN: DoCoMo regression
TEST CASES: DoCoMo_6_1_2.py

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
How to run: "python2.5 DoCoMo_6_1_2.py"
AUTHOR: Jameer Basha, jameer@stoke.com
REVIEWER: Venkat, krao@stoke.com
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
from misc import *

# import configs file
from config_docomo import *
from topo import *

# python libraries
import time 

class test_DoCoMo_6_1_2(test_case):
    myLog = getLogger()
    global pskFlag
    pskFlag = 0

    def setUp(self):
	self.myLog.info(__doc__)
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(topo.ssx['ip_addr'])
	self.ssx.telnet()

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux1["ip_addr"])
        self.xpress_vpn.telnet()

	# Telnet session to radisu server
	self.rad = Linux(topo.radius1["ip_addr"])
	self.rad.telnet()

        # wait for card to come up
        self.ssx.wait4cards()

        # CLear SSX configuration
	self.ssx.clear_config()
	self.ssx.clear_health_stats()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()

        # Close the telnet session of Xpress VPN Client
	if pskFlag:
		self.xpress_vpn.cmd("ike reset")
	        time.sleep(10)
 	        self.xpress_vpn.cmd("quit")
        self.xpress_vpn.close()
	self.rad.close()

    def test_DoCoMo_6_1_2(self):
        """
        Test case Id: -  DoCoMo_6_1_2
	"""

        self.myLog.output("\n**********start the test**************\n")
	'''
	self.myLog.info("Running vgroup")
	ssx_name= ssx["ip_addr"].split("-mc")[0]
        vportssx1 = port_ssx_linux1[0].replace('/',':')
        vportssx2 = port_ssx_radius1[0].replace('/',':')
	vportl1   = port_ssx_linux1[1].replace('eth','e')
	vportl2   = port_ssx_radius1[1].replace('eth','e')

	vgroup_new("%s:%s %s:%s"%(ssx_name,vportssx1,linux1['ip_addr'],vportl1))
	vgroup_new("%s:%s %s:%s"%(ssx_name,vportssx2,radius1['ip_addr'],vportl2))
	'''
        # Push SSX config
        self.ssx.config_from_string(docomo_var['DoCoMo_6_1_2'])
	
	#configuring tunnel on linux machine
        self.xpress_vpn.configure_ip_interface(port_ssx_linux1[1], docomo_var['xpress_phy_iface1_ip_mask'])
        self.rad.configure_ip_interface(port_ssx_radius1[1], docomo_var['radius1_ip_mask'])
	
	# start the radius, if not started
	self.myLog.output("Start the radius, if not started")
	radOp = self.rad.cmd("sudo /sbin/service radiusd status")
	if ("stop" or "dead" or "not running" in radOp):
		self.rad.cmd("sudo /sbin/service radiusd start")

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(docomo_var['xpm_autoexec'],"autoexec.cfg","/xpm/")


        # Enable debug logs for iked
        self.ssx.cmd("context %s" % docomo_var['context_name'])
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        # Initiate IKE Session from Xpress VPN Client (takama)
	self.xpress_vpn.cmd("sudo /sbin/ip addr add dev %s %s/16 brd +"%(port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(docomo_var['ses_lo_ip'],docomo_var['ssx_clnt_ip'],port_ssx_linux1[1],docomo_var['ip_pool']))
	self.xpress_vpn.cmd("sudo /sbin/ifconfig %s:1 %s netmask 255.255.0.0"%(port_ssx_linux1[1],docomo_var['xpress_phy_iface1_ip']))
	time.sleep(3)
	self.xpress_vpn.cmd("cd /xpm")
        op_client_cmd = self.xpress_vpn.cmd("sudo start_ike")
	time.sleep(10)

        ses_yn = self.ssx.cmd("show ike-session brief")
        self.myLog.output("show ike-session brief : %s"%ses_yn)
        if ses_yn.splitlines()[-1].split()[2] != 'Y':
                self.fail("FAIL : ipv4 session is not establised with correct psk")

	op1 = self.ssx.cmd("show session") + self.ssx.cmd("show ike-session brief") + self.ssx.cmd("show ike-session list") + self.ssx.cmd("show ike-session detail remote %s"%docomo_var['xpress_phy_iface1_ip'])
        self.myLog.output("Session Details: %s"%op1)
        time.sleep(4)

	self.xpress_vpn.cmd("ike reset")
        time.sleep(10)
        self.xpress_vpn.cmd("quit")

	self.myLog.info("\n\nConfiguring the incorrect psk at xpress vpn\n\n")
	self.xpress_vpn.write_to_file(docomo_var['incorrect_psk'],"autoexec.cfg","/xpm/")
        time.sleep(3)
        op_client_cmd = self.xpress_vpn.cmd("sudo start_ike")
        time.sleep(10)
	pskFlag = 1
	
	ses_yn = self.ssx.cmd("show ike-session brief")
	self.failIf("ERROR" not in ses_yn , "Session established for incorrect psk")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_DoCoMo_6_1_2)
    test_runner().run(suite)
    
