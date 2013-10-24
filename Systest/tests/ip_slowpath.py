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
DESCRIPTION             : This Script contains following ip_slowpath  APIs which has
                          been used in the Slowpath Testcases

TEST PLAN               : IP_SLOWPATH Test plan V0.3
AUTHOR                  : Ganapathi; email :  ganapathi@primesoftsolutionsinc.com
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
log = getLogger()
from StokeTest import test_case
#from ip_slowpath_config import *





def ip_verify_ip_counters_icmp(self,total_tx='none',echo_request='none',total='none',echo_reply='none',
                                   unreachable='none',mask_request='none',mask_reply='none',
                                   source_quench='none',param_problem='none',timestamp='none',
                                   redirects='none',info_reply='none',ttl_expired='none',
                                   other='none',format='none',rate_limit='none',out_str='none'):



        """
          Description: - This API verify the "show ip conters icmp" with passing differnt combinations of
                      transmitted  ICMP packet statastics such as echo request etc with output when the
                      command run.
          CLI Used- CLI.s that are used for the API  <show ip counters icmp>.
          Input: - List of differnt ICMP packet statastics Inputs such as no of Echo Request packets
                        transmitted etc.
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """

        expected={'icmp_echo_request':echo_request,'icmp_echo_reply':echo_reply,
                  'icmp_total':total_tx,'icmp_unreachable':unreachable,
                  'icmp_mask_request':mask_request,'icmp_mask_reply':mask_reply,
                  'icmp_source_quench':source_quench,'icmp_param_problem':param_problem,
                  'icmp_timestamp':timestamp,'icmp_redirects':redirects,
                  'icmp_info_reply':info_reply,'icmp_ttl_expired':ttl_expired,
                  'icmp_other':other,'icmp_format':format,'icmp_rate_limit':rate_limit}

        cli="show ip counters icmp"
        ret_str=self.cmd(cli)
       
        regex_list=['\s*Rx:\s+Total\s+(?P<rx_total>\d+)\s+Tx:\s+Total\s+(?P<icmp_total>\d+)',
             '\s+Echo\s+Request\s+(?P<rx_echo_request>\d+)\s+Echo\s+Request\s+(?P<icmp_echo_request>\d+)',
             '\s+Echo\s+Reply\s+(?P<rx_echo_reply>\d+)\s+Echo\s+Reply\s+(?P<icmp_echo_reply>\d+)',
             '\s+Unreachable\s+(?P<rx_unreachable>\d+)\s+Unreachable\s+(?P<icmp_unreachable>\d+)',
             '\s+Param\s+Problem\s+(?P<rx_param_problem>\d+)\s+Param\s+Problem\s+(?P<icmp_param_problem>\d+)',
             '\s+Redirects\s+(?P<rx_redirects>\d+)\s+redirects\s+(?P<icmp_redirects>\d+)',
            '\s+TTL\s+Expired\s+(?P<rx_ttl_expired>\d+)\s+TTL\s+Expired\s+(?P<icmp_ttl_expired>\d+)',
            '\s+Mask\s+Request\s+(?P<rx_mask_request>\d+)\s+Mask\s+Request\s+(?P<icmp_mask_request>\d+)',
            '\s+Mask\s+Reply\s+(?P<rx_mask_reply>\d+)\s+Mask\s+Reply\s+(?P<icmp_mask_reply>\d+)',
            '\s+Source\s+Quench\s+(?P<rx_source_quench>\d+)\s+Source\s+Quench\s+(?P<icmp_source_quench>\d+)',
            '\s+Timestamp\s+(?P<rx_timestamp>\d+)\s+Timestamp\s+(?P<icmp_timestamp>\d+)',
       '\s+Info\s+Request\s+(?P<rx_info_request>\d+)\s+Info\s+Reply\s+(?P<icmp_info_reply>\d+)',
            '\s+Other\s+(?P<rx_other>\d+)\s+Other\s+(?P<icmp_other>\d+)',
            '\s+Error:\s+Checksum\s+(?P<chksum_error>\d+)\s+Format\s+(?P<format_error>\d+)',
            '\s+Length\s+(?P<length_error>\d+)\s+Rate\s+Limit\s+(?P<rate_limit_error>\d+)']


        actual={}
        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]
        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0

        return 1 


