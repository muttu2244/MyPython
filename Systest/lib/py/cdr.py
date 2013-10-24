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


import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import time
import string
import sys
import re
from logging import getLogger
log = getLogger()
from StokeTest import test_case
def compare_ip_ssx(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
        array_ip_ssx = []
        for line in mib2[:n]:
           st1=re.search("\w+\:\s+(\d+\.\d+\.\d+\.\d+).*",line)
           if st1:
            st2="."+st1.group(1)
            array_ip_ssx.append(st2)
           else:
            log.info("No Ip's found on the card")
        return array_ip_ssx[:]

def compare_ip_linux(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
#        array_ip_linux = []
        for line in mib2[:n]:
           st1=re.search("\<\w+\>(\d+).*",line)
           if st1:
            st2=st1.group(1)
            st3=st2.replace("0",".")
            return st3
           #  array_ip_linux.append(st3)
          # else:
          #  return 0
          # print ("No files generated on the server")



def compare_usr_ssx(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
        array_user_ssx = []
        for line in mib2[:n]:
           st1=re.search("\w+\:\s+\w+\s+\w+\:\s+(\w+\@+\w+\-\w+)",line)
           #st1=re.search("\w+\:\s+\w+\s+\w+\:\s+(\w+\@+\w+)",line)
           if st1:
             st2=st1.group(1)
             array_user_ssx.append(st2)
           else:
             log.info("No User's found on the card")
        return array_user_ssx[:]



def compare_usr_linux(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
       # array_user_linux = []
        for line in mib2[:n]:
           st1=re.search("\<\w+\>(\w+\@+\w+\-\w+)\<\.*",line)
           if st1:
             st2=st1.group(1)
             return st2
          # else:
          #   print ("No files generated on the server")
       


def compare_cos_linux(self,mib):
        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
        array_user_linux = []
        for line in mib2[:n]:
           st1=re.search("\<\w+\>(\w+\_\w+).*",line)
           if st1:
             st2=st1.group(1)
             return st2
          # else:
          #   print ("No files generated on the server")


def compare_cos_ssx(self,mib):
        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
        array_user_linux = []
        for line in mib2[:n]:
           st1=re.search("\w+\s+\w+\:\s+(\w+\_\w+).*",line)
           if st1:
             st2=st1.group(1)
             array_user_linux.append(st2)
          # else:
          #   print ("No files generated on the server")
        return array_user_linux[:]
 
def compare_cosId_ssx(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
        array_user_linux = []
        for line in mib2[:n]:
           st1=re.search("\w+\s+\w+\:\s+\w+\_\w+\s+\((\d+)\)",line)
           if st1:
             st2=st1.group(1)
             array_user_linux.append(st2)
          # else:
          #   print ("No files generated on the server")
        return array_user_linux[:]


def compare_cosId_linux(self,mib):

        mib1=mib.strip()
        mib2=mib1.split("\r\n")
        n=len(mib2)
      #  array_user_linux = []
        for line in mib2[:n]:
           st1=re.search("\<+\w+\>(\d+).*",line)
           if st1:
             st2=st1.group(1)
             return st2
          # else:
          #   print ("No files generated on the server")


def change_clock_ssx(self,new_clock):

        new_clock1=re.search("\w+\s+(\w+\s+\d+\s+\d+)\s+\.*" , new_clock)
        new_clock2 = new_clock1.group(1)
        nc = new_clock2.split()
        nc1=nc[0].replace("Jan","01")
        nc2=nc[2]+nc1+nc[1]
        return nc2
