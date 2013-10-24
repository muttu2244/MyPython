## This file contains the configuration and IP address information of the devices ##
import topo
import topo_glcr
docomo_var = {}

docomo_var['context_name'] = "DoCoMo"
docomo_var['ssx_clnt_ip/mask'] = "17.1.1.2/16"
docomo_var['ssx_clnt_ip'] = "17.1.1.2"
docomo_var['clnt_ssx_ip/mask'] = "17.1.1.1/16"
docomo_var['clnt_ssx_ip'] = "17.1.1.1"
docomo_var['ip_netmask']        ="255.255.255.255"
docomo_var['ip_pool'] = "11.11.11.10"
docomo_var['ses_lo_ip'] = "4.4.4.4"
docomo_var['ssx_ses_ip']=       '11.11.11.1'
docomo_var['ssx_ses_ip_mask']=  '11.11.11.1/24'
docomo_var['ssx_phy_ip1']=      '10.1.1.1'
docomo_var['ssx_phy_ip1_mask']= '10.1.1.1/16'
docomo_var['ssx_rad1_ip']=  '19.1.1.21'
docomo_var['ssx_rad1_ip_mask']=  '19.1.1.21/24'
docomo_var['ssx_rad2_ip']=  '13.1.1.21'
docomo_var['ssx_rad2_ip_mask']=  '13.1.1.21/24'
docomo_var['xpress_netmask'] = '255.255.255.0'
docomo_var['radius_netmask'] = '255.255.255.0'
docomo_var['xpress_phy_iface1_ip'] = '17.1.2.1'
docomo_var['vgroup_phy_iface1_ip'] = '17.1.1.1'
docomo_var['xpress_phy_iface1_ip_mask'] = '17.1.1.1/16'
docomo_var['radius1_ip'] = '19.1.1.1'
docomo_var['radius2_ip'] = '13.1.1.1'
docomo_var['radius1_ip_mask']='19.1.1.1/24'           
docomo_var['radius2_ip_mask']='13.1.1.1/24'           
docomo_var['radius1_route']='19.1.1.0/24'
docomo_var['radius2_route']='13.1.1.0/24'           

# Port information.
docomo_var['port_ssx_linux1']=topo.port_ssx_linux1[0]
docomo_var['port_linux1_ssx']=topo.port_ssx_linux1[1]
docomo_var['ip_pool_mask'] = "11.11.11.10/32"

docomo_var['port_ssx_radius1']=topo.port_ssx_radius1[0]
docomo_var['port_radius1_ssx']=topo.port_ssx_radius1[1]
docomo_var['port_ssx_linux2']=topo.port_ssx_radius1[0]
docomo_var['port_linux2_ssx']=topo.port_ssx_radius1[1]

# Configuration Starts
##############################################################

docomo_var['DoCoMo_6_1_2'] = """context %(context_name)s
ip pool %(ip_pool)s 20
 interface clnt
  arp arpa
  ip address %(ssx_clnt_ip/mask)s
  exit
 interface rad1
  arp arpa
  ip address %(ssx_rad1_ip_mask)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
aaa profile
user authentication local
max-session 5
session authentication radius
exit
radius session authentication profile
server %(radius1_ip)s port 1812 key topsecret
exit
ipsec policy ikev2 phase1 name ph1-test1
custom
encryption aes128
hash sha-1
d-h group5
prf sha-1
gw-authentication psk 12345
peer-authentication eap
hard-lifetime 40 hours
exit
exit
ipsec policy ikev2 phase2 name ph2-test1
custom
encryption triple-des
hash md5
pfs group2
hard-lifetime 40 hours
soft-lifetime 600 secs
exit
exit
exit
port ethernet %(port_ssx_linux1)s
bind interface clnt %(context_name)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit
port ethernet %(port_ssx_radius1)s
 enable
 bind interface rad1 %(context_name)s
 exit
 exit
""" % docomo_var

#######################################################################

docomo_var['DoCoMo_6_2_1'] = docomo_var['DoCoMo_6_1_2']

#######################################################################

docomo_var['DoCoMo_6_2_5'] = """context %(context_name)s
ip pool %(ip_pool)s 20
 interface clnt
  arp arpa
  ip address %(ssx_clnt_ip/mask)s
  exit
 interface rad1
  arp arpa
  ip address %(ssx_rad1_ip_mask)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
aaa profile
user authentication local
max-session 5
session authentication radius
exit
radius session authentication profile
server %(radius1_ip)s port 1812 key topsecret
exit
ipsec policy ikev2 phase1 name ph1-test1
custom
encryption aes128
hash sha-1
d-h group5
prf sha-1
gw-authentication psk 12345
peer-authentication eap
hard-lifetime 360 secs
soft-lifetime 60 secs
exit
exit
ipsec policy ikev2 phase2 name ph2-test1
custom
encryption triple-des
hash md5
pfs group2
hard-lifetime 360 secs
soft-lifetime 60 secs
exit
exit
exit
port ethernet %(port_ssx_linux1)s
bind interface clnt %(context_name)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit
port ethernet %(port_ssx_radius1)s
 enable
 bind interface rad1 %(context_name)s
 exit
 exit
""" % docomo_var

#######################################################################

docomo_var['DoCoMo_6_2_6'] = docomo_var['DoCoMo_6_2_1']

#######################################################################

docomo_var['xpm_autoexec'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_clnt_ip)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context_name)s
test multiclient set max-concurrent    10
test multiclient set incr-ph1-life     1

test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          3des
test multiclient set ph2 hash          md5
test  multiclient set ph2 dh           2
test multiclient set ph2 life          12000
test multiclient set ph2-wild
test multiclient set delay 1000
test multiclient configure

ike start

test multiclient connect
""" % docomo_var

#######################################################################

docomo_var['incorrect_psk'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_clnt_ip)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           123456789
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context_name)s
test multiclient set max-concurrent    10
test multiclient set incr-ph1-life     1

test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          3des
test multiclient set ph2 hash          md5
test  multiclient set ph2 dh           2
test multiclient set ph2 life          12000
test multiclient set ph2-wild
test multiclient set delay 1000
test multiclient configure

ike start

test multiclient connect
""" % docomo_var

#######################################################################

# Config variables for Routing control
route_var = {}

#SSX Variables
route_var['context_name1'] = "ospf"
route_var['ospf_vlan1'] = "100"
# IP addresses used in the test
route_var['ospf_intf1_ip'] = "56.1.2.1"
route_var['ospf_intf1_ip/mask'] = "56.1.2.1/24"
route_var['cisco_ospf_intf1_ip'] = "56.1.2.2"
route_var['cisco_ospf_intf1_ip/mask'] = "56.1.2.2 255.255.255.0"
route_var['loopback_ip1'] =  "34.2.2.2"
route_var['loopback_ip1/mask'] =  "34.2.2.2/32"

#Mention your routes here
route_var['static_route1'] = "44.4.4.0 255.255.255.0"
route_var['static_route2'] = "44.4.5.0 255.255.255.0"
route_var['static_route3'] = "44.4.6.0 255.255.255.0"
route_var['static_route4'] = "44.4.7.0 255.255.255.0"
route_var['static_route5'] = "44.4.8.0 255.255.255.0"
route_var['static_route6'] = "44.4.9.0 255.255.255.0"
route_var['static_route7'] = "44.4.10.0 255.255.255.0"
route_var['static_route8'] = "44.4.11.0 255.255.255.0"
route_var['static_route9'] = "44.4.12.0 255.255.255.0"
route_var['static_route10'] = "44.4.13.0 255.255.255.0"
route_var['ospf_route1'] = "56.1.2.0 0.0.0.255"

#Port information
route_var['port_ssx1_cisco'] = topo.p_ssx1_cisco[0]
route_var['port_cisco_ssx1'] = topo.p_ssx1_cisco[1]

#####################################################################

