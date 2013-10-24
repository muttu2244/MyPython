#This File Contains Common Script Variables and Configurations for both SSX and Netscreen-5GT

#Import the Topo file.
import topo

#Common Script Variables:
###################################################################################################

#SSX Variables:
#**************
script_var={}
script_var['context']=		'india-test'
#script_var['ssx_int_name']=	'untrust'
script_var['ssx_phy_ip1']=	'10.1.1.1'
script_var['ssx_phy_ip1_mask']=	'10.1.1.1/16'

script_var['ssx_phy_ip2']=       '17.1.1.2'
script_var['ssx_phy_ip2_mask']=  '17.1.1.2/16'

script_var['ssx_ses_ip']=	'11.11.11.1'
script_var['ssx_ses_ip_mask']=	'11.11.11.1/24'
#script_var['ssx_port']=		topo.p1_ssx_ns[0]

script_var['p1_ssx1_ns1']=topo.p1_ssx1_ns1[0]
script_var['p2_ssx1_linux1']=topo.p2_ssx1_linux1[0]
script_var['p3_ssx1_linux2']=topo.p3_ssx1_linux2[0]
script_var['p4_ssx1_linux3']=topo.p4_ssx1_linux3[0]

script_var['psk']=		'12345'
script_var['auth_user']=	'aggr'
script_var['dpd_intrvl']=	'10'
script_var['dpd_retr_intrvl']=	'15'
script_var['dpd_retries']=	'2'

#**************************************************************************************************

#NS-5GT Variables:
#*****************
script_var['ns_phy_ip']=	'10.1.1.2'
script_var['ns_phy_ip_mask']=	'10.1.1.2/16'

script_var['ns_ses_ip']=        '11.11.11.2'

###################################################################################################
# Radius Variables:

script_var['radius1_ip'] = ''
script_var['radius2_ip'] = '100.3.8.164'



#Configurations for SSX:
#************************
script_var['user_add_ssx'] ="""context %(context)s
 user name user1
  password user1
  priv-level administrator
  exit
 user name user2
  password user2
  priv-level operator
  exit
 exit""" %script_var
#Common configuration of SSX:
###################################################################################################

script_var['common_ssx']="""
end
conf
context %(context)s
ip pool 11.11.11.10 20
 interface untrust
  arp arpa
  ip address %(ssx_phy_ip1_mask)s
  exit
 interface ext
  arp arpa
  ip address %(ssx_phy_ip2_mask)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
 interface radius1
  arp arpa
  ip address 100.3.8.165/24
  exit
 interface radius2
  arp arpa
  ip address 10.10.10.10/24
  exit
 exit
port ethernet %(p1_ssx1_ns1)s
 enable
 bind interface untrust %(context)s
 exit
 exit
port ethernet %(p2_ssx1_linux1)s
 enable
 bind interface ext %(context)s
 exit
 exit
port ethernet %(p3_ssx1_linux2)s
 enable
 bind interface radius1 %(context)s
 exit
 exit
port ethernet %(p4_ssx1_linux3)s
 enable
 bind interface radius2 %(context)s
 exit
 exit""" %script_var

#################################################################################################
############################################################################################################
script_var['fun_001_ssx'] = """context %(context)s
aaa profile
user authentication local"""  % script_var

############################################################################################################
script_var['fun_002_ssx'] = """context %(context)s
aaa profile
user authentication local"""  % script_var

############################################################################################################
script_var['fun_003_ssx'] = """aaa global profile
 default-domain authentication india-test
 exit"""

###########################################################################################################
script_var['fun_004_ssx'] = script_var['fun_003_ssx']

#################################################################################################################
script_var['fun_005_ssx'] ="""context %(context)s
aaa profile
 user authentication local
exit
user name user1
 password user1
 priv-level administrator
 timeout idle 60
exit
user name user2
 password user2
 priv-level operator
 timeout idle 60
exit""" % script_var

