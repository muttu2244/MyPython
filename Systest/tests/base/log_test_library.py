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
from CISCO import *
from issu import *
#from ssh import RemoteShell

from ixia import *

# private libraries
from  ike import *

#import configs file
#from issu_config import *
import topo

debug = True



"""
Notes:
http://stoke-central.stoke.com/index.php/Log_Removal

Docomo has seen some catastrophic issues when the disk becomes full
Some chages went into the 4.6B2 build that are designed to protect the system
from these type of faults. The first change is to automatically remove
excessive log files (more the 1000). The test_1000_logs tests that. 

The second feature is 
"""

        
        

class test_generate_logs(test_case):
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
        

    
    def test_generate_logs(self):
        """
        This test generates the log files only. It is designed for manual testing.
        """
        debug = True
        # Extra "dummy" files will be generated to the system to get the system to
        # the total_file_count
        total_file_count = 1020
        # Time in days to erase files
        erase_threshold = 7 
        filename_header = 'event-log-'
        log_directory = '/hd/logs'
        #log_directory = '/hdp/logs'

                
        
        password = get_hidden_password()
        self.ssx.open_hidden_shell(password)
        
        ###########
        ## Warning!
        ###########
        self.myLog.info("Warning:")
        self.myLog.info("This automatoin makes use of tail and head")
        self.myLog.info("Those binaries are not already on the SSX")
        self.myLog.info("You need to copy both of them from the script directory to:")
        self.myLog.info("/hd/logs otherwise the script will FAIL!")
        
        #################################
        ## 1. Check the state of /hd/logs
        #################################
        self.myLog.info("Testing the %s location" % log_directory)
        self.myLog.info("--------------------------------------")
        ####################
        ## Get the file list
        
        command = 'cd ' + log_directory
        # This may cause a bug here!
        #raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)
        raw_output = self.ssx.hidden_cmd(command, timeout 30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("pwd", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        if debug:
            print 'the return value was'
            print raw_output

        try:
            raw_file_count = raw_output.split()
            file_count = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        # We have placed a copy of the following two tools onto the ssx in /hd/logs
        # tail, head
        # There is a retarded bug in tail that causes it to not be able to read files
        # via stdin. A work around for this bug is as follows:
        self.myLog.info("Executing workaround to make tail work")
        raw_output = self.ssx.hidden_cmd("touch stdin", timeout=10)
        
        
        self.myLog.info("Finding the oldest log file")
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/head -1")
        oldest_file = raw_output
        self.myLog.info("The oldest logs fils is %s" % oldest_file)
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/tail -1")
        newest_file = raw_output
        self.myLog.info("The newest log file is %s" % newest_file)
        
        
        self.myLog.info("Checking the difference in date/time between the two logs")
        newest_log_parts = newest_file.split("-")
        newest_log_date = newest_log_parts[2]
        newest_log_time = newest_log_parts[3]
        newest_log_year = newest_log_date[0:4]
        newest_log_month = newest_log_date[4:6]
        newest_log_day = newest_log_date[6:8]
        
        oldest_log_parts = oldest_file.split("-")
        oldest_log_date = oldest_log_parts[2]
        oldest_log_time = oldest_log_parts[3]
        oldest_log_year = oldest_log_date[0:4]
        oldest_log_month = oldest_log_date[4:6]
        oldest_log_day = oldest_log_date[6:8]        
        
        
        self.myLog.info("Checking to see if the oldest file on the system 'should' be errased")
        # Now we have all the parts of the date/time we need to compare them to see 
        # if the time delta is greater then 7 days or some user defined value
        should_be_errased = False
        # If the years are different then errase
        if newest_log_year > oldest_log_year:
            self.myLog.info("files will be errased")
            should_be_errased = True
        # If the day value is larger
        elif newest_log_day > oldest_log_day:
            if int(newest_log_day) - int(oldest_log_day) >= erase_threshold:
                self.myLog.info("files will be errased")
                should_be_errased = True
            else:
                self.myLog.info("The oldest file is not old enough to be errased")
        self.myLog.info("The oldest file is not old enough to be errased")
        
        self.myLog.info("------------------------------------------------------------------------")
        self.myLog.info("We will now generate files that are newer then the file errasal threshold")
        self.myLog.info("This will cause ALL files that are newer then the date to be errased")
                

        self.myLog.info("We found %s files in /hd/logs" % file_count)
        files_to_generate = total_file_count - file_count
        self.myLog.info("For this test we will generate %s files" % files_to_generate)
        
            
        #file_date = int(raw_file_date[2]) - 1
        if debug:
            self.myLog.debug("These are the variables we will use:")
            self.myLog.debug("newest_log_year: %s" % newest_log_year)
            self.myLog.debug("newest_log_day: %s" % newest_log_day)
            self.myLog.debug("newest_log_month: %s" % newest_log_month)
            self.myLog.debug("erase_threshold: %s" % erase_threshold)
        file_date = str(newest_log_year) + str(newest_log_month)
        self.myLog.debug("file_date: %s" % file_date)
        erase_day = int(newest_log_day) + int(erase_threshold) + 1
        self.myLog.debug("erase_day: %s" % erase_day)
        file_date = file_date + str(erase_day)
        self.myLog.debug("file_date: %s" % file_date)
        self.myLog.info("The fake log files will be generated with date: %s" % file_date)
        
    
        ##########################
        ## Generate Fake log files
        ##########################
         
        for i in range(0,files_to_generate):
            if debug:
                print '===================================='
                print 'Workin on file number:', i, 'of:', files_to_generate
            complete_file_name = filename_header + str(file_date) + '-' + str.rjust(str(i), 6, '0')
            if debug:
                print 'The fake file will be called:', complete_file_name
            
            #command = 'cp ' + oldest_file + ' ' + complete_file_name
            command = 'touch ' + complete_file_name
            if debug:
                print 'The command will be:'
                print command
            
            raw_output = self.ssx.hidden_cmd(command)


        self.myLog.info("Done generating fake log files")
        self.myLog.info("--------------------------------------")
        #self.ssx.hidden_cmd("\n")
        self.ssx.close_hidden_shell()
        
        self.myLog.info("Checking to see the status of the log buffers")
        log_counters = show_logging(self.ssx)
        self.myLog.info("The log files will be errased when:")
        self.myLog.info("%s = %s" % (log_counters['Glob-D']['Next-Ix 1'], log_counters['Glob-D']['Next Save-Ix 1']))
        log_events_to_generate = int(log_counters['Glob-D']['Next Save-Ix 1']) - int(log_counters['Glob-D']['Next-Ix 1'])
        self.myLog.info("We need to generate %s log events to cause the log to flush to disk" % log_events_to_generate)



        
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    
    print 'Now in main'

    suite = test_suite()
    suite.addTest(test_generate_logs)
    test_runner().run(suite)
    
    print 'Done!'
