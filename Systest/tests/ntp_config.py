import topo

script_var = {}
var_dict={
	  'cntxt1'     	: "local"  ,
	  'context_name'     : "ntptest"  ,
	  'infc_r1_ip/m':"7.1.1.10/24",
	  'infc_r1_ip':"7.1.1.10",
	  'infc_linux1_ip/m':"7.1.1.1/24",
	  'infc_linux1_ip':"7.1.1.1",
	  'infc_r2_ip/m':"25.1.1.10/24",
	  'infc_linux2_ip/m':"25.1.1.1/24",
	  'infc_linux2_ip':"25.1.1.1",
	  'secondary_server':"10.10.10.102", 
	  'intf_lo1_ip/mask':"17.17.17.20/32",
	  'intf_lo1_ip':"17.17.17.20",

        }

#SSX port
var_dict['infc_r1_port'] = topo.p1_linux_ssx[1]
var_dict['infc_r2_port'] = topo.p2_linux_ssx[1]

#SSX management ip.
var_dict['ssx_mgmt_ip_addr'] = topo.ssx_mgmt_ip_addr
var_dict['ssx_mgmt_ip_addr_mask'] = topo.ssx_mgmt_ip_addr + "/" + "24"

var_dict['key'] = '3'
var_dict['version'] = '3'

var_dict['text'] = 'a1'
var_dict['wrong_ip'] = '234.34.34.34'
var_dict['long_key'] = '4294967296'
var_dict['key1'] = '2'
var_dict['version1'] = '2'
var_dict['wrong_version'] = '0'
max_server = ["35.1.1.1", "35.1.1.2" , "35.1.1.3" , "35.1.1.4" , "35.1.1.5" , "35.1.1.6" , "35.1.1.7" , "35.1.1.8" , "35.1.1.9"]

#########################################################################################
script_var['common_ssx'] = """
context %(cntxt1)s

interface mgmt management
  arp arpa
  ip address 10.3.255.103/24
  exit
 ip route 0.0.0.0/0 10.3.255.1
 exit
port ethernet 0/0
 bind interface mgmt local
exit
enable
exit

""" %(var_dict)
######################################################################################################

script_var['NTP_FUN_001']="""

context %(cntxt1)s
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s
exit
exit
no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

######################################################################################################
script_var['NTP_CLI_005']=script_var['NTP_FUN_001']
script_var['NTP_FUN_008']=script_var['NTP_FUN_001']
script_var['NTP_FUN_022']=script_var['NTP_FUN_001']
script_var['NTP_FUN_018']=script_var['NTP_FUN_001']
######################################################################################################

script_var['NTP_FUN_002']="""

context %(context_name)s
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s
exit
exit
no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(context_name)s
 exit
enable
exit """ %(var_dict)

#################################################################################################
script_var['NTP_FUN_003']="""

context %(cntxt1)s

 interface ntp
  arp arpa
  ip address %(infc_r2_ip/m)s
  exit
 interface ntp_1
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit


ntp profile
server %(infc_linux2_ip)s 
server %(infc_linux1_ip)s prefer
exit
exit
no port ethernet %(infc_r1_port)s
port ethernet %(infc_r1_port)s
 bind interface ntp_1 %(cntxt1)s
 exit
