#!/usr/bin/env python2.5

#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : This script will invoke CLI-Driver script command for SSX-Commands
REFERENCE               : SSX-CLI Test and Automation Strategy
TEST CASES              : cli_exec_boot
TOPOLOGY DIAGRAM        :

        |------------------|                       
        | Python Framework |                         |-----------|
        |------------------|-------------------------|    SSX    |
        | CLI Driver Tool  |                         |-----------|
        |------------------|


AUTHOR                  : Alok Mohapatra ; email:alok@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : CLI-driver tool
DATE			: 25th April 2007
"""


### Importing system libraries 
import sys, os, re
import time
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

### Importing libraries from the python framework
from Linux import Linux
from log import buildLogger
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner
from SSX import SSX
from helpers import is_healthy

### Importing topo file and Config file
import topo
from config import *

class cli_conf_all_gld(test_case):
   
    myLog=getLogger()

    def setUp(self):
      
        #Establish telnet session for connecting to SSX and checking its status
        self.myLog.output("Trying to connect to SSX ")
	self.ssx = SSX(topo.ssx_con['ip_addr'])
	self.ssx.telnet()
        self.ssx.clear_health_stats()

    def tearDown(self):
        #Closing down the telnet sessions
        self.ssx.close()
	self.myLog.output("All The Telnet Sessions Closed Successfully")

    def test_cli_conf_aaa_gld(self):
      
	# Getting the SSX version for log files
        ssx_vrsn = self.ssx.get_version()
        script_var['ssx_ver']= ssx_vrsn['branch']

         # Getting the required cli-driver.pl script option according to SSX connection type
        if   "con" in topo.ssx_system['ip_addr']:
                cli_dvr_optn  = "-z"
        elif self.ssx._isnfs():
                cli_dvr_optn  = ""
        else:
                cli_dvr_optn  = " -u %(ssx_user)s -p %(ssx_pw)s " % script_var

        # Pushing the var(cli-driver.pl script option) value into the script_var variable
        script_var['ssx_type']=cli_dvr_optn

        # closing of SSX connection
        self.ssx.close()
 
        # Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_aaa_pos_%(ssx_ver)s.log %(ssx_type)s -i aaa_global_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_aaa_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_conf_admn_gld(self):
        """Starting Test Case Steps"""

        #closing SSX connection
        self.ssx.close()     
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_admn_pos_%(ssx_ver)s.log %(ssx_type)s -i admin_global_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_admn_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


	# Enabling the Telnet session
        self.ssx.configcmd("admin global profile")
        self.ssx.configcmd("no disable telnet")


    ''' 	
    def test_cli_conf_dot1_gld(self):
        """Starting Test Case Steps"""
      
        #closing SSX connection
        self.ssx.close()
     
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_dot1_pos_%(ssx_ver)s.log %(ssx_type)s -i dot1q-policy_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
 
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_dot1_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
    '''	


    def test_cli_pos_ipsc_gld(self):
        """Starting Test Case Steps"""

        #closing SSX connection
        self.ssx.close()          
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_ipsc_pos_%(ssx_ver)s.log %(ssx_type)s -i ipsec_global_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

       # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_ipsc_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    '''	
    def test_cli_pos_logg(self):
      
        #closing SSX connection
        self.ssx.close()

	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_logg_pos_%(ssx_ver)s.log %(ssx_type)s  -f %(drvr-data_log)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_logg_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

 	# Disabling Logging at console
 	self.ssx.configcmd("no logging console")
	
	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is loggt healthy")		
    ''' 		


    def test_cli_pos_ntp_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_ntp_pos_%(ssx_ver)s.log %(ssx_type)s -i ntp-global_global_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_ntp_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_pos_port_gld(self):
        """Starting Test Case Steps"""

        #closing SSX connection
        self.ssx.close()
        
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_port_pos_%(ssx_ver)s.log %(ssx_type)s -i port_ethernet_2/3 -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_port_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_pos_qos_gld(self):
        """Starting Test Case Steps"""
        #closing SSX connection
        self.ssx.close()
     
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_qos_pos_%(ssx_ver)s.log %(ssx_type)s -i qos-port-profile_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_qos_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """
    def test_cli_pos_snmp(self):
        #closing SSX connection
        self.ssx.close()
      
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_snmp_pos_%(ssx_ver)s.log %(ssx_type)s -i snmp -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_snmp_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """

    def test_cli_pos_tunl_gld(self):
        """Starting Test Case Steps"""

        #closing SSX connection
        self.ssx.close()
      
	# Running the cli-driver commnad
	
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_tunl_pos_%(ssx_ver)s.log %(ssx_type)s -i tunnel_local_type_ipsec_protocol_ip44_context_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

       
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_tunl_pos_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log files created Succesfully")
	
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		



if __name__ == '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_conf_all_gld)
    test_runner().run(suite)
    
