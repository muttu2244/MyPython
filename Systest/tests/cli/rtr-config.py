
script_var={}


script_var['interface']="""
end
conf
cont local
interface server1
  arp arpa
  ip unreachables
  ip address 20.1.1.2/24
  exit
 interface server2
  arp arpa
  ip unreachables
  ip address 40.1.1.2/24
  exit
end
"""

script_var['rtr'] = """
end
conf
cont local
 rtr 3
  type echo protocol ipicmpecho 20.1.1.1 source 20.1.1.2
  exit
end
"""
script_var['sched'] = """
end
conf
cont local
 rtr schedule 3
 ip route 45.1.1.0/24 20.1.1.1 tracker 3
 exit
end
"""
script_var['port'] = """
end
conf
port ethernet 2/2
bind interface server1 local
exit
enable
exit
end
"""

