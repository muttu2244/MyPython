## This file contains the configuration and IP address information of the devices ##
import topo
haimc_var = {}

haimc_var['max_tuns_slot3'] = "1"
haimc_var['max_tuns_slot2'] = "1"
haimc_var['context1'] = "cont1"
haimc_var['context2'] = "cont2"
haimc_var['Ini_context_name'] = "iniPerf1"
haimc_var['Ini_context_name2'] = "iniPerf2"
haimc_var['Resp_context_name'] = "respPerf1"
haimc_var['Resp_context_name2'] = "respPerf2"
haimc_var['dpd_interval'] = "60"
haimc_var['retry_interval'] = "60"
haimc_var['dpd_maximum_retries'] = "3"
haimc_var['retransmit_interval'] = "15"
haimc_var['sess_max_retries'] = "5"
haimc_var['session_remove_timer'] = "300"
haimc_var['psk_key'] =  "1234567890"
haimc_var['phase1_soft_life'] = "7500"
haimc_var['phase1_hard_life'] = "7200"
haimc_var['phase2_soft_life'] = "3900"
haimc_var['phase2_hard_life'] = "3500"
haimc_var['vrf_name'] 	      = "card3"
haimc_var['vrf_name2']         = "card2"

haimc_var['ssx_ses_ip'] =  "11.11.11.1"
haimc_var['ssx_ses_ip/mask'] =  "11.11.11.1/24"
haimc_var['ssx_ses_ip1'] =  "12.12.12.1"
haimc_var['ssx_ses_ip1/mask'] =  "12.12.12.1/24"
haimc_var['rad_server_ip'] =  "12.2.2.2"
haimc_var['rad_server_ip/mask'] =  "12.2.2.2/24"
haimc_var['cisco_rad_server_ip'] =  "12.2.2.1"
haimc_var['cisco_rad_server_ip/mask'] =  "12.2.2.1 255.255.255.0"
haimc_var['server_port'] = '1812'
haimc_var['server_key'] =  'topsecret'
haimc_var['starting_ip_pool'] = '6.6.2.1'
haimc_var['no_of_ip_pool'] =  '1024'
haimc_var['active_slot3_ip'] = '26.1.1.1'
haimc_var['active_slot3_ip/mask'] = '26.1.1.1/24'
haimc_var['standby_4slot3_ip'] = '16.1.1.1'
haimc_var['standby_4slot3_ip/mask'] = '16.1.1.1/24'
haimc_var['cisco_active_slot3_ip'] = '26.1.1.2'
haimc_var['cisco_active_slot3_ip_mask'] = '26.1.1.2 255.255.255.0'
haimc_var['cisco_standby_4slot3_ip'] = '16.1.1.2'
haimc_var['cisco_standby_4slot3_ip_mask'] = '16.1.1.2 255.255.255.0'
haimc_var['rad_intf_4slot3_ip'] =  "13.2.2.1"
haimc_var['rad_intf_4slot3_ip/mask'] =  "13.2.2.1/24"
haimc_var['bkp_rad_intf_4slot3_ip'] =  "14.2.2.1"
haimc_var['bkp_rad_intf_4slot3_ip/mask'] =  "14.2.2.1/24"
haimc_var['cisco_rad_intf_4slot3_ip'] =  "13.2.2.2"
haimc_var['cisco_rad_intf_4slot3_ip/mask'] =  "13.2.2.2 255.255.255.0"
haimc_var['cisco_bkp_rad_intf_4slot3_ip'] =  "14.2.2.2"
haimc_var['cisco_bkp_rad_intf_4slot3_ip/mask'] =  "14.2.2.2 255.255.255.0"
haimc_var['lpbk_ip'] =  "11.11.11.11"
haimc_var['lpbk_ip/mask'] =  "11.11.11.11/32"
haimc_var['cisco_lpbk_ip/mask'] =  "11.11.11.11 255.255.255.255"
haimc_var['lpbk_ip_summary'] =  "11.11.11.0/24"
haimc_var['lpbk_ip1'] =  "22.22.22.22"
haimc_var['lpbk_ip1/mask'] =  "22.22.22.22/32"
haimc_var['cisco_lpbk_ip1/mask'] =  "22.22.22.22 255.255.255.255"
haimc_var['active_slot2_ip'] = '26.2.2.1'
haimc_var['active_slot2_ip/mask'] = '26.2.2.1/24'
haimc_var['standby_4slot2_ip'] = '16.2.2.1'
haimc_var['standby_4slot2_ip/mask'] = '16.2.2.1/24'
haimc_var['cisco_active_slot2_ip'] = '26.2.2.2'
haimc_var['cisco_active_slot2_ip_mask'] = '26.2.2.2 255.255.255.0'
haimc_var['cisco_standby_4slot2_ip'] = '16.2.2.2'
haimc_var['cisco_standby_4slot2_ip_mask'] = '16.2.2.2 255.255.255.0'
haimc_var['rad_intf_4slot2_ip'] =  "13.3.3.1"
haimc_var['rad_intf_4slot2_ip/mask'] =  "13.3.3.1/24"
haimc_var['bkp_rad_intf_4slot2_ip'] =  "14.3.3.1"
haimc_var['bkp_rad_intf_4slot2_ip/mask'] =  "14.3.3.1/24"
haimc_var['cisco_rad_intf_4slot2_ip'] =  "13.3.3.2"
haimc_var['cisco_rad_intf_4slot2_ip/mask'] =  "13.3.3.2 255.255.255.0"
haimc_var['cisco_bkp_rad_intf_4slot2_ip'] =  "14.3.3.2"
haimc_var['cisco_bkp_rad_intf_4slot2_ip/mask'] =  "14.3.3.2 255.255.255.0"
#haimc_var['tunnel_intf_slot2_startIp'] = "155.1.1.1"
#haimc_var['tunnel_intf_slot3_startIp'] = "156.1.1.1"
haimc_var['cisco_ixia_slot2_ip/mask'] = "10.10.50.51 255.255.255.0"
haimc_var['cisco_ixia_slot2_ip'] = "10.10.50.51"
haimc_var['cisco_ixia_slot3_ip/mask'] = "10.10.60.61 255.255.255.0"
haimc_var['cisco_ixia_slot3_ip'] = "10.10.60.61"
haimc_var['ixia_cisco_slot2_ip/mask'] = "10.10.50.50 255.255.255.0"
haimc_var['ixia_cisco_slot2_ip'] = "10.10.50.50"
haimc_var['ixia_cisco_slot3_ip/mask'] = "10.10.60.60 255.255.255.0"
haimc_var['ixia_cisco_slot3_ip'] = "10.10.60.60"

