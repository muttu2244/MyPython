#SSX Variables:

#**************
import topo 
script_var={}

#SSX Variables:
#**************
script_var['context_name'] = 'test'
script_var['xauth_user']=       'user1'
script_var['xauth_passwd']=     '123user1'

script_var['ssx_max_session'] =23
script_var['ssx_custom_profile']=1000
script_var['ip_netmask']        ="255.255.255.255"
script_var['psk']=              '12345'
script_var['ssx_int_name']=     'untrust'
script_var['ssx_ip_addr/m'] = '16.1.1.100/16'
script_var['ssx_ip_addr'] = '16.1.1.100'

script_var['ssx_sess_iface1_ip'] = '4.4.4.4'
script_var['ssx_sess_iface1_ip_mask'] = '4.4.4.4/32'
script_var['ssx_ip_pool'] = '7.7.2.1 10'

#Variables regarding IKEV1 session.
script_var['ssx_ses_ip']=       '11.11.11.1'
script_var['ssx_ses_ip_mask']=  '11.11.11.1/24'
script_var['ns_ses_ip']=        '11.11.11.2'
script_var['ns2_ses_ip']=       '11.11.11.3'

#SSX ports
script_var['ssx_port'] = topo.p1_ssx_linux1[0]
script_var['ssx_port1'] = topo.p1_ssx_linux1[0]
script_var['ssx_port2'] = topo.p1_ssx1_xpressvpn1[0]
script_var['count'] = '1'

#LINUX Variables:
#**************

script_var['linux1_ip_addr/m'] = '16.1.1.1/16'
script_var['linux1_ip_addr'] = '16.1.1.1'
script_var['linux1_ip_addr_mask'] ="255.255.0.0"


#XPRESS-VPN Variables:
#**************
#script_var['xpress_phy_iface1'] = '17.1.2.1/16'
#script_var['xpress_phy_iface1_ip'] = '17.1.2.1'
#script_var['xpress_phy_iface1_ip_mask'] = '17.1.2.1/16'
#script_var['xpress_phy_iface1_mask']="255.255.0.0"
#script_var['xpress_phy_iface2_ip'] = '17.1.2.2'
#script_var['ssx_phy_iface1_ip'] = '17.1.1.2'
#script_var['ssx_phy_iface1_ip_mask'] = '17.1.1.2/16'
script_var['ssx_phy_iface1_ip'] = '17.1.1.2'
script_var['ssx_phy_iface1_ip_mask'] = '17.1.1.2/16'
script_var['ssx_phy_iface1_ip_network_mask'] = '17.1.0.0/16'
script_var['ssx_ip_pool_start'] = '7.7.2.1'
script_var['ssx_ip_pool'] = '7.7.2.1 5'

script_var['ssx_ip_pool_network'] = '7.7.2.0/24'

#script_var['ssx_sess_iface1_name'] = 'vpn'
script_var['ssx_sess_iface1_ip'] = '4.4.4.4'
script_var['ssx_sess_iface1_ip_mask'] = '4.4.4.4/32'
script_var['xpressvpn1_phy_iface1_ip'] = "17.1.1.1"
script_var['xpressvpn1_phy_iface1_ip_mask'] = "17.1.1.1/16"
script_var['xpress_phy_iface1_ip'] = '17.1.2.1'
script_var['xpress_phy_iface1_ip_mask'] = '255.255.0.0'


#NS-4GT Variables:
#*****************

script_var['ns_phy_ip']='16.1.2.1'
script_var['ike_mode']=         'Main'
script_var['ns_phy_ip_mask']=   '16.1.2.1/16'

#Variables for SSH.
script_var['password']     = 'user1'
script_var['user']=          'user1'
ssh_user=script_var['user']+"@"+script_var['context_name']
ssx_name_list=topo.ssx1["ip_addr"].split("-")
ssx_name=ssx_name_list[0]
ssh_user_pass   = script_var['password']


