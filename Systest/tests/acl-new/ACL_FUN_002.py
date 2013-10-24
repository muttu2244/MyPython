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

DESCRIPTION:To verify icmp traffic after applying the permite rule to acl context.
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_002

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |         									|
       |              ETH1                                       Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR : jayanth@stoke.com
REVIEWER:

HOW TO RUN : python ACL_FUN_002.py 

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



class test_ACL_FUN_002(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(xpress_vpn['ip_addr'],xpress_vpn['user_name'],xpress_vpn['password'])

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
    def test_ACL_FUN_002(self):
	        #vgroup b/w ssx and host
        #out = ssx["ip_addr"].split("-mc")[0]
        #os.system("vgroup %s:%s  %s:%s"%(out,ssx1_port,xpress_vpn['ip_addr'],xpress_vpn['interface']))


	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn[1], script_var['xpress_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_002'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("clear ip counters")
	time.sleep(5)
	#ping operation   
        ping_op=self.linux.cmd("ping -c 5 %s"%(script_var['ssx_phy_iface1_ip']),timeout=30)
        self.failIfEqual(ping_op,0,"Ping through interface failed when acl applied")

	# this api will check whether the icmp stats are getting incremented or not
	icmpCounters=self.ssx.cmd("show ip counters icmp")
        self.myLog.output("icmpCounters exists in SSX:%s" %(icmpCounters))

        output=ip_verify_ip_counters_icmp(self.ssx,total_tx='5',total='5',echo_request='5', echo_reply='5', unreachable='0', \
        mask_request='0', mask_reply='0', source_quench= '0' , param_problem='0', timestamp='0',\
        redirects='0', info_reply='0', ttl_expired='0', other='0')
        self.failUnlessEqual(output,0,"ip_counters_icmp failed")

       # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ACL_FUN_002)
    test_runner(stream = sys.stdout).run(suite)

