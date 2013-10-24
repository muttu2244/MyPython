#This File Contains Common Script Variables and Configurations for both SSX,Netscreen-5GT and Xpress-VPN

#Import the Topo file.
import topo


#SSX Variables:
#**************
script_var={}

script_var['ssx_max_session'] =23
script_var['ssx_custom_profile']=1000
script_var['ip_netmask']	="255.255.255.255"

script_var['context']=		'india-test'

script_var['ssx_ses_ip']=	'11.11.11.1'
script_var['ssx_ses_ip_mask']=	'11.11.11.1/24'

script_var['ssx_phy_ip1']=	'10.1.1.1'
script_var['ssx_phy_ip1_mask']=	'10.1.1.1/16'

## ssx interface ip bounded to a port connected to xpressvpn client

script_var['ssx_phy_ip2']=       '17.1.1.2'
script_var['ssx_phy_ip2_mask']=  '17.1.1.2/16'

script_var['port_ssx_xpressxpn']=topo.port_ssx_linux[0]

script_var['port_ssx_radius1']=topo.port_ssx_radius1[0]
script_var['port_ssx_radius2']=topo.port_ssx_radius2[0]

script_var['ssx_rad1_ip']=  '19.1.1.21'
script_var['ssx_rad1_ip_mask']=  '19.1.1.21/24'

script_var['ssx_rad2_ip']=  '13.1.1.21'
script_var['ssx_rad2_ip_mask']=  '13.1.1.21/24'

script_var['xpress_netmask'] = '255.255.0.0'
script_var['radius_netmask'] = '255.255.255.0'


# nas Ip address

script_var['ssx_nas_ip_address']=       '19.1.1.21' # magmt route
script_var['ssx_nas_identifier']= 	'Stoke'
# ssx ports 

script_var['port_ssx_ns']=topo.port_ssx_ns[0]
script_var['port_ssx_linux']=topo.port_ssx_linux[0]
script_var['port_ssx_radius1']=topo.port_ssx_radius1[0]
script_var['port_ssx_radius2']=topo.port_ssx_radius2[0]



# ike1 
#script_var['psk']=		'12345'
#script_var['auth_user']=	'aggr'
#script_var['dpd_intrvl']=	'10'
#script_var['dpd_retr_intrvl']=	'15'
#script_var['dpd_retries']=	'2'

###############################################################################
# IKEv2 client interfaces 
##############################################################################3
script_var['xpress_phy_iface1_ip'] = '17.1.2.1'
script_var['vgroup_phy_iface1_ip'] = '17.1.1.1'
script_var['xpress_phy_iface1_ip_mask'] = '17.1.1.1/16'

### ikev2 client (xpressvpn) ips lists

clnt_ips = ("17.1.2.1","17.1.2.2","17.1.2.3","17.1.2.4","17.1.2.5","17.1.2.6",
                                        "17.1.2.7","17.1.2.8","17.1.2.9")

clnt_ips2 = ("11.11.11.10","11.11.11.11","11.11.11.12","11.11.11.13","11.11.11.14","11.11.11.15",
                                        "11.11.11.16","11.11.11.17","11.11.11.18")


#**************************************************************************************************
###############################################################################

#NS-5GT Variables:
#*****************
script_var['ns_phy_ip']=	'10.1.1.2'
script_var['ns_phy_ip_mask']=	'10.1.1.2/16'

script_var['ns_ses_ip']=        '11.11.11.2'

###############################################################################
# Radius Variables:

script_var['radius1_ip'] = '19.1.1.1'
script_var['radius2_ip'] = '13.1.1.1'

script_var['radius1_ip_mask']=                  '19.1.1.1/24'           #Huahine
script_var['radius2_ip_mask']=                  '13.1.1.1/24'           #qa-svr3


#script_var['radius2_ip'] = '17.1.1.1'
#script_var['radius2_ip'] = '10.3.5.31'

#script_var['radius2_ip'] = '100.3.8.163' 
#script_var['radius2_ip'] = '10.3.2.33'
script_var['radius2_ip_invalid'] = '10.3.5.254'

#Configurations for SSX:


##########################################################################

script_var['vgroup_ssx']="""
no context %(context)s
context %(context)s
 interface xpress_vpn 
  arp arpa
  ip address %(ssx_phy_ip2_mask)s
  exit
interface radius1
  arp arpa
  ip address %(ssx_rad1_ip_mask)s
  exit
interface radius2
  arp arpa
  ip address %(ssx_rad2_ip_mask)s
  exit
  ip route 17.1.0.0/16 %(xpress_phy_iface1_ip)s
exit
port ethernet %(port_ssx_xpressxpn)s
 enable
 bind interface xpress_vpn %(context)s
 exit
 exit
port ethernet %(port_ssx_radius1)s
 enable
 bind interface radius1 %(context)s
exit
exit
port ethernet %(port_ssx_radius2)s
 enable
 bind interface radius2 %(context)s
exit
exit""" %script_var


##########################################################################




