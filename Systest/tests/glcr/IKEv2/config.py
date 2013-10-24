import topo
# Frame-work libraries
from SSX import *
from Linux import *
from ixia import *
from CISCO import *
from log import *
from glcr import *
from lanlan import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
import pexpect
from logging import getLogger
from helpers import is_healthy
import re, time

script_var1={}

script_var1['context_name'] = 'glcr'


####### Mention IP addresses here ######################################
script_var1['rad_server1'] = "192.168.1.1"
script_var1['port_no2'] = '1822'
script_var1['server_key'] = 'topsecret'
script_var1['ipsec_loopback_ip1'] = '15.2.2.2'
script_var1['ipsec_loopback_ip1/mask'] = '15.2.2.2/32'
script_var1['session_ip1'] = '66.66.66.1'
script_var1['session_ip1/mask'] = '66.66.66.1/16'
script_var1['client_ssx_ip1'] = '10.37.10.2'
script_var1['client_ssx_ip1/mask'] = '10.37.10.2/24'
script_var1['client_ssx_ip1_red'] = '192.168.35.2'
script_var1['client_ssx_ip1_red/mask'] = '192.168.35.2/24'
script_var1['service_ssx_ip1'] = '192.168.110.2'
script_var1['service_ssx_ip1/mask'] = '192.168.110.2/24'
script_var1['service_ssx_ip1_red'] = '192.168.130.2'
script_var1['service_ssx_ip1_red/mask'] = '192.168.130.2/24'
script_var1['ssx_ixia_ip'] = '18.1.1.2'
script_var1['ssx_ixia_ip/mask'] = '18.1.1.2/24'
script_var1['sst_ixia_ip'] = '19.1.1.2'
script_var1['sst_ixia_ip/mask'] = '19.1.1.2/24'
script_var1['sst_ip'] = '15.2.2.1'


################### CISCO IP's #####################################################
script_var1['client_cisco_ip1'] = "10.37.10.1"
script_var1['client_cisco_ip1/mask'] = "10.37.10.1 255.255.255.0"
script_var1['client_cisco_ip1_red'] = "192.168.35.1"
script_var1['client_cisco_ip1_red/mask'] = "192.168.35.1 255.255.255.0"
script_var1['service_cisco_ip1'] = "192.168.110.1"
script_var1['service_cisco_ip1/mask'] = "192.168.110.1 255.255.255.0"
script_var1['service_cisco_ip1_red'] = "192.168.130.1"
script_var1['service_cisco_ip1_red/mask'] = "192.168.130.1 255.255.255.0"
script_var1['ssx_cisco_4ixia'] = "18.1.1.1 255.255.255.0"
script_var1['ssx_cisco_4ixia_ip'] = "18.1.1.1"
script_var1['sst_cisco_4ixia'] = "19.1.1.1 255.255.255.0"
script_var1['sst_cisco_4ixia_ip'] = "19.1.1.1"
script_var1['cisco_ixia_4ssx_ip'] = "30.210.1.3 255.255.255.0"
script_var1['cisco_ixia_4sst_ip'] = "10.210.1.3 255.255.255.0"
script_var1['sst_cisco_ip'] = "15.2.2.3 255.255.255.0" 
script_var1['radius_ip'] = "192.168.1.1 255.255.255.0"


################### Misc Variables #####################################################
script_var1['no_of_sessions1'] = "2000"
script_var1['max_sessions_glc'] = "60000"
script_var1['psk_key'] = 'SBM_demo'
script_var1['ph1_hard_lifetime'] =  '130'
script_var1['ph1_soft_lifetime'] = '129'
script_var1['ph2_hard_lifetime'] = '121'
script_var1['ph2_soft_lifetime'] = '120'
script_var1['logical_slot_100'] = "100"
script_var1['logical_slot_101'] = "101"

