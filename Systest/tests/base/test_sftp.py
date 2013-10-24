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

# This is used to run two sftp at the same time
import threading

debug = True




class sftp_thread(threading.Thread):
    myLog = getLogger()
    
    def __init__(self, username, password, sftp_host, source_file, dest_file, ssx):
    
        self.username = username
        self.password = password
        self.sftp_host = sftp_host 
        self.source_file = source_file
        self.dest_file = dest_file
        self.ssx = ssx
        
        threading.Thread.__init__ ( self )
        
    def run(self):
    
    
        self.myLog.info("now inside a thread!")
        if debug:
            self.myLog.debug("recieved the following variables:")
            self.myLog.debug("username: %s" % self.username)
            self.myLog.debug("password: %s" % self.password)
            self.myLog.debug("sftp host: %s" % self.sftp_host)
            self.myLog.debug("source file: %s" % self.source_file)
            self.myLog.debug("dest file: %s" % self.dest_file)
    
        self.myLog.info("We will attempt to copy both files at the same time")
        command = 'copy sftp://' + self.username + '@' + self.sftp_host + ':' + self.source_file + ' ' + self.dest_file
        
        if debug:
            self.myLog.debug("The command will be:")
            self.myLog.debug(command)

        retr = self.ssx.ftppasswd(command, self.password, 220)
        self.myLog.info("The return value was: %s" % retr)        
        

class test_concurrent_sftp(test_case):
    myLog = getLogger()
    
    def setUp(self):
        
        print 'Now in setUp'
        self.myLog.info("now in setUp function")
        ## SSX ##
        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()
        
        self.ssx1 = SSX(topo.ssx1["ip_addr"])
        self.ssx1.telnet()
        
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

        self.ssx1.close()                
        

    
    def test_concurrent_sftp(self):
        """
        This test runs two sftp connections at the same time to verify PR 
        """
        debug = True
        username = 'regress'
        password = 'gleep7'
        sftp_host = '172.17.0.82'
        test_filename = '/auto/build/builder/4.5B2/2009081013/qnx/cb/mc/StokeOS-4.5B2'
        file_list = ['/hd/StokeOS-4.5B2_1', '/hd/StokeOS-4.5B2_2']
        
        self.myLog.info("We will now attempt to copy 1 file over")

        command = 'copy sftp://' + username + '@' + sftp_host + ':' + test_filename + ' ' + file_list[0]
        if debug:
            self.myLog.debug("The command will be:")
            self.myLog.debug(command)

        retr = self.ssx.ftppasswd(command, password, 220)
        self.myLog.info("The return value was: %s" % retr)
        
        self.myLog.info("Deleting the first test file")
        command = 'del ' + file_list[0]
        self.ssx.cmd(command)
        

        self.myLog.info("Starting our multi threaded copy")
        self.myLog.info("--------------------------------")
        for dest_filename in file_list:
            self.myLog.info("now copying the test file to: %s" % dest_filename)
            
            # This is a messy workaround for the fact we need to change both the filename
            # and the ssx name per connection
            if dest_filename == '/hd/StokeOS-4.5B2_1':
                sftp_thread(username, password, sftp_host, test_filename, dest_filename, self.ssx).start()
            elif dest_filename == '/hd/StokeOS-4.5B2_2':
                sftp_thread(username, password, sftp_host, test_filename, dest_filename, self.ssx1).start()
            else:
                self.myLog.error("oops need to create more if branches")


        
        
        
if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_concurrent_sftp)
    test_runner().run(suite)