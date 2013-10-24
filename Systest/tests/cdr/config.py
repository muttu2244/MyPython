import topo

#SSX variables used in SNMP configuration:
#******************************************
### upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e ###

script_var = {}

script_var['context_name']="cdr-1" 

#Contexts for establishing Mutliple IKEV2(ikev6 & ikev8)sessions with 2 different CDR context's(cdr-1 & cdr-2):
#*****************************************************************************************************************************
script_var['context_name1']="cdr-1"
script_var['context_name2']="cdr-2"


script_var['upload_profile1']="customer"
script_var['upload_profile2']="backup"
script_var['upload_profile3']="stoke_log"
script_var['upload_profile4']="temp"

script_var['xpress_phy_iface2_ip_mask'] = "15.1.1.1/24"
script_var['xpress_phy_iface1_ip_mask'] = "17.1.1.1/16"
script_var['ssx_phy_ip1_xvpn_mask']=  '17.1.1.2/16'
script_var['xpress_phy_iface1_ip'] = '17.1.2.1'
script_var['vgroup_phy_iface1_ip'] = '17.1.1.1'

script_var['upload_server_ip1'] = "17.1.2.1"
script_var['upload_server_ip2'] = "15.1.2.1"

#script_var['upload_server_mgmt_ip']   =	"10.3.5.11"
#script_var['upload_server_mgmt_mask'] = "10.3.5.11/24"
script_var['upload_server_mgmt_ip'] = "10.3.2.22"
script_var['upload_server_mgmt_mask'] = "10.3.2.22/24"

#script_var['SSX_mgmt_ip_mask']   = "10.3.255.30/24"
script_var['SSX_mgmt_ip_mask']   = "10.4.2.23/24"

#script_var['SSX_route_ip']   = "10.3.255.1"
script_var['SSX_route_ip']   = "10.4.2.1"

script_var['ssx_port1']=topo.p1_ssx_xpressvpn1[0]
script_var['ssx_port2']=topo.p1_ssx_xpressvpn2[0]
script_var['ssx_port3']=topo.p1_ssx_xpressvpn3[0]


script_var['ssx_port1_multi']=topo.p1_ssx_xpressvpn1_multi[0]
script_var['ssx_port2_multi']=topo.p1_ssx_xpressvpn2_multi[0]

script_var['pool_ip']='7.7.2.1'
script_var['pool_ip2']='9.9.2.1'

script_var['ses_loopip']='4.4.4.4'
script_var['ses_loopip2']='4.4.4.5'

script_var['ses_loopip_mask']='4.4.4.4/32'
script_var['ses_loopip2_mask']='4.4.4.5/32'


###############################################################################
# Radius Variables:

script_var['radius1_ip'] = '69.0.0.1'
script_var['ssx_radius1_ip'] = '69.0.0.21'
script_var['radius2_ip'] = '13.0.0.1'
script_var['ssx_radius2_ip'] = '13.0.0.21'

script_var['radius1_ip_mask']=                  '69.0.0.1/24'           #Huahine
script_var['radius2_ip_mask']=                  '13.0.0.1/24'           #qa-svr3


###############################################################################


#script_var['ssx_port1_mgmt']=topo.p1_ssx_xpressvpn1[0]
script_var['ssx_port1_mgmt']="0/0"

script_var['incorrect_ip']="18.1.2.1"

# For VGroup
script_var['vgroup_ssx']="""
no context %(context_name)s
context %(context_name)s
 interface xpress_vpn 
  arp arpa
  ip address %(ssx_phy_ip1_xvpn_mask)s
  exit
  ip route 17.1.0.0/16 %(xpress_phy_iface1_ip)s
exit
port ethernet %(ssx_port1)s
 enable
 bind interface xpress_vpn %(context_name)s
 exit
exit """ %script_var

