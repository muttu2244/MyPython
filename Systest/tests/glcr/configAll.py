import topo
#import topoOrig
script_var = {}
#Testopia configs
script_var['username'] = "automation@stoke.com"
script_var['password'] = "automation"
script_var['url']      = "https://bugzilla.stoke.com/xmlrpc.cgi"



#SSX configurations

script_var['context_name'] = 'stoke1'
script_var['tunnel_name']  = 'tun0_1'
script_var['acl_name'] = 'stoke1ACL'
script_var['acl_name1'] = 'session_acl'
script_var['sess_name'] = 'aclses'
script_var['radiusLoc'] = '/a/radius1/sbin/'
script_var['active_slot2_ip'] = '17.1.1.2'
script_var['active_slot2_ip_mask'] = '17.1.1.2/24'
script_var['cisco_active_slot2_ip'] = '17.1.1.1'
script_var['cisco_active_slot2_ip_mask'] = '17.1.1.1 255.255.255.0'

script_var['standby_slot4_ip'] = '27.1.1.2'
script_var['standby_slot4_ip_mask'] = '27.1.1.2/24'
script_var['cisco_standby_slot4_ip'] = '27.1.1.1'
script_var['cisco_standby_slot4_ip_mask'] = '27.1.1.1 255.255.255.0'

script_var['service_slot2_ip'] = '18.1.1.2'
script_var['service_slot2_ip_mask'] = '18.1.1.2/24'
script_var['cisco_service_slot2_ip'] = '18.1.1.1'
script_var['cisco_service_slot2_ip_mask'] = '18.1.1.1 255.255.255.0'

script_var['service_standby_slot2_ip'] = '28.1.1.2'
script_var['service_standby_slot2_ip_mask'] = '28.1.1.2/24'
script_var['cisco_service_standby_slot2_ip'] = '28.1.1.1'
script_var['cisco_active_standby_slot2_ip_mask'] = '28.1.1.1 255.255.255.0'



script_var['tr_Active1_vlan'] = 1000
script_var['tr_Stdby1_vlan'] =  1001

script_var['tr_Active1_port']= topo.p_tr_active1_ssx_cisco_slot2[0]
script_var['tr_stdBy1_port'] = topo.p_tr_stdby1_ssx_cisco_slot4[0]
script_var['sr_Active1_port']= topo.p_sr_active1_ssx_cisco_slot3[0]
script_var['sr_stdBy1_port'] = topo.p_sr_stdby1_ssx_cisco_slot4[0]


script_var['p_tr_active1_ssx_cisco_slot2']= topo.p_tr_active1_ssx_cisco_slot2[1]
script_var['p_tr_stdby1_ssx_cisco_slot4'] = topo.p_tr_stdby1_ssx_cisco_slot4[1]
script_var['p_sr_active1_ssx_cisco_slot3']= topo.p_sr_active1_ssx_cisco_slot3[1]
script_var['p_sr_stdby1_ssx_cisco_slot4'] = topo.p_sr_stdby1_ssx_cisco_slot4[1]

script_var['p_cisco_linux'] = topo.p_cisco_linux[0]

script_var['tnLpBkIp'] =  '4.4.4.4'
script_var['tnLpBkIpMsk'] =  '4.4.4.4/32'
script_var['tnIFIpMsk']   =  '120.1.1.1/32'

script_var['tnLpNw'] = '4.4.4.0/24'
script_var['tnIfNw'] = '120.1.1.0/24'


script_var['tnLpBkIpMsk1'] =  '4.4.4.4 255.255.255.255'
script_var['tnIFIpMsk1']   =  '120.1.1.1 255.255.255.255'


script_var['xpVpnNwIp']   =  '11.11.11.0'
script_var['xpVpnNwMsk']   =  '11.11.11.0/24'

script_var['psk_val']   =  1234567890

script_var['slot2LogNo']= 100

script_var['lanIpMsk']= '2.2.2.2/32'
script_var['lanIp_mask'] = '2.2.2.2 255.255.255.255'
script_var['xpVpnHstIp']= '11.11.11.11'
script_var['xpVpnHstMsk']= '11.11.11.11/32'

