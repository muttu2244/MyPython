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
TEST CASES:ACL_PRE_001

HOW TO RUN:python2.5 ACL_PRE_001.py
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
from misc import *

#import config and topo file
from config import *
from topo import *
import topo


class test_ACL_PRE_001(test_case):
    myLog = getLogger()

    def setUp(self):

	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
	self.linux1=Linux(linux1['ip_addr'],linux1['user_name'],linux1['password'])
        self.linux.telnet()
        self.linux1.telnet()

    def tearDown(self):

	self.linux1.close()

    def test_ACL_PRE_001(self):
	#Bring Down all Linux Interfaces and Bring Up only required ones
	self.linux.cmd("sudo /sbin/ifdown eth1")
	self.linux.cmd("sudo /sbin/ifdown eth2")
	self.linux.cmd("sudo /sbin/ifdown eth3")

	self.linux1.cmd("sudo /sbin/ifdown eth1")
	self.linux1.cmd("sudo /sbin/ifdown eth2")
	self.linux1.cmd("sudo /sbin/ifdown eth3")

	self.linux.cmd("sudo /sbin/ifconfig %s %s"%(topo.p1_ssx_linux1[1],script_var['linux_phy_iface1_ip_mask']))
	self.linux1.cmd("sudo /sbin/ifconfig %s %s"%(topo.p1_ssx_linux2[1],script_var['linux_phy_iface2_ip_mask']))

	self.linux.cmd("sudo /sbin/route add -net %s gw %s"%(script_var['client1_route'],script_var['client1_gateway']))
	self.linux1.cmd("sudo /sbin/route add -net %s gw %s"%(script_var['client2_route'],script_var['client2_gateway']))


	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
	#Vgrouping Required Equipment
	vgroup_new(vlan_cfg_acl)
	vgroup_new(vlan_cfg_acl2)

        suite = test_suite()
        suite.addTest(test_ACL_PRE_001)
        test_runner(stream = sys.stdout).run(suite)