############################# Port Detail #########################
script_var1['port1_ssx_ClntCisco'] = topo.p1_ssx_clntCisco[0]
script_var1['port3_ssx_ClntCisco'] = topo.p3_ssx_clntCisco[0]
script_var1['port1_ssx_servCisco'] = topo.p1_ssx_servCisco[0]
script_var1['port3_ssx_servCisco'] = topo.p3_ssx_servCisco[0]
script_var1['port1_ClntCisco_ssx'] = topo.p1_ssx_clntCisco[1]
script_var1['port3_ClntCisco_ssx'] = topo.p3_ssx_clntCisco[1]
script_var1['port1_servCisco_ssx'] = topo.p1_ssx_servCisco[1]
script_var1['port3_servCisco_ssx'] = topo.p3_ssx_servCisco[1]
script_var1['port_servCisco_rad'] = topo.p_servCisco_radius1[0]
script_var1['ssx_to_ixia'] = topo.p1_ssx_ixia[0]
script_var1['ssx_to_cisco4ixia'] = topo.p1_ssx_ixia[1]
script_var1['sst_to_cisco4ixia'] = topo.p1_sst_ixia[1]
script_var1['cisco_ixia_4ssx'] = topo.p2_cisco_ixia[0]
script_var1['cisco_ixia_4sst'] = topo.p1_cisco_ixia[0]
script_var1['sst_cisco'] = topo.p1_sst_clntCisco[1]
######################## VLAN detail ##############################
script_var1['vlan_ClntCisco1'] = '931'
script_var1['vlan_ServCisco1'] = '936'
script_var1['vlan_ClntCisco3'] = '961'
script_var1['vlan_ClntCisco4'] = '962' 
script_var1['vlan_ServCisco3'] = '966'
script_var1['vlan_ServCisco4'] = '967'
#script_var1[''] = 
############################# SST Port Detail #####################
script_var1['sst_port1'] = topo.p1_sst_clntCisco[0]
script_var1['sst_ixia'] = topo.p1_sst_ixia[0]

################### SST and SSX Logic for generating the ip address
#as per the SST design for IKEv2 Sessions.
script_var1['sst_slot1'] = script_var1['port1_ssx_ClntCisco'].split('/')[0]
script_var1['sst_slot1_port1'] = script_var1['port1_ssx_ClntCisco'].split('/')[1]

######################## ADD your routes here #####################
#script_var1['sst_route1'] = 
#script_var1['route_to_sst1'] = 
script_var1['route_server'] = '192.168.150.0/24'
script_var1['smb1_route1'] = '30.210.0.0/16'
script_var1['smb1_route2'] = '30.211.0.0/16'
script_var1['smb2_route1'] = '10.210.0.0/16'
script_var1['smb2_route2'] = '10.211.0.0/16'
script_var1['sst_ph1_hard'] = '120'
script_var1['sst_ph1_soft'] = '119'
script_var1['sst_ph2_hard'] = '110'
script_var1['sst_ph2_soft'] =  '109'
script_var1['lp_route'] = '15.2.0.0/16'
script_var1['ip_pool_route1'] = '30.210.0.0/16'
script_var1['ip_pool_route1/mask'] = '30.210.0.0 255.255.0.0'
script_var1['ip_pool_route2'] = '10.210.0.0/16'
script_var1['ip_pool_route2/mask'] = '10.210.0.0 255.255.0.0'
script_var1['radius_route'] = '192.168.1.0/24'
script_var1['ssx_route'] = '10.37.10.0/24'

############### Configuration ###########################################
script_var1['GLCR_FUN_NEW_001'] = """
aaa global profile
 default-domain authentication %(context_name)s
 default-domain authorization local
 exit
context %(context_name)s
aaa profile
session authentication radius
  exit
 radius session authentication profile
  algorithm round-robin
  server %(rad_server1)s port %(port_no2)s key %(server_key)s
  exit
 ip pool 10.210.0.0 1024
 interface ipsec_lp1 loopback
 ip address %(ipsec_loopback_ip1/mask)s
 exit
 interface subs session
 ip session-default
 ip address %(session_ip1/mask)s
 exit
 interface clnt_cisco1
  arp arpa
  ip address %(client_ssx_ip1/mask)s
  exit
 interface clnt_cisco2
 arp arpa 
 ip address %(client_ssx_ip1_red/mask)s
 exit
 interface service_cisco1
 arp arpa 
 ip address %(service_ssx_ip1/mask)s
 exit
 interface service_cisco2
 arp arpa
 ip address %(service_ssx_ip1_red/mask)s
 exit
 interface to_ixia
 arp arpa
 ip address %(ssx_ixia_ip/mask)s
 exit
 ip route %(sst_slot1)s.%(sst_slot1_port1)s.0.0/16  %(client_cisco_ip1)s admin-distance 10
 ip route %(sst_slot1)s.%(sst_slot1_port1)s.0.0/16 %(client_cisco_ip1_red)s admin-distance 20
 ip route 15.%(sst_slot1)s.%(sst_slot1_port1)s.1/32 %(client_cisco_ip1)s admin-distance 10
 ip route 15.%(sst_slot1)s.%(sst_slot1_port1)s.1/32 %(client_cisco_ip1_red)s admin-distance 20
 ip route %(radius_route)s %(service_cisco_ip1)s admin-distance 10
 ip route %(radius_route)s %(service_cisco_ip1_red)s admin-distance 20
 ip route %(ip_pool_route2)s %(client_cisco_ip1)s admin-distance 10
 ip route %(ip_pool_route2)s %(client_cisco_ip1_red)s admin-distance 20
 ip route %(ip_pool_route1)s %(ssx_cisco_4ixia)s 
 #Need to add routes 
 ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk %(psk_key)s
   peer-authentication eap
   hard-lifetime %(ph1_hard_lifetime)s hours
   soft-lifetime %(ph1_soft_lifetime)s hours
   exit
  exit
ipsec policy ikev2 phase2 name ph2
  suite1
   hard-lifetime %(ph2_hard_lifetime)s hours
   soft-lifetime %(ph2_soft_lifetime)s hours
   exit
  exit
 exit
session-home slot 100 loopback interface ipsec_lp1 %(context_name)s
ipsec policy ikev2 phase1 name ph1
ipsec policy ikev2 phase2 name ph2
exit
port ethernet %(port1_ssx_ClntCisco)s dot1q
vlan %(vlan_ClntCisco1)s
bind interface clnt_cisco1 %(context_name)s
exit
service ipsec
exit
enable
exit
port ethernet %(port1_ssx_servCisco)s dot1q
vlan %(vlan_ServCisco1)s
bind interface service_cisco1 %(context_name)s
   exit
  exit
 enable
 exit
port ethernet %(port3_ssx_ClntCisco)s dot1q
vlan %(vlan_ClntCisco3)s
bind interface clnt_cisco2 %(context_name)s
exit
service ipsec
exit
enable
exit
port ethernet %(port3_ssx_servCisco)s dot1q
vlan %(vlan_ServCisco3)s
bind interface service_cisco2 %(context_name)s
exit
exit
enable
exit
port ethernet %(ssx_to_ixia)s
bind interface to_ixia %(context_name)s
exit
exit
enable
exit
"""%(script_var1)

