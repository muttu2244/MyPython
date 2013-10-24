""" Topology file for ACL test setup. """ 
# SSX box, lihue
ssx= {'ip_addr':'nandi-mc-con','username':'joe@local','password':'joe','name':'nandi'}
ssx1= {'ip_addr':'10.10.10.25','username':'joe@local','password':'joe'}
#xpress vpn client, tornado

linux={'ip_addr':'ganga','user_name':'regress','password':'gleep7','interface':'e3'} #express VPN
phy_linux={'ip_addr':'10.10.10.101','user_name':'regress','password':'gleep7'} #physical ip addr of ganga
linux1={'ip_addr':'godavari','user_name':'regress','password':'gleep7','interface':'e2'} #Radius Server
linux2={'ip_addr':'krishna','user_name':'regress','password':'gleep7','interface':'e3'} #express VPN


#cisco = {'ip_addr':'10.10.10.120','username':'stoke','password':'stoke','name':'almatti'}
cisco = {'ip_addr':'10.10.10.120','username':'stoke','password':'stoke'}
#xpress_vpn = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]


#Linux connectivity
p_cisco_linux  = ["0/44","eth3"]
p_cisco_linux1 = ["0/43","eth1"]
p_cisco_linux2 = ["0/5","eth3"]

#Topology connectivity for 3rd card
p_tr_active2_ssx_cisco_slot3     = ["3/0","0/25"]
p_tr_stdby2_ssx_cisco_slot4      = ["4/1","0/20"]
p_sr_active2_ssx_cisco_slot2	 = ["2/1","0/19"]
p_sr_stdby2_ssx_cisco_slot4	 = ["4/1","0/20"]

#Topology connectivity for 2nd card
p_tr_active1_ssx_cisco_slot2     = ["2/0","0/17"]
p_tr_stdby1_ssx_cisco_slot4      = ["4/0","0/16"]

p_sr_active1_ssx_cisco_slot3	 = ["3/2","0/29"]
p_sr_stdby1_ssx_cisco_slot4      = ["4/3","0/22"]