script_var['xpVpnHstIpMsk']= '11.11.11.11/24'
script_var['xpVpnHstIFMsk']= '11.11.11.11 255.255.255.0'
script_var['xpVpnNwRevMsk']= '11.11.11.0 0.0.0.255'

script_var['ciscoxpVpnHstIp']= '11.11.11.12'

script_var['ciscoxpVpnHstIpMsk']= '11.11.11.12  255.255.255.0'

script_var['xpVpnSesHstIp']= '33.33.33.33'
script_var['xpVpnSesHstMsk']= '33.33.33.33/32'
script_var['xpVpnSesHstIpMsk']= '33.33.33.33/24'
script_var['xpVpnSesHstIFMsk']= '33.33.33.33 255.255.255.0'
script_var['ciscoxpVpnSesHstIp']= '33.33.33.34'
script_var['ciscoxpVpnSesHstIpMsk']= '33.33.33.34 255.255.255.0'
script_var['xpVpnSesHstIFRevMsk']= '33.33.33.0 0.0.0.255'

script_var['linux1']= '22.22.22.22'
script_var['cisco_intf_ipmask'] = '22.22.22.23 255.255.255.0'
script_var['linux1_intf_ip_mask'] = '22.22.22.22/24'
script_var['linux1RevMsk']= '22.22.22.0 0.0.0.255'
script_var['linux1_route_mask'] = '22.22.22.0/24'
script_var['linux_nw'] = '11.11.11.0/24'
script_var['linux2_route_mask'] = '33.33.33.0/24'
script_var['linux1_nexthop_ip'] = '22.22.22.23'


script_var['prim_dns'] = '172.16.24.150'
script_var['sec_dns'] = '172.16.24.151'
script_var['def_prim_dns'] = '20.20.20.21'
script_var['def_sec_dns'] = '20.20.20.22'
script_var['ip_netmask'] = '255.255.255.255'
script_var['rad_port'] = '1822'
script_var['ip_pool'] = '25.25.25.1'
script_var['ip_pool_ipmask'] = '25.25.25.0 255.255.255.0'
script_var['ip_pool_mask'] = '25.25.25.0/24'
script_var['sess_lb'] = '6.6.6.6/32'
script_var['sess_loopback1'] = '96.1.1.1'
script_var['loopback1'] = '96.1.1.1/32'
script_var['loopbackMsk'] = '96.1.1.0/24'
script_var['loopback2'] = '100.100.100.100/32'
script_var['rtr1'] = '8000'
script_var['rtr2'] = '8500'
script_var['rtr3'] = '9100'
script_var['rtr4'] = '9200'
script_var['sess_psk_val'] = '12345'
script_var['sess_ph1_soft_lifetime']= 3000
script_var['sess_ph2_soft_lifetime']= 60
script_var['sess_ph1_hard_lifetime']= 3600
script_var['sess_ph2_hard_lifetime']= 3600


script_var['dpdInt']= 60
script_var['rtryInt']= 30
script_var['mxRtry']= 3
script_var['rTrInt']= 15
script_var['maxRtr']= 5
script_var['sesRemTimInt']= 1200
script_var['ph1_soft_lifetime']= 160
script_var['ph2_soft_lifetime']= 60
script_var['ph1_hard_lifetime']= 460
script_var['ph2_hard_lifetime']= 360

