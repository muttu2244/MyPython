'''
""" Topology file for ACL test setup. """ 
# SSX box, lihue
ssx= {'ip_addr':'bahamas-mc-con','username':'reddy@local','password':'reddy123','name':'pronto'}

#xpress vpn client, tornado

xpress_vpn = linux={'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'eth2'}
linux1={'ip_addr':'cyclops','user_name':'regress','password':'gleep7','interface':'e2'}

#xpress_vpn = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]

p1_ssx_xpressvpn= p1_ssx_xpressvpn1 =p1_ssx_linux1 = ["2/2","eth2"]
p1_ssx_linux2 = ["2/1","eth1"]

ssx2_port=p1_ssx_linux1[0]
ssx1_port=ssx2_port.replace('/',':')
linux_iface=p1_ssx_linux1[1]

#vlan_cfg_acl="%s:%s %s:%s"%("bahamas","2:2","cali","e2")
#vlan_cfg_acl2="%s:%s %s:%s"%("bahamas","2:1","cyclops","e1")
'''


""" Topology file for Laurel """
# SSX box - DUT
ssx= {'ip_addr':'nepal-mc-con','username':'joe@local','password':'joe','name':'nepal'}
#xpress vpn client
xpress_vpn = linux={'ip_addr':'ituni','user_name':'regress','password':'gleep7','interface':'eth3'}
linux1={'ip_addr':'ebini','user_name':'regress','password':'gleep7','interface':'e1'}

#xpress_vpn = {'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]

# Connectivity between easter and tornado
#p1_ssx_xpressvpn1 = ["3/0","eth2"]

p1_ssx_xpressvpn= p1_ssx_xpressvpn1 =p1_ssx_linux1 = ["2/0","eth3"]
p1_ssx_linux2 = ["2/1","eth1"]

ssx2_port=p1_ssx_linux1[0]
ssx1_port=ssx2_port.replace('/',':')
#!/usr/bin/python2.5
linux_iface=p1_ssx_linux1[1]

#vlan_cfg_acl="%s:%s %s:%s"%("qa-tmp3","2:1","cali","e1")
#vlan_cfg_acl2="%s:%s %s:%s"%("qa-tmp3","2:2","ebini","e1")
#vgroup_new(vg_cfg)


