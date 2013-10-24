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
DESCRIPTION             : This Script contains following DHCP  APIs which has
                          been used in the DHCP Testcases

TEST PLAN               : DHCP Test plan V0.3
AUTHOR                  : Rajshekar; email : Rajshekar@primesoftsolutionsinc.com
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


def get_ipaddr(self,interface):
	"""getting the ip address of the particular interface on any linux machine"""
	out = self.cmd("/sbin/ifconfig %s"%interface)
	split_out = out.split()[6]
	split_out = split_out.split(":")[1]
	return split_out


def get_hwaddr(self,interface):
	"""getting the hardware address of particular interface on any linux machine"""
        out = self.cmd("/sbin/ifconfig %s"%interface)
        split_out = out.split()[4]
        return split_out