############# CLI tests ########################
script_var['aaa_cli_001'] = """
context %(context)s
aaa profile""" %script_var

#the list of commands are used in testcase aaa_cli_001
script_var['list_of_commands']="""
debug        Debug logging
end          Exit configuration mode
exit         Exit current configuration mode
max-session  Configure max active sessions allowed in this ctx
no           Remove setting or configuration
service      Configure AAA service method-lists
session      Configure AAA session method-lists
show         Display system information
user         Configure AAA user method-lists
"""


script_var['aaa_cli_002'] = """
context %(context)s
 aaa profile
  user authentication local
  session accounting radius
  session authentication local
  service authorization local
  max-session %(ssx_max_session)i
  exit
exit
 exit""" % script_var


script_var['aaa_cli_003'] = """
 aaa global profile
 default-domain authentication %(context)s 
 default-domain authorization india-stoke
 custom-profile %(ssx_custom_profile)i
 exit
context local
 exit""" % script_var

#loading all induvisual modules

script_var['aaa_cli_004'] = """
debug module aaad authorization
debug module aaad configuration
debug module aaad exception
debug module aaad general
debug module aaad initialization
debug module aaad radius-exception
debug module aaad radius-packet
debug module aaad radius-server
debug module aaad ses-provisioning
debug module aaad session"""


#mis-configuration is lodaded
script_var['aaa_cli_005'] ="""
debug circuit-session fffffffff
max-session 66000
session  authorization ldap"""

#loading the confuguration in testcase aaa_cli_006
script_var['aaa_cli_006_before_no'] = """
 aaa global profile
 default-domain authentication %(context)s
 default-domain authorization india-stoke
 custom-profile %(ssx_custom_profile)i
exit""" % script_var

#removing the configuration using the 'no' command
script_var['aaa_cli_006_no_profile'] = """
 aaa global profile
 no default-domain authentication %(context)s
 no custom-profile %(ssx_custom_profile)i""" % script_var

#checking the removed by no command or not
script_var['aaa_cli_006_after_no'] ="""custom-profile %(ssx_custom_profile)i
 default-domain authentication %(context)s""" % script_var


script_var['aaa_cli_007'] = """
context %(context)s
 aaa profile
  user accounting radius
  user authentication radius
  session accounting radius
  session authentication radius
  service authorization local
  max-session 4
  exit
 exit
exit"""  % script_var


############ Functional tests ##################3
script_var['user_add_ssx'] ="""context %(context)s
 user name user3
  password 123user3
  priv-level administrator
  exit
 user name user4
  password 123user4
  priv-level operator
  exit
 exit""" %script_var

###################################################################################################

#Configurations for SSX:
############# CLI tests #######################################################
#     configs as per each testcase
###############################################################################

#  The list of commands are used in testcase radius_cli_001

script_var['radius_cli_001'] = """context %(context)s
 radius session authentication profile
  timeout 60
  retry 10
  max-outstanding 12
  algorithm round-robin
  reset-timeout 120
  server 1.1.1.1 port 1812 key topsecret
  exit
 exit"""%script_var
###############################################################################
script_var['radius_cli_002'] = """context %(context)s
 radius session accounting profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1813 key topsecret
  exit
 exit""" % script_var


###############################################################################
script_var['radius_cli_003'] = """context %(context)s
  radius user authentication profile
  timeout 3600
  retry 100000
  max-outstanding 127
  algorithm first
  reset-timeout 3600
  server 1.1.1.1 port 1812 key topsecret
  exit
 exit""" % script_var


###############################################################################

script_var['radius_cli_004'] = """context %(context)s
 radius user accounting profile
  timeout 3600
  retry 1000
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1813 key topsecret
  exit
 exit""" %script_var

###############################################################################

script_var['radius_cli_005'] ="""context %(context)s
 radius attribute nas-ip-address 1.2.3.4
exit"""% script_var

###############################################################################

script_var['radius_cli_006'] = """context %(context)s
exit""" % script_var
###############################################################################
script_var['radius_cli_006'] = """context %(context)s
 radius session authentication profile
  server 1.1.1.1 port 1812 key topsecret
  server 1.1.1.2 port 1812 key topsecret
  exit
 exit""" %script_var


###############################################################################

script_var['radius_cli_007'] = """timeout 3600
  retry 100000000
  max-outstanding 257
  reset-timeout 3600990"""

##############################################################################
#loading the confuguration in testcase radius_cli_008
script_var['radius_cli_008_before_no'] = """context %(context)s
radius user authentication profile
 timeout 3600
 retry 100000
 max-outstanding 127
 algorithm first
 reset-timeout 3600
 server 1.1.1.1 port 1812 key topsecret
exit
radius user accounting profile
 timeout 3600
 retry 1000
 max-outstanding 127
 algorithm round-robin
 reset-timeout 3600
 server 1.1.1.1 port 1813 key topsecret
exit
radius session authentication profile
 server 30.30.30.30 port 1812 key mysecret
 server 30.30.30.31 port 1812 key mysecrete
 exit
radius session accounting profile
 server 30.30.30.30 port 1813 key mysecret
 server 30.30.30.31 port 1813 key mysecret
 exit
exit""" % script_var

