""" Topology file for IKEv2 test setup. """


# SSX box, lihue
#ssx1 = {'ip_addr':'bahamas-mc-con.stoke.com',
ssx1 = {'ip_addr':'qa-tmp2-con.stoke.com',
#ssx1 = {'ip_addr':'easter-mc-con.stoke.com',
	'user_name':'joe@local',
	'password':'joe'}

#xpress vpn client, takama

#xpressvpn1  =   {'ip_addr':'takama.stoke.com',
xpressvpn1  =   {'ip_addr':'mara.stoke.com',
		'user_name':'regress',
		'password':'gleep7'}

###########################################################################

# Radius server1
#linux1={'ip_addr':'69.0.0.1'}
linux1={'ip_addr':'10.3.2.33'}
#linux1={'ip_addr':'10.3.5.33'}

# Gateway to reach the Radius server
linux2={'ip_addr':'10.3.2.1'}

###########################################################################

# Connectivity between lihue and takama

#p1_ssx1_xpressvpn1 = ["4/1","eth2"] # takama
p1_ssx1_xpressvpn1 = ["2/1","eth1"] # huahine

# Connectivity b/w lihue and radius server (radius interface to be known)qa-svr3

p2_ssx1_linux1 = ["3/1", "eth1"]
#p2_ssx1_linux1 = ["3/1", "eth3"]

###########################################################################

# Access type
cli_acess_type =  "console"