#########################################################################################
script_var['add_ip_takama'] = """

max_count=5

n3=2
n4=1

i=1
while [ $n3 -le 255 ]
do
        while [ $n4 -le 255 ]
        do
                /sbin/ip addr add dev eth1 7.7.$n3.$n4/16 brd +
                /sbin/ip route add 4.4.4.4 via 17.1.1.2 dev eth1 src 7.7.$n3.$n4
                /sbin/ifconfig eth1:$i 17.1.$n3.$n4 netmask 255.255.0.0
                ((i += 1 ))
                if [ $i -ge $max_count ]
                then
                        exit 0
                fi
                (( n4 += 1 ))
        done
        (( n3 += 1 ))
        n4=0
done """ % script_var

script_var['cdr_common_config']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format ttlv
   upload-server 17.1.2.1 protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
######################################################################

script_var['CDR_FUN_026']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
######################################################################



script_var['CDR_FUN_020']= """
context %(context_name)s
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
no cdr
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   include 0-6
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   include 0-6
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   include 0-6
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
 exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
 exit """ %script_var
########################################################################
script_var['CDR_FUN_030']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet  %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var

###################################################################################
script_var['CDR_FUN_031']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet  %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var

###################################################################################


########################################################################
script_var['CDR_FUN_032']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
!   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format ttlv
!   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
!   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet  %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var

###################################################################################


script_var['CDR_FUN_033']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
  file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet  %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
!  exit
!port ethernet 0/0
! bind interface mgm %(context_name)s
!  exit
! enable
 exit """ %script_var
   

script_var['CDR_FUN_033A']="""
context  %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 2
  file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
 exit """ %script_var

#########################################################################
script_var['CDR_FUN_002']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
 ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   !upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var

###################################################################################


script_var['CDR_FUN_002A']= """
conf
context %(context_name)s
cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format ttlv
   !upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol tftp 
   exit
  exit
 exit
exit """ % script_var
###################################################################################


###################################################################################


script_var['CDR_FUN_002B']= """
conf
context %(context_name)s
no cdr
exit
exit
exit """ % script_var
###################################################################################

script_var['CDR_FUN_002C']= """
conf
context %(context_name)s
cdr
  disk-commit-interval 1440
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
exit
exit
exit """ % script_var
###################################################################################


script_var['CDR_FUN_002D']= """
conf
context %(context_name)s
 no event volume 1000_bytes 1000 action generate-cdr repeat
 event volume 1GB_bytes 1000000000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1GB_bytes
  exit
 no class-of-service icmp_policy
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1GB_bytes
    exit
   exit
  enable
  exit
cdr
  disk-commit-interval 120
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
exit
exit
exit """ % script_var
###################################################################################


script_var['CDR_FUN_005']= """
conf
context %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format ttlv
   !upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   upload-server %(upload_server_ip1)s protocol tftp 
   exit
  exit
exit """ % script_var
###################################################################################

script_var['CDR_FUN_006']= """
conf
context %(context_name)s
 cdr
  upload-profile %(upload_profile1)s
   interval 2
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 2
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
exit """ % script_var

###################################################################################


script_var['CDR_FUN_007A']= """
conf
context %(context_name)s
 cdr
  upload-profile %(upload_profile1)s
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
exit """ % script_var
###################################################################################



script_var['CDR_FUN_007']= """
conf
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool 7.7.2.1 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
  filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address 4.4.4.4/32
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 interface mgmt management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 3600 secs
   soft-lifetime 500 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3600 secs
   soft-lifetime 600 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   10 class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  upload-profile %(upload_profile1)s 
   interval 2
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgmt cdr-1
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans cdr-1
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
exit """ % script_var
###################################################################################



script_var['CDR_FUN_036']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################



script_var['CDR_FUN_037']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################
script_var['CDR_FUN_012']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
   exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa 
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 3600 secs
   soft-lifetime 500 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 3600 secs
   soft-lifetime 600 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 3
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 3
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 3
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################


script_var['CDR_FUN_015']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa 
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  upload-profile %(upload_profile1)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################

script_var['CDR_FUN_013']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
   exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
 exit
exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################


script_var['CDR_FUN_016']= """
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 390 secs
   soft-lifetime 80 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 390 secs
   soft-lifetime 70 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 8
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################


