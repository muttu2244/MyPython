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

DESCRIPTION: Behavior during contected to console
TEST MATRIX: 
TEST CASE  : DoCoMo_7_14_1
TOPOLOGY   : GLC-R Setup with host connected behind Initiator.

HOW TO RUN : python2.5 DoCoMo_7_14_1.py
AUTHOR     : jameer@stoke.com
REVIEWER   : krao@stoke.com 
"""

import sys, os, commands
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from CISCO import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy, insert_char_to_string
from misc import *
from glcr import *
from lanlan import *

#Import config and topo files
from config_docomo import *
from topo import *


## Threading the processes
from threading import Thread

class testIt(Thread):
   threadLog = getLogger()
   def __init__ (self,myHandle):
	Thread.__init__(self)
	self.ssxHandle = myHandle
	self.status = -1

   def run(self):
	# Let me run the thread, so I no need to 
	# wait till it loads the configuration.
	self.threadLog.info("Loading the bulk configuration")
	self.ssxHandle.cmd("load configuration /hd/DoCoMo_7_14_1.cfg", timeout=12000)
	self.status = 1


global ssxfdList, getPath, scriptServer
getPath = sys.path[0]
ssxfdList = []
hostName = commands.getoutput("hostname")
scriptServer = commands.getoutput("host %s"% hostName)
scriptServer = scriptServer.split()[-1]

class test_DoCoMo_7_14_1(test_case):
    myLog = getLogger()

    def setUp(self):
	global ssxfdList, getPath, scriptServer
        #Establish a telnet session
        self.myLog.info(__doc__)
	self.myLog.info("Establish a telnet session to Console")
	self.ssx_con = SSX(ssx["ip_addr"])
	ssxfdList.append(self.ssx_con)
	for i in xrange(2):
		self.ssx = SSX(ssx["hostname"])
		ssxfdList.append(self.ssx)
	ssxfdList = tuple(ssxfdList)

	ssxfdList[0].telnet()
	# Clear the running config
	ssxfdList[0].wait4cards()
	ssxfdList[0].clear_config()

	# Load minimum configuration
	ssxfdList[0].load_min_config(ssx["hostname"])
	ssxfdList[0].cmd("end")
	ssxfdList[0].cmd("context local")
	ssxfdList[0].ftppasswd ("copy sftp://regress@%s:%s/DoCoMo_7_14_1.cfg /hd/DoCoMo_7_14_1.cfg noconfirm"%(scriptServer,getPath))


	# Enable the debug logs
	ssxfdList[0].cmd("debug module aaad all")	
	ssxfdList[0].cmd("debug module iked all")	
	ssxfdList[0].cmd("debug module tunmgr all")	

	# Establish a telnet session.
	for fdIndex in xrange(1,3):
		ssxfdList[fdIndex].telnet()


    def tearDown(self):

        # Checking SSX Health
        hs = ssxfdList[0].get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

        # Close the telnet sessions
	for ssxfd in ssxfdList:
                ssxfd.close()

    def test_DoCoMo_7_14_1(self):

        self.myLog.output("\n**********starting the test**************\n")
	self.myLog.info("Calling the thread process for loading the bulk config,\n so that we can access console while loading")
	loadBulk = testIt(ssxfdList[1]) # Loading the bulk config from management.
	loadBulk.start()

	# Verifying the console access while cpu usage is max.
	self.myLog.info("\n\nVerifying the console access while cpu usage is maximum\n\n")
	cnt = 0
	while(cnt < 15):
		self.myLog.output("CPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))
		cpuUtil = ssxfdList[0].cmd('show process cpu non-zero | grep "CPU0 Utilization"')
		fiveSec = re.search("CPU0\s+Utilization\s+for\s+5\s+seconds:\s+(\d+\.\d+)", cpuUtil, re.I)
		oneMin = re.search("\s+1\s+Minute:\s+(\d+\.\d+)", cpuUtil, re.I)
		self.myLog.output("CPU Utilization:\n")
		self.myLog.output("5 Seconds : %s Percentage"%fiveSec.group(1))
		self.myLog.output("1 minute  : %s Percentage"%oneMin.group(1))

		if ((float(oneMin.group(1)) >= float(80.00)) and (float(fiveSec.group(1)) >= float(80.00))):
			self.myLog.output("CPU Usage is more than or equal to 80 Precentage")
			self.myLog.output("CPU Usage is more than 80 Precentage")
	                self.myLog.output("Current CPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))
        	        self.myLog.info("\n\n\n able to operate on console when CPU load is 60 ~ 99 Percentage\n\n\n")
			break

		cnt = cnt + 1
		time.sleep(15)

	if ((float(oneMin.group(1)) >= float(80.00)) or (float(fiveSec.group(1)) >= float(80.00))):
		self.myLog.output("CPU Usage is more than 80 Precentage")
		self.myLog.output("Current CPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))
		self.myLog.info("\n\n\n able to operate on console when CPU load is 60 ~ 99 Percentage\n\n\n")
	else:
		self.myLog.info("Not able to reach the CPU Usage till 80.00 Percentage")
		self.myLog.output("CurrentCPU Utilization: %s"%ssxfdList[0].cmd("show process cpu non-zero"))

	loadBulk.join()



if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DoCoMo_7_14_1)
        test_runner().run(suite)

