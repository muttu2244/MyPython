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

Description: - Verify that the SSX sends all the essential & valid 
		attributes in the access-request message to the RADIUS server .
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-001

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

How to run: "python2.5 RADIUS_MISC_001.py"
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
from NS import NS
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from aaa import *
from ike import *
from misc import *

#import configs file
from aaa_config import *
from topo import *

class test_RADIUS_MISC_001(test_case):

    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1['ip_addr'])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],topo.linux["password"])
        self.xpress_vpn.telnet()


        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


        """Establish a telnet session to Radius server 1."""
        self.ether_linux = Linux(radius1['ip_addr'],radius1['user_name'],
                                        radius1['password'])
        self.ether_linux.telnet()


    def tearDown(self):
        """Clear the config and Close down the telnet session."""

        self.ssx.close()
        self.xpress_vpn.close()
	self.ether_linux.close()

    def test_RADIUS_MISC_001(self):

        """
        Test case Id: -  RADIUS-FUN-001
        """

        #Vgrouping the Topology
	''' 
        vgroup_new(vlan_cfg_ns)
        vgroup_new(vlan_cfg_linux)
        vgroup_new(vlan_cfg_radius1)
        vgroup_new(vlan_cfg_radius2)
	''' 


	self.myLog.output("\n**********start the test**************\n")
	# Configure SSX to forward session authentication credentials to 
	# radius server for authentication.
	self.ssx.config_from_string(script_var['common_ssx'])
	self.ssx.config_from_string(script_var['rad_fun_001_v2_ssx'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['EAP_MD5_xpressvpn'],"autoexec.cfg","/xpm/")
        self.xpress_vpn.write_to_file(script_var['add_ip_takama'],"add_ip_takama","/xpm/")

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
	# Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug") 

        self.myLog.output(" Step 1 - removing the file rad_fun_001.pcap")
        self.ether_linux.cmd("sudo rm_fun_001.pcap -f")

        self.myLog.output (" Step 2 -Start tethereal to capture the packets and store the result in file x")
        #self.ether_linux.cmd('sudo /usr/sbin/tethereal -h')
        self.ether_linux.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_001.pcap -R "radius" & '% topo.port_ssx_radius1[1])



        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        self.xpress_vpn.cmd("sudo chmod 777 add_ip_takama")
        self.xpress_vpn.cmd("sudo ./add_ip_takama")
        time.sleep(3)
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
        time.sleep(10)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")

       
        #### terminate tethereal & read the pcap file contents
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        time.sleep(5)
        self.ether_linux.cmd("sudo pkill tethereal")

        # Check whether the pcap file is created or not
        ll_output = self.ether_linux.cmd("ls -lrt *.pcap")
        self.failUnless( "rad_fun_001.pcap" in ll_output,"Testcase FAILED because pcap file has not created ")
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_001.pcap -R "radius.code == 1"',timeout = 30)
        self.failUnless(output, """ Expected - packet with radius.code == 1  Actual = %s"""% output)

        self.myLog.output (" Step 4 - read the content of the file rad_fun_001.pcap")
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_001.pcap -R "radius.User_Name == user1@india-test"',timeout = 30)
        self.failUnless( output, " Expected - packet with radius.User_Name == user1@india-test")
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_001.pcap -R "radius.NAS_IP_Address == %s"'% script_var['ssx_nas_ip_address'],timeout = 30)
        self.failUnless(output, " Expected - packet with radius.NAS_IP_Address == %s"% script_var['ssx_nas_ip_address'])
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_001.pcap -R "radius.NAS_Port_Type == 5" ',timeout = 30)
        self.failUnless(output, " Expected - packet with radius.NAS_Port_Type == 5")
        output=self.ether_linux.cmd('sudo /usr/sbin/tethereal -r rad_fun_001.pcap -R "radius.NAS_Identifier == %s"'% script_var['ssx_nas_identifier'],timeout = 30)
        self.failUnless(output, " Expected - packet with radius.NAS_Identifier == %s"% script_var['ssx_nas_identifier'])

        #Check out the SA status in SSX.
        self.ssx.cmd("context %s" %script_var['context'])
        sa_output= sa_check(self.ssx,script_var['xpress_phy_iface1_ip'])
        self.failUnless(sa_output,"SA not loaded")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_RADIUS_MISC_001)
    test_runner(stream=sys.stdout).run(suite)

