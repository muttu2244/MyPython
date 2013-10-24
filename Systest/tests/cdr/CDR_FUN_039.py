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

DESCRIPTION:To Verify  CDR data gets uploaded with multiple include filters.
TEST PLAN: CDR Test plans
TEST CASES: CDR_FUN_039
        
TOPOLOGY DIAGRAM: 
        
          
          |---------------|        |----------------|
          |               |        |                |            
          |    LINUX      | ------ |      SSX       |                                                                 
          | 17.1.1.1/24   |e1   2/3| 17.1.1.2/16    |                               
          |---------------|        |----------------|
        
        
AUTHOR:  suhasini@primesoftsolutionsinc.com 
        
REVIEWER: alok@primesoftsolutionsinc.com

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


class test_CDR_FUN_039(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(xpress_vpn1['ip_addr'],xpress_vpn1['user_name'],xpress_vpn1['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Establish a telnet session to the radius servers
        self.radclient_radius1 = Linux(xpress_vpn2_multi['ip_addr'],xpress_vpn2_multi['user_name'],
                                xpress_vpn2_multi['password'])
        self.radclient_radius1.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()
        self.radclient_radius1.close()

    def test_CDR_FUN_039(self):

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
        #self.xpress_vpn.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])
        self.radclient_radius1.configure_ip_interface(ssx_vgroup1[1], script_var['radius1_ip_mask'])


        #Vgrouping the Topology 
        vgroup_new(vlan_cfg_str1)


	#configuring interface on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

	# Push xpress vpn config on linux
        self.linux.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        self.linux.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")

        # Push SSX config
        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Pushing configuration with multiple include filters 4,0,1")
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

        self.ssx.config_from_string(script_var['CDR_FUN_039'])
    

         #Vgrouping the Topology 
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
 

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


        self.linux.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux.cmd("quit")

        self.ssx.cmd("context %s" %(script_var['context_name']))
        #clearing sessions on ssx
        #self.ssx.cmd("clear session all")

        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
	self.myLog.info("Waiting for 60 seconds to get the files generated on the linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")
        
        time.sleep(90) 

        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Checking of ttlv files which are generated on SSX-%s ...... " % ssx['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")



        #Checking for Record type(0)=SESSION_START in  ttlv files using CDR dump tool
        self.linux.cmd("cd")
        self.linux.cmd("cd /tftpboot/")
        linuxtftp = self.linux.cmd("ls -rth | grep \".ttlv\" | tail -n 1")
        linuxtftp1 = linuxtftp.strip()
        linuxtftp2 = linuxtftp1.strip().strip()
        self.failUnless(linuxtftp2,"Files are not generated on the Linux machine")



        self.ssx.cmd("context cdr-1")
        #res = self.ssx.cmd("copy tftp://17.1.2.1/%s /hd" % linuxtftp2)
	res = self.ssx.ftppasswd("copy sftp://root@%s:/tftpboot/%s /hd/%s noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2,linuxtftp2))
        time.sleep(25)
        self.ssx.shellcmd("cd /hd")
        ttl1= self.ssx.shellcmd("cdrdump -f %s -r 0 | grep \"Record type(0)=SESSION_START\"" % linuxtftp2)
        self.myLog.output(ttl1)
        self.failUnless('Record index too high' not in ttl1, "Record is not generated")


        self.ssx.cmd("context cdr-1")
        self.ssx.cmd("clear session all")
        time.sleep(30)
        self.linux.cmd("cd /tftpboot/")
        linuxtftp = self.linux.cmd("ls -rth | grep \".ttlv\" | tail -n 1")
        linuxtftp1 = linuxtftp.strip()
        linuxtftp2 = linuxtftp1.strip().strip()
        self.failUnless(linuxtftp2,"Files are not generated on the Linux machine")


        #res = self.ssx.cmd("copy tftp://17.1.2.1/%s /hd noconfirm" % linuxtftp2)
	res = self.ssx.ftppasswd("copy sftp://root@%s:/tftpboot/%s /hd/%s noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2,linuxtftp2))
        time.sleep(15)
        self.ssx.shellcmd("cd /hd")
        ttl1= self.ssx.shellcmd("cdrdump -f %s -r 0 | grep \"Record type(5)=CLASS_STOP\"" % linuxtftp2)
        self.myLog.output(ttl1)
	self.failUnless('Record index too high' not in ttl1, "Record is not generated")


#        Out = Verify_class_name_in_cdr_records(self.ssx,record = ttl1,class_name ="icmp_class",test_string="Record type(5)=CLASS_STOP")
#        self.failUnless(Out == 1,"Test case failed due to incorrect class_name parameter in cdr record of class")
      

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
        suite.addTest(test_CDR_FUN_039)
        test_runner(stream=sys.stdout).run(suite)
