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
TEST PLAN : DHCP CLI test plans
TEST CASES : DHCP_CLI_001, DHCP_CLI_008,DHCP_CLI_010,DHCP_CLI_011, DHCP_CLI_012,
DHCP_CLI_013,DHCP_CLI_014,DHCP_CLI_015.
TOPOLOGY DIAGRAM:

	-------------------------------------------------------------------------
                          LINUX                       SSX  

       |			    	 	     context -A			|
       |         Trans  IP = 2.1.1.1/24	---------- > TransIP = 2.1.1.2/24	|
			eth1	                         port-4/0 
         -------------------------------------------------------------------------
HOW TO RUN:python2.5 DHCP_CLI_TESTCASES.py

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

class test_DHCP_CLI_TESTCASES(test_case):
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

    def test_DHCP_CLI_TESTCASES(self):

        self.myLog.output("\n**********start the test**************\n")
        #var1=topo1[0]+" "+topo1[1]
        #self.linux5.cmd("PATH=$PATH:/volume/labtools/util")
        #self.linux5.cmd("vgroup %s" % var1)
        #var2=topo2[0]+" "+topo2[1]
        #self.linux5.cmd("vgroup %s" % var2)
        #vgroup b/w SSX and linux.
        #vg_output1 = vgroup_new(topo1[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

        
	# Push SSX config
        self.ssx.config_from_string(script_var['DHCP_CLI_TESTCASES'])

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
        print "is this outstr printing"+outstr
        #time.sleep(300)
	#Verifying the required DHCP messages from tethreal capture file on dhcp client side	   
	#self.failIf("Discover" not in outstr.split())
	self.failIf("Request" not in outstr.split())

	Ip_out = get_ipaddr(self.linux2,p1_ssx_linux2[1])
        Start_addr_out = script_var['client_ip_range_start'].split(".")[3]
        Start_addr = int(Start_addr_out)
        End_addr_out = script_var['client_ip_range_end'].split(".")[3]
        End_addr  = int(End_addr_out)
        self.failIf(int(Ip_out.split(".")[3]) not in range(Start_addr,End_addr))


        # Save the SSX configuration
        self.ssx.cmd("exit")
        self.ssx.cmd("delete stoke.cfg")
        self.ssx.cmd("configuration save")
        self.ssx.cmd("context %s"%script_var['context_name'])


        # Checking the DHCP related CLI commands
        # This is for test case DHCP_CLI_001
        a = self.ssx.cmd("show configuration | grep ERROR:")
        self.failIf("ERROR:" in a.split())
        a = self.ssx.cmd("show dhcp counters")
        self.failIf("ERROR:" in a.split())
        self.failIf("Relay" not in a.split())
        a = self.ssx.cmd("clear dhcp counters")
        self.failIf("ERROR:" in a.split())
        a = self.ssx.cmd("show port")
        self.failIf("ERROR:" in a.split())
        a = self.ssx.cmd("show context")
        self.failIf("%s"%script_var['context_name'] not in a.split())
        a = self.ssx.cmd("show context all")
        self.failIf("local" not in a.split())
        a = self.ssx.cmd("show dhcp server all")
        self.failIf("Address" not in a.split())
        a = self.ssx.cmd("show ip interface")
        self.failIf("%s"%script_var['ssx_client_ip_addr/mask'] not in a.split())
        self.failIf("Up" not in a.split())

        # Verifying the test case DHCP_CLI_008 - Verify DHCP relay option command.
      
        a = self.ssx.cmd("show dhcp opt82")
        self.failIf("Enable" not in a.split())
        # Now disable the DHCP relay option and verify
        
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("interface server1")
        self.ssx.cmd("no dhcp relay option")
        self.ssx.cmd("exit")
        self.ssx.cmd("interface client")
        self.ssx.cmd("no dhcp relay option")
        self.ssx.cmd("end")
        a = self.ssx.cmd("show dhcp opt82")
        self.failIf("Disable" not in a.split())


        # Verifying the test case DHCP_CLI_010 - Verify the configured DHCP parameters can be deleted.
 
        self.ssx.cmd("exit")
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("interface server1")
        a = self.ssx.cmd("no arp arpa")
        self.failIf("ERROR:" in a.split())
        #a = self.ssx.cmd("no dhcp relay option")
        self.failIf("ERROR:" in a.split())
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")
        a = self.ssx.cmd("no port ethernet %s"%script_var['infc_client1_port'])
        self.failIf("ERROR:" in a.split())
        self.ssx.cmd("end")        


        # Verifying the test case DHCP_CLI_011 - Verify the configured DHCP parameters can be modified.

        self.ssx.cmd("exit")
        self.ssx.cmd("load configuration stoke.cfg")
        # Verifying the DHCP_CLI_o11
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("interface server1")
        a = self.ssx.cmd("no dhcp relay option")
        b = self.ssx.cmd("dhcp relay") 
        self.failIf("ERROR:" in a.split())
        self.failIf("ERROR:" in b.split())
        self.ssx.cmd("end")


        # Verifying the test case DHCP_CLI_012 - Verify that SSX displays error message when parameters are mis-configured.

        self.ssx.cmd("exit")
        self.ssx.cmd("load configuration stoke.cfg")
        # Verifying the DHCP_CLI_012
        self.ssx.cmd("configuration")
        self.ssx.cmd("context %s"%script_var['context_name'])
        a = self.ssx.cmd("dhcp relay server 0.0.0.0")
        self.failIf("ERROR:" not in a.split())
        a = self.ssx.cmd("dhcp relay server 255.255.255.255")
        self.failIf("ERROR:" not in a.split())
        a = self.ssx.cmd("dhcp relay server 0.1.23.2")
        self.failIf("ERROR:" not in a.split())
        a = self.ssx.cmd("dhcp relay server 256.20.20.20")
        self.failIf("ERROR:" not in a.split())
        self.ssx.cmd("interface server1")
        a = self.ssx.cmd("dhcp option")
        self.failIf("ERROR:" not in a.split())
        self.ssx.cmd("end")


        # Verifying test case DHCP_CLI_013 - Verify all the DHCP related debug commands.

        self.ssx.cmd("exit")
        self.ssx.cmd("load configuration stoke.cfg")
        # Verifying the DHCP_CLI_013
        self.ssx.cmd("context %s"%script_var['context_name'])
        a = self.ssx.cmd("show context | grep dhcp")
        b = a.split()
        self.ssx.cmd("debug context %s"%b[1])
        self.ssx.cmd("debug slot 2")
        self.ssx.cmd("debug check all")
        self.ssx.cmd("debug hold")
        a = self.ssx.cmd("show debug")
        self.failIf("Hold" not in a.split())
        self.ssx.cmd("debug go")
        a = self.ssx.cmd("show debug")
        self.failIf("Hold" in a.split())

        #Verifying the test cases DHCP_CLI_014 and DHCP_CLI_015 
        #Verify that SSX allows maximum five DHCP servers to be configured
        # in a context And Verify that SSX allows deleting a DHCP server
        #  and adding a new DHCP server.

        self.ssx.cmd("exit")
        self.ssx.cmd("configuration")
        self.ssx.cmd("context test")
        self.ssx.cmd("dhcp relay server 1.1.1.1")
        self.ssx.cmd("dhcp relay server 1.1.1.2")
        self.ssx.cmd("dhcp relay server 1.1.1.3")
        self.ssx.cmd("dhcp relay server 1.1.1.4")
        self.ssx.cmd("dhcp relay server 1.1.1.5")
        a = self.ssx.cmd("dhcp relay server 1.1.1.6")
        self.failIf("ERROR:" not in a.split())
        self.ssx.cmd("no dhcp relay server 1.1.1.1")
        a = self.ssx.cmd("dhcp relay server 1.1.1.6")
        self.failIf("ERROR:" in a.split())
        self.ssx.cmd("exit")
        self.ssx.cmd("exit")


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
        suite.addTest(test_DHCP_CLI_TESTCASES)
        test_runner(stream=sys.stdout).run(suite)