##########################################################################
script_var['test_GRED_ACL_TUN_FUN_001']= """
ipsec global profile
 dpd interval %(dpdInt)s retry-interval %(rtryInt)s maximum-retries %(mxRtry)s
 retransmit interval %(rTrInt)s maximum-retries %(maxRtr)s send-retransmit-response

 session-remove-timer interval %(sesRemTimInt)s
 exit
context %(context_name)s
 interface active
  arp arpa
  ip address %(active_slot2_ip_mask)s
  exit
 interface service
  arp arpa
  ip address %(service_slot2_ip_mask)s
  exit
 interface service_standby
  arp arpa
  ip address %(service_standby_slot2_ip_mask)s
  exit
 interface standby
  arp arpa
  ip address %(standby_slot4_ip_mask)s
  exit
 interface tun_lp loopback
  ip address %(tnLpBkIpMsk)s
  exit
 interface tun_iface tunnel
  ip address %(tnIFIpMsk)s
  exit
 ip route %(xpVpnNwMsk)s %(cisco_active_slot2_ip)s
 ip route %(xpVpnNwMsk)s %(cisco_standby_slot4_ip)s admin-distance 10
 ip route %(linux1_route_mask)s %(cisco_service_slot2_ip)s
 ip route %(linux1_route_mask)s %(cisco_service_standby_slot2_ip)s admin-distance 10
ipsec policy ikev2 phase1 name 1p1
  suite1
   gw-authentication psk %(psk_val)s
   peer-authentication psk
   hard-lifetime %(ph1_hard_lifetime)s secs
   soft-lifetime %(ph1_soft_lifetime)s secs
   exit
  exit
 ipsec policy ikev2 phase2 name 1p2
  suite1
   hard-lifetime %(ph2_hard_lifetime)s secs
   soft-lifetime %(ph2_soft_lifetime)s secs
   exit
  exit
 exit
admin-access global profile
 exit
session-home slot %(slot2LogNo)s loopback interface tun_lp %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 exit
no port ethernet %(tr_Active1_port)s dot1q
port ethernet %(tr_Active1_port)s dot1q
 vlan %(tr_Active1_vlan)s
  bind interface active %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_Active1_port)s
port ethernet %(sr_Active1_port)s
 bind interface service %(context_name)s
  exit
 enable
 exit
no port ethernet %(tr_stdBy1_port)s dot1q
port ethernet %(tr_stdBy1_port)s dot1q
 vlan %(tr_Stdby1_vlan)s
  bind interface standby %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_stdBy1_port)s
port ethernet %(sr_stdBy1_port)s
 bind interface service_standby %(context_name)s
  exit
 enable
 exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
  ip route %(lanIpMsk)s
  ip route %(xpVpnHstMsk)s
  exit
 ipsec policy ikev2 phase2 name 1p2
 ipsec policy ikev2 phase1 name 1p1
  psk %(psk_val)s
  exit
 exit
""" %script_var
#print script_var['ACL_FUN_010']

##########################################################################


script_var['test_ACL_Func_Main']= """
ipsec global profile
 dpd interval %(dpdInt)s retry-interval %(rtryInt)s maximum-retries %(mxRtry)s
 retransmit interval %(rTrInt)s maximum-retries %(maxRtr)s send-retransmit-response

 session-remove-timer interval %(sesRemTimInt)s
 exit
context %(context_name)s
 interface active
  arp arpa
  ip unreachable
  ip address %(active_slot2_ip_mask)s
  exit
 interface service
  arp arpa
  ip unreachable
  ip address %(service_slot2_ip_mask)s
  exit
 interface service_standby
  arp arpa
  ip unreachable
  ip address %(service_standby_slot2_ip_mask)s
  exit
 interface standby
  arp arpa
  ip unreachable
  ip address %(standby_slot4_ip_mask)s
  exit
 interface tun_lp loopback
  ip address %(tnLpBkIpMsk)s
  exit
 interface tun_iface tunnel
  ip address %(tnIFIpMsk)s
  exit
 ip route %(xpVpnNwMsk)s %(cisco_active_slot2_ip)s
 ip route %(xpVpnNwMsk)s %(cisco_standby_slot4_ip)s admin-distance 10
 ip route %(linux1_route_mask)s %(cisco_service_slot2_ip)s
 ip route %(linux1_route_mask)s %(cisco_service_standby_slot2_ip)s admin-distance 10
 ipsec policy ikev2 phase1 name 1p1
  suite1
   gw-authentication psk %(psk_val)s
   peer-authentication psk
   hard-lifetime %(ph1_hard_lifetime)s secs
   soft-lifetime %(ph1_soft_lifetime)s secs
   exit
  exit
 ipsec policy ikev2 phase2 name 1p2
  suite1
   hard-lifetime %(ph2_hard_lifetime)s secs
   soft-lifetime %(ph2_soft_lifetime)s secs
   exit
  exit
 exit
admin-access global profile
 exit
session-home slot %(slot2LogNo)s loopback interface tun_lp %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 exit
no port ethernet %(tr_Active1_port)s dot1q
port ethernet %(tr_Active1_port)s dot1q
 vlan %(tr_Active1_vlan)s
  bind interface active %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_Active1_port)s
port ethernet %(sr_Active1_port)s
 bind interface service %(context_name)s
  exit
 enable
 exit
no port ethernet %(tr_stdBy1_port)s dot1q
port ethernet %(tr_stdBy1_port)s dot1q
 vlan %(tr_Stdby1_vlan)s
  bind interface standby %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_stdBy1_port)s
port ethernet %(sr_stdBy1_port)s
 bind interface service_standby %(context_name)s
  exit
 enable
 exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
  ip route %(lanIpMsk)s
  ip route %(xpVpnHstMsk)s
  exit
 ipsec policy ikev2 phase2 name 1p2
 ipsec policy ikev2 phase1 name 1p1
  psk %(psk_val)s
  exit
 exit
""" %script_var
#print script_var['ACL_FUN_010'] 


