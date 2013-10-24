""" Topology file for 4.6 OSPF """

###If you are not using any port on SSX and CISCO , please give valid dumy port
#Device info
ssx_ini = Initiator = {'ip_addr':'kenya-mc-con','user_name': 'joe@local','password':'joe', 'hostname':'kenya'}
ssx_resp = Responder = {'ip_addr':'yemen','user_name': 'joe@local','password':'joe', 'hostname':'yemen'}
cisco1 = cisco =  {'ip_addr':'c4900m-15-con','user_name':'cisco','password' : 'cisco'}

ixia = {'ip_addr':'10.1.10.13','username':'joe@local','password':'stoke','name':'ixia'}
apc = linux = {'ip_addr':'hutch', 'user_name':'regress','password':'gleep7','interface':'e2'}


host1 = linux = {'ip_addr':'mara', 'user_name':'regress','password':'gleep7','interface':'e2'} #Host connected to Initiator - SSX1
host2 = linux = {'ip_addr':'qa-radius-7', 'user_name':'regress','password':'gleep7','interface':'e1'} #Host connected to Responder - SSX2
#apc = linux = {'ip_addr':'qa-radxpm-1', 'user_name':'regress','password':'gleep7','interface':'e1'} #Host connected to Responder - SSX2

#Please give valid dummy ports if you dont use
# Radius server (For bringing up sessions)
p_cisco_rad  = ["2/7","eth3"]
p_cisco_rad2 = ["2/8","eth5"]


#Connectivity for Responder
p_active_ssx_cisco_slot2 = ["2/1","2/1"] # Logical slot 100 and 101 will be dependent on this port number
p_active_ssx_cisco_slot3 = ["3/1","2/2"] # Logical slot 100 and 101 will be dependent on this port number
p_standby_ssx_cisco_slot2 = ["4/0","2/14"]
p_standby_ssx_cisco_slot3 = ["4/1","2/15"]
p_to_rad_active_ssx_cisco_slot2 = ["2/2","2/13"]
p_to_rad_standby_ssx_cisco_slot2 = ["3/2","2/4"]
p_to_rad_active_ssx_cisco_slot3 = ["2/3","2/19"]
p_to_rad_standby_ssx_cisco_slot3 =  ["3/3","2/18"]

#Connectivity for Initiator
p_ini_cisco_slot2 = ["2/1","1/2"] #This var will be responsible for the logical slot for initiator
p_ini_cisco_slot3 = ["3/1","1/4"]

p_cisco_host2 = ["2/10","eth1"]

p_ini_ixia        = ["2/0","01 11 14"] # Three numbers in IXIA indicates ChassisID, cardID and portID.
p_ini_slot2_ixia  = p_ini_ixia
p_ini_slot3_ixia  = ["2/1","01 11 16"]  ## Need to make
p1_cisco_ixia     = ["2/5", "01 11 14"] ## Exit and Entry for card2 traffic from Cisco
p2_cisco_ixia     = ["2/6", "01 11 16"] ## Exit and Entry for card2 traffic from Cisco

# Dummy ports for tunnels on Initiator
dummy_ports = ["2/0", "3/0"] # ["Second card",  "Third card"]

ixia_owner = "jameer"
ixiaConfigPath = "D:/System"

