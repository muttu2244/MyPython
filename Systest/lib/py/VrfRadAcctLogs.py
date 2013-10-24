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
DESCRIPTION             : APIs for SOAK CASES
TEST PLAN               : MDO SOAK
AUTHOR                  : Rajshekar - rajshekar@stoke.com
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import time
import string
import sys
import re
from pexpect import *

from logging import getLogger
log = getLogger()
from StokeTest import test_case


def verifyRadAcctLogs(selfSsx,selfLinux,soakType="2",loopCnt="10",ctxtList=[],acctLogsPathName="/usr/local/var/log/radius/radacct"):
        """
        Description : API used to verify the Correct Number of Account Start and Stop records are generated 
                      or not for "x" number of UEs in each context depending on Type of SOAK you are running..

        Arguments   :  
                      soakType : Type of Soak ("RANAP MIX"  OR "SESSION FLAP SOAK")
                      if soakType  = "1" then it is "RANAP MIX SOAK"
                      if soakType  = "2" then it "SESSION FLAP SOAK"
                      loopCnt : how many times loop was repeated incase of "SESSION FLAP SOAK"
                      ctxtList = contextNames as list
                      acctLogsPathName = Path of accounting logs

        Example     : Verifying the Records in RANAP MIX SOAK
                      Ex1 : verifyRadAcctLogs(selfList = [self.ssx,self.linux],soakType="1",ctxtList=["%s"%ctxt1,"%s"%ctxt2],acctLogsPathName="/usr/etc/var")
                      Ex1 : verifyRadAcctLogs(selfList = [self.ssx,self.linux],soakType="1",ctxtList=["%s"%ctxt1,"%s"%ctxt2])

                      Verifying the Records in SESSION FLAP SOAK
                      Ex1:verifyRadAcctLogs(selfList=[self.ssx,self.linux],soakType="2",loopCnt="20",ctxtList=["%s"%ctxt1,"%s"%ctxt2],acctLogsPathName="/usr/etc/var")
                      Ex2 :verifyRadAcctLogs(selfList = [self.ssx,self.linux],soakType="2",loopCnt="10",ctxtList=["%s"%ctxt1,"%s"%ctxt2])
        ReturnValue : 1 on Success and 0 on Failure
        """

        #===========  Initialize errorList and InfoList for displaying the output at the end
        #             (which is useful for debugging purpose )
        error = 0
        errList = []
        infoList = []
        if soakType == "1" :
           infoList.append("RANAP MIX SOAK : \n ")
        if soakType == "2" :
           infoList.append("SESSION FLAP SOAK : \n")

        #============= context list should not be empty
        if len(ctxtList) == 0 :
           errList.append("No contexts given as input - Please give the context name in list")
           return 0

        #=======  Get the context and NAS ip configred in dictionary 
        ctxtAndNasIpDict = {}
        for ctxt in ctxtList :
            out = selfSsx.cmd("sh conf cont %s | grep nas-ip-address"%ctxt)
            if "nas-ip-addr" in out :
               ipAddr = out.split()[3]
               ctxtAndNasIpDict[ctxt] = ipAddr

        #============= Get  the contexts       
        ctxts = ctxtAndNasIpDict.keys()

        #============== Loop through the contexts for verifying Radius Account Start and Stop Logs
        for ctxt in ctxts :
            nasIp = ctxtAndNasIpDict[ctxt]

            #================ Get the Total Number of Active Sessions
            output = selfSsx.cmd("show mdo counter det sm context %s | grep \"Activate PDP Context Accept\""%ctxt)
            actPdpList = []
            output = output.strip().split("\n")
            actSesCntList = []
            for out in output:                
                out = out.strip()  
                if re.search("\s*Activate PDP Context Accept\s+:\s+\d+",out) :
                   pdpList = re.search("\s*Activate PDP Context Accept\s+:\s+\d+",out) 
                   outr =  pdpList.group(0)
                   count = re.search("\d+","%s"%outr).group(0)
                   actSesCntList.append(count)
            numOfActSes = 0
            for actSesCnt in actSesCntList :
                numOfActSes = numOfActSes + int(actSesCnt)

            #================= Get the Filename on Linux server
            acctLogsPathName1 = "%s/%s"%(acctLogsPathName,nasIp)
            fileName = selfLinux.cmd("sudo ls -rth %s | grep detail | tail -1"%acctLogsPathName1)
            
            #================= Verify wether the Record is generated or not
            if "No such file or directory" in fileName :
               errList.append("No Account Start and Stop Records are genearted on Context %s"%ctxt) 
               continue
        
            #================= Get the actual number of Account Start and Stop Records
            fileName = re.search("detail-\d+",fileName).group(0)
            fileName = fileName.split()[0]              
            startCount = selfLinux.cmd("sudo grep \"Acct-Status-Type = Start\" %s/%s | wc -l"%(acctLogsPathName1,fileName))
            l = re.search("\d+",startCount)
            count= l.group(0)
            actStartActRcds = count
            stopCount = selfLinux.cmd("sudo grep \"Acct-Status-Type = Stop\" %s/%s | wc -l"%(acctLogsPathName1,fileName))
            l = re.search("\d+",stopCount)
            count= l.group(0)
            actStopActRcds = count

            #================= Get the Expected  number of Account Start and Stop Records
            #=======  Check for RANAP MIX SOAK
            if soakType == "1" :
               soakVer = 1
               #Check number of start and stop records
               expStartActRcds = 14 * int(numOfActSes)
               expStopActRcds  = 14 * int(numOfActSes)

            #========  CHECK FOR SESSION FLAP SOAK
            elif soakType == "2" :
               soakVer = 1
               #Check number of start and stop records
               expStartActRcds = (int(loopCnt) * 1) * int(numOfActSes)
               expStopActRcds  = (int(loopCnt) * 1) * int(numOfActSes)
            else :
               #Code can be added here for verifying the Radius account logs related to nonsoak
               soakVer = 0

            #========== Verify the Correct Number Of Start and Stop Account Records generated
            if soakVer == 1 :
               if soakType == "1" :
                  infoList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(ctxt,numOfActSes))
               elif soakType == "2" :
                  infoList.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s\n\n"%(ctxt,numOfActSes,loopCnt))
            else :
               #Code can be added here for verifying the Radius account logs related to nonsoak
               infoList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(ctxt,numOfActSes))

            infoList.append("Actual Num Of Acct Start Records : %s - Num Of Acct Stop Records : %s \n\n\n"%(actStartActRcds,actStopActRcds))

            if expStartActRcds != actStartActRcds :
               if soakType == "1" :
                  errList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(ctxt,numOfActSes))
                  errList.append("Actual Num Of Acct Start Records : %s - Num Of Acct Stop Records : %s "%(actStartActRcds,actStopActRcds))
               elif soakType == "2" :
                  errList.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s"%(ctxt,numOfActSes,loopCnt))
                  errList.append("Actual Num Of Acct Start Records : %s - Num Of Acct Stop Records : %s "%(actStartActRcds,actStopActRcds))
               errList.append("But Expected Num Of Acct Start Records : %s "%(expStartActRcds))

            if expStopActRcds != actStopActRcds:
               if soakType == "1" :
                  errList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(ctxt,numOfActSes))
                  errList.append("Actual Num Of Acct Start Records : %s - Num Of Acct Stop Records : %s "%(actStartActRcds,actStopActRcds))
               elif soakType == "2" :
                  errList.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s"%(ctxt,numOfActSes,loopCnt))
                  errList.append("Actual Num Of Acct Start Records : %s - Num Of Acct Stop Records : %s "%(actStartActRcds,actStopActRcds))
               errList.append("But Expected  Num Of Acct Stop Records : %s\n\n\n"%(expStopActRcds))

        log.info("\n\n\n\n########################################")
        log.info("Information Regarding Total Number of Account Start and Stop Records")
        for  info in infoList :
             log.info("%s"%info)
        log.info("########################################\n\n\n\n")

        if error :
           log.info("\n\n\n\n########################################")
           log.info("BELOW STEPS FAILED")
           for err  in errList :
               log.error("%s"%err)
           log.info("########################################\n\n\n\n")
           return 0
        else :
           return 1