#Tracker Id Configuration
#------- On SSX
haimc_var['track3'] = "120"
haimc_var['track1'] = "110"
#------- On CISCO
haimc_var['Rtracker_id'] = "10"
haimc_var['Rtracker_id1'] = "20"

# Vlan Information
haimc_var['vlan4slot2'] 	= "520"
haimc_var['standby_vlan4slot2'] = "540"
haimc_var['service_vlan4slot2'] = "531"
haimc_var['serback_vlan4slot2'] = "542"
haimc_var['vlan4slot3'] 	= "530"
haimc_var['standby_vlan4slot3'] = "541"
haimc_var['service_vlan4slot3'] = "521"
haimc_var['serback_vlan4slot3'] = "543"
haimc_var['ini_vlan4slot2'] 	= "620"
haimc_var['ini_vlan4slot3'] 	= "630"
haimc_var['rtr_id1'] = "55"
haimc_var['rtr_id2'] = "66"
haimc_var['ospf_process_id'] = "143"
haimc_var['ospf_process_id1'] = "133"
haimc_var['cisco_ospf_net_transport'] = '26.2.2.0 0.0.0.255'
haimc_var['cisco_ospf_net_service'] = '13.3.3.0 0.0.0.255'

#Mention your routes here.
haimc_var['route_to_cisco_active_rad'] =  "13.2.2.0/24"
haimc_var['route_to_cisco_standby_rad'] =  "14.2.2.0/24"
haimc_var['route_to_cisco_active_rad_slot2'] =  "13.3.3.0/24"
haimc_var['route_to_cisco_standby_rad_slot2'] =  "14.3.3.0/24"
haimc_var['route_to_host_ns'] = "192.168.1.0/24"
haimc_var['route_to_ns_phy_ip'] =  '20.1.1.0/24'
haimc_var['route_ip_pool'] = '6.6.0.0/16'
haimc_var['route_to_rad_srvr'] =  "12.2.2.0/24"
haimc_var['default_route'] = '0.0.0.0/0'
haimc_var['active_route_4slot3'] = '26.1.1.0/24'
haimc_var['standby_route_4slot3'] = '16.1.1.0/24'
haimc_var['active_route_4slot2'] = '26.2.2.0/24'
haimc_var['standby_route_4slot2'] = '16.2.2.0/24'
haimc_var['dummy_intf_routes_slot2'] = "45.0.0.0 255.0.0.0"
haimc_var['dummy_intf_routes_slot3'] = "46.0.0.0 255.0.0.0"
haimc_var['tunnel_intf_routes_slot2'] = "55.0.0.0 255.0.0.0"
haimc_var['tunnel_intf_routes_slot3'] = "56.0.0.0 255.0.0.0"
haimc_var['resp_tunnel_intf_routes_slot2'] = "55.0.0.0 255.0.0.0"
haimc_var['resp_tunnel_intf_routes_slot3'] = "56.0.0.0 255.0.0.0"
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""

