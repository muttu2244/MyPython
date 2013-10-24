""" Topology file for ISSU test setup. """

# SSX box, australia
ssx1 = {'ip_addr':'seattle',
        'ip_addr_2':'australia-mc1-con',
        'user_name':'joe@local',
        'password':'joe'}
                
#xpress vpn client, qa-radxpm-1
xpressvpn1  =   {'ip_addr':'qa-radxpm-1',
                'user_name':'regress',
                'password':'gleep7','interface':'eth2'}
                
#xpress vpn client, qa-radxpm-3
xpressvpn2  =   {'ip_addr':'qa-radxpm-3',
                'user_name':'regress',
                'password':'gleep7','interface':'eth1'}
                
#xpress vpn client, qa-radxpm-8
xpressvpn3  =   {'ip_addr':'qa-radxpm-8',
                'user_name':'regress',
                'password':'gleep7','interface':'eth2'}
                               
# radius server and linux endpoint, qa-radius-16
radius = {'ip_addr':'qa-radius-16',
                'user_name':'regress',
               'password':'gleep7','interface':'eth1'}



###########################################################################

# Radius server1
#linux1={'ip_addr':'10.3.5.33'}
#linux1={'ip_addr':'13.0.0.1'}
#linux1={'ip_addr':'192.168.150.1'}
linux1={'ip_addr':'10.11.1.1'}

# Now using raidus1 to depricate calling it linux1
radius1={'ip_addr':'10.11.1.1'}

# Gateway to reach the Radius server
linux2={'ip_addr':'10.3.5.31'}

###########################################################################


# This configuration changes per test and must be moved into a configuration section!
p1_ssx1_xpressvpn1 = ["2/0","eth2"] 
p1_ssx1_xpressvpn2 = ["2/0","eth1"]
p1_ssx1_xpressvpn3 = ["2/0","eth2"]

# This configuration changes every test and must be moved into a configruation section!
# Connectivity b/w ssx and radius server (radius interface to be known)qa-svr3
p1_ssx1_radius1 = p2_ssx1_linux1 = ["2/3", "eth1"]

###############################################################################
# IXIA

# mention your SSX ports connected to IXIA and ixia's vars
#p1_ssx_ixia = "3/3"
p1_cisco_ixia = "3/3"
p2_xpress_vpn_ixia = "2/3"
ixia_user = "jalfrey"
chassisID = 01
cardID = 03
TxportID = 2
RxportID = 3
nframes = 10

ixia_tcl_scripts= [
"source \"D:/Configs/Jeremiah/XpressVPN-1_session_0.3.2.tcl\"", 
"source \"D:/Configs/Jeremiah/XpressVPN-1_session_0.3.3.tcl\""
]


#################################################################################################################
# Versions
#################################################################################################################
'''The convention is to call X to X any version to a minor version like 4.6A1 to 4.6B1. This leads to confusion 
when programming because it makes no logical sense. In this configuration file it X will be the "base" version
There will be three versions in each direction X - 3 , X - 2, X - 1, X, X + 1, X + 2, X + 3
in addition we need to test minor to minor. Those version will be called A and B

Generally the X + 1, X + 2, X + 3, minor a and minor b versions will be all taken from the same build ID directory
The minus one, minus two and minus three builds will be taken from the old official releases. 
'''

"""
# 4.6B1S2 testing
# Legacy build for ISSUv1 to ISSUv2 testing
issu_v1 = {'tree':'4.3B3', 'build':'2008121116', 'package_name':'4.3B3'}
# minux_three is missing from build location!
minus_three = {'tree':'4.5B2', 'build':'2009081013', 'package_name':'4.5B2'}
minus_two = {'tree':'4.6B1', 'build':'2010013022', 'package_name':'4.6B1'}
minus_one = {'tree':'4.6B1S1', 'build':'2010051019', 'package_name':'4.6B1S1'}
base_version = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.6B1S2'}
minor_a = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.6X1B1S2'}
minor_b = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.6X2B1S2'}
plus_one = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.146X1B1S2'}
plus_two = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.246X1B1S2'}
plus_three = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.346X1B1S2'}
"""

# 4.6B2 testing
# Legacy build for ISSUv1 to ISSUv2 testing
issu_v1 = {'tree':'4.3B3', 'build':'2008121116', 'package_name':'4.3B3'}
# minux_three is missing from build location!
minus_four = {'tree':'4.5B2', 'build':'2009081013', 'package_name':'4.5B2'}
minus_three = {'tree':'4.6B1', 'build':'2010013022', 'package_name':'4.6B1'}
minus_two = {'tree':'4.6B1S1', 'build':'2010051019', 'package_name':'4.6B1S1'}
minus_one = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.6B1S2'}
base_version = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.6B2'}
minor_a = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.6X1B2'}
minor_b = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.6X2B2'}
plus_one = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.146X1B2'}
plus_two = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.246X1B2'}
plus_three = {'tree':'4.6B2', 'build':'2011011322', 'package_name':'4.346X1B2'}



# 4.7 Testing
"""
# Legacy build for ISSUv1 to ISSUv2 testing
issu_v1 = {'tree':'4.3B3', 'build':'2008121116', 'package_name':'4.3B3'}
# minux_three is missing from build location!
minus_three = {'tree':'4.6B1', 'build':'2010013022', 'package_name':'4.6B1'}
minus_two = {'tree':'4.6B1S1', 'build':'2010051019', 'package_name':'4.6B1S1'}
minus_one = {'tree':'4.6B1S2', 'build':'2010062215', 'package_name':'4.6B1S2'}
base_version = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.6X1B1S2'}
minor_a = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.7X1'}
minor_b = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.7X2'}
plus_one = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.147X1'}
plus_two = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.247X1'}
plus_three = {'tree':'4.7', 'build':'2010072402', 'package_name':'4.347X1'}
"""


#######################################################
# APC
#######################################################
apc_imc0 = 'australia-s0'
apc_imc1 = 'australia-s1'
apc_glc2 = 'australia-s2'
apc_glc3 = 'australia-s3'
apc_glc4 = 'australia-s4'

#######################################################
# CISCO
#######################################################
cisco = {'ip_addr':'qa-c6509-4-con','password':'stoke'}

cisco_port = {'GLC-2':{'2/0':'5/1','2/1':'5/2','2/2':'5/3','2/3':'5/4'}, \
              'GLC-3':{'3/0':'5/5','3/1':'5/6','3/2':'5/7','3/3':'5/8'}, \
              'GLC-4':{'4/0':'5/9','4/1':'5/10','4/2':'5/11','4/3':'5/12'}}

#############              
## SSX Ports
#############
ssx_2_0 = '10.11.20.1'
