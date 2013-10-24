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

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import pexpect
import time
import re
import pingwalk
import misc
from Host import Host
from logging import getLogger
from os.path import normpath


log = getLogger()
top_lib_dir = os.path.abspath(qa_lib_dir)

def wait_for_ls_test_server_ready(self,testSerName) :
    #Waiting for maximum time taking for changing state to ready,
    #Inorder to avoid the unnecessary output in Logs
    time.sleep(108)
    self.cmd("set testSerName %s"%testSerName)
    while 1 :
       self.cmd("set tsInfo [ls::retrieve TsInfo -Name $testSerName]")
       status = self.cmd("ls::get $tsInfo -State")
       status = status.strip()
       if status=="READY":
           return 1
           break

def configure_landslide_ip_interface(self,serName,intId,address,mask,pool,numIps,Enable="true",Auto="true"):
    """Configure an interface with ip address and mask.  This will first flush the device
    to clear any existing configuration.
    """
    #self.cmd("set serverName $serName")
    #self.cmd("set ipAddress $address
    self.cmd("set serName %s"%serName)
    self.cmd("set tsc [ls::perform RetrieveTsConfiguration -Name $serName cfguser]")
    self.cmd("ls::config $tsc.Eth(%s) -Ip %s -Mask %s -Pool %s -NumIps %s -Enable %s -Auto %s"%(intId,address,mask,pool,numIps,Enable,Auto))
    self.cmd("ls::perform ApplyTsConfiguration $tsc cfguser -force")
    self.wait_for_ls_test_server_ready(serName)

def recycle_test_server_and_get_status(self,testSerName = "Spirent") :
    """Recycle test server
    """
    self.cmd("ls::perform RecycleTs -name %s"%testSerName)
    wait_for_ls_test_server_ready(self,testSerName)
    status = self.cmd("ls::get $tsInfo -State")
    status = status.strip()
    if status=="READY":
       return 1
    else: 
       return 0

def set_terminal_server_id(self,serName):
    """set the terminal server id because most of TCL APIs takes
    only the test server id.
    """
    self.cmd("set ts_Name %s"%serName)
    output = self.cmd("set tsId [ls::query TsId $ts_Name]")
    if "TS not found" in output.strip():
       return 0
    else :
       return 1

def run_diameter_server(self):
    """
    Used for the starting Diameter server .
    1. validate the files
    2. then starts the diameter server 
    3. check for errors And Warnings
    """ 
    self.cmd("ls::perform validate -testsession $test_Dia")
    self.cmd("ls::perform Run -TestSession $test_Dia")
    result = self.cmd("ls::get $test_Dia -errorsAndWarnings")
    if ("Invalid" not in result):
       return 1
    else:
       return 0

def stop_diameter_server(self,testHandle="test_Dia"):
    """set to stop test server id.
    """
    output = self.cmd("ls::perform Stop -TestSession $%s"%testHandle)
 #   output = self.cmd("ls::get -$%s -TestStateOrStep"%testHandle )
    if ("COMPLETE" in output):
       return 1
    else :
       return 0

def run_ike_client(self):
    """
    Used for the starting ike client .
    1. validate the files
    2. then starts the ike client
    3. check for errors And Warnings
    """
    self.cmd("ls::perform validate -testsession $test_")
    self.cmd("ls::perform Run -TestSession $test_")
    result = self.cmd("ls::get $test_ -errorsAndWarnings")
    if ("Invalid" not in result):
       return 1
    else:
       return 0

def stop_ike_client(self,testHandle="test_"):
    """set to stop test server id.
    """
    output = self.cmd("ls::perform Stop -TestSession $%s"%testHandle)
#    output = self.cmd("ls::get -$%s -TestStateOrStep"%testHandle )
    if ("COMPLETE" in output):
       return 1
    else :
       return 0

def start_cgf_tool(self, option="i"):
    """Starts the cgf tool as : daemon mode - no shell """

    self.cmd("cd /home/regress/open-cgf_v0.13/bin")
    self.cmd("sudo ./open-cgf -stop")
    time.sleep(4)
    self.cmd("sudo ./open-cgf -D")
    time.sleep(4)
    #" checking for successful start of process"
    procOp = self.cmd("sudo ps -ef | grep open-cgf")
    if ("erlang" in procOp):
       return 1
    else:
       return 0


