import topo

script_var = {}
psr_var={}
if topo.p_ssx2_cisco[0].split("/")[0] == "3":        # Logical slot for Initiator
        psr_var['ini_logical_slot'] = "3"
else:
        psr_var['ini_logical_slot'] = "2"

# SSX vars
script_var['hello_int'] = 30
script_var['hello_new'] = 40
script_var['hello_mul'] = "4"
script_var['poll_int'] = 120
script_var['changed_hello'] = '45'
script_var['dead_int_def'] = '120'
script_var['context_name'] = 'ospf1'
script_var['context_name1'] = 'ospf2'
script_var['context_name2'] = 'ospf3'
script_var['area_id'] = '0'
script_var['intf1_ip'] = '3.3.3.1'
script_var['intf1_ip/mask'] = '3.3.3.1/24'
script_var['intf_lo1_ip']  = '10.10.10.10'
script_var['area_id1'] = '10'
script_var['area_id2'] = '1'
script_var['area_id3'] = '2'
script_var['cost'] = '20'
#SSX Variables
script_var['context_common'] = 'NTT'
script_var['ssx_phy_iface_ip'] = '17.1.1.2'
script_var['ssx_phy_iface_ip_mask'] = '17.1.1.2/24'
script_var['ssx_loopback_iface_ip'] = '4.4.4.4'
script_var['ssx_loopback_iface_ip_mask'] = '4.4.4.4/32'
script_var['ssx_loopback_net'] = '4.4.0.0/16'
script_var['ssx_phy_iface1_ip'] = '16.1.1.2'
script_var['ssx_phy_iface1_ip_mask'] = '16.1.1.2/24'
script_var['ssx_phy_iface2_ip'] = '19.1.1.2'
script_var['ssx_phy_iface2_ip_mask'] = '19.1.1.2/24'
script_var['ssx_phy_iface3_ip'] = '20.1.1.2'
script_var['ssx_phy_iface3_ip_mask'] = '20.1.1.2/24'
script_var['ssx_port_2'] = topo.p1_ssx_ixia[0]
script_var['ssx_port_3'] = topo.p2_ssx_ixia[0]
script_var['ntp_server'] = '172.16.0.10'

# Please provide the valid PATH of OS on server
script_var['Stoke_Os_Path'] = "/auto/build/builder/laurel/2011062801/qnx/cb/mc"

#SSX Variables
psr_var['context_name'] = "Initiator"
psr_var['context_name1'] = "Responder"
psr_var['hostname_resp'] = topo.Responder['hostname']
psr_var['hostname_ini'] = topo.Initiator['hostname']
psr_var['dpd_intvl'] = "30"
psr_var['dpd_retry'] = "30"
psr_var['dpd_max'] = "2"
psr_var['session-remove-timer'] = "1200"
psr_var['psk'] = "1234567890"
psr_var['tunnel_psk'] = "abc12345"
psr_var['count'] = "5"
psr_var['local-ph1-id'] = "jameer@stoke.com"
psr_var['remote-ph1-id'] = "mkhare@stoke.com"
psr_var['tunnelSleep'] = 60
psr_var['hard_lifetime_ph1'] = '3600'
psr_var['hard_lifetime_ph2'] = '3600'
psr_var['soft_lifetime_ph1'] = '3000'
psr_var['soft_lifetime_ph2'] = '60'
psr_var[''] = ""

#Add your IP addresses here
psr_var['local_primary_ip'] = "92.1.1.2"
psr_var['local_primary_ip/mask'] = "92.1.1.2/24"
psr_var['local_secondary_ip'] = "96.1.1.2"
psr_var['local_secondary_ip/mask'] = "96.1.1.2/24"
psr_var['service_ip'] = "57.1.1.2"
psr_var['service_ip/mask'] = "57.1.1.2/24"
psr_var['cisco_local_primary_ip'] = "92.1.1.1"
psr_var['cisco_local_primary_ip/mask'] = "92.1.1.1 255.255.255.0"
psr_var['cisco_local_secondary_ip'] = "96.1.1.1"
psr_var['cisco_local_secondary_ip/mask'] = "96.1.1.1 255.255.255.0"
psr_var['linux_service_ip'] = "57.1.1.1"
psr_var['linux_service_ip/mask'] = "57.1.1.1/24"
psr_var['remote_ip/mask'] = "94.1.1.2/24"
psr_var['remote_ip'] = "94.1.1.2"
psr_var['cisco_remote_ip/mask'] = "94.1.1.1 255.255.255.0"
psr_var['cisco_remote_ip'] = "94.1.1.1"
psr_var['ini_linux_ip/mask'] = "78.1.1.2/24"
psr_var['ini_linux_ip'] = "78.1.1.2"
psr_var['linux_ini_ip/mask'] = "78.1.1.1/24"
psr_var['linux_ini_ip'] = "78.1.1.1"

