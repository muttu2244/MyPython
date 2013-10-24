
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

DESCRIPTION:To verify igmp traffic after applying permit rule to acl context
TEST PLAN: ACL Sanity Test plans
TEST CASE ID: ACL_FUN_023

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24  ------------>   TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              eth1                                       Port 3/3               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_023.py
AUTHOR:rajshekar@primesoftsolutionsinc.com  
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



class test_ACL_FUN_023(test_case):
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

    def test_ACL_FUN_023(self):

          #vgroup b/w SSX and LINUX.
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configure interface on linux machine
	self.linux.configure_ip_interface(p1_ssx_linux1[1],script_var['linux_phy_iface1_ip_mask'])
	
        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_023'])

	#changing context and clear port counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("clear port %s counters "%(p1_ssx_linux1[0]))

	 #nemesis tool for generating igmp packets on linux.
        self.linux.cmd("sudo nemesis igmp -D %s -S %s -d %s"%(script_var['ssx_phy_iface1_ip'],script_var['linux_phy_iface1_ip'],p1_ssx_linux1[1]))

        #Verifying port counters.
	time.sleep(10)	
        cmd_op=self.ssx.cmd("show  port %s counters "%(p1_ssx_linux1[0]))
        self.myLog.output("displaying port counters after sending igmp traffic : %s"%cmd_op)
        output = verify_port_counters(self.ssx,cmd_op,1)

        self.failUnless(output == 1,"igmp through interface passed when acl applied")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_ACL_FUN_023)
        test_runner(stream = sys.stdout).run(suite)