##########################################################################
script_var['test_ACL_Func_Sess']= """
aaa global profile
 default-domain authentication stoke1
 exit

ipsec global profile
 dpd interval %(dpdInt)s retry-interval %(rtryInt)s maximum-retries %(mxRtry)s
 retransmit interval %(rTrInt)s maximum-retries %(maxRtr)s send-retransmit-response
 session-remove-timer interval %(sesRemTimInt)s
 exit

context stoke1
 aaa profile
  session accounting none
  session authentication radius
  service authorization local
  max-session 10000
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name %(sess_name)s 
  dns primary %(prim_dns)s
  dns secondary %(sec_dns)s
  ip address pool
  ip netmask %(ip_netmask)s
  class-of-service aclser
  event volume 1000_bytes
  exit
session profile default
  dns primary %(def_prim_dns)s
  dns secondary %(def_sec_dns)s
  ip address pool
  ip netmask %(ip_netmask)s
  timeout absolute 7200
  exit
 radius session authentication profile
  algorithm round-robin
  server %(linux1)s port %(rad_port)s key topsecret
  exit
 ip pool %(ip_pool)s 1000
 interface service_standby
  arp arpa
  ip address %(service_standby_slot2_ip_mask)s
  exit
 interface service
  arp arpa
  ip address %(service_slot2_ip_mask)s
  exit
 interface ses_int session loopback
  ip session-default
  ip address %(sess_lb)s
  exit
 interface loopback1 loopback
  ip address %(loopback1)s
  exit
 interface loopback2 loopback
  ip address %(loopback2)s
  exit
 interface active
  arp arpa
  ip address %(active_slot2_ip_mask)s
  exit
 interface standby
  arp arpa
  ip address %(standby_slot4_ip_mask)s
  exit
 interface tun_lp loopback
  ip address %(tnLpBkIpMsk)s
  exit
 interface tun_iface tunnel
  ip address %(tnIFIpMsk)s
  exit
 rtr %(rtr1)s
  type echo protocol ipicmpecho %(cisco_service_slot2_ip)s source %(service_slot2_ip)s
  frequency 60
  exit
 rtr %(rtr2)s
  type echo protocol ipicmpecho %(cisco_service_standby_slot2_ip)s source %(service_standby_slot2_ip)s
  frequency 60
  exit
 rtr %(rtr3)s
  type echo protocol ipicmpecho %(cisco_active_slot2_ip)s source %(active_slot2_ip)s
  frequency 60
  exit
 rtr %(rtr4)s
  type echo protocol ipicmpecho %(cisco_standby_slot4_ip)s source %(standby_slot4_ip)s
  frequency 60
  exit
 rtr schedule %(rtr1)s
 rtr schedule %(rtr2)s
 rtr schedule %(rtr3)s
 rtr schedule %(rtr4)s
 ip route %(linux1_route_mask)s %(cisco_service_slot2_ip)s tracker %(rtr1)s
 ip route %(linux1_route_mask)s %(cisco_service_standby_slot2_ip)s admin-distance 20 tracker %(rtr2)s
 ip route %(linux_nw)s %(cisco_active_slot2_ip)s tracker %(rtr3)s
 ip route %(linux_nw)s %(cisco_standby_slot4_ip)s admin-distance 20 tracker %(rtr4)s
 ip route %(linux2_route_mask)s %(cisco_active_slot2_ip)s tracker %(rtr3)s
 ip route %(linux2_route_mask)s %(cisco_standby_slot4_ip)s admin-distance 20 tracker %(rtr4)s
 ipsec policy ikev2 phase1 name 1p1
  suite1
   gw-authentication psk %(psk_val)s
   peer-authentication psk
   hard-lifetime %(ph1_hard_lifetime)s secs
   soft-lifetime %(ph1_soft_lifetime)s secs
   exit
  exit
 ipsec policy ikev2 phase2 name 1p2
  suite1
   hard-lifetime %(ph2_hard_lifetime)s secs
   soft-lifetime %(ph2_soft_lifetime)s secs
   exit
  exit
 ipsec policy ikev2 phase1 name ph1_eap_crypto_001
  custom
   gw-authentication psk %(sess_psk_val)s
   peer-authentication eap
   hard-lifetime %(sess_ph1_hard_lifetime)s secs
   soft-lifetime %(sess_ph1_soft_lifetime)s secs
   encryption aes128
   hash sha-1
   d-h group5
   prf sha-1
   exit
  exit
 ipsec policy ikev2 phase2 name ph2_cust_crypt_001
  custom
   hard-lifetime %(sess_ph2_hard_lifetime)s secs
   soft-lifetime %(sess_ph2_soft_lifetime)s secs
   encryption aes128
   hash sha-1
   pfs group2
   exit
  exit
 exit
admin-access global profile
 exit
session-home slot 100 loopback interface loopback1 stoke1
 ipsec session context name stoke1
 ipsec policy ikev2 phase1 name ph1_eap_crypto_001
 ipsec policy ikev2 phase2 name ph2_cust_crypt_001
 exit
session-home slot 100 loopback interface tun_lp stoke1
 ipsec session context name stoke1
 ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 exit

port ethernet %(tr_Active1_port)s dot1q
 vlan %(tr_Active1_vlan)s
  bind interface active %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit

port ethernet %(sr_Active1_port)s
 bind interface service %(context_name)s
  exit
 enable
 exit
port ethernet %(tr_stdBy1_port)s dot1q
 vlan %(tr_Stdby1_vlan)s
  bind interface standby %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %(sr_stdBy1_port)s
 bind interface service_standby %(context_name)s
  exit
 enable
 exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
  ip route %(lanIpMsk)s
  ip route %(xpVpnHstMsk)s
  exit
 ipsec policy ikev2 phase2 name 1p2
 ipsec policy ikev2 phase1 name 1p1
  psk %(psk_val)s
  exit
 exit

""" %script_var



