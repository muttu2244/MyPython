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

DESCRIPTION:To  Verify that there is no long term memory in SSX by adding and deleting maximum servers multiple times.

 
TEST PLAN: Sanity Test plans
TEST CASES: DHCP-NEG-002

TOPOLOGY DIAGRAM:

	--------------------------------------------------
       |	                                         |
       |			    SSX	                 |
       |		Context - A	    	 	 |
       |         Trans  IP = 2.1.1.1/24			 |		
       |              port 4/0                           |
         -------------------------------------------------

HOW TO RUN:python2.5 DHCP-NEG-002.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:himanshu@primesoftsolutionsinc.com

"""
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import SSX
from Linux import *
from dhcp import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy


#import configs file
from dhcp_config import *
from  topo import *

class test_DHCP_NEG_002(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1 = Linux(linux1["ip_addr"])
	self.linux2 = Linux(linux2["ip_addr"])
	self.linux1.telnet()
	self.linux2.telnet()
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.linux1.close()
	self.linux2.close()

    def test_DHCP_NEG_002(self):

        self.myLog.output("\n**********start the test**************\n")

	# Push SSX config
        self.ssx.config_from_string(script_var['DHCP_NEG_002'])

	#Record which shows DHCP servers in SSX before deleating context in which DHCP servers configured
	self.ssx.configcmd("end")
	self.ssx.configcmd("context dhcp")
	self.myLog.output("\n\n")
	Servers_out = self.ssx.cmd("show dhcp server all")
	self.myLog.output("\n\nRecord which shows DHCP servers in SSX before deleating context in which DHCP servers configured %s"%Servers_out)
	
	#Record which shows DHCP servers in SSX after deleating context in which DHCP servers configured
	self.ssx.configcmd("no context %s"%script_var['context_name'])
	Servers_out = self.ssx.cmd("show dhcp server all")
	self.myLog.output("\n\n")
	self.myLog.output("\n\nRecord which shows DHCP servers in SSX after deleating context in which DHCP servers configured \n%s\n"%Servers_out)
 	self.failIf("Reserved" in Servers_out)																										

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


	      	   
if __name__ == '__main__':

	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DHCP_NEG_002)
        test_runner(stream=sys.stdout).run(suite)

