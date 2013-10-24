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
DESCRIPTION             : APIs for MDO Counters
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

def get_ctxt_app_coun(self,context="local") :

       """
       Description : API used to get the context based application related counter values of corresponding counter fields.

       Arguments   : context : Name of the context

       Example     : get_ctxt_app_coun(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.
       countNameDic = {"IMSI   Request  Generated":"ImsiReqGen",\
                    "IMSI   Response Consumed":"ImsiRespCon", \
                   "IMEI   Request  Generated" : "ImeiReqGen",\
                   "IMEI   Response Consumed":"ImeiRespCon", \
                   "Auth and Ciph Req Modified" :"AuthCiphReqMod",\
                   "Act Sec PDP Ctxt Req Consumed" : "PdpCtxtReqCons",\
                   "Act Sec PDP Ctxt Reject Generated" : "ActSecPdpCtxtRejGen",\
                   "Req Sec PDP Ctxt Act Consumed": "ReqPdpCtxtActCons", \
                   "Req Sec PDP Ctxt Act Reject Generated": "ReqSecPdpCtxtActRejGen",\
                   "Deact Req towards MS Generated" : "DeactReqMsGen",\
                   "Deact Req towards SGSN Generated":"DeactReqSgsnGen", \
                   "Deact Accept from SGSN Consumed" : "DeactAccSgsnCons",\
                   "Deact Accept from MS Consumed"   : "DeactAccMsCons",\
                   "RAB Assignment Request Modified" : "RabAsiReqModi",\
                   "RAB Assignment Request Pass thru" : "RabAsiReqPas",\
                   "RAB Assignment Response Pass thru" : "RabAsiResPas",\
                   "RABs Modified" : "RabsModi",\
                   "RABs Pass thru" : "RabsPass",\
                   "RABs Released" : "RabsRel",\
                   "Active Sess Del (Re-activate)" : "ActSesDelReAct",\
                   "Active Sess Del (Re-attach)"   : "ActSesDelReAtta",\
                   "Idle Sess Del (Re-attach)"     : "IdleSesDelReAtta",\
                   "Current Sess rate"             : "CurSesRate",\
                   "Average Sess rate"             : "AvgSesRate"}

       actual = {}
       errList = []
       couValList = []

       # Get the Counter value corresponding to Counter name in dictionary .
       for key in countNameDic :
          out = self.cmd("show mdo counter det app context %s | grep \"%s\""%(context,key))
          # Sum up the counter values related to same counter name in all Slots
          output = out.split("\n")          
          for out in output:
              if "ERROR" in out :
                 errList.append("Error occured while executing \"show mdo counter det app context\" with option %s"%key)
                 continue
              if re.search("\s*%s\s+:\s+\d+"%key,out) :
                 couVal = re.search("\s*%s\s+:\s+\d+"%key,out)
                 countVal =  couVal.group(0)
                 count = re.search("\d+","%s"%countVal).group(0)
                 couValList.append(count)
          count = 0
          for val in couValList:
              count  = count + int(val)
          count = str(count)
          if len(count) >= 10 :
             count = int(count[:-1])

          actual[countNameDic[key]] = count 

       if len(errList) :
          log.info("\n\n\n######################################")
          for err in errList :
              log.error("%s"%err)
          log.info("######################################\n\n\n")
          return 0
       else :
          return actual

def get_ctxt_sccp_coun(self,context="local") :

       """
       Description : API used to get the context based sccp related counter values of corresponding counter fields.

       Arguments   : context : Name of the context

       Example     : get_ctxt_sccp_coun(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.
       countNameDic = {"Packets                Sent" : "PktSnt",\
                    "Packets                Received":"PktRcvd", \
                   " Connection Request     Sent" : "ConReqSnt",\
                   "Connection Request     Received":"ConReqRcvd", \
                   "Connection Confirm     Sent" :"ConConfSnt",\
                   "Connection Confirm     Received" : "ConConfRcvd",\
                   "Connection Refused     Sent" : "ConRefSnt",\
                   "Connection Refused     Received": "ConRefRcvd", \
                   "Release                Sent": "RelSnt",\
                   "Release                Received" : "RelRcvd",\
                   "Data Form 1            Sent":"DeactReqSgsnGen", \
                   "Data Form 1            Received" : "DeactAccSgsnCons",\
                   "Data Form 2            Sent":"DeactReqSgsnGen", \
                   "Data Form 2            Received" : "DeactAccSgsnCons",\
                   "Data ACK               Sent"     : "DataAckSnt",\
                   "Data ACK               Received" : "DataAckRcvd",\
                   "Unidata                Sent"     : "UniDataSnt",\
                   "Unidata                Received" : "UniDataRcvd",\
                   "Unidata  Service       Sent" : "UniDataSer",\
                   "Unidata  Service       Received" : "UniDataRcvd",\
                   "Expedited Data         Sent" : "ExpDataSnt",\
                   "Expedited Data         Received" : "ExpDataRcvd",\
                   "Expedited Data  ACK    Sent" : "ExpDataAckSnt",\
                   "Expedited Data  ACK    Received" : "ExpDataAckRcvd",\
                   "Reset Req              Sent"     : "ResetReqSnt",\
                   "Reset Req              Received" : "ResettReqRcvd",\
                   "Reset Confirm          Sent"     : "ResetConfSnt",\
                   "Reset Confirm          Received" : "ResetConfRcvd",\
                   "PDU Error              Sent"     : "PduErrSnt",\
                   "PDU Error              Received" : "PduErrRcvd",\
                   "Inactivity Test        Sent"     : "InactTstSnt",\
                   "Inactivity Test        Received" : "InactTstRcvd",\
                   "Extended Unidata       Sent"     : "ExtUniDataSnt",\
                   "Extended Unidata       Received" : "ExtUniDataRcvd",\
                   "Extended Unidata Serv  Sent"     : "ExtUniDataSerSnt",\
                   "Extended Unidata Serv  Received" : "ExtUniDataSerRcvd" }

       actual = {}
       errList = []
       couValList = []

       # Get the Counter value corresponding to Counter name in dictionary .
       for key in countNameDic :
          out = self.cmd("show mdo counter det sccp context %s | grep \"%s\""%(context,key))
          # Sum up the counter values related to same counter name in all Slots
          output = out.split("\n")
          for out in output:
              if "ERROR" in out :
                 errList.append("Error occured while executing \"show mdo counter det app context\" with option %s"%key)
                 continue
              if re.search("\s*%s\s+:\s+\d+"%key,out) :
                 couVal = re.search("\s*%s\s+:\s+\d+"%key,out)
                 outr =  couVal.group(0)
                 count = re.search("\d+","%s"%outr).group(0)
                 couValList.append(count)
          count = 0
          for val in couValList:
              count  = count + int(val)
          count = str(count)
          if len(count) >= 10 :
             count = int(count[:-1])
          actual[countNameDic[key]] = count

       if len(errList) :
          log.info("\n\n\n######################################")
          for err in errList :
              log.error("%s"%err)
          log.info("######################################\n\n\n")
          return 0
       else :
          return actual

def get_ctxt_sctp_coun(self,context="local") :

       """
       Description : API used to get the context based sctp related counter values of corresponding counter fields.

       Arguments   : context : Name of the context

       Example     : get_ctxt_sctp_coun(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.
       countNameDic = {"Associations           Accepted" : "AssAcptd",\
                    "Associations           Initiated":    "AssIniti", \
                   "Graceful Association   Shutdown" : "GraAssShut",\
                   "Ungraceful Association Shutdown":"UngrAssShut", \
                   "Data Chunks            Sent" :"DataChuSnt",\
                   "Data Chunks            Received" : "DataChuRcvd",\
                   "Data Bytes             Sent" : "DataBytesSnt",\
                   "Data Bytes             Received": "DataBytesRcvd", \
                   "Init                   Sent": "InitSnt",\
                   "Init                   Received" : "InitRcvd",\
                   "Init Ack               Sent":"InitAckSnt", \
                   "Init Ack               Received" : "InitAckRcvd",\
                   "Cookie Echo            Sent" :     "CookEchSnt",\
                   "Cookie Echo            Received":"CookEchRcvd", \
                   "Cookie ACK             Sent" : "CookAckSnt",\
                   "Cookie ACK             Received"     : "CookAckRcvd",\
                   "Heartbeat              Sent" : "HeaBeatSnt",\
                   "Heartbeat              Received"     : "HeaBeatRcvd",\
                   "Heartbeat Ack          Sent" : "HeaBeatAckSnt",\
                   "Heartbeat Ack          Received" : "HeaBeatAckRcvd",\
                   "SACK                   Sent" : "SackSnt",\
                   "SACK                   Received" : "SackRcvd",\
                   "Abort                  Sent" : "AbortSnt",\
                   "Abort                  Received" : "AbortRcvd",\
                   "Shutdown               Sent" : "ShutSnt",\
                   "Shutdown               Received"     : "ShutRcvd",\
                   "Shutdown Ack           Sent" : "ShutAckSnt",\
                   "Shutdown Ack           Received"     : "ShutAckRcvd",\
                   "Shutdown Complete      Sent" : "ShutComplSnt",\
                   "Shutdown Complete      Received"     : "ShutComplRcvd",\
                   "Packets                Sent" : "PktsSnt",\
                   "Packets                Received"     : "PktsRcvd",\
                   "Packets                Untouched" : "PktsUntouc",\
                   "Transmit               Skipped"     : "PktsSkip"}

       actual = {}
       errList = []
       couValList = []

       # Get the Counter value corresponding to Counter name in dictionary .
       for key in countNameDic :
          out = self.cmd("show mdo counter det sctp context %s | grep \"%s\""%(context,key))
          # Sum up the counter values related to same counter name in all Slots
          output = out.split("\n")
          for out in output:
              if "ERROR" in out :
                 errList.append("Error occured while executing \"show mdo counter det app context\" with option %s"%key)
                 continue
              if re.search("\s*%s\s+:\s+\d+"%key,out) :
                 couVal = re.search("\s*%s\s+:\s+\d+"%key,out)
                 outr =  couVal.group(0)
                 count = re.search("\d+","%s"%outr).group(0)
                 couValList.append(count)
          count = 0
          for val in couValList:
              count  = count + int(val)
          count = str(count)
          if len(count) >= 10 :
             count = int(count[:-1])
          actual[countNameDic[key]] = count

       if len(errList) :
          log.info("\n\n\n######################################")
          for err in errList :
              log.error("%s"%err)
          log.info("######################################\n\n\n")
          return 0
       else :
          return actual

def get_ctxt_sm_coun(self,context="local") :
       """
       Description : API used to get the context based session management related counter values of corresponding counter fields.

       Arguments   : context : Name of the context

       Example     : get_ctxt_sm_coun(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.
       countNameDic = {"Activate PDP Context Request" : "ActPdpCtxtReq",\
                    "Activate PDP Context Accept":    "ActPdpCtxtAcpt", \
                   "Activate PDP Context Reject" : "ActPdpCtxtRej",\
                   "De-Activate PDP Context Request from SGSN":"DeactPdpCtxtReqSgsn", \
                   "De-Activate PDP Context Request from UE" :"DeactPdpCtxtReqUe",\
                   "De-Activate PDP Context Accept  from SGSN" : "DeactPdpCtxtAcptSgsn",\
                   "De-Activate PDP Context Accept  from UE" : "DeactPdpCtxtAcptUe",\
                   "Modify PDP Context Request from SGSN" : "ModPdpCtxtReqSgsn",\
                   "Modify PDP Context Request from UE" : "ModPdpCtxtReqUe",\
                   "Modify PDP Context Accept  from SGSN" : "ModPdpCtxtAcptSgsn",\
                   "Modify PDP Context Accept  from UE" : "ModPdpCtxtAcptUe",\
                   "Modify PDP Context Reject from SGSN" : "ModPdpCtxtRejSgsn",\
                   "Modify PDP Context Reject from UE" : "ModPdpCtxtRejUe" }

       actual = {}
       errList = []
       couValList = []

       # Get the Counter value corresponding to Counter name in dictionary .
       for key in countNameDic :
          out = self.cmd("show mdo counter det sm context %s | grep \"%s\""%(context,key))
          # Sum up the counter values related to same counter name in all Slots
          output = out.split("\n")
          for out in output:
              if "ERROR" in out :
                 errList.append("Error occured while executing \"show mdo counter det app context\" with option %s"%key)
                 continue
              if re.search("\s*%s\s+:\s+\d+"%key,out) :
                 couVal = re.search("\s*%s\s+:\s+\d+"%key,out)
                 outr =  couVal.group(0)
                 count = re.search("\d+","%s"%outr).group(0)
                 couValList.append(count)
          count = 0
          for val in couValList:
              count  = count + int(val)
          count = str(count)
          if len(count) >= 10 :
             count = int(count[:-1])
          actual[countNameDic[key]] = count

       if len(errList) :
          log.info("\n\n\n######################################")
          for err in errList :
              log.error("%s"%err)
          log.info("######################################\n\n\n")
          return 0
       else :
          return actual

def get_ctxt_ranap_coun(self,context="local") :

       """
       Description : API used to get the context based ranap related counter values of corresponding counter fields.

       Arguments   : context : Name of the context

       Example     : get_ctxt_ranap_coun(self.ssx,context="mdo1")

       ReturnValue : 0 if Fails else <conuterName CounterValue> in form of dictionary
       """

       # Dictionary holds the counter name taken from command output on SSX and
       # Value is the Counter name in short cut.
       countNameDic = {"Packets                 Sent" : "PktsSnt",\
                    "Packets                 Received": "PktsRecd", \
                   "Initial UE              Sent" : "InitUeSnt",\
                   "Initial UE              Received" : "InitUeRcvd", \
                   "Direct Transfer         Sentest" :"InitUeTransSent",\
                   "Direct Transfer         Received" : "InitUeTransRcvd",\
                   "Common ID               Sent" : "CommoIdSnt",\
                   "Common ID               Received" : "CommoIdRcvd",\
                   "RAB Assignment Request  Sent" : "RabAssiReqSnt",\
                   "RAB Assignment Request  Received" : "RabAssiReqRcvd",\
                   "RAB Assignment Response Sent" : "RabAssiRespSnt",\
                   "RAB Assignment Response Received" : "RabAssiRespRcvd",\
                   "Connection Release      Sent" : "ConRelSnt",\
                   "Connection Release      Received" : "ConRelRcvd",\
                   "Current RANAP msg recieving rate" : "CurRanapMsgRecRate",\
                   "Average RANAP msg recieving rate" : "AvgRanapMsgRecRate",\
                   "Current RANAP msg sending   rate" : "CurRanapMsgSendRate",\
                   "Average RANAP msg sending   rate" : "AvgRanapMsgSendRate"}


       actual = {}
       errList = []
       couValList = []

       # Get the Counter value corresponding to Counter name in dictionary .
       for key in countNameDic :
          out = self.cmd("show mdo counter det ranap context %s | grep \"%s\""%(context,key))
          # Sum up the counter values related to same counter name in all Slots
          output = out.split("\n")
          for out in output:
              if "ERROR" in out :
                 errList.append("Error occured while executing \"show mdo counter det app context\" with option %s"%key)
                 continue
              if re.search("\s*%s\s+:\s+\d+"%key,out) :
                 couVal = re.search("\s*%s\s+:\s+\d+"%key,out)
                 outr =  couVal.group(0)
                 count = re.search("\d+","%s"%outr).group(0)
                 couValList.append(count)
          count = 0
          for val in couValList:
              count  = count + int(val)
          count = str(count)
          if len(count) >= 10 :
             count = int(count[:-1])
          actual[countNameDic[key]] = count

       if len(errList) :
          log.info("\n\n\n######################################")
          for err in errList :
              log.error("%s"%err)
          log.info("######################################\n\n\n")
          return 0
       else :
          return actual

