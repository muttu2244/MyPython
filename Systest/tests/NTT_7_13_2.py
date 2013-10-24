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

DESCRIPTION: Copy and overwrite configuration from CF and check the configuration is applied, and check no packet loss during this activity
TEST PLAN: 
TEST CASES: NTT_7_13_2

Topology Diagram :

IXIA ---------> 3/0 SSX 3/1 -------> IXIA

HOW TO RUN: python2.5 NTT_7_13_2.py
AUTHOR: rajshekar@stoke.com
REIEWER: 

"""

import sys, os,commands

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
import re
from ixia import *
#import configs file and topo..
from config_raja import *
from topo import *

# Place for variables
fileName = "config_original.cfg" # Original file, should be in current directory.
tunFileName = "tuunnel_config_original.cfg"            # Only tunnel configuration form original file.
noOfTunnels = 99                          # Number of tunnels in the box
thresholdVal = 5                          # This value indicates, number of to and forth to be
                                          # verified for the disappered line at boundary
initVal = 12                              # Initial boundary value, here 2^initVal[ex: 2^12 = 4k,
                                          # so for 4K initail boundary it should be 12.

class test_NTT_7_13_2(test_case):
    myLog = getLogger()

    def setUp(self):
      
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.ssx.telnet()
        self.ixia = IXIA(ixia['ip_addr'])
        self.ixia.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

        # Load minimum configuration
        self.ssx.load_min_config(ssx["hostname"])
 
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        self.ixia.cmd("ixLogout")
        self.ixia.cmd("cleanUp")
        self.ixia.close()

    def test_NTT_7_13_2(self):

        self.myLog.output("==================Starting The Test====================")

        #Get the script location
        getPath = sys.path[0]

        #Get the ip adress of server where you are running the script.
        hostName = commands.getoutput("hostname")
        if "silicon" in hostName:
             scriptServer = "10.10.10.182"
        else:
             scriptServer = commands.getoutput("host %s"% hostName)
             scriptServer = scriptServer.split()[-1]

        # Before going to actual test, am making sure SSX has huge config so copying the file from 
        # server to SSX.
        self.myLog.info("Before going to actual test, am making sure SSX has huge config so copying the file from server to SSX")
        self.ssx.cmd("term wid infi")
        self.ssx.cmd("term len infi")
        self.ssx.cmd("delete /cfint/%s nocon"%fileName)
        self.ssx.cmd("delete /cfint/ssx.cfg nocon")
        self.ssx.ftppasswd("copy sftp://regress@%s:%s/%s /cfint/%s"%(scriptServer,getPath,fileName,fileName))
        self.ssx.cmd("load conf /cfint/%s"%fileName,timeout=10000)
        self.ssx.cmd("save config /cfint/ssx.cfg")
        time.sleep(60)

        # Push SSX config
        self.ssx.config_from_string("%s"%script_var['SSX_7_13_2'])

        # Pull required TCL and IXIA packages to our test topo
        self.ixia.cmd("package require IxTclHal")
        self.ixia.cmd("package require IxTclExplorer")

        # Login with your username
        login = self.ixia.cmd("ixLogin %s"%ixia_owner)
        #login = int(a.splitlines()[-1])
        if not int(login):
           self.myLog.output("User %s has logged in Successfully"%ixia_owner)

        # Push the IXIA Config
        self.ixia.cmd("source \"D:/OSPF_NBMA/Xlated/XLATED_8_3_1_15.tcl\"")

        source1 = self.ixia.cmd("ixTransmitPortArpRequest %s"%p1_ssx_ixia[1])
        if not int(source1):
           self.myLog.output("ARP request sent successfully TX port\n")

        # Push the IXIA Config
        self.ixia.cmd("source \"D:/OSPF_NBMA/Xlated/XLATED_8_3_1_16.tcl\"")
        self.myLog.output("\n\n----Sourcing is done successfully----\n")
        source2 = self.ixia.cmd("ixTransmitPortArpRequest %s"%p2_ssx_ixia[1])
        if not int(source2):
           self.myLog.output("ARP request sent successfully from Rx port\n")

        # Clear the IXIA stats before transmitting traffic
        self.myLog.info("\n\n Clear the IXIA stats before transmitting traffic \n\n")
        self.ixia.cmd("set PortList { { %s } { %s } }"%(p1_ssx_ixia[1], p2_ssx_ixia[1]))
        self.myLog.info("clearing stats: %s"%self.ixia.cmd("ixClearStats PortList"))

        # Start Bidirectional traffic
        self.myLog.info("\n\n Start Bidirectional traffic \n\n")
        Tx1 = self.ixia.cmd("ixStartPortTransmit %s"%p1_ssx_ixia[1])
        if not int(Tx1):
           self.myLog.output("Transmitting on the port %s"%p1_ssx_ixia[1].split()[2])

        Tx2 = self.ixia.cmd("ixStartPortTransmit %s"%p2_ssx_ixia[1])
        if not int(Tx2):
           self.myLog.output("Transmitting on the port %s"%p2_ssx_ixia[1].split()[2])
        self.ssx.cmd("end")

        # Copy the File from CF to Linux Server
        self.myLog.info("\n\n Copy the File from CF to Linux Server\n\n")
        self.ssx.ftppasswd("copy /cfint/ssx.cfg sftp://regress@%s:%s/ssx.cfg"%(scriptServer,getPath))
        self.myLog.info("\n\n File copied successfully from CF to Linux Server\n\n")
        time.sleep(60)

        # Stop Transmitting..
        self.myLog.info("\n\n Stop the traffic from IXIA \n\n")
        self.ixia.cmd("ixStopPortTransmit %s"%p1_ssx_ixia[1])
        self.myLog.output("\nTransmission is stopped at port %s...\n"%p1_ssx_ixia[1].split()[2])

        self.ixia.cmd("ixStopPortTransmit %s"%p2_ssx_ixia[1])
        self.myLog.output("\nTransmission is stopped at port: %s\n"%p2_ssx_ixia[1].split()[2])

        # Get the IXIA stats
        self.myLog.info("\n\n Get the IXIA stats \n\n")
        self.myLog.info("Stats for the port:%s\n"%p1_ssx_ixia[1])
        self.ixia.cmd("stat get statAllStats %s"%p1_ssx_ixia[1])
        PktsSentFrmClntToInt = self.ixia.cmd("stat cget -framesSent")
        PktsRecvdFrmIntToClnt = self.ixia.cmd("stat cget -framesReceived")

        self.myLog.info("Stats for the port:%s\n"%p2_ssx_ixia[1])
        self.ixia.cmd("stat get statAllStats %s"%p2_ssx_ixia[1])
        PktsSentFrmIntToClnt = self.ixia.cmd("stat cget -framesSent")
        PktsRecvdFrmClntToInt = self.ixia.cmd("stat cget -framesReceived")

        self.myLog.info("\n\n Below are the IXIA stats while copying file FROM CF to Linux server \n\n")
        self.myLog.output("\n Traffic sent from Client to Internet %s"%PktsSentFrmClntToInt)
        self.myLog.output("\n Traffic sent from Internet to Client%s"%PktsSentFrmIntToClnt)
        self.myLog.output("\n Traffic received from Client to Internet %s"%PktsRecvdFrmClntToInt)
        self.myLog.output("\n Traffic received from Internet to Client%s"%PktsRecvdFrmIntToClnt)

        self.myLog.info("\n\n Check if there is Packet loss while copying file from CF \n\n")
        pktLoss = int(PktsSentFrmClntToInt) - int(PktsRecvdFrmClntToInt)
        self.failIf(int(PktsSentFrmClntToInt)>int(PktsRecvdFrmClntToInt),"Packet loss of %s observed while copying file from CF"%pktLoss)
        self.myLog.info("\n\n Checked , no packet loss observed while copying file from CF \n\n")

        self.myLog.info("\n\n Clearing the IXIA stat \n\n")
        self.myLog.info("clearing stats: %s"%self.ixia.cmd("ixClearStats PortList"))

        # Start Bidirectional traffic
        self.myLog.info("\n\n Start Bidirectional traffic \n\n")
        Tx1 = self.ixia.cmd("ixStartPortTransmit %s"%p1_ssx_ixia[1])
        if not int(Tx1):
           self.myLog.output("Transmitting on the port %s"%p1_ssx_ixia[1].split()[2])

        Tx2 = self.ixia.cmd("ixStartPortTransmit %s"%p2_ssx_ixia[1])
        if not int(Tx2):
           self.myLog.output("Transmitting on the port %s"%p2_ssx_ixia[1].split()[2])

        self.ssx.cmd("end")
        # Copy the File from Linux Server to CF
        self.myLog.info("\n\n overwriting file in CF\n\n")
        self.ssx.cmd("delete /cfint/ssx.cfg nocon")
        self.ssx.ftppasswd("copy sftp://regress@%s:%s/ssx.cfg /cfint/ssx.cfg"%(scriptServer,getPath))
        self.myLog.info("\n\n Done overwriting file in CF\n\n")
        time.sleep(60)

        # Get the IXIA stats
        self.myLog.info("\n\n Get the IXIA stats \n\n")
        self.myLog.info("Stats for the port:%s\n"%p1_ssx_ixia[1])
        self.ixia.cmd("stat get statAllStats %s"%p1_ssx_ixia[1])
        PktsSentFrmClntToInt = self.ixia.cmd("stat cget -framesSent")
        PktsRecvdFrmIntToClnt = self.ixia.cmd("stat cget -framesReceived")

        self.myLog.info("Stats for the port:%s\n"%p2_ssx_ixia[1])
        self.ixia.cmd("stat get statAllStats %s"%p2_ssx_ixia[1])
        PktsSentFrmIntToClnt = self.ixia.cmd("stat cget -framesSent")
        PktsRecvdFrmClntToInt = self.ixia.cmd("stat cget -framesReceived")

        self.myLog.info("\n\n Below are the IXIA stats while copying file FROM CF to Linux server \n\n")
        self.myLog.output("\n Traffic sent from Client to Internet %s"%PktsSentFrmClntToInt)
        self.myLog.output("\n Traffic sent from Internet to Client%s"%PktsSentFrmIntToClnt)
        self.myLog.output("\n Traffic received from Client to Internet %s"%PktsRecvdFrmClntToInt)
        self.myLog.output("\n Traffic received from Internet to Client%s"%PktsRecvdFrmIntToClnt)

        self.myLog.info("\n\n Check if there is Packet loss while overwriting file in CF \n\n")
        pktLoss = int(PktsSentFrmClntToInt) - int(PktsRecvdFrmClntToInt)
        self.failIf(int(PktsSentFrmClntToInt)>int(PktsRecvdFrmClntToInt),"Packet loss of %s observed while overwriting file in CF"%pktLoss)
        self.myLog.info("\n\n Checked , no packet loss observed while overwriting file in CF CF \n\n")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_7_13_2.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_NTT_7_13_2)
        test_runner(stream=sys.stdout).run(suite)


