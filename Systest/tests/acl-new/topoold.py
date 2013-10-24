""" Topology file for IKEv2 test setup. """


# SSX box, lihue
ssx= {'ip_addr':'aruba-mc-con','username':'reddy@local','password':'reddy123'}
#ssx= {'ip_addr':'samoa-mc-con','username':'reddy@local','password':'reddy123'}




#xpress vpn client, tornado

linux={'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'}
xpress_vpn = {'ip_addr':'tornado','user_name':'regress','password':'gleep7','interface':'e1'}
xpress_vpn1 = {'ip_addr':'tornado','user_name':'regress','password':'gleep7','interface':'e1'}
###########################################################################

# Connectivity between easter and tornado
p1_ssx_xpressvpn= ["2/1","eth1"]
# Connectivity between easter and tornado
p1_ssx_xpressvpn1 = ["2/1","eth1"] 

ssx1_port="2:1"
