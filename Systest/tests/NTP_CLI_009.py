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

DESCRIPTION: Verify all the NTP related debug commands
TEST PLAN:NTP CLI Test plans
TEST CASES: NTP_CLI_009

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            17.1.1.1/24  ---------------->     17.1.1.10/24                     |
       |                                                                                |
       |              e3                                         Port 3/1               |
         --------------------------------------------------------------------------------


HOW TO RUN: python2.5 NTP_CLI_009.py
AUTHOR: nkasera@stoke.com
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
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy,diff_in_time_ssx
import re
from misc import *

#import configs file and topo file
from ntp_config import *
from topo import *



class test_NTP_CLI_009(test_case):
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

    def test_NTP_CLI_009(self):

	 #vgroup b/w NTP client and NTP server
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring interface on linux machine
	
	self.myLog.output("==================Starting The Test====================")
	self.linux.configure_ip_interface(p2_linux_ssx[0],var_dict['infc_linux2_ip/m'])

	# Push NTP configuration on NTP client
        #self.ssx.config_from_string(script_var['common_ssx'])
        self.ssx.config_from_string(script_var['NTP_CLI_009'])
	self.linux.cmd("cd /etc")
        self.linux.cmd("sudo rm -f ntp.conf")
        self.linux.cmd("sudo touch ntp.conf")
        self.linux.cmd("sudo chmod a+rwx ntp.conf")
        self.linux.write_to_file(script_var['ntp.conf'],"ntp.conf","/etc/")
	
	self.ssx.cmd("clear log debug")
	self.ssx.cmd("debug module ntp all")
	op = self.ssx.cmd("show debug")
	self.failUnless("Module ntp group all" in op , "ntp debug module not enabled")
	
	time.sleep(10)
	#Checking Service availability of ntp on linux(NTP server) machine
        self.myLog.output("======Checking Service availability of ntp on linux(NTP server) machine====")
        self.linux.cmd("sudo /sbin/service ntpd stop")
        Cmd_out = self.linux.cmd("sudo /sbin/service ntpd start")
        self.failUnless(Cmd_out != "ntpd: unrecognized service","service not available so install ntp service into NTP server")

	self.myLog.output("Delay of 1 min")	
	time.sleep(60)
	#Checking connectivity b/w NTP server  and NTP client
        self.myLog.output("======Checking connectivity b/w NTP server  and NTP client=====")
        self.ssx.cmd("context %s"%var_dict['cntxt1'])
        Ping_out = self.ssx.ping(var_dict['infc_linux2_ip'])
        time.sleep(5)
        Ping_out = self.ssx.ping(var_dict['infc_linux2_ip'])
        self.failUnless(Ping_out == 1,"ntp server is not reachable")
		
	self.myLog.output("Delay of 10 mins for NTP synchronization")
	time.sleep(600)
	
	op = self.ssx.cmd("show ntp status")
	self.failIf(op.splitlines()[1].split()[2] != var_dict['infc_linux2_ip'] , "Show ntp status command failed : No peer found")
        self.myLog.output("Show ntp status command passed : peer found")

	op = self.ssx.cmd("show ntp associations")
        self.failIf(op.splitlines()[3].split()[0] != "*%s"%var_dict['infc_linux2_ip'] , "Show ntp associations command failed : No remote ip found")
        self.myLog.output("Show ntp associations command passed : Remote ip found")
	
	op = self.ssx.cmd("show log debug")
	self.failUnless("Ntp" in op,"No Ntp logs recorded")
	
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
	suite.addTest(test_NTP_CLI_009)
	test_runner(stream=sys.stdout).run(suite)

