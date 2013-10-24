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
from SSX import *

from logging import getLogger
log = getLogger()
#from StokeTest import test_case

def verify_vlan_counters(self,vlan1="none",vlan2="none",vlanid="none",in_pkts='none'):


        vlan2 = vlan2+"/"+vlanid
        vlan2_cou=self.cmd("show vlan counters | grep %s"%(vlan2))
        in_pkts1 =vlan2_cou.split()[1]


        if vlan1=="none":
                out_pkts=vlan2_cou.split()[3]
        else:
                vlan1=vlan1+"/"+vlanid
                vlan1_cou = self.cmd("show vlan counters | grep %s "%(vlan1))
                out_pkts =vlan1_cou.split()[3]

        if int(out_pkts) == in_pkts and  int(in_pkts1) == int(out_pkts):
                return 1
        else:
                return 0




def chk_ip_rout(self,ipaddr1="none",prtcl="none"):
    

    rt_output=self.cmd("show ip route | grep %s"%(ipaddr1))
        
    print "the  value of rt_output     is :%s"%rt_output
    print "the  value of rtoutput     is" 
    if rt_output == "":
        return 0 
    else:                   
        rt_chk = re.search( "(\d+.\d+.\d+.\d+)",rt_output)
        rt_chk_rtrn = rt_chk.group(1)
        if rt_chk_rtrn == ipaddr1 :
            if prtcl in rt_output:
                return 2
            elif prtcl == "none":           
                return 2
            else:           
                return 0
               


def create_vlan(self,numbers=1,vlanid=1) :
    vlanid = vlanid
    for i in range(1,numbers):
        output = self.cmd("vlan %s"%(vlanid))
        if output != "" :
            self.cmd("exit")
	    return 0
        self.cmd("exit")
        vlanid += 1
   # self.cmd("exit")
        

               
def create_dot1q_pol(self,crtopt="none",numbers=1,name="none",value=0,range1=0,range2=2,cosvalue=1):

     self.cmd("configuration")
     if name == "none" :
          name = 100
          name1 = name                    
     for i in range(0,numbers):
          name1 = "%s"%name+"%s"%i            
          print "the  value of number is :%d"%numbers
          output = self.cmd("dot1q-policy %s"%(name1)) 
          if output != "" :
              return 0     
              print name1
          if crtopt == 2 :
              output = self.cmd("cos map-ipv4-dscp range %s %s to  %s"%(range1,range2,cosvalue)) 
          elif crtopt == 3 :
              output = self.cmd("cos map-ipv6-dscp range %s %s to %s"%(range1,range2,cosvalue)) 
          else :
              output = self.cmd("cos default %d"%(cosvalue))
              print "the  value of rt_output     is :%s"%output

          if output != "" :
              self.cmd("exit")
	      return 0
          self.cmd("exit")


def chk_dot1q_pol(self,numbers=1,name="none"):
     count = 0

     if name == "none" :
          name = 100
          for i in range(0,numbers):
             name1 = name                    
             output = cmd("show configuration  | grep dot1q-policy") 
             name1 = "%s"%name+"%s"%i            
             print name1
             if output == "":
                 return 0 
             else:                   
                 if name1 in output:
                     count += count
                 else:           
                     return 1
              
 #     return count    


def create_vlan_dot1q(self,numofvlan=1,vlanid=1,name="none",numbers=1,crtopt=1,range1=0,range2=2,cosvalue=1) :
    for i in range(1,numofvlan):
        output = self.cmd("vlan %s"%(vlanid))
        if output != "" :
            self.cmd("exit")
	    return 0
        else : 
            for k in range(0,numbers):
                if name == "none" :
                    name = 100
                    name1 = name                    
                name1 = "%s"%name+"%s"%k            
                returnval = self.cmd("qos dot1q-policy %s"%(name1)) 
                if returnval != "" :
                    self.cmd("exit")
                    return 0     
        self.cmd("exit")
        vlanid += 1