###############################################################################
#removing the configuration using the 'no' command
script_var['radius_cli_008_no_profile'] = """context %(context)s
no radius user accounting profile
no radius user authentication profile
no radius session authentication profile
no radius session accounting profile
exit""" % script_var
#checking the removed by no command or not
script_var['radius_cli_008_after_no'] ="""radius user accounting profile
radius user authentication profile
radius session authentication profile
radius session accounting profile""" % script_var


##############################################################################
script_var['radius_cli_009'] = """context %(context)s
 radius strip-domain
 radius attribute nas-ip-address 1.2.3.4
 radius session accounting profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1813 key topsecret
  exit
 radius session authentication profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1812 key topsecret
  exit
 radius user accounting profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.2 port 1813 key topsecret
  exit
 radius user authentication profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.2 port 1812 key topsecret
  exit
 exit""" % script_var

##############################################################################
script_var['radius_cli_010'] = """context %(context)s
 radius strip-domain
 radius attribute nas-ip-address 1.2.3.4
 radius session accounting profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1813 key topsecret
  exit
 radius session authentication profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.1 port 1812 key topsecret
  exit
 radius user accounting profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.2 port 1813 key topsecret
  exit
 radius user authentication profile
  timeout 3600
  retry 100
  max-outstanding 127
  algorithm round-robin
  reset-timeout 3600
  server 1.1.1.2 port 1812 key topsecret
  exit
 exit""" %script_var

###############################################################################


###############################################################################






###############################################################################
#Common configuration of SSX:
###############################################################################

script_var['common_ssx']="""
end
conf
no context %(context)s
! context %(context)s
! interface mgm management
!  arp arpa
!  ip address 10.3.255.31/24
!  exit
! ip route 0.0.0.0/0 10.3.255.1
! exit
!  port ethernet 0/0
!   bind interface mgm india-test
!    exit
!   enable
!   exit
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
 interface rad1
  arp arpa
  ip address %(ssx_rad1_ip_mask)s
  exit
 interface rad2
  arp arpa
  ip address %(ssx_rad2_ip_mask)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
 exit
port ethernet %(port_ssx_ns)s
 enable
 bind interface untrust %(context)s
 exit
 exit
port ethernet %(port_ssx_radius1)s
 enable
 bind interface rad1 %(context)s
 exit
 exit
port ethernet %(port_ssx_radius2)s
 enable
 bind interface rad2 %(context)s
 exit
 exit
port ethernet %(port_ssx_linux)s
 enable
 bind interface ext %(context)s
 exit
 exit """ %script_var

##############################################################################
script_var['common_ssx1']="""
end
conf
no context %(context)s
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
 interface rad1
  arp arpa
  ip address %(ssx_rad1_ip_mask)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
 exit
port ethernet %(port_ssx_ns)s
 enable
 bind interface untrust %(context)s
 exit
 exit
port ethernet %(port_ssx_radius1)s
 enable
 bind interface rad1 %(context)s
 exit
 exit
port ethernet %(port_ssx_linux)s
 enable
 bind interface ext %(context)s
 exit
 exit """ %script_var


###############################################################################
script_var['fun_001_ssx'] = """context %(context)s
aaa profile
user authentication local"""  % script_var

###############################################################################
script_var['fun_002_ssx'] = """context %(context)s
aaa profile
user authentication local"""  % script_var

###############################################################################
script_var['fun_003_ssx'] = """aaa global profile
 default-domain authentication %(context)s 
 exit""" % script_var

###############################################################################
script_var['fun_004_ssx'] = script_var['fun_003_ssx']

###############################################################################
script_var['fun_005_ssx'] ="""context %(context)s
aaa profile
 user authentication local
exit
user name user3
 password 123user3
 priv-level administrator
 timeout idle 60
exit
user name user4
 password 123user4
 priv-level operator
 timeout idle 60
exit""" % script_var
###############################################################################
script_var['fun_006_ssx'] = """context %(context)s
aaa profile
 user authentication local
exit
user name user3
 password 123user3
 priv-level administrator
 timeout absolute 60
exit
user name user4
 password 123user4
 priv-level operator
 timeout absolute 60
exit""" % script_var
###############################################################################
script_var['fun_007_ssx'] = """context %(context)s
aaa profile
user authentication local
max-session 5
session authentication radius
exit
radius session authentication profile
server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var
###############################################################################
script_var['fun_007_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
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
test multiclient set delay 1000
test multiclient configure

ike start

test multiclient connect""" % script_var



###########################################################################################################
#########################################################################################################3
script_var['EAP_MD5_xpressvpn'] = """


ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap md5 password 123user1

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn user1@india-test
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

test multiclient connect""" % script_var



###############################################################################################################
###############################################################################################################


