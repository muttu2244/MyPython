""" Topology file for IKEv2 test setup. """


# SSX box, lihue
ssx= {'ip_addr':'qa-tmp2-con','username':'reddy@local','password':'reddy123'}
#ssx= {'ip_addr':'samoa-mc-con','username':'reddy@local','password':'reddy123'}




#xpress vpn client, tornado

linux={'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}
xpress_vpn = {'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}
xpress_vpn1 = {'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}
###########################################################################

# Connectivity between easter and tornado
p1_ssx_xpressvpn= ["3/0","eth2"]
# Connectivity between easter and tornado
p1_ssx_xpressvpn1 = ["3/0","eth2"] 

p1_ssx_linux1 = ["3/0","eth2"]

ssx1_port="3:0"
ssx2_port="3/0"
linux_iface="eth2"
