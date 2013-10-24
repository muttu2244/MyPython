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

DESCRIPTION: Covers testing hidden commands for Laurel
TEST PLAN:   Laurel Cli
TEST CASES:  Laurel Cli

TOPOLOGY DIAGRAM: 

DEPENDENCIES: None
How to run: "python2.5 Global_cli_002.py"
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
from Linux import *
#from CISCO import *
from log import *
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner  
from helpers import is_healthy
#from config import *
from tek import *
from mdo import *
import pexpect

class test_Global_cli_002(test_case):
    """ 
    Description: tests laurel hidden cli
    """
    my_log = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX("india-mc-con","joe@local","joe")
        self.ssx.telnet()


    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()

    
    
    def test_Global_cli_002(self):
        """
        Test case Id: -  Global_cli_002,
        Description:  -  Script for verifying Global_cli_002
        """

        hidden_cmd_list1 = ["event time cdr 200 action generate-cdr","event volume cdr1 2000 action generate-cdr","diameter attribute nas-ip-address 1.1.1.1","diameter session authentication profile","diameter stack-cfg","diameter strip-domain","cdr","dhcp relay server 1.1.1.1","filter-domain gana","filter-domain gana1","filter-protocol http gana dst-domain gana src-domain gana1","filter gana","class gana"]
        hidden_cmd_list2 = ["class-of-service gana","inbound","100 class gana","exit","outbound","200 class gana","exit","exit"]
        hidden_cmd_list3 = ["ipsec policy ikev1 phase1 name ph1","ipsec policy ikev1  phase2  name ph2","mobile-ip profile pdif"]
        hidden_cmd_list4 = ["ipsec policy ikev2 phase1 name ikev2_phase1","mobike","pdg-3gpp","ttg-3gpp","exit"]
        intf_cmd_list    = ["interface rnc","arp arpa","arp refresh","ip address 21.14.80.1/24","exit","interface rnc1","arp arpa","arp refresh","ip address 21.16.80.1/24","exit","interface gana","arp arpa","arp refresh","ip address 21.15.80.1/24","exit"]
        hidden_cmd_list5 = ["session name gana","ipsec policy ikev1 phase1 name ph1","ipsec policy ikev1 phase1 name ph2","exit","exit"]
        hidden_cmd_list6 = ["tunnel  gana type ipsec protocol ip44 context gana","ipsec policy ikev1  phase1 name ph1","ipsec policy ikev1 phase2 name ph2","exit"]
        hidden_cmd_list7= ["port ethernet 4/0 dot1q","vlan 1300","bind interface rnc gana","ipsec policy ikev1 phase1 name ph1","ipsec policy ikev1 phase2 name ph2","exit","exit","exit"]
        hidden_cmd_list8 = ["port ethernet 4/1 dot1q","vlan 1301 untagged","bind interface rnc1 gana","ipsec policy ikev1 phase1 name ph12","ipsec policy ikev1 phase2 name ph22","exit","exit","exit"]
        hidden_cmd_list9 = ["port ethernet 2/0","bind interface gana gana","ipsec policy ikev1 phase1 name ph13","ipsec policy ikev1 phase2 name ph23","exit","exit"] 
        clear_show_cmds  = ["clear cdr statistics all","clear dhcp counters","clear mobile-ip binding all","clear mobile-ip statistics all","certificate device-certificate delete all","sh cdr statistics all","sh dhcp counters","sh diameter local profile","sh mobile-ip context all","sh certificate device-certificate all"]

        cmd_list = ["event time cdr 200 action generate-cdr","event volume cdr1 2000 action generate-cdr","diameter attribute nas-ip-address 1.1.1.1"," diameter session authentication profile","algorithm first","dest-realm local","max-outstanding 200","exit","diameter stack-cfg","local-identity gana","local-realm gana","local-ip ipv4 1.1.1.1 tcp-port 4546","watch-dog-timer 30","peer-connect-timer 300","cer-timer 41","peer identity gana realm gana","host-addr ipv4 1.1.1.1","transport tcp","sibling gana","exit","exit","diameter strip-domain","cdr","disk-commit-interval 100","upload-profile perf1","directory ex1","file-format asn1","file-format ttlv","file-format xml","include 0-6","interval 200","upload-server 1.1.1.1 protocol sftp username gana password encrypted 1q2w3ein","upload-server 1.1.1.1 port 60 protocol ftp username gana password encrypted 1q2w3ein","exit","exit","dhcp relay server 1.1.1.1","filter-domain gana","ip 1.1.1.1 255.255.255.255","exit","filter-domain gana1","ip 2.2.2.2 255.255.255.255","exit","filter-protocol http gana dst-domain gana src-domain gana1","dscp 63","dst-port gt 76","dst-port lt 76","dst-port neq 76","dst-port range 80 90","established","src-port gt  76","src-port lt 76","src-port neq 76","src-port range 80 90","exit","filter gana","filter-rule 200 gana","exit","class gana","filter gana","exit","class-of-service gana","inbound","100 class gana","event time cdr","exit","exit","outbound","200 class gana","event volume cdr1","exit","exit","exit","ipsec policy ikev1 phase1 name ph1","suite4 psk xauth-chap 300 hours 200 hours","delay-expiry 20","mode-cfg local-type responder","rekey isakmp-only","rekey-responder-window 99","exit","ipsec policy ikev1  phase2  name ph2","custom aes128 md5 group2 300 hours 200 hours","custom aes192 md5 group2 300 hours 200 hours","custom aes256 md5 group2 300 hours 200 hours","custom des md5 group2 300 hours 200 hours","custom null md5 group2 300 hours 200 hours","custom  triple-des md5  group2 300 hours 200 hours","delay-expiry 20","exit","ipsec policy ikev1 phase1 name ph12","suite4 psk xauth-chap 300 hours 200 hours","delay-expiry 20","mode-cfg local-type responder","rekey isakmp-only","rekey-responder-window 99","exit","ipsec policy ikev1  phase2  name ph22","custom aes128 md5 group2 300 hours 200 hours","custom aes192 md5 group2 300 hours 200 hours","custom aes256 md5 group2 300 hours 200 hours","custom des md5 group2 300 hours 200 hours","custom null md5 group2 300 hours 200 hours","custom  triple-des md5  group2 300 hours 200 hours","delay-expiry 20","exit","ipsec policy ikev1 phase1 name ph13","suite4 psk xauth-chap 300 hours 200 hours","delay-expiry 20","mode-cfg local-type responder","rekey isakmp-only","rekey-responder-window 99","exit","ipsec policy ikev1  phase2  name ph23","custom aes128 md5 group2 300 hours 200 hours","custom aes192 md5 group2 300 hours 200 hours","custom aes256 md5 group2 300 hours 200 hours","custom des md5 group2 300 hours 200 hours","custom null md5 group2 300 hours 200 hours","custom  triple-des md5  group2 300 hours 200 hours","delay-expiry 20","exit","ipsec policy ikev2 phase1 name ikev2_phase1","mobike","additional-addrs","return-routability-check interval 2800 retry-interval 300 max-retries 5","exit","exit","ipsec policy ikev2 phase1 name ikev2_phase2","pdg-3gpp auth-method piggyback-authorize","exit","ipsec policy ikev2 phase1 name ikev2_phase3","ttg-3gpp","exit","ipsec policy ikev2 phase1 name ikev2_phase1","pdif-3gpp2","exit","exit","interface rnc","arp arpa","arp refresh","ip address 21.14.80.1/24","exit","interface rnc1","arp arpa","arp refresh","ip address 21.16.80.1/24","exit","mobile-ip profile pdif","agent-advertisement interval 23 maximum 23","mobile-registration-lifetime 34","reverse-tunnel","care-of-interface rnc","home-agent address 1.1.1.1 secure spi 264 key ascii es1 algorithm hmac-md5","mobile-station address 1.1.1.1 secure spi 264 key ascii es1 algorithm hmac-md5","exit","session name gana","ipsec policy ikev1 phase1 name ph1","ipsec policy ikev1 phase1 name ph2","exit","interface gana","arp arpa","arp refresh","ip address 21.15.80.1/24","exit","exit","tunnel  gana type ipsec protocol ip44 context gana","ipsec policy ikev1  phase1 name ph1","exit","ipsec policy ikev1 phase2 name ph2","exit","port ethernet 4/0 dot1q","vlan 1300","bind interface rnc gana","ipsec policy ikev1 phase1 name ph1","ipsec policy ikev1 phase2 name ph2","exit","exit","exit","port ethernet 4/1 dot1q","vlan 1301 untagged","bind interface rnc1 gana","ipsec policy ikev1 phase1 name ph12","ipsec policy ikev1 phase2 name ph22","exit","exit","exit","port ethernet 2/0","bind interface gana gana","ipsec policy ikev1 phase1 name ph13","ipsec policy ikev1 phase2 name ph23","exit","exit"] 
        
        self.my_log.info("**************************Before  Hidden Enable 2 ***********************")
        self.ssx.cmd("ter len infi")
        self.ssx.cmd("ter wid infi")
        self.ssx.cmd("config")
        self.ssx.cmd("cont gana")
        flag = 1
        for cmd in hidden_cmd_list1:
            out = self.ssx.cmd("%s" %cmd)
            if "ERROR:" not in out:
                self.my_log.output("Error: %s : failed" %(cmd))
                flag = 0  
                self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list2:
            out = self.ssx.cmd("%s" %cmd)
            if "class-of-service" not in cmd and "inbound" not in cmd and "outbound" not in cmd and "exit" not in cmd:
                if "ERROR:" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    #self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list3:
            out = self.ssx.cmd("%s" %cmd)
            if "ERROR" not in out:
                self.my_log.output("Error: %s : failed" %(cmd))
                flag = 0   
                self.ssx.cmd("exit") 
        for cmd in intf_cmd_list:
            out = self.ssx.cmd("%s" %cmd)

        for cmd in hidden_cmd_list4:
            out = self.ssx.cmd("%s" %cmd)
            if "ikev2" not in cmd and 'exit' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
 
        for cmd in hidden_cmd_list5:
            out = self.ssx.cmd("%s" %cmd)
            if "session" not in cmd and 'exit' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list6:
            out = self.ssx.cmd("%s" %cmd)
            if "tunnel" not in cmd and 'exit' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list7:
            out = self.ssx.cmd("%s" %cmd)
            if "port" not in cmd and "bind" not in cmd and 'exit' not in cmd and 'vlan' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list8:
            out = self.ssx.cmd("%s" %cmd)
            if "port" not in cmd and "bind" not in cmd and 'exit' not in cmd and 'vlan' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
        for cmd in hidden_cmd_list9:
            out = self.ssx.cmd("%s" %cmd)
            if "port" not in cmd and "bind" not in cmd and 'exit' not in cmd and 'vlan' not in cmd:
                if "ERROR" not in out:
                    self.my_log.output("Error: %s : failed" %(cmd))
                    flag = 0   
                    self.ssx.cmd("exit") 
        for cmd in clear_show_cmds:
            out = self.ssx.cmd("%s" %cmd)
            if "ERROR" not in out:
                self.my_log.output("Error: %s : failed" %(cmd))
                flag = 0   
                self.ssx.cmd("exit") 
        self.ssx.cmd("end")
        self.my_log.info("%s" %self.ssx.cmd("sh conf cont gana"))
        self.ssx.cmd("config")
        self.ssx.cmd("no cont gana")
        self.ssx.cmd("no port eth 4/0 dot1q")
        self.ssx.cmd("no port eth 4/1 dot1q")
        self.ssx.cmd("no port eth 2/0")
        self.ssx.cmd("end")
        
        self.my_log.info("**************************After  Hidden Enable 2 ***********************")
        self.ssx.hidden_cmds_enable(level = 2)
        self.ssx.cmd("config")
        self.ssx.cmd("cont gana")
        for cmd in cmd_list:
            out = self.ssx.cmd("%s" %cmd)
            if "ERROR" in out:
                self.my_log.output("Error: %s : failed" %(cmd))
                flag = 0   
        self.ssx.cmd("end")
        self.my_log.info("%s" %self.ssx.cmd("sh conf cont gana"))
        self.ssx.cmd("cont gana")
        for cmd in clear_show_cmds:
            out = self.ssx.cmd("%s" %cmd)
            if "ERROR" in out:
                self.my_log.output("Error: %s : failed" %(cmd))
                flag = 0   


        self.failUnless(flag,"Check for Keyword Error in log file")




 
        



if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    suite = test_suite()
    suite.addTest(test_Global_cli_002)
    test_runner().run(suite)


