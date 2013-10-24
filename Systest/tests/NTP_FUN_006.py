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

DESCRIPTION: Configure the SSX with NTP server; set the time; save the 
 config and reload. Verify that the NTP config and time still exists.
TEST PLAN: NTP Test plans
TEST CASES: NTP_FUN_006

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------
       |                                                                                |
       |                LINUX                            SSX                            |
       |          2.2.2.3/24     ------------>      2.2.2.45/24                         |
       |                                                                                |
       |              e1                              Port 2/1                          |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_006.py
AUTHOR:rajshekar@primesoftsolutionsinc.com  
REVIEWER:sudama@primesoftsolutionsinc.com

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

#import configs file
from ntp_config import *
from topo import *



class test_NTP_FUN_006(test_case):
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

    def test_NTP_FUN_006(self):

	 #vgroup b/w NTP client and NTP server
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")


	# Push NTP configuration on NTP client 
	self.ssx.config_from_string(script_var['NTP_FUN_012'])

	 #configuring interface on linux machine

        self.linux.configure_ip_interface(p1_linux_ssx[0],var_dict['infc_linux1_ip/m'])


	#Setting time on SSX (YYYY:MM:DD:HH:MIN:SS).
	self.ssx.cmd("context local")
	self.ssx.cmd("clock set 2008:01:21:09:50:34")
	
	 #Checking Service availability of ntp on linux(NTP server) machine
        self.myLog.output("======Checking Service availability of ntp on linux(NTP server) machine====")
        self.linux.cmd("sudo /sbin/service ntpd stop")
        Cmd_out = self.linux.cmd("sudo /sbin/service ntpd start")
        self.failUnless(Cmd_out != "ntpd: unrecognized service","service not available so install ntp service into NTP server")

	time.sleep(90)
	#Checking connectivity b/w NTP server  and NTP client
        self.myLog.output("======Checking connectivity b/w NTP server  and NTP client=====")
        self.ssx.cmd("context ntp")
        Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
        self.failUnless(Ping_out == 1,"ntp server is not reachable")

        #going to sleep i.e poll time interval from 64 sec to 124 seconds
        #time taken for synchronization in b/w ntp client and ntp server
        #this time is dynamically changes over time depending on the network conditions between the NTP server and the client
        time.sleep(1024)

	Clock_out = self.ssx.cmd("show clock")
	Date_out = self.linux.cmd("date")	

	 #Changing Timezone on NTP Client to UTC

        if "PST" in Clock_out:
                self.ssx.configcmd("clock  timezone UTC +8")
                Clock_out = self.ssx.cmd("show clock")
         #Changing timezone on server to UTC.
        if "UTC" not in Date_out:
                self.linux.cmd("sudo ln -sf ../usr/share/zoneinfo/UTC /etc/localtime")
                Date_out = self.linux.cmd("date")

	Clock_out = self.ssx.cmd("show clock")
	
	Config = self.ssx.cmd("show configuration")

	self.myLog.output("======Dispalying ntp status ==============")
        self.myLog.output(self.ssx.cmd("show ntp status"))

        self.myLog.output("======Dispalying ntp associations==============")

	self.myLog.output(self.ssx.cmd("show ntp associations"))
	
	
	#Reload SSX
	self.ssx.cmd("reload")
	time.sleep(35)

        self.myLog.output("======Dispalying ntp associations after reloading SSX==============")

        self.myLog.output(self.ssx.cmd("show ntp associations"))

	self.myLog.output("======Dispalying ntp configuration after reloading SSX==============")
	self.myLog.output(self.ssx.cmd("show configuration"))

	self.myLog.output("======Dispalying ntp status after reloading SSX  ==============")
        self.myLog.output(self.ssx.cmd("show ntp status"))


	After_reload_Clock_out = self.ssx.cmd("show clock")

	#Capturing only time in hours.
        After_reload_Clock_out = After_reload_Clock_out.split()[4].split(":")[0]
	Clock_out = Clock_out.split()[4].split(":")[0]

	After_reload_Config = self.ssx.cmd("show configuration")
	self.failUnless(After_reload_Config  in Config,"TEST FAILED")
	self.failUnless(After_reload_Clock_out in Clock_out,"TEST FAILED")

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
	suite.addTest(test_NTP_FUN_006)
	test_runner(stream=sys.stdout).run(suite)

