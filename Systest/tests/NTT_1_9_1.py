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

DESCRIPTION:Confirm SSX definition and loaded definition confirmed by "show config" are identical. [Bootup using configuration file in  HDD]

HOW TO RUN:python2.5 NTT_1_9_1.py
AUTHOR:rajshekar@stoke.com.
REVIEWER:

"""
import sys, os
import commands
mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
#from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from topo import *

# Place for variables
fileName = "config_original.cfg" # Original file, should be in current directory.
tunFileName = "tuunnel_config_original.cfg"            # Only tunnel configuration form original file.
noOfTunnels = 99	     		  # Number of tunnels in the box
thresholdVal = 5			  # This value indicates, number of to and forth to be 
					  # verified for the disappered line at boundary
initVal = 12				  # Initial boundary value, here 2^initVal[ex: 2^12 = 4k,
					  # so for 4K initail boundary it should be 12.

class test_NTT_1_9_1(test_case):
    myLog = getLogger()

    def setUp(self):
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()
        # Load minimum configuration
        self.ssx.load_min_config(ssx["hostname"])

    def tearDown(self):
        # Close the telnet session of SSX...
        self.ssx.close()

    def test_NTT_1_9_1(self):

        #Get the script location
        getPath = sys.path[0]

        #Get the ip adress of server where you are running the script.
        hostName = commands.getoutput("hostname")
        if "silicon" in hostName:
             scriptServer = "10.10.10.182"
        else:
             scriptServer = commands.getoutput("host %s"% hostName)
             scriptServer = scriptServer.split()[-1]

        fileOp = commands.getoutput("cat %s"% fileName)
        self.ssx.hidden_cmds_enable()
        # Copy the generated files to SSX
        self.ssx.cmd("term wid infi")
        self.ssx.cmd("term len infi")
        self.ssx.cmd("save conf mgmt.cfg")
        self.ssx.cmd("boot config file mgmt.cfg")
        self.ssx.cmd("del /hd/%s nocon"%fileName)
        self.ssx.ftppasswd("copy sftp://regress@%s:%s/%s /hd/%s"%(scriptServer,getPath,fileName,fileName))
        self.ssx.cmd("load conf /hd/%s"%fileName,timeout=10000)
        self.ssx.cmd("boot config file /hd/%s"%fileName,timeout=10000)
	
	# Verifying the number of tunnels role config
	self.myLog.info("High level check for tunnel-role config disappear")
	cntOp = self.ssx.cmd('show config | grep "tunnel-setup-role" | count')
	tuncntOp = self.ssx.cmd('show config tunnel | grep "tunnel-setup-role" | count')
	if int(cntOp.split()[-1]) < noOfTunnels:
		self.myLog.error("\nTunnel-role config is disappeared from 'show configuration'\n")
		self.myLog.info("\nDisappered lines : %s\n"%(int(noOfTunnels) - int(cntOp.split()[-1])))
	if int(tuncntOp.split()[-1]) < noOfTunnels:
                self.myLog.error("Tunnel-role config is disappeared from 'show configuration tunnel'")
		self.myLog.info("\nDisappered lines : %s\n"%(int(noOfTunnels) - int(tuncntOp.split()[-1])))

        # Clear the SSX config
        self.ssx.clear_config()

        # Get the Number of lines in conf before reloading the SSX
        self.ssx.cmd("load conf /hd/%s"%fileName,timeout=10000)
        self.myLog.info("Getting the Number of lines in show conf before reloading the SSX")
        self.myLog.info("\n\n Check the Number of lines in the config before reloading the SSX \n\n")
        out = self.ssx.cmd("show configuration | count",timeout=180)
        numOfLinesBefReboot = int(out.split(":")[1].strip())
        self.myLog.output("\n\n Number of Lines in the output before reloading the SSX are %s\n\n"%numOfLinesBefReboot)

        # Reload the SSX with boot config file
        self.myLog.info("\n\n Reload the SSX with boot config file set to /hd/%s \n\n"%fileName)
        self.ssx.reload_device(timeout=180)
        self.myLog.info("\n\n Check the Number of lines in the config after reloading the SSX \n\n")
        self.ssx.cmd("term wid infi")
        self.ssx.cmd("term len infi")

	# Get the show conf and show conf tunnel
	self.myLog.info("Getting the show conf and show conf tunnel")
	totalconfOp = self.ssx.cmd("show configuration",timeout=10000)
        op = self.ssx.cmd("show configuration | count")
        numOfLinesAfterReboot = int(op.split(":")[1].strip())
        self.myLog.output("\n\n Number of Lines in the output after reloaded the SSX are %s\n\n"%numOfLinesAfterReboot)
        self.myLog.output("\n\n Number of Lines in the output before reloading the SSX are %s\n\n"%numOfLinesBefReboot)
        self.failIf(numOfLinesBefReboot!=numOfLinesAfterReboot,"Mismatch in the number of lines before and after reboot the SSX")

	totalBytes = 0
	lenwoCR = 0
	lineNo = 0
	self.myLog.info("\n\n Verifying the configuration display buffers for 'show configuration'at boundary limits of 4K,8K,16K,32K,64K..,\n\n")
	initVal = 12
	nextBoundary = 2 ** initVal
	totalLen = len(totalconfOp) - 1
	totalconfOp = totalconfOp.splitlines()
	fileOpsplit = fileOp.splitlines()
	self.myLog.info("nextBoundary : %s"%nextBoundary)
	forMe = "lines   | len  | Total      | w/o CR   | Command"
	for item in fileOp.splitlines():
		lineNo = lineNo + 1
		lenwoCR = lenwoCR + len(item)
		totalBytes = lenwoCR + lineNo
		forMe = forMe + "%-8s| %-4s | %-10s | %-8s | %s\n"%(lineNo,len(item),(lenwoCR + lineNo),lenwoCR,item)
		if((totalBytes > nextBoundary-100) and (totalBytes < nextBoundary+100)):
			  initVal = initVal + 1
			  nextBoundary = 2 ** initVal
			  self.myLog.info("nextBoundary : %s"%nextBoundary)
			  for Index in xrange(thresholdVal):
			    if (fileOpsplit[lineNo-Index].strip() != totalconfOp[lineNo+1-Index].strip()):
			      self.myLog.info(fileOpsplit[lineNo-Index].strip())
			      self.myLog.info(totalconfOp[lineNo+1-Index].strip())
			      self.myLog.info("*"*70)
			      self.myLog.error("Line is disapperead")
			      self.myLog.info("Line Number     : %s"% (lineNo+1-Index))
                              self.myLog.info("Total Bytes     : %s"% (totalBytes + len(fileOpsplit[lineNo])))
                              self.myLog.info("Disappered Line : %s"% fileOpsplit[lineNo])
			      self.myLog.info("*"*70)
			      break

			    if fileOpsplit[lineNo+Index].strip() != totalconfOp[lineNo+1+Index].strip():
                              self.myLog.error("Line is disapperead")
                              self.myLog.info("*"*70)
                              self.myLog.info("Line Number     : %s"% (lineNo+1-Index))
                              self.myLog.info("Total Bytes     : %s"% (totalBytes + len(fileOpsplit[lineNo])))
                              self.myLog.info("Disappered Line : %s"% fileOpsplit[lineNo])
                              self.myLog.info("*"*70)
			      break
	
	initVal = 12
        self.myLog.info("\n\n Verifying the configuration display buffers for 'show configuration tunnel'at boundary limits of 4K,8K,16K,32K,64K..,\n\n")
	tunfileOp = commands.getoutput("cat %s"% tunFileName)
	tunnelconfOp = self.ssx.cmd("show configuration tunnel",timeout=10000)
        totalBytes = 0
        lenwoCR = 0
        lineNo = 0
        nextBoundary = 2 ** initVal
        tunnelconfOp = tunnelconfOp.splitlines()
        tunfileOpsplit = tunfileOp.splitlines()
        self.myLog.info("nextBoundary : %s"%nextBoundary)
	

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_1_9_1.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_NTT_1_9_1)
        test_runner().run(suite)