def telnet_glc(self,telnet_to_glc='none'):
        """
          Description: - This API will establish a telnet session with GLC from an IMC
          CLI Used- No CLI used
          Input: -    Slot no to which we want to telnet
          Output: -
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """

        cmd_str="SOCK=/nv telnet 192.168.200.20"+telnet_to_glc
        self.ses.sendline(cmd_str)
        self.ses.expect("login:")
        self.ses.sendline("root")
        return



def ip_verify_ip_counters_general(self,checksum='none',no_resource='none',
                                      source='none',ttl_expired='none',
                                      bad_version='none',option='none',
                                      frag_dropped='none',frag_malformed='none',
                                      acl_in_dropped='none',unreachable='none',
                                      length='none',runt='none',
                                      destination='none',
                                      arp_unresolved='none',other='none',
                                      frag_timeout='none',could_not_frag='none',
                                      acl_out_dropped='none',local_delivery='none',local_out='none',
                                  fragments='none',express='none',reassembled='none',exception='none',
                                  options_present='none',fragmented='none',ike_packets='none' ):

        """
          Description: - This API verify whether the packets are recieved on the line card by observing the
                         o/p stats of the command "show ip counters general" o/p ,the source counter statastics          CLI Used- CLI.s that are used for the API  <show ip counters general>.
          Input: -    source counter as a parameter
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """
        expected={'checksum':checksum,'no_resource':no_resource,
                  'source':source,'ttl_expired':ttl_expired,
                  'bad_version': bad_version,'option':option,
                  'frag_dropped':frag_dropped,'frag_malformed':frag_malformed,
                  'acl_in_dropped': acl_in_dropped,'unreachable':unreachable,
                  'length':length,'runt':runt,'destination':destination,
                  'arp_unresolved':arp_unresolved,'other': other ,
                  'frag_timeout':frag_timeout,
                  'could_not_frag':could_not_frag,
                  'acl_out_dropped':acl_out_dropped,
                  'local_delivery':local_delivery,
                  'local_out':local_out,
                  'fragments':fragments,
                  'express'  :express,
                  'reassembled':reassembled,
                  'exception':exception,
                  'options_present':options_present,
                  'fragmented':fragmented,
                  'ike_packets':ike_packets}


        regex_list=['\s+Rx:\s+Local\s+Delivery\s+(?P<local_delivery>\d+)\s+Tx:\s+Local\s+Out\s+(?P<local_out>\d+)',
                    '\s+Fragments\s(?P<fragments>\d+)\s+Express\s+(?P<express>\d+)',
                    '\s+Reassembled\s+(?P<reassembled>\d+)\s+Exception\s+(?P<exception>\d+)',
                   '\s+Options\s+Present\s+(?P<options_present>\d+)\s+Fragmented\s+(?P<fragmented>\d+)',
                  '\s+IKE\s+Packets\s+(?P<ike_packets>\d+)',
                  '\s+Error:\s+Checksum\s+(?P<checksum>\d+)\s+Unreachable\s+(?P<unreachable>\d+)',
                  '\s+No\s+Resource\s+(?P<no_resource>\d+)\s+length\s+(?P<length>\d+)',
                  '\s+Source\s+(?P<source>\d+)\s+Runt\s+(?P<runt>\d+)',
                  '\s+TTL\s+Expired\s+(?P<ttl_expired>\d+)\s+Destination\s+(?P<destination>\d+)',
                  '\s+Bad\s+Version\s+(?P<bad_version>\d+)\s+ARP\s+Unresolved\s+(?P<arp_unresolved>\d+)',
                  '\s+Option\s+(?P<option>\d+)\s+Other\s+(?P<other>\d+)',
                  '\s+Frag\s+Dropped\s+(?P<frag_dropped>\d+)\s+Frag\s+Timeout\s+(?P<frag_timeout>\d+)',
                  '\s+Frag\s+Malformed\s+(?P<frag_malformed>\d+)\s+Couldn\'t\s+Frag\s+(?P<could_not_frag>\d+)',
                  '\s+ACL-In\s+Dropped\s+(?P<acl_in_dropped>\d+)\s+ACL-Out\s+Dropped\s+(?P<acl_out_dropped>\d+)']

        actual={}
        cli="show ip counters general"
        ret_str=self.cmd(cli)

        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]
        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0

        return 1


