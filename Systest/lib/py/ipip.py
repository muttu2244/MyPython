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
DESCRIPTION             : This Script contains following IPIP  APIs which has
                          been used in the SANITY Testcases

TEST PLAN               :  Test plan
AUTHOR                  : 
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

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






def verify_tunnel_counters(self,tun1="none",tun2="none",in_pkts='none'):
	k = self.cmd("show tunnel counters | grep %s "%(tun1))
        actual_in_pkts1 =k.split()[2]
        k=self.cmd("show tunnel counters | grep %s"%(tun2))
        actual_in_pkts2 = k.split()[2]
        if int(actual_in_pkts1) == in_pkts and  int(actual_in_pkts2) == int(actual_in_pkts1):
        	return 1 
       	else:   
       		return 0        

def verify_tunnel_counters1(self,tun1="none",in_pkts='none'):
        k = self.cmd("show tunnel counters | grep %s "%(tun1))
        actual_in_pkts1 =k.split()[2]
        #k=self.cmd("show tunnel counters | grep %s"%(tun2))
        #actual_in_pkts2 = k.split()[2]
        if int(actual_in_pkts1) ==int(in_pkts):
                return 1
        else:
                return 0



def verify_multipletunnel_counters(self,tun1="none",tun2="none",in_pkts='none',tun11='none',tun21='none'):
         k = self.cmd("show tunnel counters | grep %s "%(tun1))
         actual_in_pkts1 =k.split()[2]
         k=self.cmd("show tunnel counters | grep %s"%(tun2))
         actual_in_pkts2 = k.split()[2]
         k = self.cmd("show tunnel counters | grep %s "%(tun11))
         actual_in_pkts11 =k.split()[2]
         k=self.cmd("show tunnel counters | grep %s"%(tun21))
         actual_in_pkts21 = k.split()[2]


         if int(actual_in_pkts1) ==int(in_pkts) and int(actual_in_pkts2)==int(actual_in_pkts1) and int(actual_in_pkts11)==in_pkts and int(actual_in_pkts21)==int(actual_in_pkts11) :

                 return 1
         else:
                 return 0

