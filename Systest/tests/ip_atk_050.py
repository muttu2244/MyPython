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

DESCRIPTION:Send invalid IP fragment 

TEST CASEID:ip_atk_050

TOPOLOGY DIAGRAM:

       --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            2.2.2.3/24  ---------------->     2.2.2.45/24                       |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ip_atk_050.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:Sudama@primesoftsolutionsinc.com

"""



import sys, os, time

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import Linux
from SSX import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *
#import configs file
from topo import *
from ip_atk_config import *

class test_ip_atk_050(test_case):
    myLog = getLogger()	

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        #self.ssx.clear_config()

        #Establish a telnet session to the linux1 client box.
        self.linux1 = Linux(linux1["ip_addr"],linux1["user_name"],
					linux1["password"])
        self.linux1.telnet()
	
	# wait for card to come up 
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of linux1 Client
	self.linux1.close()             

    def test_ip_atk_050(self):

	#vgroup code
	vgroup_new(vgroup_cfg_dos)

	self.myLog.output("\n**********start the test**************\n")

	
	#clearing ip,sys and port counters
	self.ssx.cmd("context test")
        self.ssx.cmd("clear ip counters")
        Cou_out = self.ssx.cmd("show ip counters ")
        self.myLog.output(Cou_out)
        self.ssx.cmd("clear syscount")
        Syscount_out = self.ssx.cmd("show syscount")
        self.myLog.output(Syscount_out)
        self.ssx.cmd("clear port %s counters drop"%script_var['ssx_port'])
        Portcou_out = self.ssx.cmd("show port %s counters drop"%script_var['ssx_port'])
        self.myLog.output(Portcou_out)
	
	#Sending invalid IP fragment 

	#hping -1 -I bge0 -a 30.1.1.1 30.1.1.2 -p 23 -i u1

	out = self.linux1.cmd("sudo ./jolt %s %s 10 &"%(script_var['ssx_ip_addr'],script_var['linux1_ip_addr']),timeout = 150)
        time.sleep(30)
	#killing jolt process
        #self.linux1.cmd("sudo kill -9 jolt") 

	# displaying ip,sys and port counters And process Cpu utilization
	Cou_out = self.ssx.cmd("show ip counters ")
        self.myLog.output(Cou_out)
        Syscount_out = self.ssx.cmd("show syscount")
        self.myLog.output(Syscount_out)
        Portcou_out = self.ssx.cmd("show port %s counters drop"%script_var['ssx_port'])
        self.myLog.output(Portcou_out)
	Cpu_out = self.ssx.cmd("show process cpu slot %s"%((p1_ssx_linux1[0].split("/"))[0]))
	self.failIf("100.00%"in Cpu_out)
	self.myLog.output(Cpu_out)


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,Warn_logs = 100), "Platform is not healthy")



if __name__ == '__main__':

         if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
         filename = os.path.split(__file__)[1].replace('.py','.log')
         log = buildLogger(filename, debug=True, console=True)
         suite = test_suite()
         suite.addTest(test_ip_atk_050)
         test_runner(stream=sys.stdout).run(suite)

