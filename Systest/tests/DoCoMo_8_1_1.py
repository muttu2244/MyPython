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
HOW TO RUN:python2.5 DoCoMo_8_1_1.py
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

class test_DoCoMo_8_1_1(test_case):
    myLog = getLogger()
    global ixia_path, cardID, portID

    def setUp(self):
	self.myLog.info(__doc__)
	self.ixia = IXIA(ixia["ip_addr"])
        self.ssx = SSX(ssx1["ip_addr"])
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

    def test_DoCoMo_8_1_1(self):
        self.myLog.output("==================Starting The Test====================")  

        # Push SSX config
        self.ssx.config_from_string(others_var['DoCoMo_8_1_1'])

        # Move into the context....
        self.ssx.cmd("context %s"%(others_var['context_name']))

        # Pull required TCL and IXIA packages to our test topo
        self.ixia.cmd("package require IxTclHal")
        self.ixia.cmd("package require IxTclExplorer")

        # Login with your username
        login = self.ixia.cmd("ixLogin %s"%ixia_owner)
        self.myLog.output("User %s has logged in Successfully"%ixia_owner)

	# Difning the tuple for error frames
	ixiaTuple = ("CRC", "Checksum")
	for item in ixiaTuple:
		# Verifying the SSX for error frame
		self.myLog.info("Verifying the SSX for %s error frame"%item)

	        # Push the IXIA Config
        	self.ixia.cmd('source "%s/DoCoMo_8_1_1_%s.tcl"'%(ixia_path,item))
	        src1 = self.ixia.cmd("ixTransmitPortArpRequest %s %s %s"%(chassisID,cardID,portID))
	        if not int(src1):
	           self.myLog.output("ARP request sent successfully from Rx port\n")

	        self.myLog.output("----Sourcing is done successfully----")

		# Clear all the counters in SSX
		self.myLog.info("Clear all the counters in SSX")
		self.ssx.cmd("clear port counters")
		self.ssx.cmd("clear ip counters")

	        # Start Transmit....
		Tx = self.ixia.cmd("ixStartPortTransmit %s %s %s"%(chassisID,cardID,portID))
		if not int(Tx):
		   self.myLog.output("Sent 10 pkts on IXIA port %s"%portID)
		time.sleep(10)
		if item == "CRC":
			# Verifying the CRCerror count on SSX
			self.myLog.info("Verifying the CRCerror count on SSX")
			crcOp = self.ssx.cmd('show port %s counters detail | grep "CRCErrors"'%p1_ssx2_ixia[0])
			self.failIf(int(crcOp.split()[1]) != 10 , "CRC Errors count is not matching with number errored pkts sent")

		else:
			# Verifying for Bad Checksum packet
			self.myLog.info("Verifying for Bad Checksum packet")
			chksumOp = self.ssx.cmd('show port %s counters drop | grep "V4 Chksum"'%p1_ssx2_ixia[0])
			if not chksumOp:
				self.fail("Could not find V4 Chksum drop")
			
			self.failIf(int(chksumOp.split(':')[1].strip()) != 10 , "V4 Chksum Drop count is not equal to number of pkts sent")

		# Make sure that IXIA is cleaned up after siurcinf
		self.myLog.info("Make sure that IXIA is cleaned up after sourcing")
		self.ixia.cmd("cleanUp")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	     	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
		os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	log = buildLogger("DoCoMo_8_1_1.log", debug=True,console=True)
	suite = test_suite()
	suite.addTest(test_DoCoMo_8_1_1)	
	test_runner().run(suite)

