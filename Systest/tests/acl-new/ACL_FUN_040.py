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

DESCRIPTION:To verify SSX maintains functionality of acl when IMC switch-over happens.
TEST PLAN: ACL Test plans
TEST CASE ID: ACL_FUN_040

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24 ---------->      TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ACL_FUN_040.py
AUTHOR: jayanth@stoke.com 
REVIEWER:
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
import re
from misc import *

#import config and topo file
from config import *
from topo import *



class test_ACL_FUN_040(test_case):
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

    def test_ACL_FUN_040(self):

	#vgroup b/w SSX and LINUX.
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring tunnel on linux machine
	#self.linux.configure_ip_interface(p1_ssx_linux[1], script_var['linux_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_040'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))

	#ping operation   
	time.sleep(5)
	ping_op=self.linux.ping(script_var['linux_phy_iface1_ip'])
	self.failUnless(ping_op == 1,"Ping through interface failed when acl applied")
	
	#SSX prompt change to standbymode
	self.ssx.cmd("context local")
	#self.ssx.cmd("system imc-switchover",timeout=180)
	self.ssx.imc_switchover_mgmt("system imc-switchover")
	time.sleep(5)
	#SSX prompt change to active mode.
	#self.ssx.cmd("system imc-switchover")

	self.ssx.cmd("context %s" %(script_var['context_name']))

	#ping operation
	ping_op=self.linux.ping(script_var['linux_phy_iface1_ip'])
        self.failUnless(ping_op == 1,"Ping through interface failed when acl applied")
	

        # Checking SSX Health
	hs = self.ssx.get_health_stats()
  	self.failUnless(is_healthy( hs,IMC_Switch=2,Card_Reset=2), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_ACL_FUN_040)
	test_runner(stream=sys.stdout).run(suite)

