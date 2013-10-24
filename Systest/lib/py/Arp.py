#!/usr/bin/env python2.5
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : APIs related to ARP.This Script contains following ARP APIs which has
                          been used in the PREARP Testcases

TEST PLAN               : PreArp
AUTHOR                  : Rajshekar; email : Rajshekar@stoke.com
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import pexpect
import time
import string
import sys
import re
from logging import getLogger
# grab the root logger.
log = getLogger()

def get_num_of_entries_in_arp_table(self,context="local"):
        """
        Description : API used to get the number of ARP entries in ARP table
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : Below method returns the output from context specified :
                      self.ssx.get_num_of_entries_in_arp_table(context="cont1")
                      Below method returns the output from context local :
                      self.ssx.get_num_of_entries_in_arp_table() 
        ReturnValue : Number of ARP entries in ARP table
        """
        
        self.cmd("end")
        self.cmd("context %s"%context)
        out = self.cmd("show ip arp | count")
        numOfEnt = int(out.split()[1]) - 2
        return numOfEnt

def verify_num_of_entries_in_arp_table(self,count = 0,context="local",exactMatch=0):
        """
        Description : API used to verify  the number of ARP entries in ARP table with or without exact match.
        Arguments   : context : specify context name otherwise it will take default context name i.e local
                      exactMatch : if you want to verify the exact number of ARP entries, its value should be 1
                                   else no need to assign the value it will take default value.
        Example     : verify the exact number of ARP entries :
                      self.ssx.verify_num_of_entries_in_arp_table(count = 10,context="cont1",exactMatch=1)
                      verify the ARP table is not empty :
                      self.ssx.verify_num_of_entries_in_arp_table()
        ReturnValue : On success return value is True else False
        """

        out = get_num_of_entries_in_arp_table(self,context="%s"%context) 
        if exactMatch == 0 :
           if out == 0 :
              return "False"
           else :
              return "True"            
        else :
           if count != out :
              return "False"
           else :
              return "True"

def clear_arp_table(self,context="local",arg="all"):
        """
        Description : API used to clear ARP table
        Arguments   : context : specify context name otherwise it will take default context name i.e local
                      arg : this variable is used for either clearing all arp entries or with ip address
        Example     : self.ssx.clear_arp_table(context="123",arg="all")
                      self.ssx.clear_arp_table(context="123",arg="1.2.3.4")
        ReturnValue : On success return value is True else False
        """

        self.cmd("end")
        self.cmd("context %s"%context)
        out = self.cmd("clear ip arp %s"%arg)
        if "Error" in out :
            return "False"
        else :
            return "True"

def get_arp_table(self,context="local"):
        """
        Description : API used to get the  ARP table
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : self.ssx.get_arp_table(context="cont1")
        ReturnValue : returns the output
        """

        self.cmd("end")
        self.cmd("context %s"%context)
        out = self.cmd("show ip arp")
        return out

def verify_arp_table(self,ipList=[],context="local"):
        """
        Description : API used to verify the ARP resolved for all IP addresses
        Arguments   : context : specify context name otherwise it will take default context name i.e local
                      ipList  : speicfy the ip addresses. Ex : ipList = ["1.2.3.4","1.3.4.5"]
        Example     : ips = ["1.2.3.4","1.3.4.5"]
                      self.ssx.verify_arp_table(ipList=ips,context="123")
        ReturnValue : On success return value is True else False
        """

        fail = 0
        self.cmd("end")
        self.cmd("context %s"%context)        
        for ip in ipList : 
            sleep = 1
            #Wait for 5 seconds,if still the ARP not resolved then make it fail
            waitForTime = 300

            while sleep <= waitForTime:
                out = self.cmd("show ip arp | grep %s"%ip)
                if "resolved" in out :
                   fail = 0
                   break
                else :
                   sleep = sleep + 1                     
                   fail = 1
                   log.info("Arp not resolved for Ip Address %s in %s secs"%(ip,sleep))
        if fail :
            return "False"
        else :
            return "True"

def clear_ip_counters(self,context="local"):
        """
        Description : API used to clear ip counters
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : self.ssx.clear_ip_counters(context="123")
        ReturnValue : On success return value is True else False
        """
        self.cmd("end")
        self.cmd("context %s"%context)
        out = self.cmd("clear ip counter")
        if "Error" in out :
            return "False"
        else :
            return "True"