route_var['DoCoMo_4_2_2'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 interface lo0 loopback
  ip address %(loopback_ip1/mask)s
  exit
 router-id 56.1.2.1
 router ospf
  redistribute static
  redistribute connected
  area 0
   interface vr1
    mtu-ignore
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s dot1q
 vlan %(ospf_vlan1)s
  bind interface vr1 %(context_name1)s
   exit
  exit
 enable
 exit
"""%route_var

#####################################################################

route_var['DoCoMo_4_3_1'] = route_var['DoCoMo_4_2_2']

#####################################################################

security_var = {}
security_var['username'] = "jameer"
security_var['passwd'] = "jameer"

security_var['DoCoMo_5_2_1'] = """
context local
aaa profile
 user authentication none
 service authorization none
 exit
user name %s
 password %s
 priv-level administrator
 exit 
interface mgt4 management
 arp arpa
 ip address %s/24
 exit
ip route 0.0.0.0/0 %s
exit
port ethernet 0/0
 bind interface mgt4 local
  exit
 enable
 exit
port ethernet 1/0
 bind interface mgt4 local
  exit
 enable
 exit
"""

#####################################################################

others_var = {}
others_var['context_name'] = "DoCoMo"
others_var['rx_ip/mask'] = "1.1.1.1/24"
others_var['rx_ip'] = "1.1.1.1"
others_var['ixia_rx_ip/mask'] = "1.1.1.2/24"
others_var['ixia_rx_ip'] = "1.1.1.1"
others_var['cntxt1']= "local" 
others_var['infc_r1_ip/m']="17.1.1.10/24"
others_var['infc_linux1_ip/m']="17.1.1.1/24"
others_var['infc_linux1_ip']="17.1.1.1"
others_var['key']= '3'

# Port information
others_var['port_ssx_ixia'] = topo.p1_ssx2_ixia[0]
others_var['port_ixia_ssx'] = topo.p1_ssx2_ixia[1]
others_var['port_ssx_linux']= topo.port_ssx_radius1[0]
others_var['port_linux_ssx']= topo.port_ssx_radius1[1]

#####################################################################

others_var['DoCoMo_8_1_1'] = """
context %(context_name)s
 interface rx
  arp arpa
  ip address %(rx_ip/mask)s
  exit
 exit
port ethernet %(port_ssx_ixia)s
 bind interface rx %(context_name)s
  exit
 enable
 exit
"""%others_var

#####################################################################

others_var['DoCoMo_PERF_NONGLCR_006'] = others_var['DoCoMo_8_1_1']

#####################################################################

others_var['DoCoMo_8_3_6']="""
context %(cntxt1)s
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit
ntp profile
server %(infc_linux1_ip)s
exit
exit
port ethernet %(port_ssx_linux)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %others_var

#####################################################################
# Basic Maintainance operations
basic_var = {}

basic_var['context_name'] = "DoCoMo"
basic_var['ssx_phy_iface_ip_mask'] = '17.1.1.2/24'
basic_var['ssx_phy_iface_ip'] = '17.1.1.2'
basic_var['snmp_server_ip_mask'] = '17.1.1.1/24'
basic_var['snmp_server_ip'] = '17.1.1.1'

# Port information
basic_var['port_ssx_snmp'] = topo.port_ssx_linux1[0]
basic_var['port_snmp_ssx'] = topo.port_ssx_linux1[1]

#####################################################################

basic_var['DoCoMo_7_5_1'] = """
context local
 interface docomo
  arp arpa
  ip address %(ssx_phy_iface_ip_mask)s
  exit
 exit
snmp
 server
  exit
 view all
  oid internet include
  oid dod include
  oid private include
  oid stoke include
  oid enterprises include
  oid org include
  oid iso include
  exit
 group v2c-group
  context local sec-model v2c notify-view all read-view all
  exit
 community
  name snmp_com1 group v2c-group context local
  name snmp_com2 group v1-group context local
  exit
 group v1-group
  context local sec-model v1 notify-view all read-view all
  exit
 notification
  notify
   name notify-inform tag-inform inform
   name notify-trap tag-trap trap
   name rmon-alarm rmon-alarm trap
   name rmon-event rmon-event trap
   exit
  target-parameters
   name v2c-param sec-name snmp_com1 sec-model v2c
   name v1-param sec-name snmp_com2 sec-model v1
   name v3-param1 sec-name v3-user1 sec-model usm noauth-nopriv
   name v3-param2 sec-name v3-user2 sec-model usm auth-priv
   exit
  notify-target
   name ituni1 %(snmp_server_ip)s tags tag-trap,info-trap,rmon-alram,rmon-events parameters v1-param timeout 10 retry 20
   name ituni2 %(snmp_server_ip)s tags tag-trap,info-trap,rmon-alram,rmon-events parameters v2c-param timeout 10 retry 20
   name ituni3 %(snmp_server_ip)s tags tag-trap,info-trap,rmon-alram,rmon-events parameters v3-param1 timeout 10 retry 20
   exit
  exit
 user v3-user1
  sec-model usm auth-proto noauth group v3-group-noauth
  exit
 group v3-group-noauth
  context local sec-model usm noauth-nopriv notify-view all read-view all
  exit
 user v3-user2
  sec-model usm auth-proto md5 auth-passw apass123 priv-proto des priv-passw vpass123 group v3-group-auth-priv
  exit
 group v3-group-auth-priv
  context local sec-model usm auth-priv notify-view all read-view all
  context local sec-model usm noauth-nopriv notify-view all read-view all
  exit
 exit
port ethernet %(port_ssx_snmp)s
 bind interface docomo local
  exit
 enable
 exit """ %basic_var

#####################################################################

ipsec_var = {}
ipsec_var['context_name'] = "india-test"
ipsec_var['context_name1'] = "india-test"
ipsec_var['dpd_interval'] = "30"
ipsec_var['retry_interval'] = "30"
ipsec_var['maximum_retries'] = "2"
ipsec_var['session_remove_timer'] = "300"
ipsec_var['psk_key'] =  "12345"
ipsec_var['ssx_ses_ip'] =  "11.11.11.1"
ipsec_var['ssx_ses_ip/mask'] =  "11.11.11.1/24"
ipsec_var['ssx_ses_ip1'] =  "12.12.12.1"
ipsec_var['ssx_ses_ip1/mask'] =  "12.12.12.1/24"
ipsec_var['rad_server_ip'] =  "12.2.2.2"
ipsec_var['rad_server_ip/mask'] =  "12.2.2.2/24"
ipsec_var['cisco_rad_server_ip'] =  "12.2.2.1"
ipsec_var['cisco_rad_server_ip/mask'] =  "12.2.2.1 255.255.255.0"
ipsec_var['server_port'] = '1812'
ipsec_var['server_key'] =  'topsecret'
ipsec_var['starting_ip_pool'] = '6.6.2.1'
ipsec_var['no_of_ip_pool'] =  '1024'
ipsec_var['active_slot3_ip'] = '26.1.1.1'
ipsec_var['active_slot3_ip/mask'] = '26.1.1.1/24'
ipsec_var['standby_4slot3_ip'] = '16.1.1.1'
ipsec_var['standby_4slot3_ip/mask'] = '16.1.1.1/24'
ipsec_var['cisco_active_slot3_ip'] = '26.1.1.2'
ipsec_var['cisco_active_slot3_ip_mask'] = '26.1.1.2 255.255.255.0'
ipsec_var['cisco_standby_4slot3_ip'] = '16.1.1.2'
ipsec_var['cisco_standby_4slot3_ip_mask'] = '16.1.1.2 255.255.255.0'
ipsec_var['rad_intf_4slot3_ip'] =  "13.2.2.1"
ipsec_var['rad_intf_4slot3_ip/mask'] =  "13.2.2.1/24"
ipsec_var['bkp_rad_intf_4slot3_ip'] =  "14.2.2.1"
ipsec_var['bkp_rad_intf_4slot3_ip/mask'] =  "14.2.2.1/24"
ipsec_var['cisco_rad_intf_4slot3_ip'] =  "13.2.2.2"
ipsec_var['cisco_rad_intf_4slot3_ip/mask'] =  "13.2.2.2 255.255.255.0"
ipsec_var['cisco_bkp_rad_intf_4slot3_ip'] =  "14.2.2.2"
ipsec_var['cisco_bkp_rad_intf_4slot3_ip/mask'] =  "14.2.2.2 255.255.255.0"
ipsec_var['lpbk_ip'] =  "36.1.1.1"
ipsec_var['lpbk_ip/mask'] =  "36.1.1.1/32"
ipsec_var['lpbk_ip1'] =  "46.1.1.1"
ipsec_var['lpbk_ip1/mask'] =  "46.1.1.1/32"
ipsec_var['active_slot2_ip'] = '26.2.2.1'
ipsec_var['active_slot2_ip/mask'] = '26.2.2.1/24'
ipsec_var['standby_4slot2_ip'] = '16.2.2.1'
ipsec_var['standby_4slot2_ip/mask'] = '16.2.2.1/24'
ipsec_var['cisco_active_slot2_ip'] = '26.2.2.2'
ipsec_var['cisco_active_slot2_ip_mask'] = '26.2.2.2 255.255.255.0'
ipsec_var['cisco_standby_4slot2_ip'] = '16.2.2.2'
ipsec_var['cisco_standby_4slot2_ip_mask'] = '16.2.2.2 255.255.255.0'
ipsec_var['rad_intf_4slot2_ip'] =  "13.3.3.1"
ipsec_var['rad_intf_4slot2_ip/mask'] =  "13.3.3.1/24"
ipsec_var['bkp_rad_intf_4slot2_ip'] =  "14.3.3.1"
ipsec_var['bkp_rad_intf_4slot2_ip/mask'] =  "14.3.3.1/24"
ipsec_var['cisco_rad_intf_4slot2_ip'] =  "13.3.3.2"
ipsec_var['cisco_rad_intf_4slot2_ip/mask'] =  "13.3.3.2 255.255.255.0"
ipsec_var['cisco_bkp_rad_intf_4slot2_ip'] =  "14.3.3.2"
ipsec_var['cisco_bkp_rad_intf_4slot2_ip/mask'] =  "14.3.3.2 255.255.255.0"

#Mention your routes here.
ipsec_var['route_to_cisco_active_rad'] =  "13.2.2.0/24"
ipsec_var['route_to_cisco_standby_rad'] =  "14.2.2.0/24"
ipsec_var['route_to_cisco_active_rad_slot2'] =  "13.3.3.0/24"
ipsec_var['route_to_cisco_standby_rad_slot2'] =  "14.3.3.0/24"
ipsec_var['route_to_host_ns'] = "192.168.1.0/24"
ipsec_var['route_to_ns_phy_ip'] =  '20.1.1.0/24'
ipsec_var['route_ip_pool'] = '6.6.0.0/16'
ipsec_var['route_to_rad_srvr'] =  "12.2.2.0/24"
ipsec_var['default_route'] = '0.0.0.0/0'
ipsec_var['active_route_4slot3'] = '26.1.1.0/24'
ipsec_var['standby_route_4slot3'] = '16.1.1.0/24'
ipsec_var['active_route_4slot2'] = '26.2.2.0/24'
ipsec_var['standby_route_4slot2'] = '16.2.2.0/24'
ipsec_var['cisco_ses_ip_route'] = "11.11.11.1 255.255.255.255"
ipsec_var['cisco_lpbk_ip_route'] = "36.1.1.1 255.255.255.255"
ipsec_var['cisco_ses_ip1_route'] = "12.12.12.1 255.255.255.255"
ipsec_var['cisco_lpbk_ip1_route'] = "46.1.1.1 255.255.255.255"
ipsec_var['cisco_route_to_pool'] = "6.6.2.1 255.255.255.255"

#Port information from topo. 
ipsec_var['port_ssx_rad_intf_4slot3'] = topo_glcr.p_to_rad_active_ssx_cisco_slot3[0]
ipsec_var['port_cisco_rad_intf_4slot3'] = topo_glcr.p_to_rad_active_ssx_cisco_slot3[1]
ipsec_var['port_ssx_bkp_rad_intf_4slot3'] =  topo_glcr.p_to_rad_standby_ssx_cisco_slot3[0]
ipsec_var['port_cisco_bkp_rad_intf_4slot3'] =  topo_glcr.p_to_rad_standby_ssx_cisco_slot3[1]
ipsec_var['port_ssx_active_4slot3'] = topo_glcr.p_active_ssx_cisco_slot3[0]
ipsec_var['port_cisco_active_4slot3'] = topo_glcr.p_active_ssx_cisco_slot3[1]
ipsec_var['port_ssx_standby_4slot3'] = topo_glcr.p_standby_ssx_cisco_slot3[0]
ipsec_var['port_cisco_standby_4slot3'] = topo_glcr.p_standby_ssx_cisco_slot3[1]

ipsec_var['port_cisco_rad_srvr'] =  topo_glcr.p_cisco_rad[0]
ipsec_var['intf_rad_srvr'] = topo_glcr.p_cisco_rad[1]

ipsec_var['port_ssx_rad_intf_4slot2'] = topo_glcr.p_to_rad_active_ssx_cisco_slot2[0]
ipsec_var['port_cisco_rad_intf_4slot2'] = topo_glcr.p_to_rad_active_ssx_cisco_slot2[1]
ipsec_var['port_ssx_bkp_rad_intf_4slot2'] =  topo_glcr.p_to_rad_standby_ssx_cisco_slot2[0]
ipsec_var['port_cisco_bkp_rad_intf_4slot2'] =  topo_glcr.p_to_rad_standby_ssx_cisco_slot2[1]
ipsec_var['port_ssx_active_4slot2'] = topo_glcr.p_active_ssx_cisco_slot2[0]
ipsec_var['port_cisco_active_4slot2'] = topo_glcr.p_active_ssx_cisco_slot2[1]
ipsec_var['port_ssx_standby_4slot2'] = topo_glcr.p_standby_ssx_cisco_slot2[0]
ipsec_var['port_cisco_standby_4slot2'] = topo_glcr.p_standby_ssx_cisco_slot2[1]

###############################################################################
#2nd context configuration
ipsec_var['context_card2'] =  "stoke"
ipsec_var['card2_context1'] = "stoke1"
ipsec_var['card2_rad_server1'] =  "192.168.150.1"
ipsec_var['card2_rad_server2'] = "192.168.150.10"
ipsec_var['card2_rad_server1/mask'] =  "192.168.150.1/24"
ipsec_var['card2_rad_server2/mask'] = "192.168.150.10/24"
ipsec_var['cisco_card2_rad_server_ip'] =  "192.168.150.150"
ipsec_var['cisco_card2_rad_server_ip/mask'] =  "192.168.150.150 255.255.255.0"
ipsec_var['card2_ses_ip'] = "66.66.66.1"
ipsec_var['card2_ses_ip/mask'] = "66.66.66.1/16"
ipsec_var['card2_ses_ip1'] = "6.6.6.1"
ipsec_var['card2_ses_ip1/mask'] = "6.6.6.1/16"
ipsec_var['ssx_card2_active'] = "192.168.144.2"
ipsec_var['ssx_card2_active/mask'] = "192.168.144.2/24"
ipsec_var['cisco_card2_active_ip'] = "192.168.144.1"
ipsec_var['cisco_card2_active_ip/mask'] = "192.168.144.1 255.255.255.0"
ipsec_var['to_rad_ip'] = "192.168.110.2"
ipsec_var['to_rad_ip/mask'] = "192.168.110.2/24"
ipsec_var['cisco_to_rad_ip'] = "192.168.110.1"
ipsec_var['cisco_to_rad_ip/mask'] = "192.168.110.1 255.255.255.0"
ipsec_var['card2_lpbk_ip'] =  "19.1.0.1"
ipsec_var['card2_lpbk_ip/mask'] =  "19.1.0.1/32"
ipsec_var['card2_lpbk_ip1'] =  "18.1.0.1"
ipsec_var['card2_lpbk_ip1/mask'] =  "18.1.0.1/32"
ipsec_var['ssx_card2_standby_ip'] = "192.168.244.2"
ipsec_var['ssx_card2_standby_ip/mask'] = "192.168.244.2/24"
ipsec_var['cisco_card2_standby_ip'] = "192.168.244.1"
ipsec_var['cisco_card2_standby_ip/mask'] = "192.168.244.1 255.255.255.0"
ipsec_var['service_bkp_ip'] = "192.168.210.2"
ipsec_var['service_bkp_ip/mask'] = "192.168.210.2/24"
ipsec_var['cisco_service_bkp_ip'] = "192.168.210.1"
ipsec_var['cisco_service_bkp_ip/mask'] = "192.168.210.1 255.255.255.0"
ipsec_var['cisco_card2_ip'] = "12.12.12.1"
ipsec_var['cisco_card2_ip/mask'] = "12.12.12.1 255.255.255.0"
ipsec_var['cisco_card2_ip1'] = "12.12.112.1"
ipsec_var['cisco_card2_ip1/mask'] = "12.12.112.1 255.255.255.0"
ipsec_var['card2_lpbk_ip1_mask'] =  "18.1.0.1 255.255.255.255"
ipsec_var['card2_ip'] = "12.12.12.12"
ipsec_var['card2_ip1'] = "12.12.112.12"
ipsec_var['card2_ph1_hard'] =  "28800"
ipsec_var['card2_ph1_soft'] = "3000"
ipsec_var['card2_ph2_hard'] = "28800"
ipsec_var['card2_ph2_soft'] = "3000"
ipsec_var['lpbk_3rCard_ip/mask'] = "15.3.2.2/32"

#LS Routes
ipsec_var['card2_cisco_route'] =  "12.12.12.0/24"
ipsec_var['card2_cisco_route1'] =  "12.12.112.0/24"
ipsec_var['card2_route_to_rad'] = "192.168.150.0/24"
ipsec_var['card2_clnt_ip_route'] =  "9.0.0.0/8"
ipsec_var['card2_clnt_ip_route1'] =  "9.2.0.0/16"
ipsec_var['card2_route_active_rad'] = "192.168.110.0/24"
ipsec_var['card2_route_backup_rad'] = "192.168.210.0/24"
ipsec_var['card2_route_active_ssx'] = "192.168.144.0/24"
ipsec_var['card2_route_backup_ssx'] = "192.168.244.0/24"
ipsec_var['card2_route_standby_ssx'] = "192.168.244.0/24"
ipsec_var['card2_ses_route'] = "10.210.0.0/16"
ipsec_var['cisco_card2_ses_route'] = "10.210.0.0 255.255.0.0"
ipsec_var['cisco_card2_ses_route1'] = "10.222.0.0 255.255.0.0"
ipsec_var['cisco_rt_card2_lpbk_ip'] = "19.1.0.1 255.255.255.255"
ipsec_var['route_to_card2_ses'] = "9.1.0.0 255.255.0.0"
ipsec_var['route_to_card2_ses1'] = "9.2.0.0 255.255.0.0"

###############################################################################
#SST Configuration
ipsec_var['sst_cisco_slot2_ip'] = "15.2.2.1"
ipsec_var['sst_cisco_slot2_ip/mask'] = "15.2.2.1/28"
ipsec_var['sst_cisco_slot3_ip'] = "15.3.2.1"
ipsec_var['sst_cisco_slot3_ip/mask'] = "15.3.2.1/28"
ipsec_var['cisco_sst_slot2_ip'] = "15.2.2.5"
ipsec_var['cisco_sst_slot2_ip/mask'] = "15.2.2.5 255.255.255.240"
ipsec_var['cisco_sst_slot3_ip'] = "15.3.2.5"
ipsec_var['cisco_sst_slot3_ip/mask'] = "15.3.2.5 255.255.255.240"
ipsec_var['sst_ixia_ip'] = "81.0.0.2"
ipsec_var['sst_ixia_ip/mask'] = "81.0.0.2/16"
ipsec_var['ixia_sst_ip'] = "81.0.0.1"
ipsec_var['ixia_sst_ip/mask'] = "81.0.0.1/16"
ipsec_var['sst_slot3_ixia_ip'] = "82.0.0.2"
ipsec_var['sst_slot3_ixia_ip/mask'] = "82.0.0.2/16"
ipsec_var['ixia_sst_slot3_ip'] = "82.0.0.1"
ipsec_var['ixia_sst_slot3_ip/mask'] = "82.0.0.1/16"
ipsec_var['ikev2_lpbk_ip'] = "15.2.2.2"
ipsec_var['ikev2_lpbk_ip/mask'] = "15.2.2.2/32"
ipsec_var['ikev2_lpbk_ip_mask'] = "15.2.2.2 255.255.255.255"
ipsec_var['lpbk_3rCard_ip_mask'] = "15.3.2.2 255.255.255.255"
ipsec_var[''] = ""

ipsec_var['route_sst_ixia'] = "10.110.0.0/16"
ipsec_var['route_sst_slot3_ixia'] = "10.222.0.0/16"
ipsec_var['cisco_route_sst_ixia'] = "10.110.0.0 255.255.0.0"
ipsec_var['route_to_sst_ses'] = "2.2.0.0/16"
ipsec_var['cisco_route_to_sst_ses'] = "2.2.0.0 255.255.0.0"
ipsec_var['route_sst_slot3'] = "3.2.0.0/16"
ipsec_var['cisco_route_sst_slot3'] = "3.2.0.0 255.255.0.0"
ipsec_var['route_to_sst_ip'] = "15.2.2.1/32"
ipsec_var['route_to_sst_slot3_ip'] = "15.3.2.1/32"
ipsec_var['route_to_cisco_sst_ip'] = "15.2.2.5/32"
ipsec_var['ssx_ses_traffic_route'] = "30.110.0.0/16"
ipsec_var['cisco_ssx_ses_traffic_route'] = "30.110.0.0 255.255.0.0"
ipsec_var['cisco_ssx_slot3_ses_traffic_route'] = "30.222.0.0 255.255.0.0"
ipsec_var['cisco_slot2_ip/mask'] = "10.10.60.61 255.255.255.0"
ipsec_var['cisco_slot2_ip'] = "10.10.60.61"
ipsec_var['cisco_slot3_ip/mask'] = "10.10.50.51 255.255.255.0"
ipsec_var['cisco_slot3_ip'] = "10.10.50.51"
ipsec_var['ixia_cisco_slot2_ip/mask'] = "10.10.60.60 255.255.255.0"
ipsec_var['ixia_cisco_slot2_ip'] = "10.10.60.60"
ipsec_var['ixia_cisco_slot3_ip/mask'] = "10.10.50.50 255.255.255.0"
ipsec_var['ixia_cisco_slot3_ip'] = "10.10.50.50"
ipsec_var[''] = ""
ipsec_var[''] = ""
ipsec_var[''] = ""
ipsec_var[''] = ""
ipsec_var[''] = ""


ipsec_var['port_sst_slot2'] = topo_glcr.p_sst_cisco_slot2[0]
ipsec_var['port_cisco_sst_slot2'] = topo_glcr.p_sst_cisco_slot2[1]
ipsec_var['port_sst_slot3'] = topo_glcr.p_sst_cisco_slot3[0]
ipsec_var['port_cisco_sst_slot3'] = topo_glcr.p_sst_cisco_slot3[1]
ipsec_var['port_sst_ixia'] = topo_glcr.p_sst_ixia[0]
ipsec_var['port_ixia_sst'] = topo_glcr.p_sst_ixia[1]
ipsec_var['port_sst_slot3_ixia'] = topo_glcr.p_sst_slot3_ixia[0]
ipsec_var['port_ixia_sst_slot3'] = topo_glcr.p_sst_slot3_ixia[1]
ipsec_var['port1_cisco_ixia'] = topo_glcr.p1_cisco_ixia[0]
ipsec_var['port1_ixia_cisco'] = topo_glcr.p1_cisco_ixia[1]
ipsec_var['port2_cisco_ixia'] = topo_glcr.p2_cisco_ixia[0]
ipsec_var['port2_ixia_cisco'] = topo_glcr.p2_cisco_ixia[1]

###############################################################################

ipsec_var['GLCR_SES_IKEv2_FUN_001'] = """
aaa global profile
 custom-profile 1
 exit
no ipsec global profile
ipsec global profile
 dpd interval 60 retry-interval 60 maximum-retries 5
 retransmit interval 15 maximum-retries 5 send-retransmit-response
 session-remove-timer interval 300
 relax-ts-check
 exit
context %(context_name)s
 aaa profile
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(card2_rad_server1)s port 1812 key %(server_key)s
  exit
 ip pool 10.110.0.0 1024
 interface subs session
  ip session-default
  ip address %(card2_ses_ip1/mask)s
  exit
 interface active_slot3
  arp arpa
  ip address %(active_slot3_ip/mask)s
  exit
  interface bkp_4slot3
  arp arpa
  ip address %(standby_4slot3_ip/mask)s
  exit
 interface rad_intf_4slot3
  arp arpa
  ip address %(rad_intf_4slot3_ip/mask)s
  exit
 interface bkp_rad_intf_4slot3
  arp arpa
  ip address %(bkp_rad_intf_4slot3_ip/mask)s
  exit
 interface ikev2OnCard3_lpbk loopback
  ip address %(lpbk_3rCard_ip/mask)s
  exit
 rtr 300
  type echo protocol ipicmpecho %(cisco_active_slot3_ip)s source %(active_slot3_ip)s
  exit
 rtr 301
  type echo protocol ipicmpecho %(cisco_standby_4slot3_ip)s source %(standby_4slot3_ip)s
  exit
 rtr 400
  type echo protocol ipicmpecho %(cisco_rad_intf_4slot3_ip)s source %(rad_intf_4slot3_ip)s
  exit
 rtr 401
  type echo protocol ipicmpecho %(cisco_bkp_rad_intf_4slot3_ip)s source %(bkp_rad_intf_4slot3_ip)s
  exit
 rtr schedule 300
 rtr schedule 301
 rtr schedule 401
 rtr schedule 400
 ip route %(card2_route_to_rad)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(card2_clnt_ip_route1)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(card2_clnt_ip_route1)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(card2_route_to_rad)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ip route %(route_sst_slot3)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_sst_slot3)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(route_to_sst_slot3_ip)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_to_sst_slot3_ip)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(ssx_ses_traffic_route)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(ssx_ses_traffic_route)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ipsec policy ikev2 phase1 name ikev2OnCard3
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10800 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 7200 secs
   exit
  exit
 exit
session-home slot 101 loopback interface ikev2OnCard3_lpbk %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase2 name ikev2_p2
 ipsec policy ikev2 phase1 name ikev2OnCard3
 exit
port ethernet %(port_ssx_active_4slot3)s
 bind interface active_slot3 %(context_name)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot3)s
 bind interface rad_intf_4slot3 %(context_name)s
  exit
 enable
 exit
 port ethernet %(port_ssx_bkp_rad_intf_4slot3)s
 bind interface bkp_rad_intf_4slot3 %(context_name1)s
  exit
 enable
 exit
port ethernet %(port_ssx_standby_4slot3)s
 bind interface bkp_4slot3 %(context_name1)s
  exit
 service ipsec
 enable
 exit

context %(context_card2)s
 aaa profile
  session authentication radius
  exit
 radius session authentication profile
  server %(card2_rad_server1)s port 1812 key %(server_key)s
  exit
 ip pool 10.222.0.0 1024
 interface ipsec_lp_21 loopback
  ip address %(ikev2_lpbk_ip/mask)s
  exit
 interface subs session
  ip session-default
  ip address %(card2_ses_ip/mask)s
  exit
 interface client_cisco11_vlan931
  arp arpa
  ip address %(ssx_card2_active/mask)s
  exit
 interface client_cisco14_vlan961_bk
  arp arpa
  ip address %(ssx_card2_standby_ip/mask)s
  exit
 interface service_cisco13_vlan951_bk
  arp arpa
  ip address %(service_bkp_ip/mask)s
  exit
 interface service_cisco17_vlan936
  arp arpa
  ip address %(to_rad_ip/mask)s
  exit
 rtr 100
  type echo protocol ipicmpecho %(cisco_card2_active_ip)s source %(ssx_card2_active)s
  exit
 rtr 101
  type echo protocol ipicmpecho %(cisco_card2_standby_ip)s source %(ssx_card2_standby_ip)s
  exit
 rtr 200
  type echo protocol ipicmpecho %(cisco_to_rad_ip)s source %(to_rad_ip)s
  exit
 rtr 201
  type echo protocol ipicmpecho %(cisco_service_bkp_ip)s source %(service_bkp_ip)s
  exit
 rtr schedule 100
 rtr schedule 101
 rtr schedule 201
 rtr schedule 200
 ip route %(route_to_sst_ses)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ses)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(card2_route_to_rad)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ip route %(card2_route_to_rad)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ipsec policy ikev2 phase1 name ikev2_p1
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10800 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 7200 secs
   exit
  exit
 exit
session-home slot 100 loopback interface ipsec_lp_21 %(context_card2)s
 ipsec session context name %(context_card2)s
 ipsec policy ikev2 phase1 name ikev2_p1
 ipsec policy ikev2 phase2 name ikev2_p2
 exit
port ethernet %(port_ssx_active_4slot2)s
 bind interface client_cisco11_vlan931 %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_standby_4slot2)s
 bind interface client_cisco14_vlan961_bk %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot2)s
 bind interface service_cisco17_vlan936 %(context_card2)s
  exit
 enable
 exit
port ethernet %(port_ssx_bkp_rad_intf_4slot2)s
 bind interface service_cisco13_vlan951_bk %(context_card2)s
  exit
 enable
 exit
"""%(ipsec_var)

################################################################################

ipsec_var['SST_GLCR_SES_IKEv2_FUN_001'] = """
no ipsec global profile
ipsec global profile
 dpd interval 60 retry-interval 60 maximum-retries 5
 exit
context local
interface to_cisco_slot2
arp arpa
ip address %(sst_cisco_slot2_ip/mask)s
exit
interface to_cisco_slot3
arp arpa
ip address %(sst_cisco_slot3_ip/mask)s
exit
interface to_ixia
arp arpa
ip address %(sst_ixia_ip/mask)s
exit
ip route %(card2_route_active_ssx)s %(cisco_sst_slot2_ip)s
ip route %(card2_route_standby_ssx)s %(cisco_sst_slot2_ip)s
ip route %(route_sst_ixia)s %(ixia_sst_ip)s
 ipsec policy ikev2 phase1 name p1_AES
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10400 secs
   exit
  exit
 ipsec policy ikev2 phase2 name p2_AES
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 6900 secs
   exit
  exit
 exit
port ethernet %(port_sst_slot2)s
 bind interface to_cisco_slot2 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
port ethernet %(port_sst_ixia)s
 bind interface to_ixia local
  ip host 81.0.0.1 00:11:22:33:44:21
  exit
 enable
 exit
port ethernet %(port_sst_slot3)s
 bind interface to_cisco_slot3 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
"""%ipsec_var

###############################################################################

ipsec_var['GLCR_SES_IKEv2_FUN_007'] = ipsec_var['GLCR_SES_IKEv2_FUN_001']
ipsec_var['SST_GLCR_SES_IKEv2_FUN_007'] = ipsec_var['SST_GLCR_SES_IKEv2_FUN_001']

###############################################################################

###############################################################################

ipsec_var['GLCR_SES_IKEv2_FUN_035'] = ipsec_var['GLCR_SES_IKEv2_FUN_007']
ipsec_var['SST_GLCR_SES_IKEv2_FUN_035'] = ipsec_var['SST_GLCR_SES_IKEv2_FUN_007']

###############################################################################

ipsec_var['GLCR_SES_IKEv2_FUN_036'] = """
aaa global profile
 custom-profile 1
 exit
no ipsec global profile
ipsec global profile
 dpd interval 60 retry-interval 60 maximum-retries 5
 retransmit interval 15 maximum-retries 5 send-retransmit-response
 session-remove-timer interval 300
 relax-ts-check
 exit
context %(context_name)s
 aaa profile
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(card2_rad_server1)s port 1812 key %(server_key)s
  exit
 ip pool 10.110.0.0 1024
 interface subs session
  ip session-default
  ip address %(card2_ses_ip1/mask)s
  exit
 interface active_slot3
  arp arpa
  ip address %(active_slot3_ip/mask)s
  exit
  interface bkp_4slot3
  arp arpa
  ip address %(standby_4slot3_ip/mask)s
  exit
 interface rad_intf_4slot3
  arp arpa
  ip address %(rad_intf_4slot3_ip/mask)s
  exit
 interface bkp_rad_intf_4slot3
  arp arpa
  ip address %(bkp_rad_intf_4slot3_ip/mask)s
  exit
 interface ikev2OnCard3_lpbk loopback
  ip address %(lpbk_3rCard_ip/mask)s
  exit
 rtr 300
  type echo protocol ipicmpecho %(cisco_active_slot3_ip)s source %(active_slot3_ip)s
  exit
 rtr 301
  type echo protocol ipicmpecho %(cisco_standby_4slot3_ip)s source %(standby_4slot3_ip)s
  exit
 rtr 400
  type echo protocol ipicmpecho %(cisco_rad_intf_4slot3_ip)s source %(rad_intf_4slot3_ip)s
  exit
 rtr 401
  type echo protocol ipicmpecho %(cisco_bkp_rad_intf_4slot3_ip)s source %(bkp_rad_intf_4slot3_ip)s
  exit
 rtr schedule 300
 rtr schedule 301
 rtr schedule 401
 rtr schedule 400
 ip route %(card2_route_to_rad)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(card2_clnt_ip_route1)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(card2_clnt_ip_route1)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(card2_route_to_rad)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ip route %(route_sst_slot3)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_sst_slot3)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(route_to_sst_slot3_ip)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_to_sst_slot3_ip)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(ssx_ses_traffic_route)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(ssx_ses_traffic_route)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ipsec policy ikev2 phase1 name ikev2OnCard3
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 exit
session-home slot 101 loopback interface ikev2OnCard3_lpbk %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase2 name ikev2_p2
 ipsec policy ikev2 phase1 name ikev2OnCard3
 exit
port ethernet %(port_ssx_active_4slot3)s
 bind interface active_slot3 %(context_name)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot3)s
 bind interface rad_intf_4slot3 %(context_name)s
  exit
 enable
 exit
 port ethernet %(port_ssx_bkp_rad_intf_4slot3)s
 bind interface bkp_rad_intf_4slot3 %(context_name1)s
  exit
 enable
 exit
port ethernet %(port_ssx_standby_4slot3)s
 bind interface bkp_4slot3 %(context_name1)s
  exit
 service ipsec
 enable
 exit

context %(context_card2)s
 aaa profile
  session authentication radius
  exit
 radius session authentication profile
  server %(card2_rad_server1)s port 1812 key %(server_key)s
  exit
 ip pool 10.222.0.0 1024
 interface ipsec_lp_21 loopback
  ip address %(ikev2_lpbk_ip/mask)s
  exit
 interface subs session
  ip session-default
  ip address %(card2_ses_ip/mask)s
  exit
 interface client_cisco11_vlan931
  arp arpa
  ip address %(ssx_card2_active/mask)s
  exit
 interface client_cisco14_vlan961_bk
  arp arpa
  ip address %(ssx_card2_standby_ip/mask)s
  exit
 interface service_cisco13_vlan951_bk
  arp arpa
  ip address %(service_bkp_ip/mask)s
  exit
 interface service_cisco17_vlan936
  arp arpa
  ip address %(to_rad_ip/mask)s
  exit
 rtr 100
  type echo protocol ipicmpecho %(cisco_card2_active_ip)s source %(ssx_card2_active)s
  exit
 rtr 101
  type echo protocol ipicmpecho %(cisco_card2_standby_ip)s source %(ssx_card2_standby_ip)s
  exit
 rtr 200
  type echo protocol ipicmpecho %(cisco_to_rad_ip)s source %(to_rad_ip)s
  exit
 rtr 201
  type echo protocol ipicmpecho %(cisco_service_bkp_ip)s source %(service_bkp_ip)s
  exit
 rtr schedule 100
 rtr schedule 101
 rtr schedule 201
 rtr schedule 200
 ip route %(route_to_sst_ses)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ses)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(card2_route_to_rad)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ip route %(card2_route_to_rad)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ipsec policy ikev2 phase1 name ikev2_p1
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 exit
session-home slot 100 loopback interface ipsec_lp_21 %(context_card2)s
 ipsec session context name %(context_card2)s
 ipsec policy ikev2 phase1 name ikev2_p1
 ipsec policy ikev2 phase2 name ikev2_p2
 exit
port ethernet %(port_ssx_active_4slot2)s
 bind interface client_cisco11_vlan931 %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_standby_4slot2)s
 bind interface client_cisco14_vlan961_bk %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot2)s
 bind interface service_cisco17_vlan936 %(context_card2)s
  exit
 enable
 exit
port ethernet %(port_ssx_bkp_rad_intf_4slot2)s
 bind interface service_cisco13_vlan951_bk %(context_card2)s
  exit
 enable
 exit
"""%(ipsec_var)

################################################################################

ipsec_var['SST_GLCR_SES_IKEv2_FUN_036'] = """
no ipsec global profile
ipsec global profile
 dpd interval 60 retry-interval 60 maximum-retries 5
 exit
context local
interface to_cisco_slot2
arp arpa
ip address %(sst_cisco_slot2_ip/mask)s
exit
interface to_cisco_slot3
arp arpa
ip address %(sst_cisco_slot3_ip/mask)s
exit
interface to_ixia
arp arpa
ip address %(sst_ixia_ip/mask)s
exit
ip route %(card2_route_active_ssx)s %(cisco_sst_slot2_ip)s
ip route %(card2_route_standby_ssx)s %(cisco_sst_slot2_ip)s
ip route %(route_sst_ixia)s %(ixia_sst_ip)s
 ipsec policy ikev2 phase1 name p1_AES
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 ipsec policy ikev2 phase2 name p2_AES
  suite1
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 exit
port ethernet %(port_sst_slot2)s
 bind interface to_cisco_slot2 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
port ethernet %(port_sst_ixia)s
 bind interface to_ixia local
  ip host 81.0.0.1 00:11:22:33:44:21
  exit
 enable
 exit
port ethernet %(port_sst_slot3)s
 bind interface to_cisco_slot3 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
"""%ipsec_var

###############################################################################

ipsec_var['GLCR_SES_IKEv2_FUN_037'] = ipsec_var['GLCR_SES_IKEv2_FUN_036']
ipsec_var['SST_GLCR_SES_IKEv2_FUN_037'] = ipsec_var['SST_GLCR_SES_IKEv2_FUN_036']

###############################################################################

ipsec_var['DoCoMo_PERF_GLCR_SESS_003'] = """
aaa global profile
 custom-profile 1
 exit
no ipsec global profile
ipsec global profile
 retransmit interval 15 maximum-retries 5 send-retransmit-response
 session-remove-timer interval 300
 relax-ts-check
 exit
context %(context_name)s
 aaa profile
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  algorithm round-robin
  server %(card2_rad_server1)s port 1812 key %(server_key)s
  #server %(card2_rad_server1)s port 1822 key %(server_key)s
  server %(card2_rad_server1)s port 1832 key %(server_key)s
  #server %(card2_rad_server1)s port 1842 key %(server_key)s
  #server %(card2_rad_server1)s port 1852 key %(server_key)s
  #server %(card2_rad_server1)s port 1862 key %(server_key)s
  #server %(card2_rad_server1)s port 1872 key %(server_key)s
  #server %(card2_rad_server1)s port 1882 key %(server_key)s
  exit
 ip pool 10.110.0.0 1024
 ip pool 10.110.4.0 1024
 ip pool 10.110.8.0 1024
 ip pool 10.110.12.0 1024
 ip pool 10.110.16.0 1024
 ip pool 10.110.20.0 1024
 ip pool 10.110.24.0 1024
 ip pool 10.110.28.0 1024
 ip pool 10.110.32.0 1024
 ip pool 10.110.36.0 1024
 ip pool 10.110.40.0 1024
 ip pool 10.110.44.0 1024
 ip pool 10.110.48.0 1024
 ip pool 10.110.52.0 1024
 ip pool 10.110.56.0 1024
 ip pool 10.110.60.0 1024
 ip pool 10.110.64.0 1024
 ip pool 10.110.68.0 1024
 ip pool 10.110.72.0 1024
 ip pool 10.110.76.0 1024
 ip pool 10.110.80.0 1024
 ip pool 10.110.84.0 1024
 ip pool 10.110.88.0 1024
 ip pool 10.110.92.0 1024
 ip pool 10.110.96.0 1024
 ip pool 10.110.100.0 1024
 ip pool 10.110.104.0 1024
 ip pool 10.110.108.0 1024
 ip pool 10.110.112.0 1024
 ip pool 10.110.116.0 1024
 ip pool 10.110.120.0 1024
 ip pool 10.110.124.0 1024
 ip pool 10.110.128.0 1024
 ip pool 10.110.132.0 1024
 ip pool 10.110.136.0 1024
 ip pool 10.110.140.0 1024
 ip pool 10.110.144.0 1024
 ip pool 10.110.148.0 1024
 ip pool 10.110.152.0 1024
 ip pool 10.110.156.0 1024
 ip pool 10.110.160.0 1024
 ip pool 10.110.164.0 1024
 ip pool 10.110.168.0 1024
 ip pool 10.110.172.0 1024
 ip pool 10.110.176.0 1024
 ip pool 10.110.180.0 1024
 ip pool 10.110.184.0 1024
 ip pool 10.110.188.0 1024
 ip pool 10.110.192.0 1024
 ip pool 10.110.196.0 1024
 ip pool 10.110.200.0 1024
 ip pool 10.110.204.0 1024
 ip pool 10.110.208.0 1024
 ip pool 10.110.212.0 1024
 ip pool 10.110.216.0 1024
 ip pool 10.110.220.0 1024
 ip pool 10.110.224.0 1024
 ip pool 10.110.228.0 1024
 ip pool 10.110.232.0 608
 interface subs session
  ip session-default
  ip address %(card2_ses_ip1/mask)s
  exit
 interface active_slot3
  arp arpa
  ip address %(active_slot3_ip/mask)s
  exit
  interface bkp_4slot3
  arp arpa
  ip address %(standby_4slot3_ip/mask)s
  exit
 interface rad_intf_4slot3
  arp arpa
  ip address %(rad_intf_4slot3_ip/mask)s
  exit
 interface bkp_rad_intf_4slot3
  arp arpa
  ip address %(bkp_rad_intf_4slot3_ip/mask)s
  exit
 interface ikev2OnCard3_lpbk loopback
  ip address %(lpbk_3rCard_ip/mask)s
  exit
 rtr 300
  type echo protocol ipicmpecho %(cisco_active_slot3_ip)s source %(active_slot3_ip)s
  exit
 rtr 301
  type echo protocol ipicmpecho %(cisco_standby_4slot3_ip)s source %(standby_4slot3_ip)s
  exit
 rtr 400
  type echo protocol ipicmpecho %(cisco_rad_intf_4slot3_ip)s source %(rad_intf_4slot3_ip)s
  exit
 rtr 401
  type echo protocol ipicmpecho %(cisco_bkp_rad_intf_4slot3_ip)s source %(bkp_rad_intf_4slot3_ip)s
  exit
 rtr schedule 300
 rtr schedule 301
 rtr schedule 401
 rtr schedule 400
 ip route %(card2_route_to_rad)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(card2_clnt_ip_route1)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(card2_clnt_ip_route1)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(card2_route_to_rad)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ip route %(route_sst_slot3)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_sst_slot3)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(route_to_sst_slot3_ip)s %(cisco_active_slot3_ip)s tracker 300
 ip route %(route_to_sst_slot3_ip)s %(cisco_standby_4slot3_ip)s admin-distance 20 tracker 301
 ip route %(ssx_ses_traffic_route)s %(cisco_rad_intf_4slot3_ip)s tracker 400
 ip route %(ssx_ses_traffic_route)s %(cisco_bkp_rad_intf_4slot3_ip)s admin-distance 20 tracker 401
 ipsec policy ikev2 phase1 name ikev2OnCard3
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10800 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 7200 secs
   exit
  exit
 exit
session-home slot 101 loopback interface ikev2OnCard3_lpbk %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase2 name ikev2_p2
 ipsec policy ikev2 phase1 name ikev2OnCard3
 exit
port ethernet %(port_ssx_active_4slot3)s
 bind interface active_slot3 %(context_name)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot3)s
 bind interface rad_intf_4slot3 %(context_name)s
  exit
 enable
 exit
 port ethernet %(port_ssx_bkp_rad_intf_4slot3)s
 bind interface bkp_rad_intf_4slot3 %(context_name1)s
  exit
 enable
 exit
port ethernet %(port_ssx_standby_4slot3)s
 bind interface bkp_4slot3 %(context_name1)s
  exit
 service ipsec
 enable
 exit

context %(context_card2)s
 aaa profile
  session authentication radius
  exit
 radius session authentication profile
  algorithm round-robin
  server %(card2_rad_server1)s port 1842 key %(server_key)s
  server %(card2_rad_server1)s port 1852 key %(server_key)s
  #server %(card2_rad_server1)s port 1922 key %(server_key)s
  #server %(card2_rad_server1)s port 1932 key %(server_key)s
  #server %(card2_rad_server1)s port 1942 key %(server_key)s
  #server %(card2_rad_server1)s port 1952 key %(server_key)s
  #server %(card2_rad_server1)s port 1962 key %(server_key)s
  #server %(card2_rad_server1)s port 1972 key %(server_key)s
  exit
 ip pool 10.222.0.0 1024
 ip pool 10.222.4.0 1024
 ip pool 10.222.8.0 1024
 ip pool 10.222.12.0 1024
 ip pool 10.222.16.0 1024
 ip pool 10.222.20.0 1024
 ip pool 10.222.24.0 1024
 ip pool 10.222.28.0 1024
 ip pool 10.222.32.0 1024
 ip pool 10.222.36.0 1024
 ip pool 10.222.40.0 1024
 ip pool 10.222.44.0 1024
 ip pool 10.222.48.0 1024
 ip pool 10.222.52.0 1024
 ip pool 10.222.56.0 1024
 ip pool 10.222.60.0 1024
 ip pool 10.222.64.0 1024
 ip pool 10.222.68.0 1024
 ip pool 10.222.72.0 1024
 ip pool 10.222.76.0 1024
 ip pool 10.222.80.0 1024
 ip pool 10.222.84.0 1024
 ip pool 10.222.88.0 1024
 ip pool 10.222.92.0 1024
 ip pool 10.222.96.0 1024
 ip pool 10.222.100.0 1024
 ip pool 10.222.104.0 1024
 ip pool 10.222.108.0 1024
 ip pool 10.222.112.0 1024
 ip pool 10.222.116.0 1024
 ip pool 10.222.120.0 1024
 ip pool 10.222.124.0 1024
 ip pool 10.222.128.0 1024
 ip pool 10.222.132.0 1024
 ip pool 10.222.136.0 1024
 ip pool 10.222.140.0 1024
 ip pool 10.222.144.0 1024
 ip pool 10.222.148.0 1024
 ip pool 10.222.152.0 1024
 ip pool 10.222.156.0 1024
 ip pool 10.222.160.0 1024
 ip pool 10.222.164.0 1024
 ip pool 10.222.168.0 1024
 ip pool 10.222.172.0 1024
 ip pool 10.222.176.0 1024
 ip pool 10.222.180.0 1024
 ip pool 10.222.184.0 1024
 ip pool 10.222.188.0 1024
 ip pool 10.222.192.0 1024
 ip pool 10.222.196.0 1024
 ip pool 10.222.200.0 1024
 ip pool 10.222.204.0 1024
 ip pool 10.222.208.0 1024
 ip pool 10.222.212.0 1024
 ip pool 10.222.216.0 1024
 ip pool 10.222.220.0 1024
 ip pool 10.222.224.0 1024
 ip pool 10.222.228.0 1024
 ip pool 10.222.232.0 1024
 ip pool 10.222.236.0 1024
 ip pool 10.222.240.0 1024
 ip pool 10.222.244.0 1024
 ip pool 10.222.248.0 1024
 interface ipsec_lp_21 loopback
  ip address %(ikev2_lpbk_ip/mask)s
  exit
 interface subs session
  ip session-default
  ip address %(card2_ses_ip/mask)s
  exit
 interface client_cisco11_vlan931
  arp arpa
  ip address %(ssx_card2_active/mask)s
  exit
 interface client_cisco14_vlan961_bk
  arp arpa
  ip address %(ssx_card2_standby_ip/mask)s
  exit
 interface service_cisco13_vlan951_bk
  arp arpa
  ip address %(service_bkp_ip/mask)s
  exit
 interface service_cisco17_vlan936
  arp arpa
  ip address %(to_rad_ip/mask)s
  exit
 rtr 100
  type echo protocol ipicmpecho %(cisco_card2_active_ip)s source %(ssx_card2_active)s
  exit
 rtr 101
  type echo protocol ipicmpecho %(cisco_card2_standby_ip)s source %(ssx_card2_standby_ip)s
  exit
 rtr 200
  type echo protocol ipicmpecho %(cisco_to_rad_ip)s source %(to_rad_ip)s
  exit
 rtr 201
  type echo protocol ipicmpecho %(cisco_service_bkp_ip)s source %(service_bkp_ip)s
  exit
 rtr schedule 100
 rtr schedule 101
 rtr schedule 201
 rtr schedule 200
 ip route %(route_to_sst_ses)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ses)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_active_ip)s admin-distance 10 tracker 100
 ip route %(route_to_cisco_sst_ip)s %(cisco_card2_standby_ip)s admin-distance 20 tracker 101
 ip route %(card2_route_to_rad)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ip route %(card2_route_to_rad)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_service_bkp_ip)s admin-distance 20 tracker 201
 ip route %(ssx_ses_traffic_route)s %(cisco_to_rad_ip)s admin-distance 10 tracker 200
 ipsec policy ikev2 phase1 name ikev2_p1
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10800 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ikev2_p2
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 7200 secs
   exit
  exit
 exit
session-home slot 100 loopback interface ipsec_lp_21 %(context_card2)s
 ipsec session context name %(context_card2)s
 ipsec policy ikev2 phase1 name ikev2_p1
 ipsec policy ikev2 phase2 name ikev2_p2
 exit
port ethernet %(port_ssx_active_4slot2)s
 bind interface client_cisco11_vlan931 %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_standby_4slot2)s
 bind interface client_cisco14_vlan961_bk %(context_card2)s
  exit
 service ipsec
 enable
 exit
port ethernet %(port_ssx_rad_intf_4slot2)s
 bind interface service_cisco17_vlan936 %(context_card2)s
  exit
 enable
 exit
port ethernet %(port_ssx_bkp_rad_intf_4slot2)s
 bind interface service_cisco13_vlan951_bk %(context_card2)s
  exit
 enable
 exit
"""%(ipsec_var)

################################################################################

ipsec_var['SST_DoCoMo_PERF_GLCR_SESS_003'] = """
context local
interface to_cisco_slot2
arp arpa
ip address %(sst_cisco_slot2_ip/mask)s
exit
interface to_cisco_slot3
arp arpa
ip address %(sst_cisco_slot3_ip/mask)s
exit
interface to_ixia
arp arpa
ip address %(sst_ixia_ip/mask)s
exit
interface to_ixia_slot3
arp arpa
ip address %(sst_slot3_ixia_ip/mask)s
exit
ip route %(card2_route_active_ssx)s %(cisco_sst_slot2_ip)s
ip route %(card2_route_standby_ssx)s %(cisco_sst_slot2_ip)s
ip route %(route_sst_ixia)s %(ixia_sst_ip)s
ip route %(route_sst_slot3_ixia)s %(ixia_sst_slot3_ip)s
 ipsec policy ikev2 phase1 name p1_AES
  suite1
   gw-authentication psk SBM_demo
   peer-authentication eap
   hard-lifetime 11100 secs
   soft-lifetime 10400 secs
   exit
  exit
 ipsec policy ikev2 phase2 name p2_AES
  suite1
   hard-lifetime 7500 secs
   soft-lifetime 6900 secs
   exit
  exit
 exit
port ethernet %(port_sst_slot2)s
 bind interface to_cisco_slot2 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
port ethernet %(port_sst_slot3)s
 bind interface to_cisco_slot3 local
  ipsec policy ikev2 phase1 name p1_AES
  ipsec policy ikev2 phase2 name p2_AES
  exit
 service ipsec
 enable
 exit
port ethernet %(port_sst_ixia)s
 bind interface to_ixia local
  ip host 81.0.0.1 00:11:22:33:44:21
  exit
 enable
 exit
port ethernet %(port_sst_slot3_ixia)s
 bind interface to_ixia_slot3 local
  exit
 enable
 exit
"""%ipsec_var

################################################################################

ipsec_var['DoCoMo_PERF_NONGLCR_006'] = others_var['DoCoMo_8_1_1']

################################################################################
route_var['NTT_4_1_6'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 router-id 1.1.1.1
 router ospf
  area 0
   interface vr1
    network-type point-to-point
    mtu-ignore
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s
  bind interface vr1 %(context_name1)s
   exit
 enable
 exit
"""%route_var

route_var['NTT_4_1_5'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 router-id 56.1.2.1
 router ospf
  area 0
   interface vr1
    mtu-ignore
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s
  bind interface vr1 %(context_name1)s
   exit
 enable
 exit
"""%route_var

route_var['NTT_4_1_12'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 router-id 56.1.2.1
 router ospf
  area 0
   interface vr1
   mtu-ignore
  priority 100
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s
  bind interface vr1 %(context_name1)s
   exit
 enable
 exit
"""%route_var


route_var['NTT_4_1_14'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 router-id 56.1.2.1
 router ospf
  area 0
   interface vr1
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s
  bind interface vr1 %(context_name1)s
   exit
 enable
 exit
"""%route_var


route_var['NTT_4_1_22'] = """
context %(context_name1)s
 interface vr1
  arp arpa
  ip unreachables
  ip mtu 1500
  ip address %(ospf_intf1_ip/mask)s
  exit
 interface lo0 loopback
  ip address %(loopback_ip1/mask)s
  exit
 router-id 56.1.2.1
 router ospf
  redistribute static
  redistribute connected
  area 0
   interface vr1
    mtu-ignore
    exit
   exit
  exit
 exit
port ethernet %(port_ssx1_cisco)s dot1q
 vlan %(ospf_vlan1)s
  bind interface vr1 %(context_name1)s
   exit
  exit
 enable
 exit
"""%route_var

route_var['NTT_4_1_23'] = route_var['NTT_4_1_22'] 
route_var['NTT_4_1_23'] = route_var['NTT_4_1_22']
route_var['NTT_4_1_20'] = route_var['NTT_4_1_22']
route_var['NTT_4_1_21'] = route_var['NTT_4_1_23']

