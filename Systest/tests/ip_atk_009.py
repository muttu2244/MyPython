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

DESCRIPTION:Send multiple telnet sessions to SSX at high rate.
 TEST PLAN:IP-ATTACK test plans
TEST CASEID:ip_atk_009

TOPOLOGY DIAGRAM:

       --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            2.2.2.3/24  ---------------->     2.2.2.45/24                       |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ip_atk_009.py
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
from SSX import SSX
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *
#import configs file
from topo import *
from ip_atk_config import *

class test_ip_atk_009(test_case):
    myLog = getLogger()	

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        #self.ssx.clear_config()

        #Establish a telnet session to the linux1 client box.
        self.linux1 = Linux(linux1["ip_addr"],linux1["user_name"],linux1["password"])
        self.linux1.telnet()
	
	# wait for card to come up 
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of linux1 Client
	self.linux1.close()             

    def test_ip_atk_009(self):


	#vgroup code
        vgroup_new(vgroup_cfg_dos)

	self.myLog.output("\n**********start the test**************\n")
	self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
	self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
	self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
	self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
	self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")
        self.linux1.cmd("konsole -T multiTelnet -e telnet 10.10.0.3")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ip_atk_009)
    test_runner().run(suite)

