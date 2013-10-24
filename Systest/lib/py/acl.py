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
from StokeTest import test_case

def int2bin(self, n, count=24):
	return "".join([str((int(n) >> y) & 1) for y in range(count-1, -1, -1)])


def verify_port_counters(self,cmd,igmppackets):

	out=cmd.split()[21]
	if int(out) >= int(igmppackets):
		return 1
	else:
		return 0		     	 	


def verify_telnet_from_ssx(self, linux_ip="10.1.1.2", username="regress", password="gleep7",timeout=None):
        ''' API To Verify Telnet from SSX to Linux'''

        self.ses.sendline("telnet %s" %linux_ip)
        log.debug("Trying to connect to Linux: %s" %(linux_ip))
        if not self.ses.expect("ogin:"):
                self.ses.sendline(username)
        if not self.ses.expect("assword:"):
                self.ses.sendline(password)
	expect_output = self.ses.expect(["bash"],50)
	if expect_output == 1:
		log.debug("Login to SSX port %s successful" %ssx_ip)
        if timeout:
                log.debug("Idle Time %s secs" %timeout)
                time.sleep(int(timeout))
                self.ses.expect(["closed"],50)
                log.debug(" Telnet Session Terminated By Linux")
                return True

        elif timeout == None:
                log.debug("Exit From Telnet")
                command = "exit"
                self.ses.sendline(command)
                return True

        expect_output = self.ses.expect(["incorrect"],50)
        if expect_output == 1:
                log.debug("Invalid user / password")
                return False


def verify_telnet_to_ssx(self, ssx_ip="10.1.1.2", username="user1@local", password="user1",timeout=None):
	'''API to Verify telnet to SSX'''
        self.ses.sendline("telnet %s" %ssx_ip)
        log.debug("Trying to connect to SSX: %s" %(ssx_ip))
        if not self.ses.expect("sername:"):
                self.ses.sendline(username)
        if not self.ses.expect("assword:"):
                self.ses.sendline(password)
        expect_output = self.ses.expect(["[#,>]","sername:"],50)
        if expect_output == 1:
                log.debug("Invalid user / password")
                return False
        log.debug("Login to SSX port %s successful" %ssx_ip)
        if timeout:
                log.debug("Idle time %s secs" %timeout)
                time.sleep(int(timeout))
                self.ses.expect(["closed"],50)
                log.debug(" Telnet Session Terminated By SSX")
                return True

        elif timeout == None:
                log.debug("Exit From Telnet")
                command = "exit"
                self.ses.sendline(command)
                return True
        else :
                return False

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
                  'icmp_other':other,'format_error':format,'rate_limit_error':rate_limit}

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
                  'icmp_other':other,'format_error':format,'rate_limit_error':rate_limit,
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

def verify_access_list_counters(self,al_name="subacl", permit_in="0", deny_in="0", redirect_in="0", permit_out="0", deny_out="0") :
	counter_data=self.cmd("show ip access-list name %s counters"%al_name)
	counter_data=counter_data.split('\n')
	print counter_data
	if counter_data[0] == '\r':
		counter_data.pop(0)
	counter_data=counter_data[1]
	counter_data=counter_data.split()
	if counter_data[0] != permit_in :
		return False
	if counter_data[1] != deny_in :
		return False
	if counter_data[2] != redirect_in :
		return False
	if counter_data[3] != permit_out :
		return False
	if counter_data[4] != deny_out :
		return False
	return True

	




