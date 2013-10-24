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
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
    
"""
The intended use of this API is to contain all the generic functions used
by other API and generic functions for operating on the SSX
"""

import os
import time
import sys
import threading
from SSX import SSX
from issu import *


class ssx_status():
    """
    This class polls the system for health statistics.
    It then maintains a status which can be polled by other python
    automation. It is designed to be run in a thread while testing
    the SSX via automation or manually. Automation will be developed
    first. Manual testing will need an additional function to format
    and output the relevant data to the tester. 
    
    This thread will constantly poll the SSX to make sure that it is
    healthy. When the thread detects a core file or crash it will
    update a common data structure detailing what failed and generate
    an internal log with the date time of the event. 
    
    The SSX supports connection via both the serial console as well
    as the Ethernet port for management. Since the user is likely to
    want to control the system via the serial port it is not possible
    to have this thread connect to that port. Instead it will always
    connect via the Ethernet port. 
    
    What this means is you must have the Ethernet port configured
    and functional. (routing etc.) 
    
    The first time you poll the SSX if there are any faults it will
    let you know by setting the health['status'] variable. The most 
    likely reason for this warning is the "show syscount" command
    has returned with one of the fields as a non zero. If you don't 
    want to see the want the health status to go to warn you can do
    one of th following
    a. Clear the syscount values before starting the health monitoring
       "clear syscount"
    b. Pull the system the first time. Then manually acknoledge the
       errors by reseting the health status to None. 
       health['status'] = None
       The advantage of doing it this way is that it does not clear
       the syscount values. Which means you are not changing the
       system. 
    
    
    Variables:
    health - main dictionary
           - 'status' if present means the SSX has had a fault
    status_log - log of all failures
    cpu_usage_threshold - level to alarm
    mem_usage_threshold - level to alarm
    disk_usage_threshold - level to alarm
    poll_count - total times polled
    
    """
    # Member Variables
    # These variabls are visible to all the methods below
    connected = False 
    # This is the actual handle
    
    
    # Configurable Warning Levles
    cpu_usage_threshold = 95
    mem_usage_threshold = 90
    disk_usage_threshold = 90

    ssx = None

    # This is a log that preserves and failures or warnings
    # That happen on the SSX itself
    # This takes care of capturing when (time) something happened
    status_log = []
    
    # This is the common data structure that all methods write to
    # Each method will create it's own section
    # in addition they can update a common structure witch relates to
    # overall health of the SSX. 
    health = {'status':None, 'last check run':'none'}
    
    # a count of times the poll method has been run
    poll_count = 0

    def __init__(self, ssx):
        """
        Initialize the connection to the SSX
        """
        debug = False
        
        if debug:
            print 'now in __init__ in ssx_status in utils.py'
            
        self.ssx = ssx


        

    def connect(self, max_tries = 3, sleep_time = 10):
        """
        This method connects to the SSX itself. When it is first called
        via the __init__ method it will connect via telnet to the 
        managament IP address of the SSX.
        From here each method in this class will allways call the
        connect method prior to executing a command. That ensures
        the system is connected. If already connected it just verifies
        that it can send a command and get a response (still connected)
        The method always returns the current time from the SSX as a 
        """
        if debug:
            print 'now in the connect method'
            #print "%s connect" % (self.getName(),)
            print 'max tries:', max_tries


        if not self.connected:                
            for tries in range(max_tries):
                try:
                    # If you want to use SSH you need to change this line!
                    self.ssx.telnet()
                    if debug:
                        print 'succussfully connected to SSX'
                    break

                except:
                    if debug:
                        print 'failed to connect to SSX:'
                        print 'sleeping', sleep_time
                    time.sleep(sleep_time)
                    
                if debug:
                    print 'Completed Try number:', tries
                

            

        time = show_time(self.ssx)
        if debug:
            print time
        self.connected = True
        return time

            
            
    def poll(self):
        """
        This is the main loop where the status is built up (polling)
        """
        heartbeat = True
        
        """
        Logical flow:
        1. "show process cpu non-zero"
           look for CPU utilization over 90% in 5 minutes
        2. "show mem" 
           look for more then 90% utilization
        3. "show syscount"
           If there are any Crit events search the logs for them
           If there are any ERR event search the log for them
           If there are any Warn Events search the log for them
           if "Process Core" look for core files
           if "process restart" ???? Search the log?
           If card restart
        4. "show version slot x" and get uptime
           if IMC switchover
           a. "show version slot x" and get uptime
        5. "show environmental"
           if there are any errors or alarms
           a. search environmental detail if fault
           b. search for log events
        6. "show port detail" 
           look for Admin: UP Link: Down
        7. "show port counters" 
           look for errors
        8. "show card" 
           look for present
        9. "show file-system" to check disk space
        10. "show upgrade status"
            look for "revert"
        11. "show log | grep foo" check for card present state and other
            important log events  
        """
        if heartbeat:
            print 'poll_cpu_utilization'
        self.poll_cpu_utilization()
        if heartbeat:
            print 'poll_mem_utilization'
        self.poll_mem_utilization()
        if heartbeat:
            print 'poll_syscount'
        self.poll_syscount()
        if heartbeat:   
            print 'poll_card_uptime'
        self.poll_card_uptime()
        if heartbeat:
            print 'poll_environmental'
        self.poll_environmental()
        if heartbeat:
            print 'poll_physical_ports'
        self.poll_physical_ports()
        if heartbeat:
            print 'poll_bad_packets'
        self.poll_bad_packets()
        if heartbeat:
            print 'poll_card_status'
        self.poll_card_status()
        if heartbeat:
            print 'poll_disk_utilization'
        self.poll_disk_utilization()
        if heartbeat:
            print 'poll_issu_status'
        self.poll_issu_status()
        if heartbeat:
            print 'poll_system_logs'
        self.poll_system_logs()
        
        self.poll_count = self.poll_count + 1
        if heartbeat:
            print 'completed polling cycle', self.poll_count
            
            
        
        return self.health['status']
        
        
        
        
        
    def poll_cpu_utilization(self):

        """
        Runs the command "show process cpu" and reads the CPU utilization
        Then if it updates the health
        If it is above the threshold level (5 minute CPU %) it also warns
        """
        debug = False
        
        if debug:
            print 'now in utils.py poll_cpu_utilization'
        
        cpu_list = ['CPU0','CPU1']
        
        if debug:
            print 'now in poll_cpu as part of utils.py'
            print 'pulling the CPU utilization now'
            
        # Get the values from the SSX

        cpu_usage = show_process_cpu(self.ssx)
        
        # we care about
        # CPU0, CPU1
        if debug:
            print 'the CPU utilization is:'
            print cpu_usage['CPU Utilization']['CPU0']
            print cpu_usage['CPU Utilization']['CPU1']
            
        for cpu in cpu_list:
            if float(cpu_usage['CPU Utilization'][cpu]['5 minute']) >= float(self.cpu_usage_threshold):
                if debug:
                    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    print 'CPU utilizaiton is above the warning threshold on CPU:', cpu
                    print 'threshold:', self.cpu_usage_threshold, 'level:', float(cpu_usage['CPU Utilization'][cpu]['5 minute'])
                    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                self.health['status'] = 'warning'
                warning_message = ("CPU utilizaiton for Slot %s is above threshold level %s" % (slot, self.cpu_usage_threshold))
                log_origin = 'poll_cpu_utilization'
                ssx_time = show_time(self.ssx)
                log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                if debug:
                    print 'the following log message will be logged:'
                    print log_message
                    
                self.status_log.append(log_message)

        
        self.health['cpu usage'] = cpu_usage
        
        self.health['last check run'] = 'cpu utilization'
        
        return 'complete'


    def poll_mem_utilization(self):
        """
        Runs the command "show mem" and reads the memory usage
        The if it updates the health data structure
        If the usage is ablve the threshold level it warns
        """
        debug = False
        if debug:
            print 'non in utils.py poll_mem_utilization'
        
        
        # Get the values from the SSX

        if debug:
            print 'pulling the memory utilization'
        mem_usage = show_mem(self.ssx)
        
        if debug:
            print 'this is what we got back'
            print mem_usage.keys()
            
        
        
        for slot in mem_usage.keys():
            if 'slot' in slot:
                if int(mem_usage[slot]['percent available']) > self.mem_usage_threshold:
                    if debug:
                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                        print 'Memory utilizaiton is above the warning threshold for:', slot
                        print 'threhold:', self.mem_usage_threshold, 'level:',  mem_usage[slot]['percent available']
                        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    self.health['status'] = 'warning'

                    warning_message = ("Memory utilizaiton for Slot %s is above threshold level %s" % (slot, self.mem_usage_threshold))
                    log_origin = 'poll_mem_utilization'
                    ssx_time = show_time(self.ssx)
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
        
        self.health['mem usage'] = mem_usage
        
        self.health['last check run'] = 'memory usage'
        
        return 'complete'
        
        
    def poll_syscount(self):
        """
        Runs the command "show syscount" and looks for any type of
        failure. It then updates the health data structure with it's
        results. If there are any failures it generates log events
        
        to prevent generating false negatives it checks to see if there
        are any new failures. It is done by comparing the previous polling
        against the current. 
        """
        debug = False
        
        if debug:
            print 'now in utils.py poll_syscount'
        

        current_syscount = show_syscount(self.ssx)
        
        try:
            previous_sycount = self.health['syscount']
            # do comparission here
            keys = previous_sycount.keys()
            for key in keys:
                # both dictionaries should have the same keys
                # If the key is missing the try block will fail
                # and the system will sipmly examine the values
                    
                if not (current_syscount[key] == previous_sycount[key]):
                    # At this point we know the key exists and that
                    # the values are different. This means something happened
                    if debug:
                        print key, 'event detected!'
                    # Due to the long polling time it is possible for the count 
                    # to be larger then 1. So we should do some math to
                    # see how many times it happened
                    event_count = int(current_syscount[key]) - int(previous_sycount[key])
                    
                    if debug:
                        print 'it happened', event_count, 'times since the last polling'
                        
                    # Now we need to log and possibly investigate here!
                
                
                    warning_message = ("detected %s event. Event occured %s times since last poll" % (key, event_count))
                    log_origin = 'poll_syscount'
                    ssx_time = show_time(self.ssx)
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
            
        except:
            keys = current_syscount.keys()
            for key in keys:
                if not (int(current_syscount[key]) == 0):
                    if debug:
                        print key, 'event detected'
                    event_count = int(current_syscount[key])
                    
                    ssx_time = show_time(self.ssx)
                    warning_message = ("detected %s event. Event occured %s times since last poll" % (key, event_count))
                    log_origin = 'poll_syscount'
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
                    
        # be sure to store the last polled data
        self.health['sycount'] = current_syscount
        self.health['last check run'] = 'syscount'
        return 'complete'
        
        
    def poll_card_uptime(self):
        """
        Runs the command "show card" to get a list of the cards in the 
        system. The runs the command "show version slot x" to get the 
        uptime of each card. This method does not generate logs or warnings
        data is reported to health['card uptime']
        """
        debug = False
        
        if debug:
            print 'now in utils.py poll_card_uptime'
        

        # Retrieve the data via "show card"
        card_list = show_card_state(self.ssx)
        # Get the list of cards. It will be like ['Slot 1, 'Slot 2', ...]
        card_names = card_list.keys()
        if debug:
            print 'found the following cards present:'
            for name in card_names:
                print '\t', name 
        # generate a list that is just the numbers like [0,1,2]
        card_numbers = []
        for card in card_names:
            if not (card == 'Status'):
                # take the raw name like "Slot 1" and take only the last char
                card_numbers.append(card[-1])
                if debug:
                    print 'the card number is:', card[-1]
        if debug:
            print 'The card numbers are:'
            for number in card_numbers:
                print '\t', number
        

        card_uptime = {}
        for card_number in card_numbers:
            if debug:
                print 'retrieving the uptime for slot:', card_number
                
            version_by_slot = show_version(self.ssx, card_number)
            card_name = 'slot ' + card_number
            card_uptime[card_name] = version_by_slot
            
        self.health['card uptime'] = card_uptime
        self.health['last check run'] = 'card uptime'
        return 'complete'
        
        
    def poll_environmental(self):
        """
        Runs the command "show environmental" to get a list of environmental
        alarms. Then generates log messages from that and reports to the common
        structure health['environmental']
        """
        debug = False
        
        if debug:
            print 'now in utils.py poll_environmental'
        

        environmental_status = show_environmental(self.ssx)
        
        sections = environmental_status.keys()
        for section in sections:
            slots = environmental_status[section].keys()
            if section == 'alarm status':
                if not (environmental_status[section]['general status'] == 'No \tSystem-Wide Alarm triggered'):
                    warning_message = ("detected an environmental event. %s" % environmental_status[section]['general status'])
                    log_origin = 'poll_environmental'
                    ssx_time = show_time(self.ssx)
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
                    
                    self.health['status'] = 'warning'
                elif not (environmental_status[section]['alarmm1'] == 'No errors detected'):
                    warning_message = ("detected an environmental event for alarmm1. %s" % environmental_status[section]['alarmm1'])
                    log_origin = 'poll_environmental'
                    ssx_time = show_time(self.ssx)
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
                    
                    self.health['status'] = 'warning'
            else:
                for slot in slots:
                    if not (environmental_status[section][slot]['source'] == 'No errors detected'):
                        warning_message = ("detected an %s environmental event. %s had error: %s" % (section, slot, environmental_status[section][slot]['source']))
                        log_origin = 'poll_environmental'
                        ssx_time = show_time(self.ssx)
                        log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                        if debug:
                            print 'the following log message will be logged:'
                            print log_message
                            
                        self.status_log.append(log_message)
                        
                        self.health['status'] = 'warning'

        self.health['environmental'] = environmental_status
        self.health['last check run'] = 'environmental'
        return 'complete'
                        
        
    def poll_physical_ports(self):
        """
        Executes the command "short port detail" and looks for ports that are both
        admin: up and link state: up. If there are any ports except the management (1/0,0/0)
        link state: down then it warns. It will also diff the previous test run to find changes
        """
        debug = False
        
        if debug:
            print 'now in utils.py poll_physical_ports'

        port_details = show_port_detail(self.ssx)
        
        # Logical flow:
        # 1. Pull the data from the SSX
        # 2. Check to see if we have a previous set of data
        #     A. Check to see if the port is down
        #        This means:
        #        Admin State: Up
        #        Link State: Down
        #     B. If the port is "down" check to see if it was already know to be down
        #        in the data for the previous run
        #     C. Warn if failed
        # 3. If not then just check and warn
        
        port_list = port_details.keys()
        for port in port_list:
            if self.health.has_key('port details'):
                if port_details[port]['Admin State'] == 'Up' and port_details[port]['Link State'] == 'Down':
                    if not (self.health['port details'][port]['Link State'] == 'Down'):
                        warning_message = ("detected a phsical port %s is down" % port)
                        log_origin = 'poll_physical_ports'
                        ssx_time = show_time(self.ssx)
                        log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                        if debug:
                            print 'the following log message will be logged:'
                            print log_message
                            
                        self.status_log.append(log_message)
                        
                        self.health['status'] = 'warning'
         
            else:
                if port_details[port]['Admin State'] == 'Up' and port_details[port]['Link State'] == 'Down':
                    warning_message = ("detected a phsical port %s is down" % port)
                    log_origin = 'poll_physical_ports'
                    ssx_time = show_time(self.ssx)
                    log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                    if debug:
                        print 'the following log message will be logged:'
                        print log_message
                        
                    self.status_log.append(log_message)
                    
                    self.health['status'] = 'warning'
                    
        self.health['port details'] = port_details
        self.health['last check run'] = 'physical port status'
        return 'complete'
        
        
    def poll_bad_packets(self):
        """
        Executes "show port counters detail" then checks
        for the following types of bad packets:
        
        Input
        
        ErrorPkts
        OctetsBad
        CRCErrors
        DataErrors
        AlignErrs
        LongPktErrs
        JabberErrs
        SymbolErrs
        UnknownMACCtrl
        RuntErrPkts
        SequenceErrs
        SymbolErrPkts
        
        Output
        
        ErrorPkts
        OctetsBad
        PktsCRCErrs
        TotalColls
        SingleColls
        MultipleColls
        LateCollisions
        ExcessiveColls
        FlowCtrlColls
        ExcessLenPkts
        UnderrunPkts
        ExcessDefers
        
        method will retain a history of what is polled last. It will only alarm
        if it sees the counters go above zero the first time or increase
        """
        
        list_of_packet_errors_input = ['ErrorPkts','OctetsBad','CRCErrors','DataErrors','AlignErrs','LongPktErrs',\
        'JabberErrs','SymbolErrs','UnknownMACCtrl','RuntErrPkts','SequenceErrs','SymbolErrPkts']
        
        list_of_packet_errors_output = ['ErrorPkts','OctetsBad','PktsCRCErrs','TotalColls','SingleColls','MultipleColls',\
        'LateCollisions','ExcessiveColls','FlowCtrlColls','ExcessLenPkts','UnderrunPkts','ExcessDefers']

        debug = False
        
        if debug:
            print 'now in utils.py poll_bad_packets'
        
        if debug:
            print 'pulling the port details'
        port_details = show_port_counters_detail(self.ssx)
        
        
        port_list = port_details.keys()
        
        """
        if debug:
            print '000000000000000000000000000000000000000000000'
            for port in port_list:
                print 'port:', port
                print '\t', port_details[port]
            print '000000000000000000000000000000000000000000000'        
        """
        
        
        if debug:
            print 'will be processing the following ports:'
            print port_list
        for port in port_list:
            if debug:
                print 'now working on port:', port
            
            if self.health.has_key('port counters'):
                if debug:
                    print 'we already have history on this port'
                if 'Input' in port:
                    if debug:
                        print 'processing Input'
                    for error_type in list_of_packet_errors_input:
                        if int(port_details[port][error_type]) > int(self.health['port counters'][port][error_type]):
                            if int(port_details[port][error_type]) > 0:
                                warning_message = ("detected a packet error of type: %s on port %s" % (error_type, port))
                                log_origin = 'poll_bad_packets'
                                ssx_time = show_time(self.ssx)
                                log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                                if debug:
                                    print 'the following log message will be logged:'
                                    print log_message
                                    
                                self.status_log.append(log_message)
                                
                                self.health['status'] = 'warning'
                elif 'Output' in port:
                    if debug:
                        print 'processing Ouput'
                    for error_type in list_of_packet_errors_output:
                        if int(port_details[port][error_type]) > int(self.health['port counters'][port][error_type]):
                            if int(port_details[port][error_type]) > 0:
                                warning_message = ("detected a packet error of type: %s on port %s" % (error_type, port))
                                log_origin = 'poll_bad_packets'
                                ssx_time = show_time(self.ssx)
                                log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                                if debug:
                                    print 'the following log message will be logged:'
                                    print log_message
                                    
                                self.status_log.append(log_message)
                                
                                self.health['status'] = 'warning'
                else:
                    print 'Found a bogus port name:', port, counter
                    print 'Port name must contain: Input, Output'
            
            
            else:
                if debug:
                    print 'getting information for the first time on this port'
                if 'Input' in port:
                    if debug:
                        print 'processing Input'
                    for error_type in list_of_packet_errors_input:
                        if int(port_details[port][error_type]) > 0:
                            warning_message = ("detected a packet error of type: %s on port %s" % (error_type, port))
                            log_origin = 'poll_bad_packets'
                            ssx_time = show_time(self.ssx)
                            log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                            if debug:
                                print 'the following log message will be logged:'
                                print log_message
                                
                            self.status_log.append(log_message)
                            
                            self.health['status'] = 'warning'
                elif 'Output' in port:
                    for error_type in list_of_packet_errors_output:
                        if debug:
                            print 'port:', port 
                            print 'now processing error type:', error_type
                            print port_details[port], port_details[port][error_type]
                        if int(port_details[port][error_type]) > 0:
                            warning_message = ("detected a packet error of type: %s on port %s" % (error_type, port))
                            log_origin = 'poll_bad_packets'
                            ssx_time = show_time(self.ssx)
                            log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                            if debug:
                                print 'the following log message will be logged:'
                                print log_message
                                
                            self.status_log.append(log_message)
                            
                            self.health['status'] = 'warning'
                else:
                    print 'Found a bogus port name:', port
                    print 'Port name must contain: Input, Output'
                    raise('invalid port name found. Must contain Input, Output')

                
        self.health['port counters'] = port_details
        self.health['last check run'] = 'packet errors'
        return 'complete'
        
        
    def poll_card_status(self):
        """
        """
        self.health['last check run'] = 'card status'
        return 'complete'        
        
    def poll_disk_utilization(self):
        """
        Runs the command "show file-system" then checks to see if
        the utilizaiton is over the threshold level
        self.disk_usage_threshold
        If it's above the level it warns
        it then stores the data into the health strucuture
        
        checks will only be made for:
        /hd
        /hdp
        """
        debug = False
        
        if debug:
            print 'now in util.py poll_disk_utilization'
        
        mounts_to_check = ['hd','hdp']


        disk_usage = show_file_system(self.ssx)
        
        for mount in mounts_to_check:
            if int(disk_usage[mount]['percent used']) > self.disk_usage_threshold:
                warning_message = ("disk usage on mount point /%s is greater then %s" % (mount, self.disk_usage_threshold))
                log_origin = 'poll_disk_utilization'
                ssx_time = show_time(self.ssx)
                log_message = ("%s - %s -%s" % (ssx_time, warning_message, log_origin))
                if debug:
                    print 'the following log message will be logged:'
                    print log_message
                    
                self.status_log.append(log_message)
                
                self.health['status'] = 'warning'                
        
        self.health['disk utilization'] = disk_usage 
        self.health['last check run'] = 'disk utilization'
        return 'complete'
        
        
        
    def poll_issu_status(self):
        """
        """
        self.health['last check run'] = 'issu status'
        return 'complete'        
        
    def poll_system_logs(self):     
        """
        """
        self.health['last check run'] = 'system logs'
        return 'complete'
        


