from topo_sys import *

script_var = {}

#SSX Variables

script_var['context_name'] = 'acltest'
script_var['ssx_phy_iface_ip'] = '17.1.1.2'
script_var['ssx_phy_iface_ip_mask'] = '17.1.1.2/24'

#Linux Variables

script_var['linux_phy_iface_ip'] = '17.1.1.1'
script_var['linux_phy_iface_ip_mask'] = '17.1.1.1/24'

#Connectivity

script_var['linux_iface'] = p1_ssx_linux[1]
script_var['ssx_port'] = p1_ssx_linux[0]

# Feature list
featureList = ['udp' , 'tcp' , 'icmp', 'igmp']


#############################################################################
script_var['ACL_SYS_001'] = """
context %(context_name)s
 interface to_host
  ip address %(ssx_phy_iface_ip_mask)s
  arp arpa
  exit
 exit
port ethernet %(ssx_port)s
 bind interface to_host %(context_name)s
  exit
 enable
exit """ %script_var
#############################################################################


