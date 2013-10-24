#!/sr/bin/env python2.5
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

DESCRIPTION: Compares Show command CLI output between Laurel and 4.6B2
TEST PLAN:   Laurel Cli
TEST CASES:  Laurel Cli

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 ShowCmdDiff.py"
AUTHOR: Ganapathi 
REVIEWER: 
"""

import sys, os
import  time


mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries 
from SSX import * 
from log import *
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner  
from helpers import is_healthy
from ShowCmdList import *

#from config import *
import pexpect
import re

class test_ShowCmdDiff(test_case):
    """ 
    Description: Compares Show command CLI output between Laurel and 4.6B2
    """

    my_log = getLogger()
    script_var = {}

    # SSX vars

    
    ssx_cfg = """
    system hostname qa-3k-1
     context local
     aaa profile
     user authentication none
     session authentication local
     exit
   interface mgt4 management
    arp arpa
    ip address 10.4.2.21/24
   exit
   interface vlanint
   arp arpa
   arp refresh
   ip address 10.11.1.1/24
   exit
    interface ex1
   arp arpa
  arp refresh
  ip address 1.1.1.1/24
  exit
 ip route 0.0.0.0/0 1.1.1.2
   exit
   port ethernet 0/0
    bind interface mgt4 local
   exit
    enable
   exit
  port ethernet 1/0
  bind interface mgt4 local 
   exit
  enable
  exit
  no port eth 2/0
  no port eth 2/1
  port ethernet 2/0
     bind interface ex1 local
    exit
   enable
   exit
  port ethernet 2/1 dot1q
   vlan 100
   bind interface vlanint local
   exit
  exit
  enable
  exit
  end
    """  %(script_var)

    ssx_cfg1 = """
    system hostname badri
     context local
     aaa profile
     user authentication none
     session authentication local
   exit
   interface mgmt management
    arp arpa
    ip address 172.16.24.45/24
   exit
   no interface vlanint 
   interface vlanint
   arp arpa
   arp refresh
   ip address 10.11.1.2/24
   exit
    interface ex1
   arp arpa
  arp refresh
  ip address 1.1.1.1/24
  exit
 ip route 0.0.0.0/0 1.1.1.2 admin 2
   exit
   port ethernet 0/0
    bind interface mgmt local
   exit
    enable
   exit
  port ethernet 1/0
  bind interface mgmt local 
   exit
  enable
  exit
  no port eth 2/0
  no port eth 2/1
  port ethernet 2/0
     bind interface ex1 local
    exit
   enable
   exit
  port ethernet 2/1 dot1q
   vlan 100
   bind interface vlanint local
   exit
  exit
  enable
  exit
  end
    """  %(script_var)
    
    def setUp(self):

        #Establish a telnet session to SSX with 4.6B2
        self.ssx = SSX("qa-3k-1-mc","root","joe")
        self.ssx.telnet()
        
        #Establish a telnet session to the SSX box with Laurel Image
        self.ssx1 = SSX("badri-mc-con","stoke@local","stoke123")
        self.ssx1.telnet()


    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()
    
    def test_ShowCmdDiff(self):
        """
        Test case Id: -  ShowCmdDiff,
        Description:  -  Script for verifying ShowCmdDiff
        """

        flag = 1
        self.ssx.config_from_string(self.ssx_cfg)
        self.ssx1.config_from_string(self.ssx_cfg1)
        cmd_dict = {}
        for command in cmd_list:
            cmd_dict["%s" %command] = """%s""" %self.ssx1.cmd("%s" %command)
  
        regexhex    = re.compile("0x\w+")
        regexspace  = re.compile("\s+")
        regexdigit  = re.compile("\d+")
        #regexhyphen = re.compile(r"-")
        regexlbrace = re.compile(r"\(")
        regexrbrace = re.compile(r"\)")
        regexrstar  = re.compile(r"\*")
        regexmac    = re.compile("\w+:\w+:\w+:\w+:\w+:\w+")
        weekList = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]
        strList  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","stoke","local","mgmt","Stoke","Unconf","Down","Up","disabled","enabled","KB","MB","all","yes","no"]
        regexpList = []
        for week in weekList:
            list1 = []
            list1.append(re.compile(week))
            list1.append("\w+")
            regexpList.append(list1)
        for mon in strList:
            list1 = []
            list1.append(re.compile(mon))
            list1.append( "\w+")
            regexpList.append(list1)
        for cmd,output in cmd_dict.items():
            regexp = re.sub(regexspace,"\s+",output)
            regexp = re.sub(regexhex,"\w+",regexp)
            regexp = re.sub(regexdigit,"\d+",regexp)
            #regexp = re.sub(regexhyphen,"\-",regexp)
            regexp = re.sub(regexlbrace,"\(",regexp)
            regexp = re.sub(regexrbrace,"\)",regexp)
            regexp = re.sub(regexrstar,"\*",regexp)
            regexp = re.sub(regexmac,"\w+:\w+:\w+:\w+:\w+:\w+",regexp)
            for regVar,sub in regexpList:
                regexp = re.sub(regVar,sub,regexp)
            
            res    = re.compile(regexp)
            str2   = self.ssx.cmd("%s" %cmd)
            m = res.search(str2)
            if m:
                self.my_log.output("************** Matched *********************")
                self.my_log.output("cmd: %s " %cmd)
                self.my_log.output("output: %s" %(m.group()))
                self.my_log.output("************** End *********************")
            else:
                self.my_log.output("************** Not  Matched *********************")
                flag = 0
                self.my_log.output("ERROR: \'%s\' command output changed" %cmd)
                self.my_log.output("Regexp Expected  : %s" %regexp)
                self.my_log.output("output Expected  : %s" %output)
                self.my_log.output("Generated Output : %s" %str2)
                self.my_log.output("***************** End    *********************")
                
        self.failUnless(flag,"Check for \'ERROR\' Key word in log file for commands where output got changed")   




if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_ShowCmdDiff)
    test_runner().run(suite)