#============ Parameters related to Test Cases
#------------- HA-IP-22
haimc_var['num_clear_tun_cmds'] = 100
#------------- HA-STRESS-05
haimc_var['num_of_iter'] = 2
#----------- HA-STRESS-07
haimc_var['maxIterations'] = 2
#----------- HA-FUN-04
haimc_var['kill_imc_resta_process'] = "Evt Evl EvlColl IkedMc Inets CDR Ntp "
haimc_var['kill_glc_resta_process'] = "Evt Evl"
haimc_var['kill_glc_non_rest_process'] = "Iked Fpd NSM Count IpLc DHCPdLC Inspectd"

#----------- HA-IP-23
haimc_var['kill_imc_non_rest_process'] = "NSM Smid Ip CtxtMgr Fpd Aaad Cli Logind Ospf Bgp Rip TunMgr DHCPdMC Dfn"

#----------- HA_STRESS_007
haimc_var['tun_slot2_ha_ip_23'] = 2047
haimc_var['tun_slot3_ha_ip_23'] = 2047

#Port information from topo. 
haimc_var['port_ssx_rad_intf_4slot3'] = topo.p_to_rad_active_ssx_cisco_slot3[0]
haimc_var['port_cisco_rad_intf_4slot3'] = topo.p_to_rad_active_ssx_cisco_slot3[1]
haimc_var['port_ssx_bkp_rad_intf_4slot3'] =  topo.p_to_rad_standby_ssx_cisco_slot3[0]
haimc_var['port_cisco_bkp_rad_intf_4slot3'] =  topo.p_to_rad_standby_ssx_cisco_slot3[1]
haimc_var['port_ssx_active_4slot3'] = topo.p_active_ssx_cisco_slot3[0]
haimc_var['port_cisco_active_4slot3'] = topo.p_active_ssx_cisco_slot3[1]
haimc_var['port_ssx_standby_4slot3'] = topo.p_standby_ssx_cisco_slot3[0]
haimc_var['port_cisco_standby_4slot3'] = topo.p_standby_ssx_cisco_slot3[1]
haimc_var['port_cisco_rad_srvr'] =  topo.p_cisco_rad[0]
haimc_var['intf_rad_srvr'] = topo.p_cisco_rad[1]
haimc_var['port_ssx_rad_intf_4slot2'] = topo.p_to_rad_active_ssx_cisco_slot2[0]
haimc_var['port_cisco_rad_intf_4slot2'] = topo.p_to_rad_active_ssx_cisco_slot2[1]
haimc_var['port_ssx_bkp_rad_intf_4slot2'] =  topo.p_to_rad_standby_ssx_cisco_slot2[0]
haimc_var['port_cisco_bkp_rad_intf_4slot2'] =  topo.p_to_rad_standby_ssx_cisco_slot2[1]
haimc_var['port_ssx_active_4slot2'] = topo.p_active_ssx_cisco_slot2[0]
haimc_var['port_cisco_active_4slot2'] = topo.p_active_ssx_cisco_slot2[1]
haimc_var['port_ssx_standby_4slot2'] = topo.p_standby_ssx_cisco_slot2[0]
haimc_var['port_cisco_standby_4slot2'] = topo.p_standby_ssx_cisco_slot2[1]

