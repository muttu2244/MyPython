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

DESCRIPTION: Detecting & classifying protocol, SSH
TEST PLAN: DPI Test Plan
TEST CASES: DPI_PD_12

TOPOLOGY DIAGRAM:

    (Xpress_VPN)                    (SSX)                         (Linux)
    -------                        --------                     -------------
   |Takama | ---------------------|Lihue-mc|-------------------|Radius Server|
    -------                        --------                     -------------


How to run: "python2.5 DPI_FUN_012.py"
AUTHOR: Venkat - krao@stoke.com
        

REVIEWER:
"""
import sys, os, time

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import SSX
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
import pexpect

# private libraries
from  ike import *
from  dpi import *
from misc import *
#import configs file
pexpect.run('perl  -pi -e \'s/proto_from_script = "\w+"/proto_from_script = "ssh"/\' ikev2_config.py')
from ikev2_config import *
from topo import *

class test_DPI_FUN_012(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        #Establish a telnet session to the Xpress VPN client box.
	self.xpress_vpn = Linux(topo.xpressvpn1["ip_addr"],topo.xpressvpn1["user_name"],
				topo.xpressvpn1["password"])
        self.xpress_vpn.telnet()	

	self.radius = Linux(topo.radius["ip_addr"],topo.radius["user_name"],
				topo.radius["password"])
        self.radius.telnet()	

    def tearDown(self):

	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of Xpress VPN Client
	self.xpress_vpn.close()             

    def test_DPI_FUN_012(self):

	self.myLog.output("\n**********start the test**************\n")

	# Push SSX config
	self.ssx.config_from_string(script_var['common_ssx'])
	self.ssx.config_from_string(script_var['fun_001_ssx'])

	self.ssx.cmd("debug module iked all")
	self.ssx.cmd("debug module aaad all")

	# Push xpress vpn config
	self.xpress_vpn.configure_ip_interface(topo.p1_ssx1_xpressvpn1[1] , ike_ip_mask)
	self.radius.configure_ip_interface(topo.p2_ssx1_radius[1] , rad_ip_mask)

	self.radius.add_route(ike_ip_mask, ipSsx2Rad,intRad2Ssx)
	self.radius.add_route(sesIpMask, ipSsx2Rad,intRad2Ssx)
	self.radius.add_route(clntMask, ipSsx2Rad,intRad2Ssx)

	self.xpress_vpn.cmd("sudo ./add_ip_takama")
	self.xpress_vpn.write_to_file(script_var['fun_001_xpressvpn'],"autoexec.cfg","/xpm/")


	# Initiate IKE Session from Xpress VPN Client (takama)
	self.xpress_vpn.cmd("cd /xpm/")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike &")
	time.sleep(5)


        # Check IKE_AUTH
        op_ssx_debug2 =  verify_in_debug(self.ssx,"AUTHEN", "PASS")
        self.failUnless(op_ssx_debug2, "ike authenticatin is not successful/failed")

	# Check SA in SSX with the remote
	ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpress_phy_iface1_ip'])
        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")
	sesIp = ssx_show_op["ip_config_assigned"]
	self.xpress_vpn.cmd("sudo /sbin/ip route add %s via %s  dev eth2 src %s" % (radius_ip_mask, ipSsx2Ike, sesIp))

	pingOutput = self.xpress_vpn.ping(ipRad2Ssx)
	self.failUnless(pingOutput, "Ping is failed b/w ike client and remote host")

	self.radius.write_to_file("DPI TESTING","dpi.html","")
	sshOutput = self.xpress_vpn.cmd("sudo scp regress@69.0.0.1:dpi.html .")
	time.sleep(10)
	self.failUnless(sshOutput, "ssh is failed b/w ike client and remote host")
	counters = get_ses_counters_qos(self.ssx)
	self.myLog.info("Rcv Pkts:%s  Xmit Pkts:%s" %(counters[0], counters[1]))
	self.failUnless(counters[0] and counters[1], "scp traffic is not bi-directional")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    vgroup_new(vlan_cfg_ike)
    vgroup_new(vlan_cfg_rad)
    suite = test_suite()
    suite.addTest(test_DPI_FUN_012)
    test_runner().run(suite)

