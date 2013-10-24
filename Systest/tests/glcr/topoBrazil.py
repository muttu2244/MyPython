""" Topology file for ACL test setup. """ 
# SSX box, lihue
ssx= {'ip_addr':'brazil-mc-con','username':'joe@local','password':'joe','name':'brazil'}
ssx1= {'ip_addr':'10.3.255.73','username':'joe@local','password':'joe'}
#xpress vpn client, tornado

linux={'ip_addr':'qa-radxpm-14','user_name':'regress','password':'gleep7','interface':'e4'} #express VPN
#phy_linux={'ip_addr':'10.1.1.38','user_name':'regress','password':'gleep7'} #physical ip addr of ganga
linux1={'ip_addr':'qa-radxpm-15','user_name':'regress','password':'gleep7','interface':'e4'} #Radius Server
#linux2={'ip_addr':'qa-radxpm-15','user_name':'regress','password':'gleep7','interface':'e4'} #express VPN


#cisco = {'ip_addr':'10.10.10.120','username':'stoke','password':'stoke','name':'almatti'}
cisco = {'ip_addr':'c4900m-4-con','username':'stoke','password':'stoke'}
#xpress_vpn = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]


#Linux connectivity
p_cisco_linux  = ["2/7","eth4"]
p_cisco_linux1 = ["2/8","eth4"]
#p_cisco_linux2 = ["2/7","eth1"]

#Topology connectivity for 3rd card
p_tr_active2_ssx_cisco_slot3     = ["3/0","1/3"]
p_tr_stdby2_ssx_cisco_slot4      = ["4/1","1/6"]
p_sr_active2_ssx_cisco_slot2	 = ["2/1","1/2"]
p_sr_stdby2_ssx_cisco_slot4	 = ["4/1","1/6"]

#Topology connectivity for 2nd card
p_tr_active1_ssx_cisco_slot2     = ["2/0","1/1"]
p_tr_stdby1_ssx_cisco_slot4      = ["4/0","1/5"]

p_sr_active1_ssx_cisco_slot3	 = ["3/0","1/3"]
p_sr_stdby1_ssx_cisco_slot4      = ["4/1","1/6"]
