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
DESCRIPTION             : APIs for JF

TEST PLAN               :  Test plan
AUTHOR                  : Venkat krao@stoke.com
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




def get_sys_mtu(self):
        mtus = self.cmd("sh system | grep -i MTU")
	if not mtus: 
		log.error("No ouput for command 'sh system | grep -i MTU'")
	if "ERROR:" in mtus:
          log.exception("")
          log.error("ERROR while verifying system MTU")
	  raise

        mtuCrnt = mtus.splitlines()[1].split(":")[-1].strip()
        mtusNxt = mtus.splitlines()[2].split(":")[-1].strip()
	log.info("MTU - Current Boot : %s Next Boot : %s" %(mtuCrnt,mtusNxt))
	return mtuCrnt,mtusNxt

def set_sys_mtu(self,mtu="2000"):
        """API is to set the system MTU as per the input, Device will be reloaded to set the requested MTU
	Usage Ex: set_sys_mtu(self.ssx,mtu="4000")
	Returns: returns 0, if set to the requested MTU
		 returns 1, If already system configured to requested MTU or requested MTU is less than 1500
        """
	if int(mtu) < 1500:
		log.error("Can not set System MTU less than 1500")
		return 1

	if verify_sys_mtu(self,mtu):
		log.info("Device will be reloaded to set the MTU")
		if int(mtu)==1500:
			self.cmd("no system mtu")
		else:
                	self.cmd("system mtu %s"% mtu)
                self.reload_device()
        else:
                log.info("Device is already set to required MTU")
                return 1
        return 0
	
def verify_sys_mtu(self,mtu="9500"):
	sysMtu = self.cmd("show system | grep -i MTU")
	if int(sysMtu.splitlines()[1].split()[-1]) == int(mtu):
		return 0
	else:
		return 1

def verify_int_mtu(self, intf, context="local"):
	self.cmd("context %s"%context)
        mtu = self.cmd("sh ip int %s | grep -i mtu" %intf)
	if not mtu: 
          	log.exception("")
		log.error("No ouput for command 'sh ip int %s | grep -i mtu'")
		raise
	mtu = mtu.split("mtu:")[-1].strip()
	return mtu

def change_interface_mtu(self, intf, context, mtu):
	self.configcmd("context %s"%context)
	self.cmd("interface %s"%intf)
	mtu_op = self.cmd("no ip mtu")
	if "ERROR" in mtu_op:
		log.error("ERROR while unconfiguring the 'ip mtu'")
		self.cmd("end")
		return 1
	mtu_op = self.cmd("ip mtu %s"%mtu)
	if "ERROR" in mtu_op:
                log.error("ERROR while configuring the 'ip mtu %s'"%mtu)
		self.cmd("end")
		return 1
	else:
		self.cmd("end")
		return 0

def verify_port_mtu(self, port):
        mtu = self.cmd("sh po %s detail | grep -i mtu" %port)
	if not mtu or ("ERROR" in mtu): 
          	log.exception("")
		log.error("No ouput for command sh po %s detail | grep -i mtu  OR ERROR in output"%port)
		raise
	mtu = mtu.split("MTU")[-1].strip()
	return mtu

def verify_tunnel_fragPkts(self,sys_mtu="9500",frame_size="9500",tun_intf_mtu="1500",no_of_Pkts=1,tunnel_name="tun"):
    """API is to verify the number of framented packets for the tunnel
       Usage Ex: verify_tunnel_fragPkts(self.ssx,"9500","9180","726",1,"tun1")
       Returns: returns 0 on successfull (if fragmented as per tunnel interface mtu and system mtu)
	                1 on un-sucess -> not fragmented as expected.
			2 on error.
    """
    if int(frame_size) >  int(sys_mtu):
	log.error("sending packets with size more than system MTU")
	return 2
    tun_cnt = self.cmd("show tunnel counters | grep \"%s   \""%tunnel_name)
    #Calculate the number of fragments
    no_of_frags = (int(frame_size)/int(tun_intf_mtu) + 1) * no_of_Pkts
    log.debug("number of fragments should be: %d"%no_of_frags)
    #Verify the fragments as per interface MTU
    fragPkts = int(tun_cnt.split()[2])
    if fragPkts == no_of_frags:
        return 0
    else:
        return 1

def verify_fragPkts(self,sys_mtu="9500",frame_size="9500",intf_mtu="1500",port="2/0",no_of_Pkts=1):
    #lets verify the interface mtu to verify for the proper counter
    no_of_frags = (int(frame_size)/int(intf_mtu) + 1) * no_of_Pkts
    remain = (int(frame_size)%int(intf_mtu))
    remain = remain+24
    fragPkts = fragPkts2 = 0
    if remain <=64:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts64\""%port)
        fragPkts2 = int(cntrem.split()[3])
    if remain >=65 and remain <=127:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts65to127\""%port)
        fragPkts2 = int(cntrem.split()[3])
    if remain >=128 and remain <=255:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts128to255\""%port)
        fragPkts2 = int(cntrem.split()[3])
    if remain >=256 and remain <=511:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts256to511\""%port)
        fragPkts2 = int(cntrem.split()[3])
    if remain >=512 and remain <=1023:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts512to1023\""%port)
        fragPkts2 = int(cntrem.split()[3])
    if remain >=1024 and remain <=1518:
        cntrem = self.cmd("show port %s counters detail | grep \"Pkts1024to1518\""%port)
        fragPkts2 = int(cntrem.split()[3])
    
    if intf_mtu <= 1023:
        cnt = self.cmd("show port %s counters detail | grep \"Pkts512to1023\""%port)
        fragPkts = int(cnt.split()[3])
    if (intf_mtu >= 1024 and intf_mtu <= 1518):
        cnt = self.cmd("show port %s counters detail | grep \"Pkts1024to1518\""%port)
        fragPkts = int(cnt.split()[3])
    else:
        cnt = self.cmd("show port %s counters detail | grep \"Pkts1519toMax\""%port)
        fragPkts = int(cnt.split()[3])
    
    TotalFrag = fragPkts + fragPkts2
    log.output("Stats:\nno_of_frags:%s\nremainder:%s\nfragPkts:%s\nfragPkts2:%s\nTotalFrag:%s\n"%(no_of_frags,remain,fragPkts,fragPkts2,TotalFrag))
    if TotalFrag == no_of_frags:
        return 0
    else:
        return 1


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

