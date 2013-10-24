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
DESCRIPTION             : This Script contains following PreArp APIs which has
                          been used in thePreArp Testcases

TEST PLAN               : PreArp Test plan V4.6
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

def enable_prearp(self,context):
        """
        Description : API used to enable PREARP
                      Note : By default PreArp is enabled on SSX but you have to
                      execute this command if it is disabled.
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : self.ssx.enable_prearp(context="123")
        ReturnValue : On success return value is True else False
        """

        self.cmd("end")
        self.cmd("config")
        self.cmd("context %s"%context)
        out = self.cmd("no ip arp noprearp")
        if "pre-arping is already on" in out or "unexpected" not in out :
           return True
        else :
           return False

def disable_prearp(self,context):
        """
        Description : API used to disable PREARP
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : self.ssx.disable_prearp(context="123")
        ReturnValue : On success return value is True else False
        """

        self.cmd("end")
        self.cmd("config")
        self.cmd("context %s"%context)
        out = self.cmd("ip arp noprearp")
        if "Error" not in out :
           return True
        else :
           return False

def verify_prearp_disabled(self,context="local") :
        """
        Description : API used to verify the PREARP disabled when executed the command 
                      Note : Here we are verifying that particular command is there in 
                             "show config" output or not
        Arguments   : context : specify context name otherwise it will take default context name i.e local
        Example     : self.ssx.prearp_disabled(context="123")
        ReturnValue : On success return value is 1 else 0
        """

        out = self.cmd("sh conf cont %s | begin \"ip arp nopre\""%context)
        if "ip arp noprearp" not in out or "Error" in out:
           return 0
        else :
           return 1
