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

DESCRIPTION:Send IP header filled with total length=10 to SSX. Repeat the test with MIN, MAX and Average and Random values of the length
TEST PLAN:IP-ATTACK test plans
TEST CASEID:ip_atk_004

TOPOLOGY DIAGRAM:

       --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            2.2.2.3/24  ---------------->     2.2.2.45/24                       |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------

HOW TO RUN:python2.5 ip_atk_004.py
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
from helpers import is_healthy
from scapy import *
from ip_slowpath import *
from misc import *
#import configs file
from topo import *
from ip_atk_config import *

class test_ip_atk_004(test_case):
    myLog = getLogger()	

    def setUp(self):
        #Establish a telnet session to the SSX box.
	self.ssx = SSX(ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        #self.ssx.clear_config()

        #Establish a telnet session to the linux1 client box.
        self.linux1 = Linux(linux1["ip_addr"],linux1["user_name"],
					linux1["password"])
        self.linux1.telnet()
        
	#Establish a telnet session to the linux2 client box. For vgroup --Ashu
	self.linux2 = Linux(linux2["ip_addr"],linux2["user_name"],
						linux2["password"])
        self.linux2.telnet()
	
	# wait for card to come up 
	self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):
	# Close the telnet session of SSX
	self.ssx.close()    
	# Close the telnet session of linux1 Client
	self.linux1.close()
	# Close the telnet session of linux2 Client-- Ashu
	self.linux2.close()

    def test_ip_atk_004(self):


	self.myLog.output("\n**********start the test**************\n")


	#vgroup b/w SSX and linux
	# Commenting two lines below for removing the vgroup code-Ashu
	vgroup_new(vgroup_cfg_dos)	
        #Push the SSX configuration
	self.ssx.config_from_string(script_var['DOS_FUN_005'])
	#Debug By Ashu - 5/15/2008 9:34:00 AM
	print " *************SSX configuration pushed*******************"
	#Debug End
	self.linux1.configure_ip_interface(p1_ssx_linux1[1],script_var['linux1_ip_addr/m'])

	#Capturing slot from port
        p1_ssx_linux1_slot = p1_ssx_linux1[0].split("/")[0]

	#Ping operation.
        self.ssx.cmd("context %s"%script_var['context_name'])
        time.sleep(5)
	Ping_out = self.ssx.ping(script_var['linux1_ip_addr'])
	time.sleep(5)
	Ping_out = self.ssx.ping(script_var['linux1_ip_addr'])
        self.failUnless(Ping_out == 1,"no connectivity b/w ssx and linux")

	self.ssx.cmd("clear log debug")
	#clearing ip,sys and port counters
        self.ssx.cmd("context %s"%script_var['context_name'])
	 
       	self.ssx.cmd("clear ip counters ")
        self.myLog.output("IP counters exist on SSX:%s"%self.ssx.cmd("show ip counters"))

        self.ssx.cmd("clear syscount")
        self.myLog.output("System counters exist on SSX:%s"%self.ssx.cmd("show syscount"))

        self.ssx.cmd("clear port %s counters drop"%script_var['ssx_port'])
        self.myLog.output("Port counters exist on SSX:%s"%self.ssx.cmd("show port %s counters drop"%script_var['ssx_port']))


	"""this API will return the mac_address of directly connected port of
           SSX machine to linux machine which runs scapy which takes
           slot/port as argumnet   """

	slot_port = p1_ssx_linux1[0]
	print slot_port
	dst_mac_address = get_mac_address(self.ssx,port=slot_port)
	print dst_mac_address
      
	dst_ip_adr = script_var['linux1_ip_addr']
	
        #sending packets with header total length 10
        invoke_scapy(self.linux1,dst_mac_adr = dst_mac_address,sudo_passwd=linux1['password'],dst_ip_adr = dst_ip_adr ,from_interface=p1_ssx_linux1[1],ip_hdr_len = 10,log = self.myLog)


        #displaying ip,port and syscounters and Cpu utilization

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
         suite.addTest(test_ip_atk_004)
         test_runner(stream=sys.stdout).run(suite)