##########################################################################

script_var['test_ACL_untagged_port']= """
ipsec global profile
 dpd interval %(dpdInt)s retry-interval %(rtryInt)s maximum-retries %(mxRtry)s
 retransmit interval %(rTrInt)s maximum-retries %(maxRtr)s send-retransmit-response

 session-remove-timer interval %(sesRemTimInt)s
 exit
context %(context_name)s
 interface active
  arp arpa
  ip address %(active_slot2_ip_mask)s
  exit
 interface service
  arp arpa
  ip address %(service_slot2_ip_mask)s
  exit
 interface service_standby
  arp arpa
  ip address %(service_standby_slot2_ip_mask)s
  exit
 interface standby
  arp arpa
  ip address %(standby_slot4_ip_mask)s
  exit
 interface tun_lp loopback
  ip address %(tnLpBkIpMsk)s
  exit
 interface tun_iface tunnel
  ip address %(tnIFIpMsk)s
  exit

 ip route %(xpVpnNwMsk)s %(cisco_active_slot2_ip)s
 ip route %(xpVpnNwMsk)s %(cisco_standby_slot4_ip)s admin-distance 10
 ip route %(linux1_route_mask)s %(cisco_service_slot2_ip)s
 ip route %(linux1_route_mask)s %(cisco_service_standby_slot2_ip)s admin-distance 10
admin-access global profile
 exit
session-home slot %(slot2LogNo)s loopback interface tun_lp %(context_name)s
 ipsec session context name %(context_name)s
 exit
no port ethernet %(tr_Active1_port)s dot1q
port ethernet %(tr_Active1_port)s dot1q
 vlan %(tr_Active1_vlan)s untagged
  bind interface active %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_Active1_port)s
port ethernet %(sr_Active1_port)s
 bind interface service %(context_name)s
  exit
 enable
 exit
no port ethernet %(tr_stdBy1_port)s dot1q
port ethernet %(tr_stdBy1_port)s dot1q
 vlan %(tr_Stdby1_vlan)s
  bind interface standby %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
no port ethernet %(sr_stdBy1_port)s
port ethernet %(sr_stdBy1_port)s
 bind interface service_standby %(context_name)s
  exit
 enable
 exit
 
""" %script_var
##########################################################################

