# This file Describes Topology for the Framework
"""
SSX ------------------------> CISCO
2/x or 3/x or 4/x
x=0 or 1 or 2 or 3 or 4
"""
# SSX Information
ssx = {'ip_addr' : 'india-mc-con', 'username':'joe@local','password':'joe'}
cisco = cisco1= {'ip_addr':'c4900m-8-con','user_name':'cisco','password' : 'cisco' }

#Mention your SSX ports used for the Testing...
p1_ssx_linux = ["2/0","eth1"]
p2_ssx_linux = ["2/1","eth1"]
p3_ssx_linux = ["2/2","eth1"]

p1_ssx_cisco = ["2/0","1/3"]

topo1 = (["easter:2:0","easter:2:1"])

topo2 = (["easter:2:0","easter:2:1","easter:2:2"])

