from topo import *
script_var={}

script_var['context_name'] = 'acl'
script_var['context1_name'] = 'aclx'
script_var['ssx_sess_iface1_ip'] = '11.11.11.2'
script_var['ssx_sess_iface1_ip_mask'] = '11.11.11.2/32'
script_var['xpress_sess_iface1_ip'] = '11.11.11.1'

script_var['ssx_phy_iface1_ip'] = '17.1.1.2'
script_var['ssx_phy_iface1_ip_mask'] = '17.1.1.2/24'
script_var['ssx_phy_iface1_ipv6_mask']="1001:1::201/64"
script_var['ssx_phy_iface1_ipv6']="1001:1::201"
script_var['xpress_phy_iface1_ipv6_mask']="1001:1::200/64"
script_var['xpress_phy_iface1_ipv6']="1001:1::200"

script_var['p1_ssx1_xpressvpn1'] = p1_ssx_linux1[0]

#xpress-vpn vars
script_var['xpress_phy_iface1_ip'] = '17.1.1.1'
script_var['xpress_phy_iface1_ip_mask'] = '17.1.1.1/24'
script_var['xpress_phy_iface1_mask']="255.255.255.0"
	
script_var['linux_phy_iface1_ip'] = '17.1.1.1'
script_var['linux_phy_iface1_ip_mask'] = '17.1.1.1/24'
script_var['linux_phy_iface1_mask']="255.255.255.0"
script_var['ssx_phy_iface2_ip'] = '17.1.1.3'
script_var['ssx_phy_iface2_ip_mask'] = '17.1.1.3/24'

#Linux 2 parameters - Jayanth
script_var['p1_ssx1_xpressvpn2'] =p1_ssx_linux2[0]

script_var['linux_phy_iface2_ip'] = '16.1.1.1'
script_var['linux_phy_iface2_ip_mask'] = '16.1.1.1/24'
script_var['linux_phy_iface2_mask']="255.255.255.0"
script_var['ssx_phy_iface3_ip'] = '16.1.1.2'
script_var['ssx_phy_iface3_ip_mask'] = '16.1.1.2/24'

prec_list= ('0','1','2','3','4','5','6','7')
tos_list=('0','1','2','3','4','5','6','7')

#Adding route for ping thru

script_var['client1_route'] = "16.1.1.0/24"
script_var['client1_gateway'] = "17.1.1.2"
script_var['client2_route'] = "17.1.1.0/24"
script_var['client2_gateway'] = "16.1.1.2"




#######################################################################################################################

script_var['ACL_CLI_001'] ="""
context %(context_name)s
interface to_linux
arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
exit
ip access-list subacl
permit tcp any any precedence 0 tos 0
deny icmp any any
permit udp any any
deny igmp any any
exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
bind interface to_linux %(context_name)s
ip access-group in name subacl
exit
service ipsec
enable
exit """ %(script_var)

script_var['ACL_CLI_002'] = """
context %(context_name)s
ipv6 access-list subacl
permit tcp any any established
deny icmp any any
deny ipv6 any any dscp 6 flow-label 6
permit udp any any flow-label 5
exit
interface to_xpressvpn ipv6
ipv6 nd address-resolve
ipv6 address %(ssx_phy_iface1_ipv6_mask)s
exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
bind interface to_xpressvpn %(context_name)s
ipv6 access-group in name subacl
exit
service ipsec
enable
exit  """ %(script_var)


script_var['ACL_FUN_056'] = """
context %(context_name)s
ipv6 access-list subacl
permit tcp any any
deny icmp any any
exit
interface to_xpressvpn ipv6
ipv6 nd address-resolve
  ipv6 address %(ssx_phy_iface1_ipv6_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ipv6 access-group in name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)


script_var['ACL_FUN_054'] ="""
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  permit tcp any any
  deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)




script_var['ACL_FUN_055'] ="""
context %(context_name)s
 interface to_linux1
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 interface to_linux2
  arp arpa
  ip address %(ssx_phy_iface3_ip_mask)s
  exit
 ip access-list subacl
  permit tcp any any
  deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn2)s
 bind interface to_linux2 %(context_name)s
  ip access-group out name subacl
  exit
 service ipsec
 enable
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux1 %(context_name)s
  exit
 service ipsec
 enable
 exit  """ %(script_var)




