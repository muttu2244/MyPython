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

DESCRIPTION:Send UDP traffic flood after IKEv2 session is established and check that session is not dropped and re-key happens

TEST PLAN:IP-ATTACK test plans
TEST CASEID:ip_atk_076

TOPOLOGY DIAGRAM:

       --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            2.2.2.3/24  ---------------->     2.2.2.45/24                       |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------


HOW TO RUN:python2.5 ip_atk_076.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:Sudama@primesoftsolutionsinc.com

"""
import sys, os, time

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import Linux
from SSX import SSX
from StokeTest import *
from log import buildLogger
from logging import getLogger
from misc import *
from helpers import is_healthy,diff_in_time_ssx


#import configs file
from topo import *
from ip_atk_config import *
from ike import *

class test_ip_atk_076(test_case):
    myLog = getLogger()	

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        #Establish a telnet session to the xpressvpn1 client box.
        self.xpressvpn1 = Linux(xpressvpn1["ip_addr"],xpressvpn1["user_name"],xpressvpn1["password"])
        self.xpressvpn1.telnet()
	self.linux1 = Linux(linux1["ip_addr"],linux1["user_name"],linux1["password"])
	self.linux1.telnet()
	# wait for card to come up 
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of xpressvpn1 Client
	self.xpressvpn1.close() 
	self.linux1.close()

	time.sleep(60)
	time.sleep(60)
    def test_ip_atk_076(self):



	self.myLog.output("\n**********start the test**************\n")

	#vgroup b/w SSX and XPRESSVPN.
	vgroup_new(vgroup_cfg_dos1)	
        #vgroup code
        vgroup_new(vgroup_cfg_dos)


	#Push the SSX configuration     
        self.ssx.config_from_string(script_var['common_ssx_ikev2'])
        self.ssx.config_from_string(script_var['DOS_FUN_076'])
        self.xpressvpn1.configure_ip_interface(p1_ssx1_xpressvpn1[1],script_var['xpressvpn1_phy_iface1_ip_mask'])


	    #Ping operation.
	self.ssx.cmd("context %s"%script_var['context_name'])
        time.sleep(50)
	Ping_out = self.ssx.ping(script_var['xpressvpn1_phy_iface1_ip'])
        self.failUnless(Ping_out == 1,"no connectivity b/w ssx and linux")


         #Capturing slot from port
        p1_ssx_linux1_slot = p1_ssx_linux1[0].split("/")[0]

	ssx_ph2_life = 60

	 #clearing ip,sys and port counters and displaying ip,sys and port counters 
        self.ssx.cmd("context test")

        self.ssx.cmd("clear ip counters ")
        self.myLog.output("IP counters exist on SSX:%s"%self.ssx.cmd("show ip counters"))

        self.ssx.cmd("clear syscount")
        self.myLog.output("System counters exist on SSX:%s"%self.ssx.cmd("show syscount"))

        self.ssx.cmd("clear port %s counters drop"%script_var['ssx_port'])
        self.myLog.output("Port counters exist on SSX:%s"%self.ssx.cmd("show port %s counters drop"%script_var['ssx_port']))

	
        # Push xpress vpn config on linux
        self.xpressvpn1.write_to_file(script_var['fun_014_xpressvpn'],"autoexec.cfg","/xpm/")

        #clearing sessions on ssx
        self.ssx.cmd("clear session all")

        # Initiate IKE Session from Xpress VPN Client (takama)
        self.xpressvpn1.cmd("cd /xpm")
	self.xpressvpn1.cmd("sudo ./add_ip_takama_qos-ashu") #copy this file from takama box to xpressvpn1 if not existing
        op_client_cmd = self.xpressvpn1.cmd("sudo ./start_ike",timeout = 200)


	 # Check SA in SSX with the remote 
        ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpress_phy_iface1_ip'])

        self.failUnless("ESTABLISHED" in ssx_show_op["session_state"],"failed to find SA")

        # Wait for SSX ph2 life-time

        time_diff = 0
        time.sleep(1)
        self.linux1.cmd("sudo /usr/sbin/hping3 -2 -p 22 %s --flood &"%(script_var['ssx_phy_iface1_ip_mask']),timeout = 150)
        while time_diff <= ssx_ph2_life:
          show_clock_op = self.ssx.cmd("show clock")
          time_diff = diff_in_time_ssx(ssx_show_op['child_sa_time_established'],show_clock_op)

        time.sleep(10)
	ssx_show_op = parse_show_ike_session_detail(self.ssx,script_var['xpress_phy_iface1_ip'])
        self.failUnless(int(ssx_show_op['child_sa_negotiation_count'])==2, "child-sa negotiation count didn't incriment: ph1 rekey failed, The output is: %s" % ssx_show_op['child_sa_negotiation_count'])

	#Flooding UDP traffic.	
	self.linux1.cmd("sudo pkill -9 hping")

	# displaying ip,sys and port counters And process Cpu utilization
	self.myLog.output("Displaying control plane rate limiter %s"%self.ssx.cmd("show dos slot %s counters"%p1_ssx_linux1_slot))
        self.myLog.output("IP counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show ip counters"))
        self.myLog.output("System counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show syscount"))
        self.myLog.output("Port counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show port %s counters drop"%script_var['ssx_port']))
        Cpu_out = self.ssx.cmd("show process cpu slot %s"%((p1_ssx1_xpressvpn1[0].split("/"))[0]))
        self.myLog.output(Cpu_out)

        self.failUnless("100.00%" not in Cpu_out)

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs,Warn_logs = 100), "Platform is not healthy")
if __name__ == '__main__':

         if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
         filename = os.path.split(__file__)[1].replace('.py','.log')
         log = buildLogger(filename, debug=True, console=True)
         suite = test_suite()
         suite.addTest(test_ip_atk_076)
         test_runner(stream=sys.stdout).run(suite)

