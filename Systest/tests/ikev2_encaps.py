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

DESCRIPTION: To establish ikev2 session between client and server.
TEST PLAN: IKVE2 TEst plans
TEST CASES: 

HOW TO RUN:python2.5 IKEV2_SES_001.py
AUTHOR:Jameer Basha - jameer@stoke.com
REVIEWER: Venkat - krao@stoke.com

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

#import config and topo files
from ikev2_config import *
from topo import *

class test_IKEV2_SES_001(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
        self.client = Linux(ike_clnt["ip_addr"])
        self.server = Linux(radius["ip_addr"])
        #self.linux5 = Linux(linux5["ip_addr"])
        self.client.telnet()
        self.server.telnet()
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
        #Before Closing telnet session lets kill processes that we started
        self.client.cmd("ike reset")
        time.sleep(10)
        self.client.cmd("quit")
        self.server.cmd("sudo pkill radius")
        # Close the telnet session of Xpress VPN Client
        self.client.close()
        self.server.close()
        #self.linux5.close()

    def test_IKEV2_SES_001(self):

        self.myLog.output("\n**********start the test**************\n")

        '''#vgroup operation on SSX ports...
        vport_clnt = clnt_port.replace('/',':')
        vport_svr = srvr_port.replace('/',':')
        #Argument for vgroup API..
        vgrp_str1 = """
                   %s:%s
                   %s:%s
                   """%(ssx["name"],vport1,ike_clnt['hostname'],ike_clnt['interface'])
        vgrp_str2 = """
                   %s:%s
                   %s:%s
                   """%(ssx["name"],vport2,radius['hostname'],radius['interface'])

        #Vgroup b/w SSX, Client and Server...
        vgroup_new(vgrp_str1)
        vgroup_new(vgrp_str2)'''
        
        #Configure SSX..
        self.ssx.config_from_string(script_var['common_config'])
        self.ssx.cmd("save configuration ikev2-common.cfg")
        #self.ssx.config_from_string(script_var['port_config_normal'])
        #Moving to context
        self.ssx.cmd("context %s"%script_var['context_name'])

        #Configure Ips and Routes on client end...
        self.client.configure_ip_interface(port_ssx_client[1],script_var['ike_client_ip_linux/mask'])
        self.client.add_route(script_var['ses_lo_route'],script_var['ike_client_ip_ssx'],port_ssx_client[1])
        self.client.add_route(script_var['svr_route'],script_var['ike_client_ip_ssx'],port_ssx_client[1])       
        self.client.add_route(script_var['ses_route1'],script_var['ike_client_ip_ssx'],port_ssx_client[1])

        #Lets configure autoexec.cfg file
        self.client.cmd("cd /xpm/")
        self.client.write_to_file(script_var['autoexec'],"autoexec.cfg","/xpm/")
        
        #Lets configure add_ip_route...
        self.client.cmd("sudo /sbin/ip addr add dev %s %s/16 brd +"%(port_ssx_client[1],script_var['ip_pool']))
        self.client.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(script_var['ses_lo_ip'],script_var['ike_client_ip_ssx'],port_ssx_client[1],script_var['ip_pool']))
        self.client.cmd("sudo /sbin/route add -net %s gw %s"%(script_var['ses_lo_route'],script_var['ike_client_ip_ssx']))
        self.client.cmd("sudo /sbin/ip route add %s via %s dev %s src %s"%(script_var['ses_route1'],script_var['ike_client_ip_ssx'],port_ssx_client[1],script_var['ip_pool']))
        self.client.cmd("sudo /sbin/ifconfig %s:1 19.1.2.1 netmask 255.255.0.0"%port_ssx_client[1])
        
        # Now configure IPs and Routes on server end...
        self.server.configure_ip_interface(port_ssx_srvr[1],script_var['rad_server_ip_linux/mask'])
        self.server.add_route(script_var['client_route'],script_var['rad_server_ip_ssx'],port_ssx_srvr[1])
        self.server.add_route(script_var['ses_route'],script_var['rad_server_ip_ssx'],port_ssx_srvr[1])

        # Lets kill the processes before starting..
        self.client.cmd("sudo pkill ike")
        self.server.cmd("sudo pkill radius")

        #Start the radiusd...
        #self.server.cmd("sudo touch rad_op.txt")
        self.server.cmd("sudo /usr/local/sbin/radiusd &")

        #Lets repeat for different combinations of port.
        port_client = clnt_port
        vport_clnt = clnt_port.replace('/',':')
	portType = []
        port_svr = []
        portType = ["normal" , "untagged" , "tagged"]
        port_svr = srvr_port
        #port_svr = ["2/1" , "3/1"]
        mtuList = ["100" , "200" , "1400" , "1500"]
        for mtu in mtuList:
                self.client.cmd("sudo /sbin/ifconfig eth1 mtu %s"%mtu)             
                self.myLog.output("\n\n\nVerifying the IKEV2 Sessions for the MTU : %s\n\n\n"%mtu)
	        for port_server in port_svr:
	          vport_svr = port_server.replace('/',':')
	          vgrp_str_svr = "%s:%s %s:%s"%(ssx["name"],vport_svr,radius['hostname'],radius['interface'])
	          vgroup_new(vgrp_str_svr)
	          for port in portType:
        	        #Clear existing port configuration before loading
	                self.ssx.cmd("configuration")
	                #self.ssx.cmd("no port ethernet %s"%script_var['infc_srvr_port'])
	                portList = []
	                portList = ["2/0" ,"2/1","2/2","2/3","3/0","3/1","3/2","3/3","4/0","4/1","4/2","4/3"]
	                for p in portList:
	                        self.ssx.cmd("no port ethernet %s"%p)
	                #self.ssx.cmd("no port ethernet %s"%port_server)
        	        #self.ssx.cmd("no port ethernet %s"%port_client)
	                self.ssx.cmd("exit")

	                # Load port specific configuration...
	                self.ssx.config_from_string(script_var["port_config_%s"%port] %(port_client,script_var['vlanid'],port_server))
	                if port == "tagged":
	                        vgrp_str = "vlan=%s %s:%s,tagged %s:%s"%(script_var['vlanid'],ssx["name"],vport_clnt,ike_clnt['hostname'],ike_clnt['interface'])
	                        vgroup_new(vgrp_str)
	                else:
	                        vgrp_str = "%s:%s %s:%s"%(ssx["name"],vport_clnt,ike_clnt['hostname'],ike_clnt['interface'])
	                        vgroup_new(vgrp_str)

	                if port_server == port_svr[0]:
        	                self.myLog.output("\n\n\n\n Verifying session on Same Card for %s port"%port)
	                        self.myLog.output("port info :\n client port - %s, server port - %s \n\n\n\n"%(port_client,port_server))
	                else:
	                        self.myLog.output("\n\n\n\n Verifying session on Different Card for %s port"%port)
	                        self.myLog.output("port info :\n client port - %s, server port - %s \n\n\n\n"%(port_client,port_server))


        	        # Start ike - Xvpn
	                self.client.cmd("sudo ./start_ike")
	                time.sleep(35)
	                op1 = self.ssx.cmd("show session")
	                self.myLog.output("Session: %s"%op1)
	                self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")
	                self.failIf("Authenticating" in op1, "Session is still Authenticating")
	
	                time.sleep(5)
	                pingSizeList = []
	                pingSizeList = ["46", "64", "128", "256", "512", "1372", "1498", "1500"]
	                for pingSize in pingSizeList:
	                        self.client.cmd("!ping %s -I %s -c %s -s %s -M dont -i 0 -w 1"%(script_var['rad_server_ip_linux'],script_var['ip_pool'],script_var['count'], pingSize))
        	                op = self.client.cmd("!echo $?")
                	        if int(op) != 0:
	                                self.myLog.output("Ping from client to server FAILED for the size: %s"%pingSize)
	
	
	                self.myLog.output("\n\n\n\nshow ip host :  %s\n\n\n"%self.ssx.cmd("show ip host"))
	                host = self.ssx.cmd("show ip host | grep %s"%script_var['ip_pool'])
	                self.myLog.output("show ip host : %s"%self.ssx.cmd("show ip host"))
	                self.failIf("%s"%script_var['infc_clnt_port'] not in host, "IPSEC is not established thru ipsec enabled port")
	
	                #verifying the session counters...
	                self.myLog.output("verifying the session counters after ping walk from client to server")
	                ses_cnt = self.ssx.cmd("show session counters")
	                self.myLog.output("session counters after ping from client to server:\n %s"%ses_cnt)
         	        ses_cnt_rx1 = int(ses_cnt.splitlines()[-1].split()[2])
	                ses_cnt_tx1 = int(ses_cnt.splitlines()[-1].split()[3])
	                self.failIf((ses_cnt_rx1 == 0) & (ses_cnt_tx1 == 0) , "Session counters are not incremented")

	                #PIng from server to client...
	                self.server.cmd("reset")
	                time.sleep(10)
	                for pingSize in pingSizeList:
	                        ping_op = self.server.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1" %(script_var['ip_pool'], script_var['count'], pingSize))
	                        op = self.server.cmd("echo $?")
	                        if int(op) != 0:
	                                self.myLog.output("Ping from server to client FAILED for the size: %s"%pingSize)

	                #Verifying session counters after ping from server to client...
	                self.myLog.output("Verifying session counters after ping from server to client")
	                ses_cnt = self.ssx.cmd("show session counters")
	                self.myLog.output("session counters after ping from server to client: %s\n"%ses_cnt)
	                ses_cnt_rx2 = int(ses_cnt.splitlines()[-1].split()[2])
	                ses_cnt_tx2 = int(ses_cnt.splitlines()[-1].split()[3])
	                self.failIf((ses_cnt_rx2 <= ses_cnt_rx1) & (ses_cnt_tx2 <= ses_cnt_tx1), "Sessions Counters are not incremented after ping")
	
	                #Verifying the REKEY...
	                self.myLog.output("Verifying the REKEY")
	                self.myLog.output("ike-session detail of remote end: \n%s"%self.ssx.cmd("show ike-session detail remote %s"%script_var['ike_client_ip_linux']))
	                rekey1 = self.ssx.cmd("sh ike-session detail remote %s | grep -i \"Child-SA Negotiation Count\""%script_var['ike_client_ip_linux'])
	                time.sleep(int(script_var['soft_lifetime_ph2']) - 30)
	                self.myLog.output("Rekey details after phase2 delay")
        	        self.myLog.output("ike-session detail of remote end: \n%s"%self.ssx.cmd("show ike-session detail remote %s"%script_var['ike_client_ip_linux']))
	                rekey2 = self.ssx.cmd("sh ike-session detail remote %s | grep -i \"Child-SA Negotiation Count\""%script_var['ike_client_ip_linux'])
	                self.failIf(int(rekey2.split()[-1]) <= int(rekey1.split()[-1]), "Rekay is not happened")
	
	                #Verifying traffic after REKEY...
	                self.myLog.output("Verifying ping traffic after REKEY")
	                self.myLog.output("Pinging from client to server")
	                for pingSize in pingSizeList:
	                        self.client.cmd("!ping %s -I %s -c %s -s %s -M dont -i 0 -w 1"%(script_var['rad_server_ip_linux'],script_var['ip_pool'],script_var['count'], pingSize))
	                        op = self.client.cmd("!echo $?")
	                        if int(op) != 0:
	                                self.myLog.output("Ping from client to server FAILED for the size: %s"%pingSize)
	
	                self.myLog.output("Pinging from server to client")
	                for pingSize in pingSizeList:
        	                ping_op = self.server.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1" %(script_var['ip_pool'], script_var['count'], pingSize))
	                        op = self.server.cmd("echo $?")
	                        if int(op) != 0:
        	                        self.myLog.output("Ping from server to client FAILED for the size: %s"%pingSize)

	                #Verifying session counters after ping from server to client and REKEY...
	                self.myLog.output("Verifying session counters after RERKEY and ping from server as well client")
	                ses_cnt = self.ssx.cmd("show session counters")
	                self.myLog.output("session counters after ping from server to client: %s\n"%ses_cnt)
	                ses_cnt_rx3 = int(ses_cnt.splitlines()[-1].split()[2])
	                ses_cnt_tx3 = int(ses_cnt.splitlines()[-1].split()[3])
	                self.failIf((ses_cnt_rx3 <= ses_cnt_rx2) & (ses_cnt_tx3 <= ses_cnt_tx2), "Sessions Counters are not incremented after REKEY and PING")
	

	                # Terminate the ike client...
	                self.client.cmd("ike reset")
	                time.sleep(10)
	                self.client.cmd("quit")
	
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
        suite.addTest(test_IKEV2_SES_001)
        #test_runner().run(suite)
        test_runner(stream=sys.stdout).run(suite)

