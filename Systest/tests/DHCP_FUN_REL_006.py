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

DESCRIPTION:To verify SSX (relay agent) relays the DHCP reply message from  many DHCP subscribers to DHCP server . 
TEST PLAN: Sanity Test plans
TEST CASES: DHCP-FUN-REL-006

TOPOLOGY DIAGRAM:

        -------------------------------------------------------------------------
                          LINUX                       SSX  

       |                                             context -A                 |
       |         Trans  IP = 2.1.1.1/24 ---------- > TransIP = 2.1.1.2/24       |
                        eth1                             port-4/0 
         -------------------------------------------------------------------------


HOW TO RUN:python2.5 DHCP-FUN-REL-006.py
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

#import configs file
from dhcp_config import *
from  topo import *

class test_DHCP_FUN_006(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux1 = Linux(linux1["ip_addr"])
	self.linux2 = Linux(linux2["ip_addr"])
	self.linux3 = Linux(linux3["ip_addr"])
	self.linux1.telnet()
	self.linux2.telnet()
	self.linux3.telnet()
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
	self.linux3.close()

    def test_DHCP_FUN_006(self):

        self.myLog.output("\n**********start the test**************\n")

	#vgroup b/w SSX and linux.
        #vg_output1 = vgroup_new(topo1[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
        #vg_output1 = vgroup_new(topo3[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")

	# Push SSX config
        self.ssx.config_from_string(script_var['DHCP_FUN_006'])

        #configure ip interface on DHCP  server side.
        self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['infc_server1_ip_addr/mask'])

        #adding routes 
        self.linux1.add_route(script_var['ssx_client_ip_mask'],script_var['ssx_server1_ip_addr'],p1_ssx_linux1[1])

	#Changing to server directory and writing necessary configuraion into config file
        self.linux1.cmd("cd /dhcp-4.0.0b3/server/")
        self.linux1.cmd("sudo rm -f  dhcpd.conf")
        self.linux1.write_to_file(script_var['fun_004_dhcpserver1'],"dhcpd.conf","/dhcp-4.0.0b3/server/")

	 #Killing dhcp processes on server side.
        self.linux1.cmd("sudo pkill dhcpd")
        self.linux1.cmd("sudo pkill dhclient")

        self.linux1.cmd("cd /dhcp-4.0.0b3/server/")
        op_client_cmd = self.linux1.cmd("sudo ./dhcpd -cf dhcpd.conf -lf le %s"%p1_ssx_linux1[1])

	  #Killing dhcp processes on clients side.
        if not (linux1["ip_addr"] == linux2['ip_addr']):
               self.linux2.cmd("sudo pkill dhcpd") 
               self.linux2.cmd("sudo pkill dhclient")
        if not (linux1["ip_addr"] == linux3['ip_addr']):
               self.linux3.cmd("sudo pkill dhcpd")
               self.linux3.cmd("sudo pkill dhclient")

        self.linux3.cmd("PATH=$PATH:/sbin")

        #Changing into client directory on client side.
        self.linux2.cmd("cd /dhcp-4.0.0b3/")
        self.linux2.cmd("sudo chmod 777 client")
        self.linux2.cmd("cd client")
        self.linux3.cmd("cd /dhcp-4.0.0b3/")
        self.linux3.cmd("sudo chmod 777 client")
        self.linux3.cmd("cd client")


	#Changing context and displaying DHCP counters
	self.ssx.cmd("context %s"%script_var['context_name'])
	self.ssx.cmd("clear dhcp counters")

	#Removing the tethereal capture file if its present      
	self.linux1.cmd("sudo rm -f dhcp.pcap")


	self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.output("\n Initiate DHCP client on first linux machine\n")
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")


	#Capturing the packets on remote Linux and running dhcpclient on client side
	outstr=self.linux1.cmd("sudo /usr/sbin/tethereal -i '%s' -q -w dhcp.pcap -R bootp &" %(p1_ssx_linux1[1]))
	op_client_cmd = self.linux2.cmd("sudo ./dhclient %s" %p1_ssx_linux2[1])
	
	#killing the tethreal process on remopte m/c
        self.linux1.cmd("sudo pkill tethereal")

	#reading the tethreal capture file
        outstr = self.linux1.cmd("sudo /usr/sbin/tethereal -r dhcp.pcap")

	#verifying DHCP messages.
	#self.failIf("Offer" not in outstr.split())
        self.failIf("ACK" not in outstr.split())

	  #Verifying the IP address assigned to the client 
        Ip_out = get_ipaddr(self.linux2,p1_ssx_linux2[1])
        Start_addr_out = script_var['client_ip_range_start'].split(".")[3]
        Start_addr = int(Start_addr_out)
        End_addr_out = script_var['client_ip_range_end'].split(".")[3]
        End_addr  = int(End_addr_out)

        self.failIf(int(Ip_out.split(".")[3]) not in range(Start_addr,End_addr))

	#chaging context and displaying Dhcp counters
        self.ssx.cmd("context %s"%script_var['context_name'])
        Counters_out = self.ssx.cmd("show dhcp counters")
	self.myLog.output(Counters_out)

	#grepping client and server Dhcp counters on SSX.
        Client_out = self.ssx.cmd("show dhcp counters | grep client")
        Server_out = self.ssx.cmd("show dhcp counters | grep server1")


        self.failIf((int(Client_out.split()[3]) == 1 )| (int(Client_out.split()[5]) ==1))
        self.failIf((int(Server_out.split()[2]) == 1 )| (int(Server_out.split()[4]) ==1))
 

	 #Changing context and displaying DHCP counters
        self.ssx.cmd("context %s"%script_var['context_name'])
        self.ssx.cmd("clear dhcp counters")

        #Removing the tethereal capture file if its present      
        self.linux1.cmd("sudo rm -f dhcp.pcap")
	Infc_out = p1_ssx_linux3[1]

	self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.output("\n Initiate DHCP client on second linux machine\n")
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")



        #Capturing the packets on DHCP server side. 
	#Initiating dhcpclient on client side
        outstr = self.linux1.cmd("sudo /usr/sbin/tethereal -i '%s' -q -w dhcp.pcap -R bootp &" %(p1_ssx_linux1[1]))
        op_client_cmd = self.linux3.cmd("sudo ./dhclient %s"%Infc_out,timeout=100)

        #killing the tethreal process on DHCP server side.
        self.linux1.cmd("sudo pkill tethereal")

        #reading the tethreal capture file
        outstr = self.linux1.cmd("sudo /usr/sbin/tethereal -r dhcp.pcap")

        #verifying DHCP messages.
        #self.failIf("Offer" not in outstr.split())
        self.failIf("ACK" not in outstr.split())
	
        #chaging context and displaying Dhcp counters
        self.ssx.cmd("context %s"%script_var['context_name'])
        Counters_out = self.ssx.cmd("show dhcp counters")
	self.myLog.output(Counters_out)

        #grepping client and server Dhcp counters on SSX.
        Client_out = self.ssx.cmd("show dhcp counters | grep client")
        Server_out = self.ssx.cmd("show dhcp counters | grep server")


        self.failIf((int(Client_out.split()[3]) == 1 )| (int(Client_out.split()[5]) ==1))
        self.failIf((int(Server_out.split()[2]) == 1 )| (int(Server_out.split()[4]) ==1))

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


	      	   
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_DHCP_FUN_006)
    test_runner().run(suite)