#####################################################################

script_var1['GLCR_FUN_NEW_SST_001'] = """
context local
interface cisco1
arp arpa
ip address 15.%(sst_slot1)s.%(sst_slot1_port1)s.1/28
exit
interface to_ixia
arp arpa
ip address %(sst_ixia_ip/mask)s
exit
 ip route %(ssx_route)s %(sst_cisco)s
 ip route %(ip_pool_route1)s %(sst_cisco)s
 ip route %(ip_pool_route2)s %(sst_cisco_4ixia)s
 ipsec policy ikev2 phase1 name ph1_aes
  suite1
   gw-authentication psk %(psk_key)s
   peer-authentication eap
   hard-lifetime %(sst_ph1_hard)s hours
   soft-lifetime %(sst_ph1_soft)s hours
   exit
  exit
 ipsec policy ikev2 phase2 name ph2_aes
  suite1
   hard-lifetime %(sst_ph2_hard)s hours
   soft-lifetime %(sst_ph2_soft)s hours
   exit
  exit
 exit
port ethernet %(sst_port1)s
 bind interface cisco1 local
  ipsec policy ikev2 phase1 name ph1_aes
  ipsec policy ikev2 phase2 name ph2_aes
  exit
 service ipsec
 enable
 exit
port ethernet %(sst_ixia)s
 bind interface to_ixia local
 exit
 enable
 exit
"""%(script_var1)

