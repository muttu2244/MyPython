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

DESCRIPTION: Verify the DM functionality on SSX by sending a DM request from the Radius server using rad client
TEST PLAN: Radius Dynamic Authorization Test Plan
TEST CASES: RDA-FUN-001

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

How to run: "python2.5 CDR_MISC_001.py"
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
from aaa import *
from cdr import *
from ike import *
from misc import *
from scapy import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy

# import configs file
from config import *
from topo import *

# python libraries
import time 

class test_CDR_MISC_001(test_case):
    myLog = getLogger()

    def setUp(self):

        """Establish a telnet session to the SSX box."""
        self.ssx = SSX(topo.ssx['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()
	self.ssx.wait4cards()
        # CLear SSX configuration
	self.ssx.clear_config()



        #Establish a telnet session to the Xpress VPN client box.
        self.xpress_vpn = Linux(topo.linux["ip_addr"],topo.linux["user_name"],
				topo.linux["password"])
        self.xpress_vpn.telnet()

        # Establish a telnet session to the radius servers
        self.radclient_radius1 = Linux(xpress_vpn2_multi['ip_addr'],xpress_vpn2_multi['user_name'],
				xpress_vpn2_multi['password'])
        self.radclient_radius1.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client and radius server
        self.xpress_vpn.close()
	self.radclient_radius1.close()

    def test_CDR_MISC_001(self):
        """
        Test case Id: -  CDR_MISC_001
        Description: - Verify the DM functionality on SSX, 
		by sending a DM request from the Radius server using radclient.
	"""

        self.myLog.output("\n**********start the test**************\n")

        #Clearing already existing files on the linux machine
        self.xpress_vpn.cmd("cd ~krao")
        self.xpress_vpn.cmd("sudo rm -rf *.asn1")
        self.xpress_vpn.cmd("sudo rm -rf *.xml")
        self.xpress_vpn.cmd("sudo rm -rf *.ttlv")

        self.xpress_vpn.cmd("cd /tftpboot/")
        #self.linux.cmd("sudo rm *.*")
        self.xpress_vpn.cmd("sudo rm -rf *.asn1")
        self.xpress_vpn.cmd("sudo rm -rf *.xml")
        self.xpress_vpn.cmd("sudo rm -rf *.ttlv")


        #configuring interface on linux machine
        #self.xpress_vpn.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])
        self.radclient_radius1.configure_ip_interface(ssx_vgroup1[1], script_var['radius1_ip_mask'])


        #Vgrouping the Topology 
        vgroup_new(vlan_cfg_str1)

        # Push xpress vpn config on linux
        #self.xpress_vpn.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        #self.xpress_vpn.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")


        # Push SSX config
        self.ssx.config_from_string(script_var['CDR_MISC_001'])

        # Push xpress vpn config
        self.xpress_vpn.write_to_file(script_var['autoexec_config_EAP'],"autoexec.cfg","/xpm/")
        self.xpress_vpn.write_to_file(script_var['add_ip_takama'],"add_ip_takama","/xpm/")

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        self.xpress_vpn.cmd("sudo chmod 777 add_ip_takama")
        self.xpress_vpn.cmd("sudo ./add_ip_takama")


        # Enable debug logs for RDA
        self.ssx.cmd("clear log debug")
	self.ssx.cmd("context %s" % script_var['context_name'])
	self.ssx.cmd("debug module aaad radius-dynamic-authorization")
	self.ssx.cmd("clear radius dynamic-authorization counters")

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpress_vpn.cmd("cd /xpm/")
        op_client_cmd = self.xpress_vpn.cmd("sudo ./start_ike")
	time.sleep(10)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        time.sleep(10)
        self.failUnless("IPSECv4" in op1,"Failed because there is no session of IPSEC")
        self.xpress_vpn.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.xpress_vpn.cmd("quit")


        ## Check weather IPsec session established or not  
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpress_phy_iface1_ip'])
        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"IPsec session didnot established")
    


        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Waiting for 30 seconds to get the files generated on the linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

        time.sleep(30)

        #self.xpress_vpn.cmd("ls -rth /tftpboot/ | grep \".ttlv\" ")
        self.xpress_vpn.cmd("ls -rth ~krao | grep \".xml\"")


	# Initiate a DM request
        radclient_output = self.radclient_radius1.cmd('sudo echo "Acct-Session-Id=%s" | radclient  -x %s:3799 disconnect topsecret'%(ssx_show_op['session_handle'],script_var['ssx_radius1_ip']),timeout=30)
        self.failUnless("Disconnect-ACK" in radclient_output,"SSX did not respond with Disconnect-ACK")


	time.sleep(30)
        #self.xpress_vpn.cmd("ls -rth /tftpboot/ | grep \".ttlv\" ")
        self.xpress_vpn.cmd("ls -rth ~krao | grep \".xml\"")

        # verify in RDA counters 
        self.ssx.cmd("context %s" % script_var['context_name'])
        rda_attr = self.ssx.cmd("show radius dynamic-authorization counters")

        result = verify_rda_counters_disconnect(self,rda_attr,accept="1",removed="1",reject="0")
        self.failUnless(result,"Error in SSX RDA counters")

        # Checking weather the session are cleared are not After sending DM
        show_output = self.ssx.cmd("show ike-session brief")
        self.failUnless("ERROR" in show_output,"session not cleared even after sending the DM")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

    logfile=__file__.replace('.py','.log')
    log = buildLogger(logfile, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_CDR_MISC_001)
    test_runner(stream=sys.stdout).run(suite)
    