def ip_verify_ipv6_counters_general(self,too_many_ext_hdrs='none',no_resource='none',
                                    bad_address_scope="none",hoplimit_expired='none',
                                    bad_version='none',option='none',
                                    frag_dropped='none',frag_malformed='none',
                                    reassembled='none',unreachable='none',could_not_forward="none",
                                    acl_in_dropped="none", frag_overflow='none',esp_ah="none",
                                    other='none',error_ike_pkt="none",
                                    frag_timeout='none',could_not_frag='none',reassembly="none",      
                                    acl_out_dropped='none',local_delivery='none',local_out='none',
                                   fragments='none',express='none',slowpath="none",router_header_out="none",
                                   runt='none',neighbour_unresolved="none",length="none",
                                   fragmented='none',ike_packets='none',express_forward='none' ):

        """
          Description: - This API verify whether the packets are recieved on the line card by observing the
                         o/p stats of the command "show ipv6 counters general" o/p ,the source counter statastics          CLI Used- CLI.s that are used for the API  <show ipv6 counters general>.
          Input: -    source counter as a parameter
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """





        expected={'too_many_ext_hdrs':too_many_ext_hdrs,'no_resource':no_resource,
                  'hoplimit_expired':hoplimit_expired,'bad_address_scope':bad_address_scope,
                  'bad_version': bad_version,'option':option,
                  'frag_dropped':frag_dropped,'frag_malformed':frag_malformed,
                  'acl_in_dropped': acl_in_dropped,'unreachable':unreachable,
                  'could_not_forward':could_not_forward,
                  'length':length,'other': other ,
                  'frag_timeout':frag_timeout,
                  'could_not_frag':could_not_frag,'slowpath':slowpath,'router_header_out':router_header_out,
                  'acl_out_dropped':acl_out_dropped,
                  'local_delivery':local_delivery,
                  'local_out':local_out,
                  'fragments':fragments,'esp_ah':esp_ah,'frag_overflow':frag_overflow,
                  'express'  :express,'runt':runt,
                  'reassembled':reassembled,'reassembly':reassembly,
                  'fragmented':fragmented,'error_ike_pkt':error_ike_pkt,
                  'ike_packets':ike_packets,'express_forward':express_forward}


        regex_list=['\s*Rx:\s+Total\s+(?P<rx_total>\d+)\s+Tx:\s+Total\s+(?P<tx_total>\d+)',
                    '\s+Local\s+Delivery\s+(?P<local_delivery>\d+)\s+Local\s+Out\s+(?P<local_out>\d+)',
                    '\s+Fragments\s(?P<fragments>\d+)\s+Express\s+Forward\s+(?P<express_forward>\d+)',
                    '\s+Reassembled\s+(?P<reassembled>\d+)\s+Slowpath\s+Forward\s+(?P<slowpath_forward>\d+)',
                   '\s+IKE\s+Packets\s+(?P<rx_ike_packets>\d+)\s+Fragmented\s+(?P<fragmented>\d+)',
                  '\s+Route\s+Header\s+Out\s+(?P<route_hdr_out>\d+)',
                  '\s+Error:\s+Too\s+many\s+Ext\s+Hdrs\s+(?P<too_many_ext_hdrs>\d+)\s+Unreachable\s+(?P<unreachable>\d+)',
                  '\s+No\s+Resource\s+(?P<no_resource>\d+)\s+length\s+(?P<length>\d+)',
                  '\s+Bad\s+Address\s+Scope\s+(?P<bad_address_scope>\d+)\s+Runt\s+(?P<runt>\d+)',
                  '\s+Hoplimit\s+Expired\s+(?P<hoplimit_expired>\d+)\s+Can\'t\s+Forward\s+(?P<could_not_forward>\d+)',
                  '\s+Bad\s+Version\s+(?P<bad_version>\d+)\s+Neighbor\s+Unresolved\s+(?P<neighbor_unresolved>\d+)', 
                  '\s+Option\s+(?P<option>\d+)\s+Other\s+(?P<other>\d+)', 
                  '\s+Frag\s+Dropped\s+(?P<frag_dropped>\d+)\s+Frag\s+Timeout\s+(?P<frag_timeout>\d+)',
                  '\s+Reassembly\s+(?P<reassembly>\d+)\s+Fragment\s+Overflow\s+(?P<frag_overflow>\d+)',
                  '\s+Frag\s+Malformed\s+(?P<frag_malformed>\d+)\s+Couldn\'t\s+Frag\s+(?P<could_not_frag>\d+)',
                  '\s+ACL-In\s+Dropped\s+(?P<acl_in_dropped>\d+)\s+ACL-Out\s+Dropped\s+(?P<acl_out_dropped>\d+)',
                   '\s+IKE\s+packet\s+(?P<error_ike_packet>\d+)\s+ESP\/AH\s+(?P<esp_ah>\d+)']
        
        actual={}
        flag=0
        cli="show ipv6 counters general"
        ret_str=self.cmd(cli)

        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]
        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0

        return 1

        
                                                                                             

