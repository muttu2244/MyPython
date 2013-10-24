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

#====================
#------- SOAK SET UP IS USING BRAMHA FOR STORING CDR LOGS BUT THE COMMAND RESPONSE is very slow.
#Before using this API , Better to copy CDR LOGS to OTHER MACHINE AND in to 
#THE path (Line Num : 114) which is statically set to /home/regress/CDR. 
#IF YOU ARE USING OTHER THAN BRAHMA please Uncomment the 113 and remove the Line Num 114.

def verifyCdrRecords(selfSsx,selfLinux,soakType="2",loopCnt="10",ctxtList=[],dataVerf={}):
        """
        Description : API used to verify the Correct Number of CDR records are generated or not.

        Arguments   : soakType : Type of Soak ("RANAP MIX"  OR "SESSION FLAP SOAK")
                      if soakType  = "1" then it is "RANAP MIX SOAK"
                      if soakType  = "2" then it "SESSION FLAP SOAK"
                      loopCnt : how many times loop was repeated incase of "SESSION FLAP SOAK"
                      ctxtEvtSubCountPathList = Elements in List are : contextName,EventName,NumberOfSubscribers,PathOfCdrRecords

        Example     : Verifying the Records in RANAP MIX SOAK
                      Ex1 : verifyCdrRecords(self.linux,soakType="1",ctxtList=["1","2"])

                      Verifying the Records in SESSION FLAP SOAK
                      Ex1 : verifyCdrRecords(self.linux,soakType="2",loopCnt="40",ctxtList=["1","2"])
        ReturnValue : NA
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
           print "No contexts given as input - Please give the context name in list"
           return 0

        #================= Loop Through the CDR generated in each context
        for context in ctxtList :

            #================ Get the Total Number of Active Sessions
            selfLinux.cmd("end")
            selfSsx.cmd("end")
            output = selfSsx.cmd("show mdo counter det sm context %s | grep \"Activate PDP Context Accept\""%context)
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
            subCount = 0
            for actSesCnt in actSesCntList :
                subCount = subCount + int(actSesCnt)
            #subCount = 2000

            #======= Get the File Format
            out = selfSsx.cmd("sh configuration context %s | grep file-format"%context)
            fileFrmt = out.split()[1]
            fileFrmt = "xml"    

            #======= Get the Event
            out = selfSsx.cmd("sh configuration context %s | grep upload-profile"%context)
            event = out.split()[1]
            event = "sftp"

            #======= Get the path 
            out = selfSsx.cmd("sh configuration context %s | grep username"%context)
            homeDir = out.split()[1]
            out = selfSsx.cmd("sh configuration context %s | grep directory"%context)
            if len(out) == 0 :
               error = 1
               errList.append("For Context %s \n : %s"%context)
               errList.append("No directory configured in your configuration")
               continue
            #path ="/"+"%s"%homeDir+"/"+"%s"%out.split()[8]      
            path ="/root/cdr/mdo1-1"

            #======== Get CDR Files on Linux Server
            file_List =  selfLinux.cmd("sudo ls -rth %s | grep %s | grep %s | grep %s"%(path,fileFrmt,context,event))
            file_List = file_List.strip()
            file_List = file_List.split()
            numOfFiles = len(file_List)

            #============= Check CDR records are generated or not
            if "No such file or directory" in file_List or numOfFiles == 1 :
               error = 1
               errList.append("For Context %s \n : %s"%context)
               errList.append("No CDR files are genearted on Context %s"%context)
               continue

            #======= Get the Last CDR File on Linux Server and Verify the data 
            if len(dataVerf) != 0 :
               infoList.append("Verify the fields in Last Cadr Record file")
               lastFile = selfLinux.cmd("sudo ls -rth %s | grep %s | grep %s | grep %s | tail -1"%(path,fileFrmt,context,event))
               last_File = lastFile.strip()
               
               last_File = last_File.split()[2]
               data = selfLinux.cmd("sudo cat %s/%s | tail -30"%(path,last_File))
               dataList = data.split("\n")
               infoList.append("Verfiy the Data in Last CDR Record")
               for value in dataVerf :
                   for data in dataList :
                       if re.search("<%s>\d+</%s>"%(value,value),"%s"%data) :
                          match = re.search("<%s>\d+</%s>"%(value,value),"%s"%data).group(0)
                          actCount = re.search("\d+",match).group(0)
                          expCount = dataVerf[value]
                          infoList.append("Field %s : Value is %s "%(value,actCount))
                          if actCount != expCount :
                             error = 1

                             errList.append("Expected Value for %s is %s but actual value is %s"%(value,expCount,actCount))
            infoList.append("\n\n\n")

            #RANAP MIX SOAK
            """
            This soak intend to simulate real network traffic ,RANAP messages generated in live network
            and test SSX's capabilities to handle and sustain this Network traffic.
            On an average each users goes through this cycle in a 3 hour period.
            1 Attach + 2Activate + 20 Location Updates + 12 Re-locations + 2Deactivates + 1 Detach.
            """

            #SESSION FLAP SOAK
            """
            This soak is designed match session flap by doing activations and deactivations.
            Attach + Activate + Data send + Deactivate + Detach in loop
            """

            #Check for RANAP MIX SOAK
            if soakType == "1" :
               soakVer = 1 
               #Check number of start and stop records
               expNumStartRcds = 14 * int(subCount)
               expNumStopRcds  = 14 * int(subCount)

            #CHECK FOR SESSION FLAP SOAK
            elif soakType == "2" :
               soakVer = 1
               #Check number of start and stop records
               expNumStartRcds = (int(loopCnt) * 1) * int(subCount)
               expNumStopRcds  = (int(loopCnt) * 1) * int(subCount)
            else :
               #Code can be added here for verifying the CDR records related to nonsoak 
               soakVer = 0

            #=========== Get the Number of CDR Start,Stop and Interim Records generated in each file
            startRcdList = []
            stopRcdList  = []
            intrmRcdList = []
            numOfFiles = len(file_List)
            init1 = 0
            selfLinux.cmd("cd %s"%path)
            if numOfFiles :               
                while numOfFiles-1:
                      file = file_List[init1]
                      count = selfLinux.cmd("sudo cat %s/%s | grep \"<SessionStartRecord>\" | wc -l"%(path,file))
                      count = count.split()[:-1][-1]
                      startRcdList.append(count)                
                      count = selfLinux.cmd("sudo cat %s/%s | grep \"<SessionStopRecord>\" | wc -l"%(path,file))
                      count = count.split()[:-1][-1]
                      stopRcdList.append(count)
                      #count = selfLinux.cmd("sudo cat %s/%s | grep \"<SessionInterimRecord>\" | wc -l"%(path,file))
                      #count = count.split()[:-1][-1]
                      #count = re.search("\d+",count).group(0)
                      #intrmRcdList.append(count)
                      init1 = init1 + 1
                      numOfFiles = numOfFiles - 1

            #=========== Get the Total Number of CDR Start,Stop and Interim Records generated
            actNumStartRcds = 0
            actNumStopRcds  = 0
            intrmRcdCount   = 0
            for cou in startRcdList :
                actNumStartRcds = actNumStartRcds + int(cou)

            for cou in stopRcdList :
                actNumStopRcds  = actNumStopRcds + int(cou)

            for cou in intrmRcdList :
                intrmRcdCount =  intrmRcdCount + int(cou)

            #========== Verify the Correct Number Of Start and Stop Records and Interim Records generated
            if soakVer == 1 :
               if soakType == "1" :
                  infoList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(context,subCount))
               elif soakType == "2" :
                  infoList.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s"%(context,subCount,loopCnt))
            else :
               #Code can be added here for verifying the CDR records related to nonsoak
               infoList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(context,subCount))

            infoList.append("Actual Num Of CDR Interim Records : %s"%intrmRcdCount)
            infoList.append("Actual Num Of CDR Start Records : %s - Num Of CDR Stop Records : %s "%(actNumStartRcds,actNumStopRcds)) 

            if intrmRcdCount == 0 :
                infoList.append("CDR Interim records generated are %s"%intrmRcdCount)

            if expNumStartRcds != actNumStartRcds :                 
               error = 1 
               if soakType == "1" :
                  errList.append("For Context %s \n \t\t\t Num Of UEs : %s"%(context,subCount))
               elif soakType == "2" :
                  errList.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s"%(context,subCount,loopCnt))

               errList.append("Actual Num Of CDR Start Records : %s "%actNumStartRcds)
               errList.append("But Expected Num Of CDR Start Records : %s "%(expNumStartRcds))

            if expNumStopRcds != actNumStopRcds :
               error = 1
               if soakType == "1" :
                  error.append("For Context %s \n \t\t\t Num Of UEs : %s"%(context,subCount))
               elif soakType == "2" :
                  error.append("For Context %s \n  \t\t\tNum Of UEs : %s Number Of Loops : %s"%(context,subCount,loopCnt))
               errList.append("Actual Num Of CDR Stop Records : %s "%actNumStopRcds)
               errList.append("But Expected Num Of CDR Stop Records : %s "%(expNumStopRcds))
            infoList.append("\n\n")

        log.info("\n\n\n\n########################################")
        log.info("Information regarding CDR START,STOP and Interim Records generated ")
        for  info in infoList :
             log.info("%s"%info)
        log.info("########################################\n\n\n\n")

        if error == 1  :
            log.info("\n\n\n\n########################################")
            log.info("BELOW STEPS FAILED")

            for err  in errList :
                error = 1
                log.error("%s"%err)
            log.info("########################################\n\n\n\n")
            return 0
        else :
            return 1