script_var['ssx_phy_ip']     ='10.3.255.1'

script_var['ssx_phy_ip_mask'] = topo.ssx_mgmt_ip_addr + "/" + "24"


#SSX variables used in SNMP configuration:
#******************************************


script_var['ssx_mgm_ip_addr']=topo.ssx_mgmt_ip_addr
script_var['ssx1_ip_addr']=topo.ssx_ip_addr
#This is the snmp address used in the configuration
script_var['linux1_mgm_ip_addr']=topo.linux1['ip_addr_snmp']



#These are the various community names used in SNMP for 3 versions
script_var['snmp_com1']='snmp_com1'
script_var['snmp_com2']='snmp_com2'

#These are the various parameter names used in corresponding versions
script_var['param2_ver3']='v3-param2'
script_var['param_ver2']='v2c-param'
script_var['param1_ver3']='v3-param1'
script_var['param_ver1']='v1-param'

#These are the various group names used in various versions
script_var['grp_ver2']='v2c-group'
script_var['grp_ver1']='v1-group'
script_var['grpnoauth_ver3']='v3-group-noauth'
script_var['grpauth_ver3']='v3-group-auth-priv'

#These are the user names used in version3
script_var['user2_ver3']='v3-user2'
script_var['user1_ver3']='v3-user1'

#These are the various snmp tools used int the configuration
script_var['ntytarget1']='snmp-linux'
script_var['ntytarget2']='snmp-linux1'
script_var['ntytarget3']='snmp-linux2'
script_var['ntytarget4']='snmp-linux3'

#This is the context name used
script_var['cntx_name']='local'
script_var['invalid_cntx_name']='asdef1234'
script_var['invalid_grp_ver2']='groupinvalid'
script_var['invalid_comm_name']='Snmp_com1'

#These are the privilizes used in various levels of version3 
script_var['level_name1']='noAuthNoPriv'
script_var['level_name2']='authPriv'
script_var['oid']='sysDescr.0'
script_var['oid1']='sysORDescr.1'

#These are the values passed in the script of snmp_getbulk
i1=script_var['i']='10'

#PPOE variables

script_var['absolute_timeout']=         '80'
script_var['ip_pool']=                  '8.8.8.1 100'
script_var['interface_ip2']=            '6.6.6.1/32'

###################################################

script_var['common']="""context %(context_name)s
 user name %(user)s
  password %(password)s
  priv-level administrator
  exit
 interface admin management
 arp arpa
  ip address %(ssx_phy_ip_mask)s
  exit
 ip route 0.0.0.0/0 %(ssx_phy_ip)s
 exit
port ethernet 0/0
 bind interface admin %(context_name)s
  exit
 enable
exit
exit
"""%script_var

#############################################################

script_var['common_ssx']= """
end
conf
context %(context_name)s
 domain pppoestoke advertise
aaa profile
 user authentication local
 session accounting none
 session authentication local
 service authorization local
exit
 session name session
 ip address pool
 password session123
exit
 ip pool %(ip_pool)s
 interface pppoe
 arp arpa
 ip address %(ssx_ip_addr/m)s
exit
 interface pppoe_session session loopback
 ip session-default
 ip address %(interface_ip2)s 
exit
exit """ % script_var

#####################################################
script_var['common_ssx_ikev2'] = """
end
conf
no context %(context_name)s
 !interface mgm management
 ! arp arpa
 ! ip address 10.3.255.22/24
 ! exit
 !ip route 10.3.5.0/24 10.3.255.1
 !exit
 !port ethernet 0/0
 !bind interface mgm india-test
 ! exit
 !enable
 !exit
context %(context_name)s
ip pool %(ssx_ip_pool)s
interface mobike
arp arpa
ip address %(ssx_phy_iface1_ip_mask)s
exit
interface vpn session loopback
ip session-default
ip address %(ssx_sess_iface1_ip_mask)s
exit
ip route 0.0.0.0/0 %(xpress_phy_iface1_ip)s
exit
""" % script_var


