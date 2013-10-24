#!/usr/bin/env python2.5

#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################
"""
       Description	       :  verify system MTU. Confirm system allow to define system MTU 
       Author                  :  rajshekar, rajshekar@stoke.com
"""


### Import the system libraries we need.
import sys, os, time, re, random

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### import the Stoke libraries we need.
from SSX import SSX
from log import buildLogger
from StokeTest import test_case, test_suite, test_runner
from helpers import is_healthy
from logging import getLogger
from topo import *
from config_raja import *
from jf import *

class test_NTT_3_4_1(test_case):
    myLog=getLogger()


    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx['ip_addr'], "joe@local", "joe")
	self.ssx.telnet()
        self.ssx.wait4cards()


    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()


    def test_NTT_3_4_1(self):
        sysMaxMTU = 9500
	(mtuCrnt,mtusNxt) = get_sys_mtu(self.ssx)
	#self.myLog.info("MTU - Current Boot : %s Next Boot : %s" %(mtuCrnt,mtusNxt))
	self.myLog.info("Configuring max system MTU 9180 now ..")
	self.ssx.cmd("system mtu %s" %sysMaxMTU)
	
	
	(mtuCrnt,mtusNxt) = get_sys_mtu(self.ssx)
	self.failUnless("mtuCrnt == mtusNxt", "Syste, MTU changed before reload")


	self.myLog.info("Reloading SSX now ..")
	self.ssx.reload_device()

	self.myLog.info("Reload is done")
	(mtuCrntRld,mtusNxtRld) = get_sys_mtu(self.ssx)

	self.failUnless("mtuCrntRld != mtusNxt", "MTU doesn't take affect after reload")
	

	#self.myLog.info("MTU - Current Boot : %s Next Boot : %s" %(mtuCrnt,mtusNxt))

        # Verify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs, Err_logs=5), "Platform is not healthy")


 
          
	 
         
	 #self.ssx.cmd("load configuration sst-04dec.cfg")
if __name__ == '__main__':
    if os.environ.has_key('TEST_LOG_DIR'):
        os.mkdir(os.environ['TEST_LOG_DIR'])
        os.chdir(os.environ['TEST_LOG_DIR'])

    log = buildLogger('test_NTT_3_4_1.log', debug=1, console=1)
    suite = test_suite()
    suite.addTest(test_NTT_3_4_1)
    test_runner().run(suite)
    
