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
DESCRIPTION             : This Script contains following RTC  APIs which has
                          been used in the SANITY and REGRESSION Testcases

TEST PLAN               :  Test plan
AUTHOR                  : rajshekar@primesoftsolutionsinc.com
REVIEWER                :suresh@primesoftsolutionsinc.com
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



def Verify_data_in_cdr_records(self,record,test_string="None"):
        """Verifying data field in cdr records"""
	result_int = ""
        list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\w+).*",ind_split[inde+3])
                                result_int= value_data.group(1)
        
				return result_int

def Verify_ses_in_cdr_records(self,record,test_string="None"):
	"""Verifying session name in cdr records"""

	result_int = ""
        list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\w+\@\w+).*",ind_split[inde+3])
                                result_int= value_data.group(1)

        return result_int

def Verify_ses_username_in_cdr_records(self,record,test_string="None"):
	"""Verifying session username in cdr records"""
	

	result_int = ""
        list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\w+\@\w+-\d).*",ind_split[inde+3])
                                result_int= value_data.group(1)
        Counter = self.cmd("show session counters")
        Out = Counter.split("\n")[-1].split()[0]
        if Out == result_int:
                return 1
        else:
                return 0

def Verify_ses_ipaddr_in_cdr_records(self,record,rem_ip,test_string="None"):

	"""Verifying session ipaddress in cdr records"""
	result_int = ""
        list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\d+.\d+.\d+.\d+)",ind_split)
                                result_int= value_data.group(1)
        if rem_ip == result_int:
                return True
        else:
                return False

def Verify_service_class_name_in_cdr_records(self,record = "None",service_class_name = "None",test_string="None"):
	"""Verifying service_class_name in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
				value_data=re.search("data=(\w+)",ind_split[inde+3])
				result_int= value_data.group(1)
	
	if result_int in service_class_name:
		return 1
	else:
		return 0

def Verify_class_id_in_cdr_records(self,record = "None",test_string="None"):
	"""Verifying  classid in cdr records"""

	result_int = ""
        if test_string in record:
		value_data=re.search("data=0x(\w+\d+\w+).*",record)
		result_int= value_data.group(1)
		
	Counter = self.cmd("show session detail | grep Session_handle ")
	if result_int in Counter:
		return 1
	else:
		return 0

def Verify_acl_out_name_cdr_records(self,record = "None",test_string="None"):
	"""Verifying acl_out name in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
	for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                		value_data=re.search("data=(\w+)",ind_split[inde+3])
                		result_int= value_data.group(1)

        Acl_name = self.cmd("show session detail | grep acl ")
        if result_int in Acl_name:
                return 1
        else:
                return 0

def Verify_ses_out_pkts_cdr_records(self,record = "None",num_of_pkts = "None",test_string="None"):
	"""Verifying ses_out packets in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\d+)",ind_split[inde+3])
				print value_data
                                result_int= value_data.group(1)
				print result_int

	if int(result_int) == int(num_of_pkts):
                return 1
        else:
                return 0

def Verify_class_in_pkts_cdr_records(self,record ="None",num_of_pkts = "None",test_string="None"):
	"""Verifying class_in_pkts in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\d+)",ind_split[inde+3])
                                result_int= value_data.group(1)

        if int(result_int) == int(num_of_pkts):
                return 1
        else:
                return 0


def Verify_ses_id_in_cdr_records(self,record = "None",test_string="None"):
	"""Verifying  ses_id in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
        if test_string in record:
                value_data=re.search("data=0x(\w+\d+\w+).*",record)
                result_int= value_data.group(1)

        Counter = self.cmd("show session detail | grep Session_handle ")
        if result_int in Counter:
                return 1
        else:
                return 0


def Verify_class_name_in_cdr_records(self,record ="None",class_name ="None",test_string="None"):	
	"""Verifying  class_name in cdr records"""

	result_int = ""
	list= record.split("<-------------------------------------->")
        for ind in range(len(list)):
                str2=list[ind]
                ind_split=str2.split("\n")
                for inde in range(len(ind_split)):
                        if test_string in ind_split[inde]:
                                value_data=re.search("data=(\w+_\w+)",ind_split[inde+3])
				result_int= value_data.group(1)
				
        if result_int == class_name:
                return 1
        else:
                return 0

