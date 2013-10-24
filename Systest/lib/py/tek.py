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

from pdb import set_trace as st
import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import  time, misc, re
from pexpect import *
from Host import Host
from logging import getLogger
log = getLogger()

tek_prompt_regex = "[\r\n]*K1297:RCP>"

class TEK(Host):
    def __init__(self, host,username= "", password= "",stdprompt=tek_prompt_regex):
        """tek specific init method.  Basically just filling in the blanks."""

        Host.__init__(self, host, username, password, stdprompt)
        log.output("G-35 object for host %s created." % host)
        #self.cmd("")


    def cmd(self, command, timeout = 60):
        """Routine to send a command to a tek
        Returns output of command as a string."""
        retstr = ""
        try:
            self.ses.delaybeforesend = 0.5
            self.ses.sendline(command)
            self.ses.expect(tek_prompt_regex, timeout)
            #log.info("before %s; after %s" %(self.ses.before, self.ses.after))
            retstr += self.ses.before
        except TIMEOUT:
            misc.TestError("Timeout in tek.cmd for command %s\n" % command)
        #time.sleep(3)
        log.output(" G35: %s" %retstr)
        return retstr.strip().split('\n')[-1]

    def set_subscriber_position(self,emulation="umtsgm1U1:usim",user_id="1",position="0"):
        """Routine to configure the required subscriber to required position of a particular
           emulation"""


        if int(user_id) in range(0,11):
            show = self.cmd("set %s  'Users.U1_10.User[%s].Reset_Subscriber' Reset_Subscriber" %(emulation,user_id))
            show = self.cmd("set %s  'Users.U1_10.User[%s].Position' %s" %(emulation,user_id,position))
            show = self.cmd("set %s  'Users.U1_10.User[%s].Set_Position' Set_Position" %(emulation,user_id))
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(10,31):
            show = self.cmd("set %s  'Users.U11_30.User[%s].Reset_Subscriber' Reset_Subscriber" %(emulation,user_id))
            show = self.cmd("set %s  'Users.U11_30.User[%s].Position' %s" %(emulation,user_id,position))
            show = self.cmd("set %s  'Users.U11_30.User[%s].Set_Position' Set_Position" %(emulation,user_id))
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(30,61):
            show = self.cmd("set %s  'Users.U31_60.User[%s].Reset_Subscriber' Reset_Subscriber" %(emulation,user_id))
            show = self.cmd("set %s  'Users.U31_60.User[%s].Position' %s" %(emulation,user_id,position))
            show = self.cmd("set %s  'Users.U31_60.User[%s].Set_Position' Set_Position" %(emulation,user_id))
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(60,101):
            show = self.cmd("set %s  'Users.U61_100.User[%s].Reset_Subscriber' Reset_Subscriber" %(emulation,user_id))
            show = self.cmd("set %s  'Users.U61_100.User[%s].Position' %s" %(emulation,user_id,position))
            show = self.cmd("set %s  'Users.U61_100.User[%s].Set_Position' Set_Position" %(emulation,user_id))
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(100,241):
            show = self.cmd("set %s  'Users.U100_240.User[%s].Reset_Subscriber' Reset_Subscriber" %(emulation,user_id))
            show = self.cmd("set %s  'Users.U100_240.User[%s].Position' %s" %(emulation,user_id,position))
            show = self.cmd("set %s  'ers.U100_240.User[%s].Set_Position' Set_Position" %(emulation,user_id))
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
            show = self.cmd("set %s 'Users.U100_240.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        
       
    def set_apn(self,emulation="umtsgm1U1",user_id="1",apn="internet.com"):
        """Routine to configure the required APN to required user"""

        flag = 1
        self.cmd("set %s 'IE Pool.APNS[0].APN' %s" %(emulation,apn))
        show = self.cmd("show %s 'IE Pool.APNS[0].APN'" %(emulation))
        if (show.split(":")[1].lstrip()!= apn):
                log.output("APN is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("APN is set to %s"%show.split(":")[1].lstrip())

        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].IE APN' 0" %(emulation,user_id))
        show = self.cmd("show %s  'Subscribers.Subscriber[%s].PDPC[0].IE APN'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= '0'):
                log.output("IE Pool is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE Pool is set to %s"%show.split(":")[1].lstrip())    
        
        if flag:
            return "true"
        else:
            return "false"

    def set_pool_apn(self,emulation="umtsgm1U1",apn_id="1",apn="internet.com"):
        """Routine to configure the required APN to required pool"""

        flag = 1
        self.cmd("set %s 'IE Pool.APNS[%s].APN' %s" %(emulation,apn_id,apn))
        show = self.cmd("show %s 'IE Pool.APNS[%s].APN'" %(emulation,apn_id))
        if (show.split(":")[1].lstrip()!= apn):
                log.output("Error : APN is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("APN is set to %s"%show.split(":")[1].lstrip())

        
    def set_apn_id(self,emulation="umtsgm1U1",apn_id="1",user_id="1"):
        """Routine to configure the required APN to required subscriber index"""

        flag = 1
        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].IE APN' %s" %(emulation,user_id,apn_id))
        show = self.cmd("show %s  'Subscribers.Subscriber[%s].PDPC[0].IE APN'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= apn_id):
                log.output("Error: IE Pool is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE Pool is set to %s"%show.split(":")[1].lstrip())    
        
        if flag:
            return "true"
        else:
            return "false"


    def set_rnc_pdpc_address(self,emulation="umtsgm1U1",user_id="1",ipAddress="192.168.14.12"):
        """Routine to configure the required APN to required subscriber index"""

        flag = 1
        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].Requested PDP address' %s" %(emulation,user_id,ipAddress))
        show = self.cmd("show %s  'Subscribers.Subscriber[%s].PDPC[0].Requested PDP address'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= ipAddress):
                log.output("Error: IE address is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE address is set to %s"%show.split(":")[1].lstrip())    
        
        if flag:
            return "true"
        else:
            return "false"


    def set_sgsn_pdpc_address(self,emulation="umtsgm1U1",user_id="1",ipAddress="192.168.14.12"):
        """Routine to configure the required APN to required subscriber index"""

        flag = 1
        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].PDP address' %s" %(emulation,user_id,ipAddress))
        show = self.cmd("show %s  'Subscribers.Subscriber[%s].PDPC[0].PDP address'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= ipAddress):
                log.output("Error: IE address is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE address is set to %s"%show.split(":")[1].lstrip())    
        
        if flag:
            return "true"
        else:
            return "false"


    def set_profile_rnc_pdpc_address(self,emulation="umtsgm1U1",profileId="1",ipAddress="192.168.14.12"):
        """Routine to configure the required APN to required subscriber index"""

        flag = 1
        self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].Requested PDP address' %s" %(emulation,profileId,ipAddress))
        show = self.cmd("show %s  'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].Requested PDP address'"  %(emulation,profileId))
        if (show.split(":")[1].lstrip()!= ipAddress):
                log.output("Error: IE address is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE address is set to %s"%show.split(":")[1].lstrip())

        if flag:
            return "true"
        else:
            return "false"


    def set_profile_sgsn_pdpc_address(self,emulation="umtsgm1U1",profileId="1",ipAddress="192.168.14.12"):
        """Routine to configure the required APN to required subscriber index"""

        flag = 1
        self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].PDP address' %s" %(emulation,profileId,ipAddress))
        show = self.cmd("show %s  'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].PDP address'"  %(emulation,profileId))
        if (show.split(":")[1].lstrip()!= ipAddress):
                log.output("Error: IE address is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE address is set to %s"%show.split(":")[1].lstrip())

        if flag:
            return "true"
        else:
            return "false"

    def set_pdp_address(self,emulation="umtsgm1U1",user_id="1",adress="192.168.14.210"):
        """Routine to configure the required APN to required user"""

        flag = 1
        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].PDP address' %s" %(emulation,user_id,adress))
        show = self.cmd("show %s  'Subscribers.Subscriber[%s].PDPC[0].PDP address'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= adress):
                log.output("PDP Address is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("PDP Address is set to %s"%show.split(":")[1].lstrip())

        if flag:
            return "true"
        else:
            return "false"


  
    def set_user_imei(self,emulation="umtsgm1U1:usim",user_id="1",imei="123456789"):
        """Routine to configure the required IMEI to required user"""

        show = self.cmd("set %s 'Subscribers.Subscriber[%s].Numbers.IMEI' %s" %(emulation,user_id,imei))
        show = self.cmd("show %s 'Subscribers.Subscriber[%s].Numbers.IMEI'" %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= imei):
               log.output("IMEI is not set Correctly, the current value is %s but set to imei %s" %(show.split(":")[1].lstrip(),imei))
               return "false"
        else:
               log.output("IMEI is set to %s"%(show.split(":")[1].lstrip()))
               return "true"

    def set_user_imsi(self,emulation="umtsgm1U1:usim",user_id="1",imsi="123456789"):
        """Routine to configure the required IMEI to required user"""

        self.cmd("set %s 'Subscribers.Subscriber[%s].Numbers.IMSI' %s" %(emulation,user_id,imsi))
        show = self.cmd("show %s 'Subscribers.Subscriber[%s].Numbers.IMSI'" %(emulation,user_id))
        if (show.split(":")[1].lstrip()!= imsi):
               log.output("IMSI is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
               return "false"
        else:
               log.output("IMSI is set to %s"%(show.split(":")[1].lstrip()))
               return "true"



    def set_profile_imei(self,emulation="umtsgm1U1:usim",profile_id="1",imei="123456789"):
        """Routine to configure the required IMEI to required profile"""

        show = self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].Numbers.First IMEI' %s" %(emulation,profile_id,imei))
        show = self.cmd("show %s 'Subscriber Profiles.Subscriber Profile[%s].Numbers.First IMEI'" %(emulation,profile_id))
        if (show.split(":")[1].lstrip()!= imei):
               log.output("IMEI is not set Correctly, the current value is %s but set to imei %s" %(show.split(":")[1].lstrip(),imei))
               return "false"
        else:
               log.output("IMEI is set to %s"%(show.split(":")[1].lstrip()))
               return "true"


    def set_profile_imsi(self,emulation="umtsgm1U1:usim",profile_id="1",imsi="123456789"):
        """Routine to configure the required IMSI to required profile"""

        show = self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].Numbers.First IMSI' %s" %(emulation,profile_id,imsi))
        show = self.cmd("show %s 'Subscriber Profiles.Subscriber Profile[%s].Numbers.First IMSI'" %(emulation,profile_id))
        if (show.split(":")[1].lstrip()!= imsi):
               log.output("IMSI is not set Correctly, the current value is %s but set to imsi %s" %(show.split(":")[1].lstrip(),imsi))
               return "false"
        else:
               log.output("IMSI is set to %s"%(show.split(":")[1].lstrip()))
               return "true"


    def set_profile_apn_id(self,emulation="umtsgm1U1",apn_id="1",profile_id="1"):
        """Routine to configure the required APN to required subscriber index"""


        flag = 1
        self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].IE APN' %s " %(emulation,profile_id,apn_id))
        show = self.cmd("show %s  'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].IE APN' "  %(emulation,profile_id))
        if (show.split(":")[1].lstrip()!= apn_id):
                log.output("Error: IE Pool is not set Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("IE Pool is set to %s"%show.split(":")[1].lstrip())

        if flag:
            return "true"
        else:
            return "false"


    def set_start_end_index_profile(self,emulation="umtsgm1U1",profile_id="0",start="31",end="31"):
        """Routine to configure start and end index for subscriber  profiles"""

        flag = 1
        self.cmd("set %s 'Actions.Start index subscriber profile %s' %s " %(emulation,profile_id,start))
        show = self.cmd("show %s 'Actions.Start index subscriber profile %s' " %(emulation,profile_id))
        if (show.split(":")[1].lstrip()!= start):
                log.output("Error: Start index for profile is not set  Correctly, current Value is %s " %show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("Start index for profile is set to %s"%show.split(":")[1].lstrip())

        self.cmd("set %s 'Actions.End index subscriber profile %s' %s" %(emulation,profile_id,end))
        show = self.cmd("show %s 'Actions.End index subscriber profile %s'" %(emulation,profile_id))
        if (show.split(":")[1].lstrip()!= end):
                log.output("Error: End index for profile is not set  Correctly, current Value is %s"%show.split(":")[1].lstrip())
                flag = 0
        else:
                log.output("End index for profile is set to %s"%show.split(":")[1].lstrip())

        self.cmd("set %s 'Actions.Apply Subscriber Profile %s' Execute " %(emulation,profile_id))

        if flag:
            return "true"
        else:
            return "false"
        

    def set_user_qos_rnc(self,emulation="umtsgm1U1:usim",user_id="1",qos="09121f2000808000050000"):
        """Routine to configure the required IMEI to required user"""

        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].Requested QoS hex value' %s" %(emulation,user_id,qos))
        show = self.cmd("show %s 'Subscribers.Subscriber[%s].PDPC[0].Requested QoS hex value'" %(emulation,user_id))
        if (show.split(":")[1].lstrip().rstrip('f') != qos):
               log.output("Qos is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
               return "false"
        else:
               log.output("IMSI is set to %s"%(show.split(":")[1].lstrip()))
               return "true"

    def set_user_qos_sgsn(self,emulation="umtsgm1U1:usim",user_id="1",qos="09121f2000808000050000"):
        """Routine to configure the required IMEI to required user"""

        self.cmd("set %s 'Subscribers.Subscriber[%s].PDPC[0].QoS hex value' %s" %(emulation,user_id,qos))
        show = self.cmd("show %s 'Subscribers.Subscriber[%s].PDPC[0].QoS hex value'" %(emulation,user_id))
        if (show.split(":")[1].lstrip().rstrip('f') != qos):
               log.output("Qos is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
               return "false"
        else:
               log.output("Qos is set to %s"%(show.split(":")[1].lstrip()))
               return "true"



    def set_profile_qos_rnc(self,emulation="umtsgm1U1:usim",profile_id="1",qos="09121f2000808000050000"):
        """Routine to configure the required IMEI to required user"""

        self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].Requested QoS hex value' %s" %(emulation,profile_id,qos))
        show = self.cmd("show %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].Requested QoS hex value'" %(emulation,profile_id))
        if (show.split(":")[1].lstrip().rstrip('f') != qos):
               log.output("Qos is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
               return "false"
        else:
               log.output("Qos is set to %s"%(show.split(":")[1].lstrip()))
               return "true"

    def set_profile_qos_sgsn(self,emulation="umtsgm1U1:usim",profile_id="1",qos="09121f2000808000050000"):
        """Routine to configure the required IMEI to required user"""

        self.cmd("set %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].QoS hex value' %s" %(emulation,profile_id,qos))
        show = self.cmd("show %s 'Subscriber Profiles.Subscriber Profile[%s].PDPC[0].QoS hex value'" %(emulation,profile_id))
        if (show.split(":")[1].lstrip().rstrip('f') != qos):
               log.output("Qos is not set Correctly, the current value is %s"%show.split(":")[1].lstrip())
               return "false"
        else:
               log.output("Qos is set to %s"%(show.split(":")[1].lstrip()))
               return "true"


    def set_pktgen_DatParam(self,emulation="U1-RNC-PKTGEN",connectionId = "1",activeTuunelId = "1"):
        """Routine to set datapara1 and datapara2 for emulation PKTGEN"""
        self.cmd("set %s 'Contexts.Connection[%s].Generator.DatPara1' %s" %(emulation,connectionId,activeTuunelId))
        self.cmd("set %s 'Contexts.Connection[%s].Generator.DatPara2' 5" %(emulation,connectionId))
        show = self.cmd("show %s 'Contexts.Connection[%s].Generator.DatPara1'" %(emulation,connectionId))
        if (show.split(":")[1].lstrip() != activeTuunelId):
            log.output("Error: datapara1 and datapara2 for emulation PKTGEN not set properly")
            return "false"
        else:
            log.output("datapara1 and datapara2 for emulation PKTGEN")
            return "true"
    
    def set_pktgen_trafficParam(self,emulation="U1-RNC-PKTGEN",connectionId = "1",PktFillMode = "ICMP-ECHO",PktPeriod = "1000",PktPerPeriod = "1000",PktNum = "1000"):
        """Routine to set datapara1 and datapara2 for emulation PKTGEN"""
        self.cmd("set %s 'Contexts.Connection[%s].General.PktFillMode' %s" %(emulation,connectionId,PktFillMode))
        self.cmd("set %s 'Contexts.Connection[%s].General.PktPeriod' %s" %(emulation,connectionId,PktPeriod))
        self.cmd("set %s 'Contexts.Connection[%s].General.PktPerPeriod' %s" %(emulation,connectionId,PktPerPeriod))
        self.cmd("set %s 'Contexts.Connection[%s].General.PktNum' %s" %(emulation,connectionId,PktNum))
        return "true"
           
    def start_pktgen_traffic(self,emulation="U1-RNC-PKTGEN",connectionId = "1"):
        """Routine to start traffic using PKTGEN"""
        self.cmd("set %s 'Contexts.Connection[%s].Actions.Action' Start" %(emulation,connectionId) )
        return "true"
      
    def stop_pktgen_traffic(self,emulation="U1-RNC-PKTGEN",connectionId = "1"):
        """Routine to stop traffic using PKTGEN"""
        self.cmd("set %s 'Contexts.Connection[%s].Actions.Action' Stop" %(emulation,connectionId) )
        return "true"

    def set_ueIp_internetIp_pktgen(self,emulation="U1-RNC-PKTGEN",connectionId = "0",userIp = "127.1.1.1",internetIp = "127.1.1.1"):
        """Routine to set UE ip and Internet Ip in PKTGEN emulation"""
        self.cmd("set %s 'Contexts.Connection[%s].IP.DestAddr' %s" %(emulation,connectionId,internetIp))
        self.cmd("set %s 'Contexts.Connection[%s].IP.SourceAddr' %s" %(emulation,connectionId,userIp))
        return "true"
    
    def initiate_attach(self,emulation="umtsgm1U1:usim",user_id="1"):
        """Routine to initiate attach for a particular subscriber"""

        if int(user_id) in range(0,11):
            show = self.cmd("set %s 'Users.U1_10.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(10,31):
            show = self.cmd("set %s 'Users.U11_30.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(30,61):
            show = self.cmd("set %s 'Users.U31_60.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(60,101):
            show = self.cmd("set %s 'Users.U61_100.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(100,241):
            show = self.cmd("set %s 'Users.U100_240.User[%s].Attach' Attach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        
        if (show.split(":")[1].lstrip()== 'Attach successful'):
                log.output("Attach Successful")
                print "attach successful"
                return "true" 
        else:
                return "false"
                
       
    def initiate_pdp_deactivate(self,emulation="umtsgm1U1:usim",user_id="1"):
        """Routine to initiate deactivate for a particular subscriber"""


        if int(user_id) in range(0,11):
            show = self.cmd("set %s 'Users.U1_10.User[%s].PDPC_Deactivate' PDPC_Deactivate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(10,31):
            show = self.cmd("set %s 'Users.U11_30.User[%s].PDPC_Deactivate' PDPC_Deactivate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(30,61):
            show = self.cmd("set %s 'Users.U31_60.User[%s].PDPC_Deactivate' PDPC_Deactivate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(60,101):
            show = self.cmd("set %s 'Users.U61_100.User[%s].PDPC_Deactivate' PDPC_Deactivate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(100,241):
            show = self.cmd("set %s 'Users.U100_240.User[%s].PDPC_Deactivate' PDPC_Deactivate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        if ('deactivation successful' not in show):
            log.output("PDP Deactivation Failed")
            return "false"
        else:
            log.output("PDP Deactivation Successful")
            log.output(show)
            return "true"


    def initiate_pdp_activate(self,emulation="umtsgm1U1:usim",user_id="1"):
        """Routine to initiate PDP Activation for a particular subscriber"""

        if int(user_id) in range(0,11):
            show = self.cmd("set %s 'Users.U1_10.User[%s].PDPC_Activate' PDPC_Activate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(10,31):
            show = self.cmd("set %s 'Users.U11_30.User[%s].PDPC_Activate' PDPC_Activate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(30,61):
            show = self.cmd("set %s 'Users.U31_60.User[%s].PDPC_Activate' PDPC_Activate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(60,101):
            show = self.cmd("set %s 'Users.U61_100.User[%s].PDPC_Activate' PDPC_Activate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(100,241):
            show = self.cmd("set %s 'Users.U100_240.User[%s].PDPC_Activate' PDPC_Activate" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))

        show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        if ('activation successful' not in show):
            log.output("PDP activation Failed")
            return "false"
        else:
            log.output("PDP activation Successful")
            log.output(show)
            return "true"

    def initiate_detach(self,emulation="umtsgm1U1:usim",user_id="1"):
        """Routine to initiate detach for a particular subscriber"""

        if int(user_id) in range(0,11):
            show = self.cmd("set %s 'Users.U1_10.User[%s].Detach' Detach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(10,31):
            show = self.cmd("set %s 'Users.U11_30.User[%s].Detach' Detach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(30,61):
            show = self.cmd("set %s 'Users.U31_60.User[%s].Detach' Detach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(60,101):
            show = self.cmd("set %s 'Users.U61_100.User[%s].Detach' Detach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        elif int(user_id) in range(100,241):
            show = self.cmd("set %s 'Users.U100_240.User[%s].Detach' Detach" %(emulation,user_id))
            time.sleep(15)
            show = self.cmd("show %s 'Users.Monitor.Display%s'"  %(emulation,user_id))
        if (show.split(":")[1].lstrip()== 'Detach successful'):
                log.output("detach successful")
                return "true" 
        else:
                return "false"

     

    def initiate_routing_area_update(self,emulation="umtsgm1U1:usim",user_id="1",change_position="1"):
        """Initiate routing area update"""

        self.cmd("set %s 'Users.U1_10.User[%s].Position' %s" %(emulation,user_id,change_position))
        self.cmd("set %s 'Users.U1_10.User[%s].Set_Position' Set_Position" %(emulation,user_id))
        self.cmd("set %s 'Users.U1_10.User[%s].RAU' RAU" %(emulation,user_id))
        time.sleep(15)
        show = self.cmd("show %s 'Users.Monitor.Display%s'" %(emulation,user_id))
        if ('RAU successful' not in show):
            log.output("Error: RAU Failed ")
            return "false"
        else:
            log.output("RAU Successful")
            return "true"

    def get_tunnel_state(self,emulationname,noofTunnels):
        "Get state of tunnels for the noOfTunnels"
        activelist = []
        for tunnelId in range(0,int(noofTunnels)):
            show = self.cmd("show %s 'Tunnels.Tunnel[%s].General.State' "  %(emulationname,tunnelId))
            if ('Active' in show):
                activelist.append('Active')
            else:
                 activelist.append('None')
        return activelist


    def set_tunnel_flow_ids(self,emulationname,tunnelId,flowId):
        "Set Flow labels for tunnels"
        status = 1
        show = self.cmd("set %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI User Plane Remote' %s"  %(emulationname,tunnelId,tunnelId))
        if "ERROR" not in show:
            log.output("Set tunnel Id for the tunnel")
        else:
            log.output("Error: Unable to  Set Flow Label for TEI User Plane Remote")
            status = 0

    
        show = self.cmd("set %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI Control Plane Remote' %s"  %(emulationname,tunnelId,tunnelId))
        if "ERROR" not in show:
            log.output("Set tunnel Id for the tunnel")
        else:
            log.output("Error: Unable to  Set Flow Label for TEI Control Plane Remote")
            status = 0


        show = self.cmd("set %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI User Plane Own' %s"  %(emulationname,tunnelId,tunnelId))
        if "ERROR" not in show:
            log.output("Set tunnel Id for the tunnel")
        else:
            log.output("Error: Unable to  Set Flow Label for TEI User Plane Own")
            status = 0


        show = self.cmd("set %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI Control Plane Own' %s"  %(emulationname,tunnelId,tunnelId))
        if "ERROR" not in show:
            log.output("Set tunnel Id for the tunnel")
        else:
            log.output("Error: Unable to  Set Flow Label for TEI Control Plane Own")
            status = 0

        if status == 0:
            return "true"
        else:
            return "false"


    def get_tunnel_flow_ids(self,emulationname,tunnelId):
        "Set Flow labels for tunnels"
        status = 1
        returnList = []          
        show = self.cmd("show %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI User Plane Remote'"  %(emulationname,tunnelId))
        returnList.append(show.split(":")[1].lstrip())
        show = self.cmd("show %s 'Tunnels.Tunnel[%s].General.Flow Label / TEI User Plane Own'"  %(emulationname,tunnelId))
        returnList.append(show.split(":")[1].lstrip())
        return returnList

    def negotiated_pdp_address(self,emulationname,ueId):
        "get the negotiated PDP address"
        show = self.cmd("show %s 'Subscribers.Subscriber[%s].PDPC[0].Negotiated PDP address'" %(emulationname,ueId))
        return show.split(":")[1].lstrip()

    def get_path_index(self,emulationname,tunnelId):
        "Get path Index for tunnnel"
        show = self.cmd("show %s 'Tunnels.Tunnel[%s].General.Path Index' "  %(emulationname,tunnelId))
        retval = show.split(":")[1].strip()
        return retval
            
      
    def set_path_index(self,emulationname,tunnelId,pathIndex):
        "Set path Index for tunnnel"
        show  = self.cmd("set %s 'Tunnels.Tunnel[%s].General.Path Index' %s"  %(emulationname,tunnelId,pathIndex))
        show1 = self.cmd("set %s 'Paths.Path[%s].Actions & Info.Stop' Stop"  %(emulationname,pathIndex))
        show2 = self.cmd("set %s 'Paths.Path[%s].Actions & Info.Start' Start"  %(emulationname,pathIndex))
        show  = self.cmd("show %s 'Tunnels.Tunnel[%s].General.Path Index'"  %(emulationname,tunnelId))
        if show.split(":")[1].lstrip() == pathIndex:
            log.output("Set path Index for tunnnel successful")
            return "true"
        else:
            log.output("Error:Set path Index for tunnnel not successful")
            return "false"

    def set_path_remote_ip(self,emulationname,pathIndex,remoteIp):
        "Set remote Ip for emulation name"
        show = self.cmd("set %s 'Paths.Path[%s].IP & UDP.Remote IP Address' %s"  %(emulationname,pathIndex,remoteIp))
        if "ERROR" not in show:
            log.output("Setting remote Ip  for path is successful")
            return "true"
        else:
            log.output("Error:Setting remote Ip for path is not successful")
            return "false"

    def set_path_connection_index(self,emulationname,pathIndex,connectionIndex):
        "Set connectionIndex for emulation name"
        show = self.cmd("set %s 'Paths.Path[%s].IP & UDP.IP Connection Index' %s"  %(emulationname,pathIndex,connectionIndex))
        if "ERROR" not in show:
            log.output("Setting connection Index  for path is successful")
            return "true"
        else:
            log.output("Error:Setting connection Index  for path is not successful")
            return "false"
    

    def set_path_local_ip(self,emulationname,pathIndex,localIp):
        "Set local Ip for emulation name"
        show = self.cmd("set %s 'Paths.Path[%s].IP & UDP.Local IP Address' %s"  %(emulationname,pathIndex,localIp))
        if "ERROR" not in show:
            log.output("Setting local Ip  for path is successful")
            return "true"
        else:
            log.output("Error:Setting local Ip for path is not successful")
            return "false"

    def set_path_port_num(self,emulationname,pathIndex,portNum):
        "Set port num for emulation name"
        status = 1
        show = self.cmd("set %s 'Paths.Path[%s].IP & UDP.Control Plane Port' %s"  %(emulationname,pathIndex,portNum))
        if "ERROR" not in show:
            log.output("Setting port Num  for path is successful")
        else:
            log.output("Error:Setting Port Num for path is not successful")
            status = 0
    
        show = self.cmd("set %s 'Paths.Path[%s].IP & UDP.User Plane Port' %s"  %(emulationname,pathIndex,portNum))
        if "ERROR" not in show:
            log.output("Setting port Num  for path is successful")
        else:
            log.output("Error:Setting Port Num for path is not successful")
            status = 0

        if status == 1:
            return "true"
        else:
            return "false"

    def set_rnc_user_entry_ip_data_parameter(self,emulationname,userIp,dataParameter,userEntry):
        "Set ip and data parameter for rnc pktgate"
        status = 1
        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].IP address' %s"  %(emulationname,userEntry,userIp))
        if "ERROR" not in show:
            log.output("Setting Ip for user Entry   is successful")
        else:
            log.output("Error:Setting Ip for user Entry is not successful")
            status = 0

        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].Data parameter 1' %s"  %(emulationname,userEntry,dataParameter))
      
        if "ERROR" not in show:
            log.output("Setting Data parameter for user Entry for path is successful")
        else:
            log.output("Error:Setting Data parameter for user Entry  is not successful")
            status = 0
        
        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].Data parameter 2' 5"  %(emulationname,userEntry))
        if "ERROR" not in show:
            log.output("Setting Data parameter for user Entry for path is successful")
        else:
            log.output("Error:Setting Data parameter for user Entry  is not successful")
            status = 0

        if status == 1:
            return "true"
        else:
            return "false"



    def set_rnc_user_entry_ip_data_parameter(self,emulationname,userIp,dataParameter,userEntry):
        "Set ip and data parameter for rnc pktgate"
        status = 1
        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].IP address' %s"  %(emulationname,userEntry,userIp))
        if "ERROR" not in show:
            log.output("Setting Ip for user Entry   is successful")
        else:
            log.output("Error:Setting Ip for user Entry is not successful")
            status = 0

        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].Data parameter 1' %s"  %(emulationname,userEntry,dataParameter))

        if "ERROR" not in show:
            log.output("Setting Data parameter for user Entry for path is successful")
        else:
            log.output("Error:Setting Data parameter for user Entry  is not successful")
            status = 0
        
        show = self.cmd("set %s 'IP User Entries.IP User Entry[%s].Data parameter 2' 5"  %(emulationname,userEntry))
        if "ERROR" not in show:
            log.output("Setting Data parameter for user Entry for path is successful")
        else:
            log.output("Error:Setting Data parameter for user Entry  is not successful")
            status = 0

        if status == 1:
            return "true"
        else:
            return "false"
        
 

    def get_rnc_user_data_parameter(self,emulationname,userEntry):
        "Set ip and data parameter for rnc pktgate"
        show = self.cmd("show %s 'Contexts.Connection[%s].Generator.DatPara1'" %(emulationname,userEntry))
        return show.split(":")[1].lstrip()
  

    def set_callgen_profile_start_terminal(self,emulationname,profileId,startIndex):
        """Set start terminal for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Start Terminal' %s"  %(emulationname,profileId,startIndex))
        if "ERROR" not in show:
            log.output("Set start terminal for profile in callgen for profile %s"  %profileId)
            return "true"
        else:
            log.output("Error:Set start terminal for profile in callgen for profile %s"  %profileId)
            return "false"
 

    def set_callgen_profile_end_terminal(self,emulationname,profileId,endIndex):
        """Set stop terminal for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].End Terminal' %s"  %(emulationname,profileId,endIndex))
        if "ERROR" not in show:
            log.output("Set end terminal for profile in callgen for profile %s"  %profileId)
            return "true"
        else:
            log.output("Error:Set end terminal for profile in callgen for profile %s"  %profileId)
            return "false"

    def set_callgen_profile_start_scenario(self,emulationname,profileId,scenario):
        """Set start terminal for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Start Scenario' '%s'"  %(emulationname,profileId,scenario))
        if "ERROR" not in show:
            log.output("Set start scenario for profile in callgen for profile %s"  %profileId)
            return "true"
        else:
            log.output("Error:Set start scenario for profile in callgen for profile %s"  %profileId)
            return "false"

    def set_callgen_profile_call_scenario(self,emulationname,profileId,scenario):
        """Set start terminal for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Call Scenario' '%s'"  %(emulationname,profileId,scenario))
        if "ERROR" not in show:
            log.output("Set call scenario for profile in callgen for profile %s"  %profileId)
            return "true"
        else:
            log.output("Error:Set call scenario for profile in callgen for profile %s"  %profileId)
            return "false"

    def set_callgen_profile_stop_scenario(self,emulationname,profileId,scenario):
        """Set stop terminal for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Stop Scenario' '%s'"  %(emulationname,profileId,scenario))
        if "ERROR" not in show:
            log.output("Set stop scenario for profile in callgen for profile %s"  %profileId)
            return "true"
        else:
            log.output("Error:Set stop scenario for profile in callgen for profile %s"  %profileId)
            return "false"


    def set_callgen_profile_start_call(self,emulationname,profileId):
        """Start call  for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Start Automatic calls' START"  %(emulationname,profileId))
        if "ERROR" not in show:
            log.output("Start call scenario for profile %s in callgen"  %profileId)
            return "true"
        else:
            log.output("Error:Start Call scenario for profile %s in callgen"  %profileId)
            return "false"


    def set_callgen_profile_stop_call(self,emulationname,profileId):
        """Stop call  for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Stop Automatic calls' STOP"  %(emulationname,profileId))
        if "ERROR" not in show:
            log.output("Stop call scenario for profile %s in callgen"  %profileId)
            return "true"
        else:
            log.output("Error:Stop Call scenario for profile %s in callgen"  %profileId)
            return "false"


    def set_callgen_profile_abort_call(self,emulationname,profileId):
        """Abort call  for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Abort Automatic calls' ABORT"  %(emulationname,profileId))
        if "ERROR" not in show:
            log.output("Abort call scenario for profile %s in callgen"  %profileId)
            return "true"
        else:
            log.output("Error:Abort Call scenario for profile %s in callgen"  %profileId)
            return "false"

    def set_callgen_profile_poffset(self,emulationname,profileId,poffset):
        """set poffset for profile in callgen"""
        show = self.cmd("set %s 'Profiles.Profile[%s].Profile Toffset' %s"  %(emulationname,profileId,poffset))
        if "ERROR" not in show:
            log.output("set poffset for  profile %s in callgen"  %profileId)
            return "true"
        else:
            log.output("Error:set poffset  for profile %s in callgen"  %profileId)
            return "false"

    def getUMTSGMOverviewCounters(self,emulation):
            """This routine returns a dictonary for all counter values present in UMTSGM Overview counters"""
            retdict = {}
            show = self.cmd("show %s 'Counters.Overview.Attach Proc Attempts'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['AttachProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.Attach Proc success'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['AttachProcsuccess'] = retval
            show = self.cmd("show %s 'Counters.Overview.Attach Proc rejected'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['AttachProcrejected'] = retval
            show = self.cmd("show %s 'Counters.Overview.Attach Proc timed out'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['AttachProctimedout'] = retval
            show = self.cmd("show %s 'Counters.Overview.Detach Proc Attempts'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DetachProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.Detach Proc success'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DetachProcsuccess'] = retval
            show = self.cmd("show %s 'Counters.Overview.Detach Proc timed out'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DetachProctimedOut'] = retval
            show = self.cmd("show %s 'Counters.Overview.RAU Proc Attempts'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['RAUProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.RAU Proc success'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['RAUProcsuccess'] = retval
            show = self.cmd("show %s 'Counters.Overview.RAU rejected'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['RAUProcrejected'] = retval
            show = self.cmd("show %s 'Counters.Overview.RAU Proc timed out'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['RAUProctimedout'] = retval
            show = self.cmd("show %s 'Counters.Overview.Activation Proc Attempts'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['ActivationProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.Activation Proc success'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['ActivationProcsuccess'] = retval
            show = self.cmd("show %s 'Counters.Overview.Activation Proc rejected'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['ActivationProcreject'] = retval
            show = self.cmd("show %s 'Counters.Overview.Activation Proc timed out'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['ActivationProctimedout'] = retval
            show = self.cmd("show %s 'Counters.Overview.Deactivation Proc Attempts'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DeactivationProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.Deactivation Proc success'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DeactivationProcAttempts'] = retval
            show = self.cmd("show %s 'Counters.Overview.Deactivation Proc timed out'"  %(emulation))
            retval = show.split(":")[1].strip()
            retdict['DeactivationProcAttempts'] = retval
            return retdict
