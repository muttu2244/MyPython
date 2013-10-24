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

DESCRIPTION:send fragment with large offset.

TEST PLAN:IP-ATTACK test plans
TEST CASEID:ip_atk_010
***************************************This code doesnt represent actual test case ************************
TOPOLOGY DIAGRAM:

       --------------------------------------------------------------------------------

       |                LINUX                            SSX            
       |            2.2.2.3/24  ---------------->     2.2.2.45/24                       |
       |                                                                                |
       |              e1                                         Port 2/1               |
         --------------------------------------------------------------------------------

HOW TO RUN:python2.5 ip_atk_010.py
AUTHOR:rajshekar@primesoftsolutionsinc.com
REVIEWER:Sudama@primesoftsolutionsinc.com

"""

import sys, os, time

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# frame-work libraries
from Linux import *
from SSX import *
from scapy import *
from StokeTest import *
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
from pexpect import *
from misc import *

#import configs file
from topo import *
from ip_atk_config import *

class test_ip_atk_010(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()

        # Clear the SSX config
        self.ssx.clear_config()

        # checking the ssx health status
        self.ssx.clear_health_stats()

        #Establish a telnet session to the Linux.
        self.lin_obj1 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj2 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj3 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj4 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj5 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj6 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])

        self.lin_obj7 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj8 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj9 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj10 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj11 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])
        self.lin_obj12 = Linux(topo.linux1["ip_addr"],topo.linux1["user_name"],topo.linux1["password"])

        self.lin_obj1.telnet()
        self.lin_obj2.telnet()
        self.lin_obj3.telnet()
        self.lin_obj4.telnet()
        self.lin_obj5.telnet()
        self.lin_obj6.telnet()
        self.lin_obj7.telnet()
        self.lin_obj8.telnet()
        self.lin_obj9.telnet()
        self.lin_obj10.telnet()
        self.lin_obj11.telnet()
        self.lin_obj12.telnet()

    def tearDown(self):

        # Close the telnet session of SSX
                self.ssx.close()    

        # Close the telnet session of Linux 
                self.lin_obj1.close()
                self.lin_obj2.close()
                self.lin_obj3.close()
                self.lin_obj4.close()
                self.lin_obj5.close()
                self.lin_obj6.close()
                self.lin_obj7.close()
                self.lin_obj8.close()
                self.lin_obj9.close()
                self.lin_obj10.close()
                self.lin_obj11.close()
                self.lin_obj12.close()
    def test_ip_atk_010(self):

        self.myLog.output("\n->->->->->->->-> START TEST <-<-<-<-<-<-<-<-\n")

        # Push SSX config to create user
        self.ssx.config_from_string(script_var['common'])

        ssh_output=self.lin_obj1.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to SSH to SSX for 1 st ssh")

        ssh_output=self.lin_obj2.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to SSH to SSX for 2 nd ssh")

        ssh_output=self.lin_obj3.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to SSH to SSX for 3 rd ssh")

        ssh_output=self.lin_obj4.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to SSH to SSX for 4 th ssh")

        ssh_output=self.lin_obj5.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to SSH to SSX for 5 th ssh")

        ssh_output=self.lin_obj6.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to Telnet to SSX for 1 st telnet")

        ssh_output=self.lin_obj7.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to Telnet to SSX for 2 nd telnet")

        ssh_output=self.lin_obj8.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to Telnet to SSX for 3 rd telnet")

        ssh_output=self.lin_obj9.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to Telnet to SSX for 4 th telnet")

        ssh_output=self.lin_obj10.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(ssh_output,"Unable to Telnet to SSX for 5 th telnet")

        ssh_output=self.lin_obj11.ssh(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(not ssh_output,"SSH to SSX is Allowed even more than 10 of (ssh + telnet)")

        ssh_output=self.lin_obj12.telnet2ssx(ssx_name,ssh_user,ssh_user_pass)
        self.failUnless(not ssh_output,"Telnet to ssx is allowed for more than 10 of (ssh+ telnet)")

        # Check the SSX health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


if __name__ == '__main__':

         if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
         filename = os.path.split(__file__)[1].replace('.py','.log')
         log = buildLogger(filename, debug=True, console=True)
         suite = test_suite()
         suite.addTest(test_ip_atk_010)
         test_runner(stream=sys.stdout).run(suite)