def ip_verify_ip_counters_udp(self,checksum='none',no_port='none',
                                  rx_total='none',tx_total='none',
                                  short_pkt='none',short_hdr='none',
                                  full='none',no_port_bcast='none' ):

        """
          Description: - This API verify whether the UDP packets are recieved on the line card by observing the
                         o/p stats of the command "show ip counters udp" o/p ,the source counter statastics              CLI Used- CLI.s that are used for the API  <show ip counters udp>.
          Input: -  the stats of the o/p of the command
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """


        expected={'checksum':checksum,'no_port':no_port,
                  'rx_total':rx_total,'tx_total':tx_total,
                  'short_pkt':short_pkt,'short_hdr':short_hdr,
                  'full':full,'no_port_bcast':no_port_bcast}
        regex_list=['\s+Rx:\s+Total\s+(?P<rx_total>\d+)',
                    '\s+Tx:\s+Total\s+(?P<tx_total>\d+)',
                    '\s+Error:\s+Checksum\s+(?P<checksum>\d+)',
                    '\s+No\s+Port\s+(?P<no_port>\d+)',
                    '\s+Short\s+packet\s+(?P<short_pkt>\d+)',
                    '\s+Short\s+header\s+(?P<short_hdr>\d+)',
                    '\s+Full\s+(?P<full>\d+)',
                    '\s+No\s+port\s+bcast\s+(?P<no_port_bcast>\d+)'] 



        actual={}
        cli="show ip counters udp"
        ret_str=self.cmd(cli)
        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]

        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0

        return 1 









def get_mac_address(self,port='none'):


        """
          Description: - This API will return the mac_adress of the port which is directly connected
                         to the linux machine
          CLI Used- "show port"
          Input: -    slot and port as a parameter format slot/port
          Output: - Returns returns the mac address of the required port
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """


        out_str=self.cmd("show port")

        split_list=out_str.split("\n")

        for line in split_list:
             if (re.compile(port)).search(line):
                ret_list=line.split()
                return ret_list[(len(ret_list))-1].strip("\n")








def get_cli_passwd(self,day='none',level='none'):
        """
          Description: - This API will return the password to enable required hidden level in SSX box
                         of a particular day today,tommorrow or yesterday
          CLI Used-   runs the cli-pwd command on linux m/c
          Input: -    day,level number
          Output: - Returns the password
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """




        flag=0
        count=7
        os.system("cli-pwd >> pwd.txt")
        fileptr=file("pwd.txt","r")
        lvl_str= "level %s"%(level)


        for line in fileptr:
            if (re.compile(day,re.I)).search(line) or flag==1:
                if (re.compile(lvl_str,re.I)).search(line):
                      var=line.partition(((re.compile("enable",re.I)).search(line)).group())
                      list1=var[2].split(',')
                      fileptr.close()
                      os.system("rm pwd.txt")
                      return list1[0].strip()
                flag=1
                count = count - 1
                if count == 0:
                    flag=0
        return "not found"







def generic_get_slot_and_port(self,slot_port='none'):
        """
          Description: - This API will splits the i/p parameter string into slot and port
                         and place these values into a dictionary
          CLI Used-   no CLI used
          Input: -    string as parameter
          Output: - Returns the dictionary with slot and parameter
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """


        dict={}
        regex=(re.compile(r'(\d+)/(\d+)').search(slot_port))
        dict['slot']=regex.group(1)
        dict['port']=regex.group(2)
        return dict

def get_hex_ip_addr(self,dot_ip='none'):
        """
          Description: - This API will return the Hex format of the IP which takes dotted format of IP as input                          parameter.
          CLI Used-   no CLI used
          Input: -    Dotted format of IP address
          Output: -   Hex format of IP address
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """

        regex=(re.compile(r'(\d+).(\d+).(\d+).(\d+)').search(dot_ip))
        if int(regex.group(1))>15:
             first_octet=(str(hex(int(regex.group(1))))).replace("0x","")
        else:
             first_octet=(str(hex(int(regex.group(1))))).replace("x","")

        if int(regex.group(2))>15:
             second_octet=(str(hex(int(regex.group(2))))).replace("0x","")
        else:
             second_octet=(str(hex(int(regex.group(2))))).replace("x","")

        if int(regex.group(3))>15:
             third_octet=(str(hex(int(regex.group(3))))).replace("0x","")
        else:
             third_octet=(str(hex(int(regex.group(3))))).replace("x","")

        if int(regex.group(4))>15:
             fourth_octet=(str(hex(int(regex.group(4))))).replace("0x","")
        else:
             fourth_octet=(str(hex(int(regex.group(4))))).replace("x","")

        return first_octet+second_octet+third_octet+fourth_octet



