
""" DOS_ATTACKS Topology Information """

'''
# SSX1 (lihue-mc-con)

ssx1 = { 'ip_addr'   : 'easter-mc-con', 
	'user_name': 'joe@local',
	'password' : 'joe123' }


#Linux Client (cyclops)
linux1={'ip_addr':'iceman',
	'ip_addr_snmp':'iceman',
	'user_name':'regress',
	'password':'gleep7'}
linux2={'ip_addr':'ituni',
        'user_name':'regress',
        'password':'gleep7'}
#NetScreen ( qa-ns4-con)
ns={'ipaddr':'qa-ns4-con',
        'user_name': 'netscreen',
        'password' : 'netscreen' }

#xpress vpn client, tornado 
xpressvpn1 = {'ip_addr':'ituni',
                'user_name':'regress',
                'password':'gleep7'}
#_____________________________________________________________________________________

#Connectivity b/w SSX  and LINUX.
p1_ssx_linux1 = ["2/0", "eth1"]
topo2=(["vgroup","easter:2:0","iceman:e1"])

#Connectivity b/w SSX  and NS5
topo3=(["vgroup","easter:2:1","qa-ns4:0"])

#Connectivity b/w SSX and XPRESSVPN
p1_ssx1_xpressvpn1 = ["2/1","eth1"]
topo1=(["vgroup","easter:2:1","ituni:e1"])

#_____________________________________________________________________________________

ssx_mgmt_ip_addr = "10.3.255.31"

#client Access type
cli_access_type = "console"
#vgroup code
vgroup_cfg_dos = " %s:%s %s:%s" % ("easter","2:0", "iceman", "e1")
vgroup_cfg_dos1 = "%s:%s %s:%s" % ("easter", "2:1", "ituni", "e1")
vgroup_cfg_dos2 = "%s:%s %s:%s" % ("easter", "2:1", "qa-ns4", "e0")

'''
######################################################################################
############## use lines below for regression
######################################################################################
ssx1 = { 'ip_addr'   : 'gabbar-mc-con',
        'user_name': 'joe@local',
        'password' : 'joe' }


#Linux Client (qa-radxpm-11)
linux1={'ip_addr':'periyar',
        'ip_addr_snmp':'10.10.10.125',
        'user_name':'regress',
        'password':'gleep7'}
linux2={'ip_addr':'vansadhara',
        'user_name':'regress',
        'password':'gleep7'}
#NetScreen ( qa-ns4-con)
ns={'ipaddr':'qa-ns4-con',
        'user_name': 'netscreen',
        'password' : 'netscreen' }

#xpress vpn client, tornado
xpressvpn1 = {'ip_addr':'vansadhara',
                'user_name':'regress',
                'password':'gleep7'}
#_____________________________________________________________________________________

#Connectivity b/w SSX  and LINUX.
p1_ssx_linux1 = ["2/0", "eth2"]
topo2=(["vgroup","bahamas:4:0","bora:e1"])

#Connectivity b/w SSX  and NS5
topo3=(["vgroup","bahamas:3:1","qa-ns4:0"])

#Connectivity b/w SSX and XPRESSVPN
p1_ssx1_xpressvpn1 = ["2/1","eth8"]
topo1=(["vgroup","bahamas:3:1","huahine:e1"])

#_____________________________________________________________________________________

ssx_mgmt_ip_addr = "172.16.25.15"
ssx_ip_addr = "172.16.25.118"
#client Access type
cli_access_type = "console"
#vgroup code
vgroup_cfg_dos = " %s:%s %s:%s" % ("bahamas","4:0", "huahine", "e1")
vgroup_cfg_dos1 = "%s:%s %s:%s" % ("bahamas", "3:1", "bora", "e1")
vgroup_cfg_dos2 = "%s:%s %s:%s" % ("bahamas", "3:1", "qa-ns4", "e0")

