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

DESCRIPTION:To verify SSX (relay agent) relays the DHCP reply message from  many DHCP subscribers to DHCP server.
 
TEST PLAN: Sanity Test plans
TEST CASES: DHCP-FUN-REL-024

TOPOLOGY DIAGRAM:

        --------------------------------------------------------------------------------
       |                LINUX                            SSX                            |
       |         Trans  IP = 2.1.1.1/24                  TransIP = 2.1.1.2/24           |
       |                               -------------->                                  |
       |                     ETH1                                   Port 3/0            |
         --------------------------------------------------------------------------------

HOW TO RUN:python2.5 DHCP-FUN-REL-024.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:himanshu@primesoftsolutionsinc.com

"""
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import SSX
from Linux import *
from dhcp import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from misc import *

#import dhcp_configs file
from dhcp_config import *
from  topo import *

class test_DHCP_FUN_024(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1 = Linux(linux1["ip_addr"])
	self.linux2 = Linux(linux2["ip_addr"])
	self.linux1.telnet()
	self.linux2.telnet()
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

    def test_DHCP_FUN_024(self):

        self.myLog.output("\n**********start the test**************\n")
	        #vgroup b/w ssx and host
        #vg_output1 = vgroup_new(topo1[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")


	# Push SSX config
        self.ssx.config_from_string(script_var['DHCP_FUN_024'])

        #configure ip interface on linux machine
        self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['infc_server1_ip_addr/mask'])

        #adding route 
        self.linux1.add_route(script_var['ssx_client_ip_mask'],script_var['ssx_server1_ip_addr'],p1_ssx_linux1[1])

        self.linux1.cmd("sudo pkill dhcpd")
        self.linux1.cmd("sudo pkill dhclient")

	 #Changing context and displaying DHCP counters
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("clear dhcp counters")

	self.linux1.cmd("cd /dhcp-4.0.0b3/server/")

	self.linux1.cmd("sudo pkill dhcpd")
	self.linux1.cmd("sudo pkill dhclient")

        #Removing the tethereal capture file if its present      
        self.linux1.cmd("sudo rm -f dhcp.pcap")

	Hwaddr_out = get_hwaddr(self.linux2,p1_ssx_linux2[1])
	script_var['hwaddr'] = Hwaddr_out
	script_var['fun_004_dhcpserver1'] = """
	ddns-update-style ad-hoc;
	ddns-update-style interim;
	shared-network %(infc_server1_ip_range)s-%(ssx_client_ip_range)s {
	subnet %(infc_server1_ip_range)s netmask %(infc_server1_ip_mask)s {
	}
	subnet %(ssx_client_ip_range)s netmask  %(infc_client_ip_mask)s {
	}
	  #option domain-name-servers ns1.internal.example.org;
	pool{
	  range %(client_ip_range_start)s %(client_ip_range_end)s;
	  option domain-name "internal.example.org";
	  option routers %(infc_client_ip_addr)s ;
	  option broadcast-address 16.0.0.255;
	  default-lease-time 1;
	  max-lease-time 2;
	}
	host xyz{
	 fixed-address 20.20.20.202;
	hardware ethernet %(hwaddr)s ;
	default-lease-time 1;
	}
		}
	""" %(script_var)

	self.linux1.write_to_file(script_var['fun_004_dhcpserver1'],"dhcpd.conf","/dhcp-4.0.0b3/server/")
	op_client_cmd = self.linux1.cmd("sudo ./dhcpd -cf dhcpd.conf -lf le %s"%p1_ssx_linux1[1])



        #Capturing the packets on remote Linux and running dhcpclient on client side
        outstr=self.linux1.cmd("sudo /usr/sbin/tethereal -i '%s' -q -w dhcp.pcap -R bootp &" %(p1_ssx_linux1[1]))
	
        
	self.linux2.cmd("cd /dhcp-4.0.0b3/client/")

        op_client_cmd = self.linux2.cmd("sudo ./dhclient %s"%p1_ssx_linux1[1],timeout=250)
	time.sleep(20)
	
        #killing the tethreal process on remopte m/c
        self.linux1.cmd("sudo pkill tethereal")


        #reading the tethreal capture file
        outstr = self.linux1.cmd("sudo /usr/sbin/tethereal -r dhcp.pcap")
	self.failIf("Discover" not in outstr.split())
	self.failIf("Offer" not in outstr.split())
	self.failIf("ACK" not in outstr.split())
        self.failIf("Request" not in outstr.split())

	

        #chaging context and displaying Dhcp counters
	self.linux1.cmd("sudo pkill tethereal")
        self.ssx.cmd("context %s"%script_var['context_name'])
        Counters_out = self.ssx.cmd("show dhcp counters")
	Counters_out = Counters_out.split("\n")[6]

 

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


	      	   
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_DHCP_FUN_024)
    test_runner().run(suite)

