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

DESCRIPTION:For a session,specify time and volume events along with action to generate cdr records and verify that the configured events trigger and action generates cdr record as expected.
TEST PLAN: CDR Test plans
TEST CASES:CDR_HA_FUN_004 
        
TOPOLOGY DIAGRAM: 
        
          
          |---------------|        |----------------|
          |               |        |                |            
          |    LINUX      | ------ |      SSX       |                                                                 
          | 17.1.1.1/24   |e1   2/3| 17.1.1.2/16    |                               
          |---------------|        |----------------|
        
HOW TO RUN:python2.5 CDR_HA_FUN_004.py
AUTHOR:		laxmana@stoke.com
REVIEWER:	srinivas@stoke.com

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
from rtc import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *

#import private libraries
from ike import *
from misc import *

class test_CDR_HA_FUN_004(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx_HA["name"])
	self.linux=Linux(xpress_vpn1['ip_addr'],xpress_vpn1['user_name'],xpress_vpn1['password'])
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

    def test_CDR_HA_FUN_004(self):

	# Enable debug logs for iked
	self.ssx.cmd("clear log debug")
	self.ssx.cmd("debug module count all")
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
	
	 # Push SSX config
        self.ssx.config_from_string(script_var['CDR_FUN_033'])

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


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd")
        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")
        time.sleep(5)
         
        self.linux.cmd("sudo ./start_ike")
        time.sleep(10)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")

	#Initiate Ping through tunnel 
        op_ping = self.linux.ping_xpress_vpn(script_var['pool_ip'],script_var['ses_loopip'],"1050","4")
        self.failUnless(op_ping,"Ping through tunnel failed")
        self.linux.cmd("quit")

        #Executing IMC-Switc-Over
        self.ssx.imc_switchover_mgmt("system imc-switchover")

        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Waiting for 60 seconds to get the files generated on the linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

        time.sleep(200)


	'''
        self.ssx.close()
        self.ssx = SSX(ssx_HA["ip_addr"])
        self.ssx.telnet()
	'''

        self.linux.cmd("cd /tftpboot/ | grep \".ttlv\"")
        linuxtftp = self.linux.cmd("ls -rth /tftpboot/ | grep \".ttlv\" | tail -n 1")
        linuxtftp1 = linuxtftp.strip()
        linuxtftp2 = linuxtftp1.strip().strip()
        self.myLog.info(linuxtftp1)
        self.myLog.info(linuxtftp2)
        self.failUnless(linuxtftp2,"Files are not generated on the Linux machine")

        #self.ssx.cmd("context cdr-1")
        self.ssx.cmd("context local")
	#res = self.ssx.ftppasswd("copy sftp://root@%s:/tftpboot/%s /hd/%s noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2,linuxtftp2))
	res = self.ssx.cmd("copy tftp://%s/%s /hd noconfirm" % (script_var['upload_server_mgmt_ip'],linuxtftp2))
	#res = self.ssx.ftppasswd("copy tftp://%s:%s /hd/%s noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2,linuxtftp2))
        time.sleep(20)


	#ttl1= self.ssx.shellcmd("cd /hdp/cdr/cdr-1/customer")
	ttl1= self.ssx.shellcmd("cd /hd")
        time.sleep(10)
        ttl1 =  self.ssx.shellcmd("ls -rth | grep .ttlv | tail -n -1")
        ttl2 = ttl1.split("\n")
        ttl3 =  ttl2[1]

        ttl1= self.ssx.shellcmd("cdrdump -f %s -r 0"%ttl3)
        self.myLog.output(ttl1)
        self.failUnless('Record index too high' not in ttl1, "Record one is not generated")

        ttl1= self.ssx.shellcmd("cdrdump -f %s -r 1"%ttl3)
        self.myLog.output(ttl1)
	Out = Verify_data_in_cdr_records(self,record = ttl1,test_string="tag(2)=INTERIM_RECORD_TYPE")
        self.failUnless(Out == "1" ,"Time events are not triggered for session")

        ttl1= self.ssx.shellcmd("cdrdump -f %s -r 2"%ttl3)
        self.myLog.output(ttl1)
        Out = Verify_data_in_cdr_records(self,record = ttl1,test_string="tag(2)=INTERIM_RECORD_TYPE")
        self.failUnless(Out == "2" ,"Volume events are not triggered for session")

	self.myLog.info("\n\n")
	self.myLog.info("*" *50)
	self.myLog.output("\n\nTime and volume events to session generated as expected\n\n")
	self.myLog.info("*" *50)

	self.myLog.output("\n\nDisplaying events configured on ssx\n\n%s\n\n"%self.ssx.cmd("show events"))


        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,IMC_Switch=1,Card_Reset=1), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_CDR_HA_FUN_004)
        test_runner(stream=sys.stdout).run(suite)