script_var['CDR_FUN_018']= """
context %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server 10.3.5.57 protocol tftp
   exit
  exit
exit """ % script_var
###################################################################################



script_var['CDR_FUN_038']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
  exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   include 4
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
 !upload-profile %(upload_profile2)s
 ! interval 1
 ! file-format ttlv
 ! upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
 ! exit
!  upload-profile %(upload_profile3)s
!   interval 1
!   file-format xml
!   upload-server %(upload_server_ip1)s protocol tftp
!   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
######################################################################
script_var['CDR_FUN_039']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting radius
  session authentication local
  service authorization local
  exit
 event time 120_seconds 40 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  event time 120_seconds
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface linux1
  arp arpa
  ip address 69.0.0.21/24
  exit
 radius session accounting profile
  server 69.0.0.1 port 1813 key topsecret
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   include 0 4 5
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
 !upload-profile %(upload_profile2)s
 ! interval 1
 ! file-format ttlv
 ! upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
 ! exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit
port ethernet %(ssx_port2)s
 bind interface linux1 %(context_name)s
  exit
 enable
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit """ %script_var
######################################################################
 
script_var['CDR_FUN_040']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event time 120_seconds 120 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface mgm management
  arp arpa
  ip address %(SSX_mgmt_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(SSX_route_ip)s
 interface linux1
  arp arpa
ip address 5.1.1.1/24
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   include 4-6
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
 upload-profile %(upload_profile2)s
  interval 1
  file-format ttlv
  upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
  exit
  upload-profile %(upload_profile3)s
   include 0-6
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet 0/0
 bind interface mgm %(context_name)s
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
######################################################################

script_var['CDR_FUN_041']="""
conf
context %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   include 0-6
   exit
 exit """ %script_var


######################################################################


script_var['CDR_FUN_042']="""
conf
context %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   include 0
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   include 3
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile3)s
   include 4
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit """ %script_var


######################################################################

script_var['CDR_FUN_059']="""
conf
context cdrdup
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event time 120_seconds 120 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
 ip address 5.1.1.1/24
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
 interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol ftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################
##############################################################################################
script_var['CDR_NEG_003']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
  event time 120_seconds 120 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
 ip address 5.1.1.1/24
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
  interval 1
   file-format ttlv
   upload-server %(incorrect_ip)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(incorrect_ip)s protocol sftp username krao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(incorrect_ip)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################




script_var['CDR_NEG_004']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
  event time 120_seconds 120 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
 ip address 5.1.1.1/24
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol ftp username incorrectkrao password 1q2w3e
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username incorrectkrao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################
script_var['CDR_NEG_005']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
  event time 120_seconds 120 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
 ip address 5.1.1.1/24
  exit
  interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
 exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format asn
   upload-server %(upload_server_ip1)s protocol ftp username krao password incorrectpwd
   exit
  upload-profile %(upload_profile3)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password incorrectpwd
   exit
  exit
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var
##############################################################################################


script_var['CDR_MISC_001']="""

context local
 exit
context %(context_name)s
 aaa profile
  user authentication local
  session accounting radius
  session authentication radius
  max-session 5
  exit
 event time 120_seconds 40 action generate-cdr
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev2
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  event time 120_seconds
  exit
 radius session authentication profile
  server 69.0.0.1 port 1812 key topsecret
  exit
 radius session accounting profile
  server 69.0.0.1 port 1813 key topsecret
  exit
 ip pool 7.7.2.1 20
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
  filter-rule 10 icmp_protcol
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface rad1
  arp arpa
  ip address 69.0.0.21/24
  exit
 interface sub session loopback
  ip session-default
  ip address 4.4.4.4/32
  exit
 ipsec policy ikev2 phase1 name p11
  custom
   gw-authentication psk 12345
   peer-authentication eap
   hard-lifetime 40 hours
   encryption aes128
   hash sha-1
   d-h group5
   prf sha-1
   exit
  exit
 ipsec policy ikev2 phase2 name p12
  custom
   hard-lifetime 40 hours
   soft-lifetime 600 secs
   encryption triple-des
   hash md5
   pfs group2
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   10 class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 radius dynamic-authorization profile
  server %(radius1_ip)s  key topsecret
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   include 0 4 5
   exit
  upload-profile %(upload_profile2)s
   interval 1
   file-format xml
   upload-server %(upload_server_ip1)s protocol sftp username krao password 1q2w3e
   exit
  exit
 exit
port ethernet %(ssx_port2)s
 bind interface rad1 %(context_name)s
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var




script_var['SC_EA_004']="""
no context %(context_name)s
context %(context_name)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
event volume 1000_bytes 1000 action generate-cdr
event time 2_secs 2 action generate-cdr
 session name ikev2
  ip address pool