def stop_cgf_tool(self, option="i"):
    """Stops the cgf tool as : stopping open-cgf """

    self.cmd("cd /home/regress/open-cgf_v0.13/bin")
    self.cmd("sudo ./open-cgf -stop")
    procOp = self.cmd("sudo ps -ef | grep open-cgf")
    if ("erlang" not in procOp ):
       return 1
    else:
       return 0


def backup_old_cdrs(self, option="i"):
    """Stops the cgf tool as : stopping open-cgf """
    self.cmd(" mkdir /home/regress/old-cdrs")
    self.cmd("cd /tmp/log")
    self.cmd("sudo mv -f CDR*.cdr /home/regress/old-cdrs/")
    procOp = self.cmd("ls | grep .cdr")
    if ("CDR" not in procOp ):
       return 1
    else:
       return 0

def backup_old_normal_cdrs(self, option="i"):
    """Stops the cgf tool as : stopping open-cgf """
    self.cmd(" mkdir /home/regress/normal-cdrs")
    self.cmd("cd /home/regress/sudan/CDR")
    self.cmd("mv -f *.cdr /home/regress/normal-cdrs/")
    procOp = self.cmd("ls | grep .cdr")
    if ("XML" not in procOp ):
       return 1
    else:
       return 0



def check_cdrs(self, option="i"):
    """Stops the cgf tool as : stopping open-cgf """
                
    cmdOp = self.cmd("cd /tmp/log")
    if ("No such file or directory" in cmdOp):
         return 0
    else:  
         procOp = self.cmd("ls | grep .cdr")
         if ("CDR" in procOp):
             return 1
         else:
            return 0


def check_normal_cdrs(self, option="i"):
    """Stops the cgf tool as : stopping open-cgf """

    cmdOp = self.cmd("cd /home/regress/sudan/CDR")
    if ("No such file or directory" in cmdOp):
         return 0
    else:
         procOp = self.cmd("ls | grep .cdr")
         if ("XML" in procOp):
             return 1
         else:
            return 0



def check_a_process(self, procName="open-cfg", procName1="erlang"):
    """
    Description  : Check the a process instances doing grep for that process 
                   of the process name given.
    Arguments    : procName - Name of the process to be checked.
    Return Value : 1 for success and 0 for failure 
    """
    procOp = self.cmd("sudo ps -ef | grep %s"% procName)
    if ("%s" % procName1 in procOp ):
       return 1
    else: 
       return 0


def verify_show_session_counters(self,expected_pkts="0") :
    """This returns a list indexed on username of every session listed along with a
       dictionary of the values
    """

    debug = False
    flag = 0

    # Example Data
    """
    01 Tue May 11 10:32:22 PDT 2010.
    02
    03 Username             Session    Rcv Pkts    Xmit Pkts   Rcv Bytes   Xmit Bytes
    04                      Handle
    05 -------------------- ---------- ----------- ----------- ----------- -----------
    06 16502102800650210@r2 fc44020b         58869       58897     2708020     2709492
    07 16502102800650211@r2 fc44021b             0           0           0           0
    """
    results = {}

    command = "show session counters"
    session_counters_raw = self.cmd(command)

    if debug:
        print 'This is the raw result:', session_counters_raw

    if len(session_counters_raw) > 0:
        # Chop the ouput into lines
        session_counters = session_counters_raw.splitlines()
        # we need to figure out which lines to read. The output is variable.
        # The header information is always 5 lines long.
        # We can take the lenght of the output and subtract the header to get
        # the length of the output we want.

        # The calculation should net a negative number. We hope.
        line_count = 6 - len(session_counters)
        if debug:
            print 'We calculated there should be', line_count, 'lines to parse'
            print 'If the above output is positive then something went wrong.'

        print 'Found', abs(line_count), 'sessions active'

        if debug:
            print 'The lines we will process are:'
            print session_counters[line_count:]

        # This odd syntax should get us only the last N lines.
        for line in session_counters[line_count:]:
            if '-------' in line:
                print 'We went too far and got the seperator!'
                print 'Please increase the number of lines to count in.'
            else:
                # Create a fresh local dictionary to accumulate the results into
                line_dict = {}
                # cut the line into words
                words = line.split()
                # The list is indexed on the username
                # so we will store it here for clean code
                username = words[0]
                # Everything else is dumpted into the local dictionary
                line_dict['Username'] = words[0]
                line_dict['Session Handle'] = words[1]
                line_dict['Rcv Pkts'] = words[2]
                line_dict['Xmit Pkts'] = words[3]
                line_dict['Rcv Bytes'] = words[4]
                line_dict['Xmit Bytes'] = words[5]

                # This packs the line dictionary into the results dictionary
                results[username] = line_dict
                
                # verfiy the pkts
                if expected_pkts != "0" :
 		   for item in results :
		       if results[item]["Xmit Pkts"] == results[item]["Rcv Pkts"] == expected_pkts:
		 	  flag = flag + 1
		       else:
		          return 0
                
    return 1

