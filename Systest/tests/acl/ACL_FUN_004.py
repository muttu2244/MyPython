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

DESCRIPTION:To verify implicit ACL rules(Deny all)
TEST PLAN: ACL Test plans
TEST CASES:ACL_FUN_004

TOPOLOGY DIAGRAM:


        ---------------------------------------------

       |                             SSX            
       |                   TransIP = 2.2.2.45/24    |
       |     
       |                     Port 2/1               |
         --------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_004.py
AUTHOR: rajshekar@primesoftsolutionsinc.com 
REVIEWER:suresh@primesoftsolutionsinc.com 

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from acl import *
from helpers import is_healthy
from misc import *

#import config and topo file
from config import *
from topo import *



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


	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_004'])


        #changing context and clear port counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear port counters")

        #applying nemesis tool for generating igmp packets
        self.linux.cmd("sudo /usr/local/bin/nemesis icmp -S %s -D %s -d %s "%( script_var['xpress_phy_iface1_ip'], script_var['ssx_phy_iface1_ip'],p1_ssx_xpressvpn[1]))
        time.sleep(20)

        #verifying port counters
        #cmd_op = self.ssx.cmd("show  port %s counters "%(p1_ssx_xpressvpn1[0]))
        #portcounters = self.ssx.cmd("show port counters | grep %s"%(ssx2_port))
        #print portcounters
     
        output=ip_verify_ip_counters_icmp(self.ssx,total_tx='0',total='0',echo_request='0', echo_reply='0', unreachable='0', \
        mask_request='0', mask_reply='0', source_quench= '0' , param_problem='0', timestamp='0',\
        redirects='0', info_reply='0', ttl_expired='0', other='0')
        print output

        self.failIfEqual(output,0,"Implicit Deny All Failed")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_004)
        test_runner(stream = sys.stdout).run(suite)

