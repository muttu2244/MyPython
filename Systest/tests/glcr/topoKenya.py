""" Topology file for ACL test setup. """ 
# SSX box, lihue
ssx= {'ip_addr':'kenya-mc-con','username':'joe@local','password':'joe','name':'kenya-mc-con'}
#ssx1= {'ip_addr':'10.10.10.25','username':'joe@local','password':'joe'}
#xpress vpn client, tornado

linux={'ip_addr':'hutch','user_name':'regress','password':'gleep7','interface':'e2'} #express VPN
linux1={'ip_addr':'takama','user_name':'regress','password':'gleep7','interface':'e2'} #Radius Server
linux2={'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'e2'} #express VPN


#cisco = {'ip_addr':'10.10.10.120','username':'stoke','password':'stoke','name':'almatti'}
cisco = {'ip_addr':'c4900m-15-con','username':'stoke','password':'stoke'}
#xpress_vpn = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}
#xpress_vpn1 = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e2'}

# Connectivity between easter and tornado
#p1_ssx_xpressvpn= ["3/0","eth2"]


#Linux connectivity
p_cisco_linux  = ["2/8","eth2"]
p_cisco_linux1 = ["2/11","eth2"]
p_cisco_linux2 = ["2/12","eth2"]

#Topology connectivity for 3rd card
p_tr_active2_ssx_cisco_slot3     = ["3/1","1/4"]
p_tr_stdby2_ssx_cisco_slot4      = ["4/1","1/6"]
p_sr_active2_ssx_cisco_slot2	 = ["2/1","1/2"]
p_sr_stdby2_ssx_cisco_slot4	 = ["4/0","1/5"]

#Topology connectivity for 2nd card
p_tr_active1_ssx_cisco_slot2     = ["2/0","1/3"]
p_tr_stdby1_ssx_cisco_slot4      = ["4/0","1/5"]

p_sr_active1_ssx_cisco_slot3	 = ["3/0","1/1"]
p_sr_stdby1_ssx_cisco_slot4      = ["2/1","1/2"]
