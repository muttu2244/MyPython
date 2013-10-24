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

DESCRIPTION:To verify udp traffic when permit rule is applied to the acl context
TEST PLAN: Sanity Test plans
TEST CASES:ACL_FUN_004

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |     
       |                 ETH1                                    Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  jayanth@stoke.com
        
REVIEWER:

"""

import sys, os, getopt

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from acl import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *
#import private libraries
from ike import *


class test_ACL_FUN_004(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_ACL_FUN_004(self):
	
        #vgroup b/w ssx and host
        #out = ssx["ip_addr"].split("-mc")[0]
        #os.system("vgroup %s:%s  %s:%s"%(out,ssx1_port,xpress_vpn1['ip_addr'],xpress_vpn1['interface']))

	# Enable debug logs for iked
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        #changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip counters")

	# Push SSX config
        self.ssx.config_from_string(script_var['ACL_FUN_004'])

	#configuring interface on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

	# Push xpress vpn config on linux
        self.linux.write_to_file(script_var['ACL_FUN_XPM_common'],"autoexec.cfg","/xpm/")

	#clearing sessions on ssx
	self.ssx.cmd("clear session all")

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd /xpm")
        op_client_cmd = self.linux.cmd("sudo ./start_ike")
	time.sleep(30)
        # Check SA in SSX with the remote (17.1.1.1)
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpress_phy_iface1_ip'])
        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")

	
        self.myLog.output("==================Starting The Test====================")
	

	#checking counters of udp by using api
	self.ssx.cmd("context %s" %(script_var['context_name']))
	udpCounters=self.ssx.cmd("show ip counters udp")
        self.myLog.output("Counters exists in SSX:%s" %(udpCounters))
	output=ip_verify_ip_counters_udp(self.ssx,checksum='0',rx_total='2',tx_total='2',short_pkt='0',short_hdr='0',full='0',no_port_bcast='0' )
        self.failUnlessEqual(output,1,"ip_counters_icmp failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ACL_FUN_004)
    test_runner(stream = sys.stdout).run(suite)

