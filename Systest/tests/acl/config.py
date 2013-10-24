from topo import *
script_var={}

script_var['context_name'] = 'acl'
script_var['ssx_sess_iface1_ip'] = '11.11.11.2'
script_var['ssx_sess_iface1_ip_mask'] = '11.11.11.2/32'
script_var['xpress_sess_iface1_ip'] = '11.11.11.1'

script_var['ssx_phy_iface1_ip'] = '17.1.1.2'
script_var['ssx_phy_iface1_ip_mask'] = '17.1.1.2/24'
script_var['ssx_phy_iface1_ipv6_mask']="1001:1::201/64"
script_var['ssx_phy_iface1_ipv6']="1001:1::201"
script_var['xpress_phy_iface1_ipv6_mask']="1001:1::200/64"
script_var['xpress_phy_iface1_ipv6']="1001:1::200"

script_var['p1_ssx1_xpressvpn1'] ="3/0"

#xpress-vpn vars
script_var['xpress_phy_iface1_ip'] = '17.1.1.1'
script_var['xpress_phy_iface1_ip_mask'] = '17.1.1.1/24'
script_var['xpress_phy_iface1_mask']="255.255.255.0"
	

#######################################################################################################################3
script_var['SAN_ACL_11-DENYIGMP'] = """
context %(context_name)s
ip access-list subacl
10 deny igmp any any
exit
interface to_xpressvpn
  arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
 exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group in name subacl
exit
 service ipsec
 enable
exit  """ %(script_var)

script_var['SAN_ACL_11-PERMITIGMP']="""
context %(context_name)s
ip access-list subacl
10 permit igmp any any
exit
interface to_xpressvpn
  arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
 exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group in name subacl
exit
 service ipsec
 enable
exit  """ %(script_var)
######################################################################################################################
script_var['SAN_ACL_11-PERMITICMP'] = """
context %(context_name)s
ip access-list subacl
10 permit icmp any any
exit
interface to_xpressvpn
  arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
 exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
 enable
exit  """ %(script_var)

script_var['SAN_ACL_11-DENYICMP']="""
context %(context_name)s
ip access-list subacl
10 deny icmp any any
exit
interface to_xpressvpn
  arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
 exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
 enable
exit  """ %(script_var)

##########################################################################################################################33
script_var['SAN_ACL_011-PERMITUDP'] = """
context %(context_name)s
ip access-list subacl
10 permit udp any any
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name user1
  ip address 11.11.11.2
  ip netmask 255.255.255.255
  password encrypted 62465C1E16452450
  exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
interface sub session
ip address 11.11.11.1/24
exit
ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3000 secs
   soft-lifetime 2000 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ph2
  suite2
   hard-lifetime 2000 secs
   soft-lifetime 1000 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
ipsec policy ikev2 phase1 name ph1
  ipsec policy ikev2 phase2 name ph2
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)
########################################################################################################3
script_var['SAN_ACL_011-DENYUDP'] = """
context %(context_name)s
ip access-list subacl
10 permit udp any any
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name user1
  ip address 11.11.11.2
  ip netmask 255.255.255.255
  password encrypted 62465C1E16452450
  exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3000 secs
   soft-lifetime 2000 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ph2
  suite2
   hard-lifetime 2000 secs
   soft-lifetime 1000 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
ipsec policy ikev2 phase1 name ph1
  ipsec policy ikev2 phase2 name ph2
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

#############################################################################################################
script_var['SAN_ACL_011-PERMITTCP'] = """
context local
 interface mgm management
  arp arpa
  ip address 10.3.255.11/24
  exit
 ip route 10.3.5.0/24 10.3.255.1
 exit
port ethernet 0/0
bind interface mgm local
exit
  enable
 exit

context %(context_name)s
ip access-list subacl
10 permit tcp any eq 21 any  
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group in name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

#####################################################################################################################
script_var['SAN_ACL_011-DENYTCP'] = """
context local
 exit
context %(context_name)s
ip access-list subacl
10 deny tcp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)


##########################################################################################
script_var['SAN_ACL_013_OUT'] = """
context local
interface mgm management
  arp arpa
  ip address 10.3.255.11/24
  exit
 ip route 10.3.5.0/24 10.3.255.1
 exit
port ethernet 0/0
bind interface mgm local
exit
  enable
 exit
context %(context_name)s
ip access-list subacl
permit icmp any any
exit 

interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

script_var['SAN_ACL_013_IN'] = """
no context %(context_name)s
context %(context_name)s
configuration 
context %(context_name)s
ip access-list subacl
deny icmp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn  %(context_name)s
 ip access-group in name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)


#########################################################################################################################################
script_var['SAN_ACL_014'] = """
context %(context_name)s
ip access-list subacl
deny icmp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s 
enable
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
  exit  """ %(script_var)

script_var['SAN_ACL_014-1'] = """
context %(context_name)s
 ip access-list subacl
no deny icmp any any
10 permit icmp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s 
enable
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
  exit  """ %(script_var)
###################################################################################################333


script_var['SAN_ACL_015'] = """
context %(context_name)s
ip access-list subacl
deny icmp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s 
enable
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
  exit  """ %(script_var)

script_var['SAN_ACL_015-1'] = """
context %(context_name)s
no ip access-list subacl
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s 
enable
 bind interface to_xpressvpn %(context_name)s
exit
 service ipsec
  exit  """ %(script_var)
