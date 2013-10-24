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

DESCRIPTION: "Enable to boot from CF.Enable to copy/remove files between CF and HD, and check no packet loss during this activity."
TEST PLAN: 
TEST CASES: NTT_7_13_1

Topology Diagram :

IXIA ---------> 3/0 SSX 3/1 -------> IXIA

HOW TO RUN: python2.5 NTT_7_13_1.py
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

class test_NTT_7_13_1(test_case):
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

    def test_NTT_7_13_1(self):

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

        self.ssx.cmd("delete /hd/boot.nonfs.bin_test nocon")
        #self.ssx.cmd("delete /cfint/ssx.cfg nocon")
        self.ssx.cmd("delete /cfint/boot.nonfs.bin_test nocon")
        # Push SSX config
        self.ssx.config_from_string("%s"%script_var['SSX_7_13_1'])
        self.ssx.cmd("save conf /cfint/ssx.cfg")
        self.ssx.cmd("boot config file /cfint/ssx.cfg")


        # Before going to actual test, making sure SSX has OS in HD  so copying the file from 
        # server to SSX.
        self.myLog.info("\n\n Before going to actual test, making sure HD has OS so copying the file from server to SSX \n\n")
        self.ssx.cmd("term wid infi")
        self.ssx.cmd("term len infi")
        self.ssx.ftppasswd("copy sftp://regress@%s:%s/boot.nonfs.bin /hd/boot.nonfs.bin_test"%(scriptServer,script_var['Stoke_Os_Path']))
        time.sleep(30)
        self.myLog.info("\n\n Copying the OS from HD to CF , to make sure both have OS \n\n")
        self.ssx.cmd("copy /hd/boot.nonfs.bin_test /cfint/boot.nonfs.bin_test")

        # Pull required TCL and IXIA packages to our test topo
        self.ixia.cmd("package require IxTclHal")
        self.ixia.cmd("package require IxTclExplorer")

        # Login with your username
        login = self.ixia.cmd("ixLogin %s"%ixia_owner)
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

        # Delete the OS from HD
        self.myLog.info("\n\n Delete the OS from HD\n\n")
        op = self.ssx.cmd("del /hd/boot.nonfs.bin_test nocon ")
        self.myLog.info("\n\n  successfully Deletes the OS from HD\n\n")

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

        # Copy the OS from CF to HD 
        self.myLog.info("\n\n Copy the OS from CF to HD \n\n")
        op = self.ssx.cmd("copy /cfint/boot.nonfs.bin_test /hd/boot.nonfs.bin_test") 
        self.myLog.info("\n\n Copied the OS from CF to HD\n\n")

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

        self.ssx.cmd("delete /hd/boot.nonfs.bin_test nocon")
        #self.ssx.cmd("delete /cfint/ssx.cfg nocon")
        self.ssx.cmd("delete /cfint/boot.nonfs.bin_test nocon")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        log = buildLogger("NTT_7_13_1.log", debug=True,console=True)
        suite = test_suite()
        suite.addTest(test_NTT_7_13_1)
        test_runner(stream=sys.stdout).run(suite)


