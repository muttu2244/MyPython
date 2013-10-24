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

DESCRIPTION:
TEST PLAN:DHCP HIGH AVAILABILITY Test plans
TEST CASES: DHCP-HA-00

TOPOLOGY DIAGRAM:

	-------------------------------------------------------------------------

         -------------------------------------------------------------------------
HOW TO RUN:python2.5 DHCP_HA_003.py

"""
import sys, os, time

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

class test_DHCP_HA_003(test_case):
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

    def test_DHCP_HA_003(self):

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
        self.ssx.config_from_string(script_var['DHCP_HA_003'])

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

	Ip_out = get_ipaddr(self.linux2,p1_ssx_linux2[1])
        Start_addr_out = script_var['client_ip_range_start'].split(".")[3]
        Start_addr = int(Start_addr_out)
        End_addr_out = script_var['client_ip_range_end'].split(".")[3]
        End_addr  = int(End_addr_out)
        self.failIf(int(Ip_out.split(".")[3]) not in range(Start_addr,End_addr))

        # Verifying the HA 
  
        self.ssx.cmd("exit")
        self.ssx.reload_device()        
        self.ssx.cmd("terminal length infinite")
        self.ssx.cmd("terminal width infinite")
        a = self.ssx.cmd("show configuration")
        self.failIf("context %s"%script_var['context_name'] not in a)
        
        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs, Card_Reset = 1), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_DHCP_HA_003)
        test_runner(stream=sys.stdout).run(suite)