# IP Addresses related to Initiator
slot2_id = int(topo.p_ini_cisco_slot2[0].split("/")[0])
slot2_port = int(topo.p_ini_cisco_slot2[0].split("/")[1])
slot3_id = int(topo.p_ini_cisco_slot3[0].split("/")[0])
slot3_port = int(topo.p_ini_cisco_slot3[0].split("/")[1])
haimc_var['ini_cisco_slot2_ip'] = "15.%s.%s.1"%(slot2_id,slot2_port+1)
haimc_var['ini_cisco_slot2_ip/mask'] = "15.%s.%s.1/28"%(slot2_id,slot2_port+1)
haimc_var['ini_cisco_slot3_ip'] = "15.%s.%s.1"%(slot3_id,slot3_port+1)
haimc_var['ini_cisco_slot3_ip/mask'] = "15.%s.%s.1/28"%(slot3_id,slot3_port+1)
haimc_var['cisco_ini_slot2_ip'] = "15.%s.%s.5"%(slot2_id,slot2_port+1)
haimc_var['cisco_ini_slot2_ip/mask'] = "15.%s.%s.5 255.255.255.240"%(slot2_id,slot2_port+1)
haimc_var['cisco_ini_slot3_ip'] = "15.%s.%s.5"%(slot3_id,slot3_port+1)
haimc_var['cisco_ini_slot3_ip/mask'] = "15.%s.%s.5 255.255.255.240"%(slot3_id,slot3_port+1)
haimc_var['ini_ixia_ip'] = "81.0.0.2"
haimc_var['ini_ixia_ip/mask'] = "81.0.0.2/16"
haimc_var['ixia_ini_ip'] = "81.0.0.1"
haimc_var['ixia_ini_ip/mask'] = "81.0.0.1/16"
haimc_var['ini_slot3_ixia_ip'] = "82.0.0.2"
haimc_var['ini_slot3_ixia_ip/mask'] = "82.0.0.2/16"
haimc_var['ixia_ini_slot3_ip'] = "82.0.0.1"
haimc_var['ixia_ini_slot3_ip/mask'] = "82.0.0.1/16"
haimc_var['dummy_intf_slot2_startIp'] = "45.1.1.1"
haimc_var['dummy_intf_slot3_startIp'] = "46.1.1.1"
haimc_var['tunnel_intf_slot2_startIp'] = "55.1.1.1"
haimc_var['tunnel_intf_slot3_startIp'] = "56.1.1.1"
haimc_var['cisco_ixia_ip'] = "83.0.0.2"
haimc_var['cisco_ixia_ip/mask'] = "83.0.0.2 255.255.0.0"
haimc_var['ixia_cisco_ip'] = "83.0.0.1"
haimc_var['ixia_cisco_ip/mask'] = "83.0.0.1/16"
haimc_var['cisco_slot3_ixia_ip'] = "84.0.0.2"
haimc_var['cisco_slot3_ixia_ip/mask'] = "84.0.0.2 255.255.0.0"
haimc_var['ixia_cisco_slot3_ip'] = "84.0.0.1"
haimc_var['ixia_cisco_slot3_ip/mask'] = "84.0.0.1/16"

