
""" AAA Topology Information """

'''

#**********************************************************************
#**************  U S E R    S E C T I O N  ****************************
#**********************************************************************


### SSX1 (lihue-mc-con)

ssx1 =          {'ip_addr':'salvador-mc-con','username':'joe@local','password':'joe123','name':'salvador'}
ssx2_ha =       {'ip_addr':'salvador','username':'joe@local','password':'joe123','name':'salvador'}


### Netscreen1 (qa-ns1-con)
ns              =       {'ip_addr':'qa-ns1-con','user_name':'netscreen','password':'netscreen','interface':'e0', 'name':'qa-ns1'}
### Linux Client (Takama)
linux           =       {'ip_addr':'takama','user_name':'regress','password':'gleep7','interface':'e1'}
### Radius Server1 (Huahine)
radius1         =       {'ip_addr':'takama','user_name':'regress','password':'gleep7','interface':'e2'}
### Radius Server2 (Takama)
radius2         =       {'ip_addr':'tornado','user_name':'regress','password':'gleep7','interface':'e1'}


### Ethernet Ports Connectivity Information
#**********************************************************************

port_ssx_ns  =     ['4/3', 'e0'   ]     ##Netscreen (qa-ns1)
port_ssx_linux =   ['2/0', 'eth1']      ##Linux Client (Takama)
port_ssx_radius1 = ['2/1', 'eth2']      ##Radius Server1 (Takama)
port_ssx_radius2 = ['3/0', 'eth2']      ##Radius Server2 (Tornado)

#**********************************************************************

ssx_vgroup_ns =      ["4:3","e0"   ]    ##Netscreen (qa-ns1)
ssx_vgroup_linux =   ["2:0","eth1"]     ##Linux Client (Takama)
ssx_vgroup_radius1 = ["2:1","eth2"]     ##Radius Server1 (Takama)
ssx_vgroup_radius2 = ["3:0","eth2"]     ##Radius Server2 (Tornado)


'''


#**********************************************************************
#**************  R E G R E S S I O N    S E C T I O N  ****************
#**********************************************************************


### SSX1 (bahamas-mc-con)

ssx1 = 		{'ip_addr':'bahamas-mc-con','username':'joe@local','password':'joe123','name':'bahamas'}
ssx2_ha = 	{'ip_addr':'bahamas','username':'joe@local','password':'joe123','name':'bahamas'}


### Netscreen1 (qa-ns1-con)
ns 		=	{'ip_addr':'qa-ns5-con','user_name':'netscreen','password':'netscreen','interface':'0', 'name':'qa-ns5'}
### Linux Client (Takama)
linux 		=	{'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e1'}
### Radius Server1 (Huahine)
radius1 	=	{'ip_addr':'takama','user_name':'regress','password':'gleep7','interface':'e1'}
### Radius Server2 (Takama)
radius2 	=	{'ip_addr':'bora','user_name':'regress','password':'gleep7','interface':'e2'}


### Ethernet Ports Connectivity Information
#**********************************************************************

port_ssx_ns  =     ['2/2', '0'   ]	##Netscreen (qa-ns1)
port_ssx_linux =   ['3/2', 'eth1']	##Linux Client (Takama)
port_ssx_radius1 = ['2/1', 'eth1']  	##Radius Server1 (Huahine 
port_ssx_radius2 = ['3/1', 'eth2'] 	##Radius Server2 (Takama)

#**********************************************************************

ssx_vgroup_ns =      ["2:2","0"   ]	##Netscreen (qa-ns1)
ssx_vgroup_linux =   ["3:2","eth1"]	##Linux Client (Takama)
ssx_vgroup_radius1 = ["2:1","eth1"]	##Radius Server1 (Huahine)
ssx_vgroup_radius2 = ["3:1","eth2"]	##Radius Server2 (Takama)



### Cli Access type
cli_access_type = "console"

#**********************************************************************

#Vgrouping b/w bahamas & qa-ns5
vlan_cfg_ns="""
                %s:%s
                %s:%s
                 """ %(ssx1['name'],ssx_vgroup_ns[0],ns['name'],ssx_vgroup_ns[1])

#**********************************************************************

#Vgrouping b/w bahamas & ituni
vlan_cfg_linux="""
                %s:%s
                %s:%s
                 """ %(ssx1['name'],ssx_vgroup_linux[0], linux['ip_addr'],linux['interface'])

#**********************************************************************

#Vgrouping b/w bahamas & bora
vlan_cfg_radius1="""
                %s:%s
                %s:%s
                 """ %(ssx1['name'],ssx_vgroup_radius1[0],radius1['ip_addr'],radius1['interface'])

#**********************************************************************

#Vgrouping b/w bahamas & qa-svr3
vlan_cfg_radius2="""
                %s:%s
                %s:%s
                 """ %(ssx1['name'],ssx_vgroup_radius2[0],radius2['ip_addr'],radius2['interface'])

#**********************************************************************