script_var['fun_001_xpressvpn'] = """
### this is the new configuration format.
ike listen %(xpVpnHstIp)s   500
ike listen %(xpVpnHstIp)s  4500
ike start

### IKE debugging
ike log                 stdout off
ike log                 file off
ike log                 filename xpressvpn.log
ike decode              full
ike debug               off

### IPSec debugging
#ipsec pktdump           error full
#ipsec log               debug


alias LHOST %(xpVpnHstIp)s                           #this is the physical IP of the XpressVPN client PC
alias RHOST %(tnLpBkIp)s                          #this is the physical IP of the SSX
alias IKE_SEL ${LHOST},${RHOST}
ike ph1 addx    IKE_SEL  main psk %(psk_val)s aes-128 sha1 2 %(ph1_soft_lifetime)s v2
#ike ph1 options IKE_SEL  mode-cfg-client
#ike ph1 options IKE_SEL  initial-contact
#ike ph1 myid    IKE_SEL  userfqdn test-session@stoke
ike ph2 addx    %(xpVpnHstMsk)s 0.0.0.0/0 0 IKE_SEL esp tunnel aes-128 sha1 2 %(ph2_soft_lifetime)s
ike connect any

""" % script_var
#print script_var['fun_001_xpressvpn']
##########################################################################

script_var['fun_013_xpressvpn'] = """
### this is the new configuration format.
ike listen %(xpVpnHstIp)s   500
ike listen %(xpVpnHstIp)s  4500
ike start

### IKE debugging
ike log                 stdout off
ike log                 file off
ike log                 filename xpressvpn.log
ike decode              full
ike debug               off

### IPSec debugging
#ipsec pktdump           error full
#ipsec log               debug


alias LHOST %(xpVpnHstIp)s                           #this is the physical IP of the XpressVPN client PC
alias RHOST %(tnLpBkIp)s                          #this is the physical IP of the SSX
alias IKE_SEL ${LHOST},${RHOST}
ike ph1 addx    IKE_SEL  main psk %(psk_val)s aes-128 sha1 2 500 v2
#ike ph1 options IKE_SEL  mode-cfg-client
#ike ph1 options IKE_SEL  initial-contact
#ike ph1 myid    IKE_SEL  userfqdn test-session@stoke
ike ph2 addx    %(xpVpnHstMsk)s 0.0.0.0/0 0 IKE_SEL esp tunnel aes-128 sha1 2 300
ike connect any

""" % script_var

#####################################################################
script_var['fun_011_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap
ike listen any  500
ipsec addr add %(xpVpnSesHstIFMsk)s 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt


#test multiclient set remote           %(tnLpBkIp)s 500
test multiclient set remote           %(sess_loopback1)s 500
test multiclient set local            %(xpVpnSesHstIp)s  500
test multiclient set numclients       1
#test multiclient set numclients        100
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           %(sess_psk_val)s
#test multiclient set ph1 myid          userfqdn 165012345@stoke1
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context_name)s
#test multiclient set max-concurrent    1
test multiclient set max-concurrent    10
test multiclient set incr-ph1-life     1
test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          aes-128
test multiclient set ph2 hash          sha1
test  multiclient set ph2 dh           2
test multiclient set ph2 life          12000
test multiclient set ph2-wild
test multiclient set delay 200
test multiclient configure
ike start
test multiclient connect