event volume 1000_bytes
  event time 2_secs
  exit
 ip pool %(pool_ip)s 500
 interface ikev2 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans
  arp arpa
  ip address 17.1.1.2/16 
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
 hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
   file-format ttlv
   upload-server %(upload_server_ip1)s protocol tftp
   exit
exit
exit
port ethernet %(ssx_port1)s
 bind interface local_trans %(context_name)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var



script_var['cdr_cli_001'] = """
context %(context_name)s
cdr""" %script_var

#the list of commands are used in testcase aaa_cli_001
script_var['list_of_commands1']="""
debug                 Debug logging
disk-commit-interval  Set cdr TTLV disk-commit timer interval
end                   Exit configuration mode
exit                  Exit current configuration mode
no                    Remove setting or configuration
show                  Display system information
upload-profile        Create cdr server for files uploading
"""

#####################################################################


script_var['cdr_cli_002'] = """
context %(context_name)s
 cdr
  disk-commit-interval 1
  upload-profile customer
   interval 1
   file-format xml
   upload-server 17.1.2.1 protocol tftp
   exit
  exit
 exit
""" % script_var

#the list of commands are used in testcase aaa_cli_003
script_var['list_of_commands2']="""
context cdr-1
 cdr
  disk-commit-interval 1
  upload-profile customer
   interval 1
   file-format xml
   upload-server 17.1.2.1 protocol tftp
   exit
  exit
 exit
"""

#####################################################################

script_var['cdr_cli_003'] = """
context %(context_name)s
cdr
upload-profile %(upload_profile3)s
""" % script_var

#the list of commands are used in testcase aaa_cli_003
script_var['list_of_commands3']="""
debug          Debug logging
end            Exit configuration mode
exit           Exit current configuration mode
file-format    Upload file format
include        Configure CDR record IDs to include for this profile
interval       Set cdr file upload interval
no             Remove setting or configuration
show           Display system information
upload-server  Configure upload file server
"""

#####################################################################

script_var['cdr_cli_004'] = """
context %(context_name)s
no cdr
""" % script_var

  
#####################################################################


script_var['cdr_cli_005'] = """
context %(context_name)s
""" % script_var


#####################################################################


script_var['cdr_cli_006'] = """
context %(context_name)s
cdr
""" % script_var

#the list of commands are used in testcase aaa_cli_003
script_var['list_of_commands6']="""
check            Determine how the various selections are applied
circuit-session  Circuit/session handle debugging
context          Context debugging
go               Re-enable log debugging after 'debug hold' has been entered
hold             Disable all log debugging until 'debug go' is entered
module           Module debugging
next-session     Next session bring-up debugging
process-module   Process module debugging
slot             Slot debugging
"""

script_var['list_of_commands7']="""
all        All debugging for this module
cdrbuf     CDR Buffer Tracking events
cdrmsg     CDR Msg events
conf       Configuration events
ctxmgr     CDR Context Manager events
exception  CDR exception debugging
file       File events
ha         HA events
msgtrig    CDR Message disk commit trigger events
timedur    Time Duration Tracking events
timer      Timer events
upload     File upload
"""

#the list of commands are used in testcase aaa_cli_003
script_var['list_of_commands8']="""
cdrlib   Module cdrlib logging
cdrproc  Module cdrproc logging
cdrtest  Module cdrtest logging
"""


