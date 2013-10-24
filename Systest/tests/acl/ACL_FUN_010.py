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

DESCRIPTION:To verify IPV6 acl (icmp traffic) 
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_010

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |         									|
       |              ETH1                                       Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  
        
REVIEWER:

HOW TO RUN : python ACL_FUN_010.py

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



class test_SAN_ACL_010(test_case):
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

    def test_SAN_ACL_010(self):
	        #vgroup b/w ssx and host
        #out = ssx["ip_addr"].split("-mc")[0]
        #os.system("vgroup %s:%s  %s:%s"%(out,ssx1_port,xpress_vpn['ip_addr'],xpress_vpn['interface']))

	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn[1],script_var['xpress_phy_iface1_ipv6_mask'])

	


        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_010'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	time.sleep(5)
	self.ssx.cmd("clear ipv6 counters")

	#ping operation   
	ping_op=self.ssx.ping(dest=script_var['xpress_phy_iface1_ipv6'])
	time.sleep(5)
	#changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        time.sleep(5)
        self.ssx.cmd("clear ipv6 counters")

        #ping operation   
        ping_op=self.ssx.ping(dest=script_var['xpress_phy_iface1_ipv6'])
        time.sleep(5)
        self.failIfEqual(ping_op,0,"Ping through interface failed when acl applied")


	# this api will check whether the icmp stats are getting incremented or not
	icmpCounters=self.ssx.cmd("show ipv6 counters icmp")
        self.myLog.output("icmpCounters exists in SSX:%s" %(icmpCounters))

	output=ip_verify_ipv6_counters_icmp(self.ssx,total_tx='6',echo_request='5',echo_reply='0',unreachable='0',param_problem='0', redirects='0',                  ttl_expired='0',too_big='0',other='0',format='0',rate_limit='0',router_solicit='0',router_advertise='0',neighbor_solicit='0',neighbor_advertise='1')
	self.failUnlessEqual(output,1,"ip_counters_icmp failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	"""print "Starting Main"
	testlogdir = ""
	if os.environ.has_key('TEST_LOG_DIR'):
        	testlogdir = os.environ['TEST_LOG_DIR']

	opts, args = getopt.getopt(sys.argv[1:], "d:")
	for o, a in opts:
        	if o == "-d":
			testlogdir = a

	if testlogdir != "":
        	os.mkdir(testlogdir)
	        os.chdir(testlogdir)"""
	""" Code Commented By : Jayanth"""
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_SAN_ACL_010)
	test_runner(stream = sys.stdout).run(suite)

