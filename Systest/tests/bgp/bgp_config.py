import topo

script_var = {}

# SSX vars
script_var['context_name'] = 'bgp1'
script_var['context_name1'] = 'bgp2'
script_var['intf_lo1_ip/mask']  = '5.5.5.1/32'
script_var['intf_lo2_ip/mask']  = '5.5.5.2/32'
script_var['intf_lo3_ip/mask']  = '5.5.5.3/32'
script_var['intf_lo1_ip']  = '5.5.5.1'
script_var['intf_lo2_ip']  = '5.5.5.2'
script_var['intf_lo3_ip']  = '5.5.5.3'
script_var['intf1_ip'] = '1.1.1.1'
script_var['intf1_ip/mask'] = '1.1.1.1/24'
script_var['intf1_ip_mask'] = '1.1.1.1 255.255.255.0'
script_var['intf2_ip'] = '1.1.1.2'
script_var['intf2_ip/mask'] = '1.1.1.2/24'
script_var['intf2_ip_mask'] = '1.1.1.2 255.255.255.0'
script_var['auto_no1'] = '100'
script_var['auto_no2'] = '200'
script_var['auto_no3'] = '101'
script_var['auto_no4'] = '201'

# Getting Port information from topo file..,

script_var['intf1_port'] = topo.p1_ssx_linux[0]
script_var['intf2_port'] = topo.p2_ssx_linux[0]
script_var['intf3_port'] = topo.p3_ssx_linux[0]
script_var['slot2port_cisco'] = topo.p1_ssx_cisco[1]
script_var['vlan1'] = "101"

#####################################################################

script_var['BGP_FUN_001'] = """
context %(context_name)s
 interface intf1
  arp arpa
  ip address %(intf1_ip/mask)s
  exit
  router-id %(intf1_ip)s
  router bgp %(auto_no1)s
   peer-group test remote-as %(auto_no2)s
    enable
    neighbor %(intf2_ip)s
    enable
    exit
   exit
  exit
 exit 
context %(context_name1)s
 interface intf2
  arp arpa
  ip address %(intf2_ip/mask)s
  exit
 router-id %(intf2_ip)s
  router bgp %(auto_no3)s
   peer-group test remote-as %(auto_no4)s
   enable
   neighbor %(intf1_ip)s
   enable
   exit
  exit
 exit
exit
port ethernet %(intf1_port)s
 bind interface intf1 %(context_name)s
  exit
 enable
 exit
port ethernet %(intf2_port)s
 bind interface intf2 %(context_name1)s
  exit
 enable
 exit """%(script_var)

#####################################################################

script_var['BGP_BASIC-DutCfg'] = """
context %(context_name)s
 interface intf1
  arp arpa
  ip address %(intf1_ip/mask)s
  exit
  router-id %(intf1_ip)s
  router bgp %(auto_no1)s
   peer-group test remote-as %(auto_no2)s
    enable
    neighbor %(intf2_ip)s
    enable
    update-source %(intf1_ip)s
    exit
   exit
  exit  """%(script_var)

#script_var['BGP_BASIC_CiscoCfg'] = """