psr_var['localLpbk_ip'] = "83.1.1.2"
psr_var['localLpbk_ip/mask'] = "83.1.1.2/32"
psr_var['remoteLpbk_ip'] = "85.1.1.2"
psr_var['remoteLpbk_ip/mask'] = "85.1.1.2/32"
psr_var['localTun_ip'] = "20.20.3.4"
psr_var['localTun_ip/mask'] = "20.20.3.4/32"
psr_var['remoteTun_ip/mask'] = "10.20.3.4/32"
psr_var['remoteTun_ip'] = "10.20.3.4"

#Mention your routes here
psr_var['localLpbk_route'] = "83.1.1.0/24"
psr_var['cisco_localLpbk_route'] = "83.1.1.0 255.255.255.0"
psr_var['remoteLpbk_route'] = "85.1.1.0/24"
psr_var['cisco_remoteLpbk_route'] = "85.1.1.0 255.255.255.0"
psr_var['localTrafficRoute'] = "78.1.1.1/32"
psr_var['remoteTrafficRoute'] = "57.1.1.1/32"
psr_var['lin_cisco_route'] = "57.1.1.0/24"
psr_var['ini_linux_route'] = "78.1.1.0 255.255.255.0"
psr_var['ini_linux_route1'] = "78.1.1.0/24"
psr_var['primary_trans_route'] = "92.1.1.0/24"
psr_var['secondary_trans_route'] = "96.1.1.0/24"
psr_var['service_route'] = "57.1.1.0/24"
psr_var['cisco_service_route'] = "57.1.1.0 255.255.255.0"
psr_var['remote_net'] = "94.1.1.0/24"
psr_var['cisco_ospf_service_primary'] = "57.1.1.0 0.0.0.255"
psr_var['cisco_ospf_service_secondary'] = "95.1.1.0 0.0.0.255"
psr_var['cisco_route_service_secondary'] = "95.1.1.0 255.255.255.0"
psr_var['route_remoteTun_ip'] = "10.20.3.4 255.255.255.255"
psr_var['route_localTun_ip'] = "20.20.3.4 255.255.255.255"

#Get the port details here
psr_var['linux_service_port'] = topo.p_cisco_host2[1]
psr_var['port_initator'] = topo.p_ssx2_cisco[0]
psr_var['port_cisco_ini'] = topo.p_ssx2_cisco[1]
psr_var['port_ini_linux'] = topo.p_ssx2_host1[0]
psr_var['vlan1'] = "570" # Vlan responsible for active path
psr_var['vlan2'] = "670" # Vlan responsible for standby path
psr_var['vlan3'] = "770" # Vlan used at service port
psr_var['vlan4'] = "870"
psr_var['vlan5'] = "970" # Vlan used for Initiator SSX
psr_var['Rtracker_id'] = "100"
psr_var['Rtracker_id1'] = "200"

#Linux Variables

script_var['linux_phy_iface_ip'] = '17.1.1.1'
script_var['linux_phy_iface_ip_mask'] = '17.1.1.1/24'
script_var['linux_phy_iface1_ip'] = '19.1.1.1'
script_var['linux_phy_iface1_ip_mask'] = '19.1.1.1/24'

script_var['SSX_7_13_2'] = """
context local
 interface ixia1
  arp arpa
  ip address %(ssx_phy_iface_ip_mask)s
  exit
 logging syslog %(linux_phy_iface1_ip)s 7
 interface ixia2
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 interface ntt
  arp arpa
  ip address %(ssx_phy_iface2_ip_mask)s
  exit
 exit
no port ethernet %(ssx_port_2)s
port ethernet %(ssx_port_2)s
 bind interface ixia1 local
  exit
 enable
 exit
no port ethernet %(ssx_port_3)s
port ethernet %(ssx_port_3)s
 bind interface ixia2 local
  exit
 enable
 exit
 """ %script_var
script_var['SSX_7_13_1'] = script_var['SSX_7_13_2']
script_var['SSX_7_12_1_1'] = """
context local
 interface int1
  arp arpa
  ip address 192.168.0.1/24
  exit
 exit
port ethernet %(ssx_port_2)s
 description /To_D-eBGW-R_0_g4/0/1
 bind interface int1 local
  exit
 service ipsec
 enable
 exit
""" %script_var

