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

Description: - Verify that the session authentication can be performed using 
		different authentication protocols(PAP, CHAP, EAP) simultaneously .  
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-033

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


How to run: "python2.5 RADIUS_FUN_033.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
        Raja rathnam - rathnam@primesoftsolutionsinc.com
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
from ike import *
from aaa import *
from SSX import SSX
from NS import NS
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

#import configs file
from aaa_config import *
from topo import *

class test_RADIUS_FUN_033(test_case):

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

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.xpress_vpn.telnet()
        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
        self.ns5gt.telnet()
        self.ns5gt.clear_config()


    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()
	self.xpress_vpn.close()

    def test_RADIUS_FUN_033(self):

        """
        Test case Id: -  RADIUS-FUN-033
        """

        #On SSX configure an AAA profile with the session authentication set to Radius
        self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['rad_fun_033_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_033_ns5gt'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['fun_007_xpressvpn'],"autoexec.cfg","/xpm/")

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	# Initiate IKEv1 session from a Netscreen to the SSX 
        # ping ikev1 clent from ssx
        self.ssx.ping('%s'% script_var['ns_phy_ip'])
        time.sleep(5)
        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")

        self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
	self.failUnless(ping_output, "session authentication with Radius is not\
 			successed even with valid session credentials")
	#Verify IKEv1 session authentication 
        #op_debug =  aaa_verify_authentication(self.ssx,"user1@%s" %script_var['context'],"local")
        #self.failUnless(op_debug, "phase-1 session authentication and establishment is not successful")
        #op_debug =  aaa_verify_authentication(self.ssx,"user1@%s" %script_var['context'],"radius")
        #self.failUnless(op_debug, "Verifying in debug:X-auth not successful")
        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        #sa_output= sa_check(self.ssx,script_var['ns_phy_ip'])
        #self.failUnless(sa_output,"SA not loaded")


        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")
        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
        time.sleep(5)
        #Consider 9 client
        op_ssx_sa = self.ssx.cmd("show session detail")
        i=0
        count=0
        ssx_max_ses=2
        for i in range(0,len(clnt_ips)):
          if clnt_ips2[i] in op_ssx_sa:
            count=count+1
        self.myLog.output("\n\n************* the no. of ikev2 sessions:%d\n\n"%count)
        self.failUnless(count==ssx_max_ses,"IKEv2 multiclient SA Formation Failed")

        op_debug =  aaa_verify_authentication(self.ssx,"16502102800650210@%s" %script_var['context'],"radius")
        self.failUnless(op_debug, "Verifying in debug:X-auth not successful")
					
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_033)
    test_runner().run(suite)
    
