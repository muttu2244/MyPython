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

DESCRIPTION:To Verify that ACL is applied when the option 'established' on TCP connections is enabled in the rule. Repeat the case with both permit and deny rules
TEST PLAN: Sanity Test plans
TEST CASES: ACL_FUN_041

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |              eth1                                       Port 2/1               |
         --------------------------------------------------------------------------------



AUTHOR:  jayanth@stoke.com
        
REVIEWER:

HOW TO RUN : python ACL_FUN_041.py
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
import string


#import configs file
from config import *
from topo import *



class test_ACL_FUN_041(test_case):
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
    def test_ACL_FUN_041(self):

	#vgroup b/w ssx and host
	#out = ssx["ip_addr"].split("-mc")[0]
        #os.system("vgroup %s:%s  %s:%s"%(out,ssx1_port,linux['ip_addr'],linux['interface']))


	#configuring tunnel on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn[1], script_var['xpress_phy_iface1_ip_mask'])

        self.myLog.output("==================Starting The Test====================")

	# Push SSX config
	self.ssx.config_from_string(script_var['ACL_FUN_041'])

	#changing context and clearing ip counters
	self.ssx.cmd("context %s" %(script_var['context_name']))
	self.ssx.cmd("clear ip access-list name subacl  counters")
	time.sleep(5)
	self.linux.cmd("sudo /usr/local/bin/nemesis tcp -S %s -D %s -d %s -fSA -vv"%( script_var['xpress_phy_iface1_ip'], script_var['ssx_phy_iface1_ip'],p1_ssx_xpressvpn[1]))	
	#time.sleep(10)
	result=self.ssx.cmd("show ip access-list name subacl counters")	
	
	lines=result.split("\n")

	output=lines[2].strip(' ')
	#output=output.strip('0')
	output=output[0]

	self.failUnless(output, "ACL failed to allow TCP Established packet")

	self.ssx.config_from_string(script_var['ACL_FUN_041_MOD'])

	self.ssx.cmd("context %s" %(script_var['context_name']))
        self.ssx.cmd("clear ip access-list name subacl  counters")
        time.sleep(5)
        self.linux.cmd("sudo /usr/local/bin/nemesis tcp -S %s -D %s -d %s -fSA -vv"%( script_var['xpress_phy_iface1_ip'], script_var['ssx_phy_iface1_ip'],p1_ssx_xpressvpn[1]))
        #time.sleep(10)
        result=self.ssx.cmd("show ip access-list name subacl counters")

        lines=result.split("\n")
        #print lines[2]

        output=lines[2].strip(' ')
        if output[0]=='0':
		output=output.strip('0')
		output=output.strip(' ')
        	output=output[0]
	else :
		output='0'

        self.failUnless(output, "ACL failed to disallow TCP Established packet")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ACL_FUN_041)
    test_runner(stream = sys.stdout).run(suite)

