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
DESCRIPTION             : This script will invoke "ipv6 forwarding disable " on SSX CLI (Configuration mode)
REFERENCE               : SSX-cli Test and Automation Strategy
TEST CASES              : ipv6_001_conf,
                          ipv6_002_rae,
                          ipv6_003_ere,
                          ipv6_004_rm2,
                          ipv6_005_all
TOPOLOGY DIAGRAM        :

        |------------------|                       
        | Python Framework |                         |-----------|
        |------------------|-------------------------|    SSX    |
        | CLI Driver Tool  |                         |-----------|
        |------------------|


AUTHOR                  : Alok Mohapatra ; email:alok@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : cli-driver tool
UPDATE DATE             : 30th April 2007
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

class cli_conf_ipv6(test_case):
   
    myLog = getLogger()  

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

    ####################################################################

    def test_ipv6_001_pos(self):
        """Starting Test Case Steps"""
    
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

      	# Running the cli-driver commnad
	os.system(" cli-driver.pl -l %(cli_fldr)s/conf_ipv6_pos%(ssx_ver)s.log %(ssx_type)s  -f %(drvr-data_ipv6)s -c %(ssx_system)s " %script_var)    	

        # Opening SSX Connection Again
        self.ssx = SSX(topo.ssx_con['ip_addr'])
        self.ssx.telnet()

        # Comparing the log file against the golden file
	self.myLog.output("Comparing the log files")
	diff_out = os.system("diff %(gldn_fldr)s/%(ssx_ver)s/gld_conf_ipv6_pos_%(ssx_ver)s.log  %(cli_fldr)s/conf_ipv6_pos%(ssx_ver)s.log" %script_var )	
	# Declaring Test result according to diff output
	self.failUnless(not diff_out ,"Test Fail due to mismatch in logs")	
        
	# Checking SSX Health	
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")		

    ####################################################################

        

if  __name__== '__main__':

    # Build A log File.  Note Console Output Is Enabled.
    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    # Build The Test Suite And Run It.
    suite = test_suite()
    suite.addTest(cli_conf_ipv6)
    test_runner().run(suite)
    
