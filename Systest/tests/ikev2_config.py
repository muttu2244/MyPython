import topo 

script_var = {}

# SSX vars
script_var['context_name'] = 'india-test'
script_var['context_name1'] = 'india-test1'
script_var['max_session'] = '10000'
script_var['ses_name'] = 'ikev2'
script_var['dns_prmry'] = '172.16.24.171'
script_var['dns_scndry'] = '172.16.24.172'
script_var['dns_prmry_default'] = '20.1.1.2'
script_var['dns_scndry_default'] = '20.1.1.3'
script_var['timeout_abs'] = '7200'
script_var['svr_port'] = '1812'
script_var['svr_key'] = 'topsecret'
script_var['ip_pool'] = '6.6.2.1'
script_var['no_ip_pool'] = '1024'
script_var['ph1_name'] = 'ph1_eap_crypto_001'
script_var['ph2_name'] = 'ph2_cust_crypt_001'
script_var['hard_lifetime_ph1'] = '3600'
script_var['hard_lifetime_ph2'] = '3600'
script_var['soft_lifetime_ph1'] = '3000'
script_var['soft_lifetime_ph2'] = '120'
script_var['adm_dst1'] = '10'
script_var['adm_dst2'] = '20'
script_var['ps_key'] = '12345'
script_var['count'] = '3'

# Ip Adresses to be used
script_var['rad_server_ip_linux'] = '10.1.1.2'
script_var['rad_server_ip_linux/mask'] = '10.1.1.2/24'
script_var['rad_server_ip_ssx'] = '10.1.1.1'
script_var['rad_server_ip_ssx/mask'] = '10.1.1.1/24'
script_var['ike_client_ip_linux'] = '19.1.1.1'
script_var['ike_client_ip_linux/mask'] = '19.1.1.1/24'
script_var['ike_client_ip_ssx'] = '19.1.1.2'
script_var['ike_client_ip_ssx/mask'] = '19.1.1.2/24'
script_var['ses_lo_ip'] = '5.5.5.5'
script_var['ses_lo_ip/mask'] = '5.5.5.5/32'
script_var['lo_ip'] = '95.1.1.1'
script_var['lo_ip/mask'] = '95.1.1.1/32'
script_var['vlanid'] = '1950'
script_var['vlanid1'] = '1850'
#script_var['red_port2_vlan'] = '1750'
#script_var['red_port3_vlan'] = '1650'
#script_var['red_port4_vlan'] = '1550'
#script_var['lo0_ip'] = '10.10.10.10'
#script_var['lo0_ip/mask'] = '10.10.10.10/32'
#script_var['area_id1'] = '10'

#Routes Info vars
script_var['client_route'] = '19.1.1.0/24'
script_var['ses_route'] = '6.6.2.0/24'
script_var['svr_route'] = '10.1.1.0/24'
script_var['ses_lo_route'] = '95.1.1.0/24'
script_var['ses_route1'] = '5.5.5.0/24'

#Getting port info from topo file...
script_var['infc_srvr_port']=topo.srvr_port
script_var['infc_clnt_port']=topo.clnt_port

#  ******************************************************************************** #

### 			IKEV2 Session Configurations 			###

#  ******************************************************************************** #

script_var['common_config'] =  """
end
context local
config
aaa global profile
 default-domain authentication %(context_name)s
 exit
 context %(context_name)s
  aaa profile
  session accounting none
  session authentication radius
  service authorization local
  max-session %(max_session)s
  exit
 session name %(ses_name)s
  dns primary %(dns_prmry)s
  dns secondary %(dns_scndry)s
  ip address pool
  ip netmask 255.255.255.255
  exit
 session profile default
 dns primary %(dns_prmry_default)s
 dns secondary %(dns_scndry_default)s
 ip address pool
 ip netmask 255.255.255.255
 timeout absolute %(timeout_abs)s
 exit
radius session authentication profile
 server %(rad_server_ip_linux)s port %(svr_port)s key %(svr_key)s
 exit
 ip pool %(ip_pool)s %(no_ip_pool)s
 interface intf1
  arp arpa
  ip unreachables
  ip address %(ike_client_ip_ssx/mask)s
  exit
 interface ses_int session loopback
  ip session-default
  ip address %(ses_lo_ip/mask)s
  exit
 interface lo0 loopback
  ip address %(lo_ip/mask)s
  exit
 interface rad
  arp arpa
  ip address %(rad_server_ip_ssx/mask)s
  exit
 interface untagged1
  arp arpa
  ip address 10.1.2.3/24
  exit
 interface untagged2
  arp arpa
  ip address 20.1.2.3/24
  exit
 ipsec policy ikev2 phase1 name %(ph1_name)s
  custom
   gw-authentication psk %(ps_key)s 
   peer-authentication eap 
   hard-lifetime %(hard_lifetime_ph1)s secs
   soft-lifetime %(soft_lifetime_ph1)s secs
   encryption aes128
   hash sha-1
   d-h group5
   prf sha-1
   exit
  exit
 ipsec policy ikev2 phase2 name %(ph2_name)s
  custom
   hard-lifetime %(hard_lifetime_ph2)s secs
   soft-lifetime %(soft_lifetime_ph2)s secs
   encryption aes128
   hash sha-1
   pfs group2
   exit
  exit
 exit """%script_var