#mis-configuration is lodaded
script_var['cdr_cli_013'] ="""
debug circuit-session fffffffff
"""


#mis-configuration is lodaded
script_var['cdr_cli_014'] ="""
disk-commit-interval 0
"""

#mis-configuration is lodaded
script_var['cdr_cli_015'] ="""
disk-commit-interval 1440001
"""


#####################################################################


script_var['autoexec_config'] = """

ike log            stdout off
ike listen any  500
ipsec addr add %(upload_server_ip1)s 255.255.0.0 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           17.1.1.2 500
test multiclient set local            %(upload_server_ip1)s 500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            2
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn ikev2@%(context_name)s
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

test multiclient connect """ % script_var

#########################################################################################
script_var['add_iptakama'] = """

max_count=3

n3=2
n4=1

i=1
while [ $n3 -le 255 ]
do
        while [ $n4 -le 255 ]
        do
                #echo 9.9.$n3.$n4
                #echo ip addr add dev eth0 10.10.$n3.$n4/16 brd +
                /sbin/ip addr add dev eth1 7.7.$n3.$n4/16 brd +
                #/sbin/ip addr add dev eth2 7.7.$n3.$n4/16 brd +
                #echo ip route add 4.4.4.4 via 15.1.1.1 dev eth2 src 9.9.$n3.$n4
                /sbin/ip route add 4.4.4.4 via 17.1.1.2 dev eth1 src 7.7.$n3.$n4
                /sbin/ifconfig eth1:$i 17.1.$n3.$n4 netmask 255.255.255.0
                #echo ifconfig eth2:$i 15.1.$n3.$n4 netmask 255.255.0.0
                #echo ifconfig eth2:$i 15.1.$n3.$n4 netmask 255.255.0.0
                #/sbin/ifconfig eth1:$i 17.1.$n3.$n4 netmask 255.255.0.0
                ((i += 1 ))
                if [ $i -ge $max_count ]
                then
                        exit 0
                fi
                (( n4 += 1 ))
        done
        (( n3 += 1 ))
        n4=0
done """ % script_var


#####################################################################


script_var['autoexec_config_EAP'] = """

ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  17.1.2.1  17.1.1.1/16 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           17.1.1.2 500
test multiclient set local            17.1.2.1   500
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

test multiclient connect """ % script_var





script_var['autoexec_config_takama_multi'] = """

ike log            stdout off
ike listen any  500
ipsec addr add %(upload_server_ip1)s 255.255.0.0 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt


test multiclient set remote           17.1.1.2 500
test multiclient set local            %(upload_server_ip1)s 500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            2
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn ikev6@%(context_name1)s
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

test multiclient connect """ % script_var

#########################################################################################
script_var['add_ip_takama_multi'] = """

max_count=1

n3=2
n4=1

i=1
while [ $n3 -le 255 ]
do
        while [ $n4 -le 255 ]
        do
                #echo 9.9.$n3.$n4
                #echo ip addr add dev eth0 10.10.$n3.$n4/16 brd +
                /sbin/ip addr add dev eth1 7.7.$n3.$n4/16 brd +
                #echo ip route add 4.4.4.4 via 15.1.1.1 dev eth2 src 9.9.$n3.$n4
                #/sbin/ip route add 4.4.4.4 via 17.1.1.2 dev eth1 src 7.7.$n3.$n4
                /sbin/ip route add 4.4.4.4 via 17.1.1.2 dev eth1 src 7.7.$n3.$n4
                #echo ifconfig eth2:$i 15.1.$n3.$n4 netmask 255.255.0.0
                /sbin/ifconfig eth1:$i 17.1.$n3.$n4 netmask 255.255.0.0
                ((i += 1 ))
                if [ $i -ge $max_count ]
                then
                        exit 0
                fi
                (( n4 += 1 ))
        done
        (( n3 += 1 ))
        n4=0
done """ % script_var


###################################################################################