script_var['fun_007_xpressvpn_multi'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
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
test multiclient set delay 1000
test multiclient configure

ike start

test multiclient connect""" % script_var
###############################################################################



script_var['fun_008_ssx'] = """context %(context)s
aaa profile
user authentication none
exit""" % script_var

###############################################################################
script_var['fun_009_ssx'] = """context %(context)s
aaa profile
user authentication radius
exit
radius user authentication profile
server %(radius1_ip)s port 1812 key topsecret
exit""" % script_var
###############################################################################
script_var['fun_010_ssx'] = """context %(context)s
aaa profile
user authentication radius
exit
radius user authentication profile
server %(radius1_ip)s port 1812 key topsecret
exit"""  % script_var
##############################################################################
script_var['fun_011_ssx'] = """context %(context)s
aaa profile
user authentication radius local
exit
radius user authentication profile
retry 1
timeout 1
server %(radius2_ip_invalid)s port 1812 key topsecret
exit""" % script_var

###############################################################################
script_var['fun_012_ssx'] = """context %(context)s
 user name user0
  password user0
  priv-level administrator
 exit
aaa profile
 user authentication radius local
exit
radius user authentication profile
server %(radius1_ip)s port 1812 key topsecret
exit""" % script_var

##############################################################################
script_var['fun_013_ssx'] = """context %(context)s
aaa profile
  user accounting radius
  user authentication radius
exit
 radius user authentication profile
  server %(radius1_ip)s port 1812 key topsecret
 exit
 radius user accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit"""  % script_var
###############################################################################
script_var['fun_014_ssx'] = """context %(context)s
aaa profile
  user authentication none"""

###############################################################################
script_var['fun_015_ssx'] = """

context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##############################################################################

script_var['fun_016_ssx'] = script_var['fun_015_ssx'] 

##############################################################################

script_var['fun_017_ssx'] = script_var['fun_015_ssx'] 

##############################################################################
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
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##############################################################################
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
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##############################################################################

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
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit""" % script_var
##############################################################################
#script_var['fun_021_ssx']=script_var['fun_020_ssx']

script_var['fun_021_ssx'] = """
conf
no aaa global profile
exit
"""



##############################################################################

script_var['fun_022_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

#############################################################################

script_var['fun_023_ssx'] = script_var['fun_022_ssx']

#############################################################################

script_var['fun_024_ssx'] = script_var['fun_022_ssx'] 

#############################################################################

script_var['fun_025_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  user authentication radius local
  service authorization local
  exit
 radius session authentication profile
  retry 1
  timeout 1
  server %(radius2_ip_invalid)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var
##############################################################################

script_var['fun_026_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name localuser
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123localuser
  exit
 aaa profile
  session authentication radius local
  service authorization local
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##############################################################################
script_var['fun_027_ssx']="""context %(context)s
 aaa profile
  session accounting radius
  session authentication radius
  service authorization local
 exit
 session name aggr
  password 12345
  exit
 radius session authentication profile
 retry 1
 timeout 1
  server %(radius1_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var

###############################################################################
script_var['fun_028_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  user authentication local
  service authorization local
  session authentication radius 
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ %script_var
###############################################################################
script_var['fun_029_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  user authentication radius 
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

###############################################################################
script_var['fun_030_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication local
  service authorization local
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

##############################################################################

script_var['fun_031_ssx'] = """
context %(context)s
 session name aggr
 ipsec policy ikev1 phase1 name p11
  password 12345
  exit
 session name user1
  ipsec policy ikev1 phase2 name p21
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
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
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##############################################################################

script_var['radius_fun_012_ssx'] = """context %(context)s
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

###############################################################################


#Configurations for Netscreen-5GT:
#*********************************
###############################################################################

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
set auth radius accounting port 1813
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

###############################################################################
#
#   Netscreen Configuration for the Test Case "ikev1_int_002_ns5gt":
#
###############################################################################

script_var['fun_015_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr@%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var

###############################################################################
script_var['fun_016_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id invaliduser@%(context)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var

###############################################################################
script_var['fun_017_ns5gt']="""set ike gateway "v4gate" xauth client any username invalid@%(context)s password 123user1""" %script_var
###############################################################################
script_var['fun_018_ns5gt'] = script_var['fun_015_ns5gt']
#script_var['fun_018_ns5gt'] = """ set ike gateway "v4gate" dpd interval 3
###############################################################################
script_var['fun_019_ns5gt'] = script_var['fun_015_ns5gt']
###############################################################################
script_var['fun_020_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1"
set ike gateway "v4gate" xauth client any username user1 password 123user1 """%script_var
################################################################## %(context)s #############
script_var['fun_021_ns5gt']="""
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1"
set ike gateway "v4gate" xauth client any username user1 password 123user1 """%script_var
###############################################################################
script_var['fun_022_ns5gt']=script_var['fun_015_ns5gt']
###############################################################################
script_var['fun_023_ns5gt']=script_var['fun_016_ns5gt']
###############################################################################
script_var['fun_024_ns5gt']="""set ike gateway "v4gate" xauth client any username invalid@%(context)s password 123user1""" %script_var
###############################################################################
#script_var['fun_025_ns5gt']="""set ike gateway "v4gate" xauth client any username invalid@%(context)s password 123user1""" %script_var
script_var['fun_025_ns5gt']= script_var['fun_015_ns5gt']
###############################################################################
script_var['fun_026_ns5gt']="""set ike gateway "v4gate" xauth client any username localuser@%(context)s password 123localuser""" %script_var
###############################################################################
script_var['fun_027_ns5gt'] = script_var['fun_015_ns5gt']
###############################################################################
script_var['fun_028_ns5gt'] = script_var['fun_015_ns5gt']

###############################################################################
script_var['fun_029_ns5gt']=script_var['fun_015_ns5gt']

###############################################################################
script_var['fun_030_ns5gt']=script_var['fun_015_ns5gt']

###############################################################################
script_var['fun_031_ns5gt'] = script_var['fun_015_ns5gt']

###############################################################################
script_var['fun_032_ns5gt'] = """
set ike gateway "v4gate" address %(ssx_phy_ip1)s Aggr local-id aggr outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare 12345 proposal "p1" """%script_var
###############################################################################
###############################################################################
script_var['neg_001_ns5gt'] = script_var['fun_015_ns5gt']
###############################################################################

script_var['neg_002_ns5gt'] = script_var['fun_015_ns5gt']
###############################################################################
script_var['neg_003_ns5gt'] = script_var['fun_015_ns5gt']
###############################################################################
script_var['neg_001_ssx'] = script_var['fun_015_ssx'] 

###############################################################################
script_var['neg_002_ssx']= """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  user authentication local
  session authentication radius
  service authorization local
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

 
###############################################################################
script_var['neg_003_ssx']= """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var





##########################################################################
#                                                                        #
#                   RADIUS FUNCTIONAL CONFIGS                            #
#                                                                        #
##########################################################################


##########################################################################
#			EAP_MD5 CONFIG                                   #
##########################################################################

script_var['rad_fun_001_v2_ssx'] = """context %(context)s
 exit
context india-test
 aaa profile
  user authentication local
  session authentication radius
  exit
 session name user1
  ip address pool
  password encrypted 62465C1E16452450
  exit
 radius session authentication profile
  server 19.1.1.1 port 1812 key topsecret
  exit
 ipsec policy ikev2 phase1 name ph1-test1
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
 ipsec policy ikev2 phase2 name ph2-test1
  custom
   hard-lifetime 40 hours
   soft-lifetime 600 secs
   encryption triple-des
   hash md5
   pfs group2
   exit
  exit
  exit
port ethernet %(port_ssx_linux)s
 service ipsec
 enable
 bind interface ext %(context)s
 ipsec policy ikev2 phase1 name ph1-test1
 ipsec policy ikev2 phase2 name ph2-test1
 exit
 exit """ %script_var




##########################################################################




script_var['rad_fun_001_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius attribute nas-ip-address %(ssx_nas_ip_address)s
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var


##########################################################################

script_var['rad_fun_002_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 timeout 10
 retry 3
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################

script_var['rad_fun_003_ssx'] = script_var['fun_024_ssx']

##########################################################################

script_var['rad_fun_004_ssx'] = script_var['fun_007_ssx']

##########################################################################

script_var['rad_fun_005_ssx'] = script_var['rad_fun_001_ssx']

##########################################################################

script_var['rad_fun_006_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius strip-domain
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 timeout 10
 retry 3
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit
port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################

script_var['rad_fun_007_ssx'] = script_var['fun_022_ssx']

###################################

script_var['rad_fun_007_1_ssx'] =  """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  session accounting radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
 server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var


##########################################################################

script_var['rad_fun_008_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 timeout 15
 retry 5
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit
 port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

########################################

script_var['rad_fun_008_1_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session authentication radius
  session accounting radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 timeout 15
 retry 5
 exit
 radius session accounting profile
 server %(radius1_ip)s port 1813 key topsecret
 timeout 15
 retry 5
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit
 port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

#########################################################################

script_var['rad_fun_010_ssx'] = """context %(context)s
aaa profile
 user authentication radius
 session accounting radius
 session authentication radius
exit
radius session authentication profile
 algorithm first
 server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var


####################################

script_var['rad_fun_010_1_ssx'] = """context %(context)s
aaa profile
 user authentication radius
 session accounting radius
 session authentication radius
exit
radius session authentication profile
 algorithm first
 server %(radius1_ip)s port 1812 key topsecret
 server %(radius2_ip)s port 1812 key topsecret
exit
radius session accounting profile
 algorithm first
 server %(radius1_ip)s port 1813 key topsecret
 server %(radius2_ip)s port 1813 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var

##########################################################################

script_var['rad_fun_011_ssx'] = """context %(context)s
aaa profile
 user authentication radius
 session authentication radius
exit
radius session authentication profile
 algorithm round-robin
 server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var

##################################

script_var['rad_fun_011_1_ssx'] = """context %(context)s
aaa profile
 user authentication radius
 session authentication radius
 session accounting radius
exit
radius session authentication profile
 algorithm round-robin
 server %(radius1_ip)s port 1812 key topsecret
 server %(radius2_ip)s port 1812 key topsecret
exit
radius session accounting profile
 algorithm round-robin
 server %(radius1_ip)s port 1813 key topsecret
 server %(radius2_ip)s port 1813 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var
##########################################################################

script_var['rad_fun_012_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius attribute nas-ip-address %(ssx_nas_ip_address)s
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
  server %(radius2_ip)s port 1812 key topsecret
  timeout 10
  !retry 3
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var
###################################

script_var['rad_fun_012_1_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session authentication radius
  session  accounting radius
  service authorization local
 exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
  server %(radius2_ip)s port 1812 key topsecret
  timeout 10
  retry 2
 exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
  server %(radius2_ip)s port 1813 key topsecret
  timeout 10
  retry 2
 exit

 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################

script_var['rad_fun_013_ssx'] = """context %(context)s
aaa profile
user authentication local
session authentication radius
exit
radius session authentication profile
max-outstanding 2
algorithm first
server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var

##############################

script_var['rad_fun_013_1_ssx'] = """context %(context)s
aaa profile
user authentication local
session authentication radius
session accounting radius
exit
radius session authentication profile
max-outstanding 2
algorithm first
server %(radius1_ip)s port 1812 key topsecret
server %(radius2_ip)s port 1812 key topsecret
exit
radius session accounting profile
max-outstanding 2
!algorithm first
server %(radius1_ip)s port 1813 key topsecret
server %(radius2_ip)s port 1813 key topsecret
retry 1
timeout 5
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var




##########################################################################

script_var['rad_fun_014_ssx'] = """context %(context)s
aaa profile
user authentication local
session authentication radius
exit
radius session authentication profile
algorithm first
retry 1
timeout 1
reset-timeout  30
server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var

##################################

script_var['rad_fun_014_1_ssx'] = """context %(context)s
aaa profile
user authentication local
session authentication radius
session accounting radius
exit
radius session authentication profile
 !reset-timeout 30
 !retry 1
 !timeout 1 
 algorithm first
 server %(radius1_ip)s port 1812 key topsecret
 server %(radius2_ip)s port 1812 key topsecret
exit
radius session accounting profile
 !retry 1
 !timeout 1
 !reset-timeout 30
 algorithm first
 server %(radius1_ip)s port 1813 key topsecret
 server %(radius2_ip)s port 1813 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var
 
##########################################################################

script_var['rad_fun_015_ssx'] = """context %(context)s
aaa profile
user authentication local
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var

##########################################

script_var['rad_fun_015_1_ssx'] = """context %(context)s
aaa profile
user authentication local
session accounting radius
session authentication radius
exit
radius session authentication profile
server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var


##########################################################################

script_var['rad_fun_016_ssx'] = """context %(context)s
aaa profile
session accounting radius
session authentication radius
exit
radius session authentication profile
max-outstanding 2
 retry 1
 timeout 1
server %(radius1_ip)s port 1812 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var


##########################################################################
script_var['rad_fun_016_1_ssx'] = """context %(context)s
aaa profile
session accounting radius
session authentication radius
exit
radius session authentication profile
 max-outstanding 1
 retry 1	
 server %(radius1_ip)s port 1812 key topsecret
exit
radius session accounting  profile
 max-outstanding 2
 retry 3
 server %(radius1_ip)s port 1813 key topsecret
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
port ethernet %(port_ssx_linux)s
bind interface ext %(context)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit""" % script_var
##########################################################################

script_var['rad_fun_017_ssx'] = script_var['fun_027_ssx']

##########################################################################

script_var['rad_fun_018_ssx'] = script_var['fun_027_ssx']

##########################################################################

script_var['rad_fun_019_ssx'] = script_var['fun_027_ssx']

##########################################################################

script_var['rad_fun_020_ssx'] = script_var['fun_027_ssx']

##########################################################################

script_var['rad_fun_021_ssx'] = script_var['fun_027_ssx']

##########################################################################

script_var['rad_fun_022_ssx'] =  """context %(context)s
aaa profile
  session authentication local
  session accounting radius  
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 session name user1
  ip address pool
  password 123user1
  exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var


##########################################################################
script_var['rad_fun_023_ssx'] = """context %(context)s
aaa profile
  session authentication radius
  session accounting radius
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 radius session accounting profile
  server %(radius2_ip)s port 1813 key topsecret
 exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var
##########################################################################

script_var['rad_fun_024_ssx'] = script_var['fun_027_ssx']


script_var['rad_fun_024_1_ssx'] = """context %(context)s
 aaa profile
  session accounting radius
  session authentication local
  service authorization local
 exit
 session name aggr
  password 12345
  exit
 radius session authentication profile
 retry 1
 timeout 1
  server %(radius1_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var



##########################################################################

script_var['rad_fun_025_ssx'] = script_var['fun_015_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session accounting radius
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

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

##########################################################################
script_var['rad_fun_026_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 session name user1
  ip address %(ns_ses_ip)s
  ip netmask %(ip_netmask)s
  password 123user1
  exit
 aaa profile
  session authentication local
  session accounting radius
  service authorization local
  exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var


##########################################################################

script_var['rad_fun_027_ssx'] = script_var['fun_027_ssx']

##########################################################################
script_var['rad_fun_028_ssx'] =  """context %(context)s
aaa profile
  session authentication local
  session accounting radius
  service authorization local
  exit
 session name aggr
  password 12345
  exit
 session name user1
  password 123user1
  exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
  exit
exit
exit"""% script_var

##########################################################################

script_var['rad_fun_029_ssx'] = script_var['rad_fun_028_ssx'] 

##########################################################################

script_var['rad_fun_030_ssx'] = """context %(context)s
 aaa profile
  session accounting radius
  session authentication radius
  service authorization local
 exit
 session name aggr
  password 12345
  exit
 radius session authentication profile
  server %(radius1_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
  server %(radius1_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var

##########################################################################
script_var['rad_fun_030_2_ssx'] = """context %(context)s
 aaa profile
  session accounting radius
  session authentication radius
  service authorization local
 exit
 session name aggr
  timeout idle 60 
  password 12345
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
  server %(radius2_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var

##########################################################################

##########################################################################
script_var['rad_fun_030_3_ssx'] = """context %(context)s
 aaa profile
  max-session 5
  session accounting radius
  session authentication radius
  service authorization local
 exit
 session name aggr
  password 12345
  exit
 radius session authentication profile
  server %(radius2_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
  server %(radius2_ip)s port 1813 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit"""% script_var
 

##########################################################################

script_var['rad_fun_031_ssx'] =  """
context %(context)s
 session name aggr
  password 12345
exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit
 exit

port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
exit """ % script_var
 

##########################################################################

script_var['rad_fun_031_ssx'] = script_var['fun_027_ssx'] 

##########################################################################

script_var['rad_fun_032_ssx'] = script_var['fun_027_ssx'] 

##########################################################################

script_var['rad_fun_033_ssx'] = """
context %(context)s 
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
 exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-chap 28800 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 26000 secs 0 secs
  exit

! ipsec policy ikev1 phase1 name p12
!  suite3 psk xauth-generic 800 secs 0 secs
!  exit
! ipsec policy ikev1 phase2 name p22
!  custom null sha-1 none 300 secs 0 secs
!  exit

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

port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit


port ethernet %(port_ssx_ns)s
 bind interface untrust %(context)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
!  ipsec policy ikev1 phase1 name p12
!  ipsec policy ikev1 phase2 name p22
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################

script_var['rad_fun_034_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
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

port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################


##########################################################################
#          RADIUS NEGATIVE TESTCASE CONFIS
##########################################################################

script_var['rad_neg_001_ssx'] =  """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius 
  service authorization local
 exit
 radius session authentication profile
 retry 1
 timeout 1
 server %(radius2_ip)s port 1812 key topsecret
 server %(radius1_ip)s port 1812 key topsecret
 exit
 radius session accounting profile
 retry 1
 timeout 10
 reset-timeout 5
 server %(radius2_ip)s port 1813 key topsecret
 server %(radius1_ip)s port 1813 key topsecret
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
port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit """ % script_var

##############################################################################


script_var['rad_neg_002_ssx'] =  """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius local
  service authorization local
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

port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit """ % script_var


##########################################################################



##########################################################################
script_var['rad_neg_003_ssx'] = """
context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius 
  service authorization local
 exit
 radius session authentication profile	
 server %(radius1_ip)s port 1812 key topsecret
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

port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit """ % script_var

##########################################################################

script_var['rad_neg_004_ssx'] = """context %(context)s
 session name aggr
  password 12345
  exit
 aaa profile
  session authentication radius 
  service authorization local
 exit
 radius session authentication profile
 server %(radius1_ip)s port 1812 key topsecret
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

port ethernet %(port_ssx_linux)s
 bind interface ext %(context)s
  ipsec policy ikev2 phase1 name ph1-test1
  ipsec policy ikev2 phase2 name ph2-test1
  exit
 service ipsec
 enable
exit """ % script_var


##########################################################################

script_var['rad_neg_005_ssx'] = script_var['rad_neg_004_ssx']

##########################################################################

script_var['rad_neg_006_ssx'] = script_var['rad_neg_005_ssx']

##########################################################################


#########################################################################


##########################################################################
#  									 #
#	            NS5GT CONFIGURATIONS   		  		 #
#				 			 		 #
##########################################################################

script_var['rad_fun_001_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_002_ns5gt'] = """set ike gateway "v4gate" xauth client any username user1@%(context)s password 123user1""" %script_var
###script_var['rad_fun_002_ns5gt'] = """set ike gateway "v4gate" xauth client any username user4timeout@%(context)s password 123user4timeout""" %script_var####

##########################################################################

script_var['rad_fun_003_ns5gt'] = script_var['fun_024_ns5gt']

##########################################################################

script_var['rad_fun_004_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
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


##########################################################################

script_var['rad_fun_005_ns5gt'] = script_var['fun_015_ns5gt']

script_var['rad_fun_005_1_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_006_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_007_ns5gt'] = script_var['fun_015_ns5gt']

script_var['rad_fun_007_1_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_008_ns5gt'] = script_var['fun_015_ns5gt']

script_var['rad_fun_008_1_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_010_xpressvpn'] = script_var['fun_007_xpressvpn']

script_var['rad_fun_010_1_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################

script_var['rad_fun_011_xpressvpn'] = script_var['fun_007_xpressvpn']

script_var['rad_fun_011_1_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################

script_var['rad_fun_012_ns5gt'] = script_var['fun_015_ns5gt']

script_var['rad_fun_012_1_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_013_xpressvpn'] = script_var['fun_007_xpressvpn']

script_var['rad_fun_013_1_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################

script_var['rad_fun_014_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
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
test multiclient set delay 5000
test multiclient configure

ike start

test multiclient connect""" % script_var
 

script_var['rad_fun_014_1_xpressvpn'] = script_var['rad_fun_014_xpressvpn']

##########################################################################

script_var['rad_fun_015_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
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

######################################################

script_var['rad_fun_015_1_xpressvpn'] = script_var['rad_fun_015_xpressvpn']

##########################################################################

script_var['rad_fun_016_xpressvpn'] = script_var['rad_fun_015_xpressvpn']

script_var['rad_fun_016_1_xpressvpn'] = script_var['rad_fun_015_xpressvpn']

##########################################################################

script_var['rad_fun_017_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_018_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_019_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_020_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_021_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_022_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_023_ns5gt'] = script_var['fun_015_ns5gt'] 

##########################################################################

script_var['rad_fun_024_ns5gt'] = script_var['fun_024_ns5gt']

script_var['rad_fun_024_1_ns5gt'] = script_var['fun_024_ns5gt']

##########################################################################

script_var['rad_fun_025_ns5gt'] = script_var['fun_016_ns5gt']

##########################################################################

script_var['rad_fun_026_ns5gt'] = script_var['fun_024_ns5gt']

##########################################################################

script_var['rad_fun_027_ns5gt'] = """set ike p2-proposal "p2" no-pfs esp null md5 hour 1"""

##########################################################################

script_var['rad_fun_030_ns5gt'] = script_var['fun_015_ns5gt']
script_var['rad_fun_030_2_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_030_3_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################

script_var['rad_fun_031_ns5gt'] = """set ike gateway "v4gate" xauth client any username abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcd@%(context)s password 01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567""" %script_var

##########################################################################

script_var['rad_fun_032_ns5gt'] = script_var['fun_015_ns5gt']

##########################################################################

script_var['rad_fun_033_ns5gt'] = """ set ike gateway "v4gate" xauth client chap username user1@%(context)s password 123user1 """  %script_var

##########################################################################

script_var['rad_fun_033_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################

script_var['rad_fun_034_xpressvpn'] = script_var['fun_007_xpressvpn']

##########################################################################




##########################################################################

script_var['rad_neg_001_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients        9
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context)s
aest multiclient set max-concurrent    9
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
test multiclient set delay 1500
test multiclient configure

ike start

test multiclient connect""" % script_var


##########################################################################

script_var['rad_neg_002_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients        9
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context)s
aest multiclient set max-concurrent    9
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
test multiclient set delay 3000
test multiclient configure

ike start

test multiclient connect""" % script_var



##########################################################################

script_var['rad_neg_003_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
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
test multiclient set delay 5000
test multiclient configure

ike start

test multiclient connect""" % script_var


##########################################################################

script_var['rad_neg_004_xpressvpn'] = """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients        9 
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context)s
test multiclient set max-concurrent    9
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
test multiclient set delay 5000
test multiclient configure

ike start

test multiclient connect""" % script_var


##########################################################################

script_var['rad_neg_005_xpressvpn'] =  """
ike log            stdout off
alias AUTH         eap

ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show

ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_phy_ip2)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients        4
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context)s
test multiclient set max-concurrent    9
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
test multiclient set delay 20000
test multiclient configure

ike start

test multiclient connect""" % script_var



##########################################################################

script_var['rad_neg_006_xpressvpn'] = script_var['rad_neg_005_xpressvpn']

##########################################################################

##########################################################################
#
# 	AAA HA testcase configuratuions
#
##########################################################################

##########################################################################



##########################################################################
 

##########################################################################


#########################################################################################
script_var['add_ip_takama'] = """

max_count=11

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


script_var['deb_ena_ssx'] = """
conf
context %(context)s
debug module iked all
debug module aaad all
exit
logg console
end
context %(context)s
""" % script_var



###############################################################################












