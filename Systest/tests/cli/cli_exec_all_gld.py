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

class cli_exec_boot_gld(test_case):
   
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
    ''' 	
    def test_cli_exec_boot(self):
      
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
	#os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_boot_exec_%(ssx_ver)s.log  %(ssx_type)s -C boot -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_boot_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

 	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    ''' 
    def test_cli_exec_cert(self):
      
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
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cert_exec_%(ssx_ver)s.log  %(ssx_type)s -C certificate -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_cert_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_clr(self):

        # closing of SSX connection
        self.ssx.close()
  
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_clr_exec_%(ssx_ver)s.log  %(ssx_type)s -C clear -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
      
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_clr_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_conf(self):
      
        # closing of SSX connection
        self.ssx.close()
  
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_conf_exec_%(ssx_ver)s.log  %(ssx_type)s -C configuration -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
       
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_conf_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_cntx(self):

        # closing of SSX connection
        self.ssx.close()
     
        # Running the CLI-driver commnad
        os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_cntx_exec_%(ssx_ver)s.log  %(ssx_type)s -C context -f %(drvr-data)s %(ssx_system)s " %script_var)

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
   
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_cntx_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

        self.myLog.output("Golden log file created Succesfully")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_cli_exec_copy(self):

        # closing of SSX connection
        self.ssx.close()
     
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_copy_exec_%(ssx_ver)s.log  %(ssx_type)s -C copy -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
 
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_copy_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_dbug(self):

         # closing of SSX connection
        self.ssx.close()
    
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_dbug_exec_%(ssx_ver)s.log  %(ssx_type)s -C debug -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
   
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_dbug_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		



    def test_cli_exec_delt(self):

         # closing of SSX connection
        self.ssx.close()
      
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_delt_exec_%(ssx_ver)s.log  %(ssx_type)s -C delet -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
    
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_delt_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_dir(self):

         # closing of SSX connection
        self.ssx.close()
             
	# Running the CLI-driver commnad
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_dir_exec_%(ssx_ver)s.log  %(ssx_type)s -C dir -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_dir_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		



    def test_cli_exec_drve(self):

        # closing of SSX connection
        self.ssx.close()
      
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_drve_exec_%(ssx_ver)s.log  %(ssx_type)s -C drive -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_drve_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    ''' 	
    def test_cli_exec_exit(self):

       # closing of SSX connection
        self.ssx.close()
       
               
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_exit_exec_%(ssx_ver)s.log  %(ssx_type)s -C exit -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
  
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_exit_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
    '''

    def test_cli_exec_load(self):
        """Starting Test Case Steps"""
      
        # closing of SSX connection
        self.ssx.close()
   

	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_load_exec_%(ssx_ver)s.log  %(ssx_type)s -C load -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_load_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_mdir(self):
        # closing of SSX connection
        self.ssx.close()


        # Running the CLI-driver commnad
      	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_mdir_exec_%(ssx_ver)s.log  %(ssx_type)s -C mkdir -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
     
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_mdir_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_no(self):

        # closing of SSX connection
        self.ssx.close()
       
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_no_exec_%(ssx_ver)s.log  %(ssx_type)s -C no -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
    
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_no_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    '''
    def test_cli_exec_ping(self):
      
        # closing of SSX connection
        self.ssx.close()
  
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_ping_exec_%(ssx_ver)s.log  %(ssx_type)s -C ping -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_ping_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    ''' 
    def test_cli_exec_rdir(self):
        """Starting Test Case Steps"""

        # closing of SSX connection
        self.ssx.close()

	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_rdir_exec_%(ssx_ver)s.log  %(ssx_type)s -C rmdir -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
  
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_rdir_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_renm(self):

        # closing of SSX connection
        self.ssx.close()
          
      
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_renm_exec_%(ssx_ver)s.log  %(ssx_type)s -C rename -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
       
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_renm_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_rlod(self):
        """Starting Test Case Steps"""
      
        # closing of SSX connection
        self.ssx.close()

    
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_rlod_exec_%(ssx_ver)s.log  %(ssx_type)s -C reload -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_rlod_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


    def test_cli_exec_save(self):
        """Starting Test Case Steps"""
        # closing of SSX connection
        self.ssx.close()
       
     
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_save_exec_%(ssx_ver)s.log  %(ssx_type)s -C save -f %(drvr-data)s %(ssx_system)s " %script_var)    	
        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()
 

        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_save_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		


	'''    
	def test_cli_exec_sytm(self):
         # closing of SSX connection
        self.ssx.close()
   
      
	# Running the CLI-driver commnad
	          
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_sytm_exec_%(ssx_ver)s.log  -u @local -p xyz -C system -f %(drvr-data)s %(ssx_mc)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

     
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_sytm_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
	'''
	'''
    def test_cli_exec_tcrt(self):

        #closing SSX connection
        self.ssx.close()
     
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_tcrt_exec_%(ssx_ver)s.log  %(ssx_type)s -C traceroute -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

   
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_tcrt_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
	'''
	'''
    def test_cli_exec_tlnt(self):
        """Starting Test Case Steps"""
        #closing SSX connection
        self.ssx.close()
       
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_tlnt_exec_%(ssx_ver)s.log  %(ssx_type)s -C telnet -f %(drvr-data)s %(ssx_system)s " %script_var)    	

         # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

   
        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_tlnt_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

	self.myLog.output("Golden log file created Succesfully")
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		
	'''

    def test_cli_exec_trml(self):
        """Starting Test Case Steps"""
      
        #closing SSX connection
        self.ssx.close()
	# Running the CLI-driver commnad
	 
	os.system(" cli-driver.pl -l %(gldn_fldr)s/%(ssx_ver)s/gld_trml_exec_%(ssx_ver)s.log  %(ssx_type)s -C terminal -f %(drvr-data)s %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()


        gld_file = os.system("ls %(gldn_fldr)s/%(ssx_ver)s/ | grep  gld_trml_exec_%(ssx_ver)s.log " %script_var)
        self.failUnless(not gld_file, " Golden Logs are not created")

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
    suite.addTest(cli_exec_boot_gld)
    test_runner().run(suite)
    
