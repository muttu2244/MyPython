""" Topology file for ACL test setup. """ 

# SSX box, 
ssx= {'ip_addr':'qa-tmp2-mc-con','username':'reddy@local','password':'reddy123','name':'qa-tmp2'}

# Linux Machine
linux={'ip_addr':'mara','user_name':'regress','password':'gleep7','interface':'eth2'}

# Connectivity Information
p1_ssx_linux = ["2/2","eth2"]

#Vlan String for Vgroup
vlan_cfg_acl="%s:%s %s:%s"%("qa-tmp2","2:2","mara","e2")





