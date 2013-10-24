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
DESCRIPTION             : APIs for Diameter

TEST PLAN               : Diameter
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

from logging import getLogger
log = getLogger()
from StokeTest import test_case

def verify_diameter_stats(self,statType="DER", count=3):
	"""API to verify the Diameter stats
	Usage: verify_diameter_stats(self.ssx,statType="Sessions", count = 100)
	Returns: 0 on successful, 1 on not successful
        """
	daiOp = self.cmd('show diameter stats | grep %s '% statType)
	diaCnt = daiOp.split(':')[1].strip()
	if int(diaCnt) == int(count):
		return 1
	else:
		return 0
