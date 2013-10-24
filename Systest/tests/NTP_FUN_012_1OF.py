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

DESCRIPTION:Configure the SSX with NTP Server and then IMC switchover 
and NTP server
TEST PLAN: NTP Sanity Test plans
TEST CASES: NTP_FUN_012

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24----------------> TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_012.py
AUTHOR:rajshekar@primesoftsolutionsinc.com  
REVIEWER:sudama@primesoftsolutionsinc.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import *
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy,diff_in_time_ssx
from misc import *

#import config and topo file
from ntp_config import *
from topo import *



class test_NTP_FUN_012(test_case):
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

    def test_NTP_FUN_012(self):

	#vgroup b/w NTP client and NTP server
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")



	#configuring interface on NTP server side.
	self.linux.configure_ip_interface(p1_linux_ssx[0],var_dict['infc_linux1_ip/m'])

        self.myLog.output("==================Starting The Test====================")

	# Push NTP configuration on NTP client 
	self.ssx.config_from_string(script_var['NTP_FUN_012'])
	
	#Checking Service availability of ntp on linux(NTP server) machine
	Cmd_out = self.linux.cmd("/sbin/service ntpd status")	
	self.myLog.output("======Checking Service availability of ntp on NTP client====%s"%self.linux.cmd("sudo /sbin/service ntpd start"))
	self.failUnless(Cmd_out !="ntpd: unrecognized service","service not available so install ntp service into NTP server")
	
	
	#Checking connectivity b/w linux and SSX
	self.ssx.cmd("context %s"%var_dict['cntxt1'])
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	time.sleep(5)
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	self.failUnless(Ping_out == 1,"ntp server is not reachable from ntp client")
	
	#maximum time taken (120 seconds) for synchronizing NTP server with NTP client
	time.sleep(440)

	#Dispalying ntp status on NTP client after synchronization b/w NTP server and client.
	self.myLog.output("===Dispalying ntp statusafter synchronization =====%s"%self.ssx.cmd("show ntp status"))

	#Capturing "*" symbol from result of ntp association,that represents the synchronization.
	self.myLog.output("======Dispalying ntp associations==============")
        Ntp_Asso = self.ssx.cmd("show ntp associations")
        Ntp_Asso_Symbol = (Ntp_Asso.split("\n")[3]).split()[0]
        self.failUnless("*" in Ntp_Asso_Symbol,"NTP server is not synchronized with the client")
        self.myLog.output(Ntp_Asso)

	
	 #clock and date o/p of ntp server and client after Synchronization
        self.myLog.output("==== clock and date o/p of ntp server and client after Synchronization=====")
        Clock_out = self.ssx.cmd("show clock")
        Date_out = self.linux.cmd("date")

	#Changing timezone on NTP server to UTC timezone if timezone is not UTC.
        if Date_out.split()[4] != "UTC":
                self.linux.cmd("sudo ln -sf ../usr/share/zoneinfo/UTC /etc/localtime")
	
	#Now the timezone on NTP server is UTC
	Date_out = self.linux.cmd("date")
	
	 #Changing Timezone on NTP Client to UTC
        if "PST" in Clock_out:
                self.ssx.configcmd("clock  timezone UTC +8")
                Clock_out = self.ssx.cmd("show clock")


	#Displaying clock and date o/p of ntp server and client after Synchronization.
	self.myLog.output("clock and date o/p of ntp server and client which are in UTC timezone")
	self.myLog.output(Clock_out)
	self.myLog.output(Date_out)
	
	#Splitting Date_out and Clock_out inorder to capture only time in hours:minutes:seconds.
	time_str1 = Clock_out.split()[4]
	time_str2 = Date_out.split()[3]

	#Both times are in same time zone i.e UTC 
	diff = diff_in_time_ssx(time_str1,time_str2)	
	self.failUnless(diff in range(0,100),"times are not synchronized before doing imc-switchover")

	 # Switching Over the IMC
        self.ssx.imc_switchover_mgmt("system imc-switchover")
	
	time.sleep(5)
	#Commang for coming out of Standby mode to active.
	self.ssx.imc_switchover_mgmt("system imc-switchover")

	#Storing the clock and date in corresponding variables
	Clock_out = self.ssx.cmd("show clock")
	Date_out = self.linux.cmd("date")

	#Capturing time which is in Hours:minutes:Seconds
        time_str1 = Clock_out.split()[4]
        time_str2 = Date_out.split()[3]


	#API for finding the difference b/w time on NTP server and NTP client.
	diff = diff_in_time_ssx(time_str1,time_str2)

	self.failUnlessEqual(diff in range(0,100),"times are not synchronized after imc-switchover")


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
	suite.addTest(test_NTP_FUN_012)
	test_runner(stream=sys.stdout).run(suite)

