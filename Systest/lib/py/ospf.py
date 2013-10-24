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

from logging import getLogger
log = getLogger()
#from StokeTest import test_case

def verify_ospf_state(self,state="Full"):
    state = self.cmd("show ip ospf neighbor |  grep Full")
    if state:
        return 0
    else  :
	return 1

def  verify_ospf_neighbour(self,ssx_ip,neigbrId,state="Full"):
        return_count =0
        return_count1 =0

        neighbr=self.cmd("show ip ospf neighbor |  grep %s"%neigbrId)
        neighbr=neighbr.split()
        
        #self.myLog.output("the neighbr is %s" %neighbr)
        #self.myLog.output("the neighbr is %s" %neighbr[0])
        #self.myLog.output("the neighbr is %s" %neighbr[2])
        #state1 = "Full"
        #state=neighbr[2].split("/")
        #print state 
        #if state1 == state[0] :
         #  print   
        if ssx_ip in  neighbr[5] :
            return_count = 0
        else :
            print "1..."
            print ssx_ip
            print neighbr[5]
            return_count1 = 1

        if neigbrId in neighbr[4] :
            return_count = 0
        else :
            print "2..."
            print  neigbrId
            print neighbr[4]
            return_count1 = 1
        
        if state in neighbr[2] :
            return_count = 0
        else :
            print "3..."
            print state
            print neighbr[2]  
            return_count1 = 1
        return return_count1  

#def  verify_ospf_interface(self,interface,operState="UP",neighbr="DR",count=1,neighbrFlag=0):
def  verify_ospf_interface(self,interface,operState="UP",neighbr="Backup",count=1,neighbrFlag=0,countFlag=0,ntwk="POINTOMULTIPOINT",ntwkTypeFg=0):
        return_count = 0
        intfDetail=self.cmd("show ip ospf  interface %s"%interface)
        intfDetail = intfDetail.split()
        if intfDetail[0] == interface :
            print ("in interface ..")
        else :
            return_count = 1
        if operState == intfDetail[2] :
            print "interface name is %s " %intfDetail[0]
            print "ospf sttae is in %s" %intfDetail[2]
        else :
            return_count = 1
        if neighbrFlag == 1 :
            rt_output=self.cmd("show ip ospf  interface %s"%interface)
            output = re.search( "State\s+\S+",rt_output)
            output = output.group(0)
            print output
            if neighbr in output :
                 print "ospf state is in %s" %output
            else :
                 return_count = 1
        if countFlag == 1 :
            rt_output=self.cmd("show ip ospf  interface %s"%interface)
            output = re.search( "Neighbor\s+Count\s+is\s+\w+",rt_output)
            output = output.group(0)
            print output
            output = output.split()
            print output
            print output[3]
            print "%s" %count
            if count == int(output[3]) :
                 print "neighbor count is %s" %output
            else :
                 return_count = 1
        if ntwkTypeFg == 1:
            rt_output=self.cmd("show ip ospf  interface %s"%interface)
            output = re.search( "Neighbor\s+Type\s",rt_output)
            print output 
        print "%s" %return_count

        return return_count 




def  cisco_ospf_neighbour(self,intf_name,cisco_ip,neigbrId,state="FULL"):
        return_count =0
        return_count1 =0

        neighbr=self.cmd("show ip ospf neighbor | include  %s"%intf_name)

        print "the neighbr is ....%s" %neighbr
        neighbr=neighbr.split()
        
        print "the neighbr is ...%s" %neighbr
        print "the neighbr is %s" %neighbr[0]
        print "the neighbr is %s" %neighbr[2]
        #self.myLog.output("the neighbr is %s" %neighbr)
        #self.myLog.output("the neighbr is %s" %neighbr[0])
        #self.myLog.output("the neighbr is %s" %neighbr[2])
        #state1 = "Full"
        #state=neighbr[2].split("/")
        #print state 
        #if state1 == state[0] :
         #  print   
        if intf_name in neighbr[5] :
            return_count = 0
        else :
            print "the cisco ip is %s" %intf_name 
            print "the intf_ip is  %s" %neighbr[5]
            return_count1 = 1

        if neigbrId in neighbr[4] :
            return_count = 0
        else :
            print "the neighbr is %s" %neigbrId
            print "the intf_ip is  %s" %neighbr[4]
            return_count1 = 1
            return 1
        if state in neighbr[2] :
            return_count = 0
        else :
            print "the state is %s" %state
            print "the state_ip is  %s" %neighbr[2]
            return_count1 = 1
        return return_count1  

