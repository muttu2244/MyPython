##### Topo information file for glcr/ikev2 ######


# SSX, SST, Cisco, IXIA, Landslide.
ssx1 = ssx = {'ip_addr':'presto-mc-con','username':'joe@local','password':'joe123','name':'presto'}
#ssx2 = {'ip_addr':'qa-mbc2-mc-con','username':'joe@local','password':'joe123','name':'qa-mbc2-mc-con'}
sst = {'ip_addr':'neutron-mc-con','username':'joe@local','password':'joe123','name':'neutron'}
ixia = {'ip_addr':'10.4.2.30','username':'joe@local','password':'stoke','name':'ixia'}
cisco = {'ip_addr':'qa-c6506-con','username':'','password':'cisco','name':'qa-c6506'}

# Linux Boxes
radius1 = {'ip_addr':'qa-radxpm-4','user_name':'regress','password':'gleep7','interface':'e1','hostname':'qa-radxpm-4'}

# Port information...
p1_ssx_clntCisco = ["2/1","5/11"]
p3_ssx_clntCisco = ["4/1", "5/14"]
p1_ssx_servCisco = ["2/3", "5/18"]
p3_ssx_servCisco = ["4/3", "5/20"]
p_servCisco_radius1 = ["5/21", "eth1"]
p1_sst_clntCisco = ["2/1", "5/7"]
p1_sst_ixia = ["3/1", "5/8"]
p1_ssx_ixia = ["2/0","5/9"]
p1_cisco_ixia = ["5/4","2/13"]
p2_cisco_ixia = ["5/23","2/14"]
