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

Description: - Verify that session authentication credentials are 
		always sent to the primary server when algorithm is set to first .
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-010

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
How to run: "python2.5 RADIUS_FUN_010.py"
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
from Linux import *
from SSX import SSX
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *

# import configs file
from aaa_config import *
from topo import *

# python libraries
import time 

class test_RADIUS_FUN_010(test_case):
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

    def test_RADIUS_FUN_010(self):
        """
        Test case Id: -  RADIUS_FUN_010
	"""

        self.myLog.output("\n**********start the test**************\n")

        # Push SSX config
        self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['rad_fun_010_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['rad_fun_010_xpressvpn'],"autoexec.cfg","/xpm/")
        self.xpress_vpn.write_to_file(script_var['add_ip_takama'],"add_ip_takama","/xpm/")

        # Enable debug logs for iked
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module iked all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        #### Start Ethereal capture on both the Radius servers
        self.myLog.output(" Step 1 - removing the file rad_fun_010.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_010.pcap -f")
        self.ether_radius2.cmd("sudo rm rad_fun_010.pcap -f")
        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        #self.ether_radius1.cmd('sudo /usr/sbin/tethereal   -h')
        #self.ether_radius2.cmd('sudo /usr/sbin/tethereal   -h')
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_010.pcap -R "radius" & '% topo.port_ssx_radius1[1])
        self.ether_radius2.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_010.pcap -R "radius" & '% topo.port_ssx_radius2[1])

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        self.xpress_vpn.cmd("sudo ./add_ip_takama")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")

        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        time.sleep(15)
        self.ether_radius1.cmd("sudo pkill tethereal")
        self.ether_radius2.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created in primary radius (qa-svr4)
	time.sleep(5)
        ll_output = self.ether_radius1.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_010.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")

        self.myLog.output  (" Step 4 - read the content of the file rad_fun_010.pcap ")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_010.pcap -R "radius.code == 2 " ',timeout = 30)
        self.failUnless("RADIUS" in output, """ Expected - packet with radius.code == 2,  Actual = %s"""% output)

        ll_output = self.ether_radius2.cmd("ls -lrt *.pcap")
	if "rad_fun_010.pcap" in ll_output :
		output=self.ether_radius2.cmd('sudo /usr/sbin/tethereal -r rad_fun_010.pcap -R "radius.code == 2 " ',timeout = 30)
		self.failUnless(not "RADIUS" in output,"Secondary radius sent the access accept message")
        
	# Check SA in SSX with the remote 
        #Consider 9 client
        op_ssx_sa = self.ssx.configcmd("show ike-session brief")
        i=0
        count=0
        ssx_max_ses=1
        for i in range(0,len(clnt_ips)):
          if clnt_ips[i] in op_ssx_sa:
            count=count+1
        self.myLog.output("\n\n************* the no. of ike sessions:%d\n\n"%count)
        self.failUnless(count==ssx_max_ses,"IKEv2 multiclient SA Formation Failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_010)
    test_runner(stream=sys.stdout).run(suite)
    
