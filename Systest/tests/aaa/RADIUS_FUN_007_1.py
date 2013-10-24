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

Description: -   Verify the default re-tries & timeout values 
		(3&10 sec respectively) are applied when a radius server becomes un reachable. 
		Repeating case for session accounting profile
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-FUN-007

TOPOLOGY DIAGRAM:

    (Linux)                              (SSX)                               (Linux)
    -------                             --------                          --------------
   |Takama | --------------------------|        |------------------------| qa-svr4      |
    -------                            |        |                         --------------
                                       |        |
                                       |Lihue-mc|
  (Netscreen)                          |        |                            (Linux)
    ------                             |        |                          --------------
   |qa-ns | --------------------------|        |-------------------------| qa-svr3      |
    ------                             |        |                          --------------
                                        --------

How to run: "python2.5 RADIUS_FUN_007_1.py"
AUTHOR: Mahesh - mahesh@primesoftsolutionsinc.com
	Raja rathnam - rathnam@primesoftsolutionsinc.com
REVIEWER:
"""

# Import the system libraries we need.
import sys, os

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import *
from SSX import SSX
from NS import NS
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

#import configs file
from aaa_config import *
from topo import *
from aaa import *

class test_RADIUS_FUN_007_1(test_case):

    myLog = getLogger()

    def setUp(self):
        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx1['ip_addr'])
        self.ssx.telnet()
        self.ssx.clear_health_stats()

        # Clear SSX configuration
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()


        """Establish a telnet session to the Netscreen."""
        self.ns5gt = NS(ns['ip_addr'])
        self.ns5gt.telnet()
        self.ns5gt.clear_config()

        self.ether_radius1 = Linux(radius1['ip_addr'],radius1['user_name'],radius1['password'])
        self.ether_radius1.telnet()

    def tearDown(self):
 	"""Clear the config and Close down the telnet session."""
        self.ssx.close()
        self.ns5gt.close()

        # Start the (killed) Radius daemon
        self.ether_radius1.cmd("sudo /etc/init.d/radiusd start")

	self.ether_radius1.close()

    def test_RADIUS_FUN_007_1(self):
        """
        Test case Id: -  RADIUS-FUN-007
        """

        #### Ethereal cap
        self.myLog.output(" Step 1 - removing the file rad_fun_007_1.pcap")
        self.ether_radius1.cmd("sudo rm rad_fun_007_1.pcap -f")

        self.myLog.output("Step 2 -Start tethereal to capture the packets and store the result in a pcap file")
        self.ether_radius1.cmd('sudo /usr/sbin/tethereal -i %s -q  -w rad_fun_007_1.pcap -R "radius" & '% topo.port_ssx_radius1[1])

        #Push the SSX configuration        
	self.ssx.config_from_string(script_var['common_ssx1'])
        self.ssx.config_from_string(script_var['rad_fun_007_1_ssx'])

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['rad_fun_007_1_ns5gt'])

        # Enable debug logs for aaad
        self.ssx.cmd("context %s" % script_var['context'])
        self.ssx.cmd("debug module aaad all")
        # Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

	# Kill the Radius daemon 
	self.ether_radius1.cmd("sudo /etc/init.d/radiusd stop")

	
	# Initiate IKEv1 session from a client to the SSX with valid X-auth credentials.
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.myLog.output (" Step 3 - stop tethereal by killing the tethereal application.")
        self.ether_radius1.cmd("sudo pkill tethereal")
	time.sleep(5)
        self.myLog.output  (" Step 4 - read the content of the file rad_fun_007_1.pcap ")
        output=self.ether_radius1.cmd('sudo /usr/sbin/tethereal -r rad_fun_007_1.pcap -R "radius.code == 4 && ! icmp"',timeout = 100)
        self.failUnless("radius" in output  , "Expected - packet with 'radius.code==4'" )

	'''
        #checking retry timeouts and no.of retrys
	self.myLog.output(output)
	ether_op=output.split('\n')
	count = 0
	for line in ether_op:
	    if "RADIUS" in line:
		count = count+1
        self.failUnless(count in [3,4], """ Expected - packet with 'radius.code==4' for 4 times; Actual -packets capctured with "radius.code==4" %d  times """% count)

	time_stamps = []
	for line in ether_op:
	    x=re.search('\d+.\d{6}',line)
            if x!=None :
		time_stamps.append(x.group(0))

        # check the time diff between each packet
	diff_time_stamps = 0
	for i in range(0,len(time_stamps)-1):
	    temp = float(time_stamps[i+1])-float(time_stamps[i])
            diff_time_stamps = diff_time_stamps+temp

	avg_time_stamp = diff_time_stamps/(len(time_stamps)-1)
	print avg_time_stamp
        # verifying the time intervels
        # verifying the time intervels
        self.failUnless(round(float(avg_time_stamp))in [9,10,11],"Expected -Retry time 10 sec,But Actual is: %f sec"%avg_time_stamp)
	'''


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_RADIUS_FUN_007_1)
    test_runner().run(suite)
    
