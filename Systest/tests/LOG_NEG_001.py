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
# AUTHOR: Jeremiah Alfrey jalfrey@stoke.com
#######################################################################

import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from log import *
from SSX import SSX
from Linux import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy
#from CISCO import *
from issu import *
#from ssh import RemoteShell
import datetime
import time

from ixia import *

# private libraries
from  ike import *

#import config files
from event_logging_config import *
import topo

debug = True
# Enable this to break the code to allow for manually tripping the test condition
manual_testing = False
generate_real_files = True



"""
Notes:
http://stoke-central.stoke.com/index.php/Log_Removal

Docomo has seen some catastrophic issues when the disk becomes full
Some chages went into the 4.6B2 build that are designed to protect the system
from these type of faults. The first change is to automatically remove
excessive log files (more the 1000). The test_1000_logs tests that. 
"""



class test_log_neg_001_a(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        
    
    def tearDown(self):
    

        # Close the telnet session of SSX
        self.myLog.info("clossing connection to SSX")
        self.ssx.close()

    
    def test_log_neg_001_a(self):
        """
        This test verifies the legal range for the command
        "max-retention-interval" which should be 2..365
        """
        debug = True
        
        # Push SSX config
        minimal_configuration(self.ssx)
        self.ssx.config_from_string(script_var['event_logging_default'])


        # This is a workaround for the bug in tha API device.py
        command = '\n'
        retr = self.ssx.cmd(command)
        if debug:
            self.myLog.debug("return value: %s" % retr)        

        ## Testing a value of 1 
        # This value is invalid because it is too low
        
        command = 'logging auto-save max-retention-interval 1'

        retr = self.ssx.configcmd(command)
        if debug:
            self.myLog.debug("return value: %s" % retr)

        return_val = retr.strip()
        if debug:
            self.myLog.debug("cleand up return value: %s" % return_val)
        
        return_lines = return_val.splitlines()
        if debug:
            self.myLog.debug("split into lines:")
            for line in return_lines:
                self.myLog.debug(line)
        
        self.failUnless("ERROR: value out of range (2-365)" in return_lines[1])



class test_log_neg_001_b(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        
    
    def tearDown(self):
    

        # Close the telnet session of SSX
        self.myLog.info("clossing connection to SSX")
        self.ssx.close()

    
    def test_log_neg_001_b(self):
        """
        This test verifies the legal range for the command
        "max-retention-interval" which should be 2..365
        """
        debug = True
        
        # Push SSX config
        minimal_configuration(self.ssx)
        self.ssx.config_from_string(script_var['event_logging_default'])


        # This is a workaround for the bug in tha API device.py
        command = '\n'
        retr = self.ssx.cmd(command)
        if debug:
            self.myLog.debug("return value: %s" % retr)        

        ## Testing a value of 366
        # This value is invalid because it is too high
        
        command = 'logging auto-save max-retention-interval 366'

        retr = self.ssx.configcmd(command)
        if debug:
            self.myLog.debug("return value: %s" % retr)

        return_val = retr.strip()
        if debug:
            self.myLog.debug("cleand up return value: %s" % return_val)
        
        return_lines = return_val.splitlines()
        if debug:
            self.myLog.debug("split into lines:")
            for line in return_lines:
                self.myLog.debug(line)
        
        self.failUnless("ERROR: value out of range (2-365)" in return_lines[1])








if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    
    print 'Now in main'

    suite = test_suite()
    suite.addTest(test_log_neg_001_a)
    suite.addTest(test_log_neg_001_b)

    test_runner().run(suite)
    
    print 'Done!'