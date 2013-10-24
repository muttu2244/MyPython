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
DESCRIPTION             : APIs for SEEDKEY
TEST PLAN               :  Test plan
AUTHOR                  : Rajshekar rajshekar@stoke.com
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
from pexpect import *

from logging import getLogger
log = getLogger()
from StokeTest import test_case

def deconf_key_capture(self,addrList=[],cont="stoke") :
        """API is to deconfigure key capture in specific context.
        Usage Ex: deconf_key_capture(self.ssx,addrList=["10.1.2.3"],cont="stoke")
        Returns: no returns 0
        """

        self.cmd('conf')
        self.cmd('cont %s'%cont)
        for addr in addrList :
             self.cmd('no capture seedkey address %s'%addr)

def verify_seedkey_function(self) :
        """API is to check wether the system seedkey functionality is enabled or not.
        Usage Ex: verify_seedkey_function(self.ssx)
        Returns: returns 0, if seedkey functionality not enabled
                 returns 1, If seedkey functionality enabled.
        """

        show_system = self.cmd('show system')
        pos = show_system.find("Next Boot")
        if "Keydump" in show_system[0:int(pos)-1] :
           return 1
        else :
           return 0

def get_seedkey_status(self) :
        """API is to return the status of Keydump under the output of "show system".
        Usage Ex: get_seedkey_status(self.ssx)
        Returns: returns the values of "NextBoot" and "CurBoot" depending on the keudump under
                 the output of "show system"
        """
        seedKeySta = {}

        show_system = self.cmd('show system')
        pos = show_system.find("Next Boot")
        if "Keydump" in show_system[0:int(pos)-1] :
           seedKeySta["CurBoot"] = 1
        else :
           seedKeySta["CurBoot"] = 0        
        if "Keydump" in show_system[int(pos):] :
           seedKeySta["NextBoot"] = 1
        else  :
           seedKeySta["NextBoot"] = 0
           
        return seedKeySta
        
def enable_seedkey_function(self):
        """API is to set the system seedkey functionality else enable seedkey and device will be reloaded.
        Usage Ex: enable_seedkey_function(self.ssx)
        Returns: returns 0, if set to the seedkey
                 returns 1, If already system set with seedkey and successful command execution.
        """
        res = verify_seedkey_function(self)
        if int(res) != 1 :
            com = "system keydump"
            out = self.cmd("%s"%com)
            if "Error" not in out :
                log.info("Device will be reloaded to set the keydump functionality")
                self.reload_device()
            elif "Error" in out :
                log.info("Command \"%s\" given an error \"%s\" during execution"%(com,out))
                return 0
            else :
                return 1
        return 1

def disable_seedkey_function(self):
        """API is to unset the system seedkey functionality and device will be reloaded.
        Usage Ex: disable_seedkey_function(self.ssx)
        Returns: returns 0, if unset to the seedkey
                 returns 1, If not successful command execution.
        """
        res = verify_seedkey_function(self)
        if int(res) == 1 :
            # If the seed key function enabled then disabled seedkey function.
            com = "no system keydump"
            out = self.cmd("%s"%com)
            if "Error" not in out :
                log.info("Device will be reloaded to unset the keydump functionality")
                self.reload_device()
            elif "Error" in out :
                log.info("Command \"%s\" given an error \"%s\" during execution"%(com,out))
                return 0
            else :
                return 1
        else : 
           return 1
        return 1

