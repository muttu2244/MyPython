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




class test_log_fun_004_a(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        self.begin_time_stamp = self.ssx.cmd('show clock')
        
    
    def tearDown(self):
        
        try:
            self.ssx.close_hidden_shell()
        except:
            self.myLog.info("unable to close hidden shell. It may already be closed")

        try:
            end_time_stamp = self.ssx.cmd('show clock')
            self.myLog.info("test time in UMT from SSX")
            self.myLog.info("Test began: %s" % self.begin_time_stamp)
            self.myLog.info("Test ended: %s" % end_time_stamp)
        except:
            self.myLog.error("unable to pull end timestamp")

        # Close the telnet session of SSX
        self.myLog.info("clossing connection to SSX")
        self.ssx.close()

    
    def test_log_fun_004_a(self):
        """
        This test verifies that log files written into /hd/logs and /hdp/logs
        are not written at the same time. This is done by parsing their log filenames
        
        This test generates files in the /hdp/directory
        """
        debug = True

        filename_header = 'event-log-'
        
        
        # Logical Flow
        # 1. Check the state of /hd/logs and /hdp/logs (count)
        # 2. Generate a fake log file in /hd
        # 3. Get the filename
        # 4. Verify there is no file /hdp/logs with the same filename


        
        # Push SSX config
        minimal_configuration(self.ssx)
        self.ssx.config_from_string(script_var['event_logging_default'])
        
        password = get_hidden_password()
        self.ssx.open_hidden_shell(password)
        
        #################################
        ## 1. Check the state of /hd/logs
        #################################
        
        self.myLog.info("Testing the /hd/logs location")
        self.myLog.info("--------------------------------------")
        ####################
        ## Get the file list
            
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        try:
            raw_file_count = raw_output.split()
            begin_file_count_hd = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        # We have placed a copy of the following two tools onto the ssx in /hd/logs
        # tail, head
        # There is a retarded bug in tail that causes it to not be able to read files
        # via stdin. A work around for this bug is as follows:
        self.myLog.info("Executing workaround to make tail work")
        raw_output = self.ssx.hidden_cmd("touch stdin", timeout=10)
        
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/tail -1")
        begin_newest_file_hd = raw_output
        self.myLog.info("The newest log file is %s" % begin_newest_file_hd)
        
        

        #################################
        ## 1. Check the state of /hdp/logs
        #################################
        
        self.myLog.info("Testing the /hd/logs location")
        self.myLog.info("--------------------------------------")
        ####################
        ## Get the file list
            
        raw_output = self.ssx.hidden_cmd("cd \/hdp\/logs", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        try:
            raw_file_count = raw_output.split()
            begin_file_count_hdp = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        # We have placed a copy of the following two tools onto the ssx in /hd/logs
        # tail, head
        # There is a retarded bug in tail that causes it to not be able to read files
        # via stdin. A work around for this bug is as follows:
        self.myLog.info("Executing workaround to make tail work")
        raw_output = self.ssx.hidden_cmd("touch stdin", timeout=10)
        
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/tail -1")
        begin_newest_file_hdp = raw_output
        self.myLog.info("The newest log file is %s" % begin_newest_file_hdp)




        #########################
        ## Flush the logs to disk
        #########################

        # Will need to inject 1024 8 times to flush an 8K buffer. 
        self.myLog.info("Flusing the Regular log Buffers to disk")
        command = 'evltest -S -F 1024'
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        
        
        #############################################
        ## Check the file count after flusing the log
        #############################################
        
        ###########
        ## /hd/logs
        ###########
        
        self.myLog.info("Checking /hd/logs")
        #self.ssx.open_hidden_shell(password)
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)


        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        
        try:
            raw_file_count = raw_output.split()
            end_file_count_hd = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        
        self.myLog.info("The system now has: %s files in /hd/logs" % end_file_count_hd)
        self.myLog.info("expecting there to be larger then: %s" % begin_file_count_hd)
        self.failUnless(end_file_count_hd > begin_file_count_hd)
            
            

        ###########
        ## /hd/logs
        ###########
        
        self.myLog.info("Checking /hdp/logs")
        #self.ssx.open_hidden_shell(password)
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)


        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        
        try:
            raw_file_count = raw_output.split()
            end_file_count_hdp = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        
        self.myLog.info("The system now has: %s files in /hd/logs" % end_file_count_hdp)
        self.myLog.info("expecting there to be: %s" % begin_file_count_hdp)
        self.failUnless(begin_file_count_hdp, end_file_count_hdp)
            
            
        self.ssx.close_hidden_shell()




