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
DESCRIPTION             : APIs for RIP

AUTHOR                  : Jameer - jameer@stoke.com
REVIEWER                : Venkat - krao@stoke.com
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
#from misc import *

from logging import getLogger
log = getLogger()
from StokeTest import test_case


def get_rip_state(ripHndl,peerAddr):
    """API is to get rip peer is up or not irrespective of time.Used in API verify_rip_peer()
       Usage Ex: get_rip_peer(self.ssx, peerAddr)
       Returns: 0 - if peer is up
                1 - if peer does not exist
    """

    if ripHndl.cmd("show ip rip peer |  grep %s"% peerAddr):
	return 0
    else:
	return 1

def verify_rip_peer(self, peerAddr, maxtime=100, wait_interval=10):
    """API is to verify rip peer is up or not with the specified time, this will poll the state
       depending on wait_interval and maxtime.
       Usage Ex: verify_rip_peer(self.ssx, peerAddr, maxtime=100, wait_interval=10)
       Returns: 0 - if peer is up
                1 - if peer does not exist
    """

    maxtries = maxtime / wait_interval
    if not get_rip_state(self, peerAddr):
	return 0
    while True:
	time.sleep(wait_interval)
        if get_rip_state(self, peerAddr):
		break
        maxtries -= 1
        if not maxtries:
            return 1
    return 0