######################################################################################
script_var['fun_006_ssx'] = """context %(context)s
aaa profile
 user authentication local
exit
user name user1
 password user1
 priv-level administrator
 timeout absolute 60
exit
user name user2
 password user2
 priv-level operator
 timeout absolute 60
exit""" % script_var
###########################################################################################################
script_var['fun_007_ssx'] = """context %(context)s
aaa profile
user authentication local
max-session 5
session accounting radius
session authentication radius
exit
radius session authentication profile
server %(radius2_ip)s port 1812 key topsecret
exit

ipsec policy ikev2 phase1 name ph1-test1
custom
encryption aes128
hash sha-1
d-h group5
prf sha-1
gw-authentication psk 12345
peer-authentication eap
hard-lifetime 40 hours
exit
exit
ipsec policy ikev2 phase2 name ph2-test1
custom
encryption triple-des
hash md5
pfs group2
hard-lifetime 40 hours
soft-lifetime 600 secs
exit
exit
exit
port ethernet %(p2_ssx1_linux1)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var
###########################################################################################################
#########################################################################################################3
script_var['fun_007_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  17.1.2.1  255.255.0.0 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            17.1.2.1   500
test multiclient set numclients       9
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context)s
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
test multiclient set delay 200
test multiclient configure

ike start

test multiclient connect""" % script_var
###############################################################################################################
script_var['fun_008_ssx'] = """context %(context)s
aaa profile
user authentication none
exit""" % script_var

###########################################################################################################
script_var['fun_009_ssx'] = """context %(context)s
aaa profile
user authentication radius
exit
radius user authentication profile
server %(radius2_ip)s port 1812 key topsecret
exit""" % script_var
############################################################################################################
script_var['fun_010_ssx'] = """context %(context)s
aaa profile
user authentication radius
exit
radius user authentication profile
server %(radius2_ip)s port 1812 key topsecret
exit"""  % script_var
###########################################################################################################
script_var['fun_011_ssx'] = """context %(context)s
aaa profile
user authentication radius local
exit
radius user authentication profile
server 1.1.1.1 port 1812 key topsecret
exit""" % script_var

###########################################################################################################
script_var['fun_012_ssx'] = """context %(context)s
 user name user0
  password user0
  priv-level administrator
 exit
aaa profile
 user authentication radius local
exit
radius user authentication profile
server %(radius2_ip)s port 1812 key topsecret
exit""" % script_var

############################################################################################################
script_var['fun_013_ssx'] = """context %(context)s
aaa profile
  user accounting radius
  user authentication radius
exit
 radius user authentication profile
  server %(radius2_ip)s port 1812 key topsecret
 exit
 radius user accounting profile
  server %(radius2_ip)s port 1813 key topsecret
 exit"""  % script_var
############################################################################################################
script_var['fun_014_ssx'] = """context %(context)s
aaa profile
  user authentication none"""