script_var['pppoe_fun_001_ssx'] = """
no port ethernet %(ssx_port)s 
port ethernet %(ssx_port)s 
bind interface pppoe %(context_name)s
exit
 service pppoe
 enable
exit
end  """ % script_var

#####################################################
script_var['dos_001'] = """
system hostname Aruba
ipsec global profile
 exit
context local
 user name admin
  password encrypted 321002020B
  priv-level administrator
  exit
 interface mgmt management
  arp arpa
  ip address 10.3.2.20/24
  exit
 interface eth2_0
  arp arpa
  ip address 30.1.1.254/24
  exit
 ip route 0.0.0.0/0 10.3.2.1
 exit
context test
 interface test1
  arp arpa
  ip address 16.1.1.100/16
  exit
 interface test2
  arp arpa
  ip address 30.1.1.10/16
  exit
 exit
port ethernet 0/0
 bind interface mgmt local
  exit
 enable
 exit
port ethernet %(ssx_port)s
 bind interface test1 test
  exit
 enable
 exit
port ethernet %(ssx_port1)s
 bind interface test2 test
  exit
 enable
 exit""" 


script_var['DOS_FUN_005'] = """
end
conf
no context test
context test
 interface test1
  arp arpa
  ip address %(ssx_ip_addr/m)s
exit
exit
no port ethernet %(ssx_port)s
port ethernet %(ssx_port)s dot1q
 vlan 1 untagged
 bind interface test1 test
  exit
 exit
 enable
 exit
 end
"""  %(script_var)


script_var['DOS_FUN_006'] = """
no context test
context test
aaa profile
  user authentication local
  session accounting none
  session authentication local
  exit
 session name test-session
 ip address 11.11.11.2
  ip netmask 255.255.255.255
  password encrypted 62465C1E16452450
  exit

interface untrust
  arp arpa
  ip address %(ssx_ip_addr/m)s
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
no port ethernet %(ssx_port)s
port ethernet %(ssx_port)s
bind interface untrust test
ipsec policy ikev2 phase1 name ph1
 ipsec policy ikev2 phase2 name ph2
exit
 service ipsec
 enable
 exit 

 """ %(script_var)

###########################################################

script_var['DOS_FUN_017'] = script_var['DOS_FUN_005']

###########################################################

