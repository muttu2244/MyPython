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

class cli_cntx_all_gld(test_case):
   
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

    def test_cli_cntx_aaa_gld(self):

        # Getting the SSX version
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

	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_aaa_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::aaa_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
	# Clearing the aaa configuaration for next successful connection to management port
        self.ssx.configcmd("context local")
        self.ssx.configcmd("no aaa profile")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

        """ 
    def test_cli_cntx_cdr_gld(self):
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_cdr_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::cdr -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """ 
        """    
    def test_cli_cntx_cmap_gld(self):
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_cmap_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::class-map_ipv4_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """    
	"""
    def test_cli_cntx_domn_gld(self):
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_domn_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::domain_local_advertise -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """
        """
    def test_cli_cntx_ip_gld(self):

      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_ip_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_ip)s -c %(ssx_system)s " %script_var)    	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """

    def test_cli_cntx_ipsec_gld(self):
  
        #closing SSX connection
        self.ssx.close()          
	# Running the CLI-driver command
	                                                                                              
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_ipsc_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_ipsc)s -c %(ssx_system)s " %script_var) 
        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


        """  
    def test_cli_cntx_ipv6_gld(self):

      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_ipv6_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_ipv6)s -c %(ssx_system)s " %script_var)     	

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """

    def test_cli_cntx_ntp_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_ntp_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::ntp_profile -f %(drvr-data)s -c %(ssx_system)s " %script_var)     	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()      
	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		



    def test_cli_cntx_plcy_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_plcy_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::police_profile_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)   	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_pmap_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_pmap_pos_%(ssx_ver)s.log %(ssx_type)s -i context_localpolicy-map_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_rdis_gld(self):
        """Starting Test Case Steps"""
      
        #closing SSX connection
        self.ssx.close()

	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rdis_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_rdis)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_rand_gld(self):
      
        #closing SSX connection
        self.ssx.close()

	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rand_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::random-early-detect_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_rmon_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rmon_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_rmon)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_rmap_gld(self):
      
        #closing SSX connection
        self.ssx.close()

	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rmap_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::route-map_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)   	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

        """
    def test_cli_cntx_rotr_gld(self):

        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rotr_pos_%(ssx_ver)s.log  %(ssx_type)s -i context_local -f %(drvr-data_rotr)s -c %(ssx_system)s " %script_var)   	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """

    def test_cli_cntx_user_gld(self):
        #closing SSX connection
        self.ssx.close()
     
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_user_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::user_name_local -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

        """
    def test_cli_cntx_rtid_gld(self):

        #closing SSX connection
        self.ssx.close()
    
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_rtid_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local::router-id_1.1.1.1 -f %(drvr-data)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
        """

    def test_cli_cntx_sesn_gld(self)
 
        #closing SSX connection
        self.ssx.close()
      
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_sesn_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_sesn)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_cntx_intf_gld(self):

        #closing SSX connection
        self.ssx.close()
        
	# Running the CLI-driver command
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_intf_pos_%(ssx_ver)s.log %(ssx_type)s -i context_local -f %(drvr-data_intf)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		



if __name__ == '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_cntx_all_gld)
    test_runner().run(suite)
    
