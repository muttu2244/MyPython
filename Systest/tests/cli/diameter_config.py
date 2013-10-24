script_var= {}
script_var['aaaProfile'] = """
  end
  conf
   context dia
 domain stoke.com
 domain local.com
 aaa profile
  user authentication none
  session authentication diameter
  service authorization diameter
  exit """
script_var['ipPool'] = """
  end
  conf
   context dia
 ip pool 10.10.10.10 255 """
script_var['no_ipPool'] = """
  end
  conf
   context dia
 no ip pool 10.10.10.10 255 """

script_var['interface'] = """
  end
  conf
   context dia
 interface land_eth2
  arp arpa
  ip address 192.168.10.20/24
  exit """
script_var['no_interface'] = """
  end
  conf
   context dia
no interface land_eth2 """

script_var['sesIface'] = """
  end
  conf
   context dia
 interface dia-sess session
  ip session-default
  ip address 123.123.123.123/24
  exit """
script_var['no_sesIface'] = """
  end
  conf
   context dia
no  interface dia-sess session"""

script_var['diaAttrib'] = """
  end
  conf
   context dia
 diameter attribute nas-ip-address 192.168.10.20 """
script_var['no_diaAttrib'] = """
  end
  conf
   context dia
no  diameter attribute nas-ip-address 192.168.10.20 """

script_var['diaSesAuthProfl'] = """
  end
  conf
   context dia
 diameter session authentication profile
  max-outstanding 1024
  algorithm first
  dest-realm local.com
  exit """
script_var['no_diaSesAuthProfl'] = """
  end
  conf
   context dia
 diameter session authentication profile
no  max-outstanding 1024
no  algorithm first
no  dest-realm local.com
  exit
no diameter session authentication profile """

script_var['diaStkCfg'] = """
  end
  conf
   context dia
 diameter stack-cfg
  local-identity abc.nas.com
  local-realm nas.com
  local-ip ipv4 192.168.10.20
  peer identity ls.local.com realm local.com
   host-addr ipv4 192.168.10.1
   exit """
script_var['no_diaStkCfg'] = """
  end
  conf
   context dia
 diameter stack-cfg
no  local-identity abc.nas.com
no  local-realm nas.com
no  local-ip ipv4 192.168.10.20
  peer identity ls.local.com realm local.com
no   host-addr ipv4 192.168.10.1
no  peer identity ls.local.com realm local.com
exit
no diameter stack-cfg
   exit """

script_var['destRealm'] = """
  end
  conf
   context dia
 diameter stack-cfg
  route destination-realm local.com app-id 5 next-hop-peer-id ls.local.com
  exit """

script_var['no_destRealm'] = """
  end
  conf
   context dia
 diameter stack-cfg
no  route destination-realm local.com app-id 5 next-hop-peer-id ls.local.com
  exit
no diameter stack-cfg
 """

script_var['peerIndnty'] = """
  end
  conf
   context dia
 diameter stack-cfg
  peer identity ls.local.com realm local.com
  exit """
script_var['no_peerIndnty'] = """
  end
  conf
   context dia
 diameter stack-cfg
no  peer identity ls.local.com realm local.com
  exit
 no diameter stack-cfg
 """

script_var['diaStrpDomn'] = """
  end
  conf
   context dia
diameter strip-domain """
script_var['no_diaStrpDomn'] = """
  end
  conf
   context dia
no diameter strip-domain """