# Routes related Initiator
haimc_var['route_ini_slot2_ixia'] = "10.222.0.0/16"
haimc_var['slot2_route_startIp'] = "10.222.0.0"
haimc_var['slot3_route_startIp'] = "10.110.0.0"
haimc_var['ini_slot2_route_startIp'] = "30.222.0.0"
haimc_var['ini_slot3_route_startIp'] = "30.110.0.0"
haimc_var['route_ini_slot3_ixia'] = "10.110.0.0/16"
haimc_var['cisco_route_ini_slot2_ixia'] = "10.222.0.0 255.255.0.0"
haimc_var['cisco_route_ini_slot3_ixia'] = "10.110.0.0 255.255.0.0"
haimc_var['route_to_ini_ses'] = "2.2.0.0/16"
haimc_var['cisco_route_to_ini_ses'] = "2.2.0.0 255.255.0.0"
haimc_var['route_ini_slot3'] = "3.2.0.0/16"
haimc_var['cisco_route_ini_slot3'] = "3.2.0.0 255.255.0.0"
haimc_var['routes_to_ini_ip_slot2'] = "15.%s.%s.0/28"%(slot2_id,slot2_port+1)
haimc_var['routes_to_ini_ip_slot3'] = "15.%s.%s.0/28"%(slot3_id,slot3_port+1)
haimc_var['route_to_ini_ip'] = "15.%s.%s.1/32"%(slot2_id,slot2_port+1)
haimc_var['route_to_ini_slot3_ip'] = "15.%s.%s.1/32"%(slot3_id,slot3_port+1)
haimc_var['route_to_cisco_ini_ip'] = "15.%s.%s.5/32"%(slot2_id,slot2_port+1)
haimc_var['ssx_ses_traffic_route'] = "30.110.0.0/16"
haimc_var['cisco_ssx_ses_traffic_route'] = "30.110.0.0 255.255.0.0"
haimc_var['cisco_ssx_slot3_ses_traffic_route'] = "30.222.0.0 255.255.0.0"

# Port information for Initiator
haimc_var['port_ini_slot2'] = topo.p_ini_cisco_slot2[0]
haimc_var['port_cisco_ini_slot2'] = topo.p_ini_cisco_slot2[1]
haimc_var['port_ini_slot3'] = topo.p_ini_cisco_slot3[0]
haimc_var['port_cisco_ini_slot3'] = topo.p_ini_cisco_slot3[1]
haimc_var['port_ini_ixia_slot2'] = topo.p_ini_ixia[0]
haimc_var['port_ixia_ini_slot2'] = topo.p_ini_ixia[1]
haimc_var['port_ini_ixia_slot3'] = topo.p_ini_slot3_ixia[0]
haimc_var['port_ixia_ini_slot3'] = topo.p_ini_slot3_ixia[1]
haimc_var['port1_cisco_ixia'] = topo.p1_cisco_ixia[0]
haimc_var['port1_ixia_cisco'] = topo.p1_cisco_ixia[1]
haimc_var['port2_cisco_ixia'] = topo.p2_cisco_ixia[0]
haimc_var['port2_ixia_cisco'] = topo.p2_cisco_ixia[1]

