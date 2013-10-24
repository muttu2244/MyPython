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
       Description             :       Periodic retrival of statistics
       Author                  :       Rajshekar
"""


### Import the system libraries we need.
import sys, os, getopt, time, re, random

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### import the Stoke libraries we need.
from SSX import SSX
from Linux import Linux
from log import buildLogger
from StokeTest import test_case, test_suite, test_runner
from helpers import *
from logging import getLogger
import pexpect

import time
from threading import Thread

class test_getStats(Thread):
    def __init__ (self,ssxHand,g35Hand,emuName="abcd",ctxt="noCtxt",slot="-1",numCycles="20",dirFileName="",g35Stats="yes"):
          Thread.__init__(self)
          self.ssx_handle = ssxHand
          self.g35Hand    = g35Hand
          self.ctx        = ctxt
          self.slot       = slot          
          self.numCycles  = numCycles
          self.dirFileName = dirFileName
          self.emuName =  emuName
          self.g35Stats = g35Stats

    def run(self):

        ssxHand = self.ssx_handle
        g35Hand = self.g35Hand
        ctxt  = self.ctx
        slot    = self.slot 
        numCycles  = int(self.numCycles)
        dirName    = self.dirFileName
        emuName = self.emuName
        g35Stats = self.g35Stats

        boarder = "\n" + "#" *50 + "\n"

        mdostats = []
        g35stats = []
        #var['numCycle'] = 2
        #=======

        # How many cycles you want to run
        if ctxt != "noCtxt" :
             fileName = "%s/SSX_MDO_SES_%s_COUNTERS"%(dirName,ctxt)
             for i in range(0,numCycles):
                 # SSX STATS
                 shClock1 = boarder + "SSX CLOCK BEFORE MEASUREMENTS" + boarder + ssxHand.cmd("show clock")
                 shSyscount = boarder + "SSX SYSCOUNT" + boarder + ssxHand.cmd("show syscount")
                 mdoSesCntrs = boarder + "SSX mdoSesCntrs" + boarder + ssxHand.cmd("show mdo session counter")
                 poCntrs = boarder + "SSX poCntrs" + boarder + ssxHand.cmd("show  port counters")
                 ma =  boarder + "ma shared counters "+ boarder + ssxHand.cmd("sh module mdo slot 2 ma shared")
                 sm = boarder + "sm counters"+ boarder + ssxHand.cmd("show mdo count det sm c %s"%ctxt)
                 ranap = boarder + "RANAP counters"+ boarder + ssxHand.cmd("show mdo count det ranap c %s"%ctxt)
                 app = boarder + "APP counters"+ boarder + ssxHand.cmd("show mdo count det app c %s"%ctxt)
                 m3ua = boarder + "M3UA counters"+ boarder + ssxHand.cmd("show mdo count det m3ua c %s"%ctxt)
                 sccp = boarder + "SCCP counters"+ boarder + ssxHand.cmd("show mdo count det sccp c %s"%ctxt)
                 sctp = boarder + "SCTP counters"+ boarder + ssxHand.cmd("show mdo count det sctp c %s"%ctxt)
                 
                 mdostats.append(shClock1)
                 
                 mdostats.append(sm)
                 mdostats.append(ranap)
                 mdostats.append(app)
                 mdostats.append(m3ua)
                 mdostats.append(sccp)
                 mdostats.append(sctp)
                 mdostats.append(shSyscount)
                 mdostats.append(sccp)
                 mdostats.append(mdoSesCntrs)
                 mdostats.append(poCntrs)

                 mdostat = "".join(mdostats)
                 ssxStats = ""
                 ssxStats = boarder + "SSX STATISTICS:" +  mdostat
                 # Let's create a file and write it to disk.
                 os.system("rm -rf %s"%fileName)
                 # Create a file object:
                 # in "write" mode
                 FILE = open(fileName,"a")
                 # Write all the lines at once:
                 FILE.writelines(ssxStats)
                 FILE.close()

        if slot != "-1" :
            
             fileName = "%s/SSX_MDO_SLOT_%s_COUNTERS"%(dirName,slot) 
             for i in range(0,numCycles):
                 # SSX STATS                
                 shClock1 = boarder + "SSX CLOCK BEFORE MEASUREMENTS" + boarder + ssxHand.cmd("show clock")
                 memCntrs = boarder + "SSX memCntrs"+ boarder + ssxHand.cmd("show process mem sl %s"%slot)
                 cpuCntrs = boarder + "SSX cpuCntrs"+ boarder + ssxHand.cmd("show process cpu sl %s"%slot)
                 fpd = boarder + "FPD counters"+ boarder + ssxHand.cmd("show fpd appli sl %s" %slot)
                 
                 mdostats.append(shClock1)
                 
                 mdostats.append(memCntrs)
                 mdostats.append(cpuCntrs)
                 mdostats.append(fpd)
                
                 mdostat = "".join(mdostats)
                 ssxStats = ""
                 ssxStats = boarder + "SSX STATISTICS:" +  mdostat
                 # Let's create a file and write it to disk.
                 os.system("rm -rf %s"%fileName)
                 # Create a file object:
                 # in "write" mode
                 FILE = open(fileName,"a")
                 # Write all the lines at once:
                 FILE.writelines(ssxStats)
                 FILE.close()

        if g35Stats == "yes" :
            countNameDic = {"Retransmissions Data":"retraData",\
                                 "Gaps detected"       :"gapsDet",\
                                 "Data Packets Sent"   :"dataPktSnt",\
                                 "Data Segments Sent"  :"dataSegSnt",\
                                 "Data Packets Received":"dataPktRcd",\
                                 "Data Segments Received":"dataSegRcd"}
            fileName = "%s/G35_MDO_EMU_%s_COUNTERS"%(dirName,emuName)
            out = ""
            for i in range(0,numCycles):
                 shClock1 = "\n\n" + boarder + "SSX CLOCK BEFORE MEASUREMENTS" + boarder + ssxHand.cmd("show clock")
                 g35stats.append(shClock1)
                 for key in countNameDic :
                         outPut = g35Hand.cmd("show %s \'Statistics.%s\'"%(emuName,key))
                         out = out + "\n" + outPut    
                         if "ERROR" in outPut :
                             print "\n\n########################################"
                             print "You have given the Incorrect Emulation Name : %s"%emuNameList[index]
                             return "Fail"
                 g35stats.append(out)
                 g35stat = "".join(g35stats)
                 g35Stats = ""
                 g35Stats = boarder + "G35 COUNTERS" +  g35stat
                 # Let's create a file and write it to disk.
                 os.system("rm -rf %s"%fileName)
                 # Create a file object:
                 # in "write" mode
                 FILE = open(fileName,"a")
                 # Write all the lines at once:
                 FILE.writelines(ssxStats)
                 FILE.close()

