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
DESCRIPTION             : APIs for MDO Soak and other scripts
TEST PLAN               : NA
AUTHOR                  : Rajshekar - rajshekar@stoke.com
REVIEWER                :
DEPENDENCIES            : NA
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

def ses_check(self, dest_ip="20.1.1.2"):

       """
       Description : API used to Checks the MDO Session formation in SSX for a particular tunnel ip.

       Arguments   : dest_ip : Ip Address of Destination

       Example     : ses_check(self.ssx,dest_ip="20.1.1.2")

       ReturnValue : 0 if Fails else command output
       """

       ses_exist=self.cmd("show mdo session detail address %s | grep ACTIVE"  % dest_ip)
       if ses_exist and "ERROR:" not in ses_exist:
               return ses_exist
       else:
               return False

def get_mdo_session_hand_detail(self,context="local") :

       """
       Description : API used to get the session deatails [Inluding Session Counters].
                     #Commands "show mdo session detail handle <handle>" and "show session detail handle <handle>"
                     #are having the different counter fields.[For Ex : Session Start Time,Ip Acl In/Out ........]

       Arguments   : context : Name of the context

       Example     : get_mdo_session_hand_detail(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       #For Displaying errors at the end
       errorList = []

       #For Session handle list
       sesHandList = []

       #============================== Get the Session Handle List
       self.cmd("context %s"%context)
       self.cmd("term len infi")
       self.cmd("term wid infi")
       out = self.cmd("show mdo session | grep \"Session Handle\"")
       if "ERROR" in out :
          return 0 
       sesHandles = out.split("\n")
       len1 = len(sesHandles)
       for sesHand in sesHandles:
           if sesHand == "\r" or len(sesHand) == 0 :
              continue
           sesHand = sesHand.split(":")[1]
           if "\r" in sesHand :
              sesHand = sesHand.split("\r")[0].strip()
           else :
              sesHand = sesHand.strip()
           sesHandList.append(sesHand)

       #================================ Create the Regular Expression
       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.       
       regex_list=['\s+SLOT\s+:\s+(?P<slotNum>\w+)',
                    '\s+Context\s+ID\s+:\s+(?P<contextId>\d+)',
                    '\s+IMSI\s+:\s+(?P<imsi>\w+)',
                    '\s+IMEI\s+:\s+(?P<imei>\S+)',
                    '\s+S-RNC\s+ID\s+:\s+(?P<rncId>\d+)',
                    '\s+Session\s+Handle\s+:\s+(?P<sessionHandle>\w+)',
                    '\s+APN\s+:\s+(?P<apn>\S+)',
                    '\s+Offload\s+Criteria\s+:\s+(?P<offloadCriteria>\w+\s+\d+)',
                    '\s+Session\s+Addr\s+:\s+(?P<sessionAddr>\S+)',
                    '\s+Local\s+IP\s+:\s+(?P<localIp>\S+)',
                    '\s+Local\s+TEID\s+:\s+(?P<localTeid>\w+)',
                    '\s+Remote\s+IP\s+:\s+(?P<remoteIp>\S+)',
                    '\s+Remote\s+TEID\s+:\s+(?P<remoteTeid>\w+)',
                    '\s+SGSN\s+IP\s+:\s+(?P<sgsnIp>\S+)',
                    '\s+Traffic\s+Class\s+:\s+(?P<trafficClass>\w+)',
                    '\s+Transfer\s+Delay\s+:\s+(?P<transferDelay>\d+)',
                    '\s+Traffic\s+Handling\s+priority\s+:\s+(?P<trafficHandlingPriority>\d+)',
                    '\s+Max\s+bit\s+rate\s+-\s+Uplink\s+:\s+(?P<maxUplink>\S+)',
                    '\s+Max\s+bit\s+rate\s+-\s+Downlink\s+:\s+(?P<maxdownLink>\S+)']       
       """ 
       #Taking the Counters which are in CDR files genearated on SSX.
       regex_list=['\s+IMSI\s+:\s+(?P<imsi>\w+)',
                    '\s+Session\s+Handle\s+:\s+(?P<sessionHandle>\w+)',
                    '\s+APN\s+:\s+(?P<apn>\S+)',
                    '\s+Session\s+Addr\s+:\s+(?P<sessionAddr>\S+)']
       """ 
       regex_list2=['\s*Session\s+established\s+at\s*:\s+(?P<sesStartTime>.*)\r',
                    '\s*Absolute\s+timeout\s*:\s+(?P<absTimeout>\w+)',
                    '\s*Idle\s+timeout\s*:\s+(?P<idleTimeout>\w+)',
                    '\s*Volume\s+event\s*:\s+(?P<volEvent>\w+)',
                    '\s*Time\s+event\s*:\s+(?P<timeEvent>\w+)',
                    '\s*Ip\s+acl\s+in\s*:\s+(?P<inAclName>\w+)',
                    '\s*Ip\s+acl\s+out\s*:\s+(?P<outAclName>\w+)',
                    '\s*Qos\s+policy\s*:\s+(?P<qospolicy>\w+)']

       #=====================================  Get The MDO Session details
       #Commands "show mdo session detail handle <handle>" and "show session detail handle <handle>"
       #are having the different counter fields.[For Ex : Session Start Time,Ip Acl In/Out ........]              
       actCou = {}
       for sesHand in sesHandList:
           #Get Session Deatils from the output of command "show mdo session detail handle <handle>"
           out = self.cmd("show mdo session detail handle %s"%sesHand)
           if "ERROR" in out :
              fail = 1
              errorList.append("MDO session with Handle %s not found"%sesHand)

           for regex in regex_list:
                obj=re.compile(regex,re.I)
                m=obj.search(out)
                if m:
                   dict=m.groupdict()
                   for key in dict.keys():
                       modiKey = '%s_%s'%(sesHand,key)
                       actCou[modiKey]=dict[key]

           #Get Session Deatils from the output of command "show session detail handle <handle>"
           out = self.cmd("show session detail handle %s"%sesHand)
           for regex in regex_list2:
                obj=re.compile(regex,re.I)
                m=obj.search(out)
                if m:
                   dict=m.groupdict()
                   for key in dict.keys():
                       modiKey = '%s_%s'%(sesHand,key)
                       actCou[modiKey]=dict[key]
       
           #======================================   Get Session Counters
           out = self.cmd("show session counters | grep %s"%sesHand)
           for index in range(0,len(sesHandList)):
               actCou['%s_rcvPkts'%sesHandList[index]] = out.split()[2]
               actCou['%s_txPkts'%sesHandList[index]] = out.split()[3]
               actCou['%s_rcvBytes'%sesHandList[index]] = out.split()[4]
               actCou['%s_txBytes'%sesHandList[index]] = out.split()[5]
       return actCou

def vrf_mdo_ses_cou_incr(self,context="local") :

       """
       Description : API used to verify whether the session counters are incremnted or not.

       Arguments   : context : Name of the context

       Example     : vrf_mdo_ses_cou_incr(self.ssx,context="mdo1")

       ReturnValue : returns the error List incase of Fail or Pass  
       """

       #For Displaying errors at the end
       errorList = []

       #For Session handle list
       sesHandList = []

       #============================== Get the Session Handle List
       self.cmd("context %s"%context)
       self.cmd("term len infi")
       self.cmd("term wid infi")
       out = self.cmd("show mdo session | grep \"Session Handle\"")
       if "ERROR" in out :
          errorList.append("output is not available for session handle %s"%sesHand)
       sesHandles = out.split("\n")
       len1 = len(sesHandles)
       for sesHand in sesHandles:
           if sesHand == "\r" or len(sesHand) == 0 :
              continue
           sesHand = sesHand.split(":")[1]
           if "\r" in sesHand :
              sesHand = sesHand.split("\r")[0].strip()
           else :
              sesHand = sesHand.strip()
           sesHandList.append(sesHand)
           out = self.cmd("show session counters | grep %s"%sesHand)
       for sesHand in sesHandList :    
           #======================================   Get Session Counters related to handle
           out = self.cmd("show session counters | grep %s"%sesHand)
           if "ERROR" in out :
               errorList.append("output is not available for session handle %s"%sesHand)
           for index in range(0,len(sesHandList)):
               actCou['%s_rcvPkts'%sesHandList[index]] = out.split()[2]
               if int(actCou['%s_rcvPkts'%sesHandList[index]]) != 0 :
                  errorList.append("For Session Handle %s : Received Packets are not incremented"%sesHandList[index])
               actCou['%s_txPkts'%sesHandList[index]] = out.split()[3]
               if int(actCou['%s_txPkts'%sesHandList[index]]) != 0 :
                  errorList.append("For Session Handle %s : Transmit Packets are not incremented"%sesHandList[index])

       return errorList       
       