""" % script_var
#####################################################################

script_var['deny_icmp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_icmp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['deny_icmp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_icmp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['deny_igmp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_igmp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['deny_igmp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_igmp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################

script_var['deny_tcp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_tcp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['deny_tcp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_tcp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################

script_var['deny_udp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_udp_out'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
end
""" %script_var
######################################################################
script_var['deny_udp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['permit_udp_in'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
end
""" %script_var
######################################################################
script_var['deny_udp'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2 
 ip access-group in name %(acl_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit


port ethernet %(tr_stdBy1_port)s dot1q
vlan %(tr_Stdby1_vlan)s
bind interface standby %(context_name)s
ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 ip access-group in name %(acl_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
exit
exit
end

""" %script_var
######################################################################

script_var['permit_udp'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 ip access-group in name %(acl_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit


port ethernet %(tr_stdBy1_port)s dot1q
vlan %(tr_Stdby1_vlan)s
bind interface standby %(context_name)s
ipsec policy ikev2 phase1 name 1p1
 ipsec policy ikev2 phase2 name 1p2
 ip access-group in name %(acl_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['permit_icmp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit icmp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_icmp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny icmp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################

script_var['permit_icmp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit icmp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_icmp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny icmp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_igmp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny igmp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_igmp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit igmp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_igmp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny igmp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_igmp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit igmp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_udp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny udp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_udp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit udp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_udp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny udp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_udp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit udp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_tcp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny tcp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_tcp_sess_in'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit tcp any any
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_tcp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny tcp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_tcp_sess_out'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit tcp any any
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################






script_var['permit_in_icmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp any any
exit
exit
port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['permit_out_icmp_port'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_in_icmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_out_icmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_out_igmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_in_igmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['permit_out_igmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################
script_var['permit_in_igmp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['permit_in_tcp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['permit_out_tcp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_out_tcp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################
script_var['deny_in_tcp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
######################################################################

script_var['deny_in_udp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
#########################################################################
script_var['deny_out_udp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
#########################################################################
script_var['permit_in_udp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
#########################################################################
script_var['permit_out_udp_port'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 exit
 enable
 exit
exit
end
""" %script_var
#########################################################################

script_var['deny_out_icmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['deny_in_icmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################

script_var['permit_in_icmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_out_icmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['deny_out_igmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['deny_in_igmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_in_igmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_out_igmp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################

script_var['deny_out_tcp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['deny_in_tcp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_in_tcp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_out_tcp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################

script_var['deny_out_udp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['deny_in_udp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_in_udp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################
script_var['permit_out_udp_port_untag'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp any any
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s untagged
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit

exit
""" %script_var
######################################################################

script_var['deny_icmp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 3 
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_icmp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['deny_icmp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny icmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_icmp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit icmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_igmp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_igmp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_igmp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny igmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_igmp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit igmp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_ip_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny ip %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_ip_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit ip %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_ip_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny ip %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_ip_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit ip %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_tcp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_tcp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_tcp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny tcp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_tcp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit tcp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_udp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_udp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################
script_var['deny_udp_out_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group out name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_udp_in_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit
tunnel %(tunnel_name)s type ipsec protocol ip44 context %(context_name)s
 enable
 ip local %(tnLpBkIp)s remote %(xpVpnHstIp)s
 bind interface tun_iface %(context_name)s
 ip access-group in name %(acl_name)s
exit
exit
""" %script_var
####################################################################

script_var['permit_icmp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit icmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_icmp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny icmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################


script_var['permit_icmp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit icmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_icmp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny icmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_igmp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit igmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_igmp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny igmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################

script_var['permit_igmp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit igmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_igmp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny igmp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_ip_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit ip %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_ip_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny ip %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_ip_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit ip %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_ip_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny ip %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_tcp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit tcp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_tcp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny tcp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_tcp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit tcp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_tcp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny tcp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################

script_var['permit_udp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 permit udp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 3
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_udp_sess_in_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
10 deny udp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
session name %(sess_name)s
 ip access-group in name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['permit_udp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 permit udp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 0 tos 1
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################
script_var['deny_udp_sess_out_options'] = """
context %(context_name)s
ip access-list %(acl_name1)s
20 deny udp %(xpVpnSesHstIFRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
session name %(sess_name)s
 ip access-group out name %(acl_name1)s
end
""" %script_var
######################################################################

script_var['deny_out_udp_port_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 deny udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 1 tos 2
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group out name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit
exit
""" %script_var
#########################################################################
script_var['permit_in_udp_port_options'] = """
context %(context_name)s
ip access-list %(acl_name)s
10 permit udp %(xpVpnNwRevMsk)s %(linux1RevMsk)s precedence 2 tos 0
exit
exit

port ethernet %(tr_Active1_port)s dot1q
vlan %(tr_Active1_vlan)s
bind interface active %(context_name)s
 ip access-group in name %(acl_name)s
exit
 service ipsec
 exit
 enable
 exit
exit
""" %script_var
#########################################################################


script_var['rad_users_acl_in_out'] = """
DEFAULT User-Name =~ "1650[0-9]*@stoke1",Auth-Type := EAP,EAP-Type := SIM
        EAP-Sim-Rand1 = 0x8552dae4911cf762dd2455253f408647,
        EAP-Sim-SRES1 = 0x8543f8d7,
        EAP-Sim-KC1 = 0xd549911555bdff9e,
        EAP-Sim-Rand2 = 0x8f4833e2712070145c1899a9af279675,
        EAP-Sim-SRES2 = 0x8f5911d1,
        EAP-Sim-KC2 = 0x35751663d4813312,
        EAP-Sim-Rand3 = 0x9640c3e106cec1365b107102a56bf7e9,
        EAP-Sim-SRES3 = 0x9651e1d2,
        EAP-Sim-KC3 = 0x429ba741d389dbb9,
        Stoke-ACL-In = %(acl_name1)s,
        Stoke-ACL-Out = %(acl_name1)s,
        Framed-IP-Address = 255.255.255.254,
        Framed-IP-Netmask = 255.255.255.255

""" %script_var
######################################################################

script_var['rad_users_acl_in'] = """
DEFAULT User-Name =~ "1650[0-9]*@stoke1",Auth-Type := EAP,EAP-Type := SIM
        EAP-Sim-Rand1 = 0x8552dae4911cf762dd2455253f408647,
        EAP-Sim-SRES1 = 0x8543f8d7,
        EAP-Sim-KC1 = 0xd549911555bdff9e,
        EAP-Sim-Rand2 = 0x8f4833e2712070145c1899a9af279675,
        EAP-Sim-SRES2 = 0x8f5911d1,
        EAP-Sim-KC2 = 0x35751663d4813312,
        EAP-Sim-Rand3 = 0x9640c3e106cec1365b107102a56bf7e9,
        EAP-Sim-SRES3 = 0x9651e1d2,
        EAP-Sim-KC3 = 0x429ba741d389dbb9,
        Stoke-ACL-In = %(acl_name1)s,
        Framed-IP-Address = 255.255.255.254,
        Framed-IP-Netmask = 255.255.255.255

""" %script_var
######################################################################

script_var['rad_users_acl_out'] = """
DEFAULT User-Name =~ "1650[0-9]*@stoke1",Auth-Type := EAP,EAP-Type := SIM
        EAP-Sim-Rand1 = 0x8552dae4911cf762dd2455253f408647,
        EAP-Sim-SRES1 = 0x8543f8d7,
        EAP-Sim-KC1 = 0xd549911555bdff9e,
        EAP-Sim-Rand2 = 0x8f4833e2712070145c1899a9af279675,
        EAP-Sim-SRES2 = 0x8f5911d1,
        EAP-Sim-KC2 = 0x35751663d4813312,
        EAP-Sim-Rand3 = 0x9640c3e106cec1365b107102a56bf7e9,
        EAP-Sim-SRES3 = 0x9651e1d2,
        EAP-Sim-KC3 = 0x429ba741d389dbb9,
        Stoke-ACL-Out = %(acl_name1)s,
        Framed-IP-Address = 255.255.255.254,
        Framed-IP-Netmask = 255.255.255.255

""" %script_var
######################################################################



