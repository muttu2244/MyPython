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
						   1 		2		3		4		5	6	   7		  8		9
HOW TO RUN: python2.5 genrateMe_tunnels4Ini.py <max_tun> <context_name> <dummyIntfStartIP> <tunStartIP> <transportIp> <nextHop> <dummyPort> <transportPort> <TrafficRT> <remoteIp>
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
a, b, c, d = sys.argv[3].split('.')   # This is for Dummy interfaces [4094 vlans]
w, x, y, z = sys.argv[4].split('.')   # This is for Tunnel interfaces
transportIp = sys.argv[5]
nextHop = sys.argv[6]
dummyPort = sys.argv[7]
bind2Port = sys.argv[8]
p, q, r, s = sys.argv[9].split('.')   # This is traffic selector for tunnel.
remoteIp = sys.argv[10]

# Convert to int for str
p = int(p) ; q = int(q) ; r = int(r) ; s = int (s)
a = int(a) ; b = int(b) ; c = int(c) ; d = int (d)
w = int(w) ; x = int(x) ; y = int(y) ; z = int (z)

# Let me write common stuffs first
print "system hostname %s"%topo.ssx_ini['hostname']
print "ipsec global profile"
print "dpd interval %s retry-interval %s maximum-retries %s"%(haimc_var['dpd_interval'], haimc_var['retry_interval'], haimc_var['dpd_maximum_retries'])
print "retransmit interval %s maximum-retries %s send-retransmit-response"%(haimc_var['retransmit_interval'], haimc_var['sess_max_retries'])
print "exit"
print "context %s"%context
print "interface transport"
print "arp arpa"
print "arp refresh"
print "ip address %s"%transportIp
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
print "initiator-policy INITIATOR_PLAN"
print "retry-interval 10"
print "retry-number 30"
print "hold-off-interval 10"
print "exit"
print "ip route %s/32 %s"%(remoteIp, nextHop)
print "exit"


# Logic to generate the tunnel
d = d + 1
for i in xrange(max_tun):
    if c == 255:
       b += 1
       c = 1
    if b == 255:
       a += 1
       b = 1
    c += 1

    if not (a == 127):
	print "context %s"%context
	print "interface %s"%i
	print "arp arpa"
	print "arp refresh"
	print "ip address %d.%d.%d.%d/24"%(a,b,c,d)
	print "exit"

    z = z + 1
    if z == 255:
       y += 1
       z = 1
    if y == 255:
       x += 1
       y = 1
   
    if not (w == 127): 
        print "interface Ini_tun%d tunnel"%i
        print "ip address %d.%d.%d.%d/32"%(w,x,y,z)
        print "exit"
	print "exit"
        print "tunnel %s_tun%d type ipsec protocol ip44 context %s"%(context, i, context)
        print "enable"
        print "tunnel-setup-role initiator-responder initiator-policy INITIATOR_PLAN"
	print "ip local %d.%d.%d.%d remote %s"%(a, b, c, d, remoteIp)
	print "bind interface Ini_tun%s %s"%(i, context)
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


# To bind dummy interfaces to port
print "port ethernet %s dot1q"%bind2Port
print "vlan %s"%haimc_var['ini_vlan4slot3']
print "bind interface transport %s"%context
print "exit"
print "service ipsec"
print "exit"
print "enable"
print "exit"
print "port ethernet %s dot1q"%dummyPort
print "enable"

for i in xrange(max_tun):
	print "vlan %s"%i
	print "bind interface %s %s"%(i, context)
	print "exit"
	print "service ipsec"
	print "exit"	