#LINUX .py


def invoke_scapy(self,proto='none',sudo_passwd='none',dst_mac_adr='ff:ff:ff:ff:ff:ff',dst_ip_adr='127.0.0.1',src_ip_adr='127.0.0.1',ip_checksum='none',ip_hdr_len='none',ip_pkt_len='none',ip_ttl='none',ip_flags='none',ip_options='none',from_interface='eth1',large_pkt=0,udp='none',udp_checksum='none',ip_tos='none',ip6_plen=0,log="none",count = 5):

        """
        Description:  This API will invoke scapy tool which works in python ,in
                      interpreter mode and sends 4 ip packets on required
                      interface  to required destiantion with our required
                      fields populated
        CLI used :sudo python
        Input    :The fields which we require to fill the IP packets
        Output   :Sends 4 IP packets to SSX
        Author   :Ganapathi,ganapathi@primesoftsolutionsinc.com """



        dict={'chksum':ip_checksum,'ihl':ip_hdr_len,'len':ip_pkt_len,
              'ttl':ip_ttl,'flags':ip_flags,'tos':ip_tos}
        str1=dst_mac_adr.strip()
        payload = 'X'
        if large_pkt==1:
            for i in range(1200):
                payload+='X'


        if ip_options == 'none':
            for key in dict.keys():
                if dict[key] != 'none':
                    value=int(dict[key])
                    scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",%s=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,key,value,payload,from_interface)

                    break
                else:
                    scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s")/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,payload,from_interface)
        else:
            if ip_ttl == 'none' and ip_flags == 'none':
                scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",options="%s")/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,ip_options,payload,from_interface)
            elif ip_flags != 'none':
                scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",flags=%d,options="%s")/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,ip_flags,ip_options,payload,from_interface)
         
            else:
                value=int(ip_ttl)
                scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",options="%s",ttl=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,ip_options,value,payload,from_interface)

        if udp != 'none':
            if udp_checksum != 'none':
                value2=int(udp_checksum)
                scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s")/UDP(dport=500,chksum=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,value2,payload,from_interface)
                if ip_checksum != 'none':
                    value1=int(ip_checksum)
                    scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",chksum=%d)/UDP(dport=500,chksum=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,value1,value2,payload,from_interface)
                if ip_flags != 'none':
                    value1=int(ip_flags)
                    scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",flags=%d)/UDP(dport=500,chksum=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,value1,value2,payload,from_interface)
                    if ip_options != 'none':
                       scapy_cmd='sendp(Ether(dst="%s")/IP(src="%s",dst="%s",flags=%d,options="%s")/UDP(dport=500,chksum=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,value1,ip_options,value2,payload,from_interface)
        if proto=="ipv6":
            if ip6_plen != 0:
                chksum=int(udp_checksum)
                scapy_cmd='sendp(Ether(dst="%s")/IPv6(src="%s",dst="%s",plen=%d)/UDP(dport=500,chksum=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,ip6_plen,chksum,payload,from_interface)
            else:
                scapy_cmd='sendp(Ether(dst="%s")/IPv6(src="%s",dst="%s",hlim=%d)/"%s",iface="%s")' %(str1,src_ip_adr,dst_ip_adr,ip_ttl,payload,from_interface)

        self.ses.sendline("sudo python2.5")
        retstr=self.ses.before
        which=self.ses.expect(["Password:",">>>"])

        if which != 0:

            self.ses.sendline("from scapy import *")
            if proto == "ipv6":
                self.ses.sendline("from scapy6 import *")
            retstr=self.ses.before
            self.ses.expect(">>>")
            retstr=self.ses.before

            while count > 0:
                self.ses.sendline(scapy_cmd)
                retstr =self.ses.before
                log.output("scapy_cmd::%s" %(retstr))
                self.ses.expect(">>>")
                retstr =self.ses.before
                count = count - 1

            self.ses.sendline("%c" %(0x04))
            return
        else:

            self.ses.sendline(sudo_passwd)
            self.ses.expect(">>>",20)
            retstr += self.ses.before
            self.ses.sendline("from scapy import *")
            if proto == "ipv6":
                self.ses.sendline("from scapy6 import *")
            self.ses.expect(">>>",20)
            while count > 0:
                self.ses.sendline(scapy_cmd)
                retstr = self.ses.before
                log.output("scapy_cmd::%s" %(retstr))
                self.ses.expect(">>>",5)
                count = count - 1

            self.ses.sendline("%c" %(0x04))
            return

