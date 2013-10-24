""" IKEv1 Topology Information """
### SSX1 (bahamas-mc-con)
ssx= ssx1 = { 'ipaddr'   : 'shayadri-mc-con.stoke.com',	
	'ip_addr': 'shayadri-mc-con.stoke.com',
	'user_name': 'admin',
	'password' : 'admin@local'
 }


script_var = {}
# SSX vars
script_var['hostname']                           = ssx['ip_addr']
script_var['mgmt_ip']                            = "10.10.10.48"

ssx_system = {'ip_addr' : 'shayadri-mc-con'}    # For all the scripts
ssx_con = {'ip_addr' : 'shayadri-mc-con'}       # For specific python scripts where  console ports is required
ssx_mc  = {'ip_addr' : 'shayadri'}           # For specific python scripts where  Management port is required