class ssx_crashmon(threading.Thread):
    """
    This is a thread wrapper for ssx_status class. It allows the
    polling of the system in parallel to other automated testing.
    All the logic for polling and reporting is based in ssx_status class
    """
    
    debug = False
    
    if debug:
        print 'ssx_crashmon object created'
    
    ssx_ip = None
    ssx = None
    ssx_health = None

    def __init__ (self, ssx_ip, name='crashmon'):
        """
        This method makes the initial connection to the SSX
        """
        debug = False
        
        
        if debug:
            print 'now in the __init__ method'
        
        self.ssx_ip = ssx_ip
        
        if debug:
            print 'creating the SSX Object'
            
        # here is the object for polling the status
        self.ssx = SSX(self.ssx_ip)
        
        if debug:
            print 'about to telnet to:', self.ssx_ip
            
        self.ssx.telnet()
            
        if debug:
            print 'creating a ssx_status object'
            
        self.ssx_health = ssx_status(self.ssx)

    
    
        self._stopevent = threading.Event()
        
        self._sleepperiod = 1.0
        
        threading.Thread.__init__(self, name=name)
        
        if debug:
            print 'done with the  __init__ method in ssx_crashmon'
    
        

            
                
    
    def run(self):
        """
        This is where the main code loop goes
        """
        if debug:
            print 'now in the run method'
            print "%s starts" % (self.getName(),)
        
            
        count = 0
        while not self._stopevent.isSet():
            count += 1
            print "loop %d" % (count,)
            
            
            self.ssx_health.poll()
            if self.ssx_health.health['status']:
                print "Detected a fault condition in the SSX!"
                print "printing the log"
            for line in self.ssx_health.status_log:
                print line
                  
            # this was in the example code. 
            # not sure if it's needed.
            self._stopevent.wait(self._sleepperiod)
        
        
        

        print "%s ends" % (self.getName(),)
        
    
    def join(self, timeout=None):
        """
        The join method is called when you want to terminate the thread
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        
        