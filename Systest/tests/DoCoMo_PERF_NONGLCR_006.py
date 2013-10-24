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

DESCRIPTION: Receiving error frame
HOW TO RUN:python2.5 DoCoMo_PERF_NONGLCR_006.py
AUTHOR:jameer@stoke.com
REVIEWER: krao@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from ixia import *
from SSX import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy, dec_to_any_base
import misc

#import configs file and topo file
from config_docomo import *
from topo import *

# Define your global variables
global ixia_path,cardID, portID
ixia_path = "D:/DoCoMo"
op = topo.p1_ssx2_ixia[1].split('/')
cardID = op[0]
portID = op[1]

class test_DoCoMo_PERF_NONGLCR_006(test_case):
    myLog = getLogger()
    global ixia_path, cardID, portID

    def setUp(self):
	self.myLog.info(__doc__)
	self.ixia = IXIA(ixia["ip_addr"])
        self.ssx = SSX(ssx2["ip_addr"])
        self.ssx.telnet()
	
        # wait for card to come up
        self.ssx.wait4cards()

        # Clear the SSX config
        self.ssx.clear_config()
        self.ssx.clear_health_stats()
	
        # Initiate telnet session to IXIA
	self.ixia.telnet()

    def tearDown(self):
        # Close the telnet session of SSX and IXIA
        self.ixia.cmd("ixLogout")
        self.ixia.cmd("cleanUp")
        self.ixia.close()
        self.ssx.close()

    def test_DoCoMo_PERF_NONGLCR_006(self):
        self.myLog.output("==================Starting The Test====================")  

        # Push SSX config
        #self.ssx.config_from_string(others_var['DoCoMo_PERF_NONGLCR_006'])

        # Move into the context....
        self.ssx.cmd("context %s"%(others_var['context_name']))

        # Pull required TCL and IXIA packages to our test topo
        self.ixia.cmd("package require IxTclHal")
        self.ixia.cmd("package require IxTclExplorer")

        # Login with your username
        login = self.ixia.cmd("ixLogin %s"%ixia_owner)
        self.myLog.output("User %s has logged in Successfully"%ixia_owner)
	CardId2nd = p1_ssx2_ixia[1].split('/')[0]
	PortId2nd = p1_ssx2_ixia[1].split('/')[1]
	CardId3rd = p2_ssx2_ixia[1].split('/')[0]
	PortId3rd = p2_ssx2_ixia[1].split('/')[1]

	# Difning the tuple for error frames
	ixiaTuple = (64, 96)
	for item in ixiaTuple:
		# Verifying the SSX for error frame
		self.myLog.info("Verifying the SSX for %s error frame"%item)

	        # Push the IXIA Config
        	self.ixia.cmd('source "%s/DoCoMo_Perf_NonGlcr_%s_2nd.tcl"'%(ixia_path,item))
	        self.ixia.cmd("ixTransmitPortArpRequest %s %s %s"%(chassisID,CardId2nd,PortId2nd))
		time.sleep(10)
        	self.ixia.cmd('source "%s/DoCoMo_Perf_NonGlcr_%s.tcl"'%(ixia_path,item))
	        self.ixia.cmd("ixTransmitPortArpRequest %s %s %s"%(chassisID,CardId3rd,PortId3rd))

	        self.myLog.output("----Sourcing is done successfully----")

		# Clear all the counters in SSX
		self.myLog.info("Clear all the counters in SSX")
		self.ssx.cmd("clear port counters")
		self.ssx.cmd("clear port counters drop")
		self.ssx.cmd("clear ip counters")

	        # Start Transmit....
		self.myLog.info("Sending %s bytes traffic for 120 seconds"%item)
		self.ixia.cmd("ixStartPortTransmit %s %s %s"%(chassisID,CardId2nd,PortId2nd))
		time.sleep(10)
		self.ixia.cmd("ixStartPortTransmit %s %s %s"%(chassisID,CardId3rd,PortId3rd))
		self.myLog.info("\n\nPORT COUNTERS Info while sending traffic:\n\n")
		tmp = 0
		while (tmp < 10):
			self.myLog.info("show port counters		:%s"%self.ssx.cmd("show port counters"))
			self.myLog.info("show port %s counters		:%s"%(p1_ssx2_ixia[0],self.ssx.cmd("show port %s counters"%p1_ssx2_ixia[0])))
			self.myLog.info("show port %s counters		:%s"%(p2_ssx2_ixia[0],self.ssx.cmd("show port %s counters"%p2_ssx2_ixia[0])))
			self.myLog.info("show port %s counters detail	:%s"%(p1_ssx2_ixia[0],self.ssx.cmd("show port %s counters detail"%p1_ssx2_ixia[0])))
			self.myLog.info("show port %s counters detail	:%s"%(p2_ssx2_ixia[0],self.ssx.cmd("show port %s counters detail"%p2_ssx2_ixia[0])))
			tmp = tmp + 1
			time.sleep(10)
		self.ixia.cmd("cleanUp")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	     	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
		os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	log = buildLogger("DoCoMo_PERF_NONGLCR_006.log", debug=True,console=True)
	suite = test_suite()
	suite.addTest(test_DoCoMo_PERF_NONGLCR_006)	
	test_runner().run(suite)

