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

DESCRIPTION: Verify that the Absolute-Timeout attribute can be modified after the session has been established, using CoA request
TEST PLAN: Radius Dynamic Authorization Test Plan
TEST CASES: RDA-HA-005

TOPOLOGY DIAGRAM:

    (Linux)                      (SSX)                        (Linux)
    -------                      --------                   --------------
   |Takama | -------------------|        |-----------------| qa-svr4      |
    -------                     |        |                  --------------
                                |Lihue-mc|
  (Netscreen)                   |        |                     (Linux)
    ------                      |        |                  --------------
   |qa-ns1 | -------------------|        |-----------------| qa-svr3      |
    ------                      |        |                  --------------
                                 --------

How to run: "python2.5 CDR_HA_FUN_001.py"
AUTHOR:	Raja Rathnam -rathnam@primesoftsolutionsinc.com
REVIEWER: Venkat - kvv.rao@primesoftsolutionsinc.com
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
from cdr import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

#import configs file
from config import *
from topo import *

#import private libraries
from ike import *
from misc import *
import time 

class test_CDR_HA_FUN_001(test_case):
    myLog = getLogger()

    def setUp(self):

        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx_HA['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

        # CLear SSX configuration
	self.ssx.clear_config()
        self.ssx.wait4cards()

        #Establish a telnet session to the Xpress VPN client box.
        self.linux = Linux(linux["ip_addr"],linux["user_name"],
				linux["password"])
        self.linux.telnet()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client and radius server
        self.linux.close()

    def test_CDR_HA_FUN_001(self):
        """
        Test case Id: -  CDR_HA_FUN_001
	"""

        self.myLog.output("\n**********start the test**************\n")

        #Clearing already existing files on the linux machine
        self.linux.cmd("su root")
        time.sleep(5)
        self.linux.cmd("su krao")
        time.sleep(5)
        self.linux.cmd("cd")
        time.sleep(5)
        self.linux.cmd("rm -rf *.asn1")
        self.linux.cmd("rm -rf *.xml")
        self.linux.cmd("rm -rf *.ttlv")
        self.linux.cmd("exit")
        self.linux.cmd("exit")

        self.linux.cmd("cd /tftpboot/")
        #self.linux.cmd("sudo rm *.*")
        self.linux.cmd("sudo rm -rf *.asn1")
        self.linux.cmd("sudo rm -rf *.xml")
        self.linux.cmd("sudo rm -rf *.ttlv")



        #configuring interface on linux machine
        self.linux.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

        # Push xpress vpn config on linux
        self.linux.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        self.linux.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")

        # Push SSX config
        self.ssx.config_from_string(script_var['CDR_FUN_002'])


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd")
        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")
        time.sleep(5)

        op_client_cmd = self.linux.cmd("sudo ./start_ike")
        time.sleep(55)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")


        self.linux.cmd("!ping %s -I %s -w 4 -c 4" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux.cmd("quit")

        #Changing the running configuration
        self.ssx.config_from_string(script_var['CDR_FUN_002A'])


        #Displaying the saved configuration
        saved_conf =  self.ssx.cmd("show configuration cdr")
        self.myLog.output(saved_conf)


        #Executing IMC-Switc-Over
	self.ssx.imc_switchover_mgmt("system imc-switchover")

        time.sleep(60)

        self.linux.cmd("ls -rth /tftpboot/ | grep \".xml\" ")
        self.linux.cmd("ls -rth ~krao | grep \".xml\" ")

        linuxip = self.linux.cmd("ls -rth /tftpboot/ | grep \".xml\" | tail -n 1")
        linuxip1 = linuxip.strip()
        self.myLog.output(linuxip1)

        self.failUnless(linuxip1,"Failed to generate XML files after changing the configuration")
        self.myLog.output("CDR data generation passed for a given session even after changing and saving of running configuration")
        self.myLog.info("*" *50)
        self.myLog.output("XML files were generated instead of TTLV files")
        self.myLog.info("*" *50)



        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,IMC_Switch=1,Card_Reset=1), "Platform is not healthy")



if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_CDR_HA_FUN_001)
    test_runner().run(suite)
    