############################################################################################################
script_var['fun_015_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication local
  service authorization local
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

#################################################################################################

script_var['fun_016_ssx'] = script_var['fun_015_ssx'] 
#################################################################################################
script_var['fun_017_ssx'] = script_var['fun_015_ssx'] 
#################################################################################################
script_var['fun_018_ssx'] = """
context %(context)s
 aaa profile
  session authentication local
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  timeout idle 60
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

#################################################################################################
script_var['fun_019_ssx'] = """
context %(context)s
 aaa profile
  session authentication local
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  timeout absolute 60
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var
#################################################################################################
script_var['fun_020_ssx'] = """
aaa global profile
 default-domain authentication %(context)s
 default-domain authorization %(context)s
 exit
context %(context)s
 aaa profile
  session authentication local
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit""" % script_var
#################################################################################################
script_var['fun_021_ssx']=script_var['fun_020_ssx']
#################################################################################################
script_var['fun_022_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius2_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var
#################################################################################################
script_var['fun_023_ssx'] = script_var['fun_022_ssx']
################################################################################################
script_var['fun_024_ssx'] = script_var['fun_022_ssx'] 
################################################################################################
script_var['fun_025_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication radius local
  exit
 radius session authentication profile
  server 1.1.1.1 port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var
##################################################################################################
script_var['fun_026_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user2
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user2
  exit
 aaa profile
  session authentication radius local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var
###################################################################################################
script_var['fun_027_ssx']="""context %(context)s"""

###################################################################################################
script_var['fun_028_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication local
  service authorization local
  session authentication radius 
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ %script_var
###################################################################################################

###################################################################################################
script_var['fun_030_ssx'] = script_var['fun_015_ssx'] 

###################################################################################################
script_var['fun_029_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication radius 
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 radius user authentication profile
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var
###################################################################################################

###################################################################################################
script_var['fun_030_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication local
  service authorization local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 radius user authentication profile
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit
port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var
###################################################################################
script_var['fun_030_ssx_mah'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

###################################################################################################
script_var['fun_030_ssx_mahesh'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit

ipsec policy ikev1 phase1 name p31
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p41
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p31
  ipsec policy ikev1 phase2 name p41
  exit
 service ipsec
 enable

 service ipsec
 enable
 exit
exit """ % script_var
###################################################################################################
script_var['fun_031_ssx'] = """
context %(context)s
 session name aggr
 ipsec policy ikev1 phase1 name p11
  password 12345
  exit
 session name user1
  ipsec policy ikev1 phase2 name p21
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication local
  service authorization local
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 ipsec policy ikev1 phase1 name p12
  suite2 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p22
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p12
  ipsec policy ikev1 phase2 name p22
  exit
 service ipsec
 enable
 exit
exit """ % script_var
#########################################################################################
script_var['fun_032_ssx'] = """aaa global profile
 default-domain authentication %(context)s
 default-domain authorization %(context)s
 exit

context %(context)s
 session name aggr
 ipsec policy ikev1 phase1 name p11
  password 12345
  exit
 session name user1
  ipsec policy ikev1 phase2 name p21
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication local
  service authorization local
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 ipsec policy ikev1 phase1 name p12
  suite2 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p22
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p12
  ipsec policy ikev1 phase2 name p22
  exit
 service ipsec
 enable
 exit
exit """ % script_var
###########################################################################

#Configurations for Netscreen-5GT:
#*********************************
#################################################################################################

script_var['common_ns5gt']="""

set clock timezone 0
set vrouter trust-vr sharable
set vrouter "untrust-vr"
exit
set vrouter "trust-vr"
unset auto-route-export
exit
set auth-server "Local" id 0
set auth-server "Local" server-name "Local"
set auth default auth server "Local"
set auth radius accounting port 1646
set admin name "netscreen"
set admin password "nKVUM2rwMUzPcrkG5sWIHdCtqkAibn"
set admin auth timeout 10
set admin auth server "Local"
set admin format dos
set zone "Trust" vrouter "trust-vr"
set zone "Untrust" vrouter "trust-vr"
set zone "VLAN" vrouter "trust-vr"
set zone "Untrust-Tun" vrouter "trust-vr"
set zone "Trust" tcp-rst 
set zone "Untrust" block 
unset zone "Untrust" tcp-rst 
set zone "MGT" block 
set zone "VLAN" block 
unset zone "VLAN" tcp-rst 
set zone "Untrust" screen tear-drop
set zone "Untrust" screen syn-flood
set zone "Untrust" screen ping-death
set zone "Untrust" screen ip-filter-src
set zone "Untrust" screen land
set zone "V1-Untrust" screen tear-drop
set zone "V1-Untrust" screen syn-flood
set zone "V1-Untrust" screen ping-death
set zone "V1-Untrust" screen ip-filter-src
set zone "V1-Untrust" screen land
set interface "trust" zone "Trust"
set interface "untrust" zone "Untrust"
set interface "tunnel.1" zone "Untrust"
unset interface vlan1 ip
set interface trust route
set interface untrust ip %(ns_phy_ip_mask)s
set interface untrust route
set interface "tunnel.1" ipv6 mode "host"
set interface "tunnel.1" ipv6 ip 1234::1/64
set interface "tunnel.1" ipv6 enable
unset interface vlan1 bypass-others-ipsec
unset interface vlan1 bypass-non-ip
set interface trust ip manageable
set interface untrust ip manageable
set interface untrust manage ping
set interface tunnel.1 ipv6 nd nud
set interface tunnel.1 ipv6 nd dad-count 0
set flow tcp-mss
unset flow no-tcp-seq-check
set flow tcp-syn-check
set console timeout 0
set hostname ns5gt

set pki authority default scep mode "auto"
set pki x509 default cert-path partial
set ike p1-proposal "p1" preshare group2 esp 3des sha-1 hour 8
set ike p2-proposal "p2" no-pfs esp null sha-1 hour 1
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr@%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1"
set ike gateway "v4gate" xauth client any username user1@%(context)s password 123user1
set ike gateway v4gate modecfg client pd interface tunnel.1 sla-id 1 sla-len 16
set ike respond-bad-spi 1
set ike id-mode ip
unset ipsec access-session enable
set ipsec access-session maximum 5000
set ipsec access-session upper-threshold 0
set ipsec access-session lower-threshold 0
set ipsec access-session dead-p2-sa-timeout 0
unset ipsec access-session log-error
unset ipsec access-session info-exch-connected
unset ipsec access-session use-error-log
set xauth client expect-config
set vpn "vpn4" gateway "v4gate" no-replay tunnel idletime 0 proposal "p2"
set vpn "vpn4" id 1 bind interface tunnel.1
set url protocol sc-cpa
exit
set policy id 1 from "Trust" to "Untrust"  "Any-IPv4" "Any-IPv4" "ANY" nat src permit 
set policy id 1
exit
set policy id 2 from "Untrust" to "Trust"  "Any-IPv4" "Any-IPv4" "ANY" permit 
set policy id 2
exit
set global-pro policy-manager primary outgoing-interface untrust
set global-pro policy-manager secondary outgoing-interface untrust
set nsmgmt bulkcli reboot-timeout 60
set ssh version v2
set config lock timeout 5
set modem speed 115200
set modem retry 3
set modem interval 10
set modem idle-time 10
set snmp port listen 161
set snmp port trap 162
set vrouter "untrust-vr"
exit
set vrouter "trust-vr"
unset add-default-route
set route 0.0.0.0/0 interface tunnel.1
exit
set vrouter "untrust-vr"
exit
set vrouter "trust-vr"
exit		"""%script_var

#**************************************************************************************************
#Netscreen Configuration for the Test Case "ikev1_int_002_ns5gt":

script_var['fun_015_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr@%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var

#**************************************************************************************************
script_var['fun_016_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id invaliduser@%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var

#**************************************************************************************************
script_var['fun_017_ns5gt']="""set ike gateway "v4gate" xauth client any username invalidxauthuser@%(context)s password 123user1""" %script_var
#**************************************************************************************************
script_var['fun_018_ns5gt'] = script_var['fun_015_ns5gt']
#**************************************************************************************************
script_var['fun_019_ns5gt'] = script_var['fun_015_ns5gt']
#**************************************************************************************************
script_var['fun_020_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1"
set ike gateway "v4gate" xauth client any username user1 password 123user1 """%script_var
#**************************************************************************************************
script_var['fun_021_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1"
set ike gateway "v4gate" xauth client any username user1 password 123user1 """%script_var
#**************************************************************************************************
script_var['fun_022_ns5gt']=script_var['fun_015_ns5gt']
#**************************************************************************************************
script_var['fun_023_ns5gt']=script_var['fun_016_ns5gt']
#**************************************************************************************************
script_var['fun_024_ns5gt']="""set ike gateway "v4gate" xauth client any username invalidxauthuser@%(context)s password 123user1""" %script_var
#**************************************************************************************************
script_var['fun_025_ns5gt']="""set ike gateway "v4gate" xauth client any username invalidxauthuser@%(context)s password 123user1""" %script_var
#**************************************************************************************************
script_var['fun_026_ns5gt']="""set ike gateway "v4gate" xauth client any username user2@%(context)s password 123user1""" %script_var
#**************************************************************************************************
script_var['fun_027_ns5gt']="""set ike gateway "v4gate" xauth client any username invalidxauthuser@%(context)s password 123user1""" %script_var
#**************************************************************************************************
script_var['fun_028_ns5gt'] = script_var['fun_015_ns5gt']

#**************************************************************************************************
script_var['fun_029_ns5gt']=script_var['fun_015_ns5gt']

#**************************************************************************************************
script_var['fun_030_ns5gt']=script_var['fun_015_ns5gt']

#**************************************************************************************************
script_var['fun_031_ns5gt'] = script_var['fun_015_ns5gt']

#**************************************************************************************************
script_var['fun_032_ns5gt'] = """
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var
#**************************************************************************************************
script_var['neg_001_ns5gt'] = script_var['fun_015_ns5gt']
#**************************************************************************************************

#**************************************************************************************************
script_var['neg_002_ns5gt'] = script_var['fun_015_ns5gt']
#**************************************************************************************************
#**************************************************************************************************
script_var['neg_003_ns5gt'] = script_var['fun_015_ns5gt']
#**************************************************************************************************
script_var['neg_001_ssx'] = script_var['fun_015_ssx'] 

#**************************************************************************************************
script_var['neg_002_ssx']= """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

 
#**************************************************************************************************
script_var['neg_003_ssx']= """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask 255.255.255.255
  password 123user1
  exit
 aaa profile
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(p1_ssx1_ns1)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var
