script_var['SSX_7_12_1_2'] = """
context local
 interface int1
  arp arpa
  no ip address 192.168.0.1/24
  ip address 172.16.0.1/24
  exit
 exit
port ethernet %(ssx_port_2)s
 description /To_D-eBGW-R_0_g4/0/1
 bind interface int1 local
  exit
 service ipsec
 enable
 exit
""" %script_var

###############################################################################################
#PSR Configuration
###############################################################################################

psr_var['IKEv2_PSR_L2L_Resp'] = """
system hostname %(hostname_resp)s
ipsec global profile
 dpd interval %(dpd_intvl)s retry-interval %(dpd_retry)s maximum-retries %(dpd_max)s
 retransmit interval 3 maximum-retries 3 send-retransmit-response
 session-remove-timer interval %(session-remove-timer)s
 exit
context %(context_name1)s
 interface local_primary
  arp arpa
  ip unreachables
  ip address %(local_primary_ip/mask)s
  exit
 interface local_secondary
  arp arpa
  ip unreachables
  ip address %(local_secondary_ip/mask)s
  exit
 interface to_service
  arp arpa
  ip unreachables
  ip address %(service_ip/mask)s
  exit
 interface tunnel_local loopback
  ip address %(localLpbk_ip/mask)s
  exit
 interface localpeer tunnel
  ip address %(localTun_ip/mask)s
  exit
 rtr %(Rtracker_id)s
  type echo protocol ipicmpecho %(cisco_local_primary_ip)s source %(local_primary_ip)s
  exit
 rtr %(Rtracker_id1)s
  type echo protocol ipicmpecho %(cisco_local_secondary_ip)s source %(local_secondary_ip)s
  exit
 rtr schedule %(Rtracker_id)s
 rtr schedule %(Rtracker_id1)s
 ip route %(remote_net)s %(cisco_local_primary_ip)s tracker %(Rtracker_id)s
 ip route %(remote_net)s %(cisco_local_secondary_ip)s admin-distance 100 tracker %(Rtracker_id1)s
 ip route %(remoteLpbk_route)s %(cisco_local_primary_ip)s tracker %(Rtracker_id)s
 ip route %(remoteLpbk_route)s %(cisco_local_secondary_ip)s admin-distance 100 tracker %(Rtracker_id1)s
 ipsec policy ikev2 phase1 name p1
  suite3
   gw-authentication psk %(psk)s
   peer-authentication psk
   hard-lifetime %(hard_lifetime_ph1)s secs
   soft-lifetime %(soft_lifetime_ph1)s secs
   exit
  exit
 ipsec policy ikev2 phase2 name p2
  suite3
   hard-lifetime %(hard_lifetime_ph2)s secs
   soft-lifetime %(soft_lifetime_ph2)s secs
   exit
  exit
 exit
!tunnel local1 type ipsec protocol ip44 context %(context_name1)s
! enable
! ip local %(localLpbk_ip)s remote %(remoteLpbk_ip)s
! bind interface localpeer %(context_name1)s
!  ip route %(remoteLpbk_ip/mask)s
!  ip route %(localTrafficRoute)s
!  exit
! ipsec policy ikev2 phase1 name p1
!  psk %(tunnel_psk)s
!  local-ph1-id %(local-ph1-id)s
!  remote-ph1-id %(remote-ph1-id)s
!  exit
! ipsec policy ikev2 phase2 name p2
! exit
"""% (psr_var)

###############################################################################################

psr_var['IKEv2_PSR_L2L_Resp_TUNNEL'] = """
tunnel local1 type ipsec protocol ip44 context %(context_name1)s
 enable
 ip local %(localLpbk_ip)s remote %(remoteLpbk_ip)s
 bind interface localpeer %(context_name1)s
  ip route %(remoteLpbk_ip/mask)s
  ip route %(localTrafficRoute)s
  exit
 ipsec policy ikev2 phase1 name p1
  psk %(tunnel_psk)s
  local-ph1-id %(local-ph1-id)s
  remote-ph1-id %(remote-ph1-id)s
  exit
 ipsec policy ikev2 phase2 name p2
 exit
"""% (psr_var)

###############################################################################################

psr_var['session_home_config'] ="""
session-home slot %s loopback interface tunnel_local Responder
 ipsec session context name Responder
 ipsec policy ikev2 phase1 name p1
 ipsec policy ikev2 phase2 name p2
 exit
"""

###############################################################################################

