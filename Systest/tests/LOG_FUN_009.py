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
from ike import *

#import config files
from event_logging_config import *
import topo

debug = False
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


"""
LOG_FUN_007
Verify the logs from the GLC are getting written to the active IMC after GLC switchover
"""


class test_log_fun_009(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        
        
        ## SSX ##
        #Establish a telnet session to the SSX box.        
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        
        # We need both a hidden shell and normal shell open at the same time
        # This is a second connection to the same SSX
        self.ssx1 = SSX(topo.ssx1["ip_addr"])
        self.ssx1.telnet()
    
    
    def tearDown(self):

        try:
            self.ssx1.close_hidden_shell()
        except:
            self.myLog.info("unable to close hidden shell. It may already be closed")


        # Close the telnet session of SSX
        self.myLog.info("clossing connection to SSX")
        self.ssx.close()
        self.ssx1.close()
    
    def test_log_fun_009(self):
        """
        This test demonstrates how to use the method cli_cmd which is part of issu.py
        This is an improved method for doing command execution on the SSX. The major advantage
        being that it can process more the 1000 lines of which makes it a necessity for log
        processing. 
        
        one of the other novel effects is if the pager is turned on it will automatically
        press enter to get the output until it gets the command prompt back!
        """
        
        ## 
        # Logical Flow
        # 1. Load SSX configuration
        # 2. Configure advance Logging
        # Pull GLC Log information
        # 1. Open a hidden shell
        # 2. Connect to GLC-2 (slot 2)
        # 3. pull the "show log" information
        # Pull IMC Log Information
        # 1. Pull regular logs
        # 2. Pull internatl logs
        # 3. Pull debug logs
        # Compare and Verify
        # 1. Take the regular log and find all events from slot 2
        # 2. Split the events into:
        #    a. Internal
        #    b. Regular
        #    c. Debug
        # 3. Take events from local log from slot 2 and split into:
        #    a. Internal
        #    b. Regular
        #    c. Debug
        # 4. Compare the Events looking for missing events
        #    a. Internal
        #    b. Regular
        #    c. Debug
        
        
        ################
        ## Configuration
        ################
        """
        
        # Push SSX config
        minimal_configuration(self.ssx)
        self.ssx.config_from_string(script_var['event_logging_default'])
        self.ssx.cmd("\n")
        """
        # This adds details to the log we don't need
        """
        self.myLog.info("Adding hidden logging commands")
        self.ssx.config_from_string("logging format local-index global-index")
        self.myLog.info("checking to see if the system returned from configuration")
        self.ssx.cmd("\n") 
        """
        # We want to ensure we always connect to slot0
        # That way we can test slot 1-4 for local logs
        command = 'system imc-switchback'
        self.ssx.cmd(command)
        
        # We are connecting to slot 0 or slot 1 
        # If you do a "showlog" from either slot you get the Global log
        # In order to introduce events into slot 1 you must be connected
        cards_to_test = {'slot-2':'SOCK=/nv telnet 192.168.200.202',
                         'slot-3':'SOCK=/nv telnet 192.168.200.203',
                         'slot-4':'SOCK=/nv telnet 192.168.200.204'} 

        """
        cards_to_test = {'slot-2':'SOCK=/nv telnet 192.168.200.202',
                         'slot-3':'SOCK=/nv telnet 192.168.200.203',
                         'slot-4':'SOCK=/nv telnet 192.168.200.204',
                         'slot-1':'SOCK=/nv telnet 192.168.200.201'}
        """
        
        ###############################
        ## Pull GLC logging information
        ###############################
        
        
        self.myLog.info("Pulling the internal logging information from each card")
        
        local_logs = {}
        password = get_hidden_password()
        self.ssx1.open_hidden_shell(password)
        
        for card in cards_to_test.keys():
            self.myLog.info("------------------------")
            self.myLog.info("connecting to %s" % card)
            # This is the telnet command
            command = cards_to_test[card]
            if debug:
                self.myLog.debug("The command will be: %s" % command)
            self.ssx1.ses.sendline(command)
            retr = self.ssx1.ses.expect(['login:'], timeout=30)
            if retr == 0:
                self.ssx1.ses.sendline('root')
            else:
                self.myLog.error(self.ssx1.ses.before)
                fail("no login prompt found after telnet to remote card")
            # this command will pull the "local" log from the slot
            command = 'showlog'
            if debug:
                self.myLog.debug("The command will be %s" % command)
            self.ssx1.ses.sendline(command)
            lines_to_read = True
            return_lines = []
            found_command = False
            while lines_to_read:
                try:
                    raw_line = self.ssx1.ses.readline()
                    if found_command:
                        return_lines.append(raw_line.strip())
                    if command in raw_line:
                        found_command = True
                    if debug:
                        self.myLog.debug(raw_line.strip())
                except:
                    self.myLog.info("ran out of lines to read")
                    lines_to_read = False
            if debug:
                self.myLog.info("we retrieved %s lines from that command" % len(return_lines))
            
            local_logs[card] = return_lines
            # Closing the telnet session to the GLC
            self.ssx1.ses.sendline('exit')
        
        self.myLog.info("Done collecting local logs from the cards")
        
        
        ## Debug:
        command = 'show system'
        retr = self.ssx.cmd(command)
        self.myLog.debug(retr)
        retr = cli_cmd(self.ssx, command)
        self.myLog.debug(retr)
        
        #######################
        ## Pull the Global Logs
        #######################
        
        log_types = ['debug', 'standard', 'internal']
        global_logs = {}
        for log in log_types:
        
            self.myLog.info("Now collecting the %s logs" % log)
            command = 'show log ' + log 
            if debug:
                self.myLog.debug("the command will be:")
                self.myLog.debug(command)
            global_debug = cli_cmd(self.ssx, command)
            global_logs[log] = global_debug
            
        
        #########################
        ## Split the logs by slot
        #########################
        
        # I chose to retrieve all the logs at first
        # then do the processing. This ensures there is as little
        # time between retrieving the local logs and the global logs possible
        # Any latency could allow new log entries to be generated making the
        # the coorelation more difficult
        #
        # Also the local logs were retrieved first because
        # the log entries move from local to global.
        # The hope is that any log entries will have a chance to get flushed 
        # from local to global while the automation is running
        # Under heavy load there is still a chance of log entries
        # not being present when initially polled
        
 
        
        # Example Log entry        
        """
        Feb 11 12:39:26 [2] DEBUG Iked-SYNC_IPC_REPLY_SENT: iked_lc_mc_send_iked_ec_reply: Sent reply-len 0, rc = 0
        """
        # We now need to split the local logs into "internal", "regular" and "debug"
        local_logs_by_type = {}
        
        
        self.myLog.info("Spliting the standard, debug, and local logs from the cards")
        for slot in local_logs.keys():

            # create local lists to accumulate the results into
            debug_log = []
            regular_log = []
            internal_log = []
        
            self.myLog.info("Working on slot %s" % slot)
            for log_line in local_logs[slot]:
                if debug:
                    self.myLog.debug("#####################################")
                    self.myLog.debug("The raw line is:")
                    self.myLog.debug(log_line)
                if len(log_line) > 0:
                    log_words = log_line.split()
                    if debug:
                        self.myLog.debug("The split line:")
                        self.myLog.debug(log_words)
                    try:
                        log_type = log_words[4]
                    except:
                        self.myLog.error("ERROR: Unable to determine the log type for this line!")
                    if debug:
                        self.myLog.debug("Detected a log of type: %s " % log_type)
                    
                    
                    #################
                    ## Regular Log ##
                    #################
                    if log_type == 'ERR':
                        if debug:
                            self.myLog.debug("Found an ERR type. REGULAR LOG")
                        regular_log.append(log_line)
                    elif log_type == 'INFO':
                        if debug:
                            self.myLog.debug("Found an INFO type. REGULAR LOG")
                        regular_log.append(log_line)
                    elif log_type == 'WARN':
                        if debug:
                            self.myLog.debug("found a WARN type. REGULAR LOG")
                        regular_log.append(log_line)
                    elif log_type == 'CRIT':
                        if debug:
                            self.myLog.debug("Found a CRIT type. REGULAR LOG")
                        regular_log.append(log_line)

                    ##################
                    ## Internal Log ##
                    ##################
                    elif log_type == 'INT':
                        if debug:
                            self.myLog.debug("Found an INT type: INTERNAL LOG")
                        internal_log.append(log_line)
                    
                    ###############
                    ## Debug Log ##
                    ###############
                    elif log_type == 'DEBUG':
                        if debug:
                            self.myLog.debug("Found an DEBUG type. DEBUG LOG")                    
                        debug_log.append(log_line)
                    
                    else:
                        self.myLog.error("ERROR: Unable to determine the log type for line!")
                        sys.exit(1)
                        
                else:
                    if debug:
                        self.myLog.debug("Discarding empty line")
                        
            # Store the log data in the dictionary
            local_logs_by_type[slot] = {}
            local_logs_by_type[slot]['regular log'] = regular_log
            local_logs_by_type[slot]['internal log'] = internal_log
            local_logs_by_type[slot]['debug log'] = debug_log
            
            self.myLog.info("Completed processing slot %s" % slot)
        
            self.myLog.info("**********************************************************")
            self.myLog.info("there are %s lines in the regular log" % (len(regular_log)))
            self.myLog.info("there are %s lines in the internal log" % (len(internal_log)))
            self.myLog.info("there are %s lines in the debug log" % (len(debug_log)))
            self.myLog.info("**********************************************************")
            
        self.myLog.info("found the following slot's information")
        found_slots = local_logs_by_type.keys()
        self.myLog.info(found_slots)
        for slot in found_slots:
            self.myLog.info("slot: %s" % slot)
            self.myLog.info(local_logs_by_type[slot].keys())
        
        
        
        
        # Example Log entry
        """
        show log standard
        Feb  9 17:26:48(L47:G3) [0] INFO CardMgr-CARD_DETECT: IMC1 detected in slot 1
        """
        
        # We now need to split the global logs by slot they came from.
        # The slot number is the [3] element from the start of the line
        
        self.myLog.info("Now dividing the log lines by slot number")
        if debug:
            self.myLog.debug("the following log types must be processed")
            log_types_to_process = global_logs.keys()
            for log in log_types_to_process:
                self.myLog.debug(log)
                
        global_logs_by_slot = {}
        unprocessed_lines = []
                
        for log in log_types:
            if log in global_logs.keys():
                self.myLog.info("Working on logs from %s log" % log)
                self.myLog.info("There are %s lines to process" % len(global_logs[log]))
                
                # Create some local dictionaries to contain the logs
                # The dictionaries are indexed on their local log index
                slot_0_logs = []
                slot_1_logs = []
                slot_2_logs = []
                slot_3_logs = []
                slot_4_logs = []
                
                for log_line in global_logs[log]:
                    if debug:
                        self.myLog.debug("#####################################")
                        self.myLog.debug("The raw line is:")
                        self.myLog.debug(log_line)
                    # split the line into words
                    if len(log_line) > 0:
                        log_words = log_line.split()
                        if debug:
                            self.myLog.debug("The split line:")
                            self.myLog.debug(log_words)
                            self.myLog.debug("the slot number should be: %s" % log_words[3])
                        raw_slot_id = log_words[3]
                        slot_id = raw_slot_id[1]
                        if debug:
                            self.myLog.debug("after removing the brackets it should be: %s" % slot_id)
                        try:
                            source_slot = int(slot_id)
                            if source_slot == 0:    
                                if debug:
                                    self.myLog.debug("storing the line in slot_0_logs")
                                slot_0_logs.append(log_line)
                            elif source_slot == 1:
                                if debug:
                                    self.myLog.debug("storing the line in slot_1_logs")                                
                                slot_1_logs.append(log_line)
                            elif source_slot == 2:
                                if debug:
                                    self.myLog.debug("storing the line in slot_2_logs")
                                slot_2_logs.append(log_line)
                            elif source_slot == 3:
                                if debug:
                                    self.myLog.debug("storing the line in slot_3_logs")
                                slot_3_logs.append(log_line)
                            elif source_slot == 4:
                                if debug:
                                    self.myLog.debug("storing the line in slot_4_logs")
                                slot_4_logs.append(log_line)
                            else:
                                self.myLog.error("invalid source slot found in the following line:")
                                self.myLog.error(log_line)
                                self.myLog.error("line will be discarded")
                                unprocessed_lines.append(log_line)
                                ## Debug
                                sys.exit(1)
                            if debug:
                                self.myLog.debug("the log line was stored correctly")
                        except:
                            self.myLog.error("Attempting to get the source slot from raw value: %s" % log_words[3])
                            self.myLog.error("non integer value found. Discarding the following line:")
                            self.myLog.error(log_line)
                            unprocessed_lines.append(log_line)
                            ## Debug
                            sys.exit(1)
                        
                    else:
                        if debug:
                            print 'Discarding empty line'
                
                global_logs_by_slot[log] = {}
                global_logs_by_slot[log]['slot-0'] = slot_0_logs
                global_logs_by_slot[log]['slot-1'] = slot_1_logs
                global_logs_by_slot[log]['slot-2'] = slot_2_logs
                global_logs_by_slot[log]['slot-3'] = slot_3_logs
                global_logs_by_slot[log]['slot-4'] = slot_4_logs
                
                self.myLog.info("Done processing the %s logs" % log)
                self.myLog.info("We found %s lines for slot 0" % len(slot_0_logs))
                self.myLog.info("we found %s lines for slot 1" % len(slot_1_logs))
                self.myLog.info("we found %s lines for slot 2" % len(slot_2_logs))
                self.myLog.info("we found %s lines for slot 3" % len(slot_3_logs))
                self.myLog.info("we found %s lines for slot 4" % len(slot_4_logs))

          
            else:
                self.myLog.info("We are skipping processing the following log type: %s" % log)
 
            self.myLog.info("The global logs by slot now contains:")
            slots_in_global_logs = global_logs_by_slot.keys()
            self.myLog.info(slots_in_global_logs)
            for slot in slots_in_global_logs:
                self.myLog.info(global_logs_by_slot[slot].keys())
        
        
        if len(unprocessed_lines) > 0:
            self.myLog.info("************************************************************************************")
            self.myLog.info("The following lines were not processed. The code needs to be improved to catch them")
            self.myLog.info("There are %s lines:" % len(unprocessed_lines))
            for line in unprocessed_lines:
                self.myLog.info(line)
            self.myLog.info("************************************************************************************")
        
        
        ##########################
        ## Comparing the events ##
        ##########################
        
        # Ok we now have two large dictionaries that contain all the logs
        # global_logs_by_slot = is all the logs from "show log" command on the active IMC
        # local_logs_by_type = all the logs from the IMC/GLC which are split by type of log (internal, debug, regular)
        
        # To compare these two log types the following must be done:
        # The logs move from the cards to the active IMC. If there are any log
        # events missing they will be present in the local logs but not the global logs.
        # So it makes the most sense to compare the local to the global
        
        # Along the way the local logs are a mix of (internal, global, regular)
        # Those have already been split
        # The global log contains a mix of logs by slot. Those have also been split already
        

        self.myLog.info("Here are the local log stats")
        local_log_slots = local_logs_by_type.keys()
        for slot in local_log_slots:
            local_log_types = local_logs_by_type[slot].keys()
            self.myLog.info("now processing slot: %s" % slot)
            for log_type in local_log_types:
                self.myLog.info("  There are %s %s" % ( len(local_logs_by_type[slot][log_type]), log_type))
                if len(local_logs_by_type[slot][log_type]) > 0:
                    if debug:
                        self.myLog.info("here is a sample log entry: \n %s" % local_logs_by_type[slot][log_type][0])
                    local_line_index = 0
                    global_line_start = ''
                    searching_for_start = True
                    for raw_log_entry in local_logs_by_type[slot][log_type]:
                        if debug:
                            self.myLog.debug("processing the following log line")
                            self.myLog.debug(raw_log_entry)
                        # This slices the line on spaces
                        log_entry = raw_log_entry.split()
                        local_month = log_entry[0]
                        local_day = log_entry[1]
                        local_time = log_entry[2]
                        if debug:
                            self.myLog.debug("the log has the following date time:")
                            self.myLog.debug("%s %s %s" % (local_month, local_day, local_time))
                        
                        # At this point we have the local log event all pulled appart. And we can actually compare it with 
                        # the events found in the global log file
                        if debug:
                            self.myLog.debug("now looking into the global_log_by_slot under log type: %s and slot : %s" % (log_type, slot))
                        if log_type == 'regular log':
                            global_log_type = 'standard'
                            
                        if searching_for_start:    
                            global_line_index = 0
                            for raw_line in global_logs_by_slot[global_log_type][slot]:
                                if debug:
                                    self.myLog.debug("now processing the following line from the global log")
                                    self.myLog.debug(raw_line)
                                # split the line
                                global_line = raw_line.split()
                                global_month = global_line[0]
                                global_day = global_line[1]
                                global_time = global_line[2]
                                if debug:
                                    self.myLog.debug("the global log has the following date/time:")
                                    self.myLog.debug("%s %s %s" % (global_month, global_day, global_time))
                                if local_month == global_month:
                                    if debug:
                                        self.myLog.debug("the month matches")
                                    if local_day == global_day:
                                        if debug:
                                            self.myLog.debug("the day matches")
                                        if local_time == global_time:
                                            if debug:
                                                self.myLog.debug("the time matches")
                                                self.myLog.debug("There is a good chance that these two log events are the same")
                                                self.myLog.debug(raw_log_entry)
                                                self.myLog.debug(raw_line)
                                            if raw_log_entry == raw_line:
                                                global_line_start = global_line_index
                                                searching_for_start = False
                                                if debug:
                                                    self.myLog.debug("the two lines are a perfect match.")
                                                    self.myLog.debug("We have found the begining of the local log entries in the global log")
                                                    self.myLog.debug("the logs match at line: %s" % global_line_index)
                                                break
                                global_line_index = global_line_index + 1
                        else:
                            # At this point we know the location of the last matching line in the global log
                            if debug:
                                self.myLog.debug("testing to make sure the following lines match:")
                                self.myLog.debug(raw_log_entry)
                                self.myLog.debug(global_logs_by_slot[global_log_type][slot][global_line_start])
                            self.failUnless(raw_log_entry == global_logs_by_slot[global_log_type][slot][global_line_start])
                            global_line_start = global_line_start + 1
                            
                        # Increment the local line index
                        local_line_index = local_line_index + 1
                            
                                
        
        
            
        
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    print 'Now in main'

    suite = test_suite()
    suite.addTest(test_cmd)
    test_runner().run(suite)

    print 'Done!'