#def  verify_ospf_interface(self,interface,operState="UP",neighbr="DR",count=1,neighbrFlag=0):
def  cisco_ospf_interface(self,interface,operState="up",neighbr="DR",count=1,neighbrFlag=1,countFlag=0,ntwk="POINTOMULTIPOINT",ntwkTypeFg=0):
        return_count = 0
        intfDetail=self.cmd("show ip ospf interface %s"%interface)
        print "interface detail is %s" %intfDetail
        intfDetail = intfDetail.split()
        print "interface detail is %s" %intfDetail
        print "operState is in %s state" %intfDetail[2]
        if intfDetail[0] == interface :
            print ("in interface ..")
        else :
            return_count = 1
        if operState in  intfDetail[2] :
            print "interface name is.. %s " %intfDetail[0]
            print "ospf sttae is in %s" %intfDetail[2]
        else :
            print "ospf sttae is in %s" %intfDetail[2]
            print "oper state is in %s" %intfDetail[2]
            print "interface name is %s " %intfDetail[0]
            return_count = 1
        if neighbrFlag == 1 :
            rt_output=self.cmd("show ip ospf  interface %s"%interface)
            output = re.search( "State\s+\w+",rt_output)
            output = output.group(0)
            print output
            if neighbr in output :
                 print "ospf state is in %s" %output
            else :
                 return_count = 1
        if countFlag == 1 :
            rt_output=self.cmd("show ip ospf  interface %s"%interface)
            output = re.search( "Neighbor\s+Count\s+is\s+\w+",rt_output)
            output = output.group(0)
            print output
            output = output.split()
            print output
            print output[3]
            print "%s" %count
            if count == int(output[3]) :
                 print "neighbor count is %s" %output
            else :
                 return_count = 1
        #if ntwkTypeFg == 1:
        #    rt_output=self.cmd("show ip ospf  interface %s"%interface)
        #    output = re.search( "Neighbor\s+Type\s",rt_output)
        #    print output 
        print "%s" %return_count

        return return_count 


def cisco_ip_route(self,ipaddr="none",prtcl="none",rt_type="none",intf="name",partnet_ip="none"):

    return_count = 0
    index = 0
    not_entry = "% Network not in table"
    subnet_entry = "% Subnet not in table"
    print "the ipaddr is %s" %ipaddr 
    rt_output=self.cmd("show ip route  %s"%(ipaddr))
    #rt_output = rt_output.split()
    print "the  value of rt_output     is :%s"%rt_output
    print "the  value of rtoutput     is"
    if ((rt_output == "") or (not_entry in rt_output) or (subnet_entry in rt_output)):
        print "Routing table is empty"
        return 2  
    else:
        rt_chk = re.search( "(\d+.\d+.\d+.\d+)",rt_output)
        rt_chk_rtrn = rt_chk.group(1)
        print "%s" %rt_chk_rtrn
        if rt_chk_rtrn != ipaddr :
            print "ip addr check is %s %s" %(rt_chk_rtrn,ipaddr)
            print "FAIL"
            return_count = 1
        rt_output = rt_output.split()
        print  "%s" %rt_output[0]     
        print  "%s" %rt_output[7]     
        print  "%s" %rt_output[1]     
        if (prtcl != "none")  and  ( prtcl not in rt_output[6] ):
            print "in prtcl ..."   
            print rt_output[6]  
            print "FAIL"
            return_count = 1

        print rt_output[14]
        print rt_output[13]

        #print rt_output[14].strip(",")[0]
        #if ( (rt_type != "none") and (( int(rt_output[14].strip(",")[0]) != rt_type ) or ( rt_type != rt_output[13]) )):
        if  (rt_type == "intra") :
           if  ( rt_type != rt_output[13]) :
              print "in intra if."
              print "FAIL"
              return_count = 1
        elif   (rt_type != "none") :
           if ( int(rt_output[14].strip(",")[0]) != rt_type ) :
               print "in rt_type elif."  
               print rt_output[13] 
               print "FAIL"
               return_count = 1
        print "at 30 index"
        print rt_output[30] 
        for i in  range(len(rt_output)) :
            if ( partnet_ip  in rt_output[30] ):
                if rt_output[36] == index : 
                     if rt_output[i+6] == intf :
                         print "in intf ..."   
                         break
                     else : 
                         print "fialed for vlan..."    
                         print rt_output[i+6]
                         print intf
                         print "FAIL"
                         return_count = 1  
            else:                
                if ( i - 30 ) % 16 == 0  :
                    print "index is %s" %i
	  	    print "in index is %s" %rt_output[i]
                    if partnet_ip in rt_output[i] :
                        if rt_output[i+6] == intf :
                            print "in intf ..."   
                            break
                        else :  
                            print "fialed for vlan..."    
                            print rt_output[i+6]
                            print intf
                            print "FAIL"
                            return_count = 1  
                   
         
        #print "at 36 index"
        #print rt_output[36] 
        #for i in  range(len(rt_output)) :
        #    if ( index  in rt_output[36] ):
        #        break
        #    else:                
        #        if ( i - 36 ) % 16 == 0  :
        #            print "index is %s" %i
	#  	    print "in index is %s" %rt_output[i]
        #            if index in rt_output[i] :
        #                print "in vlan interface ..."   
        #                break
        #        else :
        #            return_count = 1  
        # 
        return return_count


           

