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

DESCRIPTION: This script is used to cleanup all the cisco interfaces which are used in test topology.
TEST MATRIX: 
TEST CASE  : NA
TOPOLOGY   : GLC-R Setup with host connected behind Initiator.

HOW TO RUN : python2.5 cleanUpCisco.py
AUTHOR     : rajshekar@stoke.com
REVIEWER   : 
"""

import sys, os
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from CISCO import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy, insert_char_to_string
from misc import *
#Import config and topo files
from config import *
from topo import *

class test_cleanUpCisco(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
        self.myLog.info(__doc__)
        self.cisco = CISCO(cisco["ip_addr"])

        #Initiate the telnet session
        self.cisco.console(cisco["ip_addr"])

    def tearDown(self):
	pass

    def test_cleanUpCisco(self):

        self.myLog.output("\n**********Cleaning the cisco Interfaces used in test**************\n")


	self.myLog.info("Cleaning up Phy ports")
        self.cisco.clear_interface_config(intf=p_active_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=p_standby_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=p_active_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=p_standby_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=p_to_rad_active_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=p_to_rad_standby_ssx_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=p_to_rad_active_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=p_to_rad_standby_ssx_cisco_slot3[1])
        self.cisco.clear_interface_config(intf=p_ini_cisco_slot2[1])
        self.cisco.clear_interface_config(intf=p_ini_cisco_slot3[1])
        
        self.cisco.clear_interface_config(intf=p_cisco_rad[0])
        self.cisco.clear_interface_config(intf=p_cisco_rad2[0])
	self.cisco.clear_interface_config(intf=p1_cisco_ixia[0])
	self.cisco.clear_interface_config(intf=p1_cisco_ixia[0])
        
	self.myLog.info("Cleaning up Vlan interfaces")
        self.cisco.cmd("conf t")
        self.cisco.cmd("no interface vlan %s"%haimc_var['vlan4slot2'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['standby_vlan4slot2'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['service_vlan4slot2'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['serback_vlan4slot2'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['vlan4slot3'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['standby_vlan4slot3'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['service_vlan4slot3'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['serback_vlan4slot3'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['ini_vlan4slot2'])
        self.cisco.cmd("no interface vlan %s"%haimc_var['ini_vlan4slot3'])
        self.cisco.cmd("end")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_cleanUpCisco)
        test_runner().run(suite)