def ip_ip4_pktgen(self,card='none',slot='none',port='none',src_addr='01010101',options='0',bad_option='0',
                                dst_addr='none',pkt_len="500",bad_len='0',
                                bad_checksum='0',ttl='32',df='0',
                                no_of_pkts=0,cli_pwd="none",from_glc='1'):



        """Description:This API invo es the tool ip4_pktgen tool and
                        generates packets within the SSX box
            CLI        :CLI used is <ip4_pktgen>
            Input      :Input parameters to the API are different fields
                        in the IP header.argument(range)
                        slot(0-4),port(0-3),src_addr(hex),dst_addr(hex)
                        pktlen(28-2000),ttl(0-255),df(0 or 1),bad_len(0 or 1)
                        bad_checksum(0 or 1)

            Output     :Generates required no of  IP packets with in the SSX
                        box
            Author     :Ganapathi,ganapathi@primesoftsolutionsinc.com
            Reviewer   :           """

        passwd_prompt=re.compile("password:",re.I)
        enable_prompt_regex = "[\r\n]*\S+\[\S+\]#"
        #enabling  level 2 to start shell
        self.ses.sendline("hidden enable 2")
        self.ses.expect(passwd_prompt)
        self.ses.sendline(cli_pwd+'\n')
        if no_of_pkts > 0:
            #running the command start shell
            self.ses.sendline("start shell")
            self.ses.expect('#')
            if card=="GLC":
                telnet_glc(self,telnet_to_glc=from_glc)
            #invoking the tool ip4_pktgen in
            self.ses.sendline("ip4_pktgen")
            self.ses.expect("\r\n(.*)\r\nDo you want to generate packet with optional header fields:\r\n(.*): ")
            self.ses.sendline(options)
            if options == '1':
                self.ses.expect("\r\nGenerate with bad option:\r\n(.*): ")
                self.ses.sendline(bad_option)
            self.ses.expect("Enter the slot number of LC \(0\-4\): ")    
            self.ses.sendline(slot)  
            self.ses.expect("Enter the port number \(0\-3\): ")    
            self.ses.sendline(port)
            self.ses.expect("Enter IPv4 source address in hex:")    
            self.ses.sendline(src_addr)
            self.ses.expect("Enter IPv4 destination address in hex:")     
            self.ses.sendline(dst_addr)
            self.ses.expect("Enter total packet length \(32\-1792\):")   
            self.ses.sendline(pkt_len)
            self.ses.expect("\r\nDo you want to generate packet with bad total length:\r\n(.*): ")
            self.ses.sendline(bad_len)
            self.ses.expect("Enter TTL \(0\-255\): ")     
            self.ses.sendline(ttl)
            self.ses.expect("DF bit \(0\-1\): ")       
            self.ses.sendline(df)
            self.ses.expect("\r\nDo you want to generate packet with bad checksum:\r\n(.*): ")
            self.ses.sendline(bad_checksum)
            while  no_of_pkts > 1:
                self.ses.expect("\r\n(.*)\r\n(.*)\r\nDo you want to send the same packet again:\r\n(.*): ")
                self.ses.sendline("1")
                no_of_pkts = no_of_pkts - 1
            self.ses.sendline("%c" % 0x3)
            self.ses.expect("#")
            self.ses.sendline("exit")
            if card == "GLC":
                self.ses.expect("Connection closed by foreign host.")
                self.ses.expect("#")
                self.ses.sendline("exit")
            self.ses.expect(enable_prompt_regex)
            return  1
        else:
            self.ses.sendline("%c" % 0x3)
            return  0