script_var['DOS_FUN_024'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_026'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_027'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_028'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_034'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_040'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_013'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_016'] = script_var['DOS_FUN_005']

##########################################################

script_var['DOS_FUN_049'] = script_var['DOS_FUN_005']

##########################################################


script_var['DOS_FUN_076'] = """
configuration
context %(context_name)s
aaa profile
session accounting none
session authentication local
exit
session name test-session
ip address pool
password primesoft
exit

ipsec policy ikev2 phase1 name ph1-test1
custom
encryption aes128
hash sha-1
d-h group5
prf sha-1
gw-authentication psk 12345
peer-authentication psk
hard-lifetime 40 hours
exit
mobike
exit
exit
ipsec policy ikev2 phase2 name ph2-test1
custom
encryption triple-des
hash md5
pfs group2
hard-lifetime 40 hours
soft-lifetime 60 secs
exit
exit
exit
port ethernet %(ssx_port2)s
bind interface mobike %(context_name)s
ipsec policy ikev2 phase1 name ph1-test1
ipsec policy ikev2 phase2 name ph2-test1
exit
service ipsec
enable
exit
""" % script_var

###########################################################################

script_var['DOS_FUN_087'] = script_var['DOS_FUN_005']

##########################################################


##########################################
script_var['fun_002_xpressvpn1']="""
ike log            stdout off
ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_ip_addr)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          120
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn test-session@test
test multiclient set max-concurrent    2
test multiclient set incr-ph1-life     1

test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          3des
test multiclient set ph2 hash          md5
test  multiclient set ph2 dh           2
test multiclient set ph2 life          120
test multiclient set ph2-wild
test multiclient set delay 200
test multiclient configure

ike start

test multiclient connect """ %(script_var)

script_var['fun_002_xpressvpn']="""
ike log            stdout off
ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(ssx_ip_addr)s 500
test multiclient set local            %(xpress_phy_iface1_ip)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          psk
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          120
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn test-session@test
test multiclient set max-concurrent    2
test multiclient set incr-ph1-life     1

test multiclient set incr-local-addr    1
test multiclient set incr-remote-addr   0
test multiclient set ph2 proto         esp
test multiclient set ph2 encap         tunnel
test multiclient set ph2 encr          aes-128
test multiclient set ph2 hash          sha1
test  multiclient set ph2 dh           0
test multiclient set ph2 life          120
test multiclient set ph2-wild
test multiclient set delay 200
test multiclient configure

ike start

test multiclient connect """ %(script_var)
################################################################

script_var['fun_014_xpressvpn'] = """
ike log            stdout off
ike listen any  500
ipsec addr add  %(xpress_phy_iface1_ip)s  %(xpress_phy_iface1_ip_mask)s 1
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

""" % script_var

##########################################################################################3

script_var['common_ssx_for_ikev1']="""
end
conf
aaa global profile
 default-domain authentication %(context_name)s
 default-domain authorization %(context_name)s
 exit
context %(context_name)s
 aaa profile
  session authentication local
  service authorization local
  exit
 session name %(xauth_user)s
  ip address %(ns_ses_ip)s
    ip address pool
    ip netmask 255.255.255.255
  password %(xauth_passwd)s
  exit
 ip pool 11.11.11.11 19
 interface %(ssx_int_name)s
  arp arpa
  ip address %(ssx_ip_addr/m)s
  exit
 interface sub session
  ip session-default
  ip address %(ssx_ses_ip_mask)s
  exit
 exit

port ethernet %(ssx_port)s
 bind interface %(ssx_int_name)s %(context_name)s
 exit
 exit"""%script_var

##################################################################


#Netscreen-5GT common configuration:
#**********************************
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
set interface trust ip 192.168.1.10/24
set interface trust ip 192.168.1.10/24
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
set interface trust dhcp server service
set interface trust dhcp server auto
set interface trust dhcp server option gateway 192.168.1.1
set interface trust dhcp server option netmask 255.255.255.0
set interface trust dhcp server ip 192.168.1.33 to 192.168.1.126
set flow tcp-mss
unset flow no-tcp-seq-check
set flow tcp-syn-check
set console timeout 0
set hostname ns5gt

set pki authority default scep mode "auto"
set pki x509 default cert-path partial
set ike p1-proposal "p1" preshare group2 esp 3des sha-1 hour 8
set ike p2-proposal "p2" no-pfs esp null sha-1 hour 1
set ike gateway "v4gate" address %(ssx_ip_addr)s %(ike_mode)s outgoing-interface "untrust" local-address %(ns_phy_ip)s preshare %(psk)s proposal "p1"
set ike gateway "v4gate" xauth client any username %(xauth_user)s password %(xauth_passwd)s
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
exit            """%script_var

################################################################################


script_var['ikev1_fun_019_ssx']="""
context %(context_name)s
 session name %(ns_phy_ip)s
  password %(psk)s
  exit
 ipsec policy ikev1 phase1 name p11
  suite3 psk xauth-generic 300 secs 0 secs
  exit
 ipsec policy ikev1 phase2 name p21
  custom null sha-1 none 180 secs 0 secs
  exit
 exit

port ethernet %(ssx_port)s
 bind interface %(ssx_int_name)s %(context_name)s
  ipsec policy ikev1 phase1 name p11
  ipsec policy ikev1 phase2 name p21
  exit
 service ipsec
 enable
 exit
exit """ % script_var

#######################################################################3

script_var['ikev1_fun_019_ns5gt']="""
set ike p1-proposal "p1" preshare group2 esp 3des sha-1 seconds 480
set ike p2-proposal "p2" no-pfs esp null sha-1 seconds 240 """ %script_var

#######################################################################
#Loading SNMP Configuration:
#***************************

script_var['snmp_common_config']="""
end
conf
no snmp
snmp
 server
  exit
 view all
  oid internet include
  oid dod include
  oid private include
  oid stoke include
  oid enterprises include
  oid org include
  oid iso include
  exit
group %(grp_ver2)s
 context %(cntx_name)s sec-model v2c notify-view all read-view all
 exit
community 
 name %(snmp_com1)s group %(grp_ver2)s context %(cntx_name)s
 name %(snmp_com2)s group %(grp_ver1)s context %(cntx_name)s
 exit
group %(grp_ver1)s
 context %(cntx_name)s sec-model v1 notify-view all read-view all
 exit
notification
 notify
  name notify-inform tag-inform inform
  name notify-trap tag-trap trap
  exit
target-parameters
 name %(param_ver2)s sec-name %(snmp_com1)s sec-model v2c
 name %(param_ver1)s sec-name %(snmp_com2)s sec-model v1
 name %(param1_ver3)s sec-name %(user1_ver3)s sec-model usm noauth-nopriv
 name %(param2_ver3)s sec-name %(user2_ver3)s sec-model usm auth-priv
exit
notify-target
 name %(ntytarget1)s %(linux1_mgm_ip_addr)s tags tag-trap,tag-inform parameters %(param2_ver3)s timeout 10 retry 20
 name %(ntytarget2)s %(linux1_mgm_ip_addr)s tags tag-trap,tag-inform parameters %(param_ver2)s timeout 10 retry 20
 name %(ntytarget3)s %(linux1_mgm_ip_addr)s tags tag-trap,tag-inform parameters %(param1_ver3)s timeout 10 retry 20
 name %(ntytarget4)s %(linux1_mgm_ip_addr)s tags tag-trap,info-trap parameters %(param_ver1)s timeout 10 retry 20
 exit
exit
user %(user1_ver3)s
 sec-model usm auth-proto noauth group %(grpnoauth_ver3)s
 exit
group %(grpnoauth_ver3)s
 context %(cntx_name)s sec-model usm noauth-nopriv notify-view all read-view all
 exit
user %(user2_ver3)s
 sec-model usm auth-proto md5 auth-passw apass123 priv-proto des priv-passw vpass123 group %(grpauth_ver3)s
 exit
group %(grpauth_ver3)s
 context %(cntx_name)s sec-model usm noauth-nopriv notify-view all read-view all
 exit
exit """ % script_var

#############################################################################################################


#Running SNMPWALK in all the 3 versions:
#***************************************

script_var['snmp_walk']= """

snmpwalk -v 1 -c %(snmp_com2)s %(ssx_mgm_ip_addr)s 1 -C p > &
snmpwalk -v 2c -c %(snmp_com1)s %(ssx_mgm_ip_addr)s 1 -C p > &
snmpwalk -v 3 -u %(user2_ver3)s -l %(level_name2)s  -a MD5 -A apass123 -x DES -X vpass123 -n %(cntx_name)s %(ssx_ip_addr)s 1 -C p > & """ % script_var

######################################################################################################


script_var['pppoe_cnf_032_linux1'] = """
ETH=eth0

USER=root@stoke123

DEMAND=no

DNSTYPE=SERVER

PEERDNS=yes

DEFAULTROUTE=yes

CONNECT_TIMEOUT=60

CONNECT_POLL=2

ACNAME=

SERVICENAME=pppoestoke

CF_BASE='basename $CONFIG'
PIDFILE="/var/run/$CF_BASE-pppoe.pid"

CLAMPMSS=1412

LCP_INTERVAL=20
LCP_FAILURE=3

PPPOE_TIMEOUT=80

FIREWALL=NONE """ % script_var


##########################################################################################################################