class test_log_fun_004_b(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        self.begin_time_stamp = self.ssx.cmd('show clock')
        
    
    def tearDown(self):
        
        try:
            self.ssx.close_hidden_shell()
        except:
            self.myLog.info("unable to close hidden shell. It may already be closed")

        try:
            end_time_stamp = self.ssx.cmd('show clock')
            self.myLog.info("test time in UMT from SSX")
            self.myLog.info("Test began: %s" % self.begin_time_stamp)
            self.myLog.info("Test ended: %s" % end_time_stamp)
        except:
            self.myLog.error("unable to pull end timestamp")

        # Close the telnet session of SSX
        self.myLog.info("clossing connection to SSX")
        self.ssx.close()

    
    def test_log_fun_004_b(self):
        """
        This test verifies that log files written into /hd/logs and /hdp/logs
        are not written at the same time. This is done by parsing their log filenames
        
        This test generates files in the /hdp/directory
        """
        debug = True

        filename_header = 'event-log-'
        
        
        # Logical Flow
        # 1. Check the state of /hd/logs and /hdp/logs (count)
        # 2. Generate a fake log file in /hd
        # 3. Get the filename
        # 4. Verify there is no file /hdp/logs with the same filename


        
        # Push SSX config
        minimal_configuration(self.ssx)
        self.ssx.config_from_string(script_var['event_logging_default'])
        
        password = get_hidden_password()
        self.ssx.open_hidden_shell(password)
        
        #################################
        ## 1. Check the state of /hd/logs
        #################################
        
        self.myLog.info("Testing the /hd/logs location")
        self.myLog.info("--------------------------------------")
        ####################
        ## Get the file list
            
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        try:
            raw_file_count = raw_output.split()
            begin_file_count_hd = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        # We have placed a copy of the following two tools onto the ssx in /hd/logs
        # tail, head
        # There is a retarded bug in tail that causes it to not be able to read files
        # via stdin. A work around for this bug is as follows:
        self.myLog.info("Executing workaround to make tail work")
        raw_output = self.ssx.hidden_cmd("touch stdin", timeout=10)
        
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/tail -1")
        begin_newest_file_hd = raw_output
        self.myLog.info("The newest log file is %s" % begin_newest_file_hd)
        
        

        #################################
        ## 1. Check the state of /hdp/logs
        #################################
        
        self.myLog.info("Testing the /hd/logs location")
        self.myLog.info("--------------------------------------")
        ####################
        ## Get the file list
            
        raw_output = self.ssx.hidden_cmd("cd \/hdp\/logs", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        try:
            raw_file_count = raw_output.split()
            begin_file_count_hdp = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        # We have placed a copy of the following two tools onto the ssx in /hd/logs
        # tail, head
        # There is a retarded bug in tail that causes it to not be able to read files
        # via stdin. A work around for this bug is as follows:
        self.myLog.info("Executing workaround to make tail work")
        raw_output = self.ssx.hidden_cmd("touch stdin", timeout=10)
        
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/tail -1")
        begin_newest_file_hdp = raw_output
        self.myLog.info("The newest log file is %s" % begin_newest_file_hdp)




        #########################
        ## Flush the logs to disk
        #########################

        # Will need to inject 1024 8 times to flush an 8K buffer. 
        self.myLog.info("Flusing the Internal log Buffers to disk")
        command = 'evltest -I -F 1024'
        self.ssx.hidden_cmd(command)
        time.sleep(1)
        self.ssx.hidden_cmd(command)
        
        
        #############################################
        ## Check the file count after flusing the log
        #############################################
        
        ###########
        ## /hd/logs
        ###########
        
        self.myLog.info("Checking /hd/logs")
        #self.ssx.open_hidden_shell(password)
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)


        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        
        try:
            raw_file_count = raw_output.split()
            end_file_count_hd = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        
        self.myLog.info("The system now has: %s files in /hd/logs" % end_file_count_hd)
        self.myLog.info("expecting there to be the same: %s" % begin_file_count_hd)
        self.failUnless(end_file_count_hd == begin_file_count_hd)
            
            

        ###########
        ## /hd/logs
        ###########
        
        self.myLog.info("Checking /hdp/logs")
        #self.ssx.open_hidden_shell(password)
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)


        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        
        try:
            raw_file_count = raw_output.split()
            end_file_count_hdp = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        
        self.myLog.info("The system now has: %s files in /hd/logs" % end_file_count_hdp)
        self.myLog.info("expecting the end file count to be higher: %s" % begin_file_count_hdp)
        self.failUnless(begin_file_count_hdp < end_file_count_hdp)
            
            
        self.ssx.close_hidden_shell()




if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    
    print 'Now in main'

    suite = test_suite()
    #suite.addTest(test_log_fun_004_a)
    suite.addTest(test_log_fun_004_b)

    test_runner().run(suite)
    
    print 'Done!'