psr_var['port_config_vlan'] = """
port ethernet %s dot1q
 vlan %s
  bind interface local_primary Responder
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %s
  bind interface to_service Responder
   exit
 enable
 exit
port ethernet %s dot1q
 vlan %s
  bind interface local_secondary Responder
   exit
  service ipsec
  exit
 enable
exit
"""

###############################################################################################

psr_var['port_config_vlan_glcr'] = """
port ethernet %s dot1q
 vlan %s
  bind interface local_primary Responder
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %s dot1q
 vlan %s
  bind interface to_service Responder
   exit
  exit
 enable
 exit
port ethernet %s dot1q
 vlan %s
  bind interface local_secondary Responder
   exit
  service ipsec
  exit
 enable
exit
"""

###############################################################################################

psr_var['port_config_vlan_normal'] = """
port ethernet %s dot1q
 vlan %s
  bind interface local_primary Responder
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %s dot1q
 vlan %s
  bind interface to_service Responder
   exit
  exit
 enable
 exit
port ethernet %s
 bind interface local_secondary Responder
  exit
 service ipsec
 enable
exit
"""

###############################################################################################

psr_var['port_config_normal_vlan'] = """
port ethernet %s
  bind interface local_primary Responder
   exit
  service ipsec
 enable
 exit
port ethernet %s
  bind interface to_service Responder
   exit
 enable
 exit
port ethernet %s dot1q
 vlan %s
  bind interface local_secondary Responder
   exit
  service ipsec
  exit
 enable
exit
"""

###############################################################################################

psr_var['port_config_normal_normal'] = """
port ethernet %s
  bind interface local_primary Responder
   exit
  service ipsec
 enable
 exit
port ethernet %s
  bind interface to_service Responder
   exit
 enable
 exit
port ethernet %s
  bind interface local_secondary Responder
   exit
  service ipsec
 enable
exit
"""

###############################################################################################

psr_var['IKEv2_PSR_L2L_Ini'] = """
system hostname %(hostname_ini)s
ipsec global profile
 dpd interval %(dpd_intvl)s retry-interval %(dpd_retry)s maximum-retries %(dpd_max)s
 retransmit interval 3 maximum-retries 3 send-retransmit-response
 session-remove-timer interval %(session-remove-timer)s
 exit
context %(context_name)s
 interface remote_net1
  arp arpa
  ip unreachables
  ip address %(remote_ip/mask)s
  exit
 interface to_linux
  arp arpa
  ip unreachables
  ip address %(ini_linux_ip/mask)s
  exit
 interface tunnel_remote loopback
  ip unreachables
  ip address %(remoteLpbk_ip/mask)s
  exit
 interface remotepeer tunnel
  ip address %(remoteTun_ip/mask)s
  exit
 ip route %(localLpbk_route)s %(cisco_remote_ip)s
 ip route %(primary_trans_route)s %(cisco_remote_ip)s
 ip route %(secondary_trans_route)s %(cisco_remote_ip)s
 ipsec policy ikev2 phase1 name p1
  suite3
   gw-authentication psk %(psk)s
   peer-authentication psk
   hard-lifetime %(hard_lifetime_ph1)s secs
   soft-lifetime %(soft_lifetime_ph1)s secs
   exit
  exit
 ipsec policy ikev2 phase2 name p2
  suite3
   hard-lifetime %(hard_lifetime_ph2)s secs
   soft-lifetime %(soft_lifetime_ph2)s secs
   exit
  exit
 exit
session-home slot %(ini_logical_slot)s loopback interface tunnel_remote %(context_name)s
 ipsec session context name %(context_name)s
 ipsec policy ikev2 phase1 name p1
 ipsec policy ikev2 phase2 name p2
 exit
port ethernet %(port_initator)s dot1q
 vlan %(vlan5)s
  bind interface remote_net1 %(context_name)s
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %(port_ini_linux)s
 bind interface to_linux %(context_name)s
  exit
 enable
 exit
tunnel remote1 type ipsec protocol ip44 context %(context_name)s
 enable
 tunnel-setup-role initiator-responder
 ip local %(remoteLpbk_ip)s remote %(localLpbk_ip)s
 bind interface remotepeer Initiator
  ip route %(remoteTrafficRoute)s
  ip route %(localTrafficRoute)s
  exit
 ipsec policy ikev2 phase1 name p1
  psk %(tunnel_psk)s
  local-ph1-id %(remote-ph1-id)s
  remote-ph1-id %(local-ph1-id)s
  exit
 ipsec policy ikev2 phase2 name p2
 exit
"""% (psr_var)

