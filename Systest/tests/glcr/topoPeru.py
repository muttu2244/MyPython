""" Topology file for ACL test setup. """ 
# SSX box, lihue
ssx= {'ip_addr':'peru','username':'joe@local','password':'joe','name':'peru-mc-con'}
#ssx1= {'ip_addr':'10.10.10.25','username':'joe@local','password':'joe'}
#xpress vpn client, tornado

linux={'ip_addr':'qa-radxpm-11','user_name':'regress','password':'gleep7','interface':'e3'} #express VPN
#phy_linux={'ip_addr':'10.1.1.112','user_name':'regress','password':'gleep7'} #physical ip addr of ganga
linux1={'ip_addr':'qa-radxpm-12','user_name':'regress','password':'gleep7','interface':'e1'} #Radius Server
linux2={'ip_addr':'iceman','user_name':'regress','password':'gleep7','interface':'e2'} #express VPN


#cisco = {'ip_addr':'10.10.10.120','username':'stoke','password':'stoke','name':'almatti'}
cisco = {'ip_addr':'c4900m-14-con','username':'stoke','password':'stoke'}
#xpress_vpn = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]


#Linux connectivity
p_cisco_linux  = ["2/5","eth3"]
p_cisco_linux1 = ["2/3","eth1"]
p_cisco_linux2 = ["2/12","eth2"]

#Topology connectivity for 3rd card
p_tr_active2_ssx_cisco_slot3     = ["3/0","1/2"]
p_tr_stdby2_ssx_cisco_slot4      = ["3/1","1/4"]
p_sr_active2_ssx_cisco_slot2	 = ["2/1","1/3"]
p_sr_stdby2_ssx_cisco_slot4	 = ["4/0","1/8"]

#Topology connectivity for 2nd card
p_tr_active1_ssx_cisco_slot2     = ["2/0","1/1"]
p_tr_stdby1_ssx_cisco_slot4      = ["4/0","1/8"]

p_sr_active1_ssx_cisco_slot3	 = ["3/0","1/2"]
p_sr_stdby1_ssx_cisco_slot4      = ["4/1","1/5"]
