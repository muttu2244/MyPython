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

DESCRIPTION:To vererify that SSX obtains time from the NTP server and 
updates in the SSX correctly.
TEST PLAN: Sanity Test plans
TEST CASES: DoCoMo_8_3_6

TOPOLOGY DIAGRAM:


        --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |         Trans  IP = 2.2.2.3/24  ---------->     TransIP = 2.2.2.45/24          |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 DoCoMo_8_3_6.py
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

#import configs file and topo file
from config_docomo import *
from topo import *



class test_DoCoMo_8_3_6(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(linux2['ip_addr'],linux['user_name'],linux['password'])
        self.ssx.telnet()
        self.linux.telnet()
	'''
	# wait for card to come up
        self.ssx.wait4cards()

        # Clear the SSX config
        self.ssx.clear_config()
        self.ssx.clear_health_stats()
	'''
    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_DoCoMo_8_3_6(self):
	'''
        self.myLog.info("Running vgroup")
        ssx_name= ssx["ip_addr"].split("-mc")[0]
        vportssx1 = port_ssx_linux2[0].replace('/',':')
	vport1   = port_ssx_linux1[1].replace('eth','e')

	vgroup_new("%s:%s %s:%s"%(ssx_name,vportssx1,linux2['ip_addr'],vport1))
	'''
	# Configure the NTP Server.
	self.linux.configure_ip_interface(port_ssx_linux2[1],others_var['infc_linux1_ip/m'])

        self.myLog.output("==================Starting The Test====================")

	# Push NTP configuration on NTP client
	self.ssx.load_min_config(ssx["hostname"])
	self.ssx.config_from_string(others_var['DoCoMo_8_3_6'])	
	
	#Checking Service availability of ntp on linux(NTP server) machine
	self.myLog.output("======Checking Service availability of ntp on linux(NTP server) machine====")
	StatusOp = self.linux.cmd("sudo /sbin/service ntpd status")
	if "not running" in StatusOp:
		self.myLog.info("NTP server is not runnng, starting the server")
		self.linux.cmd("sudo /sbin/service ntpd start")

	'''
	self.linux.cmd("sudo /sbin/service ntpd stop")
	Cmd_out = self.linux.cmd("sudo /sbin/service ntpd start")	
	self.failUnless(Cmd_out != "ntpd: unrecognized service","service not available so install ntp service in NTP server")
	'''
	#Removing the tethereal capture file if its present        
        self.linux.cmd("sudo rm ntp.pcap -f")

        #Capturing the packets based on filter function on remote Linux
        outstr=self.linux.cmd("sudo /usr/sbin/tethereal -i '%s' -q -w 'ntp.pcap' &" %port_ssx_linux2[1])

	#Checking connectivity b/w NTP server  and NTP client
	self.myLog.output("======Checking connectivity b/w NTP server  and NTP client=====")
	self.ssx.cmd("context ntp")
	Ping_out = self.ssx.ping(others_var['infc_linux1_ip'])
	time.sleep(5)
	Ping_out = self.ssx.ping(others_var['infc_linux1_ip'])
	self.failUnless(Ping_out == 1,"ntp server is not reachable")

	#going to sleep i.e poll time interval from 64 sec to 124 seconds
        #time taken for synchronization in b/w ntp client and ntp server
        #this time is dynamically changes over time depending on the network conditions between the NTP server and the client
	self.myLog.info("Time given for synchronization in b/w ntp client and ntp server")
	time.sleep(540)

	self.myLog.output("======Dispalying ntp status ==============")
	self.myLog.output(self.ssx.cmd("show ntp status"))

	self.myLog.output("======Dispalying ntp associations==============")

	Ntp_associations = self.ssx.cmd("show ntp associations")
	Ntp_associations = (Ntp_associations.split("\n")[3]).split()[0]
	self.failUnless("*" in Ntp_associations,"NTP server is not synchronized with the client")
	self.myLog.output(self.ssx.cmd("show ntp associations"))

	#killing the tethreal process on remopte m/c and reading the tethreal capture file
        self.linux.cmd("sudo pkill tethereal")
        Out = self.linux.cmd("sudo /usr/sbin/tethereal -r 'ntp.pcap' -R ntp")
	self.failUnless("NTP NTP"in Out,"NTP packets are not transmitted")

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
	time_str2 = Date_out.split()[3]
	time_str1  = Clock_out.split()[4]

	self.myLog.output("======Both are in same timezone=======")
	diff = diff_in_time_ssx(time_str1,time_str2)	
	#print diff
	self.failUnless(diff in range(-31,31),"times are not matched")

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
	suite.addTest(test_DoCoMo_8_3_6)
	test_runner().run(suite)

