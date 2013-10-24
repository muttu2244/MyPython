#!/usr/bin/env python2.5

"""
##############################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#       
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#       
##############################################################################

DESCRIPTION: To Verify config can be changed during pending  CDR files to Intermediate TTLV files
TEST PLAN: CDR Test plans
TEST CASES: CDR_FUN_007
        
TOPOLOGY DIAGRAM: 
        
          
          |---------------|        |----------------|
          |               |        |                |            
          |    LINUX      | ------ |      SSX       |                                                                 
          | 17.1.1.1/24   |e1   2/3| 17.1.1.2/16    |                               
          |---------------|        |----------------|
        
        
AUTHOR:  laxmana@stoke.com
        
REVIEWER: srinivas@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from cdr import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *
#import private libraries
from ike import *

from misc import *

class test_CDR_FUN_007(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(xpress_vpn1['ip_addr'],xpress_vpn1['user_name'],xpress_vpn1['password'])
	self.linux1=Linux(xpress_vpn3_multi['ip_addr'],xpress_vpn3_multi['user_name'],xpress_vpn3_multi['password'])
        self.ssx.telnet()
        self.linux.telnet()
        self.linux1.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
	self.linux1.close()

    def test_CDR_FUN_007(self):

	# Enable debug logs for iked
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        #changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        #clearing sessions on ssx
        self.ssx.cmd("clear session all")

        #Clearing already existing files on the linux machine
        self.linux.cmd("su root")
        time.sleep(5)
        self.linux.cmd("su krao")
        time.sleep(5)
        self.linux.cmd("cd")
        time.sleep(5)
        self.linux.cmd("rm -rf *.asn1")
        self.linux.cmd("rm -rf *.xml")
        self.linux.cmd("rm -rf *.ttlv")
        self.linux.cmd("exit")
        self.linux.cmd("exit")

        self.linux.cmd("cd /tftpboot/")
        #self.linux.cmd("sudo rm *.*")
        self.linux.cmd("sudo rm -rf *.asn1")
        self.linux.cmd("sudo rm -rf *.xml")
        self.linux.cmd("sudo rm -rf *.ttlv")


	#configuring interface on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

	# Push xpress vpn config on linux
        self.linux.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        self.linux.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")

	# Push SSX config
	self.ssx.config_from_string(script_var['CDR_FUN_007'])
    


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd")
        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")
        time.sleep(5)
         
        self.linux.cmd("sudo ./start_ike")
        time.sleep(5)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSECv4" in op1,"Failed because there is no session of IPSEC")


        self.linux.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux.cmd("quit")


        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Waiting for 3 mins to change the upload server ip to upload CDR files on different linux machine")
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")
        time.sleep(180)

        #Changing the running configuration
	self.ssx.config_from_string(script_var['CDR_FUN_007A'])

        #Saving the configuration.
        self.ssx.cmd("save configuration")
        time.sleep(2)

        #Displaying the saved configuration
        saved_conf =  self.ssx.cmd("show configuration cdr")
        self.myLog.output(saved_conf)



        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Waiting for 10 mins to get the final files uploaded on linux machine 10.3.2.33(huahine) ")
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

        time.sleep(420)

        self.linux.cmd("ls -rth /tftpboot/ | grep \".ttlv\" ")

        linuxip = self.linux1.cmd("ls -rth /tftpboot/ | grep \".ttlv\" | tail -n 1")
        linuxip1 = linuxip.strip()
        self.myLog.output(linuxip1)

        self.failUnless(linuxip1,"Failed to generate TTLV files after changing the configuration")
        self.myLog.output("CDR data generation passed for a given session even after changing and saving of running new CDR configuration")
        self.myLog.info("*" *50)
        self.myLog.output("TTLV files were generated instead of ASN files")
        self.myLog.info("*" *50)

        time.sleep(3)
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
        suite.addTest(test_CDR_FUN_007)
        test_runner(stream=sys.stdout).run(suite)
