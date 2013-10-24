#====================================================================
#This file describes the target SSX, user-name, Password, configs and driver data files for CLI drievr scripts 
#====================================================================

# importing topo.py 
import topo

script_var={}

#====================================================================
#The below parameter describes the target system (SSX) and variables 
script_var['ssx_system'] = topo.ssx_system['ip_addr']
#script_var['ssx_mc']     = topo.ssx_mc['ip_addr']
script_var['ssx_con']    = topo.ssx_con['ip_addr'] 
script_var['ssx_uname']  = 'admin'                    
script_var['ssx_pw']     = 'admin'
script_var['ssx_user']   = """ %(ssx_uname)s@local""" %script_var    #To login to the SSX from managemt port
script_var['mgmt_ip']    = '10.3.255.27/24'
script_var['dflt_rout']  = '0.0.0.0/0 10.3.255.1'

#====================================================================

#Ideal SSX Configuration (Currently This configuration is not used as Console port is used for the test)
script_var['idl_ssx_conf']="""
 context local
 aaa profile
  user authentication none
  exit
 user name %(ssx_uname)s
  password %(ssx_pw)s
  priv-level administrator
  exit
 interface mgmt management
  arp arpa
  ip address %(mgmt_ip)s
  exit
 ip route %(dflt_rout)s
 exit
port ethernet 0/0
 bind interface mgmt local
  exit
 enable
 exit """ % script_var

#====================================================================


#The below parameter describes the path or name of Golden folder 
script_var['gldn_fldr']= 'golden_log'

#The below parameter describes the path or name of CLI test folder
script_var['cli_fldr']= 'cli_test_log'

#Ths below parameter is the absolute path and name of Driver data file used
script_var['drvr-data']= 'driver_data/all_pos_cfg'
script_var['drvr-data_clk']= 'driver_data/clk_pos_cfg'
script_var['drvr-data_log']= 'driver_data/log_pos_cfg'
#script_var['drvr-data_show']= 'driver_data/show_pos_cfg'
script_var['drvr-data_sytm']= 'driver_data/sytm_pos_cfg'
#script_var['drvr-data_dbug']= 'driver_data/dbug_pos_cfg'
script_var['drvr-data_ipv6']= 'driver_data/ipv6_pos_cfg'
script_var['drvr-data_intf']= 'driver_data/intf_pos_cfg'
script_var['drvr-data_ip']= 'driver_data/ip_pos_cfg'
script_var['drvr-data_ipsc']= 'driver_data/ipsc_pos_cfg'
script_var['drvr-data_rdis']= 'driver_data/rdis_pos_cfg'
script_var['drvr-data_rmon']= 'driver_data/rmon_pos_cfg'
script_var['drvr-data_rotr']= 'driver_data/rotr_pos_cfg'
script_var['drvr-data_sesn']= 'driver_data/sesn_pos_cfg'
script_var['drvr-data_hid2']= 'driver_data/hid2_pos_cfg'
script_var['drvr-data_smok']= 'driver_data/smoke_cfg'
script_var['drvr-data_fldr']= 'driver_data/fldr_pos_cfg'
script_var['drvr-data_rmap']= 'driver_data/rmap_pos_cfg'