enable
exit
no port ethernet %(infc_r2_port)s
port ethernet %(infc_r2_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

#####################################################################################################
script_var['NTP_NEG_005'] = script_var['NTP_FUN_003']
######################################################################################################
######################################################################################################


script_var['NTP_FUN_004']="""

context %(cntxt1)s

 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s
exit
exit
no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

###############################################################


################################################################################################
script_var['NTP_FUN_006']="""

context local
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit
 


ntp profile
server %(infc_linux1_ip)s  key %(key)s
exit
exit

ntp-global global profile
authenticate
authentication-key %(key)s md5 stoke
trusted-key %(key)s
exit
no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

########################################################################
script_var['NTP_FUN_010']="""

context local
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s  key %(key)s
exit
exit

ntp-global global profile
authenticate
authentication-key %(key)s md5 stoke
trusted-key %(key)s
exit
no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)


###################################################################################


script_var['NTP_FUN_011']= script_var['NTP_FUN_006']

######################################################################################
script_var['NTP_FUN_020']= """

context %(cntxt1)s
 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s  key %(key)s
exit
exit

no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

###################################################################################


script_var['NTP_FUN_011']= script_var['NTP_FUN_006']

######################################################################################

script_var['NTP_FUN_012'] = script_var['NTP_FUN_001']

############################################################################

script_var['NTP_FUN_013'] = script_var['NTP_FUN_010']

#############################################################################
#################################################################################################
script_var['NTP_FUN_016']="""

context %(cntxt1)s

 interface ntp
  arp arpa
  ip address %(infc_r2_ip/m)s
  exit
 interface ntp_1
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit


ntp profile
server %(infc_linux2_ip)s
server %(infc_linux1_ip)s
exit
exit
no port ethernet %(infc_r1_port)s
port ethernet %(infc_r1_port)s
 bind interface ntp_1 %(cntxt1)s
 exit
enable
exit
no port ethernet %(infc_r2_port)s
port ethernet %(infc_r2_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

#####################################################################################################

script_var['NTP_FUN_007']="""
context local
 exit
context %(cntxt1)s
 interface mgmt management
  arp arpa
  ip address 10.3.255.33/24
  exit

 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit
ip route 172.17.3.0/24 10.3.255.1
 ip route 10.3.5.0/24 10.3.255.1

ntp profile
server %(infc_linux1_ip)s
exit
exit

!clock  timezone PST -8 DST 1 monthformat 3 2 0 2 00 11 1 1 1 59
port ethernet 0/0
 bind interface mgmt local
  exit
 enable
 exit

no port ethernet %(infc_r1_port)s 
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)
#################################################################################################
script_var['NTP_CLI_002']="""

context %(cntxt1)s

 interface ntp
  arp arpa
  ip address %(infc_r2_ip/m)s
  exit

ntp profile
server %(infc_linux2_ip)s
exit
exit
no port ethernet %(infc_r2_port)s
port ethernet %(infc_r2_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

#################################################################################################
script_var['NTP_CLI_015']= script_var['NTP_CLI_002']
script_var['NTP_CLI_009']= script_var['NTP_CLI_002']
####################################################################################################

script_var['NTP_NEG_001']="""

context %(cntxt1)s

 interface ntp
  arp arpa
  ip address %(infc_r1_ip/m)s
  exit

ntp profile
server %(infc_linux1_ip)s
exit
exit
no port ethernet %(infc_r1_port)s
port ethernet %(infc_r1_port)s
 bind interface ntp %(cntxt1)s
 exit
enable
exit """ %(var_dict)

####################################################################################################
script_var['NTP_NEG_002']= script_var['NTP_NEG_001']
#####################################################################################################
####################################################################################################
script_var['NTP_NEG_003']= script_var['NTP_NEG_001']
script_var['NTP_NEG_004']= script_var['NTP_NEG_001']
#####################################################################################################

script_var['ntp.conf'] = """
restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery

restrict 127.0.0.1
restrict -6 ::1


server 66.187.233.4

driftfile /var/lib/ntp/drift

keys /etc/ntp/keys """ 

##################################################################################################
#####################################################################################################

script_var['ntp_lo.conf'] = """
restrict default kod nomodify notrap nopeer noquery
restrict -6 default kod nomodify notrap nopeer noquery

restrict 127.0.0.1
restrict -6 ::1


server 66.187.233.4 prefer
server 127.0.0.1

driftfile /var/lib/ntp/drift

keys /etc/ntp/keys """ 

##################################################################################################


script_var['ntp_configuration'] = """

keys /etc/ntp/keys
trustedkey %(key)s """ %(var_dict)

###########################################################################
