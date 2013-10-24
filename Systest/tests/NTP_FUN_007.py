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

DESCRIPTION:
configure the SSX with PST time zone; Set the time on SSX to enable the DST to 1 hour ; Verify that DST is 
applied on the SSX and time moves forward by an hour; Disable DST and 
verify that the current time moves back by an hour.
TEST_PLAN : NTP Sanity Test plans
TEST CASES: NTP_FUN_007

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24   ---------->    TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_007.py
AUTHOR:  rajshekar@primesoftsolutionsinc.com
REVIEWER:alok@primesoftsolutionsinc.com

"""

import sys, os

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
from helpers import is_healthy,diff_in_time_ssx
from misc import *

#import configs and topo file
from ntp_config import *
from topo import *



class test_NTP_FUN_007(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_NTP_FUN_007(self):

	  #vgroup b/w NTP client and NTP server
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring interface on linux machine
	self.linux.configure_ip_interface(p1_linux_ssx[0],var_dict['infc_linux1_ip/m'])

        self.myLog.output("==================Starting The Test====================")

	# Push NTP configuration on NTP client
	self.ssx.config_from_string(script_var['NTP_FUN_007'])
        
	#Checking Service availability of ntp on linux(NTP server) machine
	self.myLog.output("======Checking Service availability of ntp on linux(NTP server) machine====")
	self.linux.cmd("sudo /sbin/service ntpd stop")
	Cmd_out = self.linux.cmd("sudo sbin/service ntpd start")	
	self.failUnless(Cmd_out != "ntpd: unrecognized service","service not available so install ntp service into NTP server")


	#Checking connectivity b/w ntp server and ntp cLient
	self.ssx.cmd("context %s"%var_dict['cntxt1'])
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	time.sleep(5)
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])

	self.failUnless(Ping_out == 1,"ntp server is not reachable")

	#going to sleep i.e poll time interval from 64 sec to 124 seconds
        #time taken for synchronization in b/w ntp client and ntp server
        #this time is dynamically changes over time depending on the network conditions between the NTP server and the client
        time.sleep(540)

	#Dispalying ntp status after synchronization	
	self.myLog.output("======Dispalying ntp status ==============")
	self.myLog.output(self.ssx.cmd("show ntp status"))
	
	#Dispalying ntp associations after synchronization
        Ntp_Asso = self.ssx.cmd("show ntp associations")
        Ntp_Asso_Symbol = (Ntp_Asso.split("\n")[3]).split()[0]
        self.failUnless("*" in Ntp_Asso_Symbol,"NTP server is not synchronized with the client")
        self.myLog.output("======Dispalying ntp associations===:%s"%Ntp_Asso)

	
#       Changing timezone on NTP server side to UTC 
        self.linux.cmd("sudo ln -sf ../usr/share/zoneinfo/UTC/etc/localtime")
	
	#setting clock time to PST time zone 
        self.ssx.configcmd("clock  timezone PST -8 0")
        Clock_out = self.ssx.cmd("show clock")

	#setting clock time to PST time zone and enabling DST on NTP Client.
	self.ssx.configcmd("clock  timezone PST -8 0 DST  monthformat 3 2 0 2 0 11 1 1 1 59")
	self.ssx.cmd("context local")

	#Setting time on SSX (default timezone is UTC).
	self.ssx.cmd("clock set 2007:3:11:20:59:50")
		

	#setting clock time to PST time zone 
	self.ssx.cmd("context local")
	self.ssx.configcmd("clock  timezone PST -8 0")
	Clock_out = self.ssx.cmd("show clock")
	
	#Enabling DST on NTP Client.
	self.ssx.configcmd("clock  timezone PST -8 0 DST  monthformat 3 2 0 2 0 11 1 1 1 59")
	Clock_out1 = self.ssx.cmd("show clock")
	time.sleep(10)

	#Capturing only time(Hour:Minu:Sec) after  Synchronizing ssx client and ntp server
	time_str1 = Clock_out.split()[4]
	time_str2 =Clock_out1.split()[4]

	diff = diff_in_time_ssx(time_str1,time_str2)
	res =int(diff in range(3600,3625))
	self.failUnlessEqual(res,1,"time on SSX does not move forward by one hour after enabling DST")

	#Time on SSX before disabling DST.	
	Clock_out1 = self.ssx.cmd("show clock")

	#Disabling DST on ssx.
	self.ssx.configcmd("no clock  timezone PST -8 0 DST")
	self.ssx.configcmd("clock  timezone PST -8")
	Clock_out = self.ssx.cmd("show clock")


	#Capturing only time(Hour:Minu:Sec) after  Synchronizing ssx client and ntp server and after disabling DST.
	time_str1 = Clock_out.split()[4]
        time_str2 = Clock_out1.split()[4]

	#print diff
        diff = diff_in_time_ssx(time_str1,time_str2)
	self.failUnless(diff in range(3555,3625),"times are not matched after disabling DST")


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
	log = buildLogger(filename, debug=True, console=True)
	suite = test_suite()
	suite.addTest(test_NTP_FUN_007)
	test_runner(stream=sys.stdout).run(suite)

