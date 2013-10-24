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

DESCRIPTION: Verify clock synchronization when ntp profile is configured in some other context
TEST PLAN: NTP FUN Test plans
TEST CASES: NTP_FUN_002

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_002.py
AUTHOR: nkasera@stoke.com 
REVIEWER:
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

#import configs file and topo file
from ntp_config import *
from topo import *



class test_NTP_FUN_002(test_case):
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

    def test_NTP_FUN_002(self):

	#configuring interface on linux machine
        self.myLog.output("==================Starting The Test====================")
	
	self.linux.configure_ip_interface(p1_linux_ssx[0],var_dict['infc_linux1_ip/m'])
		
	#Push NTP configuration on NTP client
	#self.ssx.config_from_string(script_var['common_ssx'])
	self.ssx.config_from_string(script_var['NTP_FUN_002'])

	#removing the /etc/ntp/keys and ntp configuration.
        self.linux.cmd("sudo rm -f /etc/ntp/keys")
        self.linux.cmd("sudo rm -f /etc/ntp.conf")
	
	self.linux.cmd("cd /etc")
        self.linux.cmd("sudo rm -f ntp.conf")
        self.linux.cmd("sudo touch ntp.conf")
        self.linux.cmd("sudo chmod a+rwx ntp.conf")
        self.linux.write_to_file(script_var['ntp.conf'],"ntp.conf","/etc/")
		
	#Checking Service availability of ntp on linux(NTP server) machine
	self.myLog.output("======Checking Service availability of ntp on linux(NTP server) machine====")
	self.linux.cmd("sudo /sbin/service ntpd stop")
	Cmd_out = self.linux.cmd("sudo /sbin/service ntpd start")	
	self.failUnless(Cmd_out != "ntpd: unrecognized service","service not available so install ntp service into NTP server")


	#Checking connectivity b/w NTP server  and NTP client
	self.myLog.output("======Checking connectivity b/w NTP server  and NTP client=====")
	self.ssx.cmd("context %s"%var_dict['context_name'])
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	time.sleep(5)
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	self.failUnless(Ping_out == 1,"ntp server is not reachable")

	#going to sleep i.e poll time interval from 64 sec to 124 seconds
        #time taken for synchronization in b/w ntp client and ntp server
        #this time is dynamically changes over time depending on the network conditions between the NTP server and the client
	self.myLog.output("======Delay of 10 mins for synchronizing NTP server=====")
	time.sleep(600)

	self.myLog.output("======Dispalying ntp status ==============")
	self.myLog.output(self.ssx.cmd("show ntp status"))

	self.myLog.output("======Dispalying ntp associations==============")

	Ntp_associations = self.ssx.cmd("show ntp associations")
	Ntp_associations = (Ntp_associations.split("\n")[3]).split()[0]
	self.failUnless("*" in Ntp_associations,"NTP server is not synchronized with the client")
	self.myLog.output(self.ssx.cmd("show ntp associations"))

	Date_out = self.linux.cmd("date")
        Clock_out = self.ssx.cmd("show clock")

	#Changing Timezone on NTP Client to UTC
        self.ssx.configcmd("clock  timezone UTC 0 0")
        Clock_out = self.ssx.cmd("show clock")
	#Changing timezone on server to UTC.
        self.linux.cmd("sudo ln -sf ../usr/share/zoneinfo/UTC /etc/localtime")
        Date_out = self.linux.cmd("date")

	#Displaying Date and Clock output after synchronization of NTP server with client.
	self.myLog.output("======Date and Clock output after synchronization==============")
	Date_out = self.linux.cmd("date")
        Clock_out = self.ssx.cmd("show clock")

	#Capturing only time in hou:min:sec from date and clock outputs
	time_str2 = Date_out.split()[3]
	time_str1  = Clock_out.split()[4]

	self.myLog.output("======Both are in same timezone=======")
	diff = diff_in_time_ssx(time_str2,time_str1)	
	self.myLog.output(diff)
	self.failUnless(diff in range(0,31),"times are not matched")

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
	suite.addTest(test_NTP_FUN_002)
	test_runner(stream=sys.stdout).run(suite)