script_var['autoexec_config_huahine_multi'] = """

ike log            stdout off
ike listen any  500
ipsec addr add 15.1.2.1 255.255.0.0 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           15.1.1.2 500
test multiclient set local            15.1.2.1 500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            2
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn ikev8@%(context_name2)s
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

test multiclient connect """ % script_var

#########################################################################################


script_var['add_ip_huahine_multi'] = """

max_count=1

n3=2
n4=1

i=1
while [ $n3 -le 255 ]
do
        while [ $n4 -le 255 ]
        do
                #echo 9.9.$n3.$n4
                #echo ip addr add dev eth0 10.10.$n3.$n4/16 brd +
                /sbin/ip addr add dev eth2 9.9.$n3.$n4/16 brd +
                #echo ip route add 4.4.4.4 via 15.1.1.1 dev eth2 src 9.9.$n3.$n4
                #/sbin/ip route add 4.4.4.4 via 17.1.1.2 dev eth1 src 7.7.$n3.$n4
                /sbin/ip route add 4.4.4.5 via 15.1.1.2 dev eth2 src 9.9.$n3.$n4
                #/sbin/ifconfig eth1:$i 17.1.$n3.$n4 netmask 255.255.0.0
                /sbin/ifconfig eth2:$i 15.1.$n3.$n4 netmask 255.255.0.0
                ((i += 1 ))
                if [ $i -ge $max_count ]
                then
                        exit 0
                fi
                (( n4 += 1 ))
        done
        (( n3 += 1 ))
        n4=0
done """ % script_var




###################################################################################


script_var['CDR_FUN_MULTI']= """
no context %(context_name1)s
no context %(context_name2)s
context %(context_name1)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev6
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev6 session loopback
  ip session-default
  ip address %(ses_loopip_mask)s
  exit
 interface local_trans1
  arp arpa
  ip address 17.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
  file-format xml
   upload-server %(upload_server_ip1)s protocol tftp
   exit
  exit
 exit
port ethernet  %(ssx_port1_multi)s
 bind interface local_trans1 %(context_name1)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit
context %(context_name2)s
 aaa profile
  session accounting none
  session authentication local
  service authorization local
  exit
 event volume 1000_bytes 1000 action generate-cdr repeat
 session name ikev8
  ip address pool
  class-of-service icmp_policy
  event volume 1000_bytes
  exit
 ip pool %(pool_ip2)s 500
 filter-domain src
  ip any
  exit
 filter-domain dst
  ip any
  exit
 filter-protocol icmp icmp_protcol src-domain src dst-domain dst
  exit
 filter icmp_filter
filter-rule 10 icmp_protcol
  exit
 interface ikev8 session loopback
  ip session-default
  ip address %(ses_loopip2_mask)s
  exit
 interface local_trans2
  arp arpa
  ip address 15.1.1.2/16
  exit
 interface linux1
  arp arpa
  ip address 5.1.1.1/24
exit
 interface linux2
  arp arpa
  ip address 6.1.1.1/24
  exit
 interface linux3
  arp arpa
  ip address 7.1.1.1/24
  exit
 ipsec policy ikev2 phase2 name p12
  suite1
   hard-lifetime 360 secs
   soft-lifetime 50 secs
   exit
  exit
 ipsec policy ikev2 phase1 name p11
  suite1
   gw-authentication psk 12345
   peer-authentication psk
   hard-lifetime 360 secs
   soft-lifetime 60 secs
   exit
  exit
 class icmp_class
  filter icmp_filter
  exit
 class-of-service icmp_policy
  inbound
   class icmp_class
    event volume 1000_bytes
    exit
   exit
  enable
  exit
 cdr
  disk-commit-interval 1
  upload-profile %(upload_profile1)s
   interval 1
  file-format xml
   upload-server %(upload_server_ip2)s protocol tftp
   exit
  exit
 exit
port ethernet  %(ssx_port2_multi)s
 bind interface local_trans2 %(context_name2)s
  ipsec policy ikev2 phase1 name p11
  ipsec policy ikev2 phase2 name p12
  exit
 service ipsec
 enable
 exit """ %script_var