###########################################################################################
#Configuration varaibles								  #
###########################################################################################
haimc_var['Ini_traffic_config'] = """
context %(Ini_context_name)s
interface ixiaCard2
arp arpa
ip address %(ini_ixia_ip/mask)s
exit
ip route %(route_ini_slot2_ixia)s %(ixia_ini_ip)s
exit
port ethernet %(port_ini_ixia_slot2)s
bind interface ixiaCard2  %(Ini_context_name)s
exit
enable
exit
context %(Ini_context_name2)s
interface ixiaCard3
arp arpa
ip address %(ini_slot3_ixia_ip/mask)s
exit
ip route %(route_ini_slot3_ixia)s %(ixia_ini_slot3_ip)s
exit
port ethernet %(port_ini_ixia_slot3)s
bind interface ixiaCard3  %(Ini_context_name2)s
exit
enable
exit""" %(haimc_var)

###########################################################################################

haimc_var['IP_SLA_CONFIG'] = """
no ipsec global profile
context %(Resp_context_name)s
rtr %(rtr_id1)s
type echo protocol ipicmpecho %(cisco_active_slot2_ip)s source %(active_slot2_ip)s
exit
rtr %(rtr_id2)s
type echo protocol ipicmpecho %(cisco_rad_intf_4slot2_ip)s source %(rad_intf_4slot2_ip)s
exit
rtr schedule %(rtr_id1)s 
rtr schedule %(rtr_id2)s
ip route %(routes_to_ini_ip_slot2)s %(cisco_active_slot2_ip)s tracker %(rtr_id1)s
ip route %(routes_to_ini_ip_slot2)s %(cisco_standby_4slot2_ip)s admin-distance 200
ip route %(cisco_ssx_slot3_ses_traffic_route)s %(cisco_rad_intf_4slot2_ip)s tracker %(rtr_id2)s
ip route %(cisco_ssx_slot3_ses_traffic_route)s %(cisco_bkp_rad_intf_4slot2_ip)s admin-distance 200
ip route %(dummy_intf_routes_slot2)s %(cisco_active_slot2_ip)s tracker %(rtr_id1)s
ip route %(dummy_intf_routes_slot2)s %(cisco_standby_4slot2_ip)s admin-distance 200
end"""%(haimc_var)

###########################################################################################

haimc_var['OSPF_CONFIG'] = """
context %(Resp_context_name)s
router-id %(lpbk_ip)s
 router ospf
  redistribute subscriber-host
  redistribute connected
  summary-address %(dummy_intf_routes_slot2)s
  summary-address %(lpbk_ip_summary)s
  summary-address %(tunnel_intf_routes_slot2)s
  summary-address %(route_ini_slot2_ixia)s
  area 0
   interface transport
    dead-interval minimal hello-multiplier 4
    mtu-ignore
    exit
   interface service
    dead-interval minimal hello-multiplier 4
    mtu-ignore
    exit
   exit
  neighbor %(cisco_active_slot2_ip)s
  neighbor %(cisco_rad_intf_4slot2_ip)s
  exit
ip route %(routes_to_ini_ip_slot2)s %(cisco_standby_4slot2_ip)s admin-distance 200
ip route %(cisco_ssx_slot3_ses_traffic_route)s %(cisco_bkp_rad_intf_4slot2_ip)s admin-distance 200
ip route %(dummy_intf_routes_slot2)s %(cisco_standby_4slot2_ip)s admin-distance 200
""" %(haimc_var)

###########################################################################################

haimc_var['Ini_traffic_config_slot2'] = """
no ipsec global profile
context %(Ini_context_name)s
interface ixiaCard2
arp arpa
ip address %(ini_ixia_ip/mask)s
exit
ip route %(route_ini_slot2_ixia)s %(ixia_ini_ip)s
exit
port ethernet %(port_ini_ixia_slot2)s
bind interface ixiaCard2  %(Ini_context_name)s
exit
enable
exit""" %(haimc_var)

###########################################################################################


haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
haimc_var[''] = ""