#        return results

def show_diameter_peer_profile(self,expected_pkts="0") :

    """This returns the status of diamter status like up or in a
       dictionary of the values
    """
    debug = False
    #debug = True

    return_list = []
    lines_to_parse = []

    # Example Input
    """
    1 Peer IDs                Host Addr/fqdn  Host Realm     Port  Transport Status
    2 ------------------------------------------------------------------------------
    3 translator.service.com    12.12.12.12    service.com     3868  tcp          Up
    """
    # Example output
    """
    [{'prot': '3868', 'transport': 'tcp', 'status': 'up'}]
    """

    if debug:
        print 'Now in PdgTtg.py show_diameter_peer_profile'

    command = 'show diameter peer profile'
    raw_input = self.cmd(command)
    show_diameter_peer_profile_list = raw_input.splitlines()

    # There needs to be some error checking here but I don't know what the bad input looks like yet

    if len(show_diameter_peer_profile_list) < 3:
        print 'Detected no tunnels configured!'
        print 'Please review this raw ouptut.'
        print raw_input
        return 'No tunnels configured'

    number_of_diameter_peer_ids = len(show_diameter_peer_profile_list) - 3

    if debug:
        print 'Detected', number_of_diameter_peer_ids , 'diameter peer ids'

   # This builds up a list of lines we care about
    lines_to_parse = range(3, (number_of_diameter_peer_ids + 3))

    if debug:
        print 'The following lines will be parsed:', lines_to_parse

    for line_number in lines_to_parse:
        line = show_diameter_peer_profile_list[line_number]
        local_dict = {}
        if debug:
            print 'The raw line is:'
            print line
        words = line.split()

        local_dict['peer_ids'] = words[0]
        local_dict['host_addr_or_fqdna'] = words[1]
        local_dict['host_realm'] = words[2]
        local_dict['port'] = words[3]
        local_dict['transport'] = words[4]
        local_dict['status'] = words[5]
        if debug:
            print 'local_dict contains:'
            print local_dict
        return_list.append(local_dict)
        if debug:
    	    #print 'Completed parsing "show diameter peer profile" command'
            print 'return_list contains:'
            print return_list

    return return_list