def get_mgmt_addr(ssx_name="none"):
        """
         This API will return management port address of a given SSX .
         CLI: "nslookup "ssx_name"
         input: ssx-name as a parameter
         output:returns the ip address of mgmt port
         Author:ganapathi@primesoftsolutionsinc.com
         Reviewer:                               """ 


        cmd="nslookup %s >> mgmt.txt" %(ssx_name)
        os.system(cmd)
        fileptr=file("mgmt.txt","r")
        outputstr=fileptr.read()
        regex=re.compile('\nAddress:(\s+)(\d+).(\d+).(\d+).(\d+)\n')
        regex1=re.compile('(\d+)..(\d+).(\d+).(\d+)')
        found=regex.search(outputstr)
        found1=regex1.search(found.group())
        return found1.group() 

def ip_verify_ipv6_counters_icmp(self,total_tx='none',echo_request='none',echo_reply='none',
                                   unreachable='none',param_problem='none', redirects='none',
                                   ttl_expired='none',too_big='none',other='none',format='none',
                                   rate_limit='none',router_solicit='none',
                                   router_advertise='none',neighbor_solicit='none',neighbor_advertise="none"):

        """
          Description: - This API verify the "show ip conters icmp" with passing differnt combinations of
                      transmitted  ICMP packet statastics such as echo request etc with output when the
                      command run.
          CLI Used- CLI.s that are used for the API  <show ip counters icmp>.
          Input: - List of differnt ICMP packet statastics Inputs such as no of Echo Request packets
                        transmitted etc.
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """

        expected={'icmp_echo_request':echo_request,'icmp_echo_reply':echo_reply,
                  'icmp_total':total_tx,'icmp_unreachable':unreachable,
                  'icmp_too_big':too_big,'icmp_param_problem':param_problem,
                  'icmp_router_solicit':router_solicit,'icmp_redirects':redirects,
                  'icmp_router_advertise':router_advertise,'icmp_ttl_expired':ttl_expired,
                  'icmp_other':other,'icmp_format':format,'icmp_rate_limit':rate_limit,
                  'icmp_neighbor_solicit':neighbor_solicit,'icmp_neighbor_advertise':neighbor_advertise}

        cli="show ipv6 counters icmp"
        ret_str=self.cmd(cli)
        #splitted_icmp_list=icmplist.split('\n')
        actual={}
        regex_list=['\s*Rx:\s+Total\s+(?P<rx_total>\d+)\s+Tx:\s+Total\s+(?P<icmp_total>\d+)',
             '\s+Echo\s+Request\s+(?P<rx_echo_request>\d+)\s+Echo\s+Request\s+(?P<icmp_echo_request>\d+)',
             '\s+Echo\s+Reply\s+(?P<rx_echo_reply>\d+)\s+Echo\s+Reply\s+(?P<icmp_echo_reply>\d+)',
             '\s+Unreachable\s+(?P<rx_unreachable>\d+)\s+Unreachable\s+(?P<icmp_unreachable>\d+)',
             '\s+Param\s+Problem\s+(?P<rx_param_problem>\d+)\s+Param\s+Problem\s+(?P<icmp_param_problem>\d+)',
             '\s+Redirects\s+(?P<rx_redirects>\d+)\s+redirects\s+(?P<icmp_redirects>\d+)',
            '\s+TTL\s+Expired\s+(?P<rx_ttl_expired>\d+)\s+TTL\s+Expired\s+(?P<icmp_ttl_expired>\d+)',
            '\s+Too\s+Big\s+(?P<rx_too_big>\d+)\s+Too\s+Big\s+(?P<icmp_too_big>\d+)',
            '\s+Router\s+Solicit\s+(?P<rx_router_solicit>\d+)\s+Router\s+Solicit\s+(?P<icmp_router_solicit>\d+)',
            '\s+Router\s+Advertise\s+(?P<rx_router_advertise>\d+)\s+Router\s+Advertise\s+(?P<icmp_router_advertise>\d+)',
            '\s+Neighbor\s+Solicit\s+(?P<rx_neighbor_solicit>\d+)\s+Neighbor\s+Solicit\s+(?P<icmp_neighbor_solicit>\d+)',
       '\s+Neighbor\s+Advertise\s+(?P<rx_neighbor_advertise>\d+)\s+Neighbor\s+Advertise\s+(?P<icmp_neighbor_advertise>\d+)',
            '\s+Other\s+(?P<rx_other>\d+)\s+Other\s+(?P<icmp_other>\d+)',
            '\s+Error:\s+Checksum\s+(?P<chksum_error>\d+)\s+Format\s+(?P<format_error>\d+)',
            '\s+Length\s+(?P<length_error>\d+)\s+Rate\s+Limit\s+(?P<rate_limit_error>\d+)',
            '\s+Tx\s+Redirect\s+(?P<redirect_error>\d+)']

        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]

        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0
        return 1   



