#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke Networks.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke Networks. and may only
# be used under a license from Stoke.
#
#######################################################################

Description: Verify All DHCP Daemons test cases.
TEST PLAN:DHCP Daemons Test plans
TEST CASES: DHCP_DMN_001
            DHCP_DMN_002
            DHCP_DMN_003
            DHCP_DMN_004
            DHCP_DMN_005
            DHCP_DMN_008
            DHCP_DMN_009
            DHCP_DMN_010
            DHCP_DMN_011
            DHCP_DMN_012

Note : The test cases DHCP_DMN_006, 007, 013, 014 are not autoamted since they are not
       scheduled because relay-proxy is not implemented.

TOPOLOGY DIAGRAM:
     |-----------------|    
     |  Linux machine  | e1           2/0 SSX   2/1       e1   Linux Machine
     |     Cali        |<--------------> Easter <---------->     Cyclops
     |  DHCP Server    |                Relay                  DHCP Client
     |-----------------|                 
HOW TO RUN:python2.5 DHCP_DMN_CASES.py

"""
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from Linux import *
from dhcp import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *

#import dhcp_config and topo file
from dhcp_config import *
from  topo import *

class test_DHCP_DMN_CASES(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.linux1 = Linux(linux1["ip_addr"])
        self.linux2 = Linux(linux2["ip_addr"])
        #self.linux5 = Linux(linux5["ip_addr"])
        self.linux1.telnet()
        self.linux2.telnet()
        #self.linux5.telnet()
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
        # Close the telnet session of Xpress VPN Client
        self.linux1.close()
        self.linux2.close()
        #self.linux5.close()

    def test_DHCP_DMN_CASES(self):

        self.myLog.output("\n**********start the test**************\n")
        var1=topo1[0]+" "+topo1[1]
        #self.linux5.cmd("PATH=$PATH:/volume/labtools/util")
        #self.linux5.cmd("vgroup %s" % var1)
        var2=topo2[0]+" "+topo2[1]
        #self.linux5.cmd("vgroup %s" % var2)
        #vgroup b/w SSX and linux.
        #vg_output1 = vgroup_new(topo1[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")


        # Push SSX config
        self.ssx.config_from_string(script_var['DHCP_DMN_CASES'])

        #configure ip interface on linux machine
        self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['infc_server1_ip_addr/mask'])

        #adding route
        self.linux1.add_route(script_var['ssx_client_ip_mask'],script_var['ssx_server1_ip_addr'],p1_ssx_linux1[1])

        # Writing dhcp configuration into corresponding file on server side.
        self.linux1.cmd("cd /dhcp-4.0.0b3/server/")
        self.linux1.cmd("sudo rm -f  dhcpd.conf")
        self.linux1.write_to_file(script_var['fun_004_dhcpserver1'],"dhcpd.conf","/dhcp-4.0.0b3/server/")

        #Killing process regarding dhcp on server side.
        self.linux1.cmd("sudo pkill dhcpd")
        self.linux1.cmd("sudo pkill dhclient")


        self.linux1.cmd("cd /dhcp-4.0.0b3/server/")
        op_client_cmd = self.linux1.cmd("sudo ./dhcpd -cf dhcpd.conf -lf le %s"%p1_ssx_linux1[1])
        self.linux2.cmd("sudo pkill dhclient")
        self.linux2.cmd("sudo pkill dhcpd")
        self.linux2.cmd("sudo pkill dhclient")
        self.linux2.cmd("cd /dhcp-4.0.0b3/")
        self.linux2.cmd("sudo chmod 777 client")
        self.linux2.cmd("cd client")

        #Changing context
        self.ssx.cmd("context %s"%script_var['context_name'])

        #Capturing the packets on dhcp server and running dhcpclient on client side
        outstr=self.linux1.cmd("sudo /usr/sbin/tethereal -i '%s' -q -w dhcp.pcap -R bootp &" %(p1_ssx_linux1[1]))
        op_client_cmd = self.linux2.cmd("sudo ./dhclient %s"%p1_ssx_linux2[1],timeout = 150)

        #killing the tethreal process on remopte m/c
        self.linux1.cmd("sudo pkill tethereal")

        #reading the tethreal capture file
        outstr=self.linux1.cmd("sudo /usr/sbin/tethereal -r dhcp.pcap")
        #print "is this outstr printing"+outstr
        #time.sleep(300)
        #Verifying the required DHCP messages from tethreal capture file on dhcp client side
        #self.failIf("Discover" not in outstr.split())
        self.failIf("Request" not in outstr.split())

        # Verifying the test case DHCP_DMN_001 - Verify that when a context is created, it is registered with the DHCPD-MC.

        # Verifying the DHCP_DMN_001 - Verify that when a context is created, it is registered with the DHCPD-MC.

        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")       
        self.ssx.cmd("debug module dhcpdmc all")
        a = self.ssx.cmd("show debug")
        self.failIf("dhcpdmc" not in a.split())
        self.myLog.output("\n Registered the context with DHCPD-MC \n")

        
	# Verifying the test case DHCP_DMN_002 - Verify that when a context configuration is changed, it is updated with the DHCPD-MC. 

        self.ssx.cmd("exit")
        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name']) 
        self.ssx.cmd("dhcp relay server 1.1.1.1")
        a = self.ssx.cmd("show log tail 500 | grep DHCPdMC")
        b = a.split("\n")
        self.failIf("Relay-add:" not in a.split())
        self.myLog.output("\n When context configuration is changed, it is updated with the DHCPD-MC")


        # Verifying the test case DHCP_DMN_003 - Verify that when a context is deleted, it is unregistered with the DHCPD-MC.

        #self.ssx.cmd("configuration")
        #self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("no dhcp relay server 1.1.1.1")
        a = self.ssx.cmd("show log tail 123 | grep DHCPdMC | grep Relay-del")
        self.failIf("Relay-del:" not in a.split())
        self.myLog.output("\n When context is deleted, it is unregistered with the DHCPD-MC")
        self.ssx.cmd("end")
        self.ssx.cmd("exit")


        # Verifying the test case DHCP_DMN_004  & DHCP_DMN_005 - Verify that when an interface is configured as DHCP relay agent, it is registered with the DHCPD-MC.
        # DHCP_DMN_005 - Verify that that when in an interface, DHCP relay agent 
        # functionality is disabled, it is updated with the DHCPD-MC.

        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("interface server1")
        self.ssx.cmd("no dhcp relay")
        a = self.ssx.cmd("show log tail 123 | grep %s"%script_var['context_name'])
        self.failIf("DHCPdMC-CFG_INTF_RELAY:" not in a.split())
        self.failIf("disable:" not in a.split())
        self.myLog.output("\n\n DHCP_DMN_005 - disabling of DHCP relay agent, it is updated with the DHPD-MC\n\n")
        self.ssx.cmd("dhcp relay")
        a = self.ssx.cmd("show log tail 123 | grep %s"%script_var['context_name'])
        self.failIf("DHCPdMC-CFG_INTF_RELAY:" not in a.split())
        self.failIf("enable:" not in a.split())
        self.myLog.output("\n\n DHCP_DMN_004 - enabling of DHCP relay agent, it is updated with the DHPD-MC\n\n")
        self.ssx.cmd("end")
        self.ssx.cmd("exit")

        # Test CAses DHCP-DMN-006 & DHCP_DMN_007 are based on DHCP relay-proxy it is not yet implemented.


        # Verifying the test case DHCP_DMN_008 - Verify that when context is crerated,
        # DHCPD-LC is updated with the information by DHCPD-MC.

        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("no debug module dhcpdmc all")
        self.ssx.cmd("debug module dhcpdmc context")
        self.ssx.cmd("debug module dhcpdlc context")
        self.ssx.cmd("debug module dhcpdmc ipc")
        self.ssx.cmd("debug module dhcpdlc ipc")
        # ----------- DHCP_DMN_008 ---------
        a = self.ssx.cmd("show debug")
        #self.failIf("Module dhcpdlc group ipc." not in a.split("\n"))
        self.failIf("ipc." not in a.split())
        a = self.ssx.cmd("show dhcp ipc message | grep CtxCreate | grep DHCPd_MC")
        self.failIf("SND" not in a.split())
        self.myLog.output("\n--------- The test case DHCP_DMN_008 is verified ---------\n")
        # ----------- DHCP_DMN_009 ---------
        a = self.ssx.cmd("show dhcp ipc message | grep DHCPd_MC | grep IntfUpdate")
        self.failIf("SND" not in a.split())
        self.myLog.output("\n--------- The test case DHCP_DMN_009 is verified ---------\n")

        # ----------- DHCP_DMN_010 ---------
        self.ssx.cmd("exit")
        self.ssx.cmd("delete stoke.cfg")
        self.ssx.cmd("save configuration")
        self.ssx.clear_config()
        a = self.ssx.cmd("show dhcp ipc message | grep CtxDelete | grep DHCPd_MC")
        print a
        self.failIf("SND" not in a.split())
        a = self.ssx.cmd("show dhcp ipc message | grep CtxDelete | grep CtxMgr")
        print a
        self.failIf("RX" not in a.split())
        self.myLog.output("\n--------- The test case DHCP_DMN_010 is verified ---------\n")


        # ----------- DHCP_DMN_011 ---------
     
        self.ssx.cmd("load configuration stoke.cfg") 
        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        #self.ssx.cmd("load configuration stoke.cfg")
        a = self.ssx.cmd("show log debug | grep DHCPdMC-CFG_INTF_RELAY:")
        self.failIf("enable:" not in a.split())
        self.myLog.output("\n--------- The test case DHCP_DMN_011 is verified ---------\n")


        # ----------- DHCP_DMN_012 ---------

        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("interface server1")
        self.ssx.cmd("no dhcp relay")
        a = self.ssx.cmd("show log debug | grep DHCPdMC-CFG_INTF_RELAY:")
        self.failIf("disable:" not in a.split())
        self.ssx.cmd("end")
        self.ssx.cmd("exit")
        self.myLog.output("\n--------- The test case DHCP_DMN_012 is verified ---------\n")

 
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DHCP_DMN_CASES)
        test_runner(stream=sys.stdout).run(suite)


