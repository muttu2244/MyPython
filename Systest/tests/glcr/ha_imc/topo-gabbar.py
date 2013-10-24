""" Topology file for 4.6 OSPF """

###If you are not using any port on SSX and CISCO , please give valid dumy port
#Device info
ssx_ini = Initiator = {'ip_addr':'gabbar-mc-con','user_name': 'joe@local','password':'joe', 'hostname':'gabbar'}
ssx_resp = Responder = {'ip_addr':'hindukush','user_name': 'joe@local','password':'joe', 'hostname':'hindukush'}
cisco1 = cisco =  {'ip_addr':'172.16.25.119','user_name':'stoke','password' : 'stoke','hostname':'qac6506' }

ixia = {'ip_addr':'10.4.2.30','username':'joe@local','password':'stoke','name':'ixia'}
apc = linux = {'ip_addr':'nagavali', 'user_name':'regress','password':'gleep7','interface':'e1'}


host1 = linux = {'ip_addr':'nagavali', 'user_name':'regress','password':'gleep7','interface':'e1'} #Host connected to Initiator - SSX1
host2 = linux = {'ip_addr':'vansadhara', 'user_name':'regress','password':'gleep7','interface':'e2'} #Host connected to Responder - SSX2
#apc = linux = {'ip_addr':'qa-radxpm-1', 'user_name':'regress','password':'gleep7','interface':'e1'} #Host connected to Responder - SSX2

#Please give valid dummy ports if you dont use
# Radius server
p_cisco_rad  = ["2/7","eth1"]
p_cisco_rad2 = ["2/8","eth2"]


#Connectivity for Responder
p_active_ssx_cisco_slot2 = ["2/0","1/1"] # Logical slot 100 and 101 will be dependent on this port number
p_active_ssx_cisco_slot3 = ["3/0","1/3"] # Logical slot 100 and 101 will be dependent on this port number
p_standby_ssx_cisco_slot2 = ["4/0","1/5"]
p_standby_ssx_cisco_slot3 = ["4/1","1/6"]
p_to_rad_active_ssx_cisco_slot2 = ["2/1","1/2"]
p_to_rad_standby_ssx_cisco_slot2 = ["3/1","1/4"]
p_to_rad_active_ssx_cisco_slot3 = ["2/1","1/2"]
p_to_rad_standby_ssx_cisco_slot3 =  ["3/1","1/4"]

#Connectivity for Initiator
p_ini_cisco_slot2 = ["2/1","2/1"] #This var will be responsible for the logical slot for initiator
p_ini_cisco_slot3 = ["3/1","2/2"]

p_cisco_host2 = ["2/7","eth1"]

#=====If you are not using IXIA ports, please leave it
p_cisco_ixia_service = ["2/0","6/4"]
p_cisco_ixia_transport = ["2/5","3/10"]

p_ini_ixia        = ["2/0","01 06 04"] # Three numbers in IXIA indicates ChassisID, cardID and portID.
p_ini_slot2_ixia  = p_ini_ixia
p_ini_slot3_ixia  = ["3/0","01 06 05"]  ## Need to make
p1_cisco_ixia     = ["2/5", "01 03 10"] ## Exit and Entry for card2 traffic from Cisco
p2_cisco_ixia     = ["2/6", "01 03 11"] ## Exit and Entry for card2 traffic from Cisco

# Dummy ports for tunnels on Initiator
dummy_ports = ["2/2", "3/2"] # ["Second card",  "Third card"]

ixia_user = "prasanna"
chassisID = 01
cardID = 02
TxportID = 14
RxportID = 13
nframes = 10