def verify_port_drop_counters(self,port='none',disabled_port='none',
                                  lookup_failed='none',nitrox_drop='none',
                                  known_acl='none',drop_adjacency='none',
                                   invalid_fib='none',invalid_channel='none',
                                  buff_invalid='none',xscale_ring_full='none',
                                   invalid_circuit='none',arp_drop='none',
                                   ip6_port_drop='none',invalid_service='none',
                  v4_chksum_drop='none',v4_hdr_drop='none',v4_scr_drop='none'):
        """
          Description: - This API will verify the o/p stats of packet drops at a particular port
          CLI Used- "show port slot/port counters drop" ---->to catch the name of the particular interface
          Input: -    slot and port as a parameter format slot/port
          Output: -  verifies the output stats of the command
          Author: -  Ganapathi, ganapathi@primesoftsolutionsinc.com .
          Reviewer: -                        """

        expected={'disabled_port':disabled_port,
                  'lookup_failed':lookup_failed,
                  'nitrox_drop'  :nitrox_drop,
                  'known_acl'    :known_acl,
                  'drop_adjacency':drop_adjacency,
                 'invalid_fib':invalid_fib,
                  'invalid_channel':invalid_channel,
                  'buff_invalid':buff_invalid,
                  'xscale_ring_full':xscale_ring_full,
                  'invalid_circuit':invalid_circuit,
                  'arp_drop':arp_drop,
                  'ip6_port_drop':ip6_port_drop,
                  'invalid_service':invalid_service,
                  'v4_chksum_drop':v4_chksum_drop,
                  'v4_hdr_drop':v4_hdr_drop,
                  'v4_scr_drop': v4_scr_drop }
        actual={}
        ret_str=self.cmd("show port %s counters drop" %(port))
        regex_list=['\d+/\d+\s+Disabled\s+Port:\s+(?P<disabled_port>\d+)',
                    '\s+Lookup\s+Failed:\s+(?P<lookup_failed>\d+)',
                    '\s+Nitrox\s+Drop:\s+(?P<nitrox_drop>\d+)',
                    '\s+Known\s+Acl:\s+(?P<known_acl>\d+)',
                    '\s+Drop\s+Adjacency:\s+(?P<drop_adjacency>\d+)',
                    '\s+Invalid\s+Fib:\s+(?P<invalid_fib>\d+)',
                    '\s+Invalid\s+Channel:\s+(?P<invalid_channel>\d+)'
                    '\s+Buff\s+Invalid:\s+(?P<buff_invalid>\d+)' 
                    '\s+Xscale\s+Ring\s+Full:\s+(?P<xscale_ring_full>\d+)',
                    '\s+Invalid\s+Circuit:\s+(?P<invalid_circuit>\d+)',
                    '\s+Arp\s+Drop:\s+(?P<arp_drop>\d+)', 
                    '\s+Ip6\s+Port\s+Drop:\s+(?P<ip6_port_drop>\d+)',
                    '\s+Invalid\s+Service:\s+(?P<invalid_service>\d+)',
                    '\s+V4\s+Chksum\s+Drop:\s+(?P<v4_chksum_drop>\d+)',
                    '\s+V4\s+Hdr\s+Invalid:\s+(?P<v4_hdr_drop>\d+)',
                    '\s+V4\s+Scr\s+Invalid:\s+(?P<v4_scr_drop>\d+)']

        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]
        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    return 0
        return 1
       

def verify_tunnel_counters(self,tunnel_name="none",in_pkts='none',out_pkts='none'): 

        ret_str=self.cmd("show tunnel counters  " )
        split_list=ret_str.split('\n')
        ret_str=self.cmd("show tunnel counters | grep %s  "  %(tunnel_name))
        str2 ='\s*\w+\s+\w+\s+(\d+)\s+(\d)+\s+\d+\s+\d+'
        obj=re.compile(str2)
        found=obj.search(ret_str)
        actual_in_pkts=found.group(1)
        actual_out_pkts=found.group(2)
        if actual_in_pkts == in_pkts  and actual_out_pkts == out_pkts:
            return 1
        else:
            return 0

def get_circuit_handle(self,tunnel="none"):

        ret_str=self.cmd("show tunnel name %s" %(tunnel))
        obj=re.compile('\s*Tunnel\s+Circuit\s+Handle\s+(\w+)')
        m=obj.search(ret_str)
        return m.group() 
 
