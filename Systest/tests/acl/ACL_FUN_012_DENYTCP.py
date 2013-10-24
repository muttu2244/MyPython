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

DESCRIPTION:To verify igmp  traffic after applying deny rule to acl context.
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_012

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |              eth1                                       Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  
        
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



class test_SAN_ACL_DENYTCP(test_case):
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
    def test_SAN_ACL_DENYTCP(self):

	#vgroup b/w ssx and host
	out = ssx["ip_addr"].split("-mc")[0]
        os.system("vgroup %s:%s  %s:%s"%(out,ssx1_port,linux['ip_addr'],linux['interface']))


	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn[1], script_var['xpress_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['SAN_ACL_011-DENYTCP'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("clear port counters")
	
        #ftp  operation
        ping_op=self.ssx.cmd("copy ftp://ankit:primesoft@%s/lashmi  /hd/lashmi"%(script_var['xpress_phy_iface1_ip']))
#       self.mylog.output("the output of ftp is %s"%(ping_op))
        out=self.ssx.cmd("show ip counters tcp")
        self.myLog.output("the output of ftp is %s"%(out))
        self.failIf("3"  in  out.split()[21]  ,"ftp through interface failed when acl applied")
        # Checking SSX Health
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    testlogdir = ""
	if os.environ.has_key('TEST_LOG_DIR'):
        testlogdir = os.environ['TEST_LOG_DIR']

    opts, args = getopt.getopt(sys.argv[1:], "d:")
    for o, a in opts:
        if o == "-d":
            testlogdir = a

    if testlogdir != "":
        os.mkdir(testlogdir)
        os.chdir(testlogdir)
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_SAN_ACL_DENYTCP)
        test_runner(stream = sys.stdout).run(suite)
