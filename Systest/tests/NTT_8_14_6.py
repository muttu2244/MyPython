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

DESCRIPTION: Syslog Verify DSCP valaue.
TEST PLAN: NTT Translated Cases
TEST CASES: 9_3_6

HOW TO RUN:python2.5 9_3_6.py
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
from config_raja import *
from topo import *



class test_NTT_9_3_6(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1=self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()
	self.linux1.telnet()
        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_NTT_9_3_6(self):


	# Push SSX config
	self.ssx.config_from_string(script_var['SSX_9_3_6'])

	#Configuring Linux Interface
	self.linux.cmd("sudo /sbin/ifconfig %s %s"%(p1_ssx_linux[1],script_var['linux_phy_iface_ip_mask']))

	#setup debugging
	self.ssx.cmd("debug module iplc all")	
	
	#Setup Packet Capture
	self.linux.cmd("sudo /usr/sbin/tethereal -i %s -w 9_3_6.pcap &"%(p1_ssx_linux[1]))
	time.sleep(3)	
	
	self.ssx.cmd("ping %s repeat 1"%script_var['linux_phy_iface_ip'])
	
	self.linux.cmd("sudo pkill tethereal")
	time.sleep(5)
	output = self.linux.cmd("sudo /usr/sbin/tethereal -r 9_3_6.pcap -R 'ip.dsfield == 0x00 && ip.src == %s' -V | grep Syslog"%(script_var['ssx_phy_iface_ip']),timeout=100)	
	self.failUnless("Syslog" in output, "Dscp Value Mismatch")
	
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
	vgroup_new(vlan_cfg_linux)
        suite = test_suite()
        suite.addTest(test_NTT_9_3_6)
        test_runner(stream = sys.stdout).run(suite)