def verify_show_gtp_counters_slot(self,slot='2',total_tx='none',total_rx='none',
                           create_pdp_req_tx='none',create_pdp_resp_rx='none',
                           update_pdp_req_tx='none',update_pdp_req_rx='none',
                           update_pdp_resp_tx='none',update_pdp_resp_rx='none',
                           delete_pdp_req_tx='none',delete_pdp_req_rx='none',
                           delete_pdp_resp_tx='none',delete_pdp_resp_rx='none'):

        """
          Description: - This API verify the "show gtp counters slot 2" with passing differnt combinations
                       statastics.
          CLI Used- CLI.s that are used for the API  <show gtp counters slot 2>.
          Input: - List of differnt tatastics Inputs such as no of Request packets
                        transmit packets etc.
          Output: - Returns to the calling function ,i.e Pass or Fail .
          Author: -
          Reviewer: -                        """


        expected={'total_tx':total_tx,'total_rx':total_rx,
                 'create_pdp_req_tx':create_pdp_req_tx,'create_pdp_req_rx':create_pdp_resp_rx,
                 'update_pdp_req_tx':update_pdp_req_tx,'update_pdp_req_rx':update_pdp_req_rx,
                 'update_pdp_resp_tx':update_pdp_resp_tx,'update_pdp_resp_rx':update_pdp_resp_rx,
                 'delete_pdp_req_tx':delete_pdp_req_tx,'delete_pdp_req_rx':delete_pdp_req_rx,
                 'delete_pdp_resp_tx':delete_pdp_resp_tx,'delete_pdp_resp_rx':delete_pdp_resp_rx}

        cli="show gtp counters slot %s"  % slot
        ret_str=self.cmd(cli)
        #splitted_icmp_list=icmplist.split('\n')
        actual={}
        regex_list=['\s+Total\s+Tx\s+:\s+(?P<total_tx>\d+)\s+Total\s+Rx\s+:\s+(?P<total_rx>\d+)',
                 '\s+CREATE\s+PDP\s+REQ\s+Tx\s+:\s+(?P<create_pdp_req_tx>\d+)\s+CREATE\s+PDP\s+\RESP\s+Rx\s+:\s+(?P<create_pdp_resp_rx>\d+)',
                 '\s+UPDATE\s+PDP\s+REQ\s+Tx\s+:\s+(?P<update_pdp_req_tx>\d+)\s+UPDATE\s+PDP\s+REQ\s+Rx\s+:\s+(?P<update_pdp_req_rx>\d+)',
                 '\s+UPDATE\s+PDP\s+RESP\s+Tx\s+:\s+(?P<update_pdp_resp_tx>\d+)\s+UPDATE\s+PDP\s+RESP\s+Rx\s+:\s+(?P<update_pdp_resp_rx>\d+)',
                 '\s+DELETE\s+PDP\s+REQ\s+Tx\s+:\s+(?P<delete_pdp_req_tx>\d+)\s+DELETE\s+PDP\s+\REQ\s+Rx\s+:\s+(?P<delete_pdp_req_rx>\d+)',
                 '\s+DELETE\s+PDP\s+RESP\s+Tx\s+:\s+(?P<delete_pdp_resp_tx>\d+)\s+DELETE\s+PDP\s+\RESP\s+Rx\s+:\s+(?P<delete_pdp_resp_rx>\d+)']

        for regex in regex_list:
            obj=re.compile(regex,re.I)
            m=obj.search(ret_str)
            if m:
                dict=m.groupdict()
                for key in dict.keys():
                    actual[key]=dict[key]

        for keys in expected.keys():
            if expected[keys] != 'none':
                if expected[keys] != actual[keys]:
                    print expected[keys]
                    print actual[keys]
                    return 0
        return 1

   
def start_sst_soft_tool(self, option="i"):
    """Starts the ggsn tool as :  shell """

    self.cmd("cd /home/regress/sst_soft")
    procOp = self.cmd("./sst.sh")
    #"checking for successful start of process"
    if ("Welcome to Stoke Simulator" in procOp ):
       return 1
    else:
       return 0


def stop_sst_soft_tool(self, option="i"):
    """Stops the ggsn tool as : """

    self.cmd("cd /home/regress/sst_soft")
    self.cmd("pkill sst_soft")
    time.sleep(4)
    procOp = self.cmd("sudo ps -ef | grep ggsn")
    if ("sst_soft" not in procOp ):
       return 1
    else:
       return 0


def verify_diameter_stats(self,statType="DER", count=3):
        """API to verify the Diameter stats
        Usage: verify_diameter_stats(self.ssx,statType="Sessions", count = 100)
        Returns: 1 on successful, 0 on not successful
        """
        daiOp = self.cmd('show diameter stats | grep %s '% statType)
        diaCnt = daiOp.split(':')[1].strip()
        if int(diaCnt) == int(count):
                return 1
        else:
                return 0

def parse_show_tunnel_counters(self):
        """  API to return show tunnel counters in and out pkts counts """

        ret_str=self.cmd("show tunnel counters | grep gtp ")
        str2 ='\s*\w+\s+\w+\s+(\d+)\s+(\d)+\s+\d+\s+\d+'
        obj=re.compile(str2)
        found=obj.search(ret_str)
        actual_in_pkts=found.group(1)
        actual_out_pkts=found.group(2)
        return int(actual_in_pkts), int(actual_out_pkts)

 
