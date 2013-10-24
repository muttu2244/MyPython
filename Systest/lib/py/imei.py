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
DESCRIPTION             : API for IMEI

TEST PLAN               : MDO PERFORMANCE
AUTHOR                  : Rajshekar - rajshekar@stoke.com
REVIEWER                : 
DEPENDENCIES            : 

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

def getImeiList(imei="800000000000000",numImei="4192") :

    """
       Description  : API used to get the IMEI list in sequence (Last digit 15th is Check digit
                      and it is calculated using the Luhn Algorithm.This API will reduce manual
                      time incase of calculation of check digit for multiple IMEIs )                      

       Usage        : 1. getImeiList(imei="900000000000000",numImei="123")
                      2. getImeiList() with default arguments

       Arguments    : imei    - 15 digits number - Default value is  800000000000000
                      numImei - number of imeis - Default value is 4192

       Returns      : IMEI List on successful, "FAIL" on not successful
    """

    if len(imei) != 15 :
       log.error("please enter the imei with 15 digits but it has only %s digits"%len(imei))
       return "Fail"

    imei14Digits = imei[:-1]
    imeiList = []
    #Generate IMEI list with the given IMEI
    for num in range(0,int(numImei)):
        if num < 10 :
           imei13Digits = imei14Digits[:-1]
           imeiList.append("%s%s0"%(imei13Digits,num))
        elif num < 100 and num >= 10:
           imei12Digits = imei14Digits[:-2]
           imeiList.append("%s%s0"%(imei12Digits,num))
        elif num >=  100 and num < 1000:
           imei11Digits = imei14Digits[:-3]
           imeiList.append("%s%s0"%(imei11Digits,num))
        elif num >= 1000 :
           imei10Digits = imei14Digits[:-4]
           imeiList.append("%s%s0"%(imei10Digits,num))
        elif num >= 10000 :
           imei9Digits = imei14Digits[:-5]
           imeiList.append("%s%s0"%(imei9Digits,num))
        elif num >= 100000 :
           imei8Digits = imei14Digits[:-4]
           imeiList.append("%s%s0"%(imei8Digits,num))
        else :
           pass
    newImeiList = []
   
    #Loop through IMEI list 
    for imei in imeiList:
           imei14Digits = imei[:-1]
           length = len(imei14Digits)
           init = 1
           sum = 0
           while init <= length :
                if init%2==0 :
                   doubleDigit = 2 * int(imei14Digits[int("%s"%init)-1])
                   if doubleDigit >= 10 :
                      doubleDigit = str(doubleDigit)
                      sum = sum + int(doubleDigit[0]) + int(doubleDigit[1])
                   else :
                      sum = sum + doubleDigit
                else :
                   sum = sum + int(imei14Digits[int("%s"%init)-1])

                init = init + 1

           #Check Digit calculation
           num = sum % 10
           if num:
              chkDigit = 10 - num
           else :
              chkDigit = 0
           newImei = "%s%s" %(imei14Digits,chkDigit)
           newImeiList.append("%s"%newImei)
    return newImeiList