def verify_ip_route(self,ipaddr="none",prtcl="none",rt_type="none",intf="name",partnet_ip="none"):

    return_count = 0
    index = 0
    print "the ipaddr is %s" %ipaddr 
    rt_output=self.cmd("show ip route  %s"%(ipaddr))
    #rt_output = rt_output.split()
    print "the  value of rt_output     is :%s"%rt_output
    print "the  value of rtoutput     is"
    if rt_output == "":
        return 2
    else:
        rt_chk = re.search( "(\d+.\d+.\d+.\d+)",rt_output)
        rt_chk_rtrn = rt_chk.group(1)
        print "%s" %rt_chk_rtrn
        if rt_chk_rtrn != ipaddr :
            print "ip addr check is %s %s" %(rt_chk_rtrn,ipaddr)
            print "FAIL"
            return_count = 1
        rt_output = rt_output.split()
        print  "%s" %rt_output[0]     
        print  "%s" %rt_output[6]     
        print  "%s" %rt_output[7]     
        print  "%s" %rt_output[1]     
        if (prtcl != "none")  and  ( prtcl not in rt_output[6] ):
            print "in prtcl ..."   
            print rt_output[6]  
            print "FAIL"
            #return_count = 1
        print rt_output[7][9]
        print "the rt_type is %s" %rt_type
        if (rt_type == "intra" ) or (rt_type == "inter") :
            if (rt_type not  in rt_output[7]) :
                 print "in rt_type if "  
                 print rt_output[6] 
                 print "FAIL"
                 return_count = 1
        elif (rt_type != "none") :
            if  ( rt_type != int(rt_output[7][9]) ) :
                 print "in rt_type elif"  
                 print rt_output[6] 
                 print "FAIL"
                 return_count = 1
        print "at 17 index"
        print rt_output[17] 
        for i in  range(len(rt_output)) :
            if ( partnet_ip  in rt_output[17] ):
                if rt_output[17] == index : 
                     if rt_output[i+2] == intf :
                         print "in intf ..."   
                         break
                     else : 
                         print "fialed for vlan..."    
                         print rt_output[i+2]
                         print intf
                         print "FAIL"
                         return_count = 1  
            else:                
                if ( i - 17 ) % 5 == 0  :
                    print "index is %s" %i
	  	    print "in index is %s" %rt_output[i]
                    if partnet_ip in rt_output[i] :
                        if rt_output[i+2] == intf :
                            print "in intf ..."   
                            break
                        else :  
                            print "fialed for vlan..."    
                            print rt_output[i+2]
                            print intf
                            print "FAIL"
                            return_count = 1  
                   
         
        #print "at 36 index"
        #print rt_output[36] 
        #for i in  range(len(rt_output)) :
        #    if ( index  in rt_output[36] ):
        #        break
        #    else:                
        #        if ( i - 36 ) % 16 == 0  :
        #            print "index is %s" %i
	#  	    print "in index is %s" %rt_output[i]
        #            if index in rt_output[i] :
        #                print "in vlan interface ..."   
        #                break
        #        else :
        #            return_count = 1  
        # 
        return return_count


           


