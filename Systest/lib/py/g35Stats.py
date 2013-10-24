#!/usr/bin/python2.5
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
DESCRIPTION             : APIs for G35 STATS

TEST PLAN               : NA
AUTHOR                  : Rajshekar - rajshekar@stoke.com
REVIEWER                : 
"""

### Import the system libraries we need.
import sys, os, re

### path.
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
from logging import getLogger
# grab the root logger.
log = getLogger()

boarder = "\n" + "-" *50 + "\n"


def get_g35_stats(self,emuName):
       """
       Description : Get the emulation related counters on G35
       Arguments   : emuName - Name of the Emulation
       Usage       : get_g35_stats(self.tek,"U3-RNC-UMTSGM")
       Returns     : Returns emulated related counters and values in dictionary and 0 on Failure
       """

       countType = "Overview"     
       countNameDic = {"Attach Proc Attempts":"OverAttProcAtte",\
                    "Attach Proc success":"OverAttProcsucc", \
                   "Detach Proc Attempts" : "OverDetProcAtte",\
                   "Detach Proc success":"OverDetProcsucc", \
                   "RAU Proc Attempts" : "OverRauProcAtte",\
                   "RAU Proc success": "OverRauProcsucc", \
                   "Activation Proc Attempts" : "OverActProcAtte",\
                   "Activation Proc success":"OverActProcsucc", \
                   "Deactivation Proc Attempts" : "OverDeactProcAtte",\
                   "Deactivation Proc success" : "OverDeactProcsucc"}

       actual = {}

       for key in countNameDic :
          out = self.cmd("show %s \'Counters.%s.%s\'"%(emuName,countType,key))
          if "ERROR" in out :
             print "\n\n########################################"
             print "You have given the Incorrect Emulation Name : %s"%emuName
             return "Fail"
          actual[countNameDic[key]] = out.split(":")[1]

       countType = "Mobility Management"
       countNameDic = {"Attach Proc Attempts": "MobAttProcAtte", \
                    "Attach Proc success" : "MobAttProcsucc", \
                    "Attach Req sent IMSI" : "MobAttReqIMSI", \
                    "Attach Req sent PTMSI" : "MobAttReqPTMSI", \
                    "Attach Acc recd"       : "MobAttAccRcvd", \
                    "Attach Acc recd with PTMSI" : "MobAttAccRcvdPTMSI", \
                    "Attach Comp sent" : "MobAttComSnt", \
                    "Detach Proc Attempts": "MobDetProcAtte", \
                    "Detach Proc success" : "MobDetProcsucc", \
                    "Detach Req sent"     : "MobDetReqsent",\
                    "Detach Accept recd" : "MobDetAccRcvd", \
                    "RAU Proc Attempts" : "MobRAUProcAtt", \
                    "RAU Proc Periodic" : "MobRAUProcPer", \
                    "RAU Proc success"  : "MobRAUProcsucc", \
                    "RAU Req sent"      : "MobRAUReqsent", \
                    "RAU Accept recd"   : "MobRAUAccRcvd", \
                    "RAU Accept recd PTMSI" : "MobRAUAccRcvdPTMSI", \
                    "RAU Accept recd Periodic" : "MobRAUAccRcdPer",\
                    "RAU Comp sent" : "MobRAUComSnt", \
                    "Service Proc Attempts": "MobSerProcAtt", \
                    "Service Proc success" : "MobSerProcSuc", \
                    "Service Req sent" : "MobSerReqSnt", \
                    "Service Acc recd" : "MobSerAccRecd", \
                    "Authentication Req recd" : "MobAuthReqrecd", \
                    "Authentication Resp sent" : "MobAuthRespSent"}  

       for key in countNameDic :
          out = self.cmd("show %s \'Counters.%s.%s\'"%(emuName,countType,key))
          actual[countNameDic[key]] = out.split(":")[1]
  
       countType = "Session Management"
       countNameDic = {"Activation Proc Attempts": "SesActProcAtte", \
                    "Activation Proc success" : "SesActProcsucc", \
                    "Activation Req sent" : "SesActReqsnt" , \
                    "Activation Acc recd" : "SesActAccrecd",\
                    "Deactivation Proc Attempts": "SesDeactProcAtte", \
                    "Deactivation Proc success" : "SesDeactProcsucc", \
                    "Deactivation Req sent" : "SesDeactProcReqsnt",\
                    "Deactivation Acc recd" : "SesDeactAccrecd"} 

       for key in countNameDic :
          out = self.cmd("show %s \'Counters.%s.%s\'"%(emuName,countType,key))
          actual[countNameDic[key]] = out.split(":")[1]

       return actual

def verify_g35_stats(self,numUE,emuName="abcd",soakType="2",loopCnt="10"):
    """
    NOTE : Expect SHOULD BE THE ARGUEMNT of the FUCNTION but INORDER TO MAKE WORK EASIER,
    DEFINED IN FUNCTION TEMPORARILY.   
    Description : Verify the emulation related counters on G35
    Arguments   : emuName - Name of the Emulation --- It takes the string 
                            value and should be the emulation name on g35
                  numUE   - Number of UEs ---- It takes the integer value
                  soakType - 2 for SESSION FLAP SOAK with loopCnt 
                           - 1 for RANAP MIX SOAK 
    Usage       : verify_g35_stats(self.tek,10,emuName="U3-RNC-UMTSGM",soakType="1")
                  verify_g35_stats(self.tek,10,emuName="U3-RNC-UMTSGM",soakType="2",loopCnt=10)
    Returns     : Returns 1 on success and 0 on Failure
    """

    if emuName=="abcd" :
       print "Please specify the emuName while calling the function "
       return 0

    if int(soakType) == 2 :
       loopCnt=int("%s"%loopCnt)

    actual = get_g35_stats(self,emuName)
    if "Fail" in actual :
       return 0

    expect = {}
    if int(soakType) == 1 :
        expect["MobDetProcAtte"] = 1 * int(numUE) 
        expect["MobRAUAccRcvd"] =  1  * int(numUE) 
        expect["MobRAUProcPer"] =  8 * int(numUE) 
        expect["MobRAUComSnt"] =   20 * int(numUE) 
        expect["MobRAUReqsent"] =  20 * int(numUE) 
        expect["MobAttAccRcvd"] =  1 * int(numUE) 
        expect["MobAttReqIMSI"] =  1 * int(numUE) 
        expect["MobAttProcAtte"] =   1 * int(numUE) 
        expect["MobAttProcsucc"] = 1 * int(numUE) 
        expect["MobAttAccRcvdPTMSI"] = 1 * int(numUE) 
        expect["MobAttComSnt"] = 1 * int(numUE) 
        expect["MobRAUAccRcdPer"] =  8 * int(numUE) 
        expect["MobAttReqPTMSI"] =   1 * int(numUE) 
        expect["MobRAUProcAtt"] = 20 * int(numUE) 
        expect["MobSerProcAtt"] = 2 * int(numUE) 
        expect["MobSerReqSnt"] = 2 * int(numUE) 
        expect["MobSerAccRecd"] =  2 * int(numUE) 
        expect["MobDetProcsucc"] =  1 * int(numUE) 
        expect["MobRAUProcsucc"] = 20 * int(numUE) 
        expect["MobSerProcSuc"] = 2  * int(numUE) 
        expect["MobDetProcsucc"] =  1 * int(numUE) 
        expect["MobRAUAccRcvdPTMSI"] = 20 * int(numUE) 
        expect["MobDetReqsent"] =  1 * int(numUE) 
        expect["MobDetAccRcvd"] = 1 * int(numUE) 
 
        expect["SesDeactProcsucc"] = 2  * int(numUE) 
        expect["SesDeactProcReqsnt"] = 2 * int(numUE) 
        expect["SesActProcAtte"] =  2 * int(numUE) 
        expect["SesDeactAccrecd"] = 2 * int(numUE) 
        expect["SesDeactProcAtte"] = 2 * int(numUE) 
        expect["SesActReqsnt"] = 2 * int(numUE) 
        expect["SesActAccrecd"] = 2 * int(numUE) 
        expect["SesActProcsucc"] = 2 * int(numUE) 

        expect["OverDeactProcsucc"] = 2 * int(numUE) 
        expect["OverDetProcAtte"] = 1 * int(numUE) 
        expect["OverDetProcsucc"] = 1 * int(numUE) 
        expect["OverAttProcsucc"] = 1 * int(numUE) 
        expect["OverRauProcAtte"] = 20 * int(numUE) 
        expect["OverRauProcsucc"] = 20 * int(numUE) 
        expect["OverActProcsucc"] = 1 * int(numUE) 
        expect["OverActProcAtte"] = 1 * int(numUE) 
        expect["OverAttProcAtte"] = 1 * int(numUE) 
        expect["OverDeactProcAtte"] = 2 * int(numUE) 

    else :
        expect["MobDetProcAtte"] = 1 * int(numUE) * loopCnt
        expect["MobRAUAccRcvd"] =  0 * int(numUE) * loopCnt
        expect["MobRAUProcPer"] =  0 * int(numUE) * loopCnt
        expect["MobRAUComSnt"] =   0 * int(numUE) * loopCnt
        expect["MobRAUReqsent"] =  0 * int(numUE) * loopCnt
        expect["MobAttAccRcvd"] =  1 * int(numUE) * loopCnt
        expect["MobAttReqIMSI"] =  1 * int(numUE) * loopCnt
        expect["MobAttProcAtte"] =   1 * int(numUE) * loopCnt
        expect["MobAttProcsucc"] = 1 * int(numUE) * loopCnt
        expect["MobAttAccRcvdPTMSI"] = 1 * int(numUE) * loopCnt
        expect["MobAttComSnt"] = 1 * int(numUE) * loopCnt
        expect["MobRAUAccRcdPer"] =  0 * int(numUE) * loopCnt
        expect["MobAttReqPTMSI"] =   0 * int(numUE) * loopCnt
        expect["MobRAUProcAtt"] = 0 * int(numUE) * loopCnt
        expect["MobSerProcAtt"] = 0 * int(numUE) * loopCnt
        expect["MobSerReqSnt"] = 0 * int(numUE) * loopCnt
        expect["MobSerAccRecd"] =  0 * int(numUE) * loopCnt
        expect["MobDetProcsucc"] =  1 * int(numUE) * loopCnt
        expect["MobRAUProcsucc"] = 0 * int(numUE) * loopCnt
        expect["MobSerProcSuc"] = 0 * int(numUE) * loopCnt
        expect["MobDetProcsucc"] =  1 * int(numUE) * loopCnt
        expect["MobRAUAccRcvdPTMSI"] = 0 * int(numUE) * loopCnt
        expect["MobDetReqsent"] =  1 * int(numUE) * loopCnt
        expect["MobDetAccRcvd"] = 1 * int(numUE) * loopCnt
        expect["MobAuthReqrecd"] = 1 * int(numUE) * loopCnt 
        expect["MobAuthRespSent"] = 1 * int(numUE) * loopCnt
        expect["SesDeactProcsucc"] = 1  * int(numUE) * loopCnt
        expect["SesDeactProcReqsnt"] = 1 * int(numUE) * loopCnt
        expect["SesActProcAtte"] =  1 * int(numUE) * loopCnt
        expect["SesDeactAccrecd"] = 1 * int(numUE) * loopCnt
        expect["SesDeactProcAtte"] = 1 * int(numUE) * loopCnt
        expect["SesActReqsnt"] = 1 * int(numUE) * loopCnt
        expect["SesActAccrecd"] = 1 * int(numUE) * loopCnt
        expect["SesActProcsucc"] = 1 * int(numUE) * loopCnt

        expect["OverDeactProcsucc"] = 1 * int(numUE) * loopCnt
        expect["OverDetProcAtte"] = 1 * int(numUE) * loopCnt
        expect["OverDetProcsucc"] = 1 * int(numUE) * loopCnt
        expect["OverAttProcsucc"] = 1 * int(numUE) * loopCnt
        expect["OverRauProcAtte"] = 0 * int(numUE) * loopCnt
        expect["OverRauProcsucc"] = 0 * int(numUE) * loopCnt
        expect["OverActProcsucc"] = 1 * int(numUE) * loopCnt
        expect["OverActProcAtte"] = 1 * int(numUE) * loopCnt
        expect["OverAttProcAtte"] = 1 * int(numUE) * loopCnt
        expect["OverDeactProcAtte"] = 1 * int(numUE) * loopCnt


    errorList = []
    if soakType == "1" :
       errorList.append("SOAK TYPE : RANAP MIX SOAK")
    else :
       errorList.append("SOAK TYPE : SESSION FLAP SOAK") 

    """ Parses the details of ike session established with remote,
            and stores the SA attributes in a dictionary, and return it"""
    for key in expect :
        if int(actual[key]) != int(expect[key]) :
           errorList.append("Value mismatch for counters %s -- Actual Value : %s but Expected Value : %s"%(key,actual[key],expect[key]))

    if len(errorList) != 0 :
       log.info("\n\n\n######################################")
       for err in errorList :
          log.error("%s"%err)
       log.info("######################################\n\n\n")
       return 0
    else :
       return 1

