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


class test_log_fun_001(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        self.begin_time_stamp = self.ssx.cmd('show clock')
        
        ############
        # Linux Host
        #Create the objects with the variables from topo.py
        self.linux_1 = Linux(topo.xpressvpn1["ip_addr"],topo.xpressvpn1["user_name"],
                                topo.xpressvpn1["password"])

        try:
            self.linux_1.telnet()
        except:
            self.myLog.error("Unable to telnet to first Xpress VPN Server")
            raise
            sys.exit(1)
    
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
        
        ############
        # Linux Host        
        # Close the telnet session of Linux
        self.linux_1.close()

    
    def test_log_fun_001(self):
        """
        This test verifies the system will erase log files when the total count gets
        to be over 1000 files in either /hd/logs and the files are newer then 7 days
        
        This test will pass if there are 1000 files or less left in /hd/logs
        It generates files that are over 7 days old. All of those files should be deleted
        """
        debug = True
        # Extra "dummy" files will be generated to the system to get the system to
        # the total_file_count
        total_file_count = 1020
        # Time in days to erase files
        erase_threshold = 7 
        filename_header = 'event-log-'
        
        
        # Logical Flow
        # 1. Check the state of /hd/logs (count)
        # 2. Generate fake log files to fill the system to 1020 files
        # 3. wait some time for the logs to be errased
        #    May want to expedite this by actually generating log events
        # 4. Repeat for /hdp/log
        
        # Push SSX config
        minimal_configuration(self.ssx)
        # Config is not required for this test. 
        #self.ssx.config_from_string(script_var['event_logging_default'])
        
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
        # head is not present on the system. Tail made it on there. I failed to check in
        # the 6.0 copy of head so I now need to replace the following command with python logic
        # te replace head. 
        # This method is REALLY Slow because our python2.5 API can not handle 
        # returns that are longer then 1000 lines well. Head is preferred. 
        
        #raw_output = self.ssx.hidden_cmd("ls event-log* | /hd/logs/head -1")
        raw_output = self.ssx.hidden_cmd("ls -1 event-log* ")
        raw_lines = raw_output.splitlines()
        if debug:
            print 'here are the first 5 lines of the raw output'
            for line_number in range(0,5):
                print raw_lines[line_number]
        
        # this should be the first file 
        # the first two lines are empty
        oldest_file = raw_lines[2]
        self.myLog.info("The oldest logs file is %s" % oldest_file)
        
        # Newest is the file with the highest date. (means it was created recently)
        self.myLog.info("Finding the newest file")        
        raw_output = self.ssx.hidden_cmd("ls event-log* | tail -1")
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
        
        
        
        ##########################
        ## Generate Fake log files
        ##########################
        
        
        #log_filename = ssx_date_to_log(self.begin_time_stamp)
        log_filename = ssx_date_to_log(self.begin_time_stamp, erase_threshold)
        self.myLog.info(log_filename)
        self.myLog.info("The oldest file on the system is: %s" % oldest_file)
        self.myLog.info("The newest file on the system is: %s" % newest_file)
        self.myLog.info("Today's date from the SSX is: %s" % self.begin_time_stamp)
        self.myLog.info("Files that are: %s days old (in the past) will be generated" % erase_threshold)
        self.myLog.info("The log files will be named with this filename: event-log-%s" % log_filename)
        
        
        # At this point we have the correct log filename but it's one long string like
        # "20110129-190606". We need to decrement the hhmmss values to create more filenames. 
        # We will cut the two parts appart
        log_filename_parts = log_filename.split('-')
        log_time = log_filename_parts[1]
        log_date = log_filename_parts[0]
        
        if generate_real_files:
            self.myLog.info("We will generate real log files by copying existing files to new file names")
        else:
            self.myLog.info("Files will be generated by touching (empty) files")
            
        for i in range(0,files_to_generate):
            if debug:
                print '===================================='
                print 'Workin on file number:', i, 'of:', files_to_generate
            log_local_time = int(log_time) - i
            # This complex line will automatically make sure the time value always has 6 characters
            # There is no logic to make sure it does not go Negative!
            complete_file_name = filename_header + log_date + '-' + str.rjust(str(log_local_time), 6, '0')
            if debug:
                print 'The fake file will be called:', complete_file_name
            
            if generate_real_files:
                command = 'cp ' + oldest_file.strip() + ' ' + complete_file_name
            else:
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

        
        if manual_testing:
            self.myLog.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            self.myLog.info("At this poing the test automation will hault")
            self.myLog.info("All the log files in the /hd/logs directory have been generated")
            self.myLog.info("You must now cause the system to flush the buffers to the disk")
            self.myLog.info("to observer the erasing behaviour")
            self.myLog.info("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            sys.exit(1)


        #########################
        ## Flush the logs to disk
        #########################


        # At this point we are going to enable some debugging on the SSX
        # so that there are events to write to the log file. 
        self.myLog.info("Enabling debugging to generate log events")
        command = 'no debug all'
        self.ssx.cmd(command)
        command = 'debug module iplc all'
        self.ssx.cmd(command)
        command = 'debug module ip4 packet'
        self.ssx.cmd(command)
        
        
        # Now we need to generate network traffic from one of our linux hosts
        # The way we will generate network traffic is via a ping flood.
        # Since the ping flood would go on forever we will also specify the maximum
        # number of packets to send. To calculate this we need to know how many
        # packets equals how many log events.
        # The ratio of Packets to Log events is: 1 packet = 2 log events
        
        event_expansion_ratio = 2
        error_margin = 50
        """
        if debug:
            self.myLog.debug("stubbing in 1000 events")
            log_events_to_generate = 1000
        """
            
        packets_to_send = int(error_margin + (float(log_events_to_generate) / event_expansion_ratio))
        if debug:
            self.myLog.debug("The packet expansion ration is %s" % event_expansion_ratio)
            self.myLog.debug("We will add an additional %s packets" % error_margin)
            self.myLog.debug("A total of %s packets will be sent" % packets_to_send)
        

        # old code
        """
        # This will ping the management interface 
        command = 'sudo ping -f -q -c ' + str(packets_to_send) + ' ' + topo.ssx1["ip_addr"]
        """

        
        # there is a rate limiting firewall between the linux hosts in the lab and the SSX
        # to get around this we will need to send the packets in bursts. 

        burst_size = 100
        sleep_time = 2
        bursts_to_send = 1 + (packets_to_send / burst_size)
        if debug:
            print 'packets will be sent in bursts of', burst_size
            print 'this will take', bursts_to_send, 'bursts'
        for burst in range(0,bursts_to_send):
            if debug:
                print 'working on burst', burst ,'then sleeping', sleep_time
            command = 'sudo ping -f -q -c ' + str(burst_size) + ' ' + topo.ssx1["ip_addr"]
            time.sleep(sleep_time)
        
        
        
        self.myLog.info("About to execute '%s'" % command)
        timeout = 120
        
        self.myLog.info("Sending the ping command to the Linux host")
        self.linux_1.ses.sendline(command)
        self.myLog.info("Sending the password in response to the Sudo challenge")
        self.myLog.info("This should not be requires. It's a workaround")
        command = topo.xpressvpn1["password"]
        self.myLog.debug("the password is: %s" % command)
        self.linux_1.ses.sendline(command)
        self.myLog.info("Waiting %s seconds" % timeout)
        time.sleep(timeout)
        self.myLog.info("Checking to see if it completed")
        command = '\n'
        self.linux_1.cmd(command)
        self.myLog.info("Ping Completed as expected")
        
        
        """
        
        #(interval, count, size, timeout, ipaddr)
        #ping(self, ipaddr, count=5, size=56, timeout=5, interval=0.2)
        timeout = packets_to_send + 10
        interval = 0.2
        size = 64
        #self.linux_1.ping(interval, packets_to_send, size, timeout, topo.ssx_2_0)
        retrn_val = self.linux_1.ping(topo.ssx_2_0, packets_to_send, size, timeout)
        self.myLog.debug("return value of: %s" % retrn_val)
        """
        
        #############################################
        ## Check the file count after flusing the log
        #############################################
        
        self.myLog.info("Checking to make sure files were deleted")
        self.ssx.open_hidden_shell(password)
        raw_output = self.ssx.hidden_cmd("cd \/hd\/logs", timeout=30)

        raw_output = self.ssx.hidden_cmd("pwd", timeout=30)

        raw_output = self.ssx.hidden_cmd("ls | grep event-log | wc", timeout=30)
        
        try:
            raw_file_count = raw_output.split()
            file_count = int(raw_file_count[0])
        except:
            self.myLog.error("Unable to parse the file count: %s" % raw_file_count)
            
        
        self.myLog.info("The system now has: %s files in /hd/logs" % file_count)
        self.failIf(file_count > 1000)
            
        self.ssx.close_hidden_shell()
        
        
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)
    
    print 'Now in main'

    suite = test_suite()
    suite.addTest(test_log_fun_001)

    test_runner().run(suite)
    
    print 'Done!'