script_var['ACL_FUN_053'] ="""
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  permit tcp any any
  deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)


script_var['ACL_FUN_052'] = """
context %(context_name)s
ipv6 access-list subacl
exit
interface to_xpressvpn ipv6
ipv6 nd address-resolve
  ipv6 address %(ssx_phy_iface1_ipv6_mask)s
  exit
exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_xpressvpn %(context_name)s
 ipv6 access-group in name subacl
exit
 service ipsec
 enable
 exit  """ %(script_var)

script_var['ACL_FUN_023'] = """
context %(context_name)s
 interface to_linux1
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  permit ip any any
  exit
 interface to_linux2
  arp arpa
  ip address %(ssx_phy_iface3_ip_mask)s
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux1 %(context_name)s
  exit
 service ipsec
 enable
 exit
port ethernet %(p1_ssx1_xpressvpn2)s
 bind interface to_linux2 %(context_name)s
  ip access-group out name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_022'] = """
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




script_var['ACL_FUN_019'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any tos 4
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_020'] = """
context %(context_name)s
 interface to_linux1
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any tos 4
  exit
 interface to_linux2
  arp arpa
  ip address %(ssx_phy_iface3_ip_mask)s
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux1 %(context_name)s
  exit
 service ipsec
 enable
 exit
port ethernet %(p1_ssx1_xpressvpn2)s
 bind interface to_linux2 %(context_name)s
  ip access-group out name subacl
  exit
 enable
 exit """ %(script_var)



script_var['ACL_FUN_029'] = """
context %(context_name)s
 ip access-list subacl
  permit igmp any any
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

script_var['ACL_FUN_029_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no permit igmp any any
  deny igmp any any
  exit
 exit  """ %(script_var)



script_var['ACL_FUN_012'] = """
context %(context_name)s 
 interface to_linuxipv4
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 interface to_linuxipv6
  arp arpa
  ip address %(ssx_phy_iface1_ipv6_mask)s
  exit
 ip access-list subacl
  exit
 ipv6 access-list subacl
  exit
 exit """ %(script_var)





script_var['ACL_FUN_015'] = """
context %(context_name)s 
 interface to_linux1
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 interface to_linux2
  arp arpa
  ip address %(ssx_phy_iface3_ip_mask)s
  exit
 ip access-list subacl
  10 deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn2)s
 bind interface to_linux2 %(context_name)s
  ip access-group out name subacl
  exit
 service ipsec
 enable
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux1 %(context_name)s
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_015_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no deny icmp any any
  permit icmp any any
  exit
 exit """ %(script_var)



script_var['ACL_FUN_007'] = """
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

script_var['ACL_FUN_003']="""
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
script_var['ACL_FUN_002'] = """
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
 ip access-group in name subacl
exit
 service ipsec
 enable
exit  """ %(script_var)

script_var['ACL_FUN_006']="""
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
script_var['ACL_FUN_004'] = """
context %(context_name)s
ip access-list subacl
10 permit udp any any
exit
aaa profile
  session authentication local
  service authorization local
  exit
 session name ikev2
  ip address pool
  exit
ip pool 7.7.2.1 1
interface to_xpressvpn
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
interface sub session
ip session-default
ip address 44.44.44.1/24
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
script_var['ACL_FUN_009'] = """
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
script_var['ACL_FUN_005'] = """
!context local
 !interface mgm management
  !arp arpa
  !ip address 10.3.255.11/24
  !exit
 !ip route 10.3.5.0/24 10.3.255.1
 !exit
!port ethernet 0/0
!bind interface mgm local
!exit
  !enable
 !exit

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
script_var['ACL_FUN_008'] = """
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
script_var['UNKNOWN_001_OUT'] = """
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

script_var['UNKNOWN_001_IN'] = """
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

script_var['ACL_FUN_031'] = """
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

script_var['ACL_FUN_031-1'] = """
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
script_var['ACL_FUN_039'] = """
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
 session name ikev2
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
script_var['ACL_FUN_XPM_common']="""
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
test multiclient set ph1 myid          userfqdn ikev2@%(context_name)s
test multiclient set max-concurrent    1
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

script_var['ACL_FUN_042'] = """
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

script_var['ACL_FUN_047'] = """
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

script_var['ACL_FUN_001'] = """
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

script_var['ACL_FUN_017'] = """
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

script_var['ACL_FUN_021'] = """
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

script_var['ACL_FUN_014'] = """
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

script_var['ACL_FUN_033_IN'] = """
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

script_var['ACL_FUN_033_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no permit icmp any any
  
  exit
 exit
end """ %(script_var)

script_var['ACL_FUN_034_IN'] = """
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

script_var['ACL_FUN_034_MOD'] = """
context %(context_name)s
 ip access-list subacl
  no permit icmp any any
  deny icmp any any
  exit
 exit
end """ %(script_var)

script_var['FUN_031_XPM'] = """
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

script_var['ACL_FUN_010']= """
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


script_var['ACL_FUN_011'] = """
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
  deny icmp any any
  permit udp any any
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
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit
end""" %(script_var)

script_var['ACL_FUN_013'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 deny icmp any any
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)
script_var['ACL_FUN_013_IN'] = """
context %(context1_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface2_ip_mask)s
  exit
 ip access-list subacl
  10 permit icmp any any 
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 no bind interface to_linux %(context_name)s
 bind interface to_linux %(context1_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_030'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 deny icmp any any 
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_030_1'] = """
context %(context_name)s
 no ip access-list subacl
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  no ip access-group in name subacl
  exit
 exit """ %(script_var)


script_var['ACL_FUN_040'] = """
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
 exit """ %(script_var)


script_var['ACL_FUN_027'] = """
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
  ip access-group in name pubacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_026'] = """
context %(context_name)s
 session name ikev2
  ip address pool
  ip access-group in name usbacl
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
  deny icmp any any
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

script_var['ACL_FUN_041'] = """
context %(context_name)s
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  10 permit tcp any any established
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface to_linux %(context_name)s
  ip access-group in name subacl
  exit
 service ipsec
 enable
 exit """ %(script_var)

script_var['ACL_FUN_041_MOD'] = """
context %(context_name)s
 ip access-list subacl 
  10 deny tcp any any established
  exit
 exit """%(script_var)

script_var['ACL_FUN_032_IN'] = """
context %(context_name)s
 session name ikev2
  ip address pool
  exit
 ip pool 7.7.2.1 500
 interface ikev2 session loopback
  ip session-default
  ip address 4.4.4.4/32
  exit
 interface to_linux
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
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
 session name ikev2
  ip access-group in name subacl
  exit
 ip access-list subacl
  deny icmp any any
  exit """%(script_var)

script_var['ACL_FUN_009_2'] = """
context local
 exit
context %(context_name)s
 aaa profile
  user authentication local
  session accounting none
  session authentication local
  exit
 session name test-session
  ip address pool
  password encrypted 23060606005339071A
  exit
 ip pool 7.7.2.1 5
 interface untrust
  arp arpa
  ip address %(ssx_phy_iface1_ip_mask)s
  exit
 ip access-list subacl
  deny udp any any
  exit
 interface vpn session loopback
  ip session-default
  ip address 4.4.4.4/32
  exit
 ip route 0.0.0.0/0 17.1.2.1
 ipsec policy ikev2 phase1 name ph1-test1
  custom
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 40 hours
   encryption aes128
   hash sha-1
   d-h group5
   prf sha-1
   exit
  exit
 ipsec policy ikev2 phase2 name ph2-test1
  custom
   hard-lifetime 40 hours
   soft-lifetime 60 secs
   encryption triple-des
   hash md5
   pfs group2
   exit
  exit
 exit
port ethernet %(p1_ssx1_xpressvpn1)s
 bind interface untrust %(context_name)s
  ip access-group in name subacl
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
 exit """%(script_var)

script_var['ACL_XPM_009_2']="""
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
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn test-session@%(context_name)s
test multiclient set max-concurrent    2
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
test multiclient set delay 200
test multiclient configure

ike start

test multiclient connect
"""%(script_var)


script_var['ACL_FUN_058'] = """
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
  ip access-group in name subacl
  exit
 service ipsec
 enable
exit  """ %(script_var)

script_var['ACL_FUN_058_MOD'] = """
context %(context_name)s
 ip access-list subacl
  5 deny icmp any any
 exit
exit  """ %(script_var)