def get_cpu_utilisation(self):
        retval = {}
        percentage = 100
        count = 0
        show_proc_cpu_ut = re.compile("""^(?P<proc_name>\S+\s+\S+\s+\S+\s+\S+\s+)\s+
                                           \s+\d+\s+\S+\d+\d+\d+
                                           (?P<stack>\S+)\s+
                                           (?P<heap>\S+)\s+
                                           (?P<share>\S+)
                                           """, re.VERBOSE)
        #self.ssx.get_to_exec()
        tmp = {}
        output = self.cmd("show process cpu")
        output = output.split()
        print "Theoutput is %s" %output
        print output[5].split("%")[0]
        print output[8].split("%")[0]
        print output[11].split("%")[0] 
        print output[17].split("%")[0]
        print output[20].split("%")[0]
        print output[23].split("%")[0]
        print output[23].split("%")[0]

        if ((float(output[5].split("%")[0])  <= float(percentage) )  or  (float(output[8].split("%")[0]) <= float(percentage)) or (float(output[11].split("%")[0]) <= float(percentage)) or (float(output[17].split("%")[0])  <= float(percentage) )  or  (float(output[20].split("%")[0]) <= float(percentage)) or (float(output[23].split("%")[0]) <= float(percentage)) )  :
              print "THe cpu util is below 100% percent..."
              count = 0
        else :
              print "THe cpu util is above 100% percent..."
              count = 1
              return count       

#        if (((output[5].split("%")[0])  <= percentage )  or  ((output[8].split("%")[0]) <= percentage) or ((output[11].split("%")[0]) <= percentage) or ((output[17].split("%")[0])  <= percentage )  or  ((output[20].split("%")[0]) <= percentage) or ((output[23].split("%")[0]) <= percentage) )  :
#             print "THe cpu util is below 100% percent..."
#             count = 0
#        else :
#              print "THe cpu util is above 100% percent..."
#              count = 1
#        return count       
   

def  verify_ospf_neighbour_pmp(self,ssx_ip,neigbrId,state="Full"):
        return_count =0
        return_count1 =0

        neighbr=self.cmd("show ip ospf neighbor |  grep %s"%neigbrId)
        neighbr=neighbr.split()
        
        #self.myLog.output("the neighbr is %s" %neighbr)
        #self.myLog.output("the neighbr is %s" %neighbr[0])
        #self.myLog.output("the neighbr is %s" %neighbr[2])
        #state1 = "Full"
        #state=neighbr[2].split("/")
        #print state 
        #if state1 == state[0] :
         #  print   
        if ssx_ip in  neighbr[6] :
            return_count = 0
        else :
            print "1..."
            print ssx_ip
            print neighbr[6]
            return_count1 = 1

        if neigbrId == neighbr[5] :
            return_count = 0
        else :
            print "2..."
            print  neigbrId
            print neighbr[5]
            return_count1 = 1
        
        if state in neighbr[2] :
            return_count = 0
        else :
            print "3..."
            print state
            print neighbr[6]  
            return_count1 = 1
        return return_count1  

def  cisco_ospf_neighbour_pmp(self,intf_name,cisco_ip,neigbrId,state="FULL"):
        return_count =0
        return_count1 =0
        time.sleep(15)
        neighbr=self.cmd("show ip ospf neighbor | include  %s"%intf_name)

        print "the neighbr is ....%s" %neighbr
        neighbr=neighbr.split()
        
        print "the neighbr is ...%s" %neighbr
        print "the neighbr is %s" %neighbr[0]
        print "the neighbr is %s" %neighbr[2]
        #self.myLog.output("the neighbr is %s" %neighbr)
        #self.myLog.output("the neighbr is %s" %neighbr[0])
        #self.myLog.output("the neighbr is %s" %neighbr[2])
        #state1 = "Full"
        #state=neighbr[2].split("/")
        #print state 
        #if state1 == state[0] :
         #  print   
        if intf_name in neighbr[6] :
            return_count = 0
        else :
            print "the cisco ip is %s" %intf_name 
            print "the intf_ip is  %s" %neighbr[6]
            return_count1 = 1

        if neigbrId in neighbr[5] :
            return_count = 0
        else :
            print "the neighbr is %s" %neigbrId
            print "the intf_ip is  %s" %neighbr[5]
            return_count1 = 1
            return 1
        if state in neighbr[2] :
            return_count = 0
        else :
            print "the state is %s" %state
            print "the state_ip is  %s" %neighbr[2]
            return_count1 = 1
        return return_count1  

