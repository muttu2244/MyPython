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

DESCRIPTION: Verify that the Absolute-Timeout attribute can be modified after the session has been established, using CoA request
TEST PLAN: Radius Dynamic Authorization Test Plan
TEST CASES: RDA-HA-005

TOPOLOGY DIAGRAM:

    (Linux)                      (SSX)                        (Linux)
    -------                      --------                   --------------
   |Takama | -------------------|        |-----------------| qa-svr4      |
    -------                     |        |                  --------------
                                |Lihue-mc|
  (Netscreen)                   |        |                     (Linux)
    ------                      |        |                  --------------
   |qa-ns1 | -------------------|        |-----------------| qa-svr3      |
    ------                      |        |                  --------------
                                 --------

How to run: "python2.5 CDR_HA_FUN_002.py"
AUTHOR:	Raja Rathnam -rathnam@primesoftsolutionsinc.com
REVIEWER: Venkat - kvv.rao@primesoftsolutionsinc.com
"""


### Import the system libraries we need.
import sys, os

### To make sure that the libraries are in correct path.
mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


# frame-work libraries
from Linux import Linux
from SSX import SSX
from cdr import *
from rtc import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

#import configs file
from config import *
from topo import *

#import private libraries
from ike import *
from misc import *
import time 

class test_CDR_HA_FUN_002(test_case):
    myLog = getLogger()

    def setUp(self):

        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(ssx_HA['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

        # CLear SSX configuration
	self.ssx.clear_config()
        self.ssx.wait4cards()

        #Establish a telnet session to the Xpress VPN client box.
        self.linux = Linux(linux["ip_addr"],linux["user_name"],
				linux["password"])
        self.linux.telnet()

        #Establish a telnet session to the RADIUS server box.
	self.radius1=Linux(xpress_vpn2_multi['ip_addr'],xpress_vpn2_multi['user_name'],xpress_vpn2_multi['password'])
        self.radius1.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client and radius server
        self.linux.close()
        self.radius1.close()

    def test_CDR_HA_FUN_002(self):
        """
        Test case Id: -  CDR_HA_FUN_002
	"""

        self.myLog.output("\n**********start the test**************\n")

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
        self.radius1.configure_ip_interface(ssx_vgroup1[1], script_var['radius1_ip_mask'])


	#Vgrouping the Topology 
	vgroup_new(vlan_cfg_str1)

        # Push xpress vpn config on linux
        self.linux.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        self.linux.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")

        # Push SSX config
        self.ssx.config_from_string(script_var['CDR_FUN_039'])


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd")
        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")
        time.sleep(5)

        op_client_cmd = self.linux.cmd("sudo ./start_ike")
        time.sleep(5)
        op1 = self.ssx.configcmd("show session")
        #self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")


        self.linux.cmd("!ping %s -I %s -w 4 -c 4" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux.cmd("quit")

        #Displaying the saved configuration
        saved_conf =  self.ssx.cmd("show configuration cdr")
        self.myLog.output(saved_conf)


        #Executing IMC-Switc-Over
	self.ssx.imc_switchover_mgmt("system imc-switchover")

        time.sleep(60)


        #Check for ttlv files using CDR dump tool
        self.linux.cmd("cd /tftpboot/ | grep \".ttlv\"")
        linuxtftp = self.linux.cmd("ls -rth /tftpboot/ | grep \".ttlv\" | tail -n 1")
        linuxtftp1 = linuxtftp.strip()
        linuxtftp2 = linuxtftp1.strip().strip()
        self.myLog.info(linuxtftp1)
        self.myLog.info(linuxtftp2)
        self.failUnless(linuxtftp2,"Files are not generated on the Linux machine")

        self.ssx.cmd("context local")
        res = self.ssx.ftppasswd("copy sftp://root@%s:/tftpboot/%s /hd/%s noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2,linuxtftp2))
        time.sleep(20)

        #self.ssx.shellcmd("cd /hdp/cdr/cdr-1/customer")
        self.ssx.shellcmd("cd /hd")

        ttl1 =  self.ssx.shellcmd("ls -rth | grep .ttlv | tail -n -1")
        ttl2 = ttl1.split("\n")
        ttl3 =  ttl2[1]

        ttl2= self.ssx.shellcmd("cdrdump -f %s -r 0"%ttl3)
        self.myLog.output(ttl2)

        Out = Verify_service_class_name_in_cdr_records(self.ssx,record = ttl2,service_class_name ="icmp_policy",test_string="tag(28)=SERVICE_CLASS_NAME")
        self.failUnless(Out == 1,"Test case failed due to incorrect service_class_name parameter in cdr record of class")


        Out = Verify_class_name_in_cdr_records(self.ssx,record = ttl2,class_name ="icmp_class",test_string="tag(30)=CLASS_NAME")
        self.failUnless(Out == 1,"Test case failed due to incorrect class_name parameter in cdr record of class")
	
        Out = Verify_ses_id_in_cdr_records(self.ssx,record = ttl2,test_string="SESSION_ID")
        #self.failUnless(Out == 1,"Test case failed due to incorrect session-id parameter in cdr record of session")

        Out = Verify_ses_username_in_cdr_records(self.ssx,record = ttl2,test_string="SESSION_USERNAME")
        #self.failUnless(Out == 1,"Test case failed due to incorrect session-USERNAME parameter in cdr record of session")

        Out = Verify_ses_ipaddr_in_cdr_records(self.ssx,record = ttl2,rem_ip="7.7.2.1",test_string="SESSION_IP_ADDR")
        #self.failUnless(Out == 1,"Test case failed due to incorrect session-id parameter in cdr record of session")



        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,IMC_Switch=1,Card_Reset=1), "Platform is not healthy")



if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_CDR_HA_FUN_002)
    test_runner().run(suite)
    
