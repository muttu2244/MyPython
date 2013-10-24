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

DESCRIPTION:To Verify IKEV2 Multiple Sessions with 2 different CDR contexts &  its data getting uploaded in XML format to the configured server with TFTP protocol.
TEST PLAN: CDR Test plans
TEST CASES: CDR_FUN_045


        
TOPOLOGY DIAGRAM: 
        
          
          |---------------|        |----------------|
          |               |        |                |            
          |   LINUX 1     | ------ |      SSX       |                                                                 
          | 17.1.1.1/24   |e1   3/0|  17.1.1.2/16   |                               
          |---------------|        |                |
                                   |  15.1.1.2/16   |
				   |----------------|
                                          |  2/1
					  |
					  |
					  | e2
				   |----------------|        
				   |                |
				   |    LINUX 2     |
				   | 15.1.1.1/24    |
				   |----------------|        
        
AUTHOR: laxmana@stoke.com
        
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


class test_CDR_FUN_045(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1=Linux(xpress_vpn1_multi['ip_addr'],xpress_vpn1_multi['user_name'],xpress_vpn1_multi['password'])
	self.linux2=Linux(xpress_vpn2_multi['ip_addr'],xpress_vpn2_multi['user_name'],xpress_vpn2_multi['password'])
        self.ssx.telnet()
        self.linux1.telnet()
        self.linux2.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux1.close()
	self.linux2.close()

    def test_CDR_FUN_045(self):

	# Enable debug logs for iked
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        #clearing sessions on ssx
        self.ssx.cmd("context %s" %(script_var['context_name1']))
        self.ssx.cmd("clear session all")
        self.ssx.cmd("context %s" %(script_var['context_name2']))
        self.ssx.cmd("clear session all")

	#configuring interface on linux machine
	self.linux1.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

	#configuring interface on linux machine
	self.linux2.configure_ip_interface(p1_ssx_xpressvpn2[1], script_var['xpress_phy_iface2_ip_mask'])

        #Clearing already existing files on the linux machine
        self.linux1.cmd("su root")
        time.sleep(5)
        self.linux1.cmd("su krao")
        time.sleep(5)
        self.linux1.cmd("cd")
        time.sleep(5)
        self.linux1.cmd("rm -rf *.asn1")
        self.linux1.cmd("rm -rf *.xml")
        self.linux1.cmd("rm -rf *.ttlv")
        self.linux1.cmd("exit")
        self.linux1.cmd("exit")

        self.linux1.cmd("cd /tftpboot/")
        #self.linux1.cmd("sudo rm *.*")
        self.linux1.cmd("sudo rm -rf *.asn1")
        self.linux1.cmd("sudo rm -rf *.xml")
        self.linux1.cmd("sudo rm -rf *.ttlv")

        #Clearing already existing files on the linux machine
        self.linux2.cmd("su root")
        time.sleep(5)
        self.linux2.cmd("su krao")
        time.sleep(5)
        self.linux2.cmd("cd")
        time.sleep(5)
        self.linux2.cmd("rm -rf *.asn1")
        self.linux2.cmd("rm -rf *.xml")
        self.linux2.cmd("rm -rf *.ttlv")
        self.linux2.cmd("exit")
        self.linux2.cmd("exit")

        self.linux2.cmd("cd /tftpboot/")
        #self.linux1.cmd("sudo rm *.*")
        self.linux2.cmd("sudo rm -rf *.asn1")
        self.linux2.cmd("sudo rm -rf *.xml")
        self.linux2.cmd("sudo rm -rf *.ttlv")

        #Vgrouping the Topology 
        vgroup_new(vlan_cfg_str)
        vgroup_new(vlan_cfg_str1)


        # Push xpress vpn config on linux
        self.linux1.write_to_file(script_var['autoexec_config_takama_multi'],"autoexec.cfg","/xpm/")
        self.linux1.write_to_file(script_var['add_ip_takama_multi'],"add_ip_takama","/xpm/")

        self.linux2.write_to_file(script_var['autoexec_config_huahine_multi'],"autoexec.cfg","/xpm/")
        self.linux2.write_to_file(script_var['add_ip_huahine_multi'],"add_ip_takama","/xpm/")


        # Push SSX config
        self.ssx.config_from_string(script_var['CDR_FUN_MULTI'])

	# Initiate IKE Session from Xpress VPN Client (takama)
        self.linux1.cmd("cd")
        self.linux1.cmd("cd /xpm")
        self.linux1.cmd("sudo chmod 777 add_ip_takama")
        self.linux1.cmd("sudo ./add_ip_takama")
        self.linux2.cmd("cd")
        self.linux2.cmd("cd /xpm")
        self.linux2.cmd("sudo chmod 777 add_ip_takama")
        self.linux2.cmd("sudo ./add_ip_takama")

        time.sleep(5)

        self.linux1.cmd("sudo ./start_ike")
        time.sleep(5)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")


        self.linux1.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux1.cmd("quit")

	sess_id1 = self.ssx.cmd("show session detail | grep Session_handle ")
        self.myLog.info(sess_id1)

        self.linux2.cmd("sudo ./start_ike")
        time.sleep(5)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")


        self.linux2.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip2'],script_var['pool_ip2']))
        self.linux2.cmd("quit")

	sess_id2 = self.ssx.cmd("show session detail | grep Session_handle ")
        self.myLog.info(sess_id2)



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
        suite.addTest(test_CDR_FUN_045)
        test_runner(stream=sys.stdout).run(suite)
