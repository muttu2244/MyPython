""" Topology file for CDR setup."""

'''
#**********************************************************************
#**************  U S E R    S E C T I O N  ****************************
#**********************************************************************
# SSX box, 
ssx = {'ip_addr':'salvador-mc-con','username':'joe@local','password':'joe123','name':'salvador'}
ssx_HA = {'ip_addr':'salvador','username':'joe@local','password':'joe123','name':'salvador'}

#xpress vpn client, bora & bora

linux =       {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}


xpress_vpn1 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}
xpress_vpn2 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'} 
xpress_vpn3 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}

xpress_vpn1_multi = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}
xpress_vpn2_multi = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e3'}
xpress_vpn3_multi = {'ip_addr':'cali','user_name':'regress','password':'gleep7','interface':'e1'}


# Connectivity between salvador and bora & hauhine
p1_ssx_xpressvpn1 = ["2/1","eth1"] 
p1_ssx_xpressvpn2 = ["3/0","eth3"] 
p1_ssx_xpressvpn3 = ["4/3","eth1"] 


p1_ssx_xpressvpn1_multi = ["2/1","eth1"] 
p1_ssx_xpressvpn2_multi = ["3/0","eth3"] 

ssx_vgroup = 	["2:1","eth1"] 
ssx_vgroup1 = 	["3:0","eth3"] 
ssx_vgroupHA = 	["2:1","eth1"] 

#**********************************************************************
'''

#%%%%%%%%%%%%+++++++++$$$$$$$$$$$$$^^^^^^^^^^@@@@@@@@@@@@***************


#**********************************************************************
#**************  R E G R E S S I O N    S E C T I O N  ****************
#**********************************************************************


# SSX box, 
ssx = {'ip_addr':'bahamas-mc-con','username':'joe@local','password':'joe123','name':'bahamas'}
ssx_HA = {'ip_addr':'bahamas','username':'joe@local','password':'joe123','name':'bahamas'}


#xpress vpn client, bora & bora

linux =       {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}

xpress_vpn1 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}
xpress_vpn2 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e2'} 
xpress_vpn3 = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}

xpress_vpn1_multi = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}
xpress_vpn2_multi = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e2'}
xpress_vpn3_multi = {'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}


# Connectivity between salvador and bora & hauhine
p1_ssx_xpressvpn1 = ["2/1","eth1"] 
p1_ssx_xpressvpn2 = ["3/1","eth2"] 
p1_ssx_xpressvpn3 = ["2/2","eth1"] 


p1_ssx_xpressvpn1_multi = ["2/1","eth1"] 
p1_ssx_xpressvpn2_multi = ["3/1","eth2"] 

ssx_vgroup =    ["2:1","eth1"] 
ssx_vgroup1 =   ["3:1","eth2"] 
ssx_vgroupHA =  ["2:1","eth1"] 

#**********************************************************************


#Vgrouping the Topology 
vlan_cfg_str="""
		%s:%s
                %s:%s
                 """ %(ssx['name'],ssx_vgroup[0],linux['ip_addr'],linux['interface'])

vlan_cfg_str1="""
		%s:%s
                %s:%s
                 """ %(xpress_vpn2_multi['ip_addr'],xpress_vpn2_multi['interface'],ssx['name'],ssx_vgroup1[0])


vlan_cfg_str_HA="""
                %s:%s
                %s:%s
                 """ %(linux['ip_addr'],linux['interface'],ssx_HA['name'],ssx_vgroup[0])


