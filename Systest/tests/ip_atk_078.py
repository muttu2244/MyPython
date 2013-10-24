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

DESCRIPTION:Send UDP traffic flood after IKEv1 session is established 
TEST PLAN:IP-ATTACK test plans
TEST CASEID:ip_atk_078

Topology Diagram          :

                (qa-ns1)                            (Lihue)
                 ----------                        ----------
                |          |             port :3/1|          |
                |  NS-5GT  |----------------------|   SSX    |
                |          |                      |          |
                 ----------                        ----------




HOW TO RUN:python2.5 ip_atk_078.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:Sudama@primesoftsolutionsinc.com

"""
import sys, os, time

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import frame-work libraries
from Linux import Linux
from SSX import SSX
from StokeTest import *
from log import buildLogger
from logging import getLogger
from NS import NS
from misc import *
from helpers import is_healthy,diff_in_minutes
#import config and topo file
from topo import *
from ip_atk_config import *
from ike import *

class test_ip_atk_078(test_case):
    myLog = getLogger()	

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1["ip_addr"])
        self.ssx.telnet()

	#Establish a telnet session to the Netscreen.
        self.ns5gt = NS(ns['ipaddr'])
        self.ns5gt.telnet()
	# Inserting the code of Linux1 object -- Ashu
	#Establish a telnet session to the linux1 client box.
        self.linux1 = Linux(linux1["ip_addr"],linux1["user_name"],
                                        linux1["password"])
        self.linux1.telnet()

        #clear the configuration on Netscreen
        self.ns5gt.clear_config()


        # Clear the SSX config
   #     self.ssx.clear_config()


	# wait for card to come up 
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of Netscreen
	self.ns5gt.close()
	#Inserting code of linux1 -- Ashu
	# Close the telnet session of linux1 Client
        self.linux1.close()



    def test_ip_atk_078(self):


	self.myLog.output("\n**********start the test**************\n")

	#vgroup b/w SSX and linux
	vgroup_new(vgroup_cfg_dos)

	#vgroup b/w SSX and NS5.
	vgroup_new(vgroup_cfg_dos2)

	 #Get the configuration from a string in a config file config.py and Load it in SSX.
        self.ssx.config_from_string(script_var['common_ssx_for_ikev1'])
        self.ssx.config_from_string(script_var['ikev1_fun_019_ssx'])

	 #Push the SSX configuration     
        self.ssx.config_from_string(script_var['DOS_FUN_017'])

        #Configure interface on linux.
        self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['linux1_ip_addr/m'])

	 #Ping operation.
        self.ssx.cmd("context %s"%script_var['context_name'])
        time.sleep(5)
        Ping_out = self.ssx.ping(script_var['linux1_ip_addr'])
        self.failUnless(Ping_out == 1,"no connectivity b/w ssx and linux")


         #Capturing slot from port
        p1_ssx_linux1_slot = p1_ssx_linux1[0].split("/")[0]
	

        #Get the configuration from a string in a config file config.py and Load it in NS-5GT.
        self.ns5gt.config_from_string(script_var['common_ns5gt'])
        self.ns5gt.config_from_string(script_var['ikev1_fun_019_ns5gt'])


        # Enable debug logs for iked
        self.ssx.cmd("context %s" %script_var['context_name'])
	
        self.ssx.cmd("clear ip counters ")
        self.myLog.output("IP counters exist on SSX:%s"%self.ssx.cmd("show ip counters"))

        self.ssx.cmd("clear syscount")
        self.myLog.output("System counters exist on SSX:%s"%self.ssx.cmd("show syscount"))

        self.ssx.cmd("clear port %s counters drop"%script_var['ssx_port'])
        self.myLog.output("Port counters exist on SSX:%s"%self.ssx.cmd("show port %s counters drop"%script_var['ssx_port']))

	
        self.ssx.cmd("debug module iked all")
        #Flush the debug logs in SSX, if any
        self.ssx.cmd("clear log debug")

        #Give Ping from ns5gt to SSX.
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless( ping_output, "PINGING IS FAILED")
        time.sleep(10)

	 #Delay for 30 seconds
        self.myLog.output("Sleeping for 30 seconds....")
        delay=30
        time.sleep(delay)

        #Check out the SA status in SSX
        self.ssx.cmd("context %s"%script_var['context_name'])
        sa_output=sa_check(self.ssx, script_var['ns_phy_ip'])

        #Getting sa establish time
        sa_grep=verify_in_sa(self.ssx,script_var['ns_phy_ip'], "established")
        self.failUnless(sa_grep, "Not found 'established' in SA")
        est_time=re.search(r"Phase1 time established       : (.*) (\d+):(\d+):(\d+)",sa_grep)

        #Sleeping until  phase2 life time expires
        self.myLog.output("Sleeping for until phase2 life time expires............................")
        time.sleep(180-delay)

        #Verifying in debug messages for the keyword IKED_PH2_LIFETIME_EXPIRED
        exp_log=verify_in_debug(self.ssx,"IKED_PH2_LIFETIME_EXPIRED")
        exp_time=re.search(r"(.*) (\d+):(\d+):(\d+)",exp_log)

        #Getting the time difference between establish time and expiry time
        time_diff=diff_in_minutes(int(exp_time.group(2)),int(exp_time.group(3)),int(exp_time.group(4)),int(est_time.group(2)),int(est_time.group(3)),int(est_time.group(4)))

        self.failUnless(time_diff <= 3, "PH2 was not expired according to the ssx SA lifetime")

        #Testing Ping through the tunnel
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        ping_output=self.ns5gt.ping(script_var['ssx_ses_ip'],source="untrust")
        self.failUnless(ping_output,"Ping is Failed")

        #Verifying for negotiation count
        rekey=verify_in_sa(self.ssx,script_var['ns_phy_ip'], "\"Phase2 Negotiation Count      : 2\"")
        self.failUnless(rekey, "Rekey failed, Hence Test Failed")


	#Flooding traffic after establishing ikev1 session
	self.linux1.cmd("Hping -2 -p22 %s --flood &"%script_var['ssx_ip_addr'])
	time.sleep(40)
	self.linux1.cmd("sudo pkill -9 hping")

	 # displaying ip,sys and port counters And process Cpu utilization

	self.myLog.output("Displaying control plane rate limiter %s"%self.ssx.cmd("show dos slot %s counters"%p1_ssx_linux1_slot))
	
        self.myLog.output("IP counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show ip counters"))

        self.myLog.output("System counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show syscount"))

        self.myLog.output("Port counters exist on SSX after flooding traffic:%s"%self.ssx.cmd("show port %s counters drop"%script_var['ssx_port']))

        Cpu_out = self.ssx.cmd("show process cpu slot %s"%((p1_ssx_linux1[0].split("/"))[0]))
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
         suite.addTest(test_ip_atk_078)
         test_runner(stream=sys.stdout).run(suite)

