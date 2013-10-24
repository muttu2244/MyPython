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

DESCRIPTION:To verify working ports in vgroup of SSX.
TEST CASES: vgroup_ports
AUTHOR:rajshekar@primesoftsolutionsinc.com
TOPOLOGY DIAGRAM:

        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24                  TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from misc import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from pexpect import *
from logging import getLogger
from acl import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *



class test_vgroup_ports(test_case):
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

    def test_vgroup_ports(self):

	#configuring tunnel on linux machine
        self.linux.configure_ip_interface(ssx_vgroup[1], script_var['xpress_phy_iface1_ip_mask'])

	# Push SSX config
        self.ssx.config_from_string(script_var['vgroup_ssx'])
	self.ssx.cmd("context cdr-1")

       # Push xpress vpn config
        self.linux.write_to_file(script_var['add_ip_takama'],"add_ip_takama","/xpm/")
        self.linux.cmd("cd /xpm/")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")



	#Vgrouping the Topology 
	vgroup_new(vlan_cfg_str)

	ping_ssx = self.ssx.ping(dest=script_var['vgroup_phy_iface1_ip'])
	time.sleep(5)
	ping_ssx = self.ssx.ping(dest=script_var['vgroup_phy_iface1_ip'])
        self.failUnless(ping_ssx,"*****The ports in vgroup are not working from SSX for XpressVPN********")



        ping_linux = self.linux.cmd("ping %s -w 2 -c 2" %(script_var['upload_server_ip1']))
        self.failUnless(ping_linux,"*****The ports in vgroup are not working from Linux********")



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
	suite.addTest(test_vgroup_ports)
	test_runner(stream=sys.stdout).run(suite)
