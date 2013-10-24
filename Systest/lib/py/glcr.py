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
DESCRIPTION             : APIs for GLC-R

TEST PLAN               :  Test plan
AUTHOR                  : Jameer - jameer@stoke.com, Jayanth - jayanth@stoke.com
REVIEWER                : Venkat - krao@stoke.com, Ashu - agupta@stoke.com 
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



def verify_glcr_status(self):
	"""API to verify the system GLC-R Status of the device
	Usage: verify_glcr_status(self.ssx)
	Returns: 0 on successful, 1 on not successful
	"""
        self.wait4cards()
        glcr_op = self.cmd("show glc-redundancy")
        if "No GLC redundancy group configured" in glcr_op:
                return 1
        list = ["No Active","No Standby GLC","No Active or Standby GLC","Degraded","Partial Redundancy"]
        for item in list:
                if item in glcr_op:
                    return 1
        return 0

def set_device_to_glcr(self,timeout=300):
        """API to set device to  GLC-R.
        Usage: set_device_to_glcr(self.ssx)
        Returns: 0 on successful, 1 on error, 2 if device is already configured.
        """
	status = verify_glcr_status(self)
	if status == 0:
		log.debug("Device is already configured for GLC-R")
		return 2
	if status == 1:
		log.debug("To configure the Device to GLC-R, needs full system reload")
		self.cmd("system glc-redundancy")
		self.reload_device(timeout)
		#Given delay to cards to come up to verify glcr
		time.sleep(30)
		self.wait4cards()
		status = verify_glcr_status(self)
		if status == 0:
			return 0
		else:
			log.error("Error while configuring the device for GLC-R")
			return 1

def verify_2to1_redundancy(self):
	status = verify_glcr_status(self)
	flag = -1
	if status == 1:
		log.error("Device is not configured for Redundancy")
		flag = 1
	else:
		glcr_op = self.cmd("show glc-redundancy | grep -i \"active\"")
		if int(len(glcr_op.splitlines())) == 3:
			log.info("Device is configured for 2:1 GLC Redundancy")
			flag = 0
	return flag

def verify_1to1_redundancy(self):
        status = verify_glcr_status(self)
        flag = -1
        if status == 1:
                log.error("Device is not configured for Redundancy")
                flag = -1
        else:
                glcr_op = self.cmd("show glc-redundancy | grep -i \"active\"")
                if int(len(glcr_op.splitlines())) == 2:
                        log.info("Device is configured for 1:1 GLC Redundancy")
                        flag = 0
		else:
			log.info("Device is not  configured for 1:1 GLC Redundancy")
			flag = 1
        return flag

def configure_1to1_redunadancy(self):
	flag = -1
	status = verify_glcr_status(self)
        if status == 0:
                log.debug("Device is already configured for GLC-R")
        if status == 1:
                log.error("Device is not configured for GLC-R\nTo configure the Device to GLC-R, needs full system reload")
		self.cmd("system glc-redundancy")
                self.reload_device(timeout)
                #Given delay to cards to come up to verify glcr
                time.sleep(30)
                self.wait4cards()
                status = verify_glcr_status(self)
                if status == 0:
                        return 0
                else:
                        log.error("Error while configuring the device for GLC-R")
                        return 1
	log.debug("Verifyig the 4th Card should be redundant")
	glcr_op = self.cmd("show glc-redundancy | grep -i \"active\"")
	if ((int(glcr_op.splitlines()[1].split()[0]) == 4) or (int(glcr_op.splitlines()[-1].split()[0]) == 4)):
		log.debug("4th Card is Active, doing glc-switchback before configuring 1:1")
		self.cmd("system glc-switchback")
		time.sleep(10)
		self.wait4cards()
		op = self.cmd("system glc-presence remove 3")
		if "ERROR:" in op:
			log.error("Failed to configure 1:1 Redundant")
			return 1
		log.info("Configured device for 1:1 Redundancy")
		
	return 0

def get_number_of_switchbacks(self,slot="3"):
	status = verify_glcr_status(self)
	if status == 1:
		log.error("Device is not configured for GLC-R")
		return 0
	if int(slot) == 3:
		glcr_op = self.cmd('show glc-redundancy | grep -i "Slot 101"')
		return int(glcr_op.split()[-1])
	else:
		glcr_op = self.cmd('show glc-redundancy | grep -i "Slot 100"')
		return int(glcr_op.split()[-1])

def get_number_of_switchovers(self,slot="3"):
	status = verify_glcr_status(self)
	if status == 1:
		log.error("Device is not configured for GLC-R")
		return 0
	if int(slot) == 3:
		glcr_op = self.cmd('show glc-redundancy | grep -i "Slot 101"')
		m = re.search("\s+Switchovers\s+(\d+)",glcr_op,re.I)
		return m.group(1)
	else:
		glcr_op = self.cmd('show glc-redundancy | grep -i "Slot 100"')
		m = re.search("\s+Switchovers\s+(\d+)",glcr_op,re.I)
                return m.group(1)

def get_glcr_status(self):
	list = {}
	self.wait4cards()
	op = self.cmd('sh glc-redundancy | begin -i "Active"')
	print int(len(op.splitlines()))
	if int(len(op.splitlines())) != 4:
		log.error("Not all cards are present in Redundancy Group")
		return 1
	op_active = self.cmd('sh glc-redundancy | grep -i "Active"')
        op_standby = self.cmd('sh glc-redundancy | grep -i "Standby"')
	list['active1'] = op_active.splitlines()[1].split()[0]
	list['active2'] = op_active.splitlines()[2].split()[0]
        list['standby'] = op_standby.splitlines()[-1].split()[0]
	return list