#print script_var['common_config']

script_var['port_config_normal'] = """
port ethernet %s
  !vlan %s
  bind interface intf1 india-test
   ipsec policy ikev2 phase1 name ph1_eap_crypto_001
   ipsec policy ikev2 phase2 name ph2_cust_crypt_001
   exit
  service ipsec
   enable
 exit
port ethernet %s
 bind interface rad india-test
  exit
 enable
 exit"""

script_var['port_config_tagged'] = """
port ethernet %s dot1q
 vlan %s
  bind interface intf1 india-test
   ipsec policy ikev2 phase1 name ph1_eap_crypto_001
   ipsec policy ikev2 phase2 name ph2_cust_crypt_001
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %s
 bind interface rad india-test
  exit
 enable
 exit"""


script_var['port_config_untagged'] = """
port ethernet %s dot1q
 vlan %s untagged
  bind interface intf1 india-test
   ipsec policy ikev2 phase1 name ph1_eap_crypto_001
   ipsec policy ikev2 phase2 name ph2_cust_crypt_001
   exit
  service ipsec
  exit
 enable
 exit
port ethernet %s
 bind interface rad india-test
  exit
 enable
 exit"""



################ Configuration files on client end #################################
'''
script_var['autoexec'] = """
### this is the new configuration format.
ike listen %(ike_client_ip_linux)s 500
ike listen %(ike_client_ip_linux)s 4500
ike start

### IKE debugging
ike log                 stdout off
#ike log                 file on
#ike log                 filename xpressvpn.log
#ike decode              full
#ike debug               off

ike eap sim tripletfile simtriplets.txt

### IPSec debugging
#ipsec pktdump           error full
#ipsec log               debug

alias LHOST %(ike_client_ip_linux)s             #this is the physical IP of the XpressVPN client PC
alias RHOST %(lo_ip)s                          #this is the physical IP of the SSX
alias IKE_SEL ${LHOST},$(RHOST}
ike ph1 addx    IKE_SEL  main eap %(ps_key)s aes-128 sha1 5 12000 v2
ike ph1 options IKE_SEL nat-t
ike ph1 options IKE_SEL  mode-cfg-client
ike ph1 options IKE_SEL  mobike mobike-cookie2-size=32
ike ph1 options IKE_SEL  mobike-addl-address=192.168.1.103
ike ph1 options IKE_SEL  mobike-addl-address=192.168.1.104

ike ph1 myid    IKE_SEL  userfqdn 16502102800650210@%(context_name)s 

ike ph2 addx    %(ses_route)s 0.0.0.0/0 0 IKE_SEL esp tunnel aes-128 sha1 2 1200

ike connect any
  """%script_var

'''

script_var['autoexec'] = """

ike log            stdout off
ike listen any  500
ipsec addr add  %(ike_client_ip_linux)s 255.255.0.0 1
ipsec addr show
ike eap sim tripletfile simtriplets.txt

test multiclient set remote           %(lo_ip)s 500
test multiclient set local            %(ike_client_ip_linux)s   500
test multiclient set numclients       1
test multiclient set ph1 exchange      ikev2
test multiclient set ph1 auth          eap
test multiclient set ph1 encr          aes-128
test multiclient set ph1 hash          sha1
test multiclient set ph1 dh            5
test multiclient set ph1 life          12000
test multiclient set ph1 psk           12345
test multiclient set ph1 myid          userfqdn 16502102800650210@%(context_name)s
test multiclient set max-concurrent    2
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

"""%script_var


