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

DESCRIPTION:Configure the SSX with NTP Server and Authenticate on SSX 
and NTP server
TEST PLAN: NTP Sanity Test plans
TEST CASES: NTP_FUN_010

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24----------------> TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 NTP_FUN_010.py
AUTHOR: rajshekar@primesoftsolutionsinc.com 
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



class test_NTP_FUN_010(test_case):
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

    def test_NTP_FUN_010(self):

	#vgroup b/w NTP client and NTP server
        vg_output1 = vgroup_new(topo2[:])
        self.failUnless(vg_output1 == None,"vgroup FAILED")

	#configuring interface on NTP server.
	self.linux.configure_ip_interface(p1_linux_ssx[0],var_dict['infc_linux1_ip/m'])

        self.myLog.output("==================Starting The Test====================")

	# Push NTP configuration on NTP client .
	self.ssx.config_from_string(script_var['common_ssx'])
	self.ssx.config_from_string(script_var['NTP_FUN_010'])
	
	#Writing ntp configuration into the /etc/ntp/keys for authentication on server side.
	self.linux.cmd("sudo rm -f /etc/ntp/keys")
	self.linux.cmd("sudo rm -f /etc/ntp.conf")
	self.linux.cmd("cd /etc/")
	self.linux.cmd("sudo touch ntp.conf")

	#Writing ntp configuration into the /etc/ntp.conf for authentication on server side.
	self.linux.cmd("sudo chmod 777 ntp.conf")

	self.linux.cmd("sudo echo 'keys /etc/ntp/keys' >>/etc/ntp.conf")
	self.linux.cmd("sudo echo 'trustedkey %s'  >> /etc/ntp.conf"%(var_dict['key']))
	self.linux.cmd("cd ..")
	self.linux.cmd("cd /etc/ntp/")	
	self.linux.cmd("sudo touch keys")
	self.linux.cmd("sudo chmod 777 keys")
	self.linux.cmd("sudo echo ' %s      M      stoke' >> /etc/ntp/keys"%(var_dict['key']))		       	 		
	#Checking Service availability of ntp on NTP server(Linux)
	self.myLog.output("=====Checking Service availability of ntp on NTP server(Linux)=====")
	Cmd_out = self.linux.cmd("sudo /sbin/service ntpd stop")
	Cmd_out = self.linux.cmd("sudo /sbin/service ntpd start")	
	self.failUnless (Cmd_out != "ntpd: unrecognized service","service not available so install ntp service into NTP server")

	#Checking connectivity b/w NTP server  and NTP client
	self.ssx.cmd("context %s"%var_dict['cntxt1'])
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	#time.sleep(15)
	Ping_out = self.ssx.ping(var_dict['infc_linux1_ip'])
	self.failUnless(Ping_out == 1,"no connectivity b/w NTP server  and NTP client")
	
	#going to sleep i.e poll time interval from 64 sec to 124 seconds
        #time taken for synchronization in b/w ntp client and ntp server
        #this time is dynamically changes over time depending on the network conditions between the NTP server and the client
	time.sleep(540)

	
	self.myLog.output("======Dispalying ntp status ==============")
	self.myLog.output(self.ssx.cmd("show ntp status"))

	self.myLog.output("======Dispalying ntp associations==============")
	Ntp_Asso = self.ssx.cmd("show ntp associations")
	Ntp_Asso_Symbol = (Ntp_Asso.split("\n")[3]).split()[0]
        self.failUnless("*" in Ntp_Asso_Symbol,"NTP server is not synchronized with the client")
        self.myLog.output(Ntp_Asso)

	Date_out = self.linux.cmd("date")
        Clock_out = self.ssx.cmd("show clock")

        #Changing Timezone on NTP Client to UTC

        if "PST" in Clock_out:
                self.ssx.configcmd("clock  timezone UTC +8")
                Clock_out = self.ssx.cmd("show clock")
         #Changing timezone on server to UTC.
        if "UTC" not in Date_out:
                self.linux.cmd("sudo ln -sf ../usr/share/zoneinfo/UTC /etc/localtime")
                Date_out = self.linux.cmd("date")

        #Displaying Date and Clock output after synchronization of NTP server with client.
        self.myLog.output("======Date and Clock output after synchronization==============")
        Date_out = self.linux.cmd("date")
        Clock_out = self.ssx.cmd("show clock")

        #Capturing only time in hou:min:sec from date and clock outputs
        time_str1 = Date_out.split()[3]
        time_str2  = Clock_out.split()[4]

        self.myLog.output("======Both are in same timezone=======")
        diff = diff_in_time_ssx(time_str1,time_str2)
        print diff
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
	suite.addTest(test_NTP_FUN_010)
	test_runner(stream=sys.stdout).run(suite)