#print script_var1['GLCR_FUN_NEW_001']
#print script_var1['GLCR_FUN_NEW_SST_001']
def configure_cisco (self,cisco):

	#Configure the Swicth
        self.myLog.info("Configuring the Cisco")
	self.cisco.cmd("conf t")
        self.cisco.cmd("ip routing")
        self.cisco.cmd("end")
        self.myLog.info("cleanUp the required interfaces")
	self.cisco.clear_interface_config(intf=topo.p1_ssx_clntCisco[1])
	self.cisco.clear_interface_config(intf=topo.p3_ssx_clntCisco[1])
	self.cisco.clear_interface_config(intf=topo.p1_ssx_servCisco[1])
	self.cisco.clear_interface_config(intf=topo.p3_ssx_servCisco[1])
	self.cisco.clear_interface_config(intf=topo.p_servCisco_radius1[0])
	self.cisco.clear_interface_config(intf=topo.p1_sst_clntCisco[1])
	self.cisco.clear_interface_config(intf=topo.p1_sst_ixia[1])
	self.cisco.clear_interface_config(intf=topo.p1_ssx_ixia[1])
	self.cisco.clear_interface_config(intf=topo.p1_cisco_ixia[0])
	self.cisco.clear_interface_config(intf=topo.p2_cisco_ixia[0])

	self.myLog.info("Adding required vlans to database")
        self.cisco.cmd("vlan database")
	self.cisco.cmd("vlan %s"%script_var1['vlan_ClntCisco1'])
	self.cisco.cmd("vlan %s"%script_var1['vlan_ServCisco1'])
	self.cisco.cmd("vlan %s"%script_var1['vlan_ClntCisco3'])
	self.cisco.cmd("vlan %s"%script_var1['vlan_ClntCisco4'])
	self.cisco.cmd("vlan %s"%script_var1['vlan_ServCisco3'])
	self.cisco.cmd("vlan %s"%script_var1['vlan_ServCisco4'])
	self.cisco.cmd("exit")

	#Configure the interfaces
	self.cisco.cmd("conf t")
	self.cisco.cmd("interface vlan %s"%script_var1['vlan_ClntCisco1'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%script_var1['client_cisco_ip1/mask'])
	self.cisco.cmd("exit")
	
	self.cisco.cmd("interface vlan %s"%script_var1['vlan_ServCisco1'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%script_var1['service_cisco_ip1/mask'])
	self.cisco.cmd("exit")

	self.cisco.cmd("interface vlan %s"%script_var1['vlan_ClntCisco3'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%script_var1['client_cisco_ip1_red/mask'])
	self.cisco.cmd("exit")

	self.cisco.cmd("interface vlan %s"%script_var1['vlan_ServCisco3'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%script_var1['service_cisco_ip1_red/mask'])
	self.cisco.cmd("end")

	self.cisco.cmd("conf t")
	self.cisco.cmd("interface giga %s"%script_var1['port1_ClntCisco_ssx'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%script_var1['vlan_ClntCisco1'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%script_var1['vlan_ClntCisco1'])
	self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("exit")

	self.cisco.cmd("interface giga %s"%script_var1['port3_ClntCisco_ssx'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%script_var1['vlan_ClntCisco3'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%script_var1['vlan_ClntCisco3'])
	self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("exit")

	self.cisco.cmd("interface giga %s"%script_var1['port1_servCisco_ssx'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%script_var1['vlan_ServCisco1'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%script_var1['vlan_ServCisco1'])
	self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("exit")

	self.cisco.cmd("interface giga %s"%script_var1['port3_servCisco_ssx'])
	self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%script_var1['vlan_ServCisco3'])
	self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%script_var1['vlan_ServCisco3'])
	self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("end")

        self.myLog.info("Creating the vrf for service end")
	self.cisco.cmd("conf t")
        self.cisco.cmd("ip vrf ospf")
        self.cisco.cmd("rd 111:1")
        self.cisco.cmd("ip vrf test")
        self.cisco.cmd("rd 123:1")

	self.cisco.cmd("interface giga %s"%script_var1['ssx_to_cisco4ixia'])
	self.cisco.cmd("ip vrf forwarding ospf")
	self.cisco.cmd("ip address %s"%script_var1['ssx_cisco_4ixia'])
	self.cisco.cmd("exit")
	
	self.cisco.cmd("interface giga %s"%script_var1['sst_to_cisco4ixia'])
	self.cisco.cmd("ip vrf forwarding test")
	self.cisco.cmd("ip address %s"%script_var1['sst_cisco_4ixia'])
	self.cisco.cmd("exit")

	self.cisco.cmd("interface giga %s"%script_var1['cisco_ixia_4ssx'])
	self.cisco.cmd("ip vrf forwarding ospf")
	self.cisco.cmd("ip address %s"%script_var1['cisco_ixia_4ssx_ip'])
	self.cisco.cmd("exit")

	self.cisco.cmd("interface giga %s"%script_var1['cisco_ixia_4sst'])
	self.cisco.cmd("ip vrf forwarding test")
	self.cisco.cmd("ip address %s"%script_var1['cisco_ixia_4sst_ip'])
	self.cisco.cmd("exit")
	
	self.cisco.cmd("interface giga %s"%script_var1['sst_cisco'])
	self.cisco.cmd("ip address %s"%script_var1['sst_cisco_ip'])
	self.cisco.cmd("exit")	
	
	self.cisco.cmd("interface giga %s"%script_var1['port_servCisco_rad'])
	self.cisco.cmd("ip address %s"%script_var1['radius_ip'])
	self.cisco.cmd("exit")	


	#Adding the routes
	self.cisco.cmd("ip route %s %s"%(script_var1['ip_pool_route2/mask'],script_var1['sst_ip']))	
	self.cisco.cmd("ip route %s %s 10"%(script_var1['ip_pool_route1/mask'],script_var1['client_ssx_ip1']))	
	self.cisco.cmd("ip route %s %s 20"%(script_var1['ip_pool_route1/mask'],script_var1['client_ssx_ip1_red']))	
	
	self.cisco.cmd("ip route vrf ospf %s %s"%(script_var1['ip_pool_route2/mask'],script_var1['ssx_ixia_ip']))
        self.cisco.cmd("ip route vrf test %s %s"%(script_var1['ip_pool_route1/mask'],script_var1['sst_ixia_ip'])) 
	self.cisco.cmd("end")
	


	


