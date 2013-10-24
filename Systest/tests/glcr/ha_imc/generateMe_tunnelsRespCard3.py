#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: To generate tunnels for Initiator
TEST PLAN:
TEST CASE: Performance TCs
						   1 	     2	    3	      4		  5		6	     7
HOW TO RUN: python2.5 genrateMe_tunnelsResp.py <max_tun> <context> <startIp> <localIp> <route-Y/N> <trafficRt> <remoteStartIp>
AUTHOR: rajshekar@stoke.com
REVIEWER: krao@stoke.com

"""

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


#Import config and topo files
from config import *
from topo import *

max_tun = int(sys.argv[1])
context = sys.argv[2]
a, b, c, d = sys.argv[3].split('.')   # This is for tunnel interfaces 
localIp = sys.argv[4]
routeOption = sys.argv[5].lower()
p, q, r, s = sys.argv[6].split('.')   # This is traffic selector for tunnel at Responder
w, x, y, z = sys.argv[7].split('.')   # This is for remote Ip generation, this logic should match with the Initiator IP Generator

# Convert to int for str
a = int(a) ; b = int(b) ; c = int(c) ; d = int (d)
p = int(p) ; q = int(q) ; r = int(r) ; s = int (s)
w = int(w) ; x = int(x) ; y = int(y) ; z = int (z)

# Configuratioon starts
print "system hostname %s"%topo.ssx_resp['hostname']
print "ipsec global profile"
print "dpd interval %s retry-interval %s maximum-retries %s"%(haimc_var['dpd_interval'], haimc_var['retry_interval'], haimc_var['dpd_maximum_retries'])
print "retransmit interval %s maximum-retries %s send-retransmit-response"%(haimc_var['retransmit_interval'], haimc_var['sess_max_retries'])
print "exit"
print "context %s"%haimc_var['context2']
print "interface transport"
print "arp arpa"
print "arp refresh"
print "ip address %s"%haimc_var['active_slot3_ip/mask']
print "exit"
print "interface transback"
print "arp arpa"
print "arp refresh"
print "ip address %s"%haimc_var['standby_4slot3_ip/mask']
print "exit"
print "interface service"
print "arp arpa"
print "arp refresh"
print "ip address %s"%haimc_var['rad_intf_4slot3_ip/mask']
print "exit"
print "interface serback"
print "arp arpa"
print "arp refresh"
print "ip address %s"%haimc_var['bkp_rad_intf_4slot3_ip/mask']
print "exit"
print "interface lpbk-1 loopback"
print "ip address %s/32"%localIp
print "exit"
print "ipsec policy ikev2 phase1 name ikev2_phase1"
print "suite1"
print "gw-authentication psk %s"%haimc_var['psk_key']
print "peer-authentication psk"
print "hard-lifetime %s secs"%haimc_var['phase1_soft_life']
print "soft-lifetime %s secs"%haimc_var['phase1_hard_life']
print "exit"
print "exit"
print "ipsec policy ikev2 phase2 name ikev2_phase2"
print "suite1"
print "hard-lifetime %s secs"%haimc_var['phase2_soft_life']
print "soft-lifetime %s secs"%haimc_var['phase2_hard_life']
print "exit"
print "exit"
print "rtr %s"%haimc_var['rtr_id2']
print "type echo protocol ipicmpecho %s source %s"%(haimc_var['cisco_active_slot3_ip'],haimc_var['active_slot3_ip'])
print "exit"
print "rtr schedule %s"%haimc_var['rtr_id2']
print "initiator-policy pol1"
print "retry-interval 10"
print "retry-number 30"
print "hold-off-interval 1200"
print "exit"
if routeOption == 'y':
	print "ip route %s %s track %s"%(haimc_var['routes_to_ini_ip_slot3'], haimc_var['cisco_active_slot3_ip'],haimc_var['rtr_id2'])
	print "ip route %s %s admin-distance 20"%(haimc_var['routes_to_ini_ip_slot3'], haimc_var['cisco_standby_4slot3_ip'])
	print "ip route %s %s"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_rad_intf_4slot3_ip'])
	print "ip route %s %s admin-distance 20"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_bkp_rad_intf_4slot3_ip'])
	print "ip route %s %s track %s"%(haimc_var['dummy_intf_routes_slot3'], haimc_var['cisco_active_slot3_ip'],haimc_var['rtr_id2'])
	print "ip route %s %s admin-distance 20"%(haimc_var['dummy_intf_routes_slot3'], haimc_var['cisco_standby_4slot3_ip'])
#print "ip route %s/32 %s"%(remoteIp, nextHop)
print "exit"

# Session home config
print "session-home slot 101 loopback interface lpbk-1 %s"%haimc_var['context2']
print "ipsec session context name %s"%haimc_var['context2']
print "ipsec policy ikev2 phase1 name ikev2_phase1"
print "ipsec policy ikev2 phase2 name ikev2_phase2"
print "exit"
d = d + 1
z = z + 1
for i in xrange(max_tun):
    if c == 255:
       b += 1
       c = 1
    if b == 255:
       a += 1
       b = 1
    c += 1

    if not (a == 127):
	print "context %s"%haimc_var['context2']
        print "interface resp_tun%d tunnel"%i
        print "ip address %d.%d.%d.%d/32"%(a,b,c,d)
        print "exit"
	print "exit"
        print "tunnel %s_tun%d type ipsec protocol ip44 context %s"%(haimc_var['context2'], i, haimc_var['context2'])
        print "enable"
        print "tunnel-setup-role initiator-responder initiator-policy pol1"
       	if y == 255:
       		x += 1
       		y = 1
    	if x == 255:
       		w += 1
       		x = 1
    	y += 1

	print "ip local %s remote %d.%d.%d.%d"%(localIp, w, x, y, z)
	print "bind interface resp_tun%s %s"%(i, haimc_var['context2'])
	if s == 256:
		r += 1
		s = 0
	if r == 256:
		q += 1
		r = 0
	if q == 256:
		p += 1
		q = 0
	print "ip route %d.%d.%d.%d/32"%(p, q, r, s)
	s += 1
	print "exit"
	print "ipsec policy ikev2 phase1 name ikev2_phase1"
	print "exit"
	print "ipsec policy ikev2 phase2 name ikev2_phase2"
	print "exit"


# To bind transport and service interfaces
print "port ethernet %s dot1q"%haimc_var['port_ssx_active_4slot3']
print "vlan %s"%haimc_var['vlan4slot3']
print "bind interface transport %s"%haimc_var['context2']
print "exit"
print "service ipsec"
print "exit"
print "enable"
print "exit"
print "port ethernet %s dot1q"%haimc_var['port_ssx_rad_intf_4slot3']
print "vlan %s"%haimc_var['service_vlan4slot3']
print "bind interface service %s"%haimc_var['context2']
print "exit"
print "exit"
print "enable"
print "exit"
print "port ethernet %s dot1q"%haimc_var['port_ssx_standby_4slot3']
print "vlan %s"%haimc_var['standby_vlan4slot3']
print "bind interface transback %s"%haimc_var['context2']
print "exit"
print "service ipsec"
print "exit"
print "enable"
print "exit"
print "port ethernet %s dot1q"%haimc_var['port_ssx_bkp_rad_intf_4slot3']
print "vlan %s"%haimc_var['serback_vlan4slot3']
print "bind interface serback %s"%haimc_var['context2']
print "exit"
print "exit"
print "enable"
print "exit"