################################################################################################################3

#################################################################################################################################33
script_var['SAN_ACL_016'] = """
context %(context_name)s
ip access-list subacl
10 permit udp any any
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name user1
  ip address 11.11.11.2
  ip netmask 255.255.255.255
  password encrypted 62465C1E16452450
  exit
interface sub session
ip address 11.11.11.1/24
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3000 secs
   soft-lifetime 2000 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ph2
  suite2
   hard-lifetime 2000 secs
   soft-lifetime 1000 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s 
 bind interface to_xpressvpn %(context_name)s
ipsec policy ikev2 phase1 name ph1
  ipsec policy ikev2 phase2 name ph2
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

script_var['SAN_ACL_016-1'] = """
context %(context_name)s
ip access-list subacl
no 10 permit udp any any
10 permit icmp any any
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name user1
  ip address 11.11.11.2
  ip netmask 255.255.255.255
  password encrypted 62465C1E16452450
  exit
interface sub session
ip address 11.11.11.1/24
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3000 secs
   soft-lifetime 2000 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ph2
  suite2
   hard-lifetime 2000 secs
   soft-lifetime 1000 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
ipsec policy ikev2 phase1 name ph1
  ipsec policy ikev2 phase2 name ph2
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)
#############################################################################################################################################3
script_var['SAN_ACL_017'] = """
context %(context_name)s
ip access-list subacl
10 permit udp any any
exit
class-of-service policy
outbound
class default
exit
exit
enable
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name user1
  ip address 11.11.11.2
ip netmask 255.255.255.255
class-of-service policy
  password encrypted 62465C1E16452450
  exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
interface sub session
ip address 11.11.11.1/24
exit
ipsec policy ikev2 phase1 name ph1
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3000 secs
   soft-lifetime 2000 secs
   exit
  exit
 ipsec policy ikev2 phase2 name ph2
  suite2
   hard-lifetime 2000 secs
   soft-lifetime 1000 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
ipsec policy ikev2 phase1 name ph1
  ipsec policy ikev2 phase2 name ph2
 ip access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

#####################################################################################################################3
script_var['fun_002_xpressvpn']="""
ike log            stdout off
ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_mask)s 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_iface1_ip)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            2
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn user1@%(context_name)s
test multiclient set max-concurrent    1
test multiclient set incr-ph1-life     1

test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          aes-128
test multiclient set ph2 hash          sha1
test  multiclient set ph2 dh           0
test multiclient set ph2 life          12000
test multiclient set ph2-wild
test multiclient set delay 200
test multiclient configure

ike start

test multiclient connect """ %(script_var)
############################################################################################
script_var['fun_001_xpressvpn']="""
#!/bin/sh

echo "Please enter the number of IP addresses you want to create:"
read max_count

n3=2
n4=1

i=1
while [ $n3 -le 255 ]
do
        while [ $n4 -le 255 ]
        do
                /sbin/ip addr add dev eth1 %(ssx_sess_iface1_ip_mask)s brd +
                /sbin/ip route add  %(xpress_sess_iface1_ip)s via %(ssx_phy_iface1_ip)s dev eth1 src %(ssx_sess_iface1_ip)s
                ((i += 1 ))
                if [ $i -ge $max_count ]
                then
                        exit 0
                fi
                (( n4 += 1 ))
        done
        (( n3 += 1 ))
        n4=0
done """ %(script_var)
############################################################################################

script_var['ACL_FUN_010'] = """
context %(context_name)s
ipv6 access-list subacl
10 permit ipv6 any any
exit
interface to_xpressvpn ipv6
ipv6 nd address-resolve
  ipv6 address %(ssx_phy_iface1_ipv6_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s 
 bind interface to_xpressvpn %(context_name)s
 ipv6 access-group out name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

script_var['ACL_FUN_009'] = """
context %(context_name)s
ip access-list subacl
deny icmp any any
exit
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s dot1q
enable
vlan 1576 untagged
 bind interface to_xpressvpn %(context_name)s
 ip access-group out name subacl
exit
 service ipsec
  exit  """ %(script_var)

script_var['ACL_FUN_004'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_003'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any 8 0
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_002'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any precedence 0 
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_001'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit tcp any any 
  20 deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_031_IN'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit 
end""" %(script_var)

script_var['ACL_FUN_031_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no permit icmp any any
  
  exit
 exit
end """ %(script_var)

script_var['ACL_FUN_032_IN'] = """
context %(context_name)s
 session name ikev2
  ip address pool
  ip access-group in name subacl
  exit
 ip pool 7.7.2.1 500
 interface ikev2 session loopback
  ip session-default
  ip address 4.4.4.4/32
  exit
 interface to_linux
  arp arpa
  ip address 17.1.1.2/16
  exit
 ip access-list subacl
  10 permit icmp any any
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3600 secs
   soft-lifetime 600 secs
   exit
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 3600 secs
   soft-lifetime 500 secs
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit
end""" %(script_var)

script_var['ACL_FUN_032_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no permit icmp any any
  deny icmp any any
  exit
 exit
end """ %(script_var)

script_var['FUN_032_XPM'] = """
ike log            stdout off
ike listen any  500
ipsec addr add 17.1.2.1 255.255.0.0 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           17.1.1.2 500
test multiclient set local            17.1.2.1 500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            2
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn ikev2@acl
test multiclient set max-concurrent    5
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
"""%(script_var)
