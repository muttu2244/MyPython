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
    
### python stuff
import time
import shutil
import string

### local stuff
from logging import getLogger
from pexpect import TIMEOUT
import pexpect
import time
import datetime
import re
# what is this for?
from pprint import pprint


# Used for nslookup
import socket 

### import SSX
# this import may not be required. 
#from device import SSX

# used for unix_to_dos_path conversion
import ntpath

# used to get_mac_address
import CISCO

enable_prompt_regex = "[\r\n]*\S+\[\S+\]#"
yesno_prompt_regex =".*[\r\n.]*\(\[*yes\]*/\[*no\]*\)\s*$"

debug = False

month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# This is a complete list of all the valid ports on the SSX. When the 14 slot chassis is tested this will need to be changed
# to include the new ports
valid_port_list = ['0/0','1/0','2/0','2/1','2/2','2/3','3/0','3/1','3/2','3/3','4/0','4/1','4/2','4/3']


def cli_cmd(self, command, raw=False):
    """
    This is a greatly imroved version of cmd from /SSX/device.py
    It will read and parse the command prompt to correctly and quickly detect it.
    This method can parse very long outputs and is much faster then the existing method
    
    To use it simply send the command and the output will be returned
    
    The output is returned as a list []. If you use the raw=True you will get it as a
    single long string not split yet.
    """
    
    
    debug = False
    
    if debug:
        print 'now in cli_cmd'

    timeout = 5

    self.ses.sendline('\r')
    # The first line we read is empty
    raw_prompt = self.ses.readline()
    # This is the actual prompt
    raw_prompt = self.ses.readline()
    if debug:
        print 'raw_prompt:', raw_prompt
    
    prompt_pieces = raw_prompt.strip()
    if len(prompt_pieces) < 2:
        self.ses.sendline('\r')
        # The first line we read is empty
        raw_prompt = self.ses.readline()
        # This is the actual prompt
        raw_prompt = self.ses.readline()
        if debug:
            print 'raw_prompt:', raw_prompt
    else:
        if prompt_pieces == '#':
            if debug:
                print 'detected QNX Shell prompt: #'
            prompt = '#'
        else:
            prompt_pieces = prompt_pieces.split('[')
            if debug:
                print 'hostname:', prompt_pieces[0]
                print 'remainder:', prompt_pieces
            prompt_hostname = prompt_pieces[0]
            prompt_pieces = prompt_pieces[1].split(']')
            if debug:
                print 'Context:', prompt_pieces[0]
                print 'remainder:', prompt_pieces    
            prompt_context = prompt_pieces[0]
            prompt_admin_level = prompt_pieces[1]
    
    
    #prompt = 'australia'
    prompt = prompt_hostname + '.' + prompt_context + '.' + prompt_admin_level
    if debug:
        print 'prompt:', prompt 

    
    retr = self.ses.expect(prompt, timeout = timeout)
    if retr == 0:
        if debug:
            print 'command successfull'
    elif retr == 1:
        print 'Something broke while executing command!'
        sys.exit(1)
    else:
        print retr
        
    
    if debug:
        print 'setting term length infinite'

    self.ses.sendline('term length infinite')
    
    retr = self.ses.expect(prompt, timeout = timeout)
    if retr == 0:
        if debug:
            print 'command successfull'
    elif retr == 1:
        print 'Something broke while executing command!'
        sys.exit(1)
    else:
        print retr


    
    if debug:
        print 'About to execute the command you requested'
        print 'command:', command
        
    self.ses.sendline(command)
    retr = self.ses.expect(prompt, timeout = timeout)
    if retr == 0:
        if debug:
            print 'command successfull'
    elif retr == 1:
        print 'Something broke while executing command!'
        sys.exit(1)
    else:
        print retr


    raw_rtrn = self.ses.before
    raw_after = self.ses.after
            
    if debug:
        print 'This is what the command returned:'
        print '----------------------------------'
        print raw_rtrn
        print '-------'
        print raw_after
        print '----------------------------------'
    
    if raw:
        # We need to remove the first line of text but it's all one long line
        # so we count the length of the original command and add some for the CR\LF characters
        command_length = len(command) + 2
        return raw_rtrn[command_length:]
    # The 1: tells the system to return everything except the first line
    # The first line contains the command that was executed. 
    else:
        rtrn = raw_rtrn.splitlines()
        return rtrn[1:]


def issu_enable(self, timeout=200):
    """enables ISSU with a set timeout"""
    
    debug = False
    
    if debug:
        print 'now in issu.py method issu_enable'
	
    self.ses.sendline("system issu enable")
    index = self.ses.expect(yesno_prompt_regex,timeout=timeout)
    if index == 0 :
        self.ses.sendline("yes")
        
        if "-con" in self.host:
            self._handle_login(timeout = timeout)
        else:
            time.sleep(timeout)
            self.telnet()
    else :
        print "in enable mode"





def install(self, tree, build, package_name, target_path='/hd/issu', username = 'builder', password = 'fuxor8', linux_ip='10.1.1.101'):
    """Retrieves a package via SFTP from the network and installs the package
       tree = 4.6-prod
       build = 2010011818
       package_name = 4.6A1
       username = builder
       password = password
       full_path (optional) = /auto/build/builder/4.6-prod/2010011818/qnx/cb/mc/StokeOS-4.6A1
       linux_ip = 10.1.1.101 (this is qa-radxpm-1)
    """
    # It's assumed that the host running this script is auto mounting the build directories
    # and that the packages for installation are out there
    # It's also assumed that the SSX (DUT) has network connectivity and can reach the testing host.
    debug = False
    ## Debug
    if debug:
        print 'now in issu.py install'
        
        
    ## Validate arguments
    
    # the only argument we can actually validate is the linux_ip
    # the SSX will only accept an ip address in the sftp command not a hostname
    # so we need to first check to see if it's a hostname and then if not then
    # we can try to convert it. If that failes we must bail
    
    
    if not validIP(linux_ip):
        if debug:
            print 'detected the value linux_ip is not a valid IP address.'
            print 'attempting to do an NS lookup on the hostname'
        linux_ip_tmp = nslookup_by_ip(linux_ip)
        if validIP(linux_ip_tmp):
            linux_ip = linux_ip_tmp
        else:
            print 'invalid IP address or Host Name provided for liux_ip:', linux_ip
            return ("invalid IP address or Host Name provided for liux_ip: %s" % linux_ip)
    
    
    build_dir = '/auto/build/builder/'
    back_half = '/qnx/cb/mc/StokeOS-'
    installed_packages = []
    
    
    ## Need to see is the path /hd/issu exists
    # !!!!!
    command = 'dir ' + target_path
    #result_raw = self.cmd('dir /hd/issu')
    try:
        result_raw = self.cmd(command)
    except:
        print 'Unable to list the ISSU directory'
        print 'System responded'
        self.ses.before()
        self.ses.after()
    result = result_raw.splitlines()
    
    try:
        installed_packages = show_versions(self)
        print 'Completed reading installed packages'
        print 'Found the following versions installed:'
        for item in installed_packages:
            print item
    except:
        print 'Unable to read versions installed'
        return 'Unable to read versions installed'

    
    #####
    # Look to see if the package is already installed
    if package_name in installed_packages:
        # If so then return with a success
        print 'The package:', package_name, 'is already installed on the SSX'
        print 'Installation will be skipped.'
        return(0)
    else:
        print 'The package', package_name, 'will be installed'
    
    # the image name looks like 'StokeOS-4.5B2-2009092913'
    image_name = 'StokeOS-' + package_name + '-' + build 
    
    
    ## We need to see if the file is already on the system
    # to avoid overwriting the file
    images_on_the_system = []
    
    marker_found = False
    
    
    if debug:
        print 'About to parse the dir /hd/issu command'
    
    
    print 'Searching the hard drive for the requested version'
    
    # The result is from the earlier Dir information
    for line in result:
        if len(line) > 0:
            
            """
            if debug:
                print 'Line to be processed:', line
            """
            
        
            # This test will be run for every line
            # but there are only like 8 lines so no big deal
            if 'Unable to access directory' in result:
                # If this fails then something is really messed up!
                command = 'mkdir ' + target_path
                #self.cmd('mkdir /hd/issu')
                self.cmd(command)
            else:
                ## Warning if other files are present then their filenames
                ## will be stored but it should have net zero effect.
                
                # This turns off the storage
                if 'File system:' in line:
                    marker_found = False
                    """
                    if debug:
                        print 'Found end of versions'
                    """
                # This stores the values
                if marker_found:
                    """
                    if debug:
                        print 'Found a version:', word[3]
                    """
                    word = line.split()
                    images_on_the_system.append(word[3])
                # This turns on the storage
                if '--------- -------- ---------- ----' in line:
                    marker_found = True
                    if debug:
                        print 'Found beginning of versions'
    if debug:
        print 'Images installed on the system are:'
        for line in images_on_the_system:
            print line
        print 'We were looking for the following image'
        print image_name 
        
    if image_name in images_on_the_system:
        print 'Image was found on the HD. Will not be coppied over'
    else:
        ## Now we need to actually do the work of copying the package over.
        #####
        
        print 'Image not found on hard drive. It will be retrieved.'
            
        if debug:
            print 'Piecing the parts together'
        # We're already conntecte to the SSX
        # We need to SFTP the file from the linux_ip to the SSX
        # To do that we need to know the full path to the file
        # We have the pieces so we need to assemble them
        
        """
        if debug:
            print 'The full_path variable will contain these parts:'
            print 'build_dir:', build_dir
            print 'tree:', tree
            print 'build:', build
            print 'back_half:', back_half
            print 'package_name:', package_name
        """
        
        # we're re-defining this variable because it was not passed in
        full_path = build_dir + tree + '/' + build + back_half + package_name
        
        
        if debug:
            print 'Full path:', full_path
            print 'Image will be written to the following filename:', image_name
            print 'It will be written to /hd/issu/' + image_name
        
            
        # At this point we have all the pieces to assemble the SFTP command
        """
        cmd = 'copy sftp://' + username + '@' + linux_ip + ':' + full_path + \
           ' /hd/issu/' + image_name
        """
        # added target path for specifiying location to install TO
        cmd = 'copy sftp://' + username + '@' + linux_ip + ':' + full_path + \
           ' ' + target_path + '/' + image_name

        
        
        print 'about to run the command:'
        print cmd
        
        
        ##########
        # Copy the file over
        # Here we run the command using the ftppasswd method
        retr = self.ftppasswd(cmd, password, 210)
        if retr:
            print 'Failed to SFTP the file over. Aborting install!'
            return(1)
        
        if debug:
            print 'Completed sending the new build to the SSX'
        
    
    ###########
    # At this point the file is actually on the SSX and we can attempt to "install" it. 
    #command = 'system install package /hd/issu/' + image_name
    # Added target path
    command = 'system install package ' + target_path + '/' + image_name
    
    if debug:
        print "install command will be: %s" % command
    
    #self.cmd(command)
    #result = self.cmd('yes')
    
    self.ses.sendline("%s" % command)
    index = self.ses.expect(['will be done', 'Install is not permitted'], timeout=30)
    print self.ses.before
    if index == 0:
        print 'recieved YES/NO prompt'
        self.ses.sendline('yes')
        print 'installing package .....'
    elif index == 1:
        print 'ISSU is already in progress. Can not install package!'
        return 'ERROR - Install is not permitted as ISSU Revert is in progress'
    else:
        return 'Failed to install package'
    index = self.ses.expect(['invalid package path or file', 'Installation complete', 'Installed packages maximum limit'], timeout=300)
    if index == 0:
        print 'System unable to install file. Bad filename or path'
        return(1)
    elif index == 1:
        print 'Installation complete!'
        return(0)
    elif index == 2:
        print 'There are too many packages installed. Please manually remove at lest 1.'
        return(1)
    else:
        print 'Timeout while installing package.'
        return(1)
            
def change_version(self, version, method, config_filename='default', ignore_port_down = False):
    """Performs Upgrade, Revert and Select
    """
    
    debug = False
    
    
    # Wait time could be externall exposed if needed
    wait_time = 10
    
    if method not in ('upgrade','revert','select'):
        return "Unsuported method %s" % method
    ###########
    # UPGRADE #
    ###########
    elif method == 'upgrade':
        print 'now in issu.py change_version upgrade'
        versions_installed = show_versions(self)
        if version in versions_installed:
            # Send the upgrade command
            if ignore_port_down:
                if debug:
                    print 'about to run the command:'
                    print "system upgrade package %s ignore-port-down" % version
                self.ses.sendline("system upgrade package %s ignore-port-down" % version)
            else:
                if debug:
                    print 'about to run the command:'
                    print "system upgrade package %s" % version
                self.ses.sendline("system upgrade package %s" % version)
            index = self.ses.expect(['Save configuration to file', 'Package not installed', \
                    'not supported', 'ISSU mode is disabled', 'in inconsistent state', \
                    'Upgrade is in progress', 'No Previous Version'], timeout=wait_time)
            if index == 0:
                if config_filename == 'default':
                    print 'Saving system configuration to default filename'
                    # Press enter to accept the default system prompt
                    self.ses.sendline()
                else:
                    print 'Saving system configuration to:', config_filename
                    # Otherwise put in the filename
                    # Expected format is '/hd/issu-upgd-2010-04-20.cfg'
                    self.ses.sendline(config_filename)
                index_2 = self.ses.expect(['Proceed?', 'ERROR: Slot 0 StokeBloader images',\
                          'ERROR: Slot 1 StokeBloader images', 'ERROR: Slot 2 StokeBloader images', \
                          'ERROR: Slot 3 StokeBloader images', 'ERROR: Slot 4 StokeBloader images'], timeout=wait_time)
                if index_2 == 0:
                    # Use this method because we are expecting the prompt
                    self.cmd('yes')
                    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    print 'system now upgrading to version:', version
                    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    return 0
                elif index_2 == 1:
                    print 'Flash banks do not match.'
                    return 'Flash mismatch at slot 0'
                elif index_2 == 2:
                    print 'Flash banks do not match.'
                    return 'Flash mismatch at slot 1'
                elif index_2 == 3:
                    print 'Flash banks do not match.'
                    return 'Flash mismatch at slot 2'
                elif index_2 == 4:
                    print 'Flash banks do not match.'
                    return 'Flash mismatch at slot 3'
                elif index_2 == 5:
                    print 'Flash banks do not match.'
                    return 'Flash mismatch at slot 4'  
                else:
                    return "Timeout while waiting for proceed prompt"
                    
            elif index == 1:
                # Should be converted to log Error message
                print 'Package not Installed'
                return 'Package not installed'
            elif index == 2:
                # Should be converted to log Error message
                print "Package selected: %s is not supported" %version
                return "Package selected: %s is not supported" %version
            elif index == 3:
                print 'ISSU dissabled on system. Aborting!'
                return 'ISSU dissabled on system. Aborting!'
            elif index == 4:
                print 'ISSU Already in process. Unable to Upgrade!'
                return 'ISSU Already in process. Unable to Upgrade!'
            elif index == 5:
                print 'Upgrade is already in progress'
                return 'upgrade already in progress'
            elif index == 6:
                print 'No Previous version present in ISSU history to revert to'
                return 'previous version not present'
            else: 
                print "Timeout when attempting to %s package %s" % (method, version)
        else:
            print 'Unable to upgrade to version', version
            print 'Package not installed on sysetm'
            return 'Unable to upgrade to package, because it is not installed'
    ##########            
    # REVERT #
    ##########            
    elif method == 'revert':
        if debug:
            print 'in issus.py change_version reverting'    
        self.ses.sendline('system revert package ignore-port-down')
        index = self.ses.expect(['Save configuration to file', 'not supported', 'Pre-Revert Checks Failed', \
                                'ISSU Upgrade is in progress', 'not permitted during ISSU soak phase', \
                                'in inconsistent state'], timeout=wait_time)
        if index == 0:
            if config_filename == 'default':
                # Press enter to accept the default system prompt
                self.ses.sendline()
            else:
                # Otherwise put in the filename
                # Expected format is '/hd/issu-upgd-2010-04-20.cfg'
                self.ses.sendline(config_filename)
            index_2 = self.ses.expect('Proceed?', timeout=wait_time)
            if index_2 == 0:
                # Use this method because we are expecting the prompt
                self.cmd('yes')
                return 0
            if index_2 == 1:
                return "Timeout while waiting for proceed prompt"
        elif index == 1:
            print 'Revert not supported!'
            return 'Revert not supported!'
        elif index == 2:
            print 'Pre-Revert Checks Failed'
            return 0
        elif index == 3:
            print 'ISSU Upgrade is in progress. Revert aborted!'
            return 'ISSU Upgrade is in progress. Revert aborted!'
        elif index == 4:
            print 'not permitted during ISSU soak phase'
            return 'not permitted during ISSU soak phase'
        elif index == 5:
            print 'Action will leave card(s) in inconsistent state'
            print 'This error comes up when the system is still booting right after the cards come to'
            print 'Running State. Please try putting a time.sleep(60) in the code to fix this!'
            self.cmd('no')
            return 'ISSU Action still in process. Action will leave card(s) in inconsistent state;'
        else: 
            print "Timeout when attempting to %s" % method
            
    ##########
    # SELECT #
    ########## 
    elif method == 'select':
        # Due to the fact that they changed the prompts from ISSUv1 to ISSUv2
        # we get the prompts in a different combination and order. 
        # There are several paths through this code. 
        
        
        if debug:
            print 'in issu.py change_version selecting'
            print 'about to run the following command:'
            print "system select package %s" % version
            
        self.ses.sendline("system select package %s" % version)
        
        if debug:
            print 'Command sent. Waiting for response'
        
        index = self.ses.expect(['Select will clear revert history', 'will erase all revert history', 'Proceed?', \
        'Package not installed', 'Select is not permitted during ISSU soak phase', 'same as Current Version', \
        'Save configuration to file'], timeout=wait_time)
        
        if debug:
            print 'Parsing system response'
            
        if (index in [0,1,2]):
            # 'Select will clear revert history'
            # Proceed? (yes/[no])
            self.ses.sendline('yes')
            if index == 2:
                # We got the early proceed prompt from ISSUv1
                return 0

        elif index == 3:
            print 'Package not installed!'
            return 'Package not installed!'
            
        elif index == 4:
            print 'Select is not permitted during ISSU soak phase'
            return 'Select is not permitted during ISSU soak phase'
            
        elif index == 5:
            print 'Requested version is already current version'
            return 0
        
        elif index == 6:
            if config_filename == 'default':
                # Press enter to accept the default system prompt
                self.ses.sendline()
            else:
                # Otherwise put in the filename
                # Expected format is '/hd/issu-upgd-2010-04-20.cfg'
                self.ses.sendline(config_filename)
        else: 
            print self.ses.before()
            print "Timeout when attempting to %s package %s" % (method, version)
            return 'Timeout during Select'
        

        index = self.ses.expect(['Save configuration to file', 'System will be automatically reloaded'], timeout=wait_time)
        if index == 0:
            if config_filename == 'default':
                # Press enter to accept the default system prompt
                self.ses.sendline()
            else:
                # Otherwise put in the filename
                # Expected format is '/hd/issu-upgd-2010-04-20.cfg'
                self.ses.sendline(config_filename)
                
        elif index == 1:
            print 'Save Filename prompt not detected.'
        
        else: 
            print "Timeout when attempting to %s package %s" % (method, version)
            return 'Timeout during Select'
        
        
        index = self.ses.expect('Proceed?', timeout=wait_time)
        if index == 0:
            # Use this method because we are expecting the prompt
            
            self.ses.sendline('yes')
            #self.ssx.cmd('yes')
           
	    if (self.host.find("-con") != -1):
		print('Using console.  Need to wait for Shutdown')  
                index = self.ses.expect('Shutdown', timeout=60)
		if index != 0:
		    print 'System did not shutdown to reboot'
		    return 1	

            # At this point the system is doing a reboot if everything 
            # worked as planned. 
            #time.sleep(1)
            #self.ssx.wait4cards()
            print 'Select command accepted by system'
            print 'System will now reboot the GLC then the IMC'
            print 'After command completes telnet sessions to the system will be lost'
            return 0
        else:
            return "Timeout while waiting for proceed prompt"
            
    # Catch all for change version
    else:
        return "Version requested was not %s" % method
        
        
    
def upgrade(self, version, auto_corect = True):
    """Wrapper function for change_version
    """
    print 'now in issu.py upgrade'
    retr = change_version(self, version, 'upgrade')
    
    # Sometimes the flash does not match on the cards
    # It's easy to correct and not a situation for alarm
    
    bad_flash = False

    if auto_corect:
        print 'Checking to see if there was any flash corruption.'
        
        try:
            return_code = str(retr)
        except:
            print 'unable to cast the return value as a string!'
            return 1
            
        if 'slot 0' in return_code:
            # If it's bad correct the flash corruption
            bad_flash = True
            print 'Correcting flash mismatch'
            command = 'flash commit 0' 
            self.ses.sendline(command)
            retr = self.ses.expect(['PRIMARY bank copied to BACKUP bank.'], timeout = 30)
            if retr == 0:
                print 'Commit passed'
            else:
                print 'unable to correct flash problem on slot 0'
                return 'Corrupt flash image on slot 0'
        elif 'slot 1' in return_code:
            bad_flash = True
            print 'Correcting flash mismatch'        
            command = 'flash commit 1' 
            self.ses.sendline(command)
            retr = self.ses.expect(['PRIMARY bank copied to BACKUP bank.'], timeout = 30)
            if retr == 0:
                print 'Commit passed'
            else:
                print 'unable to correct flash problem on slot 1'
                return 'Corrupt flash image on slot 1'
        elif 'slot 2' in return_code:
            bad_flash = True
            print 'Correcting flash mismatch'        
            command = 'flash commit 2' 
            self.ses.sendline(command)
            retr = self.ses.expect(['PRIMARY bank copied to BACKUP bank.'], timeout = 30)
            if retr == 0:
                print 'Commit passed'
            else:
                print 'unable to correct flash problem on slot 2'
                return 'Corrupt flash image on slot 2'
        elif 'slot 3' in return_code:
            bad_flash = True
            print 'Correcting flash mismatch'
            command = 'flash commit 3' 
            self.ses.sendline(command)
            retr = self.ses.expect(['PRIMARY bank copied to BACKUP bank.'], timeout = 30)
            if retr == 0:
                print 'Commit passed'
            else:
                print 'unable to correct flash problem on slot 3'
                return 'Corrupt flash image on slot 3'                    
        elif 'slot 4' in return_code:
            bad_flash = True
            print 'Correcting flash mismatch'
            command = 'flash commit 4' 
            self.ses.sendline(command)
            retr = self.ses.expect(['PRIMARY bank copied to BACKUP bank.'], timeout = 30)
            if retr == 0:
                print 'Commit passed'
            else:
                print 'unable to correct flash problem on slot 4'
                return 'Corrupt flash image on slot 4'
        else:
            print 'No flash corruption detected.'
        
        # Then try to upgrade the system
        if bad_flash:
            print 'Attempting to upgrade the package again.'
            retr = change_version(self, version, 'upgrade')
                
    print 'now returning from issu.py upgrade'
    return retr
    

def revert(self):
    """Wrapper function for change_version
    """
    if debug:
        print 'Now in issu.py revert'
    version = 'NA'
    retr = change_version(self, version, 'revert')
    return retr

def select(self, version):
    """Wrapper function for change_version
    """
    retr = change_version(self, version, 'select')
    return retr
    
def status(self, slot_filter='all'):
    """Runs "show upgrade status" and parses the output
       returns a dictionary of card status
    """
    debug = False
    if debug:
        print 'now in issu.py status'
    
    # instantiate a dictionary to store the return data
    status_dict = {}
    
    # get the status
    raw_output = self.cmd('show upgrade status')
    
    # Check for ISSUv1
    issu_v1 = False
    
    ## Sample output
    """
    australia[local]#show upgrade status
    01 ISSU Operation:Upgrade
    02 
    03 Slot StokeOS Ver Upgrade Status
    04 ---- ----------- --------------------------------------------- 
    05   0 4.6B1       In-Progress(Flashing Started)
    06   1 4.6B1S1     Complete
    07   2 4.6B1       Not Started
    08   3 4.6B1       Not Started
    09   4 4.6B1       Not Started
    """
    
    # Sometimes it looks like this
    """
    australia[local]#show upgrade status
    01 ISSU Operation:Upgrade
    02 System is currently in ISSU soak phase
    03 
    04 Slot StokeOS Ver Upgrade Status
    05 ---- ----------- --------------------------------------------- 
    06   0 4.6B1       In-Progress(Flashing Started)
    07   1 4.6B1S1     Complete
    08   2 4.6B1       Not Started
    09   3 4.6B1       Not Started
    10   4 4.6B1       Not Started
    """
    
    # If your running an ISSUv1 build it looks like this
    """
    01 Slot   Upgrade Status
    02 ----   --------------
    03  0  Not Started 
    04  1  Not Started 
    05  2  Not Started 
    06  3  Not Started 
    07  4  Not Started 
    """

    
    # chop the output into lines
    output = raw_output.splitlines()
    """
    if debug:
        print 'Number or lines in output:', len(output)
        for line in output:
            print 'line:', line
    """
    
            
    if (len(output) > 2):
        # the data we care about is on lines 1, 5-9
        
        ## Line 1
        line_1 = output[1].rstrip()
        if (len(line_1) > 2):
            #words = output[1].split()
            words = line_1.split()
            """
            if debug:
                print 'The first line contains:', words
            """
            
            if words[0] == 'ISSU':
                ## ('ISSU', 'Operation:Upgrade')
                issu_status = words[1].split(':')
                ## ('Operation','Upgrade')
                status_dict['ISSU Status'] = issu_status[1]
                """
                if debug:
                    print 'The status detected was', status_dict['ISSU Status'] 
                """
            
            elif 'Upgrade' in line_1:
                #status_dict['ISSU Status'] = 'upgrade'
                status_dict['status'] = 'upgrade'
            elif 'Revert' in line_1:
                #status_dict['ISSU Status'] = 'revert'
                status_dict['status'] = 'revert'
            elif 'Slot' in line_1:
                print '@@@@@@@@ Detected system running ISSUv1 @@@@@@@@@'
                print 'ISSU automation not capable of parsing the output at this time'
                issu_v1 = True
                return 'Unknown Status'
            else:
                print 'Failure in issu.py status. Unknown status:', line_1
                print line_1
                return 'Unknown Status'
        ## Line 2
        line_2 = output[2].rstrip()
        if (len(line_2) > 2):
            words = line_2.split()
            if 'soak' in words: 
                status_dict['ISSU Status'] = 'soak phase'
        
        # The lenght of the output changes because they remove a line of text
        # this leads to missing card 0 sometimes. 
        # we must go look for that seperator line then
        start_line = 0
        for raw_line in output:
            start_line = start_line + 1
            if '-----------' in raw_line:
                break
        """
        if debug:
            print 'The first line we care about should be:'
            print output[start_line]
        """
            
        if issu_v1:
            for raw_line in output[start_line:]:
                if debug:
                    print 'Line to be processed is:'
                    print raw_line
                
                local_dict = {}
                line = raw_line.lstrip()
                words = line.split(' ',2)
                
                slot = "slot %s" % words[0]
                
                if debug:
                    print 'slot #', words[0]

                local_dict['status'] = words[2].lstrip()
                
                if debug:
                    print 'status:', words[2].lstrip()

                status_dict[slot] = local_dict                

            if debug:
                print 'The status_dict contains:', status_dict

                
        else:
            ## Remaining lines
            # Ths odd notation means take all the lines from 4 onward
            for raw_line in output[start_line:]:
                
                if debug:
                    print 'Line to be processed is:'
                    print raw_line
                
                local_dict = {}            
                #status = []
                line = raw_line.lstrip()
                words = line.split(' ',2)
                 
                local_dict['version'] = words[1]
                
                if debug:
                    print 'version:', words[1]
                
                local_dict['status'] = words[2].lstrip()
                
                if debug:
                    print 'status:', words[2].lstrip()
                
                slot = "slot %s" % words[0]
                
                if debug:
                    print 'slot #', words[0]
                
                status_dict[slot] = local_dict
                
                if debug:
                    print status_dict
                
            
            if debug:
                print 'The status_dict contains:', status_dict
            
            
            
        # we have now parsed all the data. Now to return what the user wants
        if slot_filter == 'all':
            """
            if debug:
                print 'returning the whole dictionary'
            """
            return status_dict
        elif slot_filter in status_dict.keys():
            if debug:
                print '=================================='
                print 'Detected filter on:', slot_filter
                print 'The filtered dictionary contains:'
                print status_dict[slot_filter]
                print '=================================='
            return status_dict[slot_filter]
        else:
            return "Invalid slot. Expected: %s" % status_dict.keys()
    else:
        # The ISSU is not in process. Return a Pass value of 0
        return status_dict
        
def install_status(self, slot_filter='all'):
    """Pulls the ISSU status of the install
       returns a dictionary of card status
    """
    debug = False
    
    if debug:
        print 'now in issu.py status'
    
    # instantiate a dictionary to store the return data
    status_dict = {}
    
    # get the status
    raw_output = self.cmd('show upgrade status')
    
    ## Sample output
    """
    australia[local]#show upgrade status
    01 ISSU Operation:Upgrade
    02 
    03 Slot StokeOS Ver Upgrade Status
    04 ---- ----------- --------------------------------------------- 
    05   0 4.6B1       In-Progress(Flashing Started)
    06   1 4.6B1S1     Complete
    07   2 4.6B1       Not Started
    08   3 4.6B1       Not Started
    09   4 4.6B1       Not Started
    """
    
    # Sometimes it looks like this
    """
    australia[local]#show upgrade status
    01 ISSU Operation:Upgrade
    02 System is currently in ISSU soak phase
    03 
    04 Slot StokeOS Ver Upgrade Status
    05 ---- ----------- --------------------------------------------- 
    06   0 4.6B1       In-Progress(Flashing Started)
    07   1 4.6B1S1     Complete
    08   2 4.6B1       Not Started
    09   3 4.6B1       Not Started
    10   4 4.6B1       Not Started
    """

    
    # chop the output into lines
    output = raw_output.splitlines()
    """
    if debug:
        print 'Number or lines in output:', len(output)
        for line in output:
            print 'line:', line
    """
    
            
    if (len(output) > 2):
        # the data we care about is on lines 1, 5-9
        
        ## Line 1
        line_1 = output[1].rstrip()
        if (len(line_1) > 2):
            #words = output[1].split()
            words = line_1.split()
            """
            if debug:
                print 'The first line contains:', words
            """
            
            if words[0] == 'ISSU':
                ## ('ISSU', 'Operation:Upgrade')
                issu_status = words[1].split(':')
                ## ('Operation','Upgrade')
                status_dict['ISSU Status'] = issu_status[1]
                """
                if debug:
                    print 'The status detected was', status_dict['ISSU Status'] 
                """
            
            if 'Upgrade' in line_1:
                status_dict['ISSU Status'] = 'upgrade'
            elif 'Revert' in line_1:
                status_dict['ISSU Status'] = 'revert'
            else:
                print 'Failure in issu.py status. Unknown status:', line_1
                print line_1
                return 'Unknown Status'
        ## Line 2
        line_2 = output[2].rstrip()
        if (len(line_2) > 2):
            words = line_2.split()
            if 'soak' in words: 
                status_dict['ISSU Status'] = 'soak phase'
        
        # The lenght of the output changes because they remove a line of text
        # this leads to missing card 0 sometimes. 
        # we must go look for that seperator line then
        start_line = 0
        for raw_line in output:
            start_line = start_line + 1
            if '-----------' in raw_line:
                break
        """
        if debug:
            print 'The first line we care about should be:'
            print output[start_line]
        """
            
        
        ## Remaining lines
        # Ths odd notation means take all the lines from 4 onward
        for raw_line in output[start_line:]:
            """
            if debug:
                print 'Line to be processed is:'
                print raw_line
            """
            local_dict = {}            
            #status = []
            line = raw_line.lstrip()
            words = line.split(' ',2)
            local_dict['version'] = words[1]
            """
            if debug:
                print 'version:', words[1]
            """
                
            local_dict['status'] = words[2].lstrip()
            """
            if debug:
                print 'status:', words[2].lstrip()
            """
            slot = "slot %s" % words[0]
            """
            if debug:
                print 'slot #', words[0]
            """
            status_dict[slot] = local_dict
            """
            if debug:
                print status_dict
            """
        
        if debug:
            print 'The status_dict contains:', status_dict
        
            
        # we have now parsed all the data. Now to return what the user wants
        if slot_filter == 'all':
            """
            if debug:
                print 'returning the whole dictionary'
            """
            return status_dict
        elif slot_filter in status_dict.keys():
            if debug:
                print '=================================='
                print 'Detected filter on:', slot_filter
                print 'The filtered dictionary contains:'
                print status_dict[slot_filter]
                print '=================================='
            return status_dict[slot_filter]
        else:
            return "Invalid slot. Expected: %s" % status_dict.keys()
    else:
        # The ISSU is not in process. Return a Pass value of 0
        return status_dict
    
def wait_issu(self, max_time = 2400, poll_interval=5):
    """Polls the system during upgrade/revert waiting for ISSU to complete
    """
    complete = False
    issu_status = status(self)
    debug = False
    
    """
    if debug:
        print 'This is what we got back from the status function'
        print issu_status
    """
    try:
        card_list = issu_status.keys()
    except:
        print 'unable to parse the status of the system.'
        return 'Failed to get status'
    
    """
    if debug:
        print 'this is our list of keys from that dictionary'
        print card_list
    """
    
    number_of_cards = len(card_list)
    if issu_status.has_key('ISSU Status'):
        print 'Detected system in ISSU.'
        number_of_cards = number_of_cards - 1
    
    ## Debug
    #print 'Now in wait_issu function!'
    #print 'The value of debug is:', debug
    """
    if debug:
        print 'Card list contains:', card_list
        print 'Detected', number_of_cards, 'cards'
    """
    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    print 'Waiting for the ISSU process to complete.'
    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    
    # This line is used for the aut-revert functions. It was interfering with
    # the normal upgrade and revert functions and needs to be re-written. 
    done = ['Complete', 'Not Started', 'Auto-Revert Complete']
    auto_reverting = False
        
    while not complete:
        time.sleep(poll_interval)
        issu_status = status(self)
        card_pass_count = 0
        for card in card_list:
            if card == 'ISSU Status':
                if issu_status['ISSU Status'] == 'Complete':
                    print 'Detected ISSU status complete'
                # Need to figure out if the system is in auto revert
                # This might be the right string
                elif issu_status['ISSU Status'] == 'Auto Revert':
                    print 'Detected systm is Auto Reverting'
                    auto_reverting = True
                    debug = True
                else:
                    print 'ISSU Status is:', issu_status['ISSU Status']
                    if debug:
                        print 'Please look for auto revert status and update,'
                        print 'issu.py function wait_issu to include exact auto revert string'
            elif (not issu_status.has_key('ISSU Status')):
                    # when that field disapears then it's done
                    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    print '^^^^^^^ ISSU Process Complete ^^^^^^^^^^^'
                    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
                    return 0
                    #complete = True
                    #break
            else:
                if debug:
                    print 'checking' , card, 'for status'
                
                #if issu_status[card]['status'] == 'Complete':
                if debug:
                    print 'About to see if the card:', card, 'is in one of these states:', done
                    print 'ISSU status for this card is reported as:',  issu_status[card]['status']
                    
                print card, ':', issu_status[card]['status']
                
                # This branch is for normal upgrade and revert
                if issu_status[card]['status'] in 'Complete':
                    if debug:
                        print '!!!! Detected card complete !!!!'
                    #print 'card', card, 'Complete'
                    card_pass_count = card_pass_count + 1
                    #If the system is in auto-rever then a "not-started" is also done
                    # Code needs to be updated to fix this. 
                
                elif 'Auto-Revert' in issu_status[card]['status']:
                    print 'Detected system in Auto-Revert via card status'
                    auto_reverting = True
                
                # This branch is for auto-reverting
                elif auto_reverting:
                    if debug:
                        print 'Now in auto-revert detection loop'
                    if issu_status[card]['status'] in done:
                        if debug:
                            print '!!!! Detected card complete !!!!'
                        card_pass_count = card_pass_count + 1
                    else:
                        print 'Card was not Done. It was:', issu_status[card]['status']
                else:
                    if debug:
                        print 'Card was not done ---'
                    print card, 'Status:', issu_status[card]['status']
                    #break

        print 'Card pass rate:', card_pass_count
        if card_pass_count == number_of_cards:
            print 'Detected all cards complete'
            complete = True
                    
        if issu_status.has_key('ISSU Status'):
            if issu_status['ISSU Status'] == 'soak phase':
                print 'Detected Soak Phase. Waiting for soak to complete.'
                complete = False
                
        # timer to make sure th polling will eventually finish        
        max_time = max_time - poll_interval
        print 'Time left:', max_time
        
        if max_time < 1:
            print 'Maximum polling time was exceeded!'
            print 'System never completed ISSU'
            return 'Timeout whill polling. Excessive time'
    
    return 0


            
def install_base(self, base_version, username = 'regress', password = 'gleep7', linux_ip = '10.1.1.101'):
    """This method is used to return the running system to a known base version prior 
       to begining normal ISSU testing. It uses the methods of install and select to 
       do this.
       self = self.ssx (SSX object)
       base_version = ['package_name':'4.7', 'build':'2010022188','tree':'4.7']
    """
    
    
    # Two branches
    # 1. If the version it's running now is not the same version then we can
    #    simply install the base version and select over to it
    # 2. The other possibility is the version it's running is not the same build ID
    #    meaning you are testing a newer or older build of the same version. 
    #    to install and select to this we must:
    #  A. Install a known good older version
    #  B. Select down to that version
    #  C. Uninstall the old package
    #  D. Install the new package
    #  E. Select to the new package
    
    if debug:
        print '----------------------------'
        print 'now in issu.py install_base'
        
    if not(username == 'regress'):
        print 'Non default username detected:', username
    if not(password == 'gleep7'):
        print 'Non default password detected:', password
    if not (linux_ip == '10.1.1.101'):
        print 'Non default linux_ip detected:', linux_ip
    
    running_ver = self.get_version()
    
    print 'System will be selected back to the base version'
    print 'Base version is:', base_version
    print 'running version is:', running_ver
    
    if debug:
        print 'testing for:', running_ver['branch'], '=', base_version['package_name']
    
    if (running_ver['branch'] == base_version['package_name']):
        if debug:
            print 'Detected that the running version name is the same as the base'
        # If the version we want to install is the same as the running version but the 
        # build ID is different then we need to do case 2 above.
        if not (running_ver['build'] == base_version['build']):
            if debug:
                print 'Build ID is different then running version.'
                print 'System will:'
                print '1. Select to older version'
                print '2. Remove old build'
                print '3. Install base version'
                print '4. Select to base version'
            ## Write code here!
            pass
        
        else:
            # If the package name and the build ID are the same then We're already
            # running the correct version. Just return 
            print 'The build ID is also the same. System now at base version.'
            return(0)
    
    
    else:
    # This is the simpler path case 1 above
        if debug:
            print 'The system is not running the base version.'
            print 'Sysetm will be installed with base version'
        
        ##########
        # Install
        print("About to install version %s" % base_version)
        retr = install(self, tree = base_version['tree'], \
                       build = base_version['build'], \
                       package_name = base_version['package_name'], \
                       username = username, \
                       password = password, \
                       linux_ip = linux_ip)
        print("install returned %s" % retr)

        if retr:
            print 'Something went wrong. Returning'
            return retr
        
        ########
        # Select
        print 'Base version now installed.'
        print 'Selecting to base version (reboot)'
        retr = select(self, base_version['package_name'])
        
        if retr:
            print 'Something went wrong. Returning'
            return retr
        else:
            return 0
            """
            print 'System performing select now.'
            print 'Please reconnect after reload'
        return 0
        """

        """
        reboot_time = 120
        print("waiting for the system to finish rebooting: %s seconds" % reboot_time)
        time.sleep(reboot_time)
        rebooting = True
        retries = 20
        while rebooting:
            print('Sleeping for 30 seconds')
            time.sleep(30)
            try:
                print 'Connecting to SSX'
                self.ssx.telnet()
                print 'Made it past the telnet command'
                # if that command does not fail then the rebooting state should change
                rebooting = False  
            except:
                print('System not up yet')
            retries = retries - 1
            print("%s retries left" % retries)
            if retries == 0:
                print("System never came back up after select!")
                sys.exit(1)
        
        print 'Completed Select to base version'
        """
        return 0
    
    

          
def check_session_traffic(self, username_list = 'all', poll_time = 10):
    """This function will use the session_counters method to pull all the active sessions.
       Then it will check session by session to see if the counters are increasing. 
       We expect some sessions will not be sending traffic. To handle that the function accepts
       a list of sessions to check. The calling program is responsible to remove items from that 
       list once they have been detected to no longet be sending traffic. 
    """
    # Accumulate the result here.
    # At the end filter based on requested usernames. 
    result = {}
    
    if username_list == 'all':
        print 'All Sessions will be examined'
        print 'Polling the session counters'
        baseline = session_counters(self)
        print 'Waiting:', poll_time, 'seconds'
        time.sleep(poll_time)
        delta = session_counters(self)
        print 'Computing the delta'
        

    else:
        print 'Select sessions will be examined'
        print 'Polling the session counters'
        # This is all the data
        raw_baseline = session_counters(self)
        print 'Waiting:', poll_time, 'seconds'
        time.sleep(poll_time)
        # this is all the data
        raw_delta = session_counters(self)
        print 'Computing the delta'
    
        baseline = {}
        delta = {}
        # Now we filter it before doing accounting
        for username in raw_baseline:
            if username in username_list:
                baseline[username] = raw_baseline[username] 
                
        # And we filter the detla as well. 
        for username in raw_delta:
            if username in username_list:
                delta[username] = raw_delta[username]
                
    if len(baseline):
        print 'Found sessions'
    else:
        print 'No Sessions are active!'
        return 'No Sessions are active!'
    # At this point we have all the data required we just need to parse it. 
    session_list = baseline.keys()
    
    print 'The following sessions will be parsed:', session_list
    
    active_sessions = 0
    inactive_sessions = 0
    total_sessions = len(session_list)
    print 'Detected', total_sessions, 'Sessions'
    for username in session_list:
        if delta.has_key(username):
            # Reset the local variables
            xmit_active = False
            rcv_active  = False
            # Check the TX
            if baseline[username]['Xmit Bytes'] < delta[username]['Xmit Bytes']:
                xmit_active = True
            # Check the RX
            if baseline[username]['Rcv Bytes'] < delta[username]['Rcv Bytes']:
                rcv_active = True
            
            # Store the results. 
            if xmit_active and rcv_active:
                result[username] = 'Active'
                active_sessions = active_sessions + 1
            elif xmit_active:
                result[username] = 'Xmit only'
                active_sessions = active_sessions + 1
            elif rcv_active:
                result[username] = 'Rcv only'
                active_sessions = active_sessions + 1
            else:
                result[username] = 'Inactive'
                inactive_sessions = inactive_sessions + 1
            
            
        else:
            print 'The following session dropped out while polling'
            print baseline[username]
            # We'll count that dropped one as an inactive session
            inactive_sessions = inactive_sessions + 1
        
    result['Active Sessions'] = active_sessions
    result['Inactive Sessions'] = inactive_sessions
    # note the variable must be cast as a float to actually get a decimal result. 
    result['Percent Active'] = 100 * (float(active_sessions) / total_sessions)
    result['Percent Inactive'] = 100 * (float(inactive_sessions) / total_sessions)
    return result
    
def show_card_state(self):
    """Simple command runs "show card" and parses the output then returns it:
    Here is a sample Dictionary output:
    
    {'Status': 'Complete', 
    'slot 2': 
        {'serial_number': '0130901190900001', 
        'state': 'Running', 
        'hw_rev': '09.01', 
        'type': 'GLC2', 
        'model_name': '4x1000Base-X'}, 
    'slot 3': 
        {'serial_number': '0110323060000110', 
        'state': 'Running', 
        'hw_rev': '02.07', 
        'type': 'GLC1', 
        'model_name': '4x1000Base-X'}, 
    'slot 0': 
        {'serial_number': '0020905420820003', 
        'state': 'Running(Active)', 
        'hw_rev': '09.05', 
        'type': 'IMC1', 
        'model_name': 'Stoke IMC1'}, 
    'slot 1': 
        {'serial_number': '0020140050000026', 
        'state': 'Running(Standby)', 
        'hw_rev': '05.02', 
        'type': 'IMC1', 
        'model_name': 'Stoke IMC1'}, 
    'slot 4': 
        {'serial_number': '0130114060000035', 
        'state': 'Running', 
        'hw_rev': '02.05', 
        'type': 'GLC2', 
        'model_name': '4x1000Base-X'}}

    NOTE: Dictionary is not Sorted
    """
    debug = False
    status_dict = {}
    
    command = "show card"
    raw_card_response = self.cmd(command)
    
    if len(raw_card_response) > 0:
        card_response = raw_card_response.splitlines()
                # There could be a test right here to make sure the lines are present
        # or we got an error message
        if 'ERROR:' in card_response[1]:
            print 'Detected an error when running: show card'
            print 'Returned text was:'
            print raw_card_response
            status_dict['Status'] = 'Error'
            return status_dict
            
        if debug:
            print 'The following lines will be processed:'
            print card_response[3:]
            print '======================================'
            
        # We don't really want the two header lines so we omit them
        for line in card_response[3:]:
            if debug:
                print 'This is the line to process:', line
            words = line.split()
            local_dict = {}
            if len(words) == 7:
                slot = words[0]
                local_dict['type'] = words[1]
                local_dict['state'] = words[2]
                local_dict['serial_number'] = words[3]
                local_dict['model_name'] = words[4] + ' ' + words[5]
                local_dict['hw_rev'] = words[6]
            elif len(words) == 6:
                slot = words[0]
                local_dict['type'] = words[1]
                local_dict['state'] = words[2]
                local_dict['serial_number'] = words[3]
                local_dict['model_name'] = words[4] 
                local_dict['hw_rev'] = words[5]
            else:
                print 'This line has too many/few elements', len(words)
                print words
                status_dict['Status'] = 'Error'
                return status_dict
            current_slot = 'slot ' + slot
            status_dict[current_slot] = local_dict
        status_dict['Status'] = 'Complete'
        return status_dict
        
def wait_for_cards(self, timeout = 360, poll_time = 10):
    """Waits for ALL cards to come to a running state by polling the system.
       This is a rewrite of device.py wait4cards and should be used as a replacement. 
    """
    debug = False
    if debug:
        print 'now in issu.py wait_for_cards'
    
    print 'System is now waiting for all cards to come to a running state'
    print 'Status will be updated every', poll_time, 'seconds'
    
    running = ['Running(Active)','Running(Standby)', 'Running']
    total_wait = 0
    
    # This will run until either the timout is reached or an error occurs or all cards
    # come to a running state
    while True:
        print '------------------------'
        running_card_count = 0
        running_card_list = []
        current_card_state = show_card_state(self)
        if current_card_state['Status'] == 'Complete':
            if debug:
                print 'was able to retrieve current card state'
                print 'now processing'
            card_list = current_card_state.keys()
            if debug:
                print 'Detected the following cards:', card_list
            for card in card_list:
                if not (card == 'Status'):
                    card_state = current_card_state[card]['state']
                    if card_state in running:
                        #print card, 'Has come to running state'
                        running_card_count = running_card_count + 1
                        running_card_list.append(card)
                    if running_card_count == (len(card_list) - 1):
                        print 'All cards have come to running state.'
                        print 'Total wait time was', total_wait
                        return 0
        else:
            return 'Failed to retrieve card state'
        
        try:
            print 'ISSU Status:', current_card_state['Status']
        except:
            print 'No ISSU Status to report'
        print 'The following cards are running', running_card_list
        print 'Elapsed time:', total_wait, 'seconds'
        time.sleep(poll_time)
        total_wait = total_wait + poll_time
        timeout = timeout - poll_time
        if timeout < 1:
            return 'Timeout while polling system'
            
def all_cards_running(self, debug=False):
    """Uses the method show_card_state to verify all cards are running. Returns True/False
       Designed as simple test to be run at the begining/end of tests. 
       Does not wait for cards. 
       
       If you want to see some output use the debug option!
    """
    if debug:
        print 'now in issu.py method all_cards_running'
        
    # This checks to see if any of the cards are in an "error" state
    card_state = show_card_state(self)
    # We don't need this record
    del card_state['Status']
    
    if debug:
        print 'here is the raw dictionary'
        print card_state
        print 'here is the card information'
        
    for card in card_state:
        if debug:
            print card_state[card]
        if 'Running' in card_state[card]['state']:
            if debug:
                print 'Card:', card, 'is in running state'
        else:
            if debug:
                print 'Card', card, 'is NOT in running state. FAIL'
            #self.fail("Card %s is NOT in running state" % card)
            return False
    
    return True
            
                    

def kill_pid(self, raw_pid='none', raw_slot=0):
    """Method kills processes by PID only
    """
    slot_range = [0,1,2,3,4]
    
    # Validate the input
    if raw_pid == 'none':
        return 'No PID Provided!'
    try:
        pid = int(raw_pid)
    except:
        print 'PID value not an Integer:', raw_pid
        return 'Non integer value for PID'
    try:
        slot = int(raw_slot)
    except:
        print 'Invalid value for slot:', raw_slot
        print 'Was expecting an integer.'
    if not (slot in slot_range):
        print 'Invalid value for slot:', slot
        print 'Must be in range:', slot_range
    
    # Build the command
    command = 'process coredump ' + str(slot) + ' ' + str(pid)
    if debug:
        print 'The command will be:', command
        
    self.ses.sendline("%s" % command)
    index = self.ses.expect(['Continue'], timeout=30)
    print self.ses.before
    if index == 0:
        self.cmd('yes') 
    else:
        print 'Failed to send core dump command!'
        return 'Failed'
    
    return 0
    
def list_ike_sessions(self, slot = 'all'):
    """Uses "show ike-session list" or "show ike-session SLOT_NUMBER list" 
    to get ike-session details. Then returns the output 
    """
    debug = False
    slot_range = [0,1,2,3,4,'all']
    # We will accumulate all the sesion information into this list
    return_session_list = []
    expected_values = ['SLOT','Session Handle','IKE Version','Remote IP',\
                       'IKE-SA ID','Session Addr','Session State']
    
    # Example input
    """
    australia[local]#show ike-session list
    01 Mon Jun 21 16:11:20 PDT 2010.
    02
    03 -------------------------------------------------------------------------------
    04 SLOT           : 2
    05 Session Handle : fc440200
    06 IKE Version    : 2
    07 Remote IP      : 10.11.2.1
    08 IKE-SA ID      : 16502102800650210@r2
    09 Session Addr   : 172.1.0.1
    10 Session State  : IPSEC-ESTABLISHED, IKE-SA DONE, CHILD-SA MATURE
    11 -------------------------------------------------------------------------------
    12
    13 -------------------------------------------------------------------------------
    14 SLOT           : 3
    15 Session Handle : f4480200
    16 IKE Version    : 2 <LAN<->LAN>
    17 Remote IP      : 10.11.3.1
    18 IKE-SA ID      : sswan
    19 Session State  : IPSEC-ESTABLISHED, IKE-SA DONE, CHILD-SA MATURE
    20 -------------------------------------------------------------------------------
    21
    """
    
    # Example return value:
    """
    [{'SLOT': ' 2', 'Session Addr': ' 172.1.0.1', 'IKE-SA ID': ' 16502102800650210@r2', 
      'IKE Version': ' 2', 'Session Handle': ' fc440201', 'Remote IP': ' 10.11.2.1', 
      'Session State': ' IPSEC-ESTABLISHED, IKE-SA DONE, CHILD-SA MATURE'}]
    """
    
    if not (slot in slot_range):
        print 'Invalid Slot ID provided for filtering:', slot
        return 'Invalid Slot ID provided for filtering:', slot
        
    if slot == 'all':
        command = 'show ike-session list'
    else:
        command = 'show ike-session ' + str(slot) + ' list'
    if debug:
        print 'The command will be:', command
    
    raw_session_list = self.cmd(command)
    session_list = raw_session_list.splitlines()
    if debug:
        print 'The raw data returned from the command was:'
        print raw_session_list
    
    if session_list[1] == 'ERROR: No sessions found on any Card':
        print 'No Sessions present'
        return 'No Sessions present'
    # So we know that the first line which is line 0 is thrown away by our cmd API
    # The first available line is line 1 which contains the date. We don't want that.
    # Line 2 contains a space which is also useless to us.
    # So we'll start parsing at line 3
    in_block = False
    local_session_dict = {}

    for line in session_list[2:]:
        
        # Look for the start. 
        if '---' in line:
            if in_block == True:
                # If we find a second one it's the end
                in_block = False
                # Now we need to stuff this info into the list we return
                if debug:
                    print 'Appending the local_sesions_dict containing:'
                    print local_session_dict
                    print 'To the return_session_list which contains:'
                    print return_session_list
                return_session_list.append(local_session_dict)
                if debug:
                    print 'Found the end of the block'
                # Flush the local_session_dict for the next block
                local_session_dict = {}
            else:
                if debug:
                    print 'Found the beging of the block'
                in_block = True
        elif in_block:
            words = line.split(':')
            if debug:
                print 'Split words are:', words  
            paramater = words[0].rstrip()
            if debug:
                print 'Stripped paramater is:', paramater
            if paramater in expected_values:
                # We simply store it in a local dictionary indexed on it's name
                if debug:
                    print 'Found a paramater we expected:', paramater
                    print 'Storing it in the local_session_dict'
                local_session_dict[paramater] = words[1].lstrip()
                if debug:
                    print 'The local_session_dict contains:', local_session_dict
            else:
                print 'Got back a value we did not expect:', words[0]
                print 'Please modify issu.py list_ike_sessions expected_values list to include this!'
        """
        else:
            print 'line contains:', line
        """
    
    print 'Succesfully parsed session list'
    return return_session_list
        

    
def list_tunnels(self):
    """Simply parses the 'show tunnel' output
    """
    debug = False
    return_list = []
    lines_to_parse = []
    # Example Input
    """
    01 Name                                        CctHdl   Type       Admin   State
    02 ------------------------------------------- -------- ---------- ------- -------
    03 tun1                                        ce000002 lan2lan:ip44 enable  up
    04 1 objects displayed.
    """
    
    # Example output
    """
    [{'CctHdl': 'ce000002', 'admin': 'enable', 'state': 'up', 'type': 'lan2lan:ip44', 'name': 'tun1'}]
    """
    
    # It looks like the last line contains the number of tunnels configured.

    if debug:
        print 'Now in issu.py list_tunnels'
    command = 'show tunnel'
    raw_input = self.cmd(command)
    show_tunnel_list = raw_input.splitlines()
    
    # There needs to be some error checking here but I don't know what the bad input looks like yet
    
    if len(show_tunnel_list) < 4:
        print 'Detected no tunnels configured!'
        print 'Please review this raw ouptut.'
        print raw_input
        return 'No tunnels configured'
        
    number_of_tunnels = len(show_tunnel_list) - 4
    
    if debug:
        print 'Detected', number_of_tunnels, 'Tunnels'
        
    # This builds up a list of lines we care about
    lines_to_parse = range(3, (number_of_tunnels + 3))
    
    if debug:
        print 'The following lines will be parsed:', lines_to_parse
        
    for line_number in lines_to_parse:
        line = show_tunnel_list[line_number]
        local_dict = {}
        if debug:
            print 'The raw line is:'
            print line
        words = line.split()
        
        local_dict['name'] = words[0]
        local_dict['CctHdl'] = words[1]
        local_dict['type'] = words[2]
        local_dict['admin'] = words[3]
        local_dict['state'] = words[4]
        if debug:
            print 'local_dict contains:'
            print local_dict
        return_list.append(local_dict)
        if debug:
            print 'return_list contains:'
            print return_list
        
    print 'Completed parsing "show tunnel" command'
    return return_list
        
    
def valid_month(month):
    """
    verifies the input is a valid 3 character month like "jan", "feb" ...
    """
    debug = False
    
    if debug:
        print 'verifying month is valid', month 

    if month in month_list:
        if debug:
            print 'Valid month detected:', month 
        return True
    else:
        if debug:
            print 'Invalid Month supplied:', month
            print 'Month must be one of the following:'
            print month_list
        return False


def valid_day_of_month(day_of_month):
    """
    verifies the input is a valid day of the month as an integer like "23"
    """
    debug = False
    ###############
    ## Day of month

    try:
        num_day = int(day_of_month)
    except:
        print 'Day of month is not an integer. OOPS!'
        return False
    if not(num_day in range(1, 32)):
        print 'invalid number for day_of_month:', day_of_month
        return False    
    elif len(day_of_month) == 0:
        print 'No day of month value provided'
        return False
    else:
        if debug:
            print 'Valid day of month detected:', day_of_month
        return True 

def valid_hour(hour):
    """
    verifies the input is a valid hour of the day like "12"
    """
    
    debug = False

    try:
        num_hour = int(hour)
    except:
        print 'Hour is not an integer:', hour
        return False
    if not(num_hour in range(0,24)):
        print 'There are only 24 hours in the day. Value too large!'
        return False
    elif len(hour) == 0:
        print 'No hour value provided!'
        return False
    else:
        if debug:
            print 'Valid hour detected:', hour 
        return True


def valid_minute(minute):
    """
    verifies the input is a valid minute like "01" or "24"
    """
    
    debug = False

    try:
        num_minute = int(minute)
    except:
        print 'Non numeric value for minute caught:', minute
        return False
    if not (num_minute in range(0, 60)):
        print 'Only 60 mintues in an hour. Invalid minute value caught:', minute
        return False
    if not (len(minute) == 2):
        print 'minute must contain two digits:', minute
        return False
    else:
        if debug:
            print 'Valid minute detected:', minute 
        return True
    

def valid_second(seconds):
    """
    verifies the input is a valid second like "01" or "24"
    """
    
    debug = False
    
    try:
        num_seconds = int(seconds)
    except:
        print 'Non numeric value for seconds caught:', seconds
        return False
    if not (num_seconds in range(0, 60)):
        print 'Only 60 mintues in an hour. Invalid seconds value caught:', seconds
        return False
    if not (len(seconds) == 2):
        print 'seconds must contain two digits:', seconds
        return False
    else:
        if debug:
            print 'Valid second detected:', seconds 
        return True

def validIP(address):
    debug = False
    
    if debug:
        print 'now in validIP in issu.py'
        print 'length of address:', len(address)
    
    
    try:
        parts = address.split(".")
    except:
        if debug:
            print 'unable to split the address:', address 
        return False
    if len(parts) != 4:
        if debug:
            print 'there are not four octests', address 
        return False
    first_octet = parts[0]

    try:
        int(first_octet)
    except:
        if debug:
            print 'first octet is not an integer', first_octet
        return False
    if int(first_octet) == 1:
        first_octet_1 = True
        if debug:
            print 'First octet is 1'
    else:
        first_octet_1 = False

    if not 1 <= int(first_octet) <= 254:
        return False
    for item in parts[1:]:
        try:
            int(item)
        except:
            if debug:
                print 'value:', item, 'is not an integer'
            return False
        if first_octet_1:
            if debug:
                print 'testing from 0 - 254'
                print 'value is:', item
            if not 0 <= int(item) <= 254:
                if debug:
                    print 'value not in range 0-254, value:', item
                return False
        else:
            if debug:
                print 'testing from 0 - 254'
                print 'value is:', item
            if not 0 <= int(item) <= 254:
                if debug:
                    print 'value not in range 1-254, value:', item
                return False 
    return True
    
    
def pull_syslog(self, clock):
    """
    Pulls the information available from "show log" and filters based on date/time
    """
    debug = False
    
    ###################
    ## Input Validation
    
    # We need to first make sure that the incoming filter list contains all the fields we need!
    
    ########
    ## Month
    if clock.has_key('month'):
        if valid_month(clock['month']):
            if debug:
                print 'Filtering on Month', clock['month']
        else:
            print 'Invalid month detected:', clock['month']
            return 'Invalid Month: ' + clock['month']
    else:
        print 'Month option not detected. Must be present'
        return 'value "month" not set'

    ###############
    ## Day of month
    if clock.has_key('day_of_month'):
        if valid_day_of_month(clock['day_of_month']):
            if debug:
                print 'Filtering on day of month', clock['day_of_month']
        else:
            print 'Invalid day of month provided:', clock['day_of_month']
            return 'Invalid day of month provided: ' + clock['day_of_month']
    else:
        print 'no day_of_month value provided!'
        return 'no day_of_month value provided!'
        
    #######
    ## Hour
    if clock.has_key('hour'):
        if valid_hour(clock['hour']):
            if debug:
                print 'Filtering on hour', clock['hour']
        else:
            print 'Invalid hour detected', clock['hour']
            return 'Invalid hour detected ' + clock['hour'] 
    
    #########
    ## Minute
    if clock.has_key('minute'):
        if valid_minute(clock['minute']):
            if debug:
                print 'Filtering on minute', clock['minute']
        else:
            print 'Invalid minute value provided:', clock['minute']
            return 'Invalid minute value provided:' + clock['minute']
    else:
        print 'No minute value found!'
        return 'no minute value found'
    
    
    #################################
    ## Retrieving the Log information
    
    # The raw log lines look like this:
    """
    Jul 19 10:43:40 [0] DEBUG Aaad-HA_SESSION_BUFF_LOAD_SUCCESS-1-0x4400d: Successfully loaded session buff type 1.
    """
    
    # To be able to parse the log based on date/time we need:
    # month, day_of_month, raw_long_time
    
    # There is a problem with the time!
    # We need thing that happened after the start time
        
    #command = "show log | begin " + '"' + clock['month'] + ' ' + clock['day_of_month'] + '"'
    command = "show log | begin " + '"' + clock['month'] + ' ' \
     + clock['day_of_month'] + ' ' + clock['hour'] + ':' + clock['minute'] + '"'
 
    if debug:
        print ("The command will be: %s" % command)
        
    self.ses.sendline(command)
    
    raw_log = ''
    raw_log_lines = []
    collecting_input = True
    while collecting_input:
        retr = self.ses.expect([':$', enable_prompt_regex], timeout = 10)
        if retr == 0:
            raw_log = self.ses.before
            raw_lines = raw_log.splitlines()
            raw_log_lines += raw_lines
            if debug:
                print '-------------------------------'
                print 'We got some input. Here it is!'
                print 'it\'s', len(raw_log), 'raw characters'
                print 'it\'s', len(raw_lines), 'lines of text'
                print 'total is now', len(raw_log_lines)
                #print raw_log_lines
                print 'more input to capture'
        elif retr == 1:
            if debug:
                print 'back the prompt'
            raw_log = self.ses.before
            raw_lines = raw_log.splitlines()
            raw_log_lines += raw_lines
            collecting_input = False
            if debug:
                print '-------------------------------'
                print 'This is the last bit of input'
                print 'We got some input. Here it is!'
                print 'it\'s', len(raw_log), 'raw characters'
                print 'it\'s', len(raw_lines), 'lines of text'
                print 'total is now', len(raw_log_lines)
                
        else:
            print 'Timeout while retrieving logs. OOPS!'
            return 'timeout while retrieving logs'
    if len(raw_log_lines) < 2:
        print 'Not enough lines caught! Here is what we did get back'
        print raw_log_lines
        return 'No log retrieved'

    if debug:
        print 'Got the log back!'
        print 'there are', len(raw_log_lines), 'lines to parse'
        print 'Here are the first three of them'
        print raw_log_lines[1]
        print raw_log_lines[2]
        print raw_log_lines[3]
        print("Searching for log events after the start time")
        print("---------------------------------------------")
        
        
        
    ###############################
    ## Parse the lines from the log
    
    # 1. Try to parse the line and detect the date/time header
    # a. If that succeeds we hold the line in escrow in case there is more on the next line
    # aa. If there is already a line in escrow we save it to the return list
    # b. If that fails we join the current line to the line in escrow and store it
    # bb. If the old line was only 3 words long we add the ":" back in
    
    # This is the container we return the data in
    ret_list = []
    discarded_lines = 0
    broken_line = False
    escrow_line = ''
    
    for line in raw_log_lines[1:]:
        # Check for empty line
        if len(line) > 0:
        
            if debug:
                print("------------------------------------")
                print("The raw line is:")
                print(line)
            
            # Cut the line into words
            words = line.split()
            
            ############################################
            ## Peace back together word missing ":" case
            if broken_line:
                if debug:
                    print 'This should be the other half of the line'
                    print escrow_line
                    print 'The complete line should be:'
                    print escrow_line, line
                    
                # Here we have the first fragmenet and we join it to the other half
                escrow_words = escrow_line.split()
                if len(escrow_words) == 3:
                    if debug:
                        print 'We caught the special case where the ":" is missing.'
                        
                    word_three = escrow_words[2] + ':' + words[0]
                    if debug:
                        print 'our assembled third word is now', word_three
                        
                    head = escrow_words[0], escrow_words[1], word_three
                    if debug:
                        print 'the first three words should now be:', head
                    
                    tail = words[1:]
                    words = head, tail
                    if debug:
                        print 'The full line should now be:'
                        print words 
                    
                    # We fixed the broken line
                    broken_line = False
                    # and we took the three words out of escrow
                    escrow_line = ''
            
            
            ##############################
            ## Parse the month date header
            try:
                month_log = words[0]
                if not (valid_month(month_log)):
                    if debug:
                        print 'Invalid month detected'
                    raise
                day_of_month_log = words[1]
                if not (valid_day_of_month(day_of_month_log)):
                    if debug:
                        print 'Invalid day of month detected'
                    raise
                raw_time_log = words[2]
                if debug:
                    print 'parsing raw_time:', raw_time_log
                long_time_log = raw_time_log.split(":")
                if debug:
                    print 'the long_time_log contains:', long_time_log
                if not (len(long_time_log) == 3):
                    if debug:
                        print 'detected invalid time format:'
                        print long_time_log
                    raise
                hour_log = long_time_log[0]
                if not (valid_hour(hour_log)):
                    if debug:
                        print 'Invalid hour detected'
                    raise
                minute_log = long_time_log[1]
                if not (valid_minute(minute_log)):
                    if debug:
                        print 'Invalid minute detected'
                    raise
                second_log = long_time_log[2]
                if not (valid_second(second_log)):
                    if debug:
                        print 'invalid second detected'
                    raise
                # We don't care about this stuff at this time but it could be 
                #   parsed in the future.
                logs_per_second_log = words[3]
                log_type = words[4]
                log_deamon = words[5]
                log_msg_type = words[6]
                log_message = words[7:]

            except:
                if debug:
                    print 'Unable to parse this line:'
                    print line
                    print 'It is probably part of the previous line'
                # Yep it's broken somehow! Either
                # 1. It's missing it's ":" "special case"
                # 2. It is so long it linewrapped. 
                broken_line = True
                # We store the fragment in escrow
                escrow_line = line
                #ret_list.append(line)
            
            if debug:
                print 'Succesfully parsed the date/time header'
            
            #####################################
            ## Filter the line based on date time
            
            if not broken_line:
                # Ok now the log is parsed we need to compare the dat time
                if debug:
                    print("The month is: %s" % month_log)
                    print("looking for a month greater then: %s" % clock['month'])
                if clock['month'] == month_log:
                # Bug here it won't pass the end of the month to the next month
                    if debug:
                        print("The day is: %s" % day_of_month_log)
                        print("Looking for a day greater then: %s" % clock['day_of_month'])
                    if clock['day_of_month'] <= day_of_month_log:
                        if debug:
                            print("The hour is: %s" % hour_log)
                            print("Looking for an hour greater then: %s" % clock['hour'])
                        if clock['hour'] <= hour_log:
                            if debug:
                                print("The minute is: %s" % minute_log)
                                print("Looking for a minute greater then: %s" % clock['minute'])
                            if clock['minute'] <= minute_log:
                                # At this point we got a good line.
                                # If we had something in escrow we need to flush it to return_list
                                if len(escrow_line) > 0:
                                    ret_list.append(escrow_line)
                                    if debug:
                                        print 'We now have a complete line that we are flusing to the return list:'
                                        print escrow_line
                                        print 'clearing the escrow'
                                    escrow_line = ''
                                # It's possible for the line to have been split onto two lines
                                # We will hold the line in escrow in case we catch the other half.
                                else:
                                    if debug:
                                        print 'We have a good line. Saving it in escrow in case we find more parts of it'
                                    escrow_line = line
                            elif clock['hour'] < hour_log:
                                # At this point we got a good line.
                                # If we had something in escrow we need to flush it to return_list
                                if len(escrow_line) > 0:
                                    ret_list.append(escrow_line)
                                    if debug:
                                        print 'We now have a complete line that we are flusing to the return list:'
                                        print escrow_line
                                        print 'clearing the escrow'
                                    escrow_line = ''
                                # It's possible for the line to have been split onto two lines
                                # We will hold the line in escrow in case we catch the other half.
                                else:
                                    if debug:
                                        print 'We have a good line. Saving it in escrow in case we find more parts of it'
                                    escrow_line = line
                            else:
                                if debug:
                                    print 'The following line was not saved becuase it is before the minute we want'
                                    print line
                                discarded_lines += 1
                        elif clock['day_of_month'] < day_of_month_log:
                            # At this point we got a good line.
                            # If we had something in escrow we need to flush it to return_list
                            if len(escrow_line) > 0:
                                ret_list.append(escrow_line)
                                if debug:
                                    print 'We now have a complete line that we are flusing to the return list:'
                                    print escrow_line
                                    print 'clearing the escrow'
                                escrow_line = ''
                                # It's possible for the line to have been split onto two lines
                                # We will hold the line in escrow in case we catch the other half.
                            else:
                                if debug:
                                    print 'We have a good line. Saving it in escrow in case we find more parts of it'
                                escrow_line = line
                        else:
                            if debug:
                                print 'The following line was not saved becuase it is before the hour we want'
                                print line
                            discarded_lines += 1                
                    else:
                        if debug:
                            print 'The following line was not saved becuase it is before the day of month we want'
                            print line
                        discarded_lines += 1
                else:
                    if debug:
                        print 'The following line was not saved becuase it is before the month we want'
                        print line
                    discarded_lines += 1
                
                
            #####################################################################################
            ## concatenate the linewrapped line to the escrow line and add it to the return value
            
            if broken_line:
                # The words in the input line were broken up earlier
                
                # Make sure it's not the "special case"
                if len(words) > 3:
                    # Make sure it's not the first input
                    #   we want to append this output
                    if len(escrow_line) > 0:
                        if debug:
                            print 'Found the tail of a linewrapped line'
                            print 'the head looks like:'
                            print escrow_line
                            print 'The tail looks like:'
                            print line
                        # We store it back into the escrow line because there could
                        #   be more linewrapped text. (Multi line)
                        escrow_line = escrow_line + line
                        if debug:
                            print 'Put together it looks like'
                            print escrow_line
                        if debug:
                            print 'clearing broken line status'
                        broken_line = False
                    else:
                        # ok something is really messed up here. 
                        # 1. It's not words long
                        # 2. We don't have any lines in escrow yet
                        # It must just be crap
                        print 'Detected something very wrong with this line:'
                        print line
                        return 'unknown exception with line' + line
                        
        
    if debug:
        print 'Flusing the last line from escrow'
        print escrow_line
    ret_list.append(escrow_line)
          
    if debug:
        print '----------------------------------------'
        print 'Completed parsing the log file'
        print 'counted', len(ret_list), 'lines of log'
        print 'discarded', discarded_lines, 'lines'
            
    return ret_list

def num_month_to_string(month):
    """
    converts numeric months to three letter string months
    """
    debug = False
    
    try:
        num_month = int(month)
    except:
        if debug:
            print 'non numeric month set'
        return 'non numeric month set'
    
    return month_list[num_month - 1]
    
def name_month_to_num(month):
    """
    converts the name like "Jul" back to a number
    """
    month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    if month in month_list:
            
            
        if month == 'Jan':
            return 1
        elif month == 'Feb':
            return 2
        elif month == 'Mar':
            return 3
        elif month == 'Apr':
            return 4
        elif month == 'May':
            return 5
        elif month == 'Jun':
            return 6        
        elif month == 'Jul':
            return 7    
        elif month == 'Aug':
            return 8        
        elif month == 'Sep':
            return 9        
        elif month == 'Oct':
            return 10        
        elif month == 'Nov':
            return 11
        elif month == 'Dec':
            return 12
        else:
            print 'oh crap! Bug in issu.py name_month_num'
    else:
        print 'Invalid month supplied:', month 
        print 'Must be one of these:', month_list
        return 'Invalid month name'
                            
def get_hidden_password(level = '2'):
    """
    This command uses the cli-pwd to retrieve the hidden enable password for today only
    It takes in as it's input the level you need. Defaulting to 2
    """
    
    debug = False
    
    if debug:
        print 'Now in issu.py method get_hidden_password'
    
    if (level in range(1,7)):
        print 'Invalid level selected:', level
        print 'Level must be:', range(1,7)
        return 'Invalid level: ' + level
        
    search_string = 'level ' + level
    
    if debug:
        print 'search string will be:', search_string
    
    password = ''
    
    shell = os.popen("cli-pwd")
    for line in shell.readlines():
        if search_string in line:
            if debug:
                print("Found the line we were looking for:")
                print(line)
            words = line.split()
            if debug:
                print("This should be the word we are looking for: %s" % words[3])
            password = words[3].strip(',')
            if debug:
                print("This should be the password: %s" % password)
                print 'exiting this loop'
            break

    if debug:
        print 'about to return:', password 
        
    return password    

def pull_internal_logs(self, clock):
    """
    This method uses the hidden shell to look at the raw log files in /hd/logs and /hdp/logs
    It then filters the logs based on a date time and returns them in a list concatenated together
    There will be a list header for each log.
    
    The input is a date time which is the same format as the split show clock value
    That can be retrieved using the issu.py show_time function
    """
    debug = False
    
    # Program Flow
    # 1. Validate Input
    # 2. Log in and pull the file list
    # 3. Parse the Special file
    # 4. Dump the other files
    # 5. Pull /hdp/logs file list
    # 6. Parse the special file
    # 7. Dump the other files
    
    
    
    
    
    ######################
    ## 1. Input Validation
    ######################
    
    # We need to first make sure that the incoming filter list contains all the fields we need!
    
    ########
    ## Month
    if clock.has_key('month'):
        if valid_month(clock['month']):
            if debug:
                print 'Filtering on Month', clock['month']
        else:
            print 'Invalid month detected:', clock['month']
            return 'Invalid Month: ' + clock['month']
    else:
        print 'Month option not detected. Must be present'
        return 'value "month" not set'

    ###############
    ## Day of month
    if clock.has_key('day_of_month'):
        if valid_day_of_month(clock['day_of_month']):
            if debug:
                print 'Filtering on day of month', clock['day_of_month']
        else:
            print 'Invalid day of month provided:', clock['day_of_month']
            return 'Invalid day of month provided: ' + clock['day_of_month']
    else:
        print 'no day_of_month value provided!'
        return 'no day_of_month value provided!'
        
    #######
    ## Hour
    if clock.has_key('hour'):
        if valid_hour(clock['hour']):
            if debug:
                print 'Filtering on hour', clock['hour']
        else:
            print 'Invalid hour detected', clock['hour']
            return 'Invalid hour detected ' + clock['hour'] 
    
    #########
    ## Minute
    if clock.has_key('minute'):
        if valid_minute(clock['minute']):
            if debug:
                print 'Filtering on minute', clock['minute']
        else:
            print 'Invalid minute value provided:', clock['minute']
            return 'Invalid minute value provided:' + clock['minute']
    else:
        print 'No minute value found!'
        return 'no minute value found'
    
    
    
    
    
    ###################################
    ## 2. Log in and pull the file list
    ###################################
    
    ######################
    ## Get enable password
    
    if debug:
        print 'retrieving the hidden enable password'
    
    password = get_hidden_password()
    
    if debug:
        print 'retrieved the password:', password

    #################
    ## open the shell
    
    if debug:
        print 'opening the hidden enable shell'

    try:
        self.open_hidden_shell(password)
    except:
        print 'Unable to open the hidden enable shell!'
        return 'failed to open the hidden shell'
    
    if debug:
        print 'about to run a simple command in the hidden shell'
    
    ####################
    ## Get the file list
    
        
    if debug:
        print 'going to /hd/logs to read the log files'
    raw_output = self.hidden_cmd("cd \/hd\/logs")
    if debug:
        print 'the return value was'
        print raw_output

    if debug:
        print 'checking the current working directory'
    raw_output = self.hidden_cmd("pwd")
    if debug:
        print 'the return value was'
        print raw_output
        
    if debug:
        print 'counting the files in the directory'
    raw_output = self.hidden_cmd('ls | wc')
    if debug:
        print 'the raw output was:', raw_output
    try:
        raw_file_count = raw_output.split()
        file_count = int(raw_file_count[0])
        if debug:
            print 'Found', file_count, 'files'
        if file_count > 1000:
            print 'There are more then 1000 log files.'
            print 'The API can not process the files.'
            print 'Please erase some files and re-try'
            return 1
    except:
        print 'The value returned from the file count was not a number'
        print 'Please take a look:', raw_output
        return 1
    
    #command = 'ls -1 event-log* | tail -n 300'
    command = 'ls -1 event-log*'
    if debug:
        print 'getting the list of log files in /hd/logs'
        print 'the command will be:', command
    #raw_output = self.hidden_cmd("ls | grep event-log", 10)
    raw_output = self.hidden_cmd(command, 10)
    #raw_output = self.cli_cmd(command)
    if debug:
        print 'the return value was'
        print raw_output
    
    ######################################
    ## Look for files with the right date
    
    file_list = []
    
    if debug:
        print 'Now parsing file list'
        print '---------------------'
    
    for line in raw_output.splitlines():
        if debug:
            print '-------------------------'
            print 'raw line:'
            print line
        # The raw line looks like this:
        """
        event-log-20100722-114132
        """
        # We split it on the "-"
        #if len(line) > 0:
        # We need to reject most of the filenames
        # our filename is always 25 characters
        if len(line) == 25:
            if debug:
                print 'found a line we care about'
            words = line.split('-')
            # Here is the decoded data we need to extract
            """
            year:  2010
            month: 07
            day:   22
            
            hour:   11
            minute: 41
            second: 32
            """
            date = words[2]
            year_file = date[:4]
            raw_month_file = date[4:6]
            month_file = num_month_to_string(raw_month_file)
            day_file = date[6:]
            
            time = words[3]
            hour_file = time[:2]
            minute_file = time[2:4]
            second_file = time[4:]
            
            if debug:
                print 'detected the following date time:'
                print 'year:', year_file, 'month:', month_file
                print 'day:', day_file
                print 'hour:', hour_file, 'minute:', minute_file, 'second:', second_file
                
            
            
            # now we must compare the parsed date/time and 
            # compare it with our filter value
            if clock['month'] == month_file:
                if debug:
                    print 'Found a file with the right month:', month_file
                if clock['day_of_month'] <= day_file:
                    if debug:
                        print 'Found a day that is equal to or greater our filter day:', day_file
                    if clock['hour'] <= hour_file:
                        if debug:
                            print 'Found an hour that is equal or greater then filter hour:', hour_file
                        if clock['minute'] <= minute_file:
                            if debug:
                                print 'found our file!'
                                print line
                                print 'Our input value for minute was:', minute_file
                                print 'The minute value we are filtering on is:', clock['minute']
                            file_list.append(line)

                        # If it's outright larger. Example I'm filtering on things that happened
                        # After 1:10 and I find something that happened at 4:04
                        # Technically the minute is smaller 10 > 04 but the hour is larger
                        # Therefore I need to keep it. 
                        elif clock['hour'] < hour_file:
                            if debug:
                                print 'Found a keeper:', line
                            file_list.append(line)
                        else:
                            file_to_search_inside = line
                            
                    elif clock['day_of_month'] < day_file:
                        if debug:
                            print 'Found a keeper', line 
                        file_list.append(line)

                    else:
                        file_to_search_inside = line
                else:
                    file_to_search_inside = line
            else:
                file_to_search_inside = line
        else:
            file_to_search_inside = ''
            
            if debug:
                print 'line is:', len(line), 'characters long'
                if len(line) > 25:
                    print 'Rejecting this file name because it is too long'
                if len(line) < 25:
                    print 'Rejecting this file name because it is too too short'        
    if debug:
        print 'Done filtering' , len(raw_output.splitlines()), 'files'
        print 'Found', len(file_list), 'files to keep'
        for file in file_list:
            print file
        print 'We filtered on: 2010' + str(name_month_to_num(clock['month'])) + clock['day_of_month'] + \
              '-' + clock['hour'] + clock['minute'] + '00'
        print 'The file that may contain some more logs is:', file_to_search_inside

        
    
    if debug:
        print 'Now we will dump the special file and search for the first entry after our date'
    
    # This is the list we return
    ret_list = []
    found_line = False
    discarded_lines = 0
    
    #############################
    ## 3. Search our special file
    #############################
    
    if len(file_to_search_inside) > 0:
        # Need to add the line reading to this function as well to speed it up. 
        try:
            command = 'wc ' + file_to_search_inside 
        except:
            print 'no files found to read. There is a bug in pull_internal_logs in issu.py!'
            sys.exit(1)
            
        try:
            raw_output = self.hidden_cmd(command, 20)
        except:
            print 'Failure while getting the line count of file', file
            return 'Failing to get the line count of file: ' + file
        # Example raw_output
        """
        387     4756    31900 event-log-20100723-140131
        """
        words = raw_output.split()
        if debug:
            print 'The raw output was:'
            print raw_output
            print 'The file:', file_to_search_inside, 'Has', words[0], 'lines of text'
        str_line_count = words[0]
        try:
            line_count = int(str_line_count)
        except:
            print 'We got a non integer for the line count!', str_line_count
            return 'invalid line count ' + str_line_count
            
            
        command = 'cat ' + file_to_search_inside       
        if debug:
            print 'Command will be:', command
            print 'Sending command.'
        self.ses.sendline(command)
        
        
        # Begin reading the line of the file
        reading_input = True
        local_lines = []
        # The first line returned is the command executed so we need to increment by 1

        while reading_input:
        
            if debug:
                print 'Lines left:', line_count
                
            try:
                line = self.ses.readline()
            except:
                print 'unable to read the line!'
                if '/bin/sh: cannot fork - try again' in line: 
                    print 'Shell died. SSX probably restarting'
                    return 'Lost Shell. SSX probably rebooting'
                
            
            if command in line:
                if debug:
                    print 'we got the command line back!'
            else:
                if found_line:
                    ret_list.append(line)
                else:
                    if len(line) > 0:
                    
                        if debug:
                            print("------------------------------------")
                            print("The raw line is:")
                            print(line)
                        
                        # Cut the line into words
                        words = line.split()
                        
                        # raw line looks like
                        """
                        Jul 23 01:50:20 [1] INFO Clock-TZSET: System timezone set to: PDT (Day Light Saving Not set)
                        """

                        ##############################
                        ## Parse the month date header
                        try:
                            month_log = words[0]
                            if not (valid_month(month_log)):
                                if debug:
                                    print 'Invalid month detected'
                                raise
                            day_of_month_log = words[1]
                            if not (valid_day_of_month(day_of_month_log)):
                                if debug:
                                    print 'Invalid day of month detected'
                                raise
                            raw_time_log = words[2]
                            if debug:
                                print 'parsing raw_time:', raw_time_log
                            long_time_log = raw_time_log.split(":")
                            if debug:
                                print 'the long_time_log contains:', long_time_log
                            if not (len(long_time_log) == 3):
                                if debug:
                                    print 'detected invalid time format:'
                                    print long_time_log
                                raise
                            hour_log = long_time_log[0]
                            if not (valid_hour(hour_log)):
                                if debug:
                                    print 'Invalid hour detected'
                                raise
                            minute_log = long_time_log[1]
                            if not (valid_minute(minute_log)):
                                if debug:
                                    print 'Invalid minute detected'
                                raise
                            second_log = long_time_log[2]
                            if not (valid_second(second_log)):
                                if debug:
                                    print 'invalid second detected'
                                raise
                            # We don't care about this stuff at this time but it could be 
                            #   parsed in the future.
                            logs_per_second_log = words[3]
                            log_type = words[4]
                            log_deamon = words[5]
                            log_msg_type = words[6]
                            log_message = words[7:]

                        except:
                            if debug:
                                print 'Unable to parse this line:'
                                print line
                                print 'It is probably part of the previous line'
                            # Yep it's broken somehow! Either
                            # 1. It's missing it's ":" "special case"
                            # 2. It is so long it linewrapped. 
                            broken_line = True
                            # We store the fragment in escrow
                            escrow_line = line
                            #ret_list.append(line)
                        
                        if debug:
                            print 'Succesfully parsed the date/time header'
                    

                        #####################################
                        ## Filter the line based on date time
                        
                        if debug:
                            print("The month is: %s" % month_log)
                            print("looking for a month greater then: %s" % clock['month'])
                        if clock['month'] == month_log:
                        # Bug here it won't pass the end of the month to the next month
                            if debug:
                                print("The day is: %s" % day_of_month_log)
                                print("Looking for a day greater then: %s" % clock['day_of_month'])
                            if clock['day_of_month'] <= day_of_month_log:
                                if debug:
                                    print("The hour is: %s" % hour_log)
                                    print("Looking for an hour greater then: %s" % clock['hour'])
                                if clock['hour'] <= hour_log:
                                    if debug:
                                        print("The minute is: %s" % minute_log)
                                        print("Looking for a minute greater then: %s" % clock['minute'])
                                    if clock['minute'] <= minute_log:
                                        # We save the line
                                        ret_list.append(line)
                                        found_line = True
                                        if debug:
                                            print 'Found the beginning line. Skipping filtering other lines'
                                    elif clock['hour'] < hour_log:
                                        found_line = True
                                        if debug:
                                            print 'Found the beginning line. Skipping filtering other lines'
                                        ret_list.append(line)
                                    else:
                                        if debug:
                                            print 'The following line was not saved becuase it is before the minute we want'
                                            print line
                                        discarded_lines += 1
                                elif clock['day_of_month'] < day_of_month_log:
                                    found_line = True
                                    if debug:
                                        print 'Found the beginning line. Skipping filtering other lines'
                                    ret_list.append(line)
                                else:
                                    if debug:
                                        print 'The following line was not saved becuase it is before the hour we want'
                                        print line
                                    discarded_lines += 1
                            elif clock['month'] < month_log:
                                found_line = True
                                if debug:
                                    print 'Found the beginning line. Skipping filtering other lines'
                                ret_list.append(line)
                            else:
                                if debug:
                                    print 'The following line was not saved becuase it is before the day of month we want'
                                    print line
                                discarded_lines += 1
                        else:
                            if debug:
                                print 'The following line was not saved becuase it is before the month we want'
                                print line
                            discarded_lines += 1
                
                # Decement the line count
                line_count = line_count - 1
                # Break when run out of lines to read
                if line_count == 0:
                    if debug:
                        'At the end of the counted lines'
                    reading_input = False

        
    
    ###################
    ## 4. Dump the rest
    ###################
    
    for file in file_list:
        if debug:
            print '----------------------------'
            print 'Now reading file:', file
            print '----------------------------'
        # At this point simply cat-ing the file and reading the output we try to filter every
        #  character for the '#' prompt. This causes a huge delay and won't work for us. 
        # Instead we will use 'wc' to count the number of lines we need to read until the next prompt
        command = 'wc ' + file
        try:
            raw_output = self.hidden_cmd(command, 20)
        except:
            print 'Failure while getting the line count of file', file
            break
        # Example raw_output
        """
        387     4756    31900 event-log-20100723-140131
        """
        words = raw_output.split()
        if debug:
            print 'The raw output was:'
            print raw_output
            print 'The file:', file, 'Has', words[0], 'lines of text'
        str_line_count = words[0]
        try:
            line_count = int(str_line_count)
        except:
            print 'We got a non integer for the line count!', str_line_count
            return 'invalid line count ' + str_line_count

        command = 'cat ' + file        
        if debug:
            print 'Command will be:', command
            print 'Sending command.'
        self.ses.sendline(command)
        
        reading_input = True
        local_lines = []
        while reading_input:
        
            if debug:
                print 'Lines left:', line_count
                
            try:
                line = self.ses.readline()
            except:
                print 'unable to read the line!'
                
            if debug:
                print 'line:'
                print line
                
            if command in line:
                if debug:
                    print 'we got the command line back!'
                reading_input = False
            else:
            
                if debug:
                    print 'Saving this line'
                    
                local_lines.append(line)
                # Decrement the line counter
                line_count = line_count - 1
                # Break when run out of lines to read
                if line_count == 0:
                    if debug:
                        'At the end of the counted lines'
                    reading_input = False
                    
            if line_count == 0:
                if debug:
                    print 'done dumping lines'
                reading_input == False
                
        if debug:
            print 'We caught:', len(local_lines), 'lines of output from file:', file
        
        for line in local_lines:
            ret_list.append(line)
        if debug:    
            print 'The complete log is now:', len(ret_list)
        
    print '000000000000000000000000000000'
    print 'Completed parsing the /hd/logs'
    print 'now parsing /hdp/logs'
    print '000000000000000000000000000000'
    
    ret_list.append("end of /hd/logs")
    ret_list.append("INTERNAL LOGS BEGIN")

    


    #######################
    ## 5. Get the file list
    #######################
        
    raw_output = self.hidden_cmd("cd \/hdp\/logs")
    if debug:
        print 'the return value was'
        print raw_output

    raw_output = self.hidden_cmd("pwd")
    if debug:
        print 'the return value was'
        print raw_output

    raw_output = self.hidden_cmd("ls | grep event-log")
    if debug:
        print 'the return value was'
        print raw_output
    
    ######################################
    ## Look for files with the right date
    
    file_list = []
    
    if debug:
        print 'Now parsing file list'
        print '---------------------'
    
    for line in raw_output.splitlines():
        if debug:
            print '-------------------------'
            print 'raw line:'
            print line
        # The raw line looks like this:
        """
        event-log-20100722-114132
        """
        # We split it on the "-"
        if len(line) > 0:
            if debug:
                print 'found a line we care about'
            words = line.split('-')
            # Here is the decoded data we need to extract
            """
            year:  2010
            month: 07
            day:   22
            
            hour:   11
            minute: 41
            second: 32
            """
            date = words[2]
            year_file = date[:4]
            raw_month_file = date[4:6]
            month_file = num_month_to_string(raw_month_file)
            day_file = date[6:]
            
            time = words[3]
            hour_file = time[:2]
            minute_file = time[2:4]
            second_file = time[4:]
            
            if debug:
                print 'detected the following date time:'
                print 'year:', year_file, 'month:', month_file
                print 'day:', day_file
                print 'hour:', hour_file, 'minute:', minute_file, 'second:', second_file
                
            
            
            # now we must compare the parsed date/time and 
            # compare it with our filter value
            if clock['month'] == month_file:
                if debug:
                    print 'Found a file with the right month:', month_file
                if clock['day_of_month'] <= day_file:
                    if debug:
                        print 'Found a day that is equal to or greater our filter day:', day_file
                    if clock['hour'] <= hour_file:
                        if debug:
                            print 'Found an hour that is equal or greater then filter hour:', hour_file
                        if clock['minute'] <= minute_file:
                            if debug:
                                print 'found our file!'
                                print line
                                print 'Our input value for minute was:', minute_file
                                print 'The minute value we are filtering on is:', clock['minute']
                            file_list.append(line)

                        # If it's outright larger. Example I'm filtering on things that happened
                        # After 1:10 and I find something that happened at 4:04
                        # Technically the minute is smaller 10 > 04 but the hour is larger
                        # Therefore I need to keep it. 
                        elif clock['hour'] < hour_file:
                            if debug:
                                print 'Found a keeper:', line
                            file_list.append(line)
                        else:
                            file_to_search_inside = line
                            
                    elif clock['day_of_month'] < day_file:
                        if debug:
                            print 'Found a keeper', line 
                        file_list.append(line)

                    else:
                        file_to_search_inside = line
                else:
                    file_to_search_inside = line
            else:
                file_to_search_inside = line
                
    print 'Done filtering' , len(raw_output.splitlines()), 'files'
    print 'Found', len(file_list), 'files to keep'
    for file in file_list:
        print file
    print 'We filtered on: 2010' + clock['month'] + clock['day_of_month'] + \
          '-' + clock['hour'] + clock['minute'] + '00'
    print 'The file that may contain some more logs is:', file_to_search_inside
        
    
    if debug:
        print 'Now we will dump the special file and search for the first entry after our date'
    
    # This is the list we return
    ret_list = []
    found_line = False
    discarded_lines = 0
    
    #############################
    ## 6. Search our special file
    #############################
    
    # Need to add the line reading to this function as well to speed it up. 

    command = 'wc ' + file_to_search_inside 
    try:
        raw_output = self.hidden_cmd(command, 20)
    except:
        print 'Failure while getting the line count of file', file
        return 'Failing to get the line count of file: ' + file
    # Example raw_output
    """
    387     4756    31900 event-log-20100723-140131
    """
    words = raw_output.split()
    if debug:
        print 'The raw output was:'
        print raw_output
        print 'The file:', file_to_search_inside, 'Has', words[0], 'lines of text'
    str_line_count = words[0]
    try:
        line_count = int(str_line_count)
    except:
        print 'We got a non integer for the line count!', str_line_count
        return 'invalid line count ' + str_line_count
        
        
    command = 'cat ' + file_to_search_inside       
    if debug:
        print 'Command will be:', command
        print 'Sending command.'
    self.ses.sendline(command)
    
    
    # Begin reading the line of the file
    reading_input = True
    local_lines = []
    # The first line returned is the command executed so we need to increment by 1

    while reading_input:
    
        if debug:
            print 'Lines left:', line_count
            
        try:
            line = self.ses.readline()
        except:
            print 'unable to read the line!'
        
        if command in line:
            if debug:
                print 'we got the command line back!'
        else:
            if found_line:
                ret_list.append(line)
            else:
                if len(line) > 0:
                
                    if debug:
                        print("------------------------------------")
                        print("The raw line is:")
                        print(line)
                    
                    # Cut the line into words
                    words = line.split()
                    
                    # raw line looks like
                    """
                    Jul 27 20:17:08 [2] INT HaMgr-ACT_CONNECTION_AVAILABLE: active ha-mgr connection available
                    """

                    ##############################
                    ## Parse the month date header
                    try:
                        month_log = words[0]
                        if not (valid_month(month_log)):
                            if debug:
                                print 'Invalid month detected'
                            raise
                        day_of_month_log = words[1]
                        if not (valid_day_of_month(day_of_month_log)):
                            if debug:
                                print 'Invalid day of month detected'
                            raise
                        raw_time_log = words[2]
                        if debug:
                            print 'parsing raw_time:', raw_time_log
                        long_time_log = raw_time_log.split(":")
                        if debug:
                            print 'the long_time_log contains:', long_time_log
                        if not (len(long_time_log) == 3):
                            if debug:
                                print 'detected invalid time format:'
                                print long_time_log
                            raise
                        hour_log = long_time_log[0]
                        if not (valid_hour(hour_log)):
                            if debug:
                                print 'Invalid hour detected'
                            raise
                        minute_log = long_time_log[1]
                        if not (valid_minute(minute_log)):
                            if debug:
                                print 'Invalid minute detected'
                            raise
                        second_log = long_time_log[2]
                        if not (valid_second(second_log)):
                            if debug:
                                print 'invalid second detected'
                            raise
                        # We don't care about this stuff at this time but it could be 
                        #   parsed in the future.
                        logs_per_second_log = words[3]
                        log_type = words[4]
                        log_deamon = words[5]
                        log_msg_type = words[6]
                        log_message = words[7:]

                    except:
                        if debug:
                            print 'Unable to parse this line:'
                            print line
                            print 'It is probably part of the previous line'
                        # Yep it's broken somehow! Either
                        # 1. It's missing it's ":" "special case"
                        # 2. It is so long it linewrapped. 
                        broken_line = True
                        # We store the fragment in escrow
                        escrow_line = line
                        #ret_list.append(line)
                    
                    if debug:
                        print 'Succesfully parsed the date/time header'
                

                    #####################################
                    ## Filter the line based on date time
                    
                    if debug:
                        print("The month is: %s" % month_log)
                        print("looking for a month greater then: %s" % clock['month'])
                    if clock['month'] == month_log:
                    # Bug here it won't pass the end of the month to the next month
                        if debug:
                            print("The day is: %s" % day_of_month_log)
                            print("Looking for a day greater then: %s" % clock['day_of_month'])
                        if clock['day_of_month'] <= day_of_month_log:
                            if debug:
                                print("The hour is: %s" % hour_log)
                                print("Looking for an hour greater then: %s" % clock['hour'])
                            if clock['hour'] <= hour_log:
                                if debug:
                                    print("The minute is: %s" % minute_log)
                                    print("Looking for a minute greater then: %s" % clock['minute'])
                                if clock['minute'] <= minute_log:
                                    # We save the line
                                    ret_list.append(line)
                                    found_line = True
                                    if debug:
                                        print 'Found the beginning line. Skipping filtering other lines'
                                elif clock['hour'] < hour_log:
                                    found_line = True
                                    if debug:
                                        print 'Found the beginning line. Skipping filtering other lines'
                                    ret_list.append(line)
                                else:
                                    if debug:
                                        print 'The following line was not saved becuase it is before the minute we want'
                                        print line
                                    discarded_lines += 1
                            elif clock['day_of_month'] < day_of_month_log:
                                found_line = True
                                if debug:
                                    print 'Found the beginning line. Skipping filtering other lines'
                                ret_list.append(line)
                            else:
                                if debug:
                                    print 'The following line was not saved becuase it is before the hour we want'
                                    print line
                                discarded_lines += 1
                        elif clock['month'] < month_log:
                            found_line = True
                            if debug:
                                print 'Found the beginning line. Skipping filtering other lines'
                            ret_list.append(line)
                        else:
                            if debug:
                                print 'The following line was not saved becuase it is before the day of month we want'
                                print line
                            discarded_lines += 1
                    else:
                        if debug:
                            print 'The following line was not saved becuase it is before the month we want'
                            print line
                        discarded_lines += 1
            
            # Decement the line count
            line_count = line_count - 1
            # Break when run out of lines to read
            if line_count == 0:
                if debug:
                    'At the end of the counted lines'
                reading_input = False

        
    
    ###################
    ## 7. Dump the rest
    ###################
    
    for file in file_list:
        if debug:
            print '----------------------------'
            print 'Now reading file:', file
            print '----------------------------'
        # At this point simply cat-ing the file and reading the output we try to filter every
        #  character for the '#' prompt. This causes a huge delay and won't work for us. 
        # Instead we will use 'wc' to count the number of lines we need to read until the next prompt
        command = 'wc ' + file
        try:
            raw_output = self.hidden_cmd(command, 20)
        except:
            print 'Failure while getting the line count of file', file
            break
        # Example raw_output
        """
        387     4756    31900 event-log-20100723-140131
        """
        words = raw_output.split()
        if debug:
            print 'The raw output was:'
            print raw_output
            print 'The file:', file, 'Has', words[0], 'lines of text'
        str_line_count = words[0]
        try:
            line_count = int(str_line_count)
        except:
            print 'We got a non integer for the line count!', str_line_count
            return 'invalid line count ' + str_line_count

        command = 'cat ' + file        
        if debug:
            print 'Command will be:', command
            print 'Sending command.'
        self.ses.sendline(command)
        
        reading_input = True
        local_lines = []
        while reading_input:
        
            if debug:
                print 'Lines left:', line_count
                
            try:
                line = self.ses.readline()
            except:
                print 'unable to read the line!'
                
            if debug:
                print 'line:'
                print line
                
            if command in line:
                if debug:
                    print 'we got the command line back!'
            else:
            
                if debug:
                    print 'Saving this line'
                    
                local_lines.append(line)
                # Decrement the line counter
                line_count = line_count - 1
                # Break when run out of lines to read
                if line_count == 0:
                    if debug:
                        'At the end of the counted lines'
                    reading_input = False
        if debug:
            print 'We caught:', len(local_lines), 'lines of output from file:', file
        
        for line in local_lines:
            ret_list.append(line)

        if debug:    
            print 'The complete log is now:', len(ret_list)
        
    ret_list.append("INTERNAL LOGS END")
 
    ###########
    ## Complete
    ###########
    
    if debug:
        print 'closing the shell'
        
    self.close_hidden_shell()
    
    if debug:
        print 'done with issu.py pull_internal_logs'

    return ret_list
    
def pull_corefiles(self, clock, username='regress', user_password='gleep7', host='10.1.1.101'):
    """
    retrieves the core files from the SSX and drops them in your CWD
    Files are renamed with the YYYY-MM-DD
    
    clock = list of split time
    username = username to log into the linux system with. Defaults to "regress"
    user_password = password for above username. Defaults to "gleep7"
    host = linux host to sftp the files to. Defaults to "10.1.1.101" which is 
    qa-radxpm-1 
    """
    # Program Flow
    # 1. Validate Input
    # 2. Get file list based on Date
    # 3. SFTP the files off
    # 4. Copy the files from /home/regress to /home/USERNAME
    
    ######################
    ## 1. Input Validation
    ######################
    
    # We need to first make sure that the incoming filter list contains all the fields we need!
    
    ########
    ## Month
    if clock.has_key('month'):
        if valid_month(clock['month']):
            if debug:
                print 'Filtering on Month', clock['month']
        else:
            print 'Invalid month detected:', clock['month']
            return 'Invalid Month: ' + clock['month']
    else:
        print 'Month option not detected. Must be present'
        return 'value "month" not set'

    ###############
    ## Day of month
    if clock.has_key('day_of_month'):
        if valid_day_of_month(clock['day_of_month']):
            if debug:
                print 'Filtering on day of month', clock['day_of_month']
        else:
            print 'Invalid day of month provided:', clock['day_of_month']
            return 'Invalid day of month provided: ' + clock['day_of_month']
    else:
        print 'no day_of_month value provided!'
        return 'no day_of_month value provided!'
        
    #######
    ## Hour
    if clock.has_key('hour'):
        if valid_hour(clock['hour']):
            if debug:
                print 'Filtering on hour', clock['hour']
        else:
            print 'Invalid hour detected', clock['hour']
            return 'Invalid hour detected ' + clock['hour'] 
    
    #########
    ## Minute
    if clock.has_key('minute'):
        if valid_minute(clock['minute']):
            if debug:
                print 'Filtering on minute', clock['minute']
        else:
            print 'Invalid minute value provided:', clock['minute']
            return 'Invalid minute value provided:' + clock['minute']
    else:
        print 'No minute value found!'
        return 'no minute value found'    
    

    ###################################
    ## 2. Log in and pull the file list
    ###################################
    
    ######################
    ## Get enable password
    
    if debug:
        print 'retrieving the hidden enable password'
    
    password = get_hidden_password()
    
    if debug:
        print 'retrieved the password:', password

    #################
    ## open the shell
    
    if debug:
        print 'opening the hidden enable shell'

    try:
        self.open_hidden_shell(password)
    except:
        print 'Unable to open the hidden enable shell!'
        return 'failed to open the hidden shell'
    
    if debug:
        print 'about to run a simple command in the hidden shell'
    
    ####################
    ## Get the file list
    dump_dirs = ['slot0','slot1','slot2','slot3','slot4']
    file_list = []
    
    for dir in dump_dirs:
        command = 'cd \/hd\/dump\/' + dir
        
        if debug:
            print 'the command will be:', command
            
        raw_output = self.hidden_cmd(command)
        
        if debug:
            print 'the return value was'
            print raw_output
            
        command = 'ls -l | grep core.gz'
        
        if debug:
            print 'the command will be:', command
            
        raw_output = self.hidden_cmd(command)
        
        if debug:
            print 'the return value was'
            print raw_output
        
        # the raw line looks like this:
        """
        -rw-r--r--  1 root      root        2807430 Jul 26 16:53 dfn.1.core.gz

        """
        discarded_lines = 0
        
        raw_lines = raw_output.splitlines()
        for line in raw_lines[2:]:
            if debug:
                print 'parsing:'
                print line
            words = line.split()
            month_log = words[5]
            day_of_month_log = words[6]
            raw_time_log = words[7]
            split_time_log = raw_time_log.split(":")
            hour_log = split_time_log[0]
            minute_log = split_time_log[1]
            filename_log = words[8]
            
            if debug:
                print filename_log, 'Month:', month_log, 'day', day_of_month_log, 'hour:', hour_log, 'Minute:', minute_log
            
            full_path = dir + '/' + filename_log
            if debug:
                print 'That file lives:', full_path
            
            #####################################
            ## Filter the line based on date time
            
            if debug:
                print("The month is: %s" % month_log)
                print("looking for a month greater then: %s" % clock['month'])
            if clock['month'] == month_log:
            # Bug here it won't pass the end of the month to the next month
                if debug:
                    print("The day is: %s" % day_of_month_log)
                    print("Looking for a day greater then: %s" % clock['day_of_month'])
                if clock['day_of_month'] <= day_of_month_log:
                    if debug:
                        print("The hour is: %s" % hour_log)
                        print("Looking for an hour greater then: %s" % clock['hour'])
                    if clock['hour'] <= hour_log:
                        if debug:
                            print("The minute is: %s" % minute_log)
                            print("Looking for a minute greater then: %s" % clock['minute'])
                        if clock['minute'] <= minute_log:
                            # We save the line
                            file_list.append(full_path)
                            if debug:
                                print 'Found a file:', filename_log
                        elif clock['hour'] < hour_log:
                            if debug:
                                print 'Found a file:', filename_log
                            file_list.append(full_path)
                        else:
                            if debug:
                                print 'The following file was not saved becuase it is before the minute we want'
                                print line
                            discarded_lines += 1
                    elif clock['day_of_month'] < day_of_month_log:
                        if debug:
                            print 'Found a file:', filename_log
                        file_list.append(full_path)
                    else:
                        if debug:
                            print 'The following file was not saved becuase it is before the hour we want'
                            print full_path
                elif clock['month'] < month_log:
                    if debug:
                        print 'Found a file:', filename_log
                    file_list.append(full_path)
                else:
                    if debug:
                        print 'The following file was not saved becuase it is before the day of month we want'
                        print filename_log
            else:
                if debug:
                    print 'The following file was not saved becuase it is before the month we want'
                    print filename_log
                
        print 'The following', len(file_list), 'core files will be coppied to the testing directory:'
        for file in file_list:
            print file
        
    self.close_hidden_shell()
    
    #################
    ## SFTP files off
    unsaved_files = []
    linux_file_list = []
    for file in file_list:
        file_parts = file.split('/')
        slot = file_parts[-2]
        filename = file_parts[-1]
        filename_parts = filename.split(".")
        if len(filename_parts) == 3:
            filename_head = filename_parts[0]
        elif len(filename_parts) == 4:
            filename_head = filename_parts[0] + '-' + filename_parts[1]
        else:
            print 'This filename has too many "." in it!'
            print filename_parts
            filename_head = filename_parts[0] + '-' + filename_parts[1]
        extension = filename_parts[-2] + '.' + filename_parts[-1]
        month = name_month_to_num(clock['month'])
        if debug:
            print 'file:', file, 'filename:', filename
            print 'in slot:', slot
        
        if not clock.has_key('year'):
            print 'No year detected. Defaulting to 2010'
            clock['year'] = '2010'
        file_name_with_timestamp = filename_head + '-' + str(clock['year']) + str(month) + \
        str(clock['day_of_month']) + str(clock['hour']) + str(clock['minute']) + '.' + str(extension)
        
        if debug:
            print 'the full filename will be:', file_name_with_timestamp
            
        command = 'copy /hd/dump/' + file + ' sftp://' + username + '@' + host + ':/home/' + username \
         + '/' + file_name_with_timestamp
        
        if debug:
            print 'The command will be:'
            print command
        print 'Copying the core file:', filename, 'off the system.'

        #self.ftppasswd(command, user_password)
        self.ftppasswd(command, user_password, 60)
        print 'File copied succesfully'
        linux_file_list.append(file_name_with_timestamp)
        
    
    """
    if len(unsaved_files) > 0:
        print 'There were:', len(file_list), 'files to copy.', len(unsaved_files), 'files were not coppied'
        #print 'These files were not coppied off the system:'
        #for file in unsaved_files:
         #   print file
    """
            
        
    print 'Completed copying Core Files off'
    
        
    current_dir = os.getcwd()
    if debug:
        print 'script is being run from:', current_dir
        
    for file in linux_file_list:
        source_path = '/home/' + username + '/'
        full_filename = source_path + file
        dest_filename = current_dir + '/' + file
        print '------------------------'
        print 'about to move:', full_filename, 'to:', dest_filename
        
        shutil.copyfile(full_filename, dest_filename)
        print 'file moved succesfully.'

    print 'All done moving the files.'

    return 0


def filter_logs(self, clock):
    """
    Pulls information available from "show log". 
    Then logs in and pulls the internal log files in /hd/logs and /hdp/logs
    It also pulls any core files to the scripts CWD
    """
    debug = False
    
    ###################
    ## Input Validation
    
    # We need to first make sure that the incoming filter list contains all the fields we need!
    if debug:
	print 'Validating the Date/Time'
    ########
    ## Month
    if clock.has_key('month'):
        if valid_month(clock['month']):
            if debug:
                print 'Filtering on Month', clock['month']
        else:
            print 'Invalid month detected:', clock['month']
            return 'Invalid Month: ' + clock['month']
    else:
        print 'Month option not detected. Must be present'
        return 'value "month" not set'

    ###############
    ## Day of month
    if clock.has_key('day_of_month'):
        if valid_day_of_month(clock['day_of_month']):
            if debug:
                print 'Filtering on day of month', clock['day_of_month']
            if clock['day_of_month'][0] == '0':
                # This line may require a space!
                clock['day_of_month'] = clock['day_of_month'].lstrip('0')
                if debug:
                    print 'the stripped hour now looks like', clock['day_of_month']
        else:
            print 'Invalid day of month provided:', clock['day_of_month']
            return 'Invalid day of month provided: ' + clock['day_of_month']
    else:
        print 'no day_of_month value provided!'
        return 'no day_of_month value provided!'
        
    #######
    ## Hour
    if clock.has_key('hour'):
        if valid_hour(clock['hour']):
            if debug:
                print 'Filtering on hour', clock['hour']
                print 'stripping any trailing zeros in the time'
        else:
            print 'Invalid hour detected', clock['hour']
            return 'Invalid hour detected ' + clock['hour'] 
    
    #########
    ## Minute
    if clock.has_key('minute'):
        if valid_minute(clock['minute']):
            if debug:
                print 'Filtering on minute', clock['minute']
        else:
            print 'Invalid minute value provided:', clock['minute']
            return 'Invalid minute value provided:' + clock['minute']
    else:
        print 'No minute value found!'
        return 'no minute value found'

    ret_logs = []
    print 'Pulling information using "show log"'
    syslog = pull_syslog(self, clock)
    print 'Completed pulling information.'
    
    ret_logs.append(syslog)
    
    print 'Pulling the internal logging information.'
    internal_logs = pull_internal_logs(self, clock)
    print 'Complete pulling the internal log informaiton'
    
    ret_logs.append(internal_logs)
    
    print 'Retrieving any core files.'
    retr = pull_corefiles(self, clock)
    print 'Completed pulling core files'
    
    print 'Completed pulling log information'
    return ret_logs
    
    
    
def generate_ixia_dict(source_file, number_of_streams, stream_dict):
    """
    This method takes the variables from the topo.py configuration file and generates
    nested dictionaries that are required for the rewrite_ixia_config method.
    This method is written to shorten the manual labor of making configurations with large
    number of streams (10 or more) and is not required if you want to write the 
    ixia_dictionary by hand.
    
    Variables:
    'Chassis IP Address' - Topo
    'Username'           - Topo
    'Source File'
    'Card Number'        - Topo
    'Port Number'        - Topo
    'Number of Streams'
    # Per stream
    'Stream Name' 
    'Source IP Address'
    'Destination IP Address'
    'Destination MAC Address'
    """
   
    # Example values (working good)
    # with only 1 stream
    """
    ixia_dict = { \
    'Chassis IP Address':'10.4.2.30', \
    'Username':'jalfrey', \
    'Source File':'JF-FUN-009-1.tcl', \
    'Card Number 3':{ \
        'Card Number':3, \
        'Port Number 3':{ \
            'Port Number':3, \
            'Source MAC Address':'00 de bb 00 00 01', \
            'Destination MAC Address':'00 DE BB 00 00 02', \
            'Stream ID 1':{ \
                'Stream ID':1, \
                'Stream Name':'Session_payload', \
                'Source IP Address':'10.11.12.1', \
                'Destination IP Address':'10.11.20.1', \
                'Destination MAC Address':'00 DE BB 00 00 02'
                }
            }
        }
    }
    """
    
    # Topo to ixia_dict variable mapping
    """
    'Chassis IP Address'    = topo.ixia['ip_addr']
    'Username'              = topo.ixia['username']
    'Source File'           = script_var['test_name'] - appears in jf_config.py
    'Card Number'           = topo.ixia['CardID']
    'Port Number'           = topo.ixia['TxportID']
    'Number of Streams'     = script_var['test_name'] - 
    # Per stream
    'Stream Name'           = script_var['test_name'] -
    'Stream ID'             = fed into script
    'Source IP Address'     =  fed into script
    'Destination IP Address' = fed into script
    'Destination MAC Address' = fed into script
    """
    




def rewrite_ixia_config(ixia_dict):
    """
    This function opens an IXIA.tcl script and rewrites the IP Address and other values to make 
    the script send traffic to any DUT
    
    All values MUST be set in this dictionary or the file can not be rewritten correctly!
    
    After this method completes it will write an ouptut file or if set to "none" it will
    return the whole configuration as a very long string which can then be split and fed 
    into the IXIA via CLI 
    
    ixia_dict{
    
    Chassis IP Address:10.4.2.30
    # The IP of the IXIA itself
    
    Username:jalfrey
    # Username that "owns" the ports that will send traffic

    Source File
    # This is the source file it is read from
    # This needs to either be a full path or relative to current directory path
    
    Output File
    # This can be set to "none" and the method will return the whole configuration
    # Or if it is set it will write the file out to disk
    
    Card Number_X: 
    # If there are multiple cards then there will be multiple dictionaries. 
    # For my configuration I use card 3 to the dictionary will be called
    # "Card Number 3"
    Dictionary { 
        Card Number
        # Card which port lives on. Same information contained in the dictionary
        # name but just as the number "3"
        Port Number X:
        # Port to be configured. There will be one key per port
        Dictionary {
            Port Number 
            # This is the port number on the IXIA itself (physical port)
            Source MAC Address
            # Can be set or left "default" which will leave the config unchanged or null ''
            Destination MAC Address
            # This is the MAC of what the IXIA is directly connected to
            # In my case it's a Cisco Router 
            Stream ID X:
            # This is the Stream ID. There is one ID per stream configured
            Dictionary: {
                Stream ID:1
                # Stream numeric ID. Matches "Stream ID X" value X
                Stream Name
                # Optional. If value is Null nothing will be set 
                # whatever was there will be left there
                Source IP Address
                # Source on IXIA side
                Destination IP Address
                # Where the traffic should go. In my case that's the SSX (DUT)
                Destination MAC Address
                # This should be the same as the "Destination MAC Address" found above
                # But clearly it can be set differently but I'm not sure why
                # Maybe for testing through a Hub? 
            }
        }
    }
    
    
    """
    
    debug = False
    
    # Configuration will overwrite this value
    generate_output_file = False
    
    ###############################
    # Variable Validation Section #
    ###############################
    
    if len(ixia_dict) > 0:
        top_keys = ixia_dict.keys()
        if debug:
            print '------------------------------------'
            print 'The top keys extracted were:'
            for key in top_keys:
                print key, ':', ixia_dict[key]
            print '------------------------------------'
                

        # IP Address
        if ixia_dict.has_key('Chassis IP Address'):
            if validIP(ixia_dict['Chassis IP Address']):
                top_keys.remove('Chassis IP Address')
                if debug:
                    print 'Chassis IP is valid'
            else:
                error_message = 'Invalid IP address for the chassis: ' + ixia_dict.has_key('Chassis IP Address')
                return error_message

        # Username
        if ixia_dict.has_key('Username'):
            if (len(ixia_dict['Username']) > 0):
                top_keys.remove('Username')
                if debug:
                    print 'Username is valid'
            else:
                error_message = 'No Username value provided'
                return error_message

        # Source File
        if ixia_dict.has_key('Source File'):
            if (ixia_dict['Source File'] == ''):
                return 'No source file value set'
            if os.path.exists(ixia_dict['Source File']):
                top_keys.remove('Source File')
                if debug:
                    print 'Source filename is valid'
            else:
                return 'unable to locate the source file!'

        # Output File
        # IF the length is zero then no file is generated
        # if it is set to "none" then no file is generated
        # Otherwise whatever the filename is it's generated with that
        # Since the filename could be mostly anything we don't validate it
        if ixia_dict.has_key('Output File'):
            # Here we change the case to lowercase so that we can compare the string once
            # Instead of testing to see if it's formatted like 'None', 'NONE', etc. 
            output_filename = ixia_dict['Output File'].lower()
            if output_filename == 'none':
                generate_output_file = False
                if debug:
                    print 'No output file will be generate'
            else:
                generate_output_file = True
                if debug:
                    print 'Output file will be generated'
            top_keys.remove('Output File')
            if debug:
                print 'Output filename is valid'
        
        if debug:
            print 'At this point the top_keys should only contain card numbers'
            print top_keys
                
                
        # At this point the top_keys dictionary should only contain entries 
        # of card numbers. like "Card Number 3"
        for card_number in top_keys:
            # Now we use this "key" to retrieve all the ports listed for that card
            # Then we verify the port list is valid
            port_list = ixia_dict[card_number].keys()
            if debug:
                print 'Now parsing the following items in the port_list'
                print port_list
            
            for port_number in port_list:
                if 'Card Number' in port_number:   
                    if not (int(ixia_dict[card_number][port_number]) in range(1,15)):
                        error_message = 'Card Number: ' + ixia_dict[card_number][port_number] + ' Outside expected range of: 1-14'
                        return error_message
                if 'Port Number' in port_number:
                    if debug:
                        print '000000000'
                        print 'port_number = ', port_number
                        print 'The port number being tested is:', ixia_dict[card_number][port_number]['Port Number']
                    # The range function is odd. If you say 1,13 you get 13 numbers 
                    # starting at 1 not zero and it ends at 12 instead of 13.
                    if not (int(ixia_dict[card_number][port_number]['Port Number']) in range(1,14)):
                        error_message = 'Port number: ' + port_number + ' on Card: ' \
                         + card_number + ' is invalide. Expected to be in the range 1 - 13'
                        return error_message
                else:
                    if debug:
                        print 'the following item wil not be parsed:'
                        print port_number
    
    else:
        return 'No variables set. Can not proceed!'
    
    ##############
    # Open Files #
    ##############
    try:
        input_file  = open(ixia_dict['Source File'], 'r')
        
    except:
        return 'Unable to open the Soucre File'
    
    if generate_output_file:
        try:
            output_file = open(ixia_dict['Output File'], 'w')
        except:
            return 'Unable to open the ouptut file!'
            
    
    
    ########################
    # Parse the input_file #
    ########################
    
    # Method:
    #
    # 1. Read the file line by line
    # 2. Look for section headers
    #    a. If the line matches one of the section headers we note that down
    #    b. The section header itself may need re-writing
    #    c. Increment the section header counter
    # 3. Inside the sections search for specific lines
    # 4. Read each line and write it to the output file
    # 5. When special lines are found re-write them and write to output file
    
    next_header = '# This Script has been generated by Ixia ScriptGen'
    next_line = 'default_nothing'
    modified_line = 'default_nothing'
    section_index = 0
    line_index = 0
    
    line_count = 0
    break_after = 345
    run_to_completion = True
    raw_keys = ixia_dict.keys()
    card_number_list = []
    port_number_list = []
    for key in raw_keys:
        if 'Card Number' in key:
            card_number_list.append(ixia_dict[key]['Card Number'])
            
    if debug:
        print 'We are expecting to configure the following cards:', card_number_list
    
    if debug:
        print 'Now reading the input file line by line looking for the section headers'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        
    for input_line in input_file:
        line_count = line_count + 1
        
        if debug and (line_count > break_after) and not run_to_completion: 
            print 'Breaking here for debuging'
            return 0
            
        if debug:
            print '******* Line Number:', line_count, ' ********************'
            print 'have: "', input_line.strip(), '"'
            print 'want Header:', next_header
            print '  want Line: "', next_line, '"'
            print '******* Line Number:', line_count, ' ********************'
            
        if next_header in input_line:
            if debug:
                print 'valid header:"', next_header, '"'
            # This will give us a numeric index telling us what section we're in
            section_index = section_index + 1
            
            if section_index == 1:
                next_line = 'if {[ixConnectToTclServer'
                if debug:
                    print 'Found first section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 2:
                modified_line = '######### Chassis list - {' + ixia_dict['Chassis IP Address'] + '} #########\n'
                next_line = 'ixConnectToChassis   {' + local_chassis_ip_address + '}'
                if debug:
                    print 'Found second section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 3:
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if debug:
                    print 'Found second section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 4:
                next_line = 'set card '
                if debug:
                    print 'Found second section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 5:
                long_card_number = 'Card Number ' + str(card_number_list[0])
                raw_port_list = ixia_dict[long_card_number].keys()
                port_name_list = []
                for key in raw_port_list:
                    if 'Port' in key:
                        port_name_list.append(key)

                if debug:
                    print 'building the port_number_list from the port_name_list:'
                    print port_name_list
                    print 'ixia_dict[long_card_number]:', ixia_dict[long_card_number]

                for port in port_name_list:

                    if debug:
                        print 'port:', port 
                        print 'long_card_number:', long_card_number

                    port_number_list.append(ixia_dict[long_card_number][port]['Port Number'])

                    if debug:
                        print 'port_number_list:', port_number_list

                if debug:
                    print 'The ports that will be configured for card:', long_card_number, 'are:', port_number_list
                # Example line
                """
                ######### Chassis-10.4.2.30 Card-3  Port-3 #########
                """
                words = input_line.split()
                raw_port_number = words[3].split('-')
                local_port_number = raw_port_number[1]
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] \
                + ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                if generate_output_file:
                    output_file.write(input_line)
                next_line = 'set port     ' + str(local_port_number)
                
            elif section_index == 6:
                if generate_output_file:
                    output_file.write(input_line)
                # This is a strange one. This header is identical to a header we have already seen in section 5
                # but if we executed the same code it would mess stuff up so we just look for it to step
                # over it. 
                next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + str(local_card_number)
                
            elif section_index == 7:
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + \
                ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if generate_output_file:
                    output_file.write(input_line)
                
            else:
                return 'Failure while parsing the section index'




        # line we're looking for
        elif  (next_line in input_line) and (len(input_line) > 2):
            if debug:
                print 'valid line: "', input_line.strip(), '"'
            words = input_line.split()
            if debug:
                print 'The line was broken into these words:'
                print words 
            
            if section_index == 1:
                if line_index == 0:
                    raw_target_word = words[2].split(']')
                    local_chassis_ip_address = raw_target_word[0]
                    if debug:
                        print 'The Chassis IP Address found in the original configuraiton file was:', local_chassis_ip_address
                    next_line = 'ixPuts "Error connecting to Tcl Server ' + local_chassis_ip_address + ' "'
                    # now we need to rewrite the line and write it to the log file
                    modified_line = '	if {[ixConnectToTclServer ' + ixia_dict['Chassis IP Address'] + ']} {\n'
                    line_index = line_index + 1
                elif line_index == 1:
                    modified_line = '		ixPuts "Error connecting to Tcl Server ' + ixia_dict['Chassis IP Address'] + ' "\n' 
                    # we may need to empy the next line variable because we are looking for a section header
                    #next_line = ''
                    next_header = '######### Chassis list - {' + local_chassis_ip_address + '} #########'
                    line_index = line_index + 1
                    # reset the line index because we are going to the next section
                    line_index = 0
                else:
                    print 'line_index out of range at value:', line_index
                    return 'Error in automation! bad line index in section 1'

                    
            elif section_index == 2:
                if line_index == 0:
                    modified_line = 'ixConnectToChassis   {' + ixia_dict['Chassis IP Address'] + '}\n'
                    next_line = 'set owner "'
                    line_index = line_index + 1
                elif line_index == 1:
                    modified_line = 'set owner "' + ixia_dict['Username'] + '"\n'
                    # going to the next section
                    next_header = '######### Chassis-' + local_chassis_ip_address + ' #########'
                    line_index = 0
                    
            elif section_index == 3:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' +  ixia_dict['Chassis IP Address'] + '"\n'
                    # going to next section
                    next_header = '######### Card Type : 10/100/1000 LSM XMVR16 ############'
                    line_index = 0
                    
            elif section_index == 4:
                if line_index == 0:
                    # There could be multiple cards. It's hard to say if there should be more then one
                    # variable for the card number. I don't think it's neccarry because the system configures
                    # the cards sequentially so it should not be overwritten. 
                    local_card_number = words[2]
                    # We take the first element from the card number list. 
                    # After we're done using that information we will delete it from the list
                    # and then we can use element zero again. (like a stack)
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    #next_header = '######### Chassis-' + local_chassis_ip_address + ' ' + local_card_number
                    next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + local_card_number
                    line_index = 0
                    
            elif section_index == 5:
                if line_index == 0:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'port                         config            -MacAddress                         "'
                elif line_index == 1:
                    long_port_number = 'Port Number ' + str(port_number_list[0])
                    # The source MAC address "can" be configured if you like
                    # But this does lead to more complexity about "what" to configure it to
                    try:
                        modified_line = next_line + ixia_dict[long_card_number][long_port_number]['Source MAC Address'] + '"\n'
                    except:
                        modified_line = input_line
                    line_index = 0
                    next_header = '######### Generating streams for all the ports from above #########'
                else:
                    error_message = 'line_index out of range 0-1 for section_index 5!'
                    return error_message
                    
            elif section_index == 6:
                error_message = 'Failure. Found a line in section six not expected.'
                return error_message
                
            elif section_index == 7:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' + ixia_dict['Chassis IP Address'] + '"\n'
                    line_index = line_index + 1
                    #next_line = 'set card    ' + local_card_number[0]
                    next_line = 'set card'
                elif line_index == 1:
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'set port     ' + local_port_number
                elif line_index == 2:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    """
                    if debug:
                        print 'Looking for the stream ID itself in this dictionary:'
                        print ixia_dict
                        print 'Using these two keys to find it:'
                        print long_card_number, long_port_number
                    """
                    raw_stream_id = ixia_dict[long_card_number][long_port_number].keys()
                    """
                    if debug:
                        print 'Sorting through this list of keys:'
                        print raw_stream_id
                    """
                    stream_id_list = []
                    for key in raw_stream_id:
                        if 'Stream ID' in key:
                            """
                            if debug:
                                print 'Found a Stream ID:', key
                            """
                            stream_id_list.append(key)
                        """
                        elif debug:
                            print 'This value was not the Stream ID:', key
                        """
                    stream_number_list = []
                    for stream_id in stream_id_list:
                        stream_number_list.append(ixia_dict[long_card_number][long_port_number][stream_id])
                    long_stream_id = stream_id_list[0]
                    next_line = 'set streamId ' + str(stream_number_list[0]['Stream ID'])
                    
                    
                # At this point we're configuring the individual streams
                # This will need to recurse itself until done with all the streams
                #
                # At the end of this mess we will check to see if there are more then one streams listed
                # in the stream_numbe_list. If so that means that there are more then on stream that 
                # needs to be rewritten. To achieve this feat we will do a little cute trick.
                # 1. We will remove the first element in the stream_number_list[0]
                # 2. Then we will change the line_index = 2 so that this whole routine
                # is repeated until there are no more streams to rewrite.
                #
                # The hopes are that all the streams are actully in this section. 
                elif line_index == 3:
                    modified_line = 'set streamId ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = '#  Stream ' + str(stream_number_list[0]['Stream ID'])
                    line_index = line_index + 1
                elif line_index == 4:
                    modified_line = '#  Stream ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = 'stream                       config            -name                               "'
                    line_index = line_index + 1
                elif line_index == 5:
                    modified_line = 'stream                       config            -name                               "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Stream Name'] + '"\n'
                    next_line = 'stream                       config            -framesize                          '
                    line_index = line_index + 1
                elif line_index == 6:
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Frame Size'):
                        modified_line = 'stream                       config            -framesize                          ' + \
                        str(ixia_dict[long_card_number][long_port_number][long_stream_id]['Frame Size']) + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip                           config            -sourceIpAddr                       "'
                    line_index = line_index + 1
                elif line_index == 7:
                    modified_line = 'ip                           config            -sourceIpAddr                       "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Address'] + '"\n'
                    next_line = 'ip                           config            -destIpAddr                         "'
                    line_index = line_index + 1
                elif line_index == 8:
                    modified_line = 'ip                           config            -destIpAddr                         "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Address'] + '"\n'
                    next_line = 'ip                           config            -destMacAddr                        "'
                    line_index = line_index + 1
                elif line_index == 9:
                    modified_line = 'ip                           config            -destMacAddr                        "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination MAC Address'] + '"\n'
                    if len(stream_number_list) > 1:
                        stream_number = stream_number_list[0]
                        stream_number_list.remove(stream_number)
                        line_index = 2
                else:
                    error_message = 'Something went wrong while processing the line_index value. Out of range 1-8'
                    return  error_message
                    
            else:
                print 'Something should happen here!'
            
            
            if len(modified_line) > 1:
                # Write out the modified line
                if generate_output_file:
                    if debug:
                        print 'The modified line to be written will be:'
                        print modified_line
                    output_file.write(modified_line)
                else:
                    print 'modified line:', modified_line
                    
            
        else:
            # Write out the original line
            if generate_output_file:
                output_file.write(input_line)
            else:
                """
                if debug:
                    print 'This is the line that would have been written out'
                    print input_line
                    print '-----------------------------------------------------------------------'
                """
    if debug:
        print 'The ending section index is:', section_index
        print 'The ending line index is:', line_index

    # Clean up
    input_file.close()
    if generate_output_file:
        print 'Closing the output file:', output_file
        output_file.close()
    else:
        if debug:
            print 'This is where we would have closed the output file'
    return 0
    
def rewrite_ixia_config_2(ixia_dict):
    # updated for setting auto increment values. used for generating 8k traffic
    
    # Due to a change in the whitepsace of the config the method for finding the next line
    # must be changed. Instead of looking for the complete string the line must be sliced
    # so the whitespace is removed. Then the list must have the varibles removed from it
    # after that the list object can be compared with another list object. 
    # This requires rewrite of all the expected lines to be lists. 
    
    # most lines can be split on whitespace. The lines containing MAC addresses have
    # whitepace where the collons shoudl be. So the comparing logig should only 
    # compare elements expected to elements read. That way it will stop reading before
    # it gets to the MAC. 
    """
    This function opens an IXIA.tcl script and rewrites the IP Address and other values to make 
    the script send traffic to any DUT
    
    All values MUST be set in this dictionary or the file can not be rewritten correctly!
    
    After this method completes it will write an ouptut file or if set to "none" it will
    return the whole configuration as a very long string which can then be split and fed 
    into the IXIA via CLI 
    
    ixia_dict{
    
    Chassis IP Address:10.4.2.30
    # The IP of the IXIA itself
    
    Username:jalfrey
    # Username that "owns" the ports that will send traffic

    Source File
    # This is the source file it is read from
    # This needs to either be a full path or relative to current directory path
    
    Output File
    # This can be set to "none" and the method will return the whole configuration
    # Or if it is set it will write the file out to disk
    
    Card Number_X: 
    # If there are multiple cards then there will be multiple dictionaries. 
    # For my configuration I use card 3 to the dictionary will be called
    # "Card Number 3"
    Dictionary { 
        Card Number
        # Card which port lives on. Same information contained in the dictionary
        # name but just as the number "3"
        Port Number X:
        # Port to be configured. There will be one key per port
        Dictionary {
            Port Number 
            # This is the port number on the IXIA itself (physical port)
            Source MAC Address
            # Can be set or left "default" which will leave the config unchanged or null ''
            Destination MAC Address
            # This is the MAC of what the IXIA is directly connected to
            # In my case it's a Cisco Router 
            Stream ID X:
            # This is the Stream ID. There is one ID per stream configured
            Dictionary: {
                Stream ID:1
                # Stream numeric ID. Matches "Stream ID X" value X
            0 - Stream Name
                # Optional. If value is Null nothing will be set 
                # whatever was there will be left there
            1 - Source IP Address
                # used for incrementing the source IP
            2 - Source IP Mask
            3 - Source IP Address Mode
                # Source on IXIA side
            4 - Source IP Address Repeat Count
                # could be ipIncrHost or ...
            5 - Source Class
                # when ipIncrHost enabled this option is ignored
                
            6 - Destination IP Address
            7 - Destination IP Mask
            8 - Destination IP Address Mode
            9 - Destination IP Address Repeat Count
            10 - Destination Class
                # Where the traffic should go. In my case that's the SSX (DUT)
            11 - Destination MAC Address
                # This should be the same as the "Destination MAC Address" found above
                # But clearly it can be set differently but I'm not sure why
                # Maybe for testing through a Hub? 
            }
        }
    }
    
    
    """

    debug = True
    
    # Configuration will overwrite this value
    generate_output_file = False
    
    ###############################
    # Variable Validation Section #
    ###############################
    
    if len(ixia_dict) > 0:
        top_keys = ixia_dict.keys()
        if debug:
            print '------------------------------------'
            print 'The top keys extracted were:'
            for key in top_keys:
                print key, ':', ixia_dict[key]
            print '------------------------------------'
                

        # IP Address
        if ixia_dict.has_key('Chassis IP Address'):
            if validIP(ixia_dict['Chassis IP Address']):
                top_keys.remove('Chassis IP Address')
                if debug:
                    print 'Chassis IP is valid'
            else:
                error_message = 'Invalid IP address for the chassis: ' + ixia_dict.has_key('Chassis IP Address')
                return error_message

        # Username
        if ixia_dict.has_key('Username'):
            if (len(ixia_dict['Username']) > 0):
                top_keys.remove('Username')
                if debug:
                    print 'Username is valid'
            else:
                error_message = 'No Username value provided'
                return error_message

        # Source File
        if ixia_dict.has_key('Source File'):
            if (ixia_dict['Source File'] == ''):
                return 'No source file value set'
            if os.path.exists(ixia_dict['Source File']):
                top_keys.remove('Source File')
                if debug:
                    print 'Source filename is valid'
            else:
                return 'unable to locate the source file!'

        # Output File
        # IF the length is zero then no file is generated
        # if it is set to "none" then no file is generated
        # Otherwise whatever the filename is it's generated with that
        # Since the filename could be mostly anything we don't validate it
        if ixia_dict.has_key('Output File'):
            # Here we change the case to lowercase so that we can compare the string once
            # Instead of testing to see if it's formatted like 'None', 'NONE', etc. 
            output_filename = ixia_dict['Output File'].lower()
            if output_filename == 'none':
                generate_output_file = False
                if debug:
                    print 'No output file will be generate'
            else:
                generate_output_file = True
                if debug:
                    print 'Output file will be generated'
            top_keys.remove('Output File')
            if debug:
                print 'Output filename is valid'
        
        if debug:
            print 'At this point the top_keys should only contain card numbers'
            print top_keys
                
                
        # At this point the top_keys dictionary should only contain entries 
        # of card numbers. like "Card Number 3"
        for card_number in top_keys:
            # Now we use this "key" to retrieve all the ports listed for that card
            # Then we verify the port list is valid
            port_list = ixia_dict[card_number].keys()
            if debug:
                print 'Now parsing the following items in the port_list'
                print port_list
            
            for port_number in port_list:
                if 'Card Number' in port_number:   
                    if not (int(ixia_dict[card_number][port_number]) in range(1,15)):
                        error_message = 'Card Number: ' + ixia_dict[card_number][port_number] + ' Outside expected range of: 1-14'
                        return error_message
                if 'Port Number' in port_number:
                    if debug:
                        print '000000000'
                        print 'port_number = ', port_number
                        print 'The port number being tested is:', ixia_dict[card_number][port_number]['Port Number']
                    # The range function is odd. If you say 1,13 you get 13 numbers 
                    # starting at 1 not zero and it ends at 12 instead of 13.
                    if not (int(ixia_dict[card_number][port_number]['Port Number']) in range(1,14)):
                        error_message = 'Port number: ' + port_number + ' on Card: ' \
                         + card_number + ' is invalide. Expected to be in the range 1 - 13'
                        return error_message
                else:
                    if debug:
                        print 'the following item wil not be parsed:'
                        print port_number
    
    else:
        return 'No variables set. Can not proceed!'
    
    ##############
    # Open Files #
    ##############
    try:
        input_file  = open(ixia_dict['Source File'], 'r')
        
    except:
        return 'Unable to open the Soucre File'
    
    if generate_output_file:
        try:
            output_file = open(ixia_dict['Output File'], 'w')
        except:
            return 'Unable to open the ouptut file!'
            
    
    
    ########################
    # Parse the input_file #
    ########################
    
    # Method:
    #
    # 1. Read the file line by line
    # 2. Look for section headers
    #    a. If the line matches one of the section headers we note that down
    #    b. The section header itself may need re-writing
    #    c. Increment the section header counter
    # 3. Inside the sections search for specific lines
    # 4. Read each line and write it to the output file
    # 5. When special lines are found re-write them and write to output file
    
    next_header = '# This Script has been generated by Ixia ScriptGen'
    next_line = 'default_nothing'
    modified_line = 'default_nothing'
    section_index = 0
    line_index = 0
    
    line_count = 1
    
    ########################
    ## Used for Debugging ##
    run_to_completion = True
    break_after = 57
    ########################
    
    raw_keys = ixia_dict.keys()
    card_number_list = []
    port_number_list = []
    next_line_cache = ''
    for key in raw_keys:
        if 'Card Number' in key:
            card_number_list.append(ixia_dict[key]['Card Number'])
            
    if debug:
        print 'We are expecting to configure the following cards:', card_number_list
    
    if debug:
        print 'Now reading the input file line by line looking for the section headers'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        
    for input_line in input_file:

        """
        if debug and (line_count >= break_after) and not run_to_completion: 
            print 'Breaking on line:', line_count ,'for debuging'
            return 0

        line_count = line_count + 1
        """
        
        
        ###################
        ## regex rewrite ##
        ###################
        local_debug = False
        
        if not (next_line_cache == next_line):
            if debug:
                print 'the next line we are looking for has changed. Regex will be regenerated'
            next_line_cache = next_line
        #Due to the searching bug we now need to change the next_line variable into a regex here
        
        # Logic
        # chop it into words
        # append the \s* betwen the words. That means any number of spaces in regex
        # then compile it into a regex pattern so we can search using it. 
        if local_debug:
            print 'reworking the next line to become regex'
            print next_line
            
        next_line_words = next_line.split()
        if local_debug:
            print 'the split words are:', next_line_words
            
        raw_regex_next_line = ''
        #word = ''
        if local_debug:
            print '*' * 40
        for raw_word in next_line_words:
            word = ''
            # regex does not like some characters and will fail!
            # we need to "escape" them with an extra slash
            if local_debug:
                print 'looking for invalid characters in word'
            for char in raw_word:
                if local_debug:
                    print 'working on char:', char
                if char in ['[',']','\\','/','{','}']:
                    if local_debug:
                        print 'found a bad char:', char
                    word = word + '[\\' + char + ']'
                else:
                    if local_debug:
                        print 'found a regular char:', char
                    word = word + char
                    
                if local_debug:
                    print 'word is now:', word
                    print '*' * 40
            
                
            if local_debug:
                print 'working on word:', raw_word
            raw_regex_next_line = raw_regex_next_line + word + '\s*'
            if local_debug:
                print 'the raw regex is now:', raw_regex_next_line
                
        # now finally at the end of the statement we need a don't care
        # we will only look for the first part of the statement
        # the end can be anything
        raw_regex_next_line = raw_regex_next_line + '.*'
        
        if local_debug:
            print 'the completed raw regex is:', raw_regex_next_line
            
        next_line_regex = re.compile(raw_regex_next_line)
        
        #######################
        ## end regex rewrite ##
        #######################
        
        if debug:
            print '******* Line Number:', line_count, ' ********************'
            print 'have: "', input_line.strip(), '"'
            print 'want Header:', next_header
            print '  want Line: "', next_line, '"'
            try:
                print '      regex: "', raw_regex_next_line, '"'
            except:
                pass
            print '******* Line Number:', line_count, ' ********************'
            

        
        
        ###############################
        ## Do the regex matchin here ##
        ###############################
        
        #There seems to be no if regex.match logic available
        #so we need to do the logic here so we can use it for a branch later
        
        match = re.search(next_line_regex, input_line)
        

        if next_header in input_line:
            if debug:
                print 'valid section header:', input_line.strip()
                
            # This will give us a numeric index telling us what section we're in
            section_index = section_index + 1
            
            if section_index == 1:
                next_line = 'if {[ixConnectToTclServer'
                if debug:
                    print 'Found first section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 2:
                modified_line = '######### Chassis list - {' + ixia_dict['Chassis IP Address'] + '} #########\n'
                next_line = 'ixConnectToChassis   {' + local_chassis_ip_address + '}'
                if debug:
                    print 'Found second section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 3:
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if debug:
                    print 'Found third section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 4:
                next_line = 'set card '
                if debug:
                    print 'Found fourth section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 5:
                if debug:
                    print 'found fith section header'
                long_card_number = 'Card Number ' + str(card_number_list[0])
                raw_port_list = ixia_dict[long_card_number].keys()
                port_name_list = []
                for key in raw_port_list:
                    if 'Port' in key:
                        port_name_list.append(key)

                if debug:
                    print 'building the port_number_list from the port_name_list:'
                    print port_name_list
                    print 'ixia_dict[long_card_number]:', ixia_dict[long_card_number]

                for port in port_name_list:

                    if debug:
                        print 'port:', port 
                        print 'long_card_number:', long_card_number

                    port_number_list.append(ixia_dict[long_card_number][port]['Port Number'])

                    if debug:
                        print 'port_number_list:', port_number_list

                if debug:
                    print 'The ports that will be configured for card:', long_card_number, 'are:', port_number_list
                                    
                # Example line
                """
                ######### Chassis-10.4.2.30 Card-3  Port-3 #########
                """
                words = input_line.split()
                raw_port_number = words[3].split('-')
                local_port_number = raw_port_number[1]
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] \
                + ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                if generate_output_file:
                    output_file.write(modified_line)
                next_line = 'set port     ' + str(local_port_number)

                    
                
            elif section_index == 6:
                if debug:
                    print 'found sixth section header'
                if generate_output_file:
                    output_file.write(input_line)
                # This is a strange one. This header is identical to a header we have already seen in section 5
                # but if we executed the same code it would mess stuff up so we just look for it to step
                # over it. 
                next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + str(local_card_number)
                
            elif section_index == 7:
                if debug:
                    print 'found seventh section header. (final)'
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + \
                ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if generate_output_file:
                    output_file.write(input_line)
                
            else:
                return 'Failure while parsing the section index'



        elif match:

            """
            The IXIA does not care about the size of the whitespace. Some .tcl files will have different amount
            of space between the variable names. The old method for searching for the lines to replace was:
            if the line we were looking for was:
            "filter config -captureTriggerPattern              anyPattern"
            the value in that line we would want to change would be:
            "anyPattern"
            So the line minus the variable we want to change would be:
            "filter config -captureTriggerPattern              "
            We were checking to see if that partial line was part of the line we wanted to change.
            The problem with this is the spacing of the original line in the tcl script could change. Say like
            "filter config       -captureTriggerPattern              "
            That would cause the line to not be found. 
            
            To work around this problem the following will be done:
            1. The string we are loooking for which is called next_line will be changed into a regular expression
            2. the file will be searched using regular expressions
            """
            # line we're looking for
            #elif  (next_line in input_line) and (len(input_line) > 2):
            # Changed order in statement so lenght is evaluated first. Faster



            if debug:
                print 'Found a next_line: "', input_line.strip(), '"'
            words = input_line.split()
            if debug:
                print 'The line was broken into these words:'
                print words 
            
            if section_index == 1:
                if debug:
                    print 'now in section 1'
                if line_index == 0:
                    raw_target_word = words[2].split(']')
                    local_chassis_ip_address = raw_target_word[0]
                    if debug:
                        print 'The Chassis IP Address found in the original configuraiton file was:', local_chassis_ip_address
                    #next_line = 'errorMsg "Error connecting to Tcl Server ' + local_chassis_ip_address + ' "'
                    next_line = 'errorMsg "Error connecting to Tcl Server 127.0.0.1 "'
                    # now we need to rewrite the line and write it to the log file
                    modified_line = '	if {[ixConnectToTclServer ' + ixia_dict['Chassis IP Address'] + ']} {\n'
                    line_index = line_index + 1
                
                elif line_index == 1:
                    modified_line = '		errorMsg "Error connecting to Tcl Server ' + ixia_dict['Chassis IP Address'] + ' "\n' 
                    # we may need to empy the next line variable because we are looking for a section header
                    #next_line = ''
                    next_header = '######### Chassis list - {' + local_chassis_ip_address + '} #########'
                    line_index = line_index + 1
                    # reset the line index because we are going to the next section
                    line_index = 0
                
                else:
                    print 'line_index out of range at value:', line_index
                    return 'Error in automation! bad line index in section 1'

                    
            elif section_index == 2:
                if line_index == 0:
                    modified_line = 'ixConnectToChassis   {' + ixia_dict['Chassis IP Address'] + '}\n'
                    next_line = 'set owner "'
                    line_index = line_index + 1
                elif line_index == 1:
                    modified_line = 'set owner "' + ixia_dict['Username'] + '"\n'
                    # going to the next section
                    next_header = '######### Chassis-' + local_chassis_ip_address + ' #########'
                    line_index = 0
                    
            elif section_index == 3:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' +  ixia_dict['Chassis IP Address'] + '"\n'
                    # going to next section
                    #next_header = '######### Card Type : 10/100/1000 LSM XMVR16 ############'
                    next_header = '######### Card Type : 10/100/1000 LSM XMVDC16 ############'
                    line_index = 0
                    
            elif section_index == 4:
                if line_index == 0:
                    # There could be multiple cards. It's hard to say if there should be more then one
                    # variable for the card number. I don't think it's neccarry because the system configures
                    # the cards sequentially so it should not be overwritten. 
                    local_card_number = words[2]
                    # We take the first element from the card number list. 
                    # After we're done using that information we will delete it from the list
                    # and then we can use element zero again. (like a stack)
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    #next_header = '######### Chassis-' + local_chassis_ip_address + ' ' + local_card_number
                    #next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + local_card_number
                    next_header = '######### Chassis-127.0.0.1'  + ' Card-' + local_card_number
                    line_index = 0
                    
            elif section_index == 5:
                if line_index == 0:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'port                         config            -MacAddress                         "'
                elif line_index == 1:
                    long_port_number = 'Port Number ' + str(port_number_list[0])
                    # The source MAC address "can" be configured if you like
                    # But this does lead to more complexity about "what" to configure it to
                    try:
                        modified_line = next_line + ixia_dict[long_card_number][long_port_number]['Source MAC Address'] + '"\n'
                    except:
                        modified_line = input_line
                    line_index = 0
                    next_header = '######### Generating streams for all the ports from above #########'
                else:
                    error_message = 'line_index out of range 0-1 for section_index 5!'
                    return error_message
                    
            elif section_index == 6:
                error_message = 'Failure. Found a line in section six not expected.'
                return error_message
                
            elif section_index == 7:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' + ixia_dict['Chassis IP Address'] + '"\n'
                    line_index = line_index + 1
                    #next_line = 'set card    ' + local_card_number[0]
                    next_line = 'set card'
                elif line_index == 1:
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'set port     ' + local_port_number
                elif line_index == 2:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    """
                    if debug:
                        print 'Looking for the stream ID itself in this dictionary:'
                        print ixia_dict
                        print 'Using these two keys to find it:'
                        print long_card_number, long_port_number
                    """
                    raw_stream_id = ixia_dict[long_card_number][long_port_number].keys()
                    """
                    if debug:
                        print 'Sorting through this list of keys:'
                        print raw_stream_id
                    """
                    stream_id_list = []
                    for key in raw_stream_id:
                        if 'Stream ID' in key:
                            """
                            if debug:
                                print 'Found a Stream ID:', key
                            """
                            stream_id_list.append(key)
                        """
                        elif debug:
                            print 'This value was not the Stream ID:', key
                        """
                    stream_number_list = []
                    for stream_id in stream_id_list:
                        stream_number_list.append(ixia_dict[long_card_number][long_port_number][stream_id])
                    long_stream_id = stream_id_list[0]
                    next_line = 'set streamId ' + str(stream_number_list[0]['Stream ID'])
                    
                    
                # At this point we're configuring the individual streams
                # This will need to recurse itself until done with all the streams
                #
                # At the end of this mess we will check to see if there are more then one streams listed
                # in the stream_numbe_list. If so that means that there are more then on stream that 
                # needs to be rewritten. To achieve this feat we will do a little cute trick.
                # 1. We will remove the first element in the stream_number_list[0]
                # 2. Then we will change the line_index = 2 so that this whole routine
                # is repeated until there are no more streams to rewrite.
                #
                # The hopes are that all the streams are actully in this section. 
                elif line_index == 3:
                    modified_line = 'set streamId ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = '#  Stream ' + str(stream_number_list[0]['Stream ID'])
                    line_index = line_index + 1
                elif line_index == 4:
                    modified_line = '#  Stream ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = 'stream                       config            -name                               "'
                    line_index = line_index + 1
                elif line_index == 5:
                    modified_line = 'stream                       config            -name                               "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Stream Name'] + '"\n'
                    next_line = 'stream                       config            -framesize                          '
                    line_index = line_index + 1
                elif line_index == 6:
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Frame Size'):
                        modified_line = 'stream                       config            -framesize                          ' + \
                        str(ixia_dict[long_card_number][long_port_number][long_stream_id]['Frame Size']) + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip                           config            -sourceIpAddr                       "'
                    line_index = line_index + 1
                elif line_index == 7:
                    modified_line = 'ip                           config            -sourceIpAddr                       "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Address'] + '"\n'
                    next_line = 'ip                           config            -destIpAddr                         "'
                    line_index = line_index + 1
                elif line_index == 8:
                    modified_line = 'ip                           config            -destIpAddr                         "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Address'] + '"\n'
                    next_line = 'ip                           config            -destMacAddr                        "'
                    line_index = line_index + 1
                elif line_index == 9:
                    modified_line = 'ip                           config            -destMacAddr                        "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination MAC Address'] + '"\n'
                    if len(stream_number_list) > 1:
                        stream_number = stream_number_list[0]
                        stream_number_list.remove(stream_number)
                        line_index = 2
                else:
                    error_message = 'Something went wrong while processing the line_index value. Out of range 1-8'
                    return  error_message
                    
            else:
                print 'Something should happen here!'
            
            
            if len(modified_line) > 1:
                # Write out the modified line
                if generate_output_file:
                    if debug:
                        print 'The modified line to be written will be:'
                        print modified_line
                    output_file.write(modified_line)
                else:
                    print 'modified line:', modified_line
                    
            
        else:
            # Write out the original line
            if generate_output_file:
                output_file.write(input_line)
            else:
                if debug:
                    print 'This is the line that would have been written out'
                    print input_line.strip()
                    print '-----------------------------------------------------------------------'
        
        #############################
        ## Global debug breakpoint ##
        #############################
        if debug and (line_count >= break_after) and not run_to_completion: 
            print 'Breaking on line:', line_count ,'for debuging'
            return 0

        line_count = line_count + 1 
        ####################
        ## end breakpoint ##
        ####################




    if debug:
        print 'The ending section index is:', section_index
        print 'The ending line index is:', line_index

    # Clean up
    input_file.close()
    if generate_output_file:
        print 'Closing the output file:', output_file
        output_file.close()
    else:
        if debug:
            print 'This is where we would have closed the output file'
    return 0



def rewrite_ixia_config_3(ixia_dict):
    # updated for setting auto increment values. used for generating 8k traffic
    
    # Due to a change in the whitepsace of the config the method for finding the next line
    # must be changed. Instead of looking for the complete string the line must be sliced
    # so the whitespace is removed. Then the list must have the varibles removed from it
    # after that the list object can be compared with another list object. 
    # This requires rewrite of all the expected lines to be lists. 
    
    # most lines can be split on whitespace. The lines containing MAC addresses have
    # whitepace where the collons shoudl be. So the comparing logig should only 
    # compare elements expected to elements read. That way it will stop reading before
    # it gets to the MAC. 
    """
    This function opens an IXIA.tcl script and rewrites the IP Address and other values to make 
    the script send traffic to any DUT
    
    All values MUST be set in this dictionary or the file can not be rewritten correctly!
    
    After this method completes it will write an ouptut file or if set to "none" it will
    return the whole configuration as a very long string which can then be split and fed 
    into the IXIA via CLI 
    
    ixia_dict{
    
    Chassis IP Address:10.4.2.30
    # The IP of the IXIA itself
    
    Username:jalfrey
    # Username that "owns" the ports that will send traffic

    Source File
    # This is the source file it is read from
    # This needs to either be a full path or relative to current directory path
    
    Output File
    # This can be set to "none" and the method will return the whole configuration
    # Or if it is set it will write the file out to disk
    
    Card Number_X: 
    # If there are multiple cards then there will be multiple dictionaries. 
    # For my configuration I use card 3 to the dictionary will be called
    # "Card Number 3"
    Dictionary { 
        Card Number
        # Card which port lives on. Same information contained in the dictionary
        # name but just as the number "3"
        Port Number X:
        # Port to be configured. There will be one key per port
        Dictionary {
            Port Number 
            # This is the port number on the IXIA itself (physical port)
            Source MAC Address
            # Can be set or left "default" which will leave the config unchanged or null ''
            Destination MAC Address
            # This is the MAC of what the IXIA is directly connected to
            # In my case it's a Cisco Router 
            Stream ID X:
            # This is the Stream ID. There is one ID per stream configured
            Dictionary: {
                Stream ID:1
                # Stream numeric ID. Matches "Stream ID X" value X
            0 - Stream Name
                # Optional. If value is Null nothing will be set 
                # whatever was there will be left there
                Frame Size 
            1 - Source IP Address
                # used for incrementing the source IP
            2 - Source IP Mask
            3 - Source IP Address Mode
                # Source on IXIA side
            4 - Source IP Address Repeat Count
                # could be ipIncrHost or ...
            5 - Source Class
                # when ipIncrHost enabled this option is ignored
                
            6 - Destination IP Address
            7 - Destination IP Mask
            8 - Destination IP Address Mode
            9 - Destination IP Address Repeat Count
            10 - Destination Class
                # Where the traffic should go. In my case that's the SSX (DUT)
            11 - Destination MAC Address
                # This should be the same as the "Destination MAC Address" found above
                # But clearly it can be set differently but I'm not sure why
                # Maybe for testing through a Hub? 
            }
        }
    }
    
    
    """

    debug = True
    
    # Configuration will overwrite this value
    generate_output_file = False
    
    ###############################
    # Variable Validation Section #
    ###############################
    
    if len(ixia_dict) > 0:
        top_keys = ixia_dict.keys()
        if debug:
            print '------------------------------------'
            print 'The top keys extracted were:'
            for key in top_keys:
                print key, ':', ixia_dict[key]
            print '------------------------------------'
                

        # IP Address
        if ixia_dict.has_key('Chassis IP Address'):
            if validIP(ixia_dict['Chassis IP Address']):
                top_keys.remove('Chassis IP Address')
                if debug:
                    print 'Chassis IP is valid'
            else:
                error_message = 'Invalid IP address for the chassis: ' + ixia_dict.has_key('Chassis IP Address')
                return error_message

        # Username
        if ixia_dict.has_key('Username'):
            if (len(ixia_dict['Username']) > 0):
                top_keys.remove('Username')
                if debug:
                    print 'Username is valid'
            else:
                error_message = 'No Username value provided'
                return error_message

        # Source File
        if ixia_dict.has_key('Source File'):
            if (ixia_dict['Source File'] == ''):
                return 'No source file value set'
            if os.path.exists(ixia_dict['Source File']):
                top_keys.remove('Source File')
                if debug:
                    print 'Source filename is valid'
            else:
                return 'unable to locate the source file!'

        # Output File
        # IF the length is zero then no file is generated
        # if it is set to "none" then no file is generated
        # Otherwise whatever the filename is it's generated with that
        # Since the filename could be mostly anything we don't validate it
        if ixia_dict.has_key('Output File'):
            # Here we change the case to lowercase so that we can compare the string once
            # Instead of testing to see if it's formatted like 'None', 'NONE', etc. 
            output_filename = ixia_dict['Output File'].lower()
            if output_filename == 'none':
                generate_output_file = False
                if debug:
                    print 'No output file will be generate'
            else:
                generate_output_file = True
                if debug:
                    print 'Output file will be generated'
            top_keys.remove('Output File')
            if debug:
                print 'Output filename is valid'
        
        if debug:
            print 'At this point the top_keys should only contain card numbers'
            print top_keys
                
                
        # At this point the top_keys dictionary should only contain entries 
        # of card numbers. like "Card Number 3"
        for card_number in top_keys:
            # Now we use this "key" to retrieve all the ports listed for that card
            # Then we verify the port list is valid
            port_list = ixia_dict[card_number].keys()
            if debug:
                print 'Now parsing the following items in the port_list'
                print port_list
            
            for port_number in port_list:
                if 'Card Number' in port_number:   
                    if not (int(ixia_dict[card_number][port_number]) in range(1,15)):
                        error_message = 'Card Number: ' + ixia_dict[card_number][port_number] + ' Outside expected range of: 1-14'
                        return error_message
                if 'Port Number' in port_number:
                    if debug:
                        print '000000000'
                        print 'port_number = ', port_number
                        print 'The port number being tested is:', ixia_dict[card_number][port_number]['Port Number']
                    # The range function is odd. If you say 1,13 you get 13 numbers 
                    # starting at 1 not zero and it ends at 12 instead of 13.
                    if not (int(ixia_dict[card_number][port_number]['Port Number']) in range(1,14)):
                        error_message = 'Port number: ' + port_number + ' on Card: ' \
                         + card_number + ' is invalide. Expected to be in the range 1 - 13'
                        return error_message
                else:
                    if debug:
                        print 'the following item wil not be parsed:'
                        print port_number
    
    else:
        return 'No variables set. Can not proceed!'
    
    ##############
    # Open Files #
    ##############
    try:
        input_file  = open(ixia_dict['Source File'], 'r')
        
    except:
        return 'Unable to open the Soucre File'
    
    if generate_output_file:
        try:
            output_file = open(ixia_dict['Output File'], 'w')
        except:
            return 'Unable to open the ouptut file!'
            
    
    
    ########################
    # Parse the input_file #
    ########################
    
    # Method:
    #
    # 1. Read the file line by line
    # 2. Look for section headers
    #    a. If the line matches one of the section headers we note that down
    #    b. The section header itself may need re-writing
    #    c. Increment the section header counter
    # 3. Inside the sections search for specific lines
    # 4. Read each line and write it to the output file
    # 5. When special lines are found re-write them and write to output file
    
    next_header = '# This Script has been generated by Ixia ScriptGen'
    next_line = 'default_nothing'
    modified_line = 'default_nothing'
    section_index = 0
    line_index = 0
    
    line_count = 1
    
    ########################
    ## Used for Debugging ##
    run_to_completion = True
    break_after = 57
    ########################
    
    raw_keys = ixia_dict.keys()
    card_number_list = []
    port_number_list = []
    next_line_cache = ''
    for key in raw_keys:
        if 'Card Number' in key:
            card_number_list.append(ixia_dict[key]['Card Number'])
            
    if debug:
        print 'We are expecting to configure the following cards:', card_number_list
    
    if debug:
        print 'Now reading the input file line by line looking for the section headers'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        print '-----------------------------------------------------------------------'
        
    for input_line in input_file:

        """
        if debug and (line_count >= break_after) and not run_to_completion: 
            print 'Breaking on line:', line_count ,'for debuging'
            return 0

        line_count = line_count + 1
        """
        
        
        ###################
        ## regex rewrite ##
        ###################
        local_debug = False
        
        if not (next_line_cache == next_line):
            if debug:
                print 'the next line we are looking for has changed. Regex will be regenerated'
            next_line_cache = next_line
        #Due to the searching bug we now need to change the next_line variable into a regex here
        
        # Logic
        # chop it into words
        # append the \s* betwen the words. That means any number of spaces in regex
        # then compile it into a regex pattern so we can search using it. 
        if local_debug:
            print 'reworking the next line to become regex'
            print next_line
            
        next_line_words = next_line.split()
        if local_debug:
            print 'the split words are:', next_line_words
            
        raw_regex_next_line = ''
        #word = ''
        if local_debug:
            print '*' * 40
        for raw_word in next_line_words:
            word = ''
            # regex does not like some characters and will fail!
            # we need to "escape" them with an extra slash
            if local_debug:
                print 'looking for invalid characters in word'
            for char in raw_word:
                if local_debug:
                    print 'working on char:', char
                if char in ['[',']','\\','/','{','}']:
                    if local_debug:
                        print 'found a bad char:', char
                    word = word + '[\\' + char + ']'
                else:
                    if local_debug:
                        print 'found a regular char:', char
                    word = word + char
                    
                if local_debug:
                    print 'word is now:', word
                    print '*' * 40
            
                
            if local_debug:
                print 'working on word:', raw_word
            raw_regex_next_line = raw_regex_next_line + word + '\s*'
            if local_debug:
                print 'the raw regex is now:', raw_regex_next_line
                
        # now finally at the end of the statement we need a don't care
        # we will only look for the first part of the statement
        # the end can be anything
        raw_regex_next_line = raw_regex_next_line + '.*'
        
        if local_debug:
            print 'the completed raw regex is:', raw_regex_next_line
            
        next_line_regex = re.compile(raw_regex_next_line)
        
        #######################
        ## end regex rewrite ##
        #######################
        
        if debug:
            print '******* Line Number:', line_count, ' ********************'
            print 'have: "', input_line.strip(), '"'
            print 'want Header:', next_header
            print '  want Line: "', next_line, '"'
            try:
                print '      regex: "', raw_regex_next_line, '"'
            except:
                pass
            print '******* Line Number:', line_count, ' ********************'
            

        
        
        ###############################
        ## Do the regex matchin here ##
        ###############################
        
        #There seems to be no if regex.match logic available
        #so we need to do the logic here so we can use it for a branch later
        
        match = re.search(next_line_regex, input_line)
        

        if next_header in input_line:
            if debug:
                print 'valid section header:', input_line.strip()
                
            # This will give us a numeric index telling us what section we're in
            section_index = section_index + 1
            
            if section_index == 1:
                next_line = 'if {[ixConnectToTclServer'
                if debug:
                    print 'Found first section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 2:
                modified_line = '######### Chassis list - {' + ixia_dict['Chassis IP Address'] + '} #########\n'
                next_line = 'ixConnectToChassis   {' + local_chassis_ip_address + '}'
                if debug:
                    print 'Found second section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 3:
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if debug:
                    print 'Found third section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(modified_line)
                    
            elif section_index == 4:
                next_line = 'set card '
                if debug:
                    print 'Found fourth section header'
                    print 'next_line updated to:', next_line
                if generate_output_file:
                    output_file.write(input_line)
                    
            elif section_index == 5:
                if debug:
                    print 'found fith section header'
                long_card_number = 'Card Number ' + str(card_number_list[0])
                raw_port_list = ixia_dict[long_card_number].keys()
                port_name_list = []
                for key in raw_port_list:
                    if 'Port' in key:
                        port_name_list.append(key)

                if debug:
                    print 'building the port_number_list from the port_name_list:'
                    print port_name_list
                    print 'ixia_dict[long_card_number]:', ixia_dict[long_card_number]

                for port in port_name_list:

                    if debug:
                        print 'port:', port 
                        print 'long_card_number:', long_card_number

                    port_number_list.append(ixia_dict[long_card_number][port]['Port Number'])

                    if debug:
                        print 'port_number_list:', port_number_list

                if debug:
                    print 'The ports that will be configured for card:', long_card_number, 'are:', port_number_list
                                    
                # Example line
                """
                ######### Chassis-10.4.2.30 Card-3  Port-3 #########
                """
                words = input_line.split()
                raw_port_number = words[3].split('-')
                local_port_number = raw_port_number[1]
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] \
                + ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                if generate_output_file:
                    output_file.write(modified_line)
                next_line = 'set port     ' + str(local_port_number)

                    
                
            elif section_index == 6:
                if debug:
                    print 'found sixth section header'
                if generate_output_file:
                    output_file.write(input_line)
                # This is a strange one. This header is identical to a header we have already seen in section 5
                # but if we executed the same code it would mess stuff up so we just look for it to step
                # over it. 
                next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + str(local_card_number)
                
            elif section_index == 7:
                if debug:
                    print 'found seventh section header. (final)'
                modified_line = '######### Chassis-' + ixia_dict['Chassis IP Address'] + \
                ' Card-' + str(card_number_list[0]) + ' Port-' + str(port_number_list[0]) +  ' #########\n'
                next_line = 'chassis                      get               "' + local_chassis_ip_address + '"'
                if generate_output_file:
                    output_file.write(input_line)
                
            else:
                return 'Failure while parsing the section index'



        elif match:

            """
            The IXIA does not care about the size of the whitespace. Some .tcl files will have different amount
            of space between the variable names. The old method for searching for the lines to replace was:
            if the line we were looking for was:
            "filter config -captureTriggerPattern              anyPattern"
            the value in that line we would want to change would be:
            "anyPattern"
            So the line minus the variable we want to change would be:
            "filter config -captureTriggerPattern              "
            We were checking to see if that partial line was part of the line we wanted to change.
            The problem with this is the spacing of the original line in the tcl script could change. Say like
            "filter config       -captureTriggerPattern              "
            That would cause the line to not be found. 
            
            To work around this problem the following will be done:
            1. The string we are loooking for which is called next_line will be changed into a regular expression
            2. the file will be searched using regular expressions
            """
            # line we're looking for
            #elif  (next_line in input_line) and (len(input_line) > 2):
            # Changed order in statement so lenght is evaluated first. Faster



            if debug:
                print 'Found a next_line: "', input_line.strip(), '"'
            words = input_line.split()
            if debug:
                print 'The line was broken into these words:'
                print words 
            
            if section_index == 1:
                if debug:
                    print 'now in section 1'
                if line_index == 0:
                    raw_target_word = words[2].split(']')
                    local_chassis_ip_address = raw_target_word[0]
                    if debug:
                        print 'The Chassis IP Address found in the original configuraiton file was:', local_chassis_ip_address
                    #next_line = 'errorMsg "Error connecting to Tcl Server ' + local_chassis_ip_address + ' "'
                    next_line = 'errorMsg "Error connecting to Tcl Server 127.0.0.1 "'
                    # now we need to rewrite the line and write it to the log file
                    modified_line = '	if {[ixConnectToTclServer ' + ixia_dict['Chassis IP Address'] + ']} {\n'
                    line_index = line_index + 1
                
                elif line_index == 1:
                    modified_line = '		errorMsg "Error connecting to Tcl Server ' + ixia_dict['Chassis IP Address'] + ' "\n' 
                    # we may need to empy the next line variable because we are looking for a section header
                    #next_line = ''
                    next_header = '######### Chassis list - {' + local_chassis_ip_address + '} #########'
                    line_index = line_index + 1
                    # reset the line index because we are going to the next section
                    line_index = 0
                
                else:
                    print 'line_index out of range at value:', line_index
                    return 'Error in automation! bad line index in section 1'

                    
            elif section_index == 2:
                if line_index == 0:
                    modified_line = 'ixConnectToChassis   {' + ixia_dict['Chassis IP Address'] + '}\n'
                    next_line = 'set owner "'
                    line_index = line_index + 1
                elif line_index == 1:
                    modified_line = 'set owner "' + ixia_dict['Username'] + '"\n'
                    # going to the next section
                    next_header = '######### Chassis-' + local_chassis_ip_address + ' #########'
                    line_index = 0
                    
            elif section_index == 3:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' +  ixia_dict['Chassis IP Address'] + '"\n'
                    # going to next section
                    #next_header = '######### Card Type : 10/100/1000 LSM XMVR16 ############'
                    next_header = '######### Card Type : 10/100/1000 LSM XMVDC16 ############'
                    line_index = 0
                    
            elif section_index == 4:
                if line_index == 0:
                    # There could be multiple cards. It's hard to say if there should be more then one
                    # variable for the card number. I don't think it's neccarry because the system configures
                    # the cards sequentially so it should not be overwritten. 
                    local_card_number = words[2]
                    # We take the first element from the card number list. 
                    # After we're done using that information we will delete it from the list
                    # and then we can use element zero again. (like a stack)
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    #next_header = '######### Chassis-' + local_chassis_ip_address + ' ' + local_card_number
                    #next_header = '######### Chassis-' + local_chassis_ip_address + ' Card-' + local_card_number
                    next_header = '######### Chassis-127.0.0.1'  + ' Card-' + local_card_number
                    line_index = 0
                    
            elif section_index == 5:
                if line_index == 0:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'port config -MacAddress                         "'
                elif line_index == 1:
                    long_port_number = 'Port Number ' + str(port_number_list[0])
                    # The source MAC address "can" be configured if you like
                    # But this does lead to more complexity about "what" to configure it to
                    try:
                        modified_line = next_line + ixia_dict[long_card_number][long_port_number]['Source MAC Address'] + '"\n'
                    except:
                        modified_line = input_line
                    line_index = 0
                    next_header = '######### Generating streams for all the ports from above #########'
                else:
                    error_message = 'line_index out of range 0-1 for section_index 5!'
                    return error_message
                    
            elif section_index == 6:
                error_message = 'Failure. Found a line in section six not expected.'
                return error_message
                
            elif section_index == 7:
                if line_index == 0:
                    modified_line = 'chassis                      get               "' + ixia_dict['Chassis IP Address'] + '"\n'
                    line_index = line_index + 1
                    #next_line = 'set card    ' + local_card_number[0]
                    next_line = 'set card'
                elif line_index == 1:
                    modified_line = 'set card     ' + str(card_number_list[0]) + '\n'
                    line_index = line_index + 1
                    next_line = 'set port     ' + local_port_number
                elif line_index == 2:
                    modified_line = 'set port     ' + str(port_number_list[0]) + '\n'
                    line_index = line_index + 1
                    """
                    if debug:
                        print 'Looking for the stream ID itself in this dictionary:'
                        print ixia_dict
                        print 'Using these two keys to find it:'
                        print long_card_number, long_port_number
                    """
                    raw_stream_id = ixia_dict[long_card_number][long_port_number].keys()
                    """
                    if debug:
                        print 'Sorting through this list of keys:'
                        print raw_stream_id
                    """
                    stream_id_list = []
                    for key in raw_stream_id:
                        if 'Stream ID' in key:
                            """
                            if debug:
                                print 'Found a Stream ID:', key
                            """
                            stream_id_list.append(key)
                        """
                        elif debug:
                            print 'This value was not the Stream ID:', key
                        """
                    stream_number_list = []
                    for stream_id in stream_id_list:
                        stream_number_list.append(ixia_dict[long_card_number][long_port_number][stream_id])
                    long_stream_id = stream_id_list[0]
                    next_line = 'set streamId ' + str(stream_number_list[0]['Stream ID'])
                    
                    
                # At this point we're configuring the individual streams
                # This will need to recurse itself until done with all the streams
                #
                # At the end of this mess we will check to see if there are more then one streams listed
                # in the stream_numbe_list. If so that means that there are more then on stream that 
                # needs to be rewritten. To achieve this feat we will do a little cute trick.
                # 1. We will remove the first element in the stream_number_list[0]
                # 2. Then we will change the line_index = 2 so that this whole routine
                # is repeated until there are no more streams to rewrite.
                #
                # The hopes are that all the streams are actully in this section. 
                elif line_index == 3:
                    ## Stream ID ##
                    modified_line = 'set streamId ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = '#  Stream ' + str(stream_number_list[0]['Stream ID'])
                    line_index = line_index + 1
                elif line_index == 4:
                    ## Stream number ##
                    modified_line = '#  Stream ' + str(stream_number_list[0]['Stream ID']) + '\n'
                    next_line = 'stream config -name                               "'
                    line_index = line_index + 1
                elif line_index == 5:
                    ## Stream name ##
                    modified_line = 'stream config -name                               "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Stream Name'] + '"\n'
                    next_line = 'stream config -framesize                          '
                    line_index = line_index + 1
                elif line_index == 6:
                    ## Framesize ##
                    # There may be a bug here. It looks like the new framesize is not single quoted
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Frame Size'):
                        modified_line = 'stream config -framesize                          ' + \
                        str(ixia_dict[long_card_number][long_port_number][long_stream_id]['Frame Size']) + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -sourceIpAddr                       "'
                    line_index = line_index + 1
                elif line_index == 7:
                    ## source IP Address ##
                    modified_line = 'ip config -sourceIpAddr                       "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Address'] + '"\n'
                    #next_line = 'ip                           config            -destIpAddr                         "'
                    next_line = 'ip config -sourceIpMask                       "'
                    line_index = line_index + 1
                
                ## New variables ##
                # This is where the new variables come in
                elif line_index == 8:
                    ## source IP Address Mask ##
                    # generally set to "255.255.0.0"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Source IP Mask'):
                        modified_line = 'ip config -sourceIpMask                       "' + \
                        ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Mask'] + '"\n'
                        
                    else:
                        modified_line = input_line
                    next_line = 'ip config -sourceIpAddrMode'
                    line_index = line_index + 1
                elif line_index == 9:
                    ## source IP Address Mode ##
                    # normally set to "ipIncrHost"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Source IP Address Mode'):
                        modified_line = 'ip config -sourceIpAddrMode                   ' + \
                        ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Address Mode'] + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -sourceIpAddrRepeatCount'
                    line_index = line_index + 1
                elif line_index == 10:
                    ## source IP Address Repeat Count##
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Source IP Address Repeat Count'):
                        modified_line = 'ip config -sourceIpAddrRepeatCount            ' + \
                        str(ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Address Repeat Count']) + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -sourceClass'
                    line_index = line_index + 1
                    
                elif line_index == 11:
                    ## source IP Class ##
                    # used for incerementing the source IP. 
                    # typicall set to "classC"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Source IP Class'):
                        modified_line = 'ip config -sourceClass                        ' + \
                        ixia_dict[long_card_number][long_port_number][long_stream_id]['Source IP Class'] + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -destIpAddr'
                    line_index = line_index + 1

                ## End new variables ##
                
                #elif line_index == 8:
                # generally set to ""30.222.0.1""
                # string is quoted
                elif line_index == 12:
                    ## destination IP address
                    modified_line = 'ip config -destIpAddr                         "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Address'] + '"\n'
                    #next_line = 'ip                           config            -destMacAddr                        "'
                    next_line = 'ip config -destIpAddrMode'
                    line_index = line_index + 1
                
                ## New variables ##

                elif line_index == 13:
                    ## destination IP Address Mode ##
                    # genearlly set to "ipIncrHost"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Destination IP Address Mode'):                    
                        modified_line = 'ip config -destIpAddrMode                     ' + \
                        ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Address Mode'] + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -destIpAddrRepeatCount'
                    line_index = line_index + 1
                

                elif line_index == 14:
                    ## destination IP Address Repeat Count ##
                    # genearlly set to "4096"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Destination IP Address Repeat Count'):                    
                        modified_line = 'ip config -destIpAddrRepeatCount              ' + \
                        str(ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Address Repeat Count']) + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -destClass'
                    line_index = line_index + 1


                elif line_index == 15:
                    ## destination Class ##
                    # genearlly set to "classC"
                    if ixia_dict[long_card_number][long_port_number][long_stream_id].has_key('Destination IP Class'):                    
                        modified_line = 'ip config -destClass                          ' + \
                        ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination IP Class'] + '\n'
                    else:
                        modified_line = input_line
                    next_line = 'ip config -destMacAddr'
                    line_index = line_index + 1

                
                ## end new variables ##
                
                #elif line_index == 9:
                elif line_index == 16:
                    ## Destionation MAC address
                    
                    ## Debug
                    print ixia_dict[long_card_number][long_port_number][long_stream_id].keys()
                    
                    modified_line = 'ip config -destMacAddr                        "' + \
                    ixia_dict[long_card_number][long_port_number][long_stream_id]['Destination MAC Address'] + '"\n'
                    if len(stream_number_list) > 1:
                        stream_number = stream_number_list[0]
                        stream_number_list.remove(stream_number)
                        line_index = 2
                else:
                    error_message = 'Something went wrong while processing the line_index value. Out of range 1-8'
                    return  error_message
                    
            else:
                print 'Something should happen here!'
            
            
            if len(modified_line) > 1:
                # Write out the modified line
                if generate_output_file:
                    if debug:
                        print 'The modified line to be written will be:'
                        print modified_line
                    output_file.write(modified_line)
                else:
                    print 'modified line:', modified_line
                    
            
        else:
            # Write out the original line
            if generate_output_file:
                output_file.write(input_line)
            else:
                if debug:
                    print 'This is the line that would have been written out'
                    print input_line.strip()
                    print '-----------------------------------------------------------------------'
        
        #############################
        ## Global debug breakpoint ##
        #############################
        if debug and (line_count >= break_after) and not run_to_completion: 
            print 'Breaking on line:', line_count ,'for debuging'
            return 0

        line_count = line_count + 1 
        ####################
        ## end breakpoint ##
        ####################




    if debug:
        print 'The ending section index is:', section_index
        print 'The ending line index is:', line_index

    # Clean up
    input_file.close()
    if generate_output_file:
        print 'Closing the output file:', output_file
        output_file.close()
    else:
        if debug:
            print 'This is where we would have closed the output file'
    return 0
    
        
                
    
def scp_to_ixia(source_file, destination_file, ixia = '10.1.10.12', username = 'ixia', password = '1102607'):
    """
    This simple method will copy a file from your local filesystem to the IXIA of choice
    to the specified file location
    """
    # local debug
    debug = True
    max_copy_time = 120
    
    if debug:
        print 'now in issu.py scp_to_ixia'
        
        
    if debug:
        print 'incoming variables:'
        print '  source_file:', source_file
        print '  destination_file:', destination_file
        print '  ixia:', ixia
        print '  username:', username 
        print '  password:', password
        
    # The Logging functions change the current working directory (CWD) to /Logs
    # That means all the files end up in /Logs instead of the script directory
    # This leads to confusion and a mess. 
    current_dir = os.getcwd()
    
    if debug:
        print 'current working dir is:', current_dir
    
    dir_name = os.path.split(current_dir)
    
    
        
    if 'Logs' in dir_name:
        if debug:
            print 'we are in the log dir!'
        in_log_dir = True
    else:
        if debug:
            print 'we are not in the log dir!'
        in_log_dir = False
        
    if in_log_dir:
        os.chdir('../')


    # we will use the os.system method. It has many failures. The best way would be to use
    # a library called paramiko. But you would need to install it everywhere
    if debug:
        print 'trying to SCP the file'

    
    """
    the format of the scp command is:
    scp <local file> <username>@<hostname/IP>:<destination file>
    """
    no_hostname = 'nodename nor servname provided, or not known'
    accept_key = 'Are you sure you want to continue connecting (yes/no)?'
    password_prompt = 'password:'
    bad_username_password = 'Permission denied, please try again.'
    no_such_local_file = 'No such file or directory'
    permission_denied = 'Permission denied'
    
    if debug:
        print 'the command will be:'
        print "scp -q %s %s@%s:%s" % (source_file, username, ixia, destination_file)
    ses = pexpect.spawn("scp -q %s %s@%s:%s" % (source_file, username, ixia, destination_file))
    
    # This is where you set the timeout for the SCP to start
    retr = ses.expect([accept_key, password_prompt, no_hostname, permission_denied], timeout = 10)
    if retr == 0:
        # This is the accept_key optionn:
        ses.sendline('yes')
        retr == ses.expect([password_prompt], timeout = 10)
        if retr == 0:
            # This is the password option:
            ses.sendline(password)
        else:
            print 'timeout waiting for password prompt'
            raise("timeout during SCP")
    elif retr == 1:
        # This is the password option:
        if debug:
            print ses.before
        ses.sendline(password)
    elif retr == 2:
        # no_hostname option
        print ses.before()
        raise("unable to SCP file. Error in command")
    elif retr == 3:
        # Permission denied
        raise("Permission denied")
    else:
        print 'timeoute while trying to SCP file'
        raise("timout during SCP")
    # this is where the max copy time is set. That means how long it takes to transfer the file
    # It's set at 120 seconds (2 minutes). That should be pleanty for any IXIA config
    #retr = ses.expect([bad_username_password, '$', no_such_local_file], timeout = max_copy_time)
    retr = ses.expect([bad_username_password, pexpect.EOF, no_such_local_file], timeout = max_copy_time)
    if retr == 0:
        print 'bad username or password provided'
        raise('bad username or password provided')
    elif retr == 1:
        if debug:
            print 'SCP successful'
    elif retr == 2:
        error_root = ses.before
        error_message = 'No such file or directory: %s' % error_root        
        print error_message
        raise('No such file or directory')
    else:
        error_message = 'maximum time: %s for SCP to complete exceeded' %  max_copy_time
        print error_message
        raise('Max copy time exceeded')
    
    
        
    return 0
    
    
def get_mac_cisco(cisco_ip, interface):
    """
    Connects to cisco and retrieves the MAC address for the interface specified.
    
    Input:
    cisco_ip = hostname or IP of console
    interface = interface on cisco. 1/0, 3/1 etc.
    
    Returns:
    MAC address
    """
    """
    All API dealing with the cisco are passed only the cisco IP. The idea is to not 
    remain connected. Cisco configuration is infrequent and generally we remain
    disconnected during the test. 
    """

    debug = True
    
    if debug:
        print 'connecting to cisco:', cisco_ip
    cisco = CISCO.CISCO(cisco_ip)
    cisco.console(cisco_ip)
    
    if debug:
        print 'figuring out the full interface name'
        
    # This code taken from CISCO.py clear_interface_config
    out = cisco.cmd("sh ip interface brief | inc %s"%interface)
    intType=re.search("(\w+Ethernet)",out).group(0)

    # conf = self.cmd("show running interface %s %s"%(intType,intf))
    interface_name = intType + ' ' + interface
    
    if debug:
        print 'the interface name is:', interface_name
    
    raw_line = cisco.cmd("show interfaces %s | include address" % interface_name)
    raw_words = raw_line.split()
    
    if debug:
        print 'raw words:', raw_words
        print 'this should be the MAC:', raw_words[6]
        
    return raw_words[6]
        
    cisco.close()

def get_mac_ssx(self, interface):
    """
    takes the SSX object. retrieves the MAC address of the port specified
    
    Input:
    SSX Object
    interface = 2/1, 3/2
    
    Returns:
    MAC address
    """
    """
    We are going to run into some problems here. the SSX can have two or four
    ports per line card. There is no way of knowing in advance if the port
    exists prior to retrieving the information. There needs to be some way
    of signaling the developer that the port does not exist. 
    """
    debug = True
    if debug:
        print 'retrieving the port information for port:', interface
        
    port_detail = show_port_detail(self, interface)
    
    if debug:
        print 'here is the dictionary we got back:'
        print port_detail[interface]
    
    return port_detail[interface]['MAC Address']
    
def cisco_mac_to_ixia_mac(mac_address):
    """
    The MAC address from a cisco is formatted: "0013.196e.0a81"
    The IXIA MAC format is                     "01 80 C2 00 00 01"
    
    This API converts from cisco to ixia format
    """
    
    debug = True
    
    if debug:
        print 'incomding MAC:', mac_address
        
    parts = str.upper(mac_address).split('.')
    part_1 = parts[0][:2]
    part_2 = parts[0][2:]
    part_3 = parts[1][2:]
    part_4 = parts[1][:2]
    part_5 = parts[2][2:]
    part_6 = parts[2][:2]
    
    ixia_mac = part_1 + ' ' + part_2 + ' ' + part_3 + ' ' + part_4 + ' ' + part_5 + ' ' + part_6
    
    return ixia_mac
    
    

def ssx_mac_to_ixia_mac(mac_address):
    """
    The MAC address from a ssx is formatted: "00:12:73:00:64:a0"
    The IXIA MAC format is                   "01 80 C2 00 00 01"
    
    This API converts from ssx to ixia format
    """
    debug = True
    
    if debug:
        print 'incoming MAC:', mac_address
        
    parts = str.upper(mac_address).split(':')
    
    
    ixia_mac = parts[0] + ' ' + parts[1] + ' ' + parts[2] + ' ' + parts[3] + ' ' + parts[4] + ' ' + parts[5]
    
    return ixia_mac    
    
    
   
def ftp(source_file, destination_file, hostname='localhost', destination_directory='current', username='regress', password='gleep7',getOrPut='put'):
    """
    This is a simple function that will take a local file specified as "source_file" 
    and FTP put it to a remote system into the destination_directory if specified.
    There are two optional variables to set the "username" and "password" of the
    remote FTP server. 
    
    source_file = full path and filename of the source file or relative path
    destination_file = the filename itself
    hostname = ip address or hostname
    destination_directory = just the directory not the filename
    username = ftp username
    password = password for that user
    getOrPut = ftp put/get.  Default: put
    
    When this function finishes it will return. If anything is returned the put/get failed.
    Return value will be the error message.
    """
    debug = False
    timeout = 10
    
    if (not os.path.exists(source_file)) and (getOrPut == 'put'):
	# check source file only if it is a put 
        return 'Invalid source file:' + source_file
    
    if debug:
        if hostname == 'localhost':
            print 'Openning connection to localhost'
        else:
            print 'Openning connection to', hostname
            
    cmd = 'ftp ' + hostname
    if debug:
        print 'command will be:', cmd
    

    try:
        ses = pexpect.spawn(cmd)
    except:
        error_message = 'unable to connect to host ' + hostname
        return error_message

    
    prompt = 'Name'
    retr = ses.expect([prompt, 'Connection refused'], timeout=timeout)
    if debug:
        print 'retr ', retr
    # This is what we want
    if retr == 0:
        if debug:
            print 'username ', username
        ses.sendline(username)
        retr = ses.expect(['Password required'], timeout=timeout)
        if retr == 0:
            if debug:
                print 'password ', password
            ses.sendline(password)
            prompt = 'ftp>'
            retr = ses.expect([prompt, 'cannot log in'], timeout=timeout)
            if retr == 0:
                print 'succusffully logged into host:', hostname
            elif retr == 1:
                return 'invalid username or password'
            else:
                return 'timeout while waiting for login (network error)'
    
    if retr == 1:
        error_message = 'Connection refused'
        return error_message
    if retr == 2:
        error_message = 'Timeout while connecting'
        return error_message

    if not (destination_directory == 'current'):
        cmd = 'cd ' + destination_directory
        if debug:
            print 'comand will be:', cmd
        ses.sendline(cmd)
        retr = ses.expect(['command successful', 'find the file specified','CWD successful'], timeout=timeout)
        if debug:
            print 'retr', retr
        if retr > 2:
            return 'Unable to change directory to: ' + destination_directory
        else:
            print 'changed directory to:', destination_directory
	# expect the prompt
        retr = ses.expect([prompt], timeout=timeout)
        if retr > 0:
            return 'Unable to get the prompt'
        else:
            if debug:
                print 'Get the prompt'
   
    if getOrPut == 'put': 
        cmd = 'put ' +  destination_file
    else:
	cmd = 'get ' + source_file + " " + destination_file
    if debug:
        print 'cmd ', cmd
    time.sleep(5)
    ses.sendline(cmd)
    retr = ses.expect(["Transfer OK",prompt], timeout)
    if debug:
        print 'retr ', retr
    if retr > 1:
        return 'unable to put the file'
    else:
        print 'file:', destination_file, 'was %s to the server successfully' %getOrPut
        
    cmd = 'bye'
    ses.sendline(cmd)
    # Done!
    return 0
        
    

    
def clear_context(self, context=""):
    """Clear the configuration of a specific context on a SSX
    Leaves no context behind. Rewrite of clear_context from device.py
    """
    debug = False
    
    # Checking to make sure the context exists!
    context_list = list_contexts(self)
    context_names = context_list.keys()
    if context in context_names:
        print "Clearing the configuration of context:", context
        command = 'config'
        
        if debug:
            print 'command will be:', command
            
        retrn_val = self.cmd(command)
        
        command = 'no context ' + context
        
        if debug:
            print 'command will be:', command
            
        retrn_val = self.cmd(command)
        
        # Code needs to be written to handle any failed return value
        if debug:
            print 'Command returned:', retrn_val
        
        command = 'end'
        if debug:
            print 'command will be:', command
            
        retrn_val = self.cmd(command)        
        
        
        ################################
        ## Verify Context was Removed ##
        ################################
        print 'Verifying Context was removed'
        command = 'show configuration context ' + context
        if debug:
            print 'The command will be:', command
        raw_retrn_val = self.cmd(command)
        retrn_val = string.lstrip(raw_retrn_val)
        expected_string = 'ERROR: Context ' + context + ' not found'
        
        if debug:
            print 'Checking to see if:'
            print '"', expected_string, '" = "', retrn_val, '"'
            
        if retrn_val == expected_string:
            print 'Context was succesfully removed'
            return
        else:
            print 'Context was NOT removed!'
            print 'System returned:', retrn_val
            sys.exit(1)
        
    else:
        print 'Context name provided:', context, 'Is NOT a context on the SSX. FAIL'
        sys.exit(1)

def minimal_configuration(self):
    """
    This method will remove all the contexts except local. This will allow loading of configuration
    without conflicting configuration from the last config used. It will also work over a telnet session
    """
    
    debug = False
    
    context_dict = list_contexts(self)
    if debug:
        print "the SSX has the following contexts:"
    context_list = context_dict.keys()
    
    if debug:
        print "=========================================="
        print "About to remove all contexts except local"
        
    for context in context_list:
        if context != 'local':
            if debug:
                print "About to clear the context:", context
            retrn_val = clear_context(self, context)
            if debug:
                print "returned:", retrn_val
                print "Context was cleared sucessfully"
                
    print 'All configuration was removed successfully except "local" context'
    
    # Now we need to unblind all the physical interfaces. 
    print 'unbinding all the Ethernet ports except admin (0/0, 1/0)'
    
    unbind_interfaces(self)
    
    return

def unbind_interfaces(self, protect_admin=True):
    """
    This will remove all the physical port configuration
    By default it will not remove the admin ports of 0/0 and 1/0
    """
    # Example Port Config
    """
    australia(cfg-port)#show conf port 
    port ethernet 0/0
     bind interface mgmt local
      exit
     enable
     exit
    port ethernet 1/0
     bind interface mgmt local
      exit
     enable
     exit
    port ethernet 2/0
     bind interface 2-0 r2
      ipsec policy ikev2 phase1 name p11
      ipsec policy ikev2 phase2 name p12
      exit
     service ipsec
     enable
     exit
    port ethernet 2/1
     bind interface 2-1 tunnels
      ipsec policy ikev2 phase1 name ph1_c1
      ipsec policy ikev2 phase2 name ph2_c1
      exit
     service ipsec
     enable
     exit
    port ethernet 2/2
     bind interface 2-2 r2
      exit
     enable
     exit
    port ethernet 2/3
     bind interface 2-3 tunnels
      exit
     enable
     exit
    port ethernet 3/0
     service ipsec
     enable
     exit
    port ethernet 3/1
     enable
     exit
    port ethernet 3/2
     enable
     exit
    port ethernet 3/3
     enable
     exit
    port ethernet 4/0
     bind interface ashu local
      exit
     service ipsec
     enable
     exit
    port ethernet 4/1
     enable
     exit
    port ethernet 4/2
     enable
     exit
    port ethernet 4/3
     enable
     exit
    """
    debug = False
    
    admin_ports = ['0/0','1/0']
    
    command = 'show conf port '
    raw_ports = self.cmd(command)
    port_conf = raw_ports.splitlines()
    # This is a list where we accumulate the commands
    # we will execute to clear the ports
    clear_commands = []
    # used to ignore the configuration in an admin port
    admin_port = False

    if debug:
        print '------------------------------------'
    for raw_line in port_conf:
        if len(raw_line) > 1:
            if debug:
                print 'The raw line is:'
                print raw_line
            words = raw_line.split()
            if debug:
                print 'after split:'
                print words
                print 'checking to see if this is an interface name'
            if words[0] == 'port':
                if debug:
                    print 'testing:', words[2]
                if words[2] in valid_port_list:
                    if debug:
                        print 'found and interface:', words[2]
                    if words[2] not in admin_ports:
                        admin_port = False
                        if debug:
                            print 'Found a port:', words[2]
                            print 'Saving it to the clear_commands'
                        if len(clear_commands) > 0:
                            clear_commands.append('exit')
                        clear_commands.append(raw_line)
                    else:
                        if protect_admin:
                            if debug:
                                print 'found an admin port'
                                print 'port will be left configured'
                            admin_port = True
                        if protect_admin == False:
                            if debug:
                                print 'found an admin interface'
                                print 'Will be unconfiguring it as well'
                            admin_port = False
                else:
                    if debug:
                        print 'This line not an interface'
                        print raw_line
            elif admin_port == False:
                if debug:
                    'line not protected as admin'
                if not 'exit' == words[0]:
                    no_line = 'no' + raw_line
                    if debug:
                        print 'no line:'
                        print no_line
                    clear_commands.append(no_line)
                else:
                    if debug:
                        print 'discarding:', raw_line
            else:
                if debug:
                    print 'discarding this line'
                    print raw_line
        if debug:
            print '------------------------------------'
         
    if debug:
        print 'Completed processing the port config'
        print 'now removing the interfaces'
        print 'The commands that will be run are:'
        print '----------------------------------'
        for line in clear_commands:
            print line
    
    
    command = 'conf'
    self.cmd(command)
    for line in clear_commands:
        self.cmd(line)
        
    if debug:
        print 'completed sending commands'
        
    command = 'end'
    self.cmd(command)
    return




def odd_or_even(value):
    """
    Very simple check to see if an integer is odd or even
    """
    try:
        int(value)
    except:
        return 'Value provided was not an integer'
    
    
    return value%2 and 'Odd' or 'Even'



    

def ssx_date_to_log(date, offset=0):
    """
    This function will take the date/time from the SSX command "show clock" and then reformat the
    date/time to be identical to the event log format of "event-log-yyyymmdd-hhmmss".
    This method is for generating the fake log files required to verify the log errasal
    This method takes as it's input the date and an offset in days. 
    The method will subtract the offset in days from the original days
    """
    
    debug = False
    
    try:
        int(offset)
    except:
        print 'The offset value passed:', offset, 'Was not an integer!'
        raise("invalid offset value %s" % offset)
    

    
    begin_time_stamp_parts = date.split()
    test_year = int(begin_time_stamp_parts[3])
    if debug:
        print 'test_year:', test_year
    test_letter_month = begin_time_stamp_parts[1]
    if debug:
        print 'test_letter_month:', test_letter_month
    test_month = name_month_to_num(test_letter_month)
    if debug:
        print 'test_month:', test_month
    test_day = int(begin_time_stamp_parts[2])
    if debug:
        print 'test_day:', test_day
    time_parts = begin_time_stamp_parts[4].split(':')
    if debug:
        print 'time_parts:', time_parts
    test_hour = int(time_parts[0])
    if debug:
        print 'test_hour', time_parts
    test_minute = int(time_parts[1])
    if debug:
        print 'test_minute:', test_minute
    test_second = int(time_parts[2])
    if debug:
        print 'test_second:', test_second
    
    # Convert the date/time into python native format
    if debug:
        print test_year, test_month, test_day, test_hour, test_minute, test_second
    now = datetime.datetime(test_year, test_month, test_day, test_hour, test_minute, test_second)

    if not(offset == 0):
        actual_offset = datetime.timedelta(days=offset)
        calculated_date = now - actual_offset
    else:
        calculated_date = now
        
    log_filename = calculated_date.strftime("%Y%m%d-%H%M%S")
    
    return log_filename
    

def nslookup_by_host(hostname):
    """
    This runs just like a command line nslookup command. You provide the hostname.
    Method returns the IP Address
    """
    debug = False
    
    if debug:
        print 'about to retrieve the ip for:', hostname 
    try:
        output = socket.gethostbyname(hostname)
        if debug:
            print 'the raw output was:', output 
    except:
        output = 'not found'
        
    return output    
        
    
def nslookup_by_ip(ip_address):
    """
    This runs just like a command line nslookup command. You provide the IP I provide the hostname    
    
    This method is broken on our systems! I don't know why. It works fine on my mac. 
    """
    debug = False
    
    if debug:
        print 'received the following IP Adress:', ip_address
    if validIP(ip_address):
        try:
            output = socket.gethostbyaddr(ip_address)
            if debug:
                print 'the raw output was:', output 
            return output[0]
        except:
            output = 'not available'
            return output 
        
    else:
        output = 'invalid IP adderss provided'
        return output  



def unix_to_dos_path(path):
    """
    On UNIX the path is formated using the forward slash /
    On Windows the path uses the backslash \
    So when you are using UNIX with windows you will need to convert
    any path statements. This takes the UNIX style path and generates a
    python friendly DOS style of path. (adding extra slashes to escape the slashes)
    
    the companion function is called dos_to_unix
    """
    debug = False
    if debug:
        print 'now in issu.py unix_to_dos'
        
    if debug:
        print 'the path passed was:'
        print path
    
    return_path = ntpath.abspath(path)
    
    return return_path
    
    
def dos_to_unix_path(path):
    """
    On UNIX the path is formated using the forward slash /
    On Windows the path uses the backslash \
    So when you are using UNIX with windows you will need to convert
    any path statements. This takes the DOS style path and generates a
    python friendly UNIX style of path. (adding extra slashes to escape the slashes)
    
    the companion function is called unix_to_dos
    """
    debug = False
    if debug:
        print 'now in issu.py dos_to_unix'
    
    if debug:
        print 'the path passed was:'
        print path
    
    return_path = ''
    if debug:
        print '*' * 40
    for char in path:
        if debug:
            print 'processing char:', char
        if char == '\\':
            if debug:
                print 'changing slash'
            return_path = return_path + '/'
        else:
            return_path = return_path + char
        if debug:
            print 'accumulated path:'
            print return_path
            print '*' * 40
    
    if debug:
        print 'the return_path looks like:'
        print return_path
        print path
        
    return return_path
            

    
def select_to_base(self, base_version):
    """
    This method will take the version and select the system back to that base version. 
    This would be used at the beginning of any ISSU related test to set the system to a
    known version. 
    
    The version iformation consists of two values.
    The version itself like:        4.6B2 = package name
    The build ID like:         2010051019 = build
    
    base_version = {'package_name':'4.6B2', 'build':'2010051019'}
    """
    debug = False
    
    # Get the current version from the SSX
    running_ver = self.ssx.get_version()
    
    if debug:
        self.myLog.info("The system is currently running %s " % running_ver)
    
    
    #if (running_ver['build'] == topo.base_version['build']):
    if (running_ver['build'] == base_version['build']):
        if debug:
            self.myLog.debug("Build version on system same as base version: %s" % running_ver['build'])
        build_the_same = True
    else:
        build_the_same = False
    #if (running_ver['branch'] == topo.base_version['package_name']):
    if (running_ver['branch'] == base_version['package_name']):
        self.myLog.debug("Branch name on the system same as base version: %s" % running_ver['branch'])
        branch_the_same = True
    else:
        branch_the_same = False
    
    if build_the_same and branch_the_same:
        if debug:
            self.myLog.info('System is running base version already. No install/select required')
    else:
        if debug:
            self.myLog.info('About to boot the system with the base version')
            #self.myLog.info("Base version is: %s " % topo.base_version)
            self.myLog.info("Base version is: %s " % base_version)
            self.myLog.debug("8888888888888888888")
        #retr = install_base(self.ssx, topo.base_version)
        retr = install_base(self.ssx, base_version)
        if debug:
            self.myLog.debug("8888888888888888888")
        if retr:
            self.myLog.error('Somethine went wrong when selecting to base version!')
            self.myLog.error(" it was: %s", retr)
            sys.exit(1)
        
        # we need to close that file handle to create a fresh one. 
        time.sleep(2)
        self.ssx.close()
        reboot_time = 200
        if debug:
            self.myLog.info("waiting for the system to finish rebooting: %s seconds" % reboot_time)
        time.sleep(reboot_time)
        rebooting = True
        retries = 20
        while rebooting:
            if debug:
                self.myLog.info('Sleeping for 30 seconds')
            time.sleep(30)
            try:
                if debug:
                    self.myLog.info('Connecting to SSX')
                self.ssx.telnet()
                if debug:
                    self.myLog.info('Made it past the telnet command')
                # if that command does not fail then the rebooting state should change
                rebooting = False  
            except:
                if debug:
                    self.myLog.info('System not up yet')
            retries = retries - 1
            if debug:
                self.myLog.info("%s retries left" % retries)
            if retries == 0:
                if debug:
                    self.myLog.info("System never came back up after select!")
                # Need to return the failure here
                #sys.exit(1)
                return 'System never came back up after select!'
        
        if debug:
            self.myLog.info('Completed Select to base version')

        self.ssx.wait4cards()
        
        return 'complete'
    
        
    



def session_counters_handle(self, session_handle):
    """This method pulls the session counters via the session handle.
	   it executes "show session counters handle <handle>"
       It returns a dictionary containing all the fields present in the output
    """
    if debug:
        print 'Now in issu.py session_counters_handle method'
    
    # Example Data
    """
    01 Tue May 11 10:32:22 PDT 2010.
    02
    03 Username             Session    Rcv Pkts    Xmit Pkts   Rcv Bytes   Xmit Bytes
    04                      Handle
    05 -------------------- ---------- ----------- ----------- ----------- ----------- 
    06 16502102800650210@r2 fc44020b         58869       58897     2708020     2709492
    """
    
    # If you provide an invalid session handle there is no response from the SSX
    # This will result in an empty dictionary being returned. 
    
    results = {}
    
    command = "show session counters handle %s" % session_handle
    session_counters_raw = self.cmd(command)
    
    if debug:
        print 'This is the raw result:', session_counters_raw
    
    if len(session_counters_raw) > 0:
        # Chop the ouput into lines
        session_counters = session_counters_raw.splitlines()
        # We have a good idea of what the ouptut is going to look like. 
        # The very last line "should" always contain our data. 
        # The column headers will not change so we don't need to look at them. 
        words = session_counters[-1:].split()
        
        results['Username'] = words[0]
        results['Session Handle'] = words[1]
        results['Rcv Pkts'] = words[2] 
        results['Xmit Pkts'] = words[3]
        results['Rcv Bytes'] = words[4]
        results['Xmit Bytes'] = words[5]
        
        if debug:
            print 'Completed parsing the output. This is what we got:'
            print results  
        
        return results
        
        
    else:
        print 'Invalid Session Handle provided:', session_handle
        return 0

def session_counters_username(self, username):
    """This method pulls the session counters via the session username.
       It returns a dictionary containing all the fields present in the output
    """
    if debug:
        print 'Now in issu.py session_counters_username method'
    
    # Example Data
    """
    01 Tue May 11 10:32:22 PDT 2010.
    02
    03 Username             Session    Rcv Pkts    Xmit Pkts   Rcv Bytes   Xmit Bytes
    04                      Handle
    05 -------------------- ---------- ----------- ----------- ----------- ----------- 
    06 16502102800650210@r2 fc44020b         58869       58897     2708020     2709492
    """
    
    # If you provide an invalid session handle there is no response from the SSX
    # This will result in an empty dictionary being returned. 
    
    results = {}
    
    command = "show session counters username %s" % username
    session_counters_raw = self.cmd(command)
    
    if debug:
        print 'This is the raw result:', session_counters_raw
    
    if len(session_counters_raw) > 0:
        # Chop the ouput into lines
        session_counters = session_counters_raw.splitlines()
        # We have a good idea of what the ouptut is going to look like. 
        # The very last line "should" always contain our data. 
        # The column headers will not change so we don't need to look at them. 
        words = session_counters[-1:].split()
        
        results['Username'] = words[0]
        results['Session Handle'] = words[1]
        results['Rcv Pkts'] = words[2] 
        results['Xmit Pkts'] = words[3]
        results['Rcv Bytes'] = words[4]
        results['Xmit Bytes'] = words[5]
        
        if debug:
            print 'Completed parsing the output. This is what we got:'
            print results  
        
        return results
        
        
    else:
        print 'Invalid Session Handle provided:', session_handle
        return 0

def session_counters(self):
    """This returns a list indexed on username of every session listed along with a 
       dictionary of the values
    """
    
    debug = False
    
    if debug:
        print 'Now in issu.py session_counters_method'
    
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
    
    # If you provide an invalid session handle there is no response from the SSX
    # This will result in an empty dictionary being returned. 
    
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
        
        """
        if debug:
            print 'The lines we will process are:'
            print session_counters[line_count:]
        """
            
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
            
        return results 
		
def show_process(self, slot='all'):
    """Runs the command 'show process' and parses the output. 
    """
    slot_list = ['slot 0','slot 1','slot 2','slot 3','slot 4']
    process_dict = {}
    debug = False
    
    # Sample raw input
    """
    australia[local]#show process 
    01 Name           PID     StartTime                CPU NumThreads Priority
    02 -------------- ------- ------------------------ --- ---------- --------
    03 NSM:0           651272 Tue Jun 01 15:31:53        0         21        7
    04 Smid:0          696345 Tue Jun 01 15:32:03        0         10        7
    05 Ip:0            696349 Tue Jun 01 15:32:07        0         32        7
    06 CtxMgr:0        696348 Tue Jun 01 15:32:07        0          9        7
    07 Fpd:0           696347 Tue Jun 01 15:32:06        0         16        7
    08 Aaad:0          696353 Tue Jun 01 15:32:09        1         31        7
    09 Cli:0           696368 Tue Jun 01 15:36:39        0          8        7
    10 Snmpd:0         696355 Tue Jun 01 15:32:09        0          9        7
    11 Inets:0         696354 Tue Jun 01 15:32:09        0         13        7
    12 Logind:0        696346 Tue Jun 01 15:32:06        0          9        7
    13 Ospf:0          696350 Tue Jun 01 15:32:07        0         10        7
    14 Bgp4:0          696351 Tue Jun 01 15:32:07        0         11        7
    15 Evl:0           696342 Tue Jun 01 15:32:03        0         13        7
    16 EvlColl:0       696343 Tue Jun 01 15:32:03        0          8        7
    17 Qosd:0          696352 Tue Jun 01 15:32:07        0         10        7
    18 IkedMc:0        696356 Tue Jun 01 15:32:09        0         11        7
    19 Ntp:0           696357 Tue Jun 01 15:32:09        0         10        7
    20 Rip:0           696358 Tue Jun 01 15:32:09        0         12        7
    21 Evt:0           696341 Tue Jun 01 15:32:03        0          9        7
    22 Fabric:0        696364 Tue Jun 01 15:32:09        0          8        7
    """
    if slot == 'all':
        command = 'show process'
    elif slot in slot_list:
        command = 'show process ' + slot  
    else:
        print 'Invalide specification for slot:', slot 
        print 'Expected slot to be one of the following:', slot_list
        return 'Invalid option'
        
    raw_process_list = self.cmd(command)
    process_list = raw_process_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print process_list
    
    for raw_line in process_list[3:]:
        line = raw_line.split()
        local_dict = {}
        if debug:
            print '----------------------------------------------'
            print 'The line to be processes is:'
            print line
        raw_name = line[0].split(':')
        name = raw_name[0]
        if debug:
            print 'The name is:', name 
    
        local_dict['pid'] = line[1]
        if debug:
            print 'The PID is:', local_dict['pid']
        day = line[2]
        month = line[3]
        year = line[4]
        time = line[5]
        start_time = day, month, year, time 
        local_dict['start_time'] = start_time
        if debug:
            print 'The start time is:', local_dict['start_time']
        local_dict['cpu'] = line[6]
        if debug:
            print 'The CPU it\'s on is:', local_dict['cpu']
        local_dict['number_of_threads'] = line[7]
        if debug:
            print 'The number of threads is:', local_dict['number_of_threads']
        local_dict['priority'] = line[8]
        if debug:
            print 'The priority is:', local_dict['priority']
        # We store each entry in the main dictionary we return
        process_dict[name] = local_dict
    
    return process_dict
    
    
def show_process_cpu(self, slot='all'):
    """Runs the command 'show process' and parses the output. 
    """
    slot_list = ['slot 0','slot 1','slot 2','slot 3','slot 4']
    process_dict = {}
    debug = False
    
    
    # Sample raw input
    
    # If you have normal page breaks turned on (normal CLI) you will see the 
    # banner information containing the column headers like "name" "PID" etc.
    # at every page break. You will also see the CPU Utilization again
    # This information is redundant and will be identical
    """
    australia[local]#show process cpu
    01 CPU0 Utilization for 5 seconds:  3.45%   1 Minute:  5.20%   5 Minutes: 11.56%
    02 CPU1 Utilization for 5 seconds:  0.21%   1 Minute:  0.22%   5 Minutes:  2.68%
    03 
    04 Name           PID     StartTime                CPU uTime  sTime  % Now
    05 -------------- ------- ------------------------ --- ------ ------ ------
    06 System:0             0 Mon Jun 20 13:22:23      0/1 16.337  5.995  0.00%
    07 NSM:0           602115 Mon Jun 20 13:22:22        0  6.909  0.904  1.09%
    08 Smid:0          671769 Mon Jun 20 13:22:31        0  1.004  0.065  0.00%
    09 Ip:0            671773 Mon Jun 20 13:22:33        0  0.524  0.095  0.09%
    10 CtxMgr:0        671772 Mon Jun 20 13:22:33        0  0.100  0.009  0.00%
    11 Fpd:0           671771 Mon Jun 20 13:22:33        0  0.253  0.037  0.19%
    12 Aaad:0          671777 Mon Jun 20 13:22:34        1  0.217  0.140  0.00%
    13 Cli:0           831542 Mon Jun 20 13:23:21        0  0.976  0.043  0.79%
    14 Cli:1           999472 Mon Jun 20 13:27:01        0  0.839  0.009  0.00%
    15 Snmpd:0         671779 Mon Jun 20 13:22:34        0  0.128  0.020  0.00%
    16 Inets:0         671778 Mon Jun 20 13:22:34        0  0.128  0.034  0.00%
    17 Logind:0        671770 Mon Jun 20 13:22:33        0  0.088  0.006  0.00%
    18 Logind:1        831541 Mon Jun 20 13:23:20        0  0.079  0.007  0.00%
    19 Ospf:0          671774 Mon Jun 20 13:22:33        0  0.126  0.013  0.00%
    20 Bgp4:0          671775 Mon Jun 20 13:22:33        0  0.132  0.016  0.00%
    21 Evl:0           671766 Mon Jun 20 13:22:31        0  0.113  0.012  0.00%
    22 EvlColl:0       671767 Mon Jun 20 13:22:31        0  0.101  0.027  0.00%
    23 Qosd:0          671776 Mon Jun 20 13:22:33        0  0.118  0.010  0.00%
    24 IkedMc:0        671780 Mon Jun 20 13:22:34        0  0.145  0.023  0.00%
    25 Ntp:0           671781 Mon Jun 20 13:22:34        0  0.106  0.021  0.00%
    26 Rip:0           671782 Mon Jun 20 13:22:34        0  0.127  0.013  0.00%
    27 Evt:0           671765 Mon Jun 20 13:22:31        0  0.129  0.029  0.00%
    28 Fabric:0        671788 Mon Jun 20 13:22:35        0  0.091  0.012  0.00%
    29 Fsync:0         671768 Mon Jun 20 13:22:31        0  0.171  0.170  0.00%
    30 TunMgr:0        671783 Mon Jun 20 13:22:34        0  0.095  0.022  0.00%
    31 PPPoEMC:0       671784 Mon Jun 20 13:22:34        0  0.091  0.016  0.00%
    32 PPPdMc:0        671785 Mon Jun 20 13:22:34        0  0.102  0.021  0.00%
    33 CDR:0           671786 Mon Jun 20 13:22:34        0  0.182  0.012  0.00%
    34 DHCPdMC:0       671787 Mon Jun 20 13:22:35        0  0.123  0.018  0.00%
    35 MIPd:0          671789 Mon Jun 20 13:22:35        0  0.133  0.021  0.00%
    36 SLA:0           671790 Mon Jun 20 13:22:35        0  0.101  0.014  0.00%
    37 Dfn:0           671791 Mon Jun 20 13:22:35        1  0.194  0.108  0.00%
    """
    
    if debug:
        print 'now in show_process_cpu in issu.py'
    
    if slot == 'all':
        command = 'show process cpu'
    elif slot in slot_list:
        command = 'show process cpu slot' + slot  
    else:
        print 'Invalid specification for slot:', slot 
        print 'Expected slot to be one of the following:', slot_list
        return 'Invalid option'
        
    raw_process_list = self.cmd(command)
    #raw_process_list = cmd(command)
    process_list = raw_process_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print process_list
    
    # processing this output will be split into two sections
    # Section 1:
    # This includes the cpu utilization stats. (2 lines)
    # Section 2:
    # This includes the states for each process (all other lines)

    #############
    # Section 1 #
    #############
    
    """
    {'CPU0': 
        {'1 minute': '7.28', 
        '5 minute': '4.44', 
        '5 second': '20.63'}, 
    'CPU1': 
        {'1 minute': '0.48', 
        '5 minute': '0.25', 
        '5 second': '0.17'}}
    """
    
    if debug:
        print 'now processing the CPU usage header'
        print '-----------------------------------'
    cpu_usage = {}
    local_dict = {}
    for line_number in range(1,3):
        if debug:
            print 'now processing line:', line_number
            print 'Raw line:', process_list[line_number]
            
        raw_input = process_list[line_number].split()
        if debug:
            print 'the splite elements are:'
            print raw_input
            
        cpu_number = raw_input[0]
        if debug:
            print 'now processing:', cpu_number
            
        local_dict[cpu_number] = {}
        
        ## 5 Second
        raw_five_second = raw_input[5]
        if debug:
            print 'processing the 5 second value:', raw_five_second
        # This is index notation for everything except the last char
        # on the line
        five_second = raw_five_second[:-1]
        if debug:
            print '5 second average:', five_second
        local_dict[cpu_number]['5 second'] = five_second
        

        ## 1 minute
        raw_one_minute = raw_input[8]
        if debug:
            print 'processing the 1 minute value:', raw_one_minute
        # This is index notation for everything except the last char
        # on the line
        one_minute = raw_one_minute[:-1]
        if debug:
            print '1 minute average:', one_minute
        local_dict[cpu_number]['1 minute'] = one_minute


        ## 5 minute
        raw_five_minute = raw_input[11]
        if debug:
            print 'processing the 5 minute value:', raw_five_minute
        # This is index notation for everything except the last char
        # on the line
        five_minute = raw_five_minute[:-1]
        if debug:
            print '5 minute average:', five_minute
        local_dict[cpu_number]['5 minute'] = five_minute

    if debug:
        print 'The CPU utilizaiton dictionary contains:'
        print local_dict
    
    process_dict['CPU Utilization'] = local_dict
    
    if debug:
        print 'The return dictionary (process_dict) now contains:'
        print process_dict
                
    
    #############
    # Section 2 #
    #############
    if debug:
        print 'now processing per process stats'
        print '--------------------------------'
        
    for raw_line in process_list[6:]:
        if debug:
            print 'now processing raw line:'
            print raw_line
        line = raw_line.split()
        local_dict = {}
        
        raw_name = line[0].split(':')
        
        ## Process Name
        name = raw_name[0]
        if debug:
            print 'The name is:', name 
    
        ## PID (program ID)
        local_dict['pid'] = line[1]
        if debug:
            print 'The PID is:', local_dict['pid']
        
        ## Start Time
        day = line[2]
        month = line[3]
        year = line[4]
        time = line[5]
        start_time = day, month, year, time 
        local_dict['start_time'] = start_time
        if debug:
            print 'The start time is:', local_dict['start_time']


        ## CPU 
        local_dict['CPU'] = line[6]
        if debug:
            print 'running on CPU:', local_dict['CPU']
            
        ## uTime  
        local_dict['uTime'] = line[7]
        if debug:
            print 'running uTime:', local_dict['uTime']
            
        ## sTime  
        local_dict['sTime'] = line[8]
        if debug:
            print 'runnit sTime:', local_dict['sTime']
        
        ## % Now
        raw_percent_now = line[9]
        # This strips the '%' off the value to make it easier
        # to process with automation
        local_dict['percent now'] = raw_percent_now[:-1]
        if debug:
            print '% now:', local_dict['percent now']
    

        # We store each entry in the main dictionary we return
        process_dict[name] = local_dict

        # uncomment of to process only 1 line
        """
        if debug:
            print '--------------------------'
            print 'stopping here for debuging'
            print '--------------------------'
            sys.exit(1)
        """
            
    if debug:
        print 'returning from show_process_cpu'
        print '-------------------------------'
    return process_dict
    
def show_tunnel_details(self, slot = 'all', handle = 'none'):
    """Retrieves the 'show ike-session list' information then 
       filters out only tunnels.
       Once tunnel handle is known can filter by handle
       Can also be filted by slot.
    """
    debug = False
    slot_range = [0,1,2,3,4,'all']
    tunnel_list = []
    
    if not (slot in slot_range):
        print 'Invalid slot passed:', slot
        print 'Expected to be one of the following:', slot_range
        return 'Invalid Slot number supplied'
    
    if slot == 'all':
        raw_session_list = list_ike_sessions(self)
    else:
        raw_session_list = list_ike_sessions(self, slot)
    
    if raw_session_list == 'No Sessions present':
        return 'No Tunnels present'
        
    if debug:
        print 'The raw_session list contains:'
        print raw_session_list
    
    # The format of the Tunnel response is similar to the tha of a Session
    # The differences are as follows:
    # 1. Contains 6 lines of output
    # 2. IKE Version = 2 <LAN<->LAN>
    # we will filter on the second option
    for item in raw_session_list:
        if debug:
            print 'the complete item is:'
            print item
            print 'Searching for ike version info'
            print item['IKE Version']
        if item['IKE Version'] == '2 <LAN<->LAN>':
            if debug:
                print '!!!!Found a tunnel!!!!'
            tunnel_list.append(item)
    
    if debug:
        print 'Here are the Tunnels'
        print tunnel_list

    return tunnel_list
    

def show_session_details(self, slot = 'all', handle = 'none'):
    """Retrieves the 'show ike-session list' information then 
       filters out only tunnels.
       Once tunnel handle is known can filter by handle
       Can also be filted by slot.
    """
    # Method not yet written. 


def show_time(self):
    """
    runs the "show clock" command returns the output
    """
    debug = False
    ret_dict = {}
    if debug:
        print 'now in issu.py show_time'
    
    time_stamp = self.cmd('show clock')
    if debug:
        print("The timestamp that was retrieved is: %s" % time_stamp)
    
    # The raw input looks like this
    """
    Mon Jul 19 2010 10:43:43 PDT
    """
    if debug:
        print("Parsing the current time")
    
    # We parse it into it's elements
    raw_time = time_stamp.split()
    ret_dict['day_of_week'] = raw_time[0]
    ret_dict['month'] = raw_time[1]
    ret_dict['day_of_month'] = raw_time[2]
    ret_dict['year'] = raw_time[3]
    raw_long_time = raw_time[4]
    ret_dict['timezone'] = raw_time[5]
    
    long_time = raw_long_time.split(":")
    ret_dict['hour'] = long_time[0]
    ret_dict['minute'] = long_time[1]
    ret_dict['second'] = long_time[2]
    
    if debug:
        print 'The fully parsed values are:'
        print ret_dict
    
    return ret_dict


def show_port_counters_detail(self, filter_port = 'None'):
    """
    This function runs the command "show port counters detail" on the SSX.
    It then takes the output from that command and parses all the values.
    For your convenience you can filter out the data from a single port by passing in
    a "filter_port" value 
    """
    debug = False
    
    
    # Example raw input
    """
    Tue Sep 28 09:45:04 PDT 2010.
    Port  Input                                Output
    ----- -----------------------------------  -----------------------------------
    0/0   Good Packets:                267565  Packets:                     149557
          Octets:                   194788889  Octets:                    24106413
          UcastPkts:                   240846  UcastPkts:                   149543
          McastPkts:                    26635  McastPkts:                        0
          BcastPkts:                       84  BcastPkts:                       14
          ErrorPkts:                        0  ErrorPkts:                        0
          OctetsGood:               194788889  OctetsGood:                24106413
          OctetsBad:                        0  OctetsBad:                        0
          PktRate(pps, 0-sec avg):          0  PktRate(pps, 0-sec avg):          0
          DataRate(bps, 0-sec avg):         0  DataRate(bps, 0-sec avg):         0
          BandWidthUtil(%, 0-sec avg):      0  BandWidthUtil(%, 0-sec avg):      0
          CRCErrors:                        0  PktsCRCErrs:                      0
          DataErrors:                       0  TotalColls:                       0
          AlignErrs:                        0  SingleColls:                      0
          LongPktErrs:                      0  MultipleColls:                    0
          JabberErrs:                       0  LateCollisions:                   0
          SymbolErrs:                       0  ExcessiveColls:                   0
          PauseFrames:                      0  PauseFrames:                      0
          UnknownMACCtrl:                   0  FlowCtrlColls:                    0
          VeryLongPkts:                     0  ExcessLenPkts:                    0
          RuntErrPkts:                      0  UnderrunPkts:                     0
          ShortPkts:                        0  ExcessDefers:                     0
          CarrierExtend:                    0
          SequenceErrs:                     0
          SymbolErrPkts:                    0
          NoResourceDrop:                   0

    1/0   Good Packets:                 53279  Packets:                       6028
          Octets:                    37718652  Octets:                      955547
          UcastPkts:                    26555  UcastPkts:                     6020
          McastPkts:                    26634  McastPkts:                        0
          BcastPkts:                       90  BcastPkts:                        8
          ErrorPkts:                        0  ErrorPkts:                        0
          OctetsGood:                37718652  OctetsGood:                  955547
          OctetsBad:                        0  OctetsBad:                        0
          PktRate(pps, 0-sec avg):          0  PktRate(pps, 0-sec avg):          0
          DataRate(bps, 0-sec avg):         0  DataRate(bps, 0-sec avg):         0
          BandWidthUtil(%, 0-sec avg):      0  BandWidthUtil(%, 0-sec avg):      0
          CRCErrors:                        0  PktsCRCErrs:                      0
          DataErrors:                       0  TotalColls:                       0
          AlignErrs:                        0  SingleColls:                      0
          LongPktErrs:                      0  MultipleColls:                    0
          JabberErrs:                       0  LateCollisions:                   0
          SymbolErrs:                       0  ExcessiveColls:                   0
          PauseFrames:                      0  PauseFrames:                      0
          UnknownMACCtrl:                   0  FlowCtrlColls:                    0
          VeryLongPkts:                     0  ExcessLenPkts:                    0
          RuntErrPkts:                      0  UnderrunPkts:                     0
          ShortPkts:                        0  ExcessDefers:                     0
          CarrierExtend:                    0
          SequenceErrs:                     0
          SymbolErrPkts:                    0
          NoResourceDrop:                   0
    """
    
    
    command = "show port counters detail"
    
    if debug:
        print 'The command to the SSX will be:', command
        print 'Calling function cli_cmd() to execute command'
        
    raw_card_response = cli_cmd(self, command)
    
    """
    if debug:
        print 'returned from cli_cmd()'
        print 'here is the raw returned value'
        print raw_card_response
        print '******************* *************** ************** ****************'
    """
    
    input_dict = {}
    output_dict = {}
    return_dict = {}
    port_name = ''

    # We start by reading only line 4 and beyond. We don't want the following lines:
    """
    Tue Sep 28 09:45:04 PDT 2010.
    Port  Input                                Output
    ----- -----------------------------------  -----------------------------------    
    """
    if debug:
        print 'the raw_card_response contains:', len(raw_card_response), 'lines'
    
    for line in raw_card_response[3:]:
        
        if debug:
            print 'processing line:'
            print '"', line, '"'
            print 'contains:', len(line), 'characters'
            
        if len(line) > 0:
            words = line.split()
            if debug:
                print 'words:'
                print words
            # At this point it splits the names and leaves the ':' on the end
            # This makes for messy processing!
            # We need to 
            # 1. identify all the words till the ':'
            # 2. Join them back into a single "word"
            new_line = []
            if words[0] in valid_port_list:
                port_name = words[0]
                # We then remove it from the list
                words.remove(port_name)
                if debug:
                    print 'Found the port name:', port_name
                
            input_dict_key = ''
            input_value = ''
            found_input_key = False
            found_input_value = False
            output_dict_key = ''
            output_value = ''
            found_output_key = False
            found_output_value = False
            
            if debug:
                print 'the line now countains:', len(words), 'words to parse'
                print words
            
            for element in words:
                if debug:
                    print 'working on word:', element
            
                if found_input_key == False:
                    if debug:
                        print 'looking for the input_key value'
                    if element[-1] == ':':
                        input_dict_key = input_dict_key + ' ' + element.strip(':')
                        found_input_key = True
                        if debug:
                            print 'found input key:', input_dict_key
                    else:
                        input_dict_key = input_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', input_dict_key
                elif (found_input_key == True) and (found_input_value == False):
                    if debug:
                        print 'looking for the input value'
                    input_value = element
                    found_input_value = True
                    if debug:
                        print 'found the input value:', input_value
                elif (found_input_value == True) and (found_output_key == False):
                    if debug:
                        print 'looking fo the output_key'
                    if element[-1] == ':':
                        output_dict_key = output_dict_key + ' ' + element.strip(':')
                        found_output_key = True
                        if debug:
                            print 'found the output key:', output_dict_key
                    else:
                        output_dict_key = output_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', output_dict_key
                else:
                    # The last thing left must be the output value
                    output_value = element
                    found_output_value = True
                    if debug:
                        print 'found the output value:', output_value

            if (found_output_value == False) and (len(words) > 2):
                print 'Unable to determine the output value for', output_dict_key
                print 'please examine the following line:'
                print line
                print 'It was broken into the following words:'
                print words
                print 'Those were recognized as:'
                print 'Input', input_dict_key, ':', input_value 
                print 'Output', output_dict_key, ': Unable to recoginze value!'
                sys.exit(1)
            
                        
                
            
            input_dict[input_dict_key.lstrip()] = input_value 
            if len(output_value) > 0:
                output_dict[output_dict_key.lstrip()] = output_value 
                
            if debug:
                print '========= Parsed Data ==========='
                print 'input_dict:'
                print input_dict 
                print 'output_dict'
                print output_dict 
                print '========= Parsed Data ==========='
                
                
        else:
            if debug:
                print 'this should be a section end'
            # When we reach the end of a section we stick our local dictionary with all the values
            # for a port into the return dictionary indexed on port name/number.
            dict_key = port_name + ' Input'
            return_dict[dict_key] = input_dict
            # We now need to clear the dictionary so we can get the next values
            input_dict = {}
            dict_key = port_name + ' Output'
            return_dict[dict_key] = output_dict
            output_dict = {}
            if debug:
                print 'section end found'
                
    if debug:
        print 'Done processing the command!'
        print 'This is what we got back'
        print return_dict
    
    
    return return_dict
                

    
def show_system_mtu(self):
    """
    This function runs the command "show system" on the SSX and searches for the MTU values
    
    It will then return a dictionar that looks like this:
    {'Next Boot': '1500', 'Current Boot': '1500'}
    """
    debug = False
    ret_dict = {}                    
    
    if debug:
        print 'about to run the command "show system | grep MTU"'
                        
    show_system_raw = self.cmd('show system | grep MTU')
    if debug:
        print 'the output of the command was:'
        print show_system_raw

    show_system_lines = show_system_raw.splitlines()
    if debug:
        print 'counted', len(show_system_lines), 'lines to parse.'
    current_boot = show_system_lines[1].split()
    ret_dict['Current Boot'] = current_boot[1]
    next_boot = show_system_lines[2].split()
    ret_dict['Next Boot'] = next_boot[1]
    
    if debug:
        print 'about to return:'
        print ret_dict
        
    return ret_dict
    
    
def show_port_detail(self, port_filter='none'):
    """
    This function runs the command "show port detail" on the SSX and returns a netsted 
    dictionary containing all the information available. 
    """
    
    # Currenlty the port_filter is not implemented
    
    debug = False

    # Example raw data
    """
    australia[r2]#show port detail 
    Tue Oct 26 13:35:08 PDT 2010.
    0/0   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:0a:d0
          Connector                           Autonegotiation:  Enabled          
                Type:       RJ45              Speed:            100              
                Vendor:     Marvell           Duplex:           Full             
                Model  No:  88E1111           MTU               1500             
                Serial No:  N/A                                                  
                Transcvr:   Unknown                                              

    1/0   Admin State:      Configured        Media Type:       Eth              
          Link State:       Down              MAC Address:      00:12:73:00:0a:d1
          Connector                           Autonegotiation:  Enabled          
                Type:       RJ45              Speed:            100              
                Vendor:     Marvell           Duplex:           Full             
                Model  No:  88E1111           MTU               1500             
                Serial No:  N/A                                                  
                Transcvr:   Unknown                                              

    2/0   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:15:80
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN08474W5T                                           
                Transcvr:   1000BASE-T                                           

    2/1   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:15:81
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN07381VZ2                                           
                Transcvr:   1000BASE-T                                           

    2/2   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:15:82
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  au220052201136                                       
                Transcvr:   1000BASE-T                                           
     
    2/3   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:15:83
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN07250ZPR                                           
                Transcvr:   1000BASE-T                                           

    3/0   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:07:40
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  AU220062414400                                       
                Transcvr:   1000BASE-T                                           

    3/1   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:07:41
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN07331GAR                                           
                Transcvr:   1000BASE-T                                           

    3/2   Admin State:      Unconfigured      Media Type:       Eth              
          Link State:       Down              MAC Address:      00:12:73:00:07:42
          Connector                           Autonegotiation:  Disabled         
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN0852519F                                           
                Transcvr:   1000BASE-T                                           

    3/3   Admin State:      Unconfigured      Media Type:       Eth              
          Link State:       Down              MAC Address:      00:12:73:00:07:43
          Connector                           Autonegotiation:  Disabled         
                Type:       SFP               Speed:            1000             
                Vendor:     AVAGO             Duplex:           Full             
                Model  No:  ABCU-5710RZ       MTU               1500             
                Serial No:  AN07250ZKZ                                           
                Transcvr:   1000BASE-T                                           

    4/0   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:09:48
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  AU210052303996                                       
                Transcvr:   1000BASE-T                                           

    4/1   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:09:49
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  AU220053201722                                       
                Transcvr:   1000BASE-T                                           

    4/2   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:09:4a
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  AU210052304186                                       
                Transcvr:   1000BASE-T                                           

    4/3   Admin State:      Up                Media Type:       Eth              
          Link State:       Up                MAC Address:      00:12:73:00:09:4b
          Connector                           Autonegotiation:  Enabled          
                Type:       SFP               Speed:            1000             
                Vendor:     FIBERXON INC.     Duplex:           Full             
                Model  No:  FTM-C012R-LM      MTU               1500             
                Serial No:  AU220053201743                                       
                Transcvr:   1000BASE-T   
    """
    ## Note:
    #
    # This data is very similar to other data but the "Connector" data is wrapped so
    # that messes things up a bit. We need to be sure to do the following:
    # 1. Look for the keyword "Connector" and then skip it
    # 2. For all the connector data we should append the word "Connector" on 
    # to the values. Such as "Type" becomes "Connector Type"
    #
    # The MAC has a bunch of Collons in it ":" and that could get "split" out
    # We should fix that somehow.  
    
    
    if debug:
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print 'now in issu.py show_port_details'
        print 'about to run the command "show port detail"'
                        
    show_port_detail_raw = self.cmd('show port detail')
    
    
    
    if debug:
        print 'the output of the command was:'
        print show_port_detail_raw
    
    ret_dict = {}
    # These dictionaries should not be needed. 
    #left_dict = {}
    #right_dict = {}
    local_dict = {}
    port_name = ''

    valid_connector_values = ['Type','Vendor','Model  No','Serial No','Transcvr']
    
    show_port_detail_lines = show_port_detail_raw.splitlines()
    
    for line in show_port_detail_lines[2:]:
        
        if debug:
            print 'processing line:'
            print '"', line, '"'
            print 'contains:', len(line), 'characters'
            
        if len(line) > 0:
        
            #=================================================
            # The values are key:value key:value on the line
            # This means there are two columns of data
            # We look for the left one first
            # then we look for the right one. 
            
            left_dict_key = ''
            left_value = ''
            found_left_key = False
            found_left_value = False
            right_dict_key = ''
            right_value = ''
            found_right_key = False
            found_right_value = False
            found_connector = False
        
        
        
            words = line.split()
            
            if debug:
                print 'words:'
                print words
                
            # At this point it splits the names and leaves the ':' on the end
            # This makes for messy processing!
            # We need to 
            # 1. identify all the words till the ':'
            # 2. Join them back into a single "word"
            
            new_line = []
            
            if words[0] in valid_port_list:
                port_name = words[0]
                # We then remove it from the list
                words.remove(port_name)
                if debug:
                    print 'Found the port name:', port_name
                    
                    
            elif words[0] == 'Connector':
                if debug:
                    print 'Found the Connector'
                    
                found_connector = True
                
                if debug:
                    print 'Removing it from the line'
                    
                words.remove('Connector')
            
            
            if debug:
                print 'the line now countains:', len(words), 'words to parse'
                print words
            
            for element in words:
                if debug:
                    print 'working on word:', element
                
                
                if found_left_key == False:
                    if debug:
                        print 'looking for the left_key value'
                    if element[-1] == ':':
                        left_dict_key = left_dict_key + ' ' + element.strip(':')
                        found_left_key = True
                        if debug:
                            print 'found left key:', left_dict_key
                    else:
                        left_dict_key = left_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', left_dict_key
                elif (found_left_key == True) and (found_left_value == False):
                    if debug:
                        print 'looking for the left value'
                    left_value = element
                    found_left_value = True
                    if debug:
                        print 'found the left value:', left_value
                elif (found_left_value == True) and (found_right_key == False):
                    if debug:
                        print 'looking fo the right_key'
                    if element[-1] == ':':
                        if element == 'Duplex:':
                            left_value = left_value + right_dict_key
                            if debug:
                                print 'Found a piece of the last value:', right_dict_key
                            right_dict_key = element.strip(':')
                            found_right_key = True
                            if debug:
                                print 'found the right key:', right_dict_key
                        else:
                            right_dict_key = right_dict_key + ' ' + element.strip(':')
                            found_right_key = True
                            if debug:
                                print 'found the right key:', right_dict_key
                    elif element == 'MTU':
                        right_dict_key = element
                        found_right_key = True
                        if debug:
                            print 'found the right key:', right_dict_key
                    else:
                        right_dict_key = right_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', right_dict_key
                else:
                    # The last thing left must be the right value
                    right_value = element
                    found_right_value = True
                    if debug:
                        print 'found the right value:', right_value
            """
            if (found_right_value == False) and (len(words) > 2):
                print 'Unable to determine the right value for', right_dict_key
                print 'please examine the following line:'
                print line
                print 'It was broken into the following words:'
                print words
                print 'Those were recognized as:'
                print 'left', left_dict_key, ':', left_value 
                print 'right', right_dict_key, ': Unable to recoginze value!'
                sys.exit(1)
            """
            
                        
                
            
            #left_dict[left_dict_key.lstrip()] = left_value
            local_dict[left_dict_key.lstrip()] = left_value 
            if len(right_value) > 0:
                #right_dict[right_dict_key.lstrip()] = right_value
                local_dict[right_dict_key.lstrip()] = right_value 
                
            if debug:
                print '========= Parsed Data ==========='
                print 'output for port:', port_name
                print 'local_dict:'
                print local_dict 
                print '========= Parsed Data ==========='
                
                
        else:
            if debug:
                print 'this should be a section end for port:', port_name
                
            # When we reach the end of a section we stick our local dictionary with all the values
            # for a port into the return dictionary indexed on port name/number.
            dict_key = port_name
            ret_dict[port_name] = local_dict
            # We now need to clear the dictionary so we can get the next values
            local_dict = {}
            if debug:
                print 'section end found'
                
    # There is still the last port information in the buffer. Need to save it too
    dict_key = port_name
    ret_dict[port_name] = local_dict
    if debug:
        print 'Last port found:', port_name
        print 'end of processing data'
        
    if debug:
        print 'completed show_port_details method'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
    return ret_dict
    
    
def show_ip_interface_detail(self, context='local'):
    """
    This function runs the command "show ip interface detail" on the SSX and returns a netsted 
    dictionary containing all the information available. 
    """
    
    # Sample raw_data
    """
    Name: tunnel_loopbk                    IP address: 10.19.0.1/32
    State: Up                              mtu:  
    Arp: Off                               Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Loopback                         Index: 0x25
    Bind/session count: 0                  Session default: No
    Bound to: None    

    Name: tun_ssx1                         IP address: 172.1.1.2/32
    State: Up                              mtu: 1500
    Arp: Off                               Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Tunnel                           Index: 0x26
    Bind/session count: 1                  Session default: No
    Bound to: lan2lan/ip4/2    

    Name: 4-0                              IP address: 10.11.40.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x27
    Bind/session count: 1                  Session default: No
    Bound to: cct 4/0/1    

    Name: 4-1                              IP address: 10.11.41.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x28
    Bind/session count: 1                  Session default: No
    Bound to: cct 4/1/1    

    Name: 4-2                              IP address: 10.11.42.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x29
    Bind/session count: 1                  Session default: No
    Bound to: cct 4/2/1    

    Name: 4-3                              IP address: 10.11.43.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x2a
    Bind/session count: 1                  Session default: No
    Bound to: cct 4/3/1    

    Name: 2-0                              IP address: 10.11.20.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x2c
    Bind/session count: 1                  Session default: No
    Bound to: cct 2/0/1    

    Name: 2-1                              IP address: 10.11.21.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x2d
    Bind/session count: 1                  Session default: No
    Bound to: cct 2/1/1    

    Name: 2-2                              IP address: 10.11.22.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x2e
    Bind/session count: 1                  Session default: No
    Bound to: cct 2/2/1    

    Name: 2-3                              IP address: 10.11.23.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x2f
    Bind/session count: 1                  Session default: No
    Bound to: cct 2/3/1    

    Name: 3-0                              IP address: 10.11.30.1/24
    State: Up                              mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x30
    Bind/session count: 1                  Session default: No
    Bound to: cct 3/0/1    

    Name: 3-1                              IP address: 10.11.31.1/24
    State: Up                              mtu: 1400
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x31
    Bind/session count: 1                  Session default: No
    Bound to: cct 3/1/1    

    Name: 3-2                              IP address: 10.11.32.1/24
    State: Down                            mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x32
    Bind/session count: 0                  Session default: No
    Bound to: None    

    Name: 3-3                              IP address: 10.11.33.1/24
    State: Down                            mtu: 1500
    Arp: On                                Arp timeout: 3600
    Arp refresh: Off                       Ignore DF: Off
    Icmp unreachables: Off                 Mask reply: Off
    Default source: No                     Description: None
    Type: Classic                          Index: 0x33
    Bind/session count: 0                  Session default: No
    Bound to: None    

    """
    debug = False
    
    # The ip interfaces are based on the context you are in
    self.cmd("context %s" % context)
    
    if debug:
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print 'now in issu.py show_ip_interface_detail'
        print 'about to run the command "show ip interface detail"'
                        
    show_ip_interface_detail_raw = self.cmd('show ip interface detail')
    
    ret_dict = {}
    local_dict = {}
    end_of_section = False
    port_name = ''
    
    show_ip_interface_detail_lines = show_ip_interface_detail_raw.splitlines()

    for line in show_ip_interface_detail_lines[1:]:
        
        if debug:
            print 'processing line:'
            print '"', line, '"'
            print 'contains:', len(line), 'characters'
            
        if len(line) > 0:
        
            #=================================================
            # The values are key:value key:value on the line
            # This means there are two columns of data
            # We look for the left one first
            # then we look for the right one. 
            
            left_dict_key = ''
            left_value = ''
            found_left_key = False
            found_left_value = False
            right_dict_key = ''
            right_value = ''
            found_right_key = False
            found_right_value = False
            found_connector = False
            
        
        
            words = line.split()
            
            if debug:
                print 'words:'
                print words
                
            # At this point it splits the names and leaves the ':' on the end
            # This makes for messy processing!
            # We need to 
            # 1. identify all the words till the ':'
            # 2. Join them back into a single "word"
            
            new_line = []
            

            if debug:
                print 'the line now countains:', len(words), 'words to parse'
                print words
            
            for element in words:
                if debug:
                    print 'working on word:', element
                                 
                                                                                
                if found_left_key == False:
                    if debug:
                        print 'looking for the left_key value'
                    if element[-1] == ':':
                        left_dict_key = left_dict_key + ' ' + element.strip(':')
                        found_left_key = True
                        if debug:
                            print 'found left key:', left_dict_key
                    else:
                        left_dict_key = left_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', left_dict_key
                elif (found_left_key == True) and (found_left_value == False):
                    if debug:
                        print 'looking for the left value'
                    left_value = element
                    found_left_value = True
                    if debug:
                        print 'found the left value:', left_value
                    
                elif found_left_key and found_left_value and (len(port_name) < 1):
                    if (left_dict_key == ' Name'):
                        port_name = left_value
                        if debug:
                            print '!!!! found ip interface name:', port_name
                   
                elif (found_left_value == True) and (found_right_key == False):
                    if debug:
                        print 'looking fo the right_key'
                    if element[-1] == ':':
                        if element == 'Duplex:':
                            left_value = left_value + right_dict_key
                            if debug:
                                print 'Found a piece of the last value:', right_dict_key
                            right_dict_key = element.strip(':')
                            found_right_key = True
                            if debug:
                                print 'found the right key:', right_dict_key
                        else:
                            right_dict_key = right_dict_key + ' ' + element.strip(':')
                            found_right_key = True
                            if debug:
                                print 'found the right key:', right_dict_key
                    else:
                        right_dict_key = right_dict_key + ' ' + element
                        if debug:
                            print 'this was just part of a longer key:', right_dict_key
                else:
                    # The last thing left must be the right value
                    right_value = element
                    found_right_value = True
                    if debug:
                        print 'found the right value:', right_value
            """
            if (found_right_value == False) and (len(words) > 2):
                print 'Unable to determine the right value for', right_dict_key
                print 'please examine the following line:'
                print line
                print 'It was broken into the following words:'
                print words
                print 'Those were recognized as:'
                print 'left', left_dict_key, ':', left_value 
                print 'right', right_dict_key, ': Unable to recoginze value!'
                sys.exit(1)
            """
            
                        
                
            
            #left_dict[left_dict_key.lstrip()] = left_value
            local_dict[left_dict_key.lstrip()] = left_value 
            if len(right_value) > 0:
                #right_dict[right_dict_key.lstrip()] = right_value
                local_dict[right_dict_key.lstrip()] = right_value 
                
            if debug:
                print '========= Parsed Data ==========='
                print 'output for port:', port_name
                print 'local_dict:'
                print local_dict 
                print '========= Parsed Data ==========='
                
                
        else:
            if debug:
                print 'this should be a section end for port:', port_name
                
            # When we reach the end of a section we stick our local dictionary with all the values
            # for a port into the return dictionary indexed on port name/number.
            dict_key = port_name
            ret_dict[port_name] = local_dict
            # We now need to clear the dictionary so we can get the next values
            local_dict = {}
            port_name = ''
            if debug:
                print 'section end found'
                
    # There is still the last port information in the buffer. Need to save it too
    dict_key = port_name
    ret_dict[port_name] = local_dict
    
    if debug:
        print 'Last port found:', port_name
        print 'end of processing data'
        
    # Return the system back to the default context
    self.cmd("context local")        
        
    if debug:
        print 'completed show_port_details method'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
    return ret_dict

def list_contexts(self):
    """This method runs the command "show context all" and parses the output.
    It returns a nested dictionary indexed on the context names
    dict = {'context name':{'index':'1','domains':'null'}}
    to get only the context names use
    dict.keys()
    """
    debug = False
    retrn_dict = {}
    
    if debug:
        print 'Now in issu.py method list_contexts'
        
    command = "show context all"
    
    
    raw_output = self.cmd(command)
    raw_lines = raw_output.splitlines()
    if debug:
        print 'The raw_lines is:', raw_lines
        print '==============================='
    for line in raw_lines[3:]:
        local_dict = {}
        if debug:
            print 'processing line:', line
        words = line.split()
        context_name = words[0]
        local_dict['index'] = words[1]
        local_dict['domains'] = words[2:]
        retrn_dict[context_name] = local_dict
        
        
        
        
    if debug:
        print 'Done with list_contexts returning'
        print 'The retrn_dict contains:'
        print retrn_dict
    
    return retrn_dict
	
def show_logging(self):
    """
    This method executes the command "show logging". That command is hidden from tab completion normally
    The data included in the response is the internal buffers that control when the files are flushed
    to the disk. This method simply retrieves that data and parses it. 
    """
    debug = False
    
    # Example Data
    """
    00                                               Save       Next
    01 Log    Size  First-Ix   Last-Ix    Next-Ix    Start-Ix   Save-Ix    W Not Read
    02 ------ ----- ---------- ---------- ---------- ---------- ---------- - ----------
    03 Local   8192          0       5653       5654                       N          0
    04                       0       5653       5654
    05 Glob-R  8192          0       1858       1859       1806       7950 N          0
    06                       0       1858       1859       1806       7950
    07 Glob-D 32768     304130     336897     336898     336790     361366 Y      24611
    08                    9218       9217       9218       9110        918
    09 Glob-I  2048       1859       3906       3907       3606       5142 Y          0
    10                    1859       1858       1859       1558       1046
    11 File Readers          1
    12 Syslog Readers        0
    """
    
    
    if debug:
        print 'Now in issu.py method show_logging'
    
    
    ret_dict = {}
    
    command = 'show logging'
    raw_output = self.cmd(command)
    if debug:
        print 'The raw values are:'
        print raw_output
        print '-------------------------------------'
    lines = raw_output.splitlines()
    if len(lines) > 0:
        local_dict = {}
        line_number = 3
        if debug:
            print 'The following lines will be processed:'
            print  lines[4:11]
            
        for line in lines[4:12]:
            if debug:
                print 'processing line:'
                print line
            words = line.split()
            if debug:
                print 'Broke the line into these words:'
                print words
                print 'testing to see if we are on an odd or even line'
                print odd_or_even(line_number)
            if (odd_or_even(line_number) == 'Odd'):
                local_dict = {}
                log_name = words[0]
                if debug:
                    print 'Found the log name:', log_name
                local_dict['Size'] = words[1]
                if debug:
                    print 'Found the Size:', words[1]
                local_dict['First-Ix 1'] = words[2]
                if debug:
                    print 'Found the First-Ix 1:', words[2]
                local_dict['Last-Ix 1'] = words[3]
                if debug:
                    print 'Found Last-IX 1:', words[3]
                local_dict['Next-Ix 1'] = words[4]
                if debug:
                    print 'Found Next-Ix 1:', words[4]
                if log_name == 'Local':
                    if debug:
                        print 'Processing local info'
                    local_dict['W'] = words[5]
                    if debug:
                        print 'found W:', words[5]
                    local_dict['Not Read'] = words[6]
                    if debug:
                        print 'found Not Read:', words[6]
                else:
                    if debug:
                        print 'Not processing local info'
                    local_dict['Save Start-Ix 1'] = words[5]
                    if debug:
                        print 'found Save Start-Ix 1:', words[5]
                    local_dict['Next Save-Ix 1'] = words[6]
                    if debug:
                        print 'found Next Save-Ix 1:', words[6]
                    local_dict['W'] = words[7]
                    if debug:
                        print 'found W:', words[7]
                    local_dict['Not Read'] = words[8]
                    if debug:
                        print 'found Not Read:', words[8]
                    
            if (odd_or_even(line_number) == 'Even'):
                local_dict['First-Ix 2'] = words[0]
                if debug:
                    print 'found First-Ix 2:', words[0]
                local_dict['Last-Ix 2'] = words[1]
                if debug:
                    print 'found Last-Ix 2:', words[1]
                local_dict['Next-Ix 2'] = words[2]
                if debug:
                    print 'found Next-Ix 2:', words[2]
                if not(log_name == 'Local'):
                    local_dict['Save Start-Ix 2'] = words[3]
                    if debug:
                        print 'Found Save Start-Ix 2:', words[3]
                    local_dict['Next Save-Ix 2'] = words[4]
                    if debug:
                        print 'found Next Save-Ix 2:', words[4]
            if debug:
                print 'storing loca_dict in ret_dict for log name:', log_name
            ret_dict[log_name] = local_dict
            if debug:
                print 'The processed line looks like:'
                print local_dict
            
            if debug:
                print 'Done with line number:', line_number
            line_number = line_number + 1
            if debug:
                print '-------------------------------------'
                
        file_readers_raw = lines[12].split()
        ret_dict['File Readers'] = file_readers_raw[2]
        syslog_readers_raw = lines[13].split()
        ret_dict['Syslog Readers'] = syslog_readers_raw[2]
        
    else:
        print 'We got no lines back from the command "show logging"!'
        print 'Something is broken!'
        sys.exit(1)
        
    return ret_dict
	
def show_mem(self):
    """
    runs the command "show memory" and parses the output
    """
    
    # Example input
    """
    australia[local]#show memory
    00
    01 Mon Jun 20 16:15:28 PDT 2011.
    02 Slot  Type  Bytes Total     Bytes Used      % Available
    03 ----- ----- --------------- --------------- ------------ 
    04 0 IMC1    2,147,483,648     689,876,992           67
    05 1 IMC1    2,147,483,648     652,500,992           69
    """
    debug = False
    
    ret_dict = {}
    
    if debug:
        print 'now in show_mem part of issu.py'
    
    command = 'show mem'
    raw_mem_list = self.cmd(command)
    mem_list = raw_mem_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        for line in mem_list:
            print line
        
    ## Date/Time
    local_dict = {}
    raw_line = mem_list[1]
    if debug:
        print 'the raw line is:'
        print raw_line
    words = raw_line.split()
    local_dict['day of week'] = words[0]
    local_dict['month'] = words[1]
    local_dict['day'] = words[2]
    raw_time = words[3]
    if debug:
        print 'the raw time is:'
        print raw_time
    time = raw_time.split(':')
    local_dict['hour'] = time[0]
    local_dict['minute'] = time[1]
    local_dict['second'] = time[2]
    local_dict['time zone'] = words[4]
    local_dict['year'] = words[5]
    ret_dict['time stamp'] = local_dict
    
    for raw_line in mem_list[4:]:
        local_dict = {}
        if debug:
            print 'the raw line is:'
            print raw_line 
        words = raw_line.split()
        if debug:
            print 'the split values are:'
            print words 
        slot = 'slot ' + words[0]
        local_dict['type'] = words[1]
        local_dict['bytes total'] = words[2]
        local_dict['bytes used'] = words[3]
        local_dict['percent available'] = words[4]
        if debug:
            print 'the local dictionary contains:'
            for key in local_dict.keys():
                print key, ':' , local_dict[key]            
        # pack the values into the return dictionary
        ret_dict[slot] = local_dict
        
    return ret_dict    
    

def show_syscount(self):
    """
    Executes the command "show syscount" and then returns
    a parsed dictionary
    """
    
    # Example Input 
    """
    0  
    1  Wed Jun 22 07:54:55 PDT 2011.
    2  System Counters:
    3    IMC Switchover:       0
    4    Card Reset:           2
    5    Card Restart:         0
    6    Process Core:         1
    7    Process Exit:         1
    8    Process Restart:      0
    9    CRIT Event:           4
    10   ERR Event:            1
    11   WARN Event:           25
    """
    
    debug = False
    
    if debug:
        print 'now in show_syscount in issu.py'
    
    ret_dict = {}
    
    command = 'show syscount'
    raw_syscount = self.cmd(command)
    syscount_lines = raw_syscount.splitlines()
    if debug:
        print 'the raw values are:'
        line_index = 0
        for line in syscount_lines:
            print repr(line_index).ljust(2), line
            line_index = line_index + 1
        
    
    # we throw away lines 0-2
    for line in syscount_lines[3:]:
        if debug:
            print 'processing the following line:'
            print line
        # Break the line into words
        words = line.split(':')
        counter_name = words[0].lstrip()
        if counter_name == 'IMC Switchover':
            ret_dict['IMC Switchover'] = int(words[1])
            
        elif counter_name == 'Card Reset':
            ret_dict['Card Reset'] = int(words[1])
            
        elif counter_name == 'Card Restart':
            ret_dict['Card Restart'] = int(words[1])
            
        elif counter_name == 'Process Core':
            ret_dict['Process Core'] = int(words[1])
            
        elif counter_name == 'Process Exit':
            ret_dict['Process Exit'] = int(words[1])
            
        elif counter_name == 'Process Restart':
            ret_dict['Process Restart'] = int(words[1])
            
        elif counter_name == 'CRIT Event':
            ret_dict['CRIT Event'] = int(words[1])
            
        elif counter_name == 'ERR Event':
            ret_dict['ERR Event'] = int(words[1])
            
        elif counter_name == 'WARN Event':
            ret_dict['WARN Event'] = int(words[1])
        
        else:
            print 'While processing the "show syscount" command encountered'
            print 'the following value: "' + words[0] + '"'
            print 'the method show_syscount can not process it!'
            sys.exit(1)
            
    return ret_dict
            

def show_version(self, slot='active'):
    """
    runs the command "show version"
    optionally will run the command "show version slot 1"
    it then parses the output and returns a dictionary of values
    """
    
    debug = True

    # the default behavior is to show the "active" cards version
    # optionally you can specify a slot 
    
    # Sample input
    """
    0  
    1  Slot 1 Information (IMC1):
    2  ----------------------------------------------------------------------------
    3  StokeOS Release 4.146X1B1S4 (2011061319).
    4  Built Mon Jun 13 20:41:21 PDT 2011 by builder.
    5  
    6  Stoke uptime is 2 minutes
    7  Card uptime is 2 minutes
    8  
    9  System restart at Wed Jun 22 09:27:18 PDT 2011
    10 Card restart at Wed Jun 22 09:27:18 PDT 2011
    11 Restart by remote reset
    12 
    13 Firmware Version: v91
    14 
    15 Stoke-Boot Version
    16   *Booted Primary: StokeBoot Release 4.2 (2009120817).
    17    Booted Backup:  StokeBoot Release 4.2 (2009120817).
    18 Stoke-Bloader Version
    19   *Booted Primary: Stoke Bootloader Release 4.146X1B1S4 (2011061319).
    20    Booted Backup:  Stoke Bootloader Release 4.6B1S4 (2011061319).
    """

    

    
    if debug:
        print 'now in show_version is issu.py'
    
    ret_dict = {}
    
    valid_slot_list = range(0,5)
    
    if slot == 'active':
        command = 'show version'
    elif int(slot) in valid_slot_list:
        command = 'show version slot ' + str(slot)
    else:
        print 'invalid option for slot:', slot
        print 'must be one of the following:', valid_slot_list
        sys.exit(1)
        
    raw_version_list = self.cmd(command)
    version_list = raw_version_list.splitlines()
    
    if debug:
        print 'the raw input was:'
        line_index = 0
        for line in version_list:
            print repr(line_index).ljust(2), line
            line_index = line_index + 1
    
    
    # Parsing:
    # Slot 1 Information (IMC1):
    line = version_list[1]
    if debug:
        print 'parsing:', line
    words = line.split()
    
    ret_dict['slot'] = words[1]
    raw_card_type = words[3]
    card_type = raw_card_type.strip('():')
    ret_dict['card type'] = card_type
    
    # Parsing:
    # StokeOS Release 4.146X1B1S4 (2011061319).
    line = version_list[3]
    if debug:
        print 'parsing:', line
    words = line.split()
    
    ret_dict['version'] = words[2]
    raw_build_id = words[3]
    build_id = raw_build_id.strip('().')
    ret_dict['build id'] = build_id
    
    # Parsing
    # Built Mon Jun 13 20:41:21 PDT 2011 by builder.
    line = version_list[4]
    if debug:
        print 'parsing:', line
    words = line.split()
    if debug:
        print 'the split line:'
        print words
    
    local_dict = {}
    local_dict['day of week'] = words[1]
    local_dict['month'] = words[2]
    local_dict['day of month'] = words[3]
    raw_time = words[4]
    time = raw_time.split(':')
    local_dict['hour'] = time[0]
    local_dict['minute'] = time[1]
    local_dict['second'] = time[2]
    local_dict['time zone'] = words[5]
    local_dict['year'] = words[6]
    ret_dict['build date time'] = local_dict
    ret_dict['build by'] = words[8]

    if (slot == 'active') or (version_list[6][0:5] == 'Stoke'):
        if debug:
            print 'parsing output for Active card'


        # Parsing
        # Stoke uptime is 2 minutes
        line = version_list[6]
        words = line.split() 
        
        local_dict = {}
        
        if len(words) == 5:
            local_dict['hour'] = 0
            local_dict['minute'] = int(words[3])
        else:
            local_dict['hour'] = int(words[3])
            local_dict['minute'] = int(words[5])
                    
        ret_dict['system uptime'] = local_dict
        
        # Parsing
        # Card uptime is 2 minutes
        line = version_list[7]
        if debug:
            print 'parsing:', line
        words = line.split() 
        if debug:
            print 'the split line contains:'
            print words 

        local_dict = {}
        
        if len(words) == 5:
            local_dict['hour'] = 0
            local_dict['minute'] = int(words[3])
        else:
            local_dict['hour'] = int(words[3])
            local_dict['minute'] = int(words[5])
        
        ret_dict['card uptime'] = local_dict

        # Parsing
        # System restart at Wed Jun 22 09:27:18 PDT 2011
        line = version_list[9]
        if debug:
            print 'parsing:', line
        words = line.split() 
        
        local_dict = {}
        local_dict['day of week'] = words[3]
        local_dict['month'] = words[4]
        local_dict['day of month'] = words[5]
        raw_time = words[6]
        time = raw_time.split(':')
        local_dict['hour'] = time[0]
        local_dict['minute'] = time[1]
        local_dict['second'] = time[2]
        local_dict['time zone'] = words[7]
        local_dict['year'] = words[8]
        ret_dict['system restart date time'] = local_dict


        # Parsing
        # Card restart at Wed Jun 22 09:27:18 PDT 2011
        line = version_list[10]
        if debug:
            print 'parsing:', line
        words = line.split() 
        
        local_dict = {}
        local_dict['day of week'] = words[3]
        local_dict['month'] = words[4]
        local_dict['day of month'] = words[5]
        raw_time = words[6]
        time = raw_time.split(':')
        local_dict['hour'] = time[0]
        local_dict['minute'] = time[1]
        local_dict['second'] = time[2]
        local_dict['time zone'] = words[7]
        local_dict['year'] = words[8]
        ret_dict['card restart date time'] = local_dict
        
        # Parsing
        # Restart by remote reset

        ret_dict['restart by'] = version_list[11:]
        
        # Parsing
        # Firmware Version: v91
        line = version_list[13]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        ret_dict['firmware version'] = words[2]


        # Parsing
        #   *Booted Primary: StokeBoot Release 4.2 (2009120817).
        line = version_list[16]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  StokeBoot Release 4.2 (2009120817).
        line = version_list[17]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke boot version'] = local_dict
        

        # Parsing
        #   *Booted Primary: Stoke Bootloader Release 4.146X1B1S4 (2011061319).
        line = version_list[21]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  Stoke Bootloader Release 4.6B1S4 (2011061319).
        line = version_list[22]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke os version'] = local_dict
    
    elif slot in ['0','1']:
        if debug:
            print 'parsing output for selected card'
            print 'card is either in slot-0 or slot-1'
           
        # sample input
        """
        0  
        1  Slot 1 Information (IMC1):
        2  ----------------------------------------------------------------------------
        3  StokeOS Release 4.6B1S2 (2010062215).
        4  Built Tue Jun 22 16:44:08 PDT 2010 by builder.
        5  
        6  Card uptime is 1 week, 5 days, 8 hours, 38 minutes
        7  
        8  Card restart at Thu Jun 23 02:18:41 PDT 2011
        9  Restart by remote reset
        10 
        11 Firmware Version: v91
        12 
        13 Stoke-Boot Version
        14   *Booted Primary: StokeBoot Release 4.2 (2009120817).
        15    Booted Backup:  StokeBoot Release 4.2 (2009120817).
        16 Stoke-Bloader Version
        17   *Booted Primary: Stoke Bootloader Release 4.6B1S2 (2010062215).
        18    Booted Backup:  Stoke Bootloader Release 4.146X1B1S4 (2011061319).
        19    Update Backup:  Stoke Bootloader Release 4.6B1S2 (2010062215).
        """
        
        # Parsing
        # Card uptime is 2 minutes
        line = version_list[6]
        if debug:
            print 'parsing:', line
        words = line.split() 
        if debug:
            print 'the split line contains:'
            print words 

        local_dict = {}
        
        if len(words) == 5:
            local_dict['hour'] = 0
            local_dict['minute'] = int(words[3])
        else:
            local_dict['hour'] = int(words[3])
            local_dict['minute'] = int(words[5])
        
        ret_dict['card uptime'] = local_dict

        # Parsing
        # Card restart at Thu Jun 23 02:33:34 PDT 2011
        line = version_list[8]
        if debug:
            print 'parsing:', line
        words = line.split() 
        
        local_dict = {}
        local_dict['day of week'] = words[3]
        local_dict['month'] = words[4]
        local_dict['day of month'] = words[5]
        raw_time = words[6]
        time = raw_time.split(':')
        local_dict['hour'] = time[0]
        local_dict['minute'] = time[1]
        local_dict['second'] = time[2]
        local_dict['time zone'] = words[7]
        local_dict['year'] = words[8]
        ret_dict['card restart date time'] = local_dict

        
        # Parsing
        # Restart by remote reset

        ret_dict['restart by'] = version_list[8:]
        
        # Parsing
        # Firmware Version: v91
        line = version_list[11]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        ret_dict['firmware version'] = words[2]


        # Parsing
        #   *Booted Primary: StokeBoot Release 4.2 (2009120817).
        line = version_list[14]
        if debug:
            print '16 *Booted Primary: StokeBoot Release 4.2 (2009120817).'
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  StokeBoot Release 4.2 (2009120817).
        line = version_list[15]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke boot version'] = local_dict
        

        # Parsing
        #   *Booted Primary: Stoke Bootloader Release 4.146X1B1S4 (2011061319).
        line = version_list[17]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  Stoke Bootloader Release 4.6B1S4 (2011061319).
        line = version_list[18]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke os version'] = local_dict

    else:
        if debug:
            print 'parsing output for selected card'
            print 'card is either in slot-2, slot-3 or slot-4'
           
        # sample input
        """
        0  
        1  Slot 2 Information (GLC2):
        2  ----------------------------------------------------------------------------
        3  StokeOS Release 4.6B1S2 (2010062215).
        4  Built Tue Jun 22 16:44:08 PDT 2010 by builder.
        5  
        6  Card uptime is 12 hours, 25 minutes
        7  
        8  Card restart at Thu Jun 23 02:33:34 PDT 2011
        9  Restart by remote reset
        10 
        11 Firmware Version: v91
        12 
        13 Stoke MicroEngine Image Release 4.0 (2010062216 builder).
        14 
        15 Stoke-Boot Version
        16   *Booted Primary: StokeBoot Release 4.2 (2009120817).
        17    Booted Backup:  StokeBoot Release 4.2 (2009120817).
        18 Stoke-Bloader Version
        19   *Booted Primary: Stoke Bootloader Release 4.6B1S2 (2010062215).
        20    Booted Backup:  Stoke Bootloader Release 4.6B1S2 (2010062215).

        """
        
        # Parsing
        # Card uptime is 2 minutes
        line = version_list[6]
        if debug:
            print 'parsing:', line
        words = line.split() 
        if debug:
            print 'the split line contains:'
            print words 

        local_dict = {}
        
        if len(words) == 5:
            local_dict['hour'] = 0
            local_dict['minute'] = int(words[3])
        else:
            local_dict['hour'] = int(words[3])
            local_dict['minute'] = int(words[5])
        
        ret_dict['card uptime'] = local_dict

        # Parsing
        # Card restart at Thu Jun 23 02:33:34 PDT 2011
        line = version_list[8]
        if debug:
            print 'parsing:', line
        words = line.split() 
        
        local_dict = {}
        local_dict['day of week'] = words[3]
        local_dict['month'] = words[4]
        local_dict['day of month'] = words[5]
        raw_time = words[6]
        time = raw_time.split(':')
        local_dict['hour'] = time[0]
        local_dict['minute'] = time[1]
        local_dict['second'] = time[2]
        local_dict['time zone'] = words[7]
        local_dict['year'] = words[8]
        ret_dict['card restart date time'] = local_dict

        
        # Parsing
        # Restart by remote reset

        ret_dict['restart by'] = version_list[8:]
        
        # Parsing
        # Firmware Version: v91
        line = version_list[11]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        ret_dict['firmware version'] = words[2]


        # Parsing
        #   *Booted Primary: StokeBoot Release 4.2 (2009120817).
        line = version_list[16]
        if debug:
            print '16 *Booted Primary: StokeBoot Release 4.2 (2009120817).'
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  StokeBoot Release 4.2 (2009120817).
        line = version_list[17]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke boot version'] = local_dict
        

        # Parsing
        #   *Booted Primary: Stoke Bootloader Release 4.146X1B1S4 (2011061319).
        line = version_list[19]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['primary'] = {'version': version, 'build id': build_id}
        
        # Parsing
        #   Booted Backup:  Stoke Bootloader Release 4.6B1S4 (2011061319).
        line = version_list[20]
        if debug:
            print 'parsing:', line
        words = line.split()
        
        local_dict = {}
        
        version = words[4]
        build_id = words[5].strip('().')
        
        local_dict['backup'] = {'version': version, 'build id': build_id}

        ret_dict['stoke os version'] = local_dict


    
        
    return ret_dict
        
        
def show_environmental(self):
    """
    Runs the command "shown environmental" and parses the output
    it then returns a nested dictionary
    """

    debug = False
    
    # sample input
    """
    0  
    1  Environmental status as of Wed Jun 22 13:41:53 2011
    2  Data polling interval is 60 second(s)
    3  
    4  Voltage readings:
    5  =================
    6  Slot		 Source				 Level
    7  ----		 ------				 -------
    8  0		 No errors detected
    9  1		 No errors detected
    10 2		 No errors detected
    11 3		 No errors detected
    12 4		 No errors detected
    13 
    14 Temperature readings:
    15 =====================
    16 Slot		 Source				 Level
    17 ----		 ------				 -------
    18 0		 No errors detected
    19 1		 No errors detected
    20 2		 No errors detected
    21 3		 No errors detected
    22 4		 No errors detected
    23 
    24 
    25 Power status:
    26 =============
    27 Slot		 Source				 Level
    28 ----		 ------				 -------
    29 PEMA		 No errors detected
    30 PEMB		 No errors detected
    31 
    32 Fan status:
    33 ===========
    34 Slot		 Source				 Level
    35 ----		 ------				 -------
    36 FANTRAY1	 No errors detected
    37 FANTRAY2	 No errors detected
    38 
    39 Alarm status:
    40 =============
    41 No 	System-Wide Alarm triggered
    42 ALARMM1		 No errors detected
    """
    
    
    if debug:
        print 'now in show_environmental in issu.py'
    
    ret_dict = {}


    command = 'show environmental'
    raw_environmental = self.cmd(command)
    environmental_lines = raw_environmental.splitlines()
    if debug:
        print 'the raw values are:'
        line_index = 0
        for line in environmental_lines:
            print repr(line_index).ljust(2), line
            line_index = line_index + 1
            
            
        


    # Now we parse the sections
    section_header = ['Voltage readings:','Temperature readings:','Power status:','Fan status:','Alarm status:']
    crap_lines = ['=================','Slot		 Source				 Level','----		 ------				 -------', \
    '=====================','=============', '===========']
    local_dict = {}
    line_counter = 0
    section_name = ''
    for line in environmental_lines[3:-4]:
        if debug:
            print 'now processing:'
            print line
        if len(line.strip()) > 1:
            if line in section_header:
                raw_section_name = line.strip(':')
                section_name = raw_section_name.lower()
                if debug:
                    print 'clearing the local dictionary'
                    
                local_dict = {}
                if debug:
                    print 'local dictionary:', local_dict
                    print 'found section header:', section_name
                    
            elif line in crap_lines:
                if debug:
                    print 'discarding this stuff:'
                    print line
                    
                pass
            else:
                words = line.split('\t')
                if debug:
                    print 'the split line looks like:'
                    print words
                try:
                    slot = int(words[0])
                except:
                    slot = words[0]
                if len(words[1]) == 0:
                    words.remove('')
                slot_name = 'slot ' + str(slot)
                local_dict[slot_name] = {}
                source = words[1].lstrip()
                local_dict[slot_name]['source'] = source
                if len(words) > 2:
                    level = words[2]
                    local_dict[slot_name]['level'] = level 
                if debug:
                    print 'the local dictionary for section:', section_name
                    print local_dict
        else:
            if len(local_dict) > 1:
                ret_dict[section_name] = local_dict
                if debug:
                    print '-------------------------------------------------------------'
                    print 'storing the following local_dict values into the main ret_dict'
                    print 'under section:', section_name
                    local_dict_keys = local_dict.keys()
                    for key in local_dict_keys:
                        print key
                        print '\t', local_dict[key]
                    print 'here is the ret_dict'
                    ret_dict_keys = ret_dict.keys()
                    for key in ret_dict_keys:
                        print key
                        sub_keys = ret_dict[key].keys()
                        for sub_key in sub_keys:
                            print '\t', sub_key
                            print '\t\t', ret_dict[key][sub_key]
                        
                    print '-------------------------------------------------------------'
            


    local_dict = {}
    general_alarm = environmental_lines[-2].strip('\t')
    local_dict['general status'] = general_alarm
    
    raw_alarmm1 = environmental_lines[-1].split('\t')
    if debug:
        print 'the last line contains:'
        print raw_alarmm1
    alarmm1 = raw_alarmm1[2].lstrip(' ')
    local_dict['alarmm1'] = alarmm1
    
    ret_dict['alarm status'] = local_dict

            
    return ret_dict
    
    
def show_file_system(self):
    """
    Runs the command "show file-system" which is a hidden command to display
    the disk utilization. It then parses the output and returns a nested
    dictionary of values. 
    """
    debug = False
    
    if debug:
        print 'now in show_file_system in issu.py'
    
    # Sample Input
    """
    0  
    1  Thu Jun 23 11:53:16 PDT 2011.
    2  Name             Size           % Used Used           Free
    3  ---------------- -------------- ------ -------------- --------------
    4  /hd              40,012,611,584     16  6,551,703,552 33,460,908,032
    5  /hdp             40,013,643,776      2    935,257,088 39,078,386,688
    6  /cfint              128,974,848     11     14,220,800    114,754,048
    7  /cfintp             130,007,040      0         53,248    129,953,792
    """
    
    ret_dict = {}


    command = 'show file-system'
    raw_file_system = self.cmd(command)
    file_system_lines = raw_file_system.splitlines()
    if debug:
        print 'the raw values are:'
        line_index = 0
        for line in file_system_lines:
            print repr(line_index).ljust(2), line
            line_index = line_index + 1
    

    for line in file_system_lines[4:]:
        local_dict = {}
        if debug:
            print 'now processing the following line:'
            print line
        words = line.split()
        if debug:
            print 'the split line contains:'
            print words
        mount_point = words[0].strip('\t/')
        local_dict['size'] = words[1]
        local_dict['percent used'] = words[2]
        local_dict['used'] = words[3]
        local_dict['free'] = words[4]
        if debug:
            print 'for the mount point:', mount_point
            print local_dict
        ret_dict[mount_point] = local_dict
        
        
    return ret_dict
	
def show_versions(self):
    """Retrieves the versions installed on the system and returns a dictionary of them
    """
    debug = False
    installed_packages = []
    ## We need to see if the package is already installed on the system!!
    show_system_raw = self.cmd('show system')

    show_system_lines = show_system_raw.splitlines()

    
    # We will parse the linse last to first searching for two things
    # 1. Other Packages:
    # 2. In-Use Packages:
    # When we find the second item we will stop searching
    searching = True    
    ndex = len(show_system_lines) - 1
    if debug:
        print 'Found', ndex, 'lines'
    while searching:
        current_line = show_system_lines[ndex]
        if debug:
            print 'Parsing this line:', current_line
        word = current_line.split()
        # If the word is in the search list we don't want that line
        if not (word[0] in ('Other','In-Use','reverts')):
            print 'Found the following version installed:', word[0]
            installed_packages.append(word[0])
        if word[0] == 'In-Use':
            print 'Found the last line. All versions read.'
            searching = False
        ndex = ndex - 1
    
                
    if debug:
        print 'Found the following versions installed:'
        for item in installed_packages:
            print item
    
    print 'returning from issu.py show_versions'
    return installed_packages

        
def show_versions_and_build(self):
    """Retrieves the versions installed on the system and returns a dictionary of them
    """
    debug = False
    installed_packages = {}
    ## We need to see if the package is already installed on the system!!
    show_system_raw = self.cmd('show system')

    show_system_lines = show_system_raw.splitlines()

    
    # We will parse the linse last to first searching for two things
    # 1. Other Packages:
    # 2. In-Use Packages:
    # When we find the second item we will stop searching
    searching = True    
    ndex = len(show_system_lines) - 1
    if debug:
        print 'Found', ndex, 'lines'
        print '------------------------'
    while searching:
        current_line = show_system_lines[ndex]
        if debug:
            print 'Parsing this line:', current_line
        word = current_line.split()
        # If the word is in the search list we don't want that line
        if not (word[0] in ('Other','In-Use','reverts', 'ISSU')):
            print 'Found the following version installed:', word[0]
            if debug:
                print 'The version should be:', word[-1]
            version = word[0]
            raw_build_id = word[-1]
            build_id = raw_build_id[1:-3]
            if debug:
                print 'Build ID determined to be:', build_id
            installed_packages[version] = build_id
            if debug:
                print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        if word[0] == 'In-Use':
            print 'Found the last line. All versions read.'
            searching = False
        ndex = ndex - 1
    
                
    if debug:
        print 'Found the following versions installed:'
        for item in installed_packages:
            print item
    
    print 'returning from issu.py show_versions'
    return installed_packages
    
    
def show_port(self):
    """
    Runs the command "show port" and parses the ouptut
    """
    debug = False
    
    # Sample raw imput
    """
    Wed Dec 14 11:15:04 PDT 2011.
    Port  Type Admin  Link   Speed Duplex Connector Medium MAC Address
    ----- ---- ------ ------ ----- ------ --------- ------ -----------------
    0/0   Eth  Config Down    100M Full   RJ45      Copper 00:12:73:00:0a:d0
    1/0   Eth  Up     Up      100M Full   RJ45      Copper 00:12:73:00:0a:d1
    """
    if debug:
        print 'now in issu.py show_port'
        
    port_dict = {}
    
    raw_port = self.cmd("show port")
    if debug:
        print 'the raw returned value was:'
        print raw_port
    port_list = raw_port.splitlines()
    if debug:
        line_index = 0
        print 'the lines are:'
        for line in port_list:
            print line_index, line
            line_index = line_index + 1
    
            
            
    labels_line = port_list[2].split()
    divider_line = port_list[3]
    columnDict = parse_divider_line(self,divider_line)
    if debug:
        print 'The columnDict is:'
        print columnDict

    for raw_line in port_list[4:]:
        line = raw_line
        local_dict = {}
        if debug:
            print '----------------------------------------------'
            print 'The line to be processes is:'
            print line
        start = columnDict[0][0]
        end = columnDict[0][1]+1
        name = line[start:end].strip()
        if debug:
            print 'The name is:', name
        local_dict["Type"] = line[0]
        for labels_idx in range(1,(len(labels_line) - 1)):
            start = columnDict[labels_idx][0]
            end = columnDict[labels_idx][1]+1
            local_dict[labels_line[labels_idx]] = line[start:end].strip()
            if debug:
                print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
            # We store each entry in the main dictionary we return
            port_dict[name] = local_dict
    
    return port_dict

    

###### Anthony Ton code start here #########

		
def show_dos_counters(self, slot):
    """Runs the command 'show dos slot <0..4> counters' and parses the output. 
    """
    dos_dict = {}
    debug = False
    
    # Sample raw input
    """
    kenya[local]#show dos slot 2 counters 
                                                     Total                Drops
    --------------------------------------------------------------------------------
    ARP                           :                    0                    0
    Local TCP                     :                    0                    0
    Local UDP                     :                    0                    0
    Local ICMP                    :                    0                    0
    IP4 MIP Exception             :                    0                    0
    IKE                           :                    0                    0
    Local Adjacency               :                    0                    0
    ARP Transit                   :                    0                    0
    IP4 Unreachable               :                    0                    0
    TTL Expired                   :                    0                    0
    TTL Expired Encap             :                    0                    0
    IP4 Options                   :                    0                    0
    Over MTU                      :                    0                    0
    kenya[local]#

    # Sample dictionary output:
    {
    'ARP': {   'Drops': '0',
               'Total': '0'},
    'ARP Transit': {   'Drops': '0',
                       'Total': '0'},
    'IKE': {   'Drops': '0',
               'Total': '0'},
    'IP4 MIP Exception': {   'Drops': '0',
                             'Total': '0'},
    'IP4 Options': {   'Drops': '0',
                       'Total': '0'},
    'IP4 Unreachable': {   'Drops': '0',
                           'Total': '0'},
    'Local Adjacency': {   'Drops': '0',
                           'Total': '0'},
    'Local ICMP': {   'Drops': '0',
                      'Total': '0'},
    'Local TCP': {   'Drops': '0',
                     'Total': '0'},
    'Local UDP': {   'Drops': '0',
                     'Total': '0'},
    'Over MTU': {   'Drops': '0',
                    'Total': '0'},
    'TTL Expired': {   'Drops': '0',
                       'Total': '0'},
    'TTL Expired Encap': {   'Drops': '0',
                             'Total': '0'}}

    """
    command = "show dos slot " + slot + " counter"
    raw_dos_list = self.cmd(command)
    dos_list = raw_dos_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print dos_list
    
    if 'ERROR:' in raw_dos_list:
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_dos_list
        dos_dict['Status'] = 'Error'
        return dos_dict
            
    for raw_line in dos_list[3:]:
        line = raw_line.split(':')
        local_dict = {}
        if debug:
            print '----------------------------------------------'
            print 'The line to be processes is:'
            print line
        name = line[0].strip()
        if debug:
            print 'The name is:', name
	raw_data = line[1].split(); 
        local_dict['Total'] = raw_data[0]
        if debug:
            print 'The Total is:', local_dict['Total']
        local_dict['Drops'] = raw_data[1]
        if debug:
            print 'The Drops is:', local_dict['Drops']
        # We store each entry in the main dictionary we return
        dos_dict[name] = local_dict
    
    return dos_dict
		
def show_fast_path_counters(self):
    """Runs the command 'show fast-path counters' and parses the output. 
    """
    fastpath_dict = {}
    debug = False
    
    # Sample raw input
    """
    kenya[local]#show fast-path counters  
    Slot Port Type                          Count
    ---- ---- ----------------------------- -----------------
       2    1 InvalidFib                                  748
       3    1 InvalidFib                                2,067
    kenya[local]#
    
    # Sample dictionary output:
    {
    '2/0': {   'Count': '363',
               'Type': 'Reserved4'},
    '2/1': {   'Count': '82',
               'Type': 'Reserved4'}}


    """
    command = "show fast-path counters"
    raw_fastpath_counters_list = self.cmd(command)
    fastpath_counters_list = raw_fastpath_counters_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print fastpath_counters_list

    labels_line = fastpath_counters_list[1].split()
    for raw_line in fastpath_counters_list[3:]:
        line = raw_line.split()
        local_dict = {}
        if debug:
            print '----------------------------------------------'
            print 'The line to be processes is:'
            print line
        name = line[0] + "/" + line[1]
        if debug:
            print 'The name is:', name
	for labels_idx in range(2,len(labels_line)):
            local_dict[labels_line[labels_idx]] = line[labels_idx]
            if debug:
            	print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
        # We store each entry in the main dictionary we return
        fastpath_dict[name] = local_dict
    
    return fastpath_dict
		
def parse_divider_line(self,str,divChar='-'):
    """ Parse the divider line and return a dictionary of length of each column
        in format {column#:[length,start,end],...,column#n:[start,end]}
        Example: "----- ---- ---------- ---" return {0:[0,4],1:[6,9],2:[11,20],3:[22,24]}
    """
    local_dict = {}
    column = 0
    startFound = False
    endFound = False
    for idx in range(0,len(str)):
        if (str[idx] == divChar) and not startFound:
            start = idx
            startFound = True
            endFound = False
        elif (str[idx] == ' ') and startFound:
            end = idx - 1
            startFound = False
            endFound = True
            local_dict[column] = [start,end]
            column += 1
    if startFound and (not endFound):
        # the last column has not been accounted for
        local_dict[column] = [start,len(str)-1]
    return local_dict

	
def show_ip_ospf_route(self):
    """Runs the command 'show ip ospf route [detail]' and parses the output. 
    """
    ipOspfRoute_dict = {}
    debug = False
    
    # Sample raw input
    """
    kenya[stoke]#show ip ospf route 
       Network/Mask       Cost  Cost2 Nexthop         Interface      Area-ID        
       ------------------ ----- ----- --------------- -------------- ---------------
    O  10.254.1.0/24          1       direct          isp            0.0.0.0        
    O  11.11.11.11/32         1       direct          lo0            0.0.0.0        
    kenya[stoke]#
    """

    command = "show ip ospf route "
    raw_ip_ospf_route_list = self.cmd(command)
    ip_ospf_route_list = raw_ip_ospf_route_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print ip_ospf_route_list

    if 'ERROR:' in ip_ospf_route_list[1]:
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_ip_ospf_route_list
        ipOspfRoute_dict['Status'] = 'Error'
        return ipOspfRoute_dict

    labels_line = ip_ospf_route_list[1].split()
    divider_line = ip_ospf_route_list[2]
    columnDict = parse_divider_line(self,divider_line)
    if debug:
        print 'The columnDict is:'
        print columnDict

    for raw_line in ip_ospf_route_list[3:]:
        line = raw_line
        local_dict = {}
        if debug:
            print '----------------------------------------------'
            print 'The line to be processes is:'
            print line
	start = columnDict[0][0]
	end = columnDict[0][1]+1
        name = line[start:end].strip()
        if debug:
            print 'The name is:', name
	local_dict["Type"] = line[0]
	for labels_idx in range(1,len(labels_line)):
	    start = columnDict[labels_idx][0]
	    end = columnDict[labels_idx][1]+1
            local_dict[labels_line[labels_idx]] = line[start:end].strip()
            if debug:
                print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
        # We store each entry in the main dictionary we return
        ipOspfRoute_dict[name] = local_dict
    
    return ipOspfRoute_dict
    
	
def show_module_iked_slot_ma_pp_detail(self,slot):
    """Runs the command 'show module iked slot <slot> ma pp detail' and parses the output. 
    """
    modIkedMaPpDetail_dict = {}
    debug = False
    
    # Sample raw input
    """
    kenya[local]#show module iked slot 2 ma pp detail 
    _global_:
     User Element Size................0  User Init Elements..............0
     User Grow Elements...............0  Max Elements....................0
     Element Size.....................0  Grow Size.......................0
     Initial Elements.................0  Grow Elements...................0
     Elements In Use..................0  Allocations....................41
     Frees............................0  Max Elements In Use.............0
    HALibHAPP::0:
     User Element Size..............384  User Init Elements.............64
     User Grow Elements..............64  Max Elements...................64
     Element Size...................396  Grow Size..................28,672
     Initial Elements................64  Grow Elements..................64
     Elements In Use.................13  Allocations....................13
     Frees............................0  Max Elements In Use............13
    HALibHAGlobCB::0:
     User Element Size..............192  User Init Elements.............16
     User Grow Elements..............16  Max Elements...................16
     Element Size...................204  Grow Size...................4,096
     Initial Elements................16  Grow Elements..................16
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    HALibAsyncCB::0:
     User Element Size...............48  User Init Elements..........1,024
     User Grow Elements...........1,024  Max Elements........4,294,967,295
     Element Size....................60  Grow Size..................65,536
     Initial Elements.............1,024  Grow Elements...............1,024
     Elements In Use..................0  Allocations................31,674
     Frees.......................31,674  Max Elements In Use.............2
    IKE Session Pool:17::0:
     User Element Size............2,120  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements...............91,216
     Element Size.................2,132  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV2 SA Pool:17::0:
     User Element Size............1,120  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements..............273,648
     Element Size.................1,132  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    ph1 pool:17::0:
     User Element Size............1,816  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements...............45,608
     Element Size.................1,828  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    natt opt pool:17::0:
     User Element Size..............132  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements...............45,608
     Element Size...................144  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    ph2 pool:17::0:
     User Element Size..............656  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements...............45,608
     Element Size...................668  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    ph2 app pool:17::0:
     User Element Size..............240  User Init Elements..........4,096
     User Grow Elements...........4,096  Max Elements...............22,804
     Element Size...................252  Grow Size.................520,192
     Initial Elements.............4,096  Grow Elements...............4,096
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    ph2 app pool:17::1:
     User Element Size..............368  User Init Elements..........2,048
     User Grow Elements...........2,048  Max Elements...............22,804
     Element Size...................380  Grow Size.................520,192
     Initial Elements.............2,048  Grow Elements...............2,048
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKE SA Info Pool:17::0:
     User Element Size..............824  User Init Elements.........16,000
     User Grow Elements..........16,000  Max Elements..............547,296
     Element Size...................836  Grow Size.................520,192
     Initial Elements............16,000  Grow Elements..............16,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    OUT SA Block HA Poo:17::0:
     User Element Size..............640  User Init Elements............356
     User Grow Elements.............356  Max Elements................5,696
     Element Size...................652  Grow Size.................233,472
     Initial Elements...............356  Grow Elements.................356
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKE Counter HA Pool:17::0:
     User Element Size..............560  User Init Elements..............4
     User Grow Elements...............4  Max Elements....................4
     Element Size...................572  Grow Size...................3,072
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................1  Allocations.....................1
     Frees............................0  Max Elements In Use.............1
    ISAKMP Statistics H:17::0:
     User Element Size..............428  User Init Elements..............4
     User Grow Elements...............4  Max Elements....................4
     Element Size...................440  Grow Size...................2,048
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................1  Allocations.....................1
     Frees............................0  Max Elements In Use.............1
    Tunmgr ha pool:17::0:
     User Element Size..............192  User Init Elements..........8,000
     User Grow Elements...........8,000  Max Elements..............364,864
     Element Size...................204  Grow Size.................520,192
     Initial Elements.............8,000  Grow Elements...............8,000
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV2 last response:17::0:
     User Element Size..............368  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size...................380  Grow Size...................2,048
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV2 last response:17::1:
     User Element Size..............624  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size...................636  Grow Size...................3,072
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV2 last response:17::2:
     User Element Size............1,136  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size.................1,148  Grow Size...................5,120
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV2 last response:17::3:
     User Element Size............2,160  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size.................2,172  Grow Size..................12,288
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV1 Last Resp HA :17::0:
     User Element Size..............368  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size...................380  Grow Size...................2,048
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV1 Last Resp HA :17::1:
     User Element Size..............624  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size...................636  Grow Size...................3,072
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV1 Last Resp HA :17::2:
     User Element Size............1,136  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size.................1,148  Grow Size...................5,120
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    IKEV1 Last Resp HA :17::3:
     User Element Size............2,160  User Init Elements..............4
     User Grow Elements...............4  Max Elements..............273,648
     Element Size.................2,172  Grow Size..................12,288
     Initial Elements.................4  Grow Elements...................4
     Elements In Use..................0  Allocations.....................0
     Frees............................0  Max Elements In Use.............0
    kenya[local]#

    # Sample dictionary output   
    {
    'HALibAsyncCB::0:': {   'Allocations': '1,446',
                            'Element Size': '60',
                            'Elements In Use': '0',
                            'Frees': '1,446',
                            'Grow Elements': '1,024',
                            'Grow Size': '65,536',
                            'Initial Elements': '1,024',
                            'Max Elements': '4,294,967,295',
                            'Max Elements In Use': '1',
                            'User Element Size': '48',
                            'User Grow Elements': '1,024',
                            'User Init Elements': '1,024'},
    'HALibHAGlobCB::0:': {   'Allocations': '0',
                             'Element Size': '204',
                             'Elements In Use': '0',
                             'Frees': '0',
                             'Grow Elements': '16',
                             'Grow Size': '4,096',
                             'Initial Elements': '16',
                             'Max Elements': '16',
                             'Max Elements In Use': '0',
                             'User Element Size': '192',
                             'User Grow Elements': '16',
                             'User Init Elements': '16'},
    'HALibHAPP::0:': {   'Allocations': '13',
                         'Element Size': '396',
                         'Elements In Use': '13',
                         'Frees': '0',
                         'Grow Elements': '64',
                         'Grow Size': '28,672',
                         'Initial Elements': '64',
                         'Max Elements': '64',
                         'Max Elements In Use': '13',
                         'User Element Size': '384',
                         'User Grow Elements': '64',
                         'User Init Elements': '64'},
    'IKE Counter HA Pool:17::0:': {   'Allocations': '1',
                                      'Element Size': '572',
                                      'Elements In Use': '1',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '3,072',
                                      'Initial Elements': '4',
                                      'Max Elements': '4',
                                      'Max Elements In Use': '1',
                                      'User Element Size': '560',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKE SA Info Pool:17::0:': {   'Allocations': '0',
                                   'Element Size': '836',
                                   'Elements In Use': '0',
                                   'Frees': '0',
                                   'Grow Elements': '16,000',
                                   'Grow Size': '520,192',
                                   'Initial Elements': '16,000',
                                   'Max Elements': '1,447,296',
                                   'Max Elements In Use': '0',
                                   'User Element Size': '824',
                                   'User Grow Elements': '16,000',
                                   'User Init Elements': '16,000'},
    'IKE Session Pool:17::0:': {   'Allocations': '0',
                                   'Element Size': '2,132',
                                   'Elements In Use': '0',
                                   'Frees': '0',
                                   'Grow Elements': '8,000',
                                   'Grow Size': '520,192',
                                   'Initial Elements': '8,000',
                                   'Max Elements': '241,216',
                                   'Max Elements In Use': '0',
                                   'User Element Size': '2,120',
                                   'User Grow Elements': '8,000',
                                   'User Init Elements': '8,000'},
    'IKEV1 Last Resp HA :17::0:': {   'Allocations': '0',
                                      'Element Size': '380',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '2,048',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '368',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV1 Last Resp HA :17::1:': {   'Allocations': '0',
                                      'Element Size': '636',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '3,072',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '624',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV1 Last Resp HA :17::2:': {   'Allocations': '0',
                                      'Element Size': '1,148',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '5,120',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '1,136',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV1 Last Resp HA :17::3:': {   'Allocations': '0',
                                      'Element Size': '2,172',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '12,288',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '2,160',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV2 SA Pool:17::0:': {   'Allocations': '0',
                                'Element Size': '1,132',
                                'Elements In Use': '0',
                                'Frees': '0',
                                'Grow Elements': '8,000',
                                'Grow Size': '520,192',
                                'Initial Elements': '8,000',
                                'Max Elements': '723,648',
                                'Max Elements In Use': '0',
                                'User Element Size': '1,120',
                                'User Grow Elements': '8,000',
                                'User Init Elements': '8,000'},
    'IKEV2 last response:17::0:': {   'Allocations': '0',
                                      'Element Size': '380',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '2,048',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '368',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV2 last response:17::1:': {   'Allocations': '0',
                                      'Element Size': '636',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '3,072',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '624',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV2 last response:17::2:': {   'Allocations': '0',
                                      'Element Size': '1,148',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '5,120',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '1,136',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'IKEV2 last response:17::3:': {   'Allocations': '0',
                                      'Element Size': '2,172',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '12,288',
                                      'Initial Elements': '4',
                                      'Max Elements': '723,648',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '2,160',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'ISAKMP Statistics H:17::0:': {   'Allocations': '1',
                                      'Element Size': '440',
                                      'Elements In Use': '1',
                                      'Frees': '0',
                                      'Grow Elements': '4',
                                      'Grow Size': '2,048',
                                      'Initial Elements': '4',
                                      'Max Elements': '4',
                                      'Max Elements In Use': '1',
                                      'User Element Size': '428',
                                      'User Grow Elements': '4',
                                      'User Init Elements': '4'},
    'OUT SA Block HA Poo:17::0:': {   'Allocations': '0',
                                      'Element Size': '652',
                                      'Elements In Use': '0',
                                      'Frees': '0',
                                      'Grow Elements': '942',
                                      'Grow Size': '520,192',
                                      'Initial Elements': '942',
                                      'Max Elements': '15,072',
                                      'Max Elements In Use': '0',
                                      'User Element Size': '640',
                                      'User Grow Elements': '942',
                                      'User Init Elements': '942'},
    'Tunmgr ha pool:17::0:': {   'Allocations': '0',
                                 'Element Size': '204',
                                 'Elements In Use': '0',
                                 'Frees': '0',
                                 'Grow Elements': '8,000',
                                 'Grow Size': '520,192',
                                 'Initial Elements': '8,000',
                                 'Max Elements': '964,864',
                                 'Max Elements In Use': '0',
                                 'User Element Size': '192',
                                 'User Grow Elements': '8,000',
                                 'User Init Elements': '8,000'},
    '_global_:': {   'Allocations': '41',
                     'Element Size': '0',
                     'Elements In Use': '0',
                     'Frees': '0',
                     'Grow Elements': '0',
                     'Grow Size': '0',
                     'Initial Elements': '0',
                     'Max Elements': '0',
                     'Max Elements In Use': '0',
                     'User Element Size': '0',
                     'User Grow Elements': '0',
                     'User Init Elements': '0'},
    'natt opt pool:17::0:': {   'Allocations': '0',
                                'Element Size': '144',
                                'Elements In Use': '0',
                                'Frees': '0',
                                'Grow Elements': '8,000',
                                'Grow Size': '520,192',
                                'Initial Elements': '8,000',
                                'Max Elements': '120,608',
                                'Max Elements In Use': '0',
                                'User Element Size': '132',
                                'User Grow Elements': '8,000',
                                'User Init Elements': '8,000'},
    'ph1 pool:17::0:': {   'Allocations': '0',
                           'Element Size': '1,828',
                           'Elements In Use': '0',
                           'Frees': '0',
                           'Grow Elements': '8,000',
                           'Grow Size': '520,192',
                           'Initial Elements': '8,000',
                           'Max Elements': '120,608',
                           'Max Elements In Use': '0',
                           'User Element Size': '1,816',
                           'User Grow Elements': '8,000',
                           'User Init Elements': '8,000'},
    'ph2 app pool:17::0:': {   'Allocations': '0',
                               'Element Size': '252',
                               'Elements In Use': '0',
                               'Frees': '0',
                               'Grow Elements': '4,096',
                               'Grow Size': '520,192',
                               'Initial Elements': '4,096',
                               'Max Elements': '60,304',
                               'Max Elements In Use': '0',
                               'User Element Size': '240',
                               'User Grow Elements': '4,096',
                               'User Init Elements': '4,096'},
    'ph2 app pool:17::1:': {   'Allocations': '0',
                               'Element Size': '380',
                               'Elements In Use': '0',
                               'Frees': '0',
                               'Grow Elements': '2,048',
                               'Grow Size': '520,192',
                               'Initial Elements': '2,048',
                               'Max Elements': '60,304',
                               'Max Elements In Use': '0',
                               'User Element Size': '368',
                               'User Grow Elements': '2,048',
                               'User Init Elements': '2,048'},
    'ph2 pool:17::0:': {   'Allocations': '0',
                           'Element Size': '668',
                           'Elements In Use': '0',
                           'Frees': '0',
                           'Grow Elements': '8,000',
                           'Grow Size': '520,192',
                           'Initial Elements': '8,000',
                           'Max Elements': '120,608',
                           'Max Elements In Use': '0',
                           'User Element Size': '656',
                           'User Grow Elements': '8,000',
                           'User Init Elements': '8,000'}}

    """

    command = "show module iked slot " + slot + " ma pp detail"
    raw_modIkedMaPpDetail_list = self.cmd(command)
    modIkedMaPpDetail_list = raw_modIkedMaPpDetail_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print modIkedMaPpDetail_list
    
    if 'ERROR:' in raw_modIkedMaPpDetail_list:
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_modIkedMaPpDetail_list
        modIkedMaPpDetail_dict['Status'] = 'Error'
        return modIkedMaPpDetail_dict

    name = None
    local_dict = {}
    for raw_line in modIkedMaPpDetail_list[1:]:
        line = raw_line.strip()
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	# if the last character is :, then it is the name
	if debug:
	    print("Last char is %s" %line[len(line)-1])
   	if line[len(line)-1] == ":":
	    if name != None:
		# Done with previous name, save it to main dictionary
		modIkedMaPpDetail_dict[name] = local_dict
        	local_dict = {}
            name = line
            if debug:
                print 'The name is:', name
	else:
	    p = re.compile('(?P<name1>[A-Za-z ]*)\.+(?P<value1>[\d,]+)\s+(?P<name2>[A-Za-z ]*)\.+(?P<value2>[\d,]+)')
	    m = p.search(line)
	    if m:
	    	dict = m.groupdict()
                if debug:
                    print("The dict is: %s " %dict)
		local_dict[dict['name1']] = dict['value1']
		local_dict[dict['name2']] = dict['value2']
		if debug:
                    print("The %s is: %s " %(dict['name1'],local_dict[dict['name1']]))
                    print("The %s is: %s " %(dict['name2'],local_dict[dict['name2']]))
    # We store last entry in the main dictionary we return
    modIkedMaPpDetail_dict[name] = local_dict
    
    return modIkedMaPpDetail_dict
    
def show_module_iked_slot_ma_pool(self,slot):
    """Runs the command 'show module iked slot <slot> ma pool' and parses the output. 
    """
    modIkedMaPool_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show module iked slot 2 ma pools
    Name             Size          InUse     Free      Allocs        Frees
    ---------------- ------------- --------- --------- ------------- -------------
    DaSet                      128        64         6            64             0
    DaJudy                      40        49     2,075        22,442        22,393
    DaJudy                      72         2     2,093            27            25
    DaJudy                     136        10       514            19             9
    CrhHandleData               60         5        35             5             0
    CrhRegData                  32         1        42             1             0
    CrhCmdBlk                8,224         5         3             5             0
    NvTimer                     56         5     7,643         8,233         8,228
    IpcConnIds                  28        12        36            12             0
    IpcArepIds                  28         6        42             7             1
    IpcReg                     156         9        26             9             0
    IpcConn                    400        10        29            12             2
    IpcRegmsg                    8         9        19             9             0
    IpcAsyncReply              344         6        10             7             1
    IpcSndrArep                 36         3        15             3             0
    IpcThrEnt                   36         0        18            10            10
    IpcThrData                  28         0        22            86            86
    IpcRmReg                    24         9        44             9             0
    IpcRmInfo                   36         1       145            25            24
    IpcAmInfo                   72         2       142         6,814         6,812
    MsgVerPool                 176         5        16             5             0
    IpcTrWantReg                28         8        40             8             0
    IpcTrRegac                  76        14        19            15             1
    IpcTrRegpc                  72        14        21            15             1
    IpcTrReg                    84         9        32             9             0
    IpcTrConn                  388        10        30            12             2
    IpcTrConnG                 188        10        25            12             2
    IpcTrSlot                   64        10        28            12             2
    IpcTrNode                  112        10        22            12             2
    IpcTrRegacI                 28        14        34            15             1
    IpcTrRegpcI                 28        14        34            15             1
    IpcTrCgIds                  28        12        36            12             0
    IpcPeer                     48        14        18            14             0
    IpcPeerMsgData              80         0        20            81            81
    IpcPeerMsg                  56         0        28            72            72
    IpcQnxReg                   80         9        23             9             0
    IpcQnxConn                  12         4        56             6             2
    IpcTcpReg                   52         9        37             9             0
    IpcTcpConn                  16         6        54             7             1
    IpcTcpRegpc                104        14        20            15             1
    IpcMsgReg                   52         9        37             9             0
    IpcMsgConn                 124        16        20            19             3
    NvMsg                    8,300         6        26        13,710        13,704
    EvtStateNotify              32         1        19             1             0
    EvtCrhCallBack               8         0        28            15            15
    EvtRegWait                  40         0        17             1             1
    H:CMOHandler                20         3       153             3             0
    H:CMOHandler                20         2       154             2             0
    H:CMOHandler                20        28       128            28             0
    H:CMOHandler                20         1       155             1             0
    CMOHandlerPool              12        34     2,010            34             0
    CMOObjectPool            8,080         0        64             2             2
    IKEd-var-pool               24     1,555    12,891         3,740         2,185
    IKEd-var-pool               40         1    10,000        10,056        10,055
    IKEd-var-pool               72         1     6,190             6             5
    IKEd-var-pool              136         4     3,509             6             2
    IKEd-var-pool              264         0     1,884             8             8
    IKEd-var-pool              520         1       976             2             1
    IKE global struc           848         1         1             1             0
    DH pool                     44    10,050     8,522        10,050             0
    RNG pool                    36     2,000     2,008         2,000             0
    cdpipc                   1,460         1       352             1             0
    JobResult                   44         0     4,166        12,050        12,050
    JobDesc                    272         0     1,831        12,050        12,050
    JobHandle                   72         0     6,191        12,050        12,050
    Func pool                   20        55       325            55             0
    sess mgmt pool              32         0     1,114         4,117         4,117
    iked_sess_h                 32         1     3,999             1             0
    p1 policy pool           2,636         0        50             1             1
    p2 policy pool              96         0        55             1             1
    DArbn:IKED_P1_MA            20         1        27             2             1
    p1 map pool                696         0        51             1             1
    DArbn:IKED_P2_MA            20         1        27             2             1
    p2 map pool                 52         0        62             1             1
    DArbn:IKED_IP_P1            20         1        27             1             0
    DArbn:IKED_IP_P2            20         1        27             1             0
    DArbn:IKED_XAUTH            20         1        27             1             0
    DArbn:IKED_IP_XA            20         1        27             1             0
    DAt:IKEDV2_RCF_R            20         0     8,060             5             5
    DAt:IKEDV2_RCF_S            20         0     8,060             3             3
    80 objects displayed.
    Stoke[local]#
    
    # Sample dictionary output

    {
    'CMOHandlerPool': {   'Allocs': '34',
                          'Free': '2,010',
                          'Frees': '0',
                          'InUse': '34',
                          'Size': '12'},
    'CMOObjectPool': {   'Allocs': '1',
                         'Free': '64',
                         'Frees': '1',
                         'InUse': '0',
                         'Size': '8,080'},
    'CrhCmdBlk': {   'Allocs': '4',
                     'Free': '4',
                     'Frees': '0',
                     'InUse': '4',
                     'Size': '8,224'},
    'CrhHandleData': {   'Allocs': '5',
                         'Free': '35',
                         'Frees': '0',
                         'InUse': '5',
                         'Size': '60'},
    'CrhRegData': {   'Allocs': '1',
                      'Free': '42',
                      'Frees': '0',
                      'InUse': '1',
                      'Size': '32'},
    'DArbn:IKED_IP_P1': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DArbn:IKED_IP_P2': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DArbn:IKED_IP_XA': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DArbn:IKED_P1_MA': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DArbn:IKED_P2_MA': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DArbn:IKED_XAUTH': {   'Allocs': '1',
                            'Free': '27',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '20'},
    'DH pool': {   'Allocs': '10,050',
                   'Free': '8,522',
                   'Frees': '0',
                   'InUse': '10,050',
                   'Size': '44'},
    'DaJudy': {   'Allocs': '12,146',
                  'Free': '2,078',
                  'Frees': '12,100',
                  'InUse': '46',
                  'Size': '40'},
    'DaJudy_1': {   'Allocs': '24',
                    'Free': '2,093',
                    'Frees': '22',
                    'InUse': '2',
                    'Size': '72'},
    'DaJudy_2': {   'Allocs': '17',
                    'Free': '514',
                    'Frees': '7',
                    'InUse': '10',
                    'Size': '136'},
    'DaSet': {   'Allocs': '64',
                 'Free': '6',
                 'Frees': '0',
                 'InUse': '64',
                 'Size': '128'},
    'EvtCrhCallBack': {   'Allocs': '3',
                          'Free': '28',
                          'Frees': '3',
                          'InUse': '0',
                          'Size': '8'},
    'EvtRegWait': {   'Allocs': '1',
                      'Free': '17',
                      'Frees': '1',
                      'InUse': '0',
                      'Size': '40'},
    'EvtStateNotify': {   'Allocs': '1',
                          'Free': '19',
                          'Frees': '0',
                          'InUse': '1',
                          'Size': '32'},
    'Func pool': {   'Allocs': '55',
                     'Free': '325',
                     'Frees': '0',
                     'InUse': '55',
                     'Size': '20'},
    'H:CMOHandler': {   'Allocs': '3',
                        'Free': '153',
                        'Frees': '0',
                        'InUse': '3',
                        'Size': '20'},
    'H:CMOHandler_1': {   'Allocs': '2',
                          'Free': '154',
                          'Frees': '0',
                          'InUse': '2',
                          'Size': '20'},
    'H:CMOHandler_2': {   'Allocs': '28',
                          'Free': '128',
                          'Frees': '0',
                          'InUse': '28',
                          'Size': '20'},
    'H:CMOHandler_3': {   'Allocs': '1',
                          'Free': '155',
                          'Frees': '0',
                          'InUse': '1',
                          'Size': '20'},
    'IKE global struc': {   'Allocs': '1',
                            'Free': '1',
                            'Frees': '0',
                            'InUse': '1',
                            'Size': '848'},
    'IKEd-var-pool': {   'Allocs': '3,543',
                         'Free': '12,904',
                         'Frees': '2,001',
                         'InUse': '1,542',
                         'Size': '24'},
    'IKEd-var-pool_1': {   'Allocs': '10,052',
                           'Free': '10,000',
                           'Frees': '10,051',
                           'InUse': '1',
                           'Size': '40'},
    'IKEd-var-pool_2': {   'Allocs': '4',
                           'Free': '6,189',
                           'Frees': '2',
                           'InUse': '2',
                           'Size': '72'},
    'IKEd-var-pool_3': {   'Allocs': '5',
                           'Free': '3,510',
                           'Frees': '2',
                           'InUse': '3',
                           'Size': '136'},
    'IKEd-var-pool_4': {   'Allocs': '2',
                           'Free': '1,884',
                           'Frees': '2',
                           'InUse': '0',
                           'Size': '264'},
    'IKEd-var-pool_5': {   'Allocs': '2',
                           'Free': '976',
                           'Frees': '1',
                           'InUse': '1',
                           'Size': '520'},
    'IpcAmInfo': {   'Allocs': '2',
                     'Free': '144',
                     'Frees': '2',
                     'InUse': '0',
                     'Size': '72'},
    'IpcArepIds': {   'Allocs': '5',
                      'Free': '43',
                      'Frees': '0',
                      'InUse': '5',
                      'Size': '28'},
    'IpcAsyncReply': {   'Allocs': '5',
                         'Free': '11',
                         'Frees': '0',
                         'InUse': '5',
                         'Size': '344'},
    'IpcConn': {   'Allocs': '12',
                   'Free': '29',
                   'Frees': '2',
                   'InUse': '10',
                   'Size': '400'},
    'IpcConnIds': {   'Allocs': '12',
                      'Free': '36',
                      'Frees': '0',
                      'InUse': '12',
                      'Size': '28'},
    'IpcMsgConn': {   'Allocs': '17',
                      'Free': '21',
                      'Frees': '2',
                      'InUse': '15',
                      'Size': '124'},
    'IpcMsgReg': {   'Allocs': '9',
                     'Free': '37',
                     'Frees': '0',
                     'InUse': '9',
                     'Size': '52'},
    'IpcPeer': {   'Allocs': '12',
                   'Free': '20',
                   'Frees': '0',
                   'InUse': '12',
                   'Size': '48'},
    'IpcPeerMsg': {   'Allocs': '62',
                      'Free': '28',
                      'Frees': '62',
                      'InUse': '0',
                      'Size': '56'},
    'IpcPeerMsgData': {   'Allocs': '71',
                          'Free': '20',
                          'Frees': '71',
                          'InUse': '0',
                          'Size': '80'},
    'IpcQnxConn': {   'Allocs': '6',
                      'Free': '56',
                      'Frees': '2',
                      'InUse': '4',
                      'Size': '12'},
    'IpcQnxReg': {   'Allocs': '9',
                     'Free': '23',
                     'Frees': '0',
                     'InUse': '9',
                     'Size': '80'},
    'IpcReg': {   'Allocs': '9',
                  'Free': '26',
                  'Frees': '0',
                  'InUse': '9',
                  'Size': '156'},
    'IpcRegmsg': {   'Allocs': '9',
                     'Free': '19',
                     'Frees': '0',
                     'InUse': '9',
                     'Size': '8'},
    'IpcRmInfo': {   'Allocs': '4',
                     'Free': '145',
                     'Frees': '3',
                     'InUse': '1',
                     'Size': '36'},
    'IpcRmReg': {   'Allocs': '9',
                    'Free': '44',
                    'Frees': '0',
                    'InUse': '9',
                    'Size': '24'},
    'IpcSndrArep': {   'Allocs': '3',
                       'Free': '15',
                       'Frees': '0',
                       'InUse': '3',
                       'Size': '36'},
    'IpcTcpConn': {   'Allocs': '5',
                      'Free': '55',
                      'Frees': '0',
                      'InUse': '5',
                      'Size': '16'},
    'IpcTcpReg': {   'Allocs': '9',
                     'Free': '37',
                     'Frees': '0',
                     'InUse': '9',
                     'Size': '52'},
    'IpcTcpRegpc': {   'Allocs': '13',
                       'Free': '21',
                       'Frees': '0',
                       'InUse': '13',
                       'Size': '104'},
    'IpcThrData': {   'Allocs': '73',
                      'Free': '22',
                      'Frees': '73',
                      'InUse': '0',
                      'Size': '28'},
    'IpcThrEnt': {   'Allocs': '6',
                     'Free': '18',
                     'Frees': '6',
                     'InUse': '0',
                     'Size': '36'},
    'IpcTrCgIds': {   'Allocs': '12',
                      'Free': '36',
                      'Frees': '0',
                      'InUse': '12',
                      'Size': '28'},
    'IpcTrConn': {   'Allocs': '12',
                     'Free': '30',
                     'Frees': '2',
                     'InUse': '10',
                     'Size': '388'},
    'IpcTrConnG': {   'Allocs': '12',
                      'Free': '25',
                      'Frees': '2',
                      'InUse': '10',
                      'Size': '188'},
    'IpcTrNode': {   'Allocs': '12',
                     'Free': '22',
                     'Frees': '2',
                     'InUse': '10',
                     'Size': '112'},
    'IpcTrReg': {   'Allocs': '9',
                    'Free': '32',
                    'Frees': '0',
                    'InUse': '9',
                    'Size': '84'},
    'IpcTrRegac': {   'Allocs': '13',
                      'Free': '20',
                      'Frees': '0',
                      'InUse': '13',
                      'Size': '76'},
    'IpcTrRegacI': {   'Allocs': '13',
                       'Free': '35',
                       'Frees': '0',
                       'InUse': '13',
                       'Size': '28'},
    'IpcTrRegpc': {   'Allocs': '13',
                      'Free': '22',
                      'Frees': '0',
                      'InUse': '13',
                      'Size': '72'},
    'IpcTrRegpcI': {   'Allocs': '13',
                       'Free': '35',
                       'Frees': '0',
                       'InUse': '13',
                       'Size': '28'},
    'IpcTrSlot': {   'Allocs': '12',
                     'Free': '28',
                     'Frees': '2',
                     'InUse': '10',
                     'Size': '64'},
    'IpcTrWantReg': {   'Allocs': '8',
                        'Free': '40',
                        'Frees': '0',
                        'InUse': '8',
                        'Size': '28'},
    'JobDesc': {   'Allocs': '12,050',
                   'Free': '1,831',
                   'Frees': '12,050',
                   'InUse': '0',
                   'Size': '272'},
    'JobHandle': {   'Allocs': '12,050',
                     'Free': '6,191',
                     'Frees': '12,050',
                     'InUse': '0',
                     'Size': '72'},
    'JobResult': {   'Allocs': '12,050',
                     'Free': '4,166',
                     'Frees': '12,050',
                     'InUse': '0',
                     'Size': '44'},
    'MsgVerPool': {   'Allocs': '5',
                      'Free': '16',
                      'Frees': '0',
                      'InUse': '5',
                      'Size': '176'},
    'NvMsg': {   'Allocs': '26',
                 'Free': '27',
                 'Frees': '21',
                 'InUse': '5',
                 'Size': '8,300'},
    'NvTimer': {   'Allocs': '1,659',
                   'Free': '7,643',
                   'Frees': '1,654',
                   'InUse': '5',
                   'Size': '56'},
    'Object Count': {   'Count': '74 objects displayed.'},
    'RNG pool': {   'Allocs': '2,000',
                    'Free': '2,008',
                    'Frees': '0',
                    'InUse': '2,000',
                    'Size': '36'},
    'cdpipc': {   'Allocs': '1',
                  'Free': '352',
                  'Frees': '0',
                  'InUse': '1',
                  'Size': '1,460'},
    'iked_sess_h': {   'Allocs': '1',
                       'Free': '3,999',
                       'Frees': '0',
                       'InUse': '1',
                       'Size': '32'},
    'sess mgmt pool': {   'Allocs': '828',
                          'Free': '1,114',
                          'Frees': '828',
                          'InUse': '0',
                          'Size': '32'}}


    """

    command = "show module iked slot " + slot + " ma pool"
    raw_modIkedMaPool_list = self.cmd(command)
    modIkedMaPool_list = raw_modIkedMaPool_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print modIkedMaPool_list
    
    if 'ERROR:' in raw_modIkedMaPool_list:
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_modIkedMaPool_list
        modIkedMaPool_dict['Status'] = 'Error'
        return modIkedMaPool_dict

    labels_line = modIkedMaPool_list[1].split()
    dupKey_dict = {}
    divider_line = modIkedMaPool_list[2]
    columnDict = parse_divider_line(self,divider_line)
    for raw_line in modIkedMaPool_list[3:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
   	if "objects displayed" in line:
	    # Save the objec count
	    modIkedMaPool_dict["Object Count"] = {"Count":line}
	else:
            local_dict = {}
	    start = columnDict[0][0]
    	    end = columnDict[0][1]+1
            name = line[start:end].strip()
            if debug:
                print 'The name is:', name
	    for labels_idx in range(1,len(labels_line)):
	        start = columnDict[labels_idx][0]
    	        end = columnDict[labels_idx][1]+1
                local_dict[labels_line[labels_idx]] = line[start:end].strip()
                if debug:
            	    print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
    	    # We store last entry in the main dictionary we return
	    if name in dupKey_dict:
		# for duplicate keys, append the index to the key ti differentiate between them
		dupKey_dict[name] += 1
		name = name + "_" + `dupKey_dict[name]`	
    	        modIkedMaPool_dict[name] = local_dict
    	    else:
		dupKey_dict[name] = 0
		modIkedMaPool_dict[name] = local_dict
    
    return modIkedMaPool_dict
    
def show_module_iked_slot_ma_shared(self,slot):
    """Runs the command 'show module iked slot <slot> ma share' and parses the output. 
    """
    modIkedMaShared_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show module iked slot 2 ma shared 
    Name/            Elements  HiWat/    In Use/   Allocs/       Alloc Fail/
     Pool Size       Elem Size User Size Free      Frees         Double Free
    ---------------- --------- --------- --------- ------------- -----------
    MBuf                97,340     4,109     4,099        18,935           0
         211,812,352     2,176     2,144    93,241        14,836           0
    FpdPage              4,964         1         1             1           0
          20,971,520     4,224     4,192     4,963             0           0
    Stoke[local]#

    # Sample dictionary output:
    {
    'FpdPage': {   'Alloc Fail/': '0',
                   'Allocs/': '1',
                   'Double Free': '0',
                   'Elem Size': '4,224',
                   'Elements': '4,964',
                   'Free': '4,963',
                   'Frees': '0',
                   'HiWat/': '1',
                   'In Use/': '1',
                   'Pool Size': '20,971,520',
                   'User Size': '4,192'},
    'MBuf': {   'Alloc Fail/': '0',
                'Allocs/': '4,099',
                'Double Free': '0',
                'Elem Size': '2,176',
                'Elements': '97,340',
                'Free': '93,241',
                'Frees': '0',
                'HiWat/': '4,099',
                'In Use/': '4,099',
                'Pool Size': '211,812,352',
                'User Size': '2,144'}}



    """

    command = "show module iked slot " + slot + " ma shared"
    raw_modIkedMaShared_list = self.cmd(command)
    modIkedMaShared_list = raw_modIkedMaShared_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print modIkedMaShared_list
    
    if 'ERROR:' in raw_modIkedMaShared_list:
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_modIkedMaShared_list
        modIkedMaShared_dict['Status'] = 'Error'
        return modIkedMaShared_dict

    labels_line1 = modIkedMaShared_list[1]
    labels_line2 = modIkedMaShared_list[2]
    divider_line = modIkedMaShared_list[3]
    columnDict = parse_divider_line(self,divider_line)
    oddLine = False
    local_dict = {}
    for raw_line in modIkedMaShared_list[4:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
        #name = line[start:end].strip()
	if oddLine:
	    labels_line = labels_line2
	else:
    	    local_dict = {}
	    labels_line = labels_line1
	for idx in columnDict.keys():
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    label = labels_line[start:end].strip()
 	    if (idx == 0) and (not oddLine):
		name = line[start:end].strip()
        	if debug:
            	    print 'The name is:', name
	    else:
            	local_dict[label] = line[start:end].strip()
            	if debug:
                    print("The %s is: %s " %(label,local_dict[label]))
    	# We store last entry in the main dictionary we return
	modIkedMaShared_dict[name] = local_dict
   	if oddLine:
	    oddLine = False
	else:
	    oddLine = True
 
    return modIkedMaShared_dict

def show_port_counters_drop(self,slotport):
    """Runs the command 'show port <slot/port> counters drop' and parses the output. 
    """
    portCountersDrop_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show port 2/1 counters drop 
    Port  Drop Counters
    ----- --------------------------------------------
    2/1   Disabled Port:                             0
          CCT expects IPv4:                      17626
    Stoke[local]#
    
    # Sample dictionary output
    {
    '2/1': {   'Disabled Port': '0',
               'Invalid FIB': '64'}}

    """

    command = "show port " + slotport + " counters drop"
    raw_portCountersDrop_list = self.cmd(command)
    portCountersDrop_list = raw_portCountersDrop_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print portCountersDrop_list
    
    if ('ERROR:' in raw_portCountersDrop_list):
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_portCountersDrop_list
        portCountersDrop_dict['Status'] = 'Error'
        return portCountersDrop_dict

    divider_line = portCountersDrop_list[2]
    columnDict = parse_divider_line(self,divider_line)
    local_dict = {}
    for raw_line in portCountersDrop_list[3:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
        tmp_name = line[start:end].strip()
	if tmp_name != "":
	    name = tmp_name	
	    local_dict = {}
       	if debug:
            print 'The name is:', name
	for idx in range(1,len(columnDict.keys())):
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    labelValue = line[start:end].strip().split(":")
            local_dict[labelValue[0].strip()] = labelValue[1].strip() 
            if debug:
                print("The %s is: %s " %(labelValue[0],local_dict[labelValue[0]]))
    	# We store last entry in the main dictionary we return
	portCountersDrop_dict[name] = local_dict
 
    return portCountersDrop_dict
    
def show_process_cpu_non_zero(self):
    """Runs the command 'show process cpu non-zero' and parses the output. 
    """
    processCpuNonZero_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show process cpu non-zero 
    CPU0 Utilization for 5 seconds:  1.94%   1 Minute:  4.29%   5 Minutes:  4.14%
    CPU1 Utilization for 5 seconds:  0.01%   1 Minute:  0.15%   5 Minutes:  0.09%

    Name           PID     StartTime                CPU uTime  sTime  % Now
    -------------- ------- ------------------------ --- ------ ------ ------
    System:0             0 Sat Oct 01 11:01:44      all 38m21s 27.748  0.99%
    NSM:0           704514 Sat Oct 01 11:01:44        0 37m15s  2.553  1.09%
    Stoke[local]#

    # Sample dictionary output

    {
    'CPU0 Utilization ': {   'fivemins': '2.54%',
                             'fivesecs': '21.03%',
                             'onemin': '3.02%'},
    'CPU1 Utilization ': {   'fivemins': '0.03%',
                             'fivesecs': '0.89%',
                             'onemin': '0.05%'},
    'Cli:0         ': {   '% Now': '0.69%',
                          'CPU': '0',
                          'PID': '974895',
                          'StartTime': 'Fri Oct 07 20:35:03',
                          'sTime': '0.021',
                          'uTime': '0.423'},
    'Ip:0          ': {   '% Now': '0.29%',
                          'CPU': '0',
                          'PID': '745500',
                          'StartTime': 'Fri Oct 07 19:39:21',
                          'sTime': '0.060',
                          'uTime': '0.451'},
    'NSM:0         ': {   '% Now': '1.09%',
                          'CPU': '0',
                          'PID': '704514',
                          'StartTime': 'Fri Oct 07 19:39:10',
                          'sTime': '0.322',
                          'uTime': '38.418'},
    'System:0      ': {   '% Now': '0.99%',
                          'CPU': 'all',
                          'PID': '0',
                          'StartTime': 'Fri Oct 07 19:39:11',
                          'sTime': '3.415',
                          'uTime': '50.834'}}

    """

    command = "show process cpu non-zero"
    raw_processCpuNonZero_list = self.cmd(command)
    processCpuNonZero_list = raw_processCpuNonZero_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print processCpuNonZero_list

    # process the first two lines of output
    for idx in range(1,3):
	local_dict = {}
	line = processCpuNonZero_list[idx] 
    	p = re.compile('(?P<cpu>CPU. Utilization )for 5 seconds:\s+(?P<fivesecs>[\d.%]+)\s+1 Minute:\s+(?P<onemin>[\d.%]+)\s+5 Minutes:\s+(?P<fivemins>[\d.%]+)')
    	m = p.search(line)
    	if m:
    	    dict = m.groupdict()
            if debug:
                print("The dict is: %s " %dict)
	    local_dict['fivesecs'] = dict['fivesecs']
            if debug:
                print("The five seconds is: %s " %(local_dict['fivesecs']))
	    local_dict['onemin'] = dict['onemin']
            if debug:
                print("The one minute is: %s " %(local_dict['onemin']))
	    local_dict['fivemins'] = dict['fivemins']
            if debug:
                print("The five minutes is: %s " %(local_dict['fivemins']))
	    processCpuNonZero_dict[dict['cpu']] = local_dict
	
    
    labels_line = processCpuNonZero_list[4]
    divider_line = processCpuNonZero_list[5]
    columnDict = parse_divider_line(self,divider_line)
    for raw_line in processCpuNonZero_list[6:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
	name = line[start:end]
       	if debug:
            print 'The name is:', name
        local_dict = {}
	for idx in range(1,len(columnDict.keys())):
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    label = labels_line[start:end].strip()
            local_dict[label] = line[start:end].strip() 
            if debug:
                print("The %s is: %s " %(label,local_dict[label]))
    	# We store last entry in the main dictionary we return
	processCpuNonZero_dict[name] = local_dict
 
    return processCpuNonZero_dict
    
    
def show_qos_red_slot(self,slot):
    """Runs the command 'show qos red slot <slot>' and parses the output. 
    """
    qosRedSlot_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show qos red slot 2
                           average     current
    port    queue weight   queue depth queue depth red drops      red tail drops
    ----    ----- -------- ----------- ----------- -------------- --------------
       0 
    	    nct        1/1           0           0              0              0
	    ct         1/1           0           0              0              0
	    ef         1/1           0           0              0              0
	    af4        1/1           0           0              0              0
	    af3        1/1           0           0              0              0
	    af2        1/1           0           0              0              0
	    af1        1/1           0           0              0              0
	    be         1/1           0           0              0              0
       1 
	    nct        1/1           0           0              0              0
	    ct         1/1           0           0              0              0
    	    ef         1/1           0           0              0              0
	    af4        1/1           0           0              0              0
	    af3        1/1           0           0              0              0
	    af2        1/1           0           0              0              0
	    af1        1/1           0           0              0              0
	    be         1/1           0           0              0              0
       2 
	    nct        1/1           0           0              0              0
	    ct         1/1           0           0              0              0
	    ef         1/1           0           0              0              0
	    af4        1/1           0           0              0              0
	    af3        1/1           0           0              0              0
	    af2        1/1           0           0              0              0
	    af1        1/1           0           0              0              0
	    be         1/1           0           0              0              0
       3 
	    nct        1/1           0           0              0              0
	    ct         1/1           0           0              0              0
	    ef         1/1           0           0              0              0
	    af4        1/1           0           0              0              0
	    af3        1/1           0           0              0              0
	    af2        1/1           0           0              0              0
	    af1        1/1           0           0              0              0
	    be         1/1           0           0              0              0
    Stoke[local]#

    # Sample dictionary output

    {
    '0 - af1': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '0 - af2': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '0 - af3': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '0 - af4': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '0 - be': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '0 - ct': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '0 - ef': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '0 - nct': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '1 - af1': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '1 - af2': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '1 - af3': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '1 - af4': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '1 - be': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '1 - ct': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '1 - ef': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '1 - nct': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '2 - af1': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '2 - af2': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '2 - af3': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '2 - af4': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '2 - be': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '2 - ct': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '2 - ef': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '2 - nct': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '3 - af1': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '3 - af2': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '3 - af3': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '3 - af4': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'},
    '3 - be': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '3 - ct': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '3 - ef': {   'average queue depth': '0',
                  'current queue depth': '0',
                  'red drops': '0',
                  'red tail drops': '0',
                  'weight': '1/1'},
    '3 - nct': {   'average queue depth': '0',
                   'current queue depth': '0',
                   'red drops': '0',
                   'red tail drops': '0',
                   'weight': '1/1'}}

    """

    command = "show qos red slot " + slot
    raw_qosRedSlot_list = self.cmd(command)
    qosRedSlot_list = raw_qosRedSlot_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print qosRedSlot_list

    if ('ERROR:' in raw_qosRedSlot_list):
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_qosRedSlot_list
        qosRedSlot_dict['Status'] = 'Error'
        return qosRedSlot_dict

    labels_line1 = qosRedSlot_list[1]
    labels_line2 = qosRedSlot_list[2]
    divider_line = qosRedSlot_list[3]
    columnDict = parse_divider_line(self,divider_line)
    for raw_line in qosRedSlot_list[4:]:
        line = raw_line.expandtabs(columnDict[1][0])
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
	tmp_name = line[start:end].strip()
	if tmp_name != "":
	    name = "%s/%s" %(slot,tmp_name)
    	    local_dict = {}
       	    if debug:
            	print 'The name is:', name
	else:
	    tmp_dict = {}
	    start = columnDict[1][0]
    	    end = columnDict[1][1]+1
	    qname = line[start:end].strip() 
	    for idx in range(2,len(columnDict.keys())):
	        start = columnDict[idx][0]
    	        end = columnDict[idx][1]+1
                label = labels_line1[start:end].strip() + " " + labels_line2[start:end].strip()
                label = label.strip()
                tmp_dict[label] = line[start:end].strip()
                if debug:
                    print("The %s is: %s " %(label,tmp_dict[label]))
	    local_dict[qname] = tmp_dict
	    qosRedSlot_dict[name] = local_dict
 
    return qosRedSlot_dict
    
def show_port_counters(self):
    """Runs the command 'show port counters' and parses the output. 
    """
    portCounters_dict = {}
    debug = False
    
    # Sample raw input
    """
    Stoke[local]#show port counter
    Wed Oct  5 04:15:01 UTC 2011.
    Port  Input Packets    Input Octets       Output Packets   Output Octets
    ----- ---------------- ------------------ ---------------- ------------------
    0/0              22907            1709566             3926             308871
    1/0                  0                  0                0                  0
    2/0              89288            7579994            76301            6534824
    2/1              86243            7314258            76124            6506526
    3/0               1660             157990             1926             127614
    3/1               1678             159519              114              11646
    4/0              17355            1377341            16934            1391282
    4/1              14305            1117637            17561            1407530
    Stoke[local]#

    # Sample dictionary output
    {
    '0/0': {   'Input Octets': '328099',
               'Input Packets': '3020',
               'Output Octets': '91680',
               'Output Packets': '684'},
    '1/0': {   'Input Octets': '0',
               'Input Packets': '0',
               'Output Octets': '0',
               'Output Packets': '0'},
    '2/0': {   'Input Octets': '32402',
               'Input Packets': '221',
               'Output Octets': '0',
               'Output Packets': '0'},
    '2/1': {   'Input Octets': '21164',
               'Input Packets': '51',
               'Output Octets': '0',
               'Output Packets': '0'}}

    """

    command = "show port counters"
    raw_portCounters_list = self.cmd(command)
    portCounters_list = raw_portCounters_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print portCounters_list

    labels_line = portCounters_list[2]
    divider_line = portCounters_list[3]
    columnDict = parse_divider_line(self,divider_line)
    for raw_line in portCounters_list[4:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
	name = line[start:end].strip()
       	if debug:
            print 'The name is:', name
        local_dict = {}
	for idx in range(1,len(columnDict.keys())):
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    label = labels_line[start:end].strip()
            local_dict[label] = line[start:end].strip() 
            if debug:
                print("The %s is: %s " %(label,local_dict[label]))
    	# We store last entry in the main dictionary we return
	portCounters_dict[name] = local_dict
 
    return portCounters_dict
    
    
def show_ike_session_counters(self):
    """Runs the command 'show ike-session counters' and parses the output. 
    """
    ikeSessionCounters_dict = {}
    debug = False
    
    """
    # Sample raw input

    iceland[ctx1]#show ike-session counters 
    Wed Oct  5 16:43:42 UTC 2011.
    -----------------------------------------------------------------------
         Phase1     Phase1     Phase1     Phase1     Phase2     Phase2
    Slot Successful Dropped    Failed     Active     Successful Failed
    ---- ---------- ---------- ---------- ---------- ---------- ----------
    2    0          0          150        0          0          150       
    ---- ---------- ---------- ---------- ---------- ---------- ----------

    Sum  0          0          150        0          0          150       

    Active Sessions: 0          Total Sessions: 0

    iceland[ctx1]#

    # Sample dictionary output

    {
    '2': {   'Phase1 Active': '0',
             'Phase1 Dropped': '0',
             'Phase1 Failed': '0',
             'Phase1 Successful': '0',
             'Phase2 Failed': '0',
             'Phase2 Successful': '0'},
    'Sessions': {   'Active Sessions': '0',
                    'Total Sessions': '0'},
    'Sum': {   'Phase1 Active': '0',
               'Phase1 Dropped': '0',
               'Phase1 Failed': '0',
               'Phase1 Successful': '0',
               'Phase2 Failed': '0',
               'Phase2 Successful': '0'}
    }

    """

    command = "show ike-session counters"
    raw_ikeSessionCounters_list = self.cmd(command)
    ikeSessionCounters_list = raw_ikeSessionCounters_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print ikeSessionCounters_list

    labels_line1 = ikeSessionCounters_list[3]
    labels_line2 = ikeSessionCounters_list[4]
    divider_line = ikeSessionCounters_list[5]
    columnDict = parse_divider_line(self,divider_line)
    processLine = 6
    for raw_line in ikeSessionCounters_list[6:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	start = columnDict[0][0]
    	end = columnDict[0][1]+1
	name = line[start:end].strip()
	if (name == "----") or (name == ""):
	    # the divider/empty line between slot and sum.  Ignore these lines
	    continue
       	if debug:
            print 'The name is:', name
        local_dict = {}
	for idx in range(1,len(columnDict.keys())):
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    label = labels_line1[start:end].strip() + " " + labels_line2[start:end].strip()
	    label = label.strip() 
            local_dict[label] = line[start:end].strip() 
            if debug:
                print("The %s is: %s " %(label,local_dict[label]))
    	# We store last entry in the main dictionary we return
	ikeSessionCounters_dict[name] = local_dict
	processLine += 1
	if name == "Sum":
	    # End of normal output display.  Stop
	    break

    for raw_line in ikeSessionCounters_list[processLine:]:
        line = raw_line
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
    	p = re.compile('(?P<active>Active Sessions):\s+(?P<actses>[\d]+)\s+(?P<total>Total Sessions):\s+(?P<totses>[\d]+)')
    	m = p.search(line)
    	if m:
	    local_dict = {}
    	    dict = m.groupdict()
            if debug:
                print("The dict is: %s " %dict)
	    local_dict[dict['active']] = dict['actses']
            if debug:
                print("The %s is: %s " %(dict['active'],local_dict[dict['active']]))
	    local_dict[dict['total']] = dict['totses']
            if debug:
                print("The %s is: %s " %(dict['total'],local_dict[dict['total']]))
    	    # We store last entry in the main dictionary we return
	    ikeSessionCounters_dict['Sessions'] = local_dict
 
    return ikeSessionCounters_dict
    
    
def show_environmental_detail(self):
    """Runs the command 'show environmental detail' and parses the output. 
    """
    environmentalDetail_dict = {}
    debug = False
    
    # Sample raw input
    """
    iceland[local]#show environmental detail 
    Environmental status as of Fri Oct  7 14:52:21 2011
    Data polling interval is 60 second(s)

    Voltage readings:
    =================
    Slot		 Source		 Reading    	 Level
    ----		 ------		 -----------	 -------
    0		 GPP         	 1111		 None
    0		 VCC 1.8V 	 1784		 None
    0		 TCAM     	 1194		 None
    0		 VCC 2.5V 	 2520		 None
    0		 DDR Term 	 1239		 None
    0		 VCC 3.3V 	 3294		 None
    0		 VCC 5.0V 	 4985		 None
    0		 FIC      	 4902		 None
    0		 SysContr    	 1478		 None
    0		 VCC 12.0V	 11989		 None
    1		 GPP         	 1122		 None
    1		 VCC 1.8V 	 1784		 None
    1		 TCAM     	 1214		 None
    1		 VCC 2.5V 	 2492		 None
    1		 DDR Term 	 1252		 None
    1		 VCC 3.3V 	 3312		 None
    1		 VCC 5.0V 	 4985		 None
    1		 FIC      	 4957		 None
    1		 SysContr    	 1494		 None
    1		 VCC 12.0V	 11923		 None
    1		 GPP         	 1122		 None
    1		 VCC 1.8V 	 1784		 None
    1		 TCAM     	 1214		 None
    1		 VCC 2.5V 	 2492		 None
    1		 DDR Term 	 1252		 None
    1		 VCC 3.3V 	 3312		 None
    1		 VCC 5.0V 	 4985		 None
    1		 FIC      	 4957		 None
    1		 SysContr    	 1494		 None
    1		 VCC 12.0V	 11923		 None
    2		 CPU 1.0V CA	 1012		 None
    2		 CPU 1.0V CB	 1004		 None
    2		 CPU 1.0V PL	 996		 None
    2		 CPU DDR3	 1492		 None
    2		 CPU SDRAM VTT	 748		 None
    2		 KBP0 Analog	 892		 None
    2		 KBP1 Analog	 892		 None
    2		 KBP0 Core	 900		 None
    2		 KBP1 Core	 900		 None
    2		 NPU 1.0V	 996		 None
    2		 NPU VDD SRAM	 1004		 None
    2		 NPU0 Analog	 988		 None
    2		 NPU1 Analog	 988		 None
    2		 NPU0 AC SD VTT	 740		 None
    2		 NPU0 BD SD VTT	 740		 None
    2		 NPU1 AC SD VTT	 740		 None
    2		 NPU1 BD SD VTT	 732		 None
    2		 NPU0 DDR3	 1492		 None
    2		 NPU1 DDR3	 1484		 None
    2		 Switch Analog	 988		 None
    2		 Switch Core	 996		 None
    2		 VCC 1.2V	 1204		 None
    2		 VCC 1.8V	 1800		 None
    2		 VCC 2.5V	 2473		 None
    2		 VCC 3.3V	 3323		 None
    2		 VCC 12.0V	 11868		 None
    
    Temperature readings:
    =====================
    Slot		 Source		 Reading    	 Level
    ----		 ------		 -----------	 -------
    0		 Inlet        	 33		 None
    0		 Outlet       	 44		 None
    0		 GPP0         	 60		 None
    0		 GPP1         	 38		 None
    1		 Inlet        	 31		 None
    1		 Outlet       	 45		 None
    1		 GPP0         	 64		 None
    1		 GPP1         	 41		 None
    2		 GPP0        	 71		 None
    2		 NPU0        	 67		 None
    2		 NPU1        	 77		 None
    
    Power status:
    =============
    Slot		 Source		 Reading    	 Level
    ----		 ------		 -----------	 -------
    PEMA		 Power Trip	 OK		 None
    PEMA		 Temperature	 OK		 None
    PEMA		 -48V Powergood	 OK		 None
    PEMA		 -48V Miswire	 OK		 None
    PEMA		 Backplane 3.3V	 OK		 None
    PEMB		 Power Trip	 Tripped	 Minor
    PEMB		 Temperature	 OK		 None
    PEMB		 -48V Powergood	 OK		 None
    PEMB		 -48V Miswire	 OK		 None
    PEMB		 Backplane 3.3V	 OK		 None

    Fan status:
    ===========
    Slot		 Source		 Reading    	 Level
    ----		 ------		 -----------	 -------
    FANTRAY1	         48V Fuse-A	 OK		 None
    FANTRAY1	         48V Fuse-B	 OK		 None
    FANTRAY1	         Fans-Stat	 OK		 None
    FANTRAY1	         Fan1 status	 0		 
    FANTRAY1	         Fan2 status	 0		 
    FANTRAY1	         Fan1 speed	 4028		 
    FANTRAY1	         Fan2 speed	 4700		 
    FANTRAY2	         48V Fuse-A	 OK		 None
    FANTRAY2	         48V Fuse-B	 OK		 None
    FANTRAY2	         Fans-Stat	 OK		 None
    FANTRAY2	         Fan1 status	 0		 
    FANTRAY2	         Fan2 status	 0		 
    FANTRAY2	         Fan1 speed	 4512		 
    FANTRAY2	         Fan2 speed	 3889		 

    Alarm status:
    =============
    Slot		 Source		 Reading    	 Level
    ----		 ------		 -----------	 -------
    ALARM1		 Backplane 3.3V	 OK		 None
    ALARM1		 Alarm Cutfoff	 Off		 None
    iceland[local]# 



    Sample dictionary output:
    =========================
    {
    'Alarm status - ALARM1 - Alarm Cutfoff': {   'level': 'None',
                                                 'reading': 'Off'},
    'Alarm status - ALARM1 - Backplane 3.3V': {   'level': 'None',
                                                  'reading': 'OK'},
    'Fan status - FANTRAY1 - 48V Fuse-A': {   'level': 'None',
                                              'reading': 'OK'},
    'Fan status - FANTRAY1 - 48V Fuse-B': {   'level': 'None',
                                              'reading': 'OK'},
    'Fan status - FANTRAY1 - Fan1 speed': {   'reading': '4028'},
    'Fan status - FANTRAY1 - Fan1 status': {   'reading': '0'},
    'Fan status - FANTRAY1 - Fan2 speed': {   'reading': '4700'},
    'Fan status - FANTRAY1 - Fan2 status': {   'reading': '0'},
    'Fan status - FANTRAY1 - Fans-Stat': {   'level': 'None',
                                             'reading': 'OK'},
    'Fan status - FANTRAY2 - 48V Fuse-A': {   'level': 'None',
                                              'reading': 'OK'},
    'Fan status - FANTRAY2 - 48V Fuse-B': {   'level': 'None',
                                              'reading': 'OK'},
    'Fan status - FANTRAY2 - Fan1 speed': {   'reading': '4338'},
    'Fan status - FANTRAY2 - Fan1 status': {   'reading': '0'},
    'Fan status - FANTRAY2 - Fan2 speed': {   'reading': '3889'},
    'Fan status - FANTRAY2 - Fan2 status': {   'reading': '0'},
    'Fan status - FANTRAY2 - Fans-Stat': {   'level': 'None',
                                             'reading': 'OK'},
    'Power status - PEMA - -48V Miswire': {   'level': 'None',
                                              'reading': 'OK'},
    'Power status - PEMA - -48V Powergood': {   'level': 'None',
                                                'reading': 'OK'},
    'Power status - PEMA - Backplane 3.3V': {   'level': 'None',
                                                'reading': 'OK'},
    'Power status - PEMA - Power Trip': {   'level': 'None',
                                            'reading': 'OK'},
    'Power status - PEMA - Temperature': {   'level': 'None',
                                             'reading': 'OK'},
    'Power status - PEMB - -48V Miswire': {   'level': 'None',
                                              'reading': 'OK'},
    'Power status - PEMB - -48V Powergood': {   'level': 'None',
                                                'reading': 'OK'},
    'Power status - PEMB - Backplane 3.3V': {   'level': 'None',
                                                'reading': 'OK'},
    'Power status - PEMB - Power Trip': {   'level': 'Minor',
                                            'reading': 'Tripped'},
    'Power status - PEMB - Temperature': {   'level': 'None',
                                             'reading': 'OK'},
    'Temperature readings - 0 - GPP0': {   'level': 'None',
                                           'reading': '60'},
    'Temperature readings - 0 - GPP1': {   'level': 'None',
                                           'reading': '39'},
    'Temperature readings - 0 - Inlet': {   'level': 'None',
                                            'reading': '33'},
    'Temperature readings - 0 - Outlet': {   'level': 'None',
                                             'reading': '45'},
    'Temperature readings - 1 - GPP0': {   'level': 'None',
                                           'reading': '64'},
    'Temperature readings - 1 - GPP1': {   'level': 'None',
                                           'reading': '41'},
    'Temperature readings - 1 - Inlet': {   'level': 'None',
                                            'reading': '31'},
    'Temperature readings - 1 - Outlet': {   'level': 'None',
                                             'reading': '45'},
    'Temperature readings - 2 - GPP0': {   'level': 'None',
                                           'reading': '71'},
    'Temperature readings - 2 - NPU0': {   'level': 'None',
                                           'reading': '67'},
    'Temperature readings - 2 - NPU1': {   'level': 'None',
                                           'reading': '76'},
    'Voltage readings - 0 - DDR Term': {   'level': 'None',
                                           'reading': '1239'},
    'Voltage readings - 0 - FIC': {   'level': 'None',
                                      'reading': '4902'},
    'Voltage readings - 0 - GPP': {   'level': 'None',
                                      'reading': '1111'},
    'Voltage readings - 0 - SysContr': {   'level': 'None',
                                           'reading': '1478'},
    'Voltage readings - 0 - TCAM': {   'level': 'None',
                                       'reading': '1194'},
    'Voltage readings - 0 - VCC 1.8V': {   'level': 'None',
                                           'reading': '1784'},
    'Voltage readings - 0 - VCC 12.0V': {   'level': 'None',
                                            'reading': '11989'},
    'Voltage readings - 0 - VCC 2.5V': {   'level': 'None',
                                           'reading': '2492'},
    'Voltage readings - 0 - VCC 3.3V': {   'level': 'None',
                                           'reading': '3294'},
    'Voltage readings - 0 - VCC 5.0V': {   'level': 'None',
                                           'reading': '4985'},
    'Voltage readings - 1 - DDR Term': {   'level': 'None',
                                           'reading': '1252'},
    'Voltage readings - 1 - FIC': {   'level': 'None',
                                      'reading': '5013'},
    'Voltage readings - 1 - GPP': {   'level': 'None',
                                      'reading': '1122'},
    'Voltage readings - 1 - SysContr': {   'level': 'None',
                                           'reading': '1486'},
    'Voltage readings - 1 - TCAM': {   'level': 'None',
                                       'reading': '1214'},
    'Voltage readings - 1 - VCC 1.8V': {   'level': 'None',
                                           'reading': '1784'},
    'Voltage readings - 1 - VCC 12.0V': {   'level': 'None',
                                            'reading': '11923'},
    'Voltage readings - 1 - VCC 2.5V': {   'level': 'None',
                                           'reading': '2492'},
    'Voltage readings - 1 - VCC 3.3V': {   'level': 'None',
                                           'reading': '3312'},
    'Voltage readings - 1 - VCC 5.0V': {   'level': 'None',
                                           'reading': '4985'},
    'Voltage readings - 2 - CPU 1.0V CA': {   'level': 'None',
                                              'reading': '1012'},
    'Voltage readings - 2 - CPU 1.0V CB': {   'level': 'None',
                                              'reading': '1004'},
    'Voltage readings - 2 - CPU 1.0V PL': {   'level': 'None',
                                              'reading': '996'},
    'Voltage readings - 2 - CPU DDR3': {   'level': 'None',
                                           'reading': '1484'},
    'Voltage readings - 2 - CPU SDRAM VTT': {   'level': 'None',
                                                'reading': '740'},
    'Voltage readings - 2 - KBP0 Analog': {   'level': 'None',
                                              'reading': '892'},
    'Voltage readings - 2 - KBP0 Core': {   'level': 'None',
                                            'reading': '892'},
    'Voltage readings - 2 - KBP1 Analog': {   'level': 'None',
                                              'reading': '892'},
    'Voltage readings - 2 - KBP1 Core': {   'level': 'None',
                                            'reading': '900'},
    'Voltage readings - 2 - NPU 1.0V': {   'level': 'None',
                                           'reading': '996'},
    'Voltage readings - 2 - NPU VDD SRAM': {   'level': 'None',
                                               'reading': '1004'},
    'Voltage readings - 2 - NPU0 AC SD VTT': {   'level': 'None',
                                                 'reading': '740'},
    'Voltage readings - 2 - NPU0 Analog': {   'level': 'None',
                                              'reading': '988'},
    'Voltage readings - 2 - NPU0 BD SD VTT': {   'level': 'None',
                                                 'reading': '740'},
    'Voltage readings - 2 - NPU0 DDR3': {   'level': 'None',
                                            'reading': '1492'},
    'Voltage readings - 2 - NPU1 AC SD VTT': {   'level': 'None',
                                                 'reading': '740'},
    'Voltage readings - 2 - NPU1 Analog': {   'level': 'None',
                                              'reading': '980'},
    'Voltage readings - 2 - NPU1 BD SD VTT': {   'level': 'None',
                                                 'reading': '740'},
    'Voltage readings - 2 - NPU1 DDR3': {   'level': 'None',
                                            'reading': '1484'},
    'Voltage readings - 2 - Switch Analog': {   'level': 'None',
                                                'reading': '988'},
    'Voltage readings - 2 - Switch Core': {   'level': 'None',
                                              'reading': '996'},
    'Voltage readings - 2 - VCC 1.2V': {   'level': 'None',
                                           'reading': '1204'},
    'Voltage readings - 2 - VCC 1.8V': {   'level': 'None',
                                           'reading': '1800'},
    'Voltage readings - 2 - VCC 12.0V': {   'level': 'None',
                                            'reading': '11868'},
    'Voltage readings - 2 - VCC 2.5V': {   'level': 'None',
                                           'reading': '2473'},
    'Voltage readings - 2 - VCC 3.3V': {   'level': 'None',
                                           'reading': '3323'}
    }


    """

    command = "show environmental detail"
    raw_environmentalDetail_list = self.cmd(command)
    environmentalDetail_list = raw_environmentalDetail_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print environmentalDetail_list

    curname = ""
    isName = False
    for raw_line in environmentalDetail_list[4:]:
        line = raw_line.strip()
	if line in ["===========","----		 ------		 -----------	 -------", \
		    "Slot		 Source		 Reading    	 Level",""]:
	    continue
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
	regList = ['(?P<label>.*):','^(?P<slot>[a-zA-Z-0-9]{1,8})\s+(?P<source>[a-zA-Z-0-9\. \-]{1,15})\s+(?P<reading>[a-zA-Z-0-9\. ]{1,11})$','(?P<slot>[a-zA-Z-0-9]{1,8})\s+(?P<source>[a-zA-Z-0-9\. \-]{1,15})\s+(?P<reading>[a-zA-Z-0-9\. ]{1,11})\s+(?P<level>[\w]{1,7})']
    	pList = [re.compile(regexp) for regexp in regList] 
	mList = [p.search(line) for p in pList] 
       	if debug:
            print 'The mList is:', mList
	local_dict = {}
	
	if curname != "":
	    name = curname
	for m in mList:
	    if m == None:
		continue
	    dict = m.groupdict()
       	    if debug:
                print 'The dict is:', dict
	    for key in dict.keys():
       		if debug:
            	    print 'The key is:', key
		if key == "label":
		    curname = dict['label'].strip()
		    name = curname
		    isName = True
       		    if debug:
            		print 'The name is:', name
		elif (key == "slot") or (key == "source"):
            	    print 'The name is:', name
            	    print 'dict[%s] is %s' %(key,dict[key])
		    name = '%s - %s' %(name,dict[key].strip())
		    isName = True
       		    if debug:
            		print 'The name is:', name
		else:
		    local_dict[key] = dict[key]
		    isName = False
            	    if debug:
                	print("The %s is: %s " %(key,local_dict[key]))
	    break		     		
    	# We store last entry in the main dictionary we return
	if not isName:
	    environmentalDetail_dict[name] = local_dict
 
    return environmentalDetail_dict
    
    
def show_process_memory(self,slot='0'):
    """Runs the command 'show process mem slot <slot>' and parses the output.
       Default slot is 0 
    """
    processMem_dict = {}
    debug = False
    
    # Sample raw input
    """
    iceland[local]#show process mem
    Process Name  PID     Text    Data    soText  soData  Stack   Heap    Shared
    ------------- ------- ------- ------- ------- ------- ------- ------- ------- 
    NSM            704514 16KB    4096    8MB     1192KB  156KB   17MB    249MB
    Smid           745496 224KB   16KB    12MB    3256KB  128KB   2504KB  21MB
    Ip             745500 4096    4096    8MB     2028KB  188KB   4928KB  260MB
    CtxMgr         745499 36KB    4096    7492KB  868KB   76KB    1268KB  21MB
    Fpd            745498 32KB    8192    7616KB  900KB   92KB    1300KB  243MB
    Aaad           745504 424KB   84KB    13MB    1312KB  204KB   5432KB  132MB
    Cli            925743 44KB    16KB    12MB    3272KB  120KB   2600KB  21MB
    Cli           1011760 44KB    16KB    12MB    3272KB  120KB   2600KB  21MB
    Snmpd          745506 604KB   52KB    7680KB  912KB   80KB    2324KB  22MB
    Inets          745505 32KB    8192    8MB     1056KB  112KB   1304KB  21MB
    Logind         745497 16KB    4096    7628KB  924KB   80KB    1268KB  21MB
    Logind        1011758 16KB    4096    7628KB  924KB   80KB    1268KB  21MB
    Ospf           745501 332KB   8192    8000KB  952KB   88KB    1304KB  38MB
    Bgp4           745502 320KB   8192    8020KB  960KB   96KB    1468KB  38MB
    Evl            745493 108KB   4096    7828KB  920KB   92KB    1272KB  25MB
    EvlColl        745494 36KB    4096    7508KB  876KB   76KB    1300KB  25MB
    Qosd           745503 180KB   4096    9MB     1108KB  92KB    1304KB  127MB
    IkedMc         745507 152KB   68KB    8MB     1004KB  88KB    1300KB  21MB
    Ntp            745508 4096    4096    8076KB  1188KB  92KB    1300KB  21MB
    Rip            745509 96KB    8192    7736KB  928KB   88KB    1268KB  38MB
    Evt            745492 32KB    4096    7492KB  868KB   76KB    1268KB  21MB
    Fsync          745495 20KB    4096    7408KB  868KB   72KB    1332KB  20MB
    TunMgr         745510 112KB   4096    7540KB  876KB   84KB    1304KB  23MB
    CDR            745511 112KB   8192    9MB     1076KB  100KB   1304KB  122MB
    DHCPdMC        745512 48KB    1028KB  7600KB  900KB   80KB    1268KB  21MB
    MIPd           745513 160KB   4096    7768KB  1952KB  96KB    2360KB  21MB
    SLA            745514 32KB    4096    7664KB  900KB   76KB    1272KB  21MB
    Dfn            745515 1172KB  4096    10MB    1072KB  92KB    13MB    21MB
    Gtppd          745516 52KB    4096    9MB     1100KB  84KB    1380KB  122MB
    iceland[local]#

    Sample dictionary output:
    =========================
    {
    'Aaad': {   'Data': '84KB',
                'Heap': '5432KB',
                'PID': '745504',
                'Shared': '132MB',
                'Stack': '204KB',
                'Text': '424KB',
                'soData': '1312KB',
                'soText': '13MB'},
    'Bgp4': {   'Data': '8192',
                'Heap': '1468KB',
                'PID': '745502',
                'Shared': '38MB',
                'Stack': '96KB',
                'Text': '320KB',
                'soData': '960KB',
                'soText': '8020KB'},
    'CDR': {   'Data': '8192',
               'Heap': '1304KB',
               'PID': '745511',
               'Shared': '122MB',
               'Stack': '100KB',
               'Text': '112KB',
               'soData': '1076KB',
               'soText': '9MB'},
    'Cli': {   'Data': '16KB',
               'Heap': '2600KB',
               'PID': '925743',
               'Shared': '21MB',
               'Stack': '120KB',
               'Text': '44KB',
               'soData': '3272KB',
               'soText': '12MB'},
    'Cli_1': {   'Data': '16KB',
                 'Heap': '2600KB',
                 'PID': '1011760',
                 'Shared': '21MB',
                 'Stack': '120KB',
                 'Text': '44KB',
                 'soData': '3272KB',
                 'soText': '12MB'},
    'Cli_2': {   'Data': '16KB',
                 'Heap': '2600KB',
                 'PID': '1011763',
                 'Shared': '21MB',
                 'Stack': '140KB',
                 'Text': '44KB',
                 'soData': '3272KB',
                 'soText': '12MB'},
    'CtxMgr': {   'Data': '4096',
                  'Heap': '1268KB',
                  'PID': '745499',
                  'Shared': '21MB',
                  'Stack': '80KB',
                  'Text': '36KB',
                  'soData': '868KB',
                  'soText': '7492KB'},
    'DHCPdMC': {   'Data': '1028KB',
                   'Heap': '1268KB',
                   'PID': '745512',
                   'Shared': '21MB',
                   'Stack': '80KB',
                   'Text': '48KB',
                   'soData': '900KB',
                   'soText': '7600KB'},
    'Dfn': {   'Data': '4096',
               'Heap': '13MB',
               'PID': '745515',
               'Shared': '21MB',
               'Stack': '92KB',
               'Text': '1172KB',
               'soData': '1072KB',
               'soText': '10MB'},
    'Evl': {   'Data': '4096',
               'Heap': '1272KB',
               'PID': '745493',
               'Shared': '25MB',
               'Stack': '92KB',
               'Text': '108KB',
               'soData': '920KB',
               'soText': '7828KB'},
    'EvlColl': {   'Data': '4096',
                   'Heap': '1300KB',
                   'PID': '745494',
                   'Shared': '25MB',
                   'Stack': '76KB',
                   'Text': '36KB',
                   'soData': '876KB',
                   'soText': '7508KB'},
    'Evt': {   'Data': '4096',
               'Heap': '1268KB',
               'PID': '745492',
               'Shared': '21MB',
               'Stack': '80KB',
               'Text': '32KB',
               'soData': '868KB',
               'soText': '7492KB'},
    'Fpd': {   'Data': '8192',
               'Heap': '1300KB',
               'PID': '745498',
               'Shared': '243MB',
               'Stack': '92KB',
               'Text': '32KB',
               'soData': '900KB',
               'soText': '7616KB'},
    'Fsync': {   'Data': '4096',
                 'Heap': '1332KB',
                 'PID': '745495',
                 'Shared': '20MB',
                 'Stack': '72KB',
                 'Text': '20KB',
                 'soData': '868KB',
                 'soText': '7408KB'},
    'Gtppd': {   'Data': '4096',
                 'Heap': '1380KB',
                 'PID': '745516',
                 'Shared': '122MB',
                 'Stack': '84KB',
                 'Text': '52KB',
                 'soData': '1100KB',
                 'soText': '9MB'},
    'IkedMc': {   'Data': '68KB',
                  'Heap': '1300KB',
                  'PID': '745507',
                  'Shared': '21MB',
                  'Stack': '88KB',
                  'Text': '152KB',
                  'soData': '1004KB',
                  'soText': '8MB'},
    'Inets': {   'Data': '8192',
                 'Heap': '1304KB',
                 'PID': '745505',
                 'Shared': '21MB',
                 'Stack': '116KB',
                 'Text': '32KB',
                 'soData': '1056KB',
                 'soText': '8MB'},
    'Ip': {   'Data': '4096',
              'Heap': '4932KB',
              'PID': '745500',
              'Shared': '260MB',
              'Stack': '188KB',
              'Text': '4096',
              'soData': '2028KB',
              'soText': '8MB'},
    'Logind': {   'Data': '4096',
                  'Heap': '1268KB',
                  'PID': '745497',
                  'Shared': '21MB',
                  'Stack': '80KB',
                  'Text': '16KB',
                  'soData': '924KB',
                  'soText': '7628KB'},
    'Logind_1': {   'Data': '4096',
                    'Heap': '1268KB',
                    'PID': '1011758',
                    'Shared': '21MB',
                    'Stack': '80KB',
                    'Text': '16KB',
                    'soData': '924KB',
                    'soText': '7628KB'},
    'Logind_2': {   'Data': '4096',
                    'Heap': '1268KB',
                    'PID': '1011762',
                    'Shared': '21MB',
                    'Stack': '100KB',
                    'Text': '16KB',
                    'soData': '924KB',
                    'soText': '7628KB'},
    'MIPd': {   'Data': '4096',
                'Heap': '2360KB',
                'PID': '745513',
                'Shared': '21MB',
                'Stack': '96KB',
                'Text': '160KB',
                'soData': '1952KB',
                'soText': '7768KB'},
    'NSM': {   'Data': '4096',
               'Heap': '17MB',
               'PID': '704514',
               'Shared': '249MB',
               'Stack': '160KB',
               'Text': '16KB',
               'soData': '1192KB',
               'soText': '8MB'},
    'Ntp': {   'Data': '4096',
               'Heap': '1300KB',
               'PID': '745508',
               'Shared': '21MB',
               'Stack': '92KB',
               'Text': '4096',
               'soData': '1188KB',
               'soText': '8076KB'},
    'Ospf': {   'Data': '8192',
                'Heap': '1304KB',
                'PID': '745501',
                'Shared': '38MB',
                'Stack': '88KB',
                'Text': '332KB',
                'soData': '952KB',
                'soText': '8000KB'},
    'Qosd': {   'Data': '4096',
                'Heap': '1304KB',
                'PID': '745503',
                'Shared': '127MB',
                'Stack': '92KB',
                'Text': '180KB',
                'soData': '1108KB',
                'soText': '9MB'},
    'Rip': {   'Data': '8192',
               'Heap': '1268KB',
               'PID': '745509',
               'Shared': '38MB',
               'Stack': '88KB',
               'Text': '96KB',
               'soData': '928KB',
               'soText': '7736KB'},
    'SLA': {   'Data': '4096',
               'Heap': '1272KB',
               'PID': '745514',
               'Shared': '21MB',
               'Stack': '76KB',
               'Text': '32KB',
               'soData': '900KB',
               'soText': '7664KB'},
    'Smid': {   'Data': '16KB',
                'Heap': '2504KB',
                'PID': '745496',
                'Shared': '21MB',
                'Stack': '132KB',
                'Text': '224KB',
                'soData': '3256KB',
                'soText': '12MB'},
    'Snmpd': {   'Data': '52KB',
                 'Heap': '2324KB',
                 'PID': '745506',
                 'Shared': '22MB',
                 'Stack': '80KB',
                 'Text': '604KB',
                 'soData': '912KB',
                 'soText': '7680KB'},
    'TunMgr': {   'Data': '4096',
                  'Heap': '1304KB',
                  'PID': '745510',
                  'Shared': '23MB',
                  'Stack': '84KB',
                  'Text': '112KB',
                  'soData': '876KB',
                  'soText': '7540KB'}}

    """

    command = "show process mem slot %s" %slot
    raw_processMem_list = self.cmd(command)
    processMem_list = raw_processMem_list.splitlines()
    if debug:
        print 'The raw value returned was:'
        print processMem_list

    if ('ERROR:' in raw_processMem_list):
        print 'Detected an error when running: ' + command
        print 'Returned text was:'
        print raw_processMem_list
        processMem_dict['Status'] = 'Error'
        return processMem_dict


    labels_line = processMem_list[1]
    divider_line = processMem_list[2]
    columnDict = parse_divider_line(self,divider_line)
    dupKey_dict = {}
    for raw_line in processMem_list[3:]:
        line = raw_line.strip()
        if debug:
            print '----------------------------------------------'
            print 'The line to be processed is:'
            print line
    	start = columnDict[0][0]
    	end = columnDict[0][1]+1
    	name = line[start:end].strip()
	if name in dupKey_dict:
	    # for duplicate keys, append the index to the key to differentiate between them
	    dupKey_dict[name] += 1
	    name = name + "_" + `dupKey_dict[name]`	
    	else:
	    dupKey_dict[name] = 0
        if debug:
            print 'The name is:', name
	local_dict = {}
	for idx in range(1,len(columnDict.keys())):
	    start = columnDict[idx][0]
    	    end = columnDict[idx][1]+1
	    labels_name = labels_line[start:end].strip()
    	    local_dict[labels_name] = line[start:end].strip()
            if debug:
               	print("The %s is: %s " %(labels_name,local_dict[labels_name]))
	# We store last entry in the main dictionary we return
	processMem_dict[name] = local_dict
 
    return processMem_dict
   

def showmoduleprocessmashared(self,slot):

    showmodprocmashared_dict = {}
    debug = False
    # Sample raw input
    """
    Stoke[local]#show module Rip slot 0 ma shared
    Name/            Elements  HiWat/    In Use/   Allocs/       Alloc Fail/
     Pool Size       Elem Size User Size Free      Frees         Double Free
    ---------------- --------- --------- --------- ------------- -----------
    MBuf                97,340    48,463    47,543        60,251           0
         211,812,352     2,176     2,144    49,797        12,708           0
    FpdPage              4,964        13        13            13           0
          20,971,520     4,224     4,192     4,951             0           0
    RouteMap             1,351         0         0             0           0
           3,145,728     2,328     2,320     1,351             0           0
    PfxList              6,553         0         0             0           0
             524,288        80        72     6,553             0           0
    CommList             9,361         0         0             0           0
             524,288        56        48     9,361             0           0
    UI32Array            5,957         0         0             0           0
             524,288        88        80     5,957             0           0
    AsPathAcl           13,106         0         0             0           0
             524,288        40        32    13,106             0           0
    RtPolRegex200       20,164         0         0             0           0
           4,194,304       208       200    20,164             0           0
    RtPolRegex400       10,280         0         0             0           0
           4,194,304       408       400    10,280             0           0
    RtPolRegex512        6,898         0         0             0           0
           4,194,304       608       600     6,898             0           0
    Stoke[local]# 
    # Sample output
     'Rip': {   'AsPathAcl': {   'Alloc Fail': '0',
                                'Allocs': '0',
                                'Double Free': '0',
                                'Elem Size': '40',
                                'Elements': '13,106',
                                'Free': '13,106',
                                'Frees': '0',
                                'HiWat': '0',
                                'In Use': '0',
                                'Pool Size': '524,288',
                                'User Size': '32'},
               'CommList': {   'Alloc Fail': '0',
                               'Allocs': '0',
                               'Double Free': '0',
                               'Elem Size': '56',
                               'Elements': '9,361',
                               'Free': '9,361',
                               'Frees': '0',
                               'HiWat': '0',
                               'In Use': '0',
                               'Pool Size': '524,288',
                               'User Size': '48'},
               'FpdPage': {   'Alloc Fail': '0',
                              'Allocs': '13',
                              'Double Free': '0',
                              'Elem Size': '4,224',
                              'Elements': '4,964',
                              'Free': '4,951',
                              'Frees': '0',
                              'HiWat': '13',
                              'In Use': '13',
                              'Pool Size': '20,971,520',
                              'User Size': '4,192'},
               'MBuf': {   'Alloc Fail': '0',
                           'Allocs': '60,251',
                           'Double Free': '0',
                           'Elem Size': '2,176',
                           'Elements': '97,340',
                           'Free': '49,797',
                           'Frees': '12,708',
                           'HiWat': '48,463',
                           'In Use': '47,543',
                           'Pool Size': '211,812,352',
                           'User Size': '2,144'},
               'PfxList': {   'Alloc Fail': '0',
                              'Allocs': '0',
                              'Double Free': '0',
                              'Elem Size': '80',
                              'Elements': '6,553',
                              'Free': '6,553',
                              'Frees': '0',
                              'HiWat': '0',
                              'In Use': '0',
                              'Pool Size': '524,288',
                              'User Size': '72'},
               'RouteMap': {   'Alloc Fail': '0',
                               'Allocs': '0',
                               'Double Free': '0',
                               'Elem Size': '2,328',
                               'Elements': '1,351',
                               'Free': '1,351',
                               'Frees': '0',
                               'HiWat': '0',
                               'In Use': '0',
                               'Pool Size': '3,145,728',
                               'User Size': '2,320'},
               'RtPolRegex200': {   'Alloc Fail': '0',
                                    'Allocs': '0',
                                    'Double Free': '0',
                                    'Elem Size': '208',
                                    'Elements': '20,164',
                                    'Free': '20,164',
                                    'Frees': '0',
                                    'HiWat': '0',
                                    'In Use': '0',
                                    'Pool Size': '4,194,304',
                                    'User Size': '200'},
               'RtPolRegex400': {   'Alloc Fail': '0',
                                    'Allocs': '0',
                                    'Double Free': '0',
                                    'Elem Size': '408',
                                    'Elements': '10,280',
                                    'Free': '10,280',
                                    'Frees': '0',
                                    'HiWat': '0',
                                    'In Use': '0',
                                    'Pool Size': '4,194,304',
                                    'User Size': '400'},
               'RtPolRegex512': {   'Alloc Fail': '0',
                                    'Allocs': '0',
                                    'Double Free': '0',
                                    'Elem Size': '608',
                                    'Elements': '6,898',
                                    'Free': '6,898',
                                    'Frees': '0',
                                    'HiWat': '0',
                                    'In Use': '0',
                                    'Pool Size': '4,194,304',
                                    'User Size': '600'},
               'UI32Array': {   'Alloc Fail': '0',
                                'Allocs': '0',
                                'Double Free': '0',
                                'Elem Size': '88',
                                'Elements': '5,957',
                                'Free': '5,957',
                                'Frees': '0',
                                'HiWat': '0',
                                'In Use': '0',
                                'Pool Size': '524,288',
                                'User Size': '80'}} 
 
    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue

        command = "show module %s slot %s ma shared" %(process,slot)
        raw_modslotmashared_list = self.cmd(command)
        if ('ERROR:' in raw_modslotmashared_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotmashared_list
            showmodprocmashared_dict[process] = {'Error':raw_modslotmashared_list.strip()}
            continue
        elif raw_modslotmashared_list == "":
            # no output.  Give out warning and continue on
            print "Command %s shows no output" %command
            continue


        modslotmashared_list = raw_modslotmashared_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotmashared_list

        labels_line1 = modslotmashared_list[1]
        labels_line2 = modslotmashared_list[2]
    	divider_line = modslotmashared_list[3]
	numcol = len(divider_line.split())
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
    
	temp_dict = {} 
	linenum = 4
        for raw_line in modslotmashared_list[4:]:
            line = raw_line 
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
	
	    if linenum % 2 == 0:
		# even line number
                local_dict = {}
            	start = columnDict[0][0]
            	end = columnDict[0][1]+1
                name = line[start:end].strip()
		startrange = 1
		labels_line = labels_line1
	    else:
		startrange = 0
		labels_line = labels_line2
            for labels_idx in range(startrange,numcol):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
		label_name = labels_line[start:end].strip(' /')
                local_dict[label_name] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(labels_line[label_name],local_dict[labels_line[label_name]]))

            # We store each entry in the temp dictionary
	    # odd line we save
	    if  linenum % 2 == 1:
                temp_dict[name] = local_dict
	    linenum += 1
        # We store each temp dictionary to process
        showmodprocmashared_dict[process] = temp_dict

    return showmodprocmashared_dict

def showmoduleprocessmapool(self,slot):

    showmodprocmapool_dict = {}
    debug = False
    # Sample raw input
    """
    Stoke[local]#show module NSM slot 2 ma pool
    Name             Size          InUse     Free      Allocs        Frees
    ---------------- ------------- --------- --------- ------------- -------------
    DaSet                      128        27         8            27             0
    DaJudy                      40        57        15           261           204
    DaJudy                      72         2        33            21            19
    DaJudy                     136         2        31            16            14
    DaJudy                     264         6        38             8             2
    CrhHandleData               60         5        35             5             0
    CrhRegData                  32        21        22            21             0
    CrhCmdBlk                8,224         4         4            21            17
    NvTimer                     56        19        24            20             1
    IpcConnIds                  28        20        28            20             0
    IpcArepIds                  28         4        44             4             0
    IpcReg                     156         4        31             4             0
    IpcConn                    400        20        19            20             0
    IpcRegmsg                    8        11        17            11             0
    IpcAsyncReply              344         4        12             4             0
    IpcSndrArep                 36         3        15             3             0
    IpcThrEnt                   36         0        18            12            12
    IpcThrData                  28         0        22           118           118
    IpcRmReg                    24         4        49             4             0
    IpcRmInfo                   36         1       145           110           109
    IpcAmInfo                   72         0       144            44            44
    MsgVerPool                 176         2        19             2             0
    IpcTrWantReg                28         4        44             4             0
    IpcTrRegac                  76        30         3            30             0
    IpcTrRegpc                  72        23        12            23             0
    IpcTrReg                    84         4        37             4             0
    IpcTrConn                  388        20        20            20             0
    IpcTrConnG                 188        15        20            15             0
    IpcTrSlot                   64        19        19            19             0
    IpcTrNode                  112        39        25            39             0
    IpcTrRegacI                 28        30        18            30             0
    IpcTrRegpcI                 28        23        25            23             0
    IpcTrCgIds                  28        15        33            15             0
    IpcPeer                     48        17        15            17             0
    IpcPeerMsgData              80         0        20           118           118
    IpcPeerMsg                  56         0        28           118           118
    IpcQnxReg                   80         4        28             4             0
    IpcQnxConn                  12        12        48            12             0
    IpcTcpReg                   52         4        42             4             0
    IpcTcpConn                  16         6        54             6             0
    IpcTcpRegpc                104        23        11            23             0
    IpcMsgReg                   52         4        42             4             0
    IpcMsgConn                 124        24        12            24             0
    NvMsg                    8,300         2        30           743           741
    EvtStateNotify              32         4        16             4             0
    EvtCrhCallBack               8         0        28             9             9
    EvtRegWait                  40         0        17             4             4
    H:CMOHandler                20         3       153             3             0
    H:CMOHandler                20         7       149             7             0
    H:CMOHandler                20        28       128            28             0
    H:CMOHandler                20         1       155             1             0
    CMOHandlerPool              12        39     2,005            39             0
    CMOObjectPool            8,080         0        64             2             2
    IpcMbType                   36         0        18             1             1
    IpcMbMsg                    36         0        40             2             2
    NvfuCdpipcInfo              48         1       133            16            15
    cdpipc                      72         0       534        48,471        48,471
    cdpipc                     264         0       518            32            32
    cdpipc                   1,460         1       352        48,502        48,501
    CardAgt I2C Job             28         0        73           404           404
    ProcMgrNPE                 680        15        20            15             0
    NPE/NSE                    188         7        28             7             0
    PWQ                        112         0        32             7             7
    ProcMgr Mon Eve             28         0        22       218,278       218,278
    64 objects displayed.
    Stoke[local]#
    # Sample output
     'NSM': {   '68 objects displ': {   'Allocs': '',
                                       'Free': '',
                                       'Frees': '',
                                       'InUse': '',
                                       'Size': 'yed.'},
               'CMOHandlerPool': {   'Allocs': '104',
                                     'Free': '1,940',
                                     'Frees': '0',
                                     'InUse': '104',
                                     'Size': '12'},
               'CMOObjectPool': {   'Allocs': '204',
                                    'Free': '64',
                                    'Frees': '204',
                                    'InUse': '0',
                                    'Size': '8,080'},
               'CardMgr I2C Job': {   'Allocs': '427,449',
                                      'Free': '72',
                                      'Frees': '427,448',
                                      'InUse': '1',
                                      'Size': '28'},
               'CrhCmdBlk': {   'Allocs': '9',
                                'Free': '8',
                                'Frees': '1',
                                'InUse': '8',
                                'Size': '8,224'},
               'CrhHandleData': {   'Allocs': '8',
                                    'Free': '32',
                                    'Frees': '0',
                                    'InUse': '8',
                                    'Size': '60'},
               'CrhRegData': {   'Allocs': '20',
                                 'Free': '23',
                                 'Frees': '0',
                                 'InUse': '20',
                                 'Size': '32'},
               'DaJudy': {   'Allocs': '1,310',
                             'Free': '18',
                             'Frees': '1,112',
                             'InUse': '198',
                             'Size': '40'},
               'DaJudy_2': {   'Allocs': '105',
                               'Free': '3',
                               'Frees': '73',
                               'InUse': '32',
                               'Size': '72'},
               'DaJudy_4': {   'Allocs': '73',
                               'Free': '20',
                               'Frees': '60',
                               'InUse': '13',
                               'Size': '136'},
               'DaJudy_8': {   'Allocs': '31',
                               'Free': '42',
                               'Frees': '29',
                               'InUse': '2',
                               'Size': '264'},
               'DaSet': {   'Allocs': '49',
                            'Free': '21',
                            'Frees': '0',
                            'InUse': '49',
                            'Size': '128'},
               'EvtCrhCallBack': {   'Allocs': '171',
                                     'Free': '28',
                                     'Frees': '171',
                                     'InUse': '0',
                                     'Size': '8'},
               'EvtRegWait': {   'Allocs': '7',
                                 'Free': '17',
                                 'Frees': '7',
                                 'InUse': '0',
                                 'Size': '40'},
               'EvtStateNotify': {   'Allocs': '7',
                                     'Free': '13',
                                     'Frees': '0',
                                     'InUse': '7',
                                     'Size': '32'},
               'H:CMOHandler': {   'Allocs': '12',
                                   'Free': '144',
                                   'Frees': '0',
                                   'InUse': '12',
                                   'Size': '20'},
               'H:CMOHandler_128': {   'Allocs': '1',
                                       'Free': '155',
                                       'Frees': '0',
                                       'InUse': '1',
                                       'Size': '20'},
               'H:CMOHandler_16': {   'Allocs': '31',
                                      'Free': '125',
                                      'Frees': '0',
                                      'InUse': '31',
                                      'Size': '20'},
               'H:CMOHandler_2': {   'Allocs': '14',
                                     'Free': '142',
                                     'Frees': '0',
                                     'InUse': '14',
                                     'Size': '20'},
               'H:CMOHandler_32': {   'Allocs': '12',
                                      'Free': '144',
                                      'Frees': '0',
                                      'InUse': '12',
                                      'Size': '20'},
               'H:CMOHandler_4': {   'Allocs': '4',
                                     'Free': '152',
                                     'Frees': '0',
                                     'InUse': '4',
                                     'Size': '20'},
               'H:CMOHandler_64': {   'Allocs': '8',
                                      'Free': '148',
                                      'Frees': '0',
                                      'InUse': '8',
                                      'Size': '20'},
               'H:CMOHandler_8': {   'Allocs': '22',
                                     'Free': '134',
                                     'Frees': '0',
                                     'InUse': '22',
                                     'Size': '20'},
               'HAMgrVRISet': {   'Allocs': '2',
                                  'Free': '20',
                                  'Frees': '0',
                                  'InUse': '2',
                                  'Size': '28'},
               'IpcAmInfo': {   'Allocs': '139',
                                'Free': '144',
                                'Frees': '139',
                                'InUse': '0',
                                'Size': '72'},
               'IpcArepIds': {   'Allocs': '22',
                                 'Free': '29',
                                 'Frees': '3',
                                 'InUse': '19',
                                 'Size': '28'},
               'IpcAsyncReply': {   'Allocs': '22',
                                    'Free': '13',
                                    'Frees': '3',
                                    'InUse': '19',
                                    'Size': '344'},
               'IpcConn': {   'Allocs': '103',
                              'Free': '37',
                              'Frees': '23',
                              'InUse': '80',
                              'Size': '400'},
               'IpcConnIds': {   'Allocs': '103',
                                 'Free': '14',
                                 'Frees': '21',
                                 'InUse': '82',
                                 'Size': '28'},
               'IpcMbMsg': {   'Allocs': '3',
                               'Free': '40',
                               'Frees': '3',
                               'InUse': '0',
                               'Size': '36'},
               'IpcMbType': {   'Allocs': '2',
                                'Free': '18',
                                'Frees': '2',
                                'InUse': '0',
                                'Size': '36'},
               'IpcMsgConn': {   'Allocs': '125',
                                 'Free': '9',
                                 'Frees': '26',
                                 'InUse': '99',
                                 'Size': '124'},
               'IpcMsgReg': {   'Allocs': '7',
                                'Free': '39',
                                'Frees': '0',
                                'InUse': '7',
                                'Size': '52'},
               'IpcPeer': {   'Allocs': '56',
                              'Free': '8',
                              'Frees': '0',
                              'InUse': '56',
                              'Size': '48'},
               'IpcPeerMsg': {   'Allocs': '458',
                                 'Free': '28',
                                 'Frees': '458',
                                 'InUse': '0',
                                 'Size': '56'},
               'IpcPeerMsgData': {   'Allocs': '452',
                                     'Free': '20',
                                     'Frees': '452',
                                     'InUse': '0',
                                     'Size': '80'},
               'IpcQnxConn': {   'Allocs': '59',
                                 'Free': '24',
                                 'Frees': '23',
                                 'InUse': '36',
                                 'Size': '12'},
               'IpcQnxReg': {   'Allocs': '7',
                                'Free': '25',
                                'Frees': '0',
                                'InUse': '7',
                                'Size': '80'},
               'IpcReg': {   'Allocs': '7',
                             'Free': '28',
                             'Frees': '0',
                             'InUse': '7',
                             'Size': '156'},
               'IpcRegmsg': {   'Allocs': '14',
                                'Free': '14',
                                'Frees': '0',
                                'InUse': '14',
                                'Size': '8'},
               'IpcRmInfo': {   'Allocs': '687',
                                'Free': '145',
                                'Frees': '686',
                                'InUse': '1',
                                'Size': '36'},
               'IpcRmReg': {   'Allocs': '7',
                               'Free': '46',
                               'Frees': '0',
                               'InUse': '7',
                               'Size': '24'},
               'IpcSndrArep': {   'Allocs': '5',
                                  'Free': '13',
                                  'Frees': '0',
                                  'InUse': '5',
                                  'Size': '36'},
               'IpcTcpConn': {   'Allocs': '19',
                                 'Free': '44',
                                 'Frees': '3',
                                 'InUse': '16',
                                 'Size': '16'},
               'IpcTcpReg': {   'Allocs': '7',
                                'Free': '39',
                                'Frees': '0',
                                'InUse': '7',
                                'Size': '52'},
               'IpcTcpRegpc': {   'Allocs': '85',
                                  'Free': '9',
                                  'Frees': '26',
                                  'InUse': '59',
                                  'Size': '104'},
               'IpcThrData': {   'Allocs': '477',
                                 'Free': '22',
                                 'Frees': '477',
                                 'InUse': '0',
                                 'Size': '28'},
               'IpcThrEnt': {   'Allocs': '38',
                                'Free': '18',
                                'Frees': '38',
                                'InUse': '0',
                                'Size': '36'},
               'IpcTrCgIds': {   'Allocs': '75',
                                 'Free': '42',
                                 'Frees': '21',
                                 'InUse': '54',
                                 'Size': '28'},
               'IpcTrConn': {   'Allocs': '103',
                                'Free': '40',
                                'Frees': '23',
                                'InUse': '80',
                                'Size': '388'},
               'IpcTrConnG': {   'Allocs': '75',
                                 'Free': '18',
                                 'Frees': '23',
                                 'InUse': '52',
                                 'Size': '188'},
               'IpcTrNode': {   'Allocs': '99',
                                'Free': '20',
                                'Frees': '23',
                                'InUse': '76',
                                'Size': '112'},
               'IpcTrReg': {   'Allocs': '7',
                               'Free': '34',
                               'Frees': '0',
                               'InUse': '7',
                               'Size': '84'},
               'IpcTrRegac': {   'Allocs': '115',
                                 'Free': '13',
                                 'Frees': '29',
                                 'InUse': '86',
                                 'Size': '76'},
               'IpcTrRegacI': {   'Allocs': '115',
                                  'Free': '10',
                                  'Frees': '29',
                                  'InUse': '86',
                                  'Size': '28'},
               'IpcTrRegpc': {   'Allocs': '85',
                                 'Free': '11',
                                 'Frees': '26',
                                 'InUse': '59',
                                 'Size': '72'},
               'IpcTrRegpcI': {   'Allocs': '85',
                                  'Free': '37',
                                  'Frees': '26',
                                  'InUse': '59',
                                  'Size': '28'},
               'IpcTrSlot': {   'Allocs': '79',
                                'Free': '20',
                                'Frees': '23',
                                'InUse': '56',
                                'Size': '64'},
               'IpcTrWantReg': {   'Allocs': '3',
                                   'Free': '45',
                                   'Frees': '0',
                                   'InUse': '3',
                                   'Size': '28'},
               'MsgVerPool': {   'Allocs': '3',
                                 'Free': '18',
                                 'Frees': '0',
                                 'InUse': '3',
                                 'Size': '176'},
               'NPE/NSE': {   'Allocs': '31',
                              'Free': '25',
                              'Frees': '21',
                              'InUse': '10',
                              'Size': '188'},
               'NSMClientSrvr': {   'Allocs': '3',
                                    'Free': '137',
                                    'Frees': '0',
                                    'InUse': '3',
                                    'Size': '104'},
               'NvMsg': {   'Allocs': '6,927',
                            'Free': '30',
                            'Frees': '6,925',
                            'InUse': '2',
                            'Size': '8,300'},
               'NvTimer': {   'Allocs': '35',
                              'Free': '24',
                              'Frees': '16',
                              'InUse': '19',
                              'Size': '56'},
               'PWQ': {   'Allocs': '31',
                          'Free': '31',
                          'Frees': '30',
                          'InUse': '1',
                          'Size': '112'},
               'ProcMgr Mon Eve': {   'Allocs': '116,642',
                                      'Free': '22',
                                      'Frees': '116,642',
                                      'InUse': '0',
                                      'Size': '28'},
               'ProcMgrNPE': {   'Allocs': '56',
                                 'Free': '0',
                                 'Frees': '21',
                                 'InUse': '35',
                                 'Size': '680'},
               'evt notify_wait': {   'Allocs': '105',
                                      'Free': '1,071',
                                      'Frees': '105',
                                      'InUse': '0',
                                      'Size': '72'},
               'evt notify_wait_2': {   'Allocs': '4',
                                        'Free': '133',
                                        'Frees': '4',
                                        'InUse': '0',
                                        'Size': '264'}} 
 
    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue

        command = "show module %s slot %s ma pool" %(process,slot)
        raw_modslotmapool_list = self.cmd(command)
        modslotmapool_list = raw_modslotmapool_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotmapool_list

        if ('ERROR:' in raw_modslotmapool_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotmapool_list
            showmodprocmapool_dict[process] = {'Error':raw_modslotmapool_list.strip()}
            continue
        elif raw_modslotmapool_list == "":
            # no output.  Give out warning and continue on
            print "Command %s shows no output" %command
            continue

        labels_line = modslotmapool_list[1].split()
    	divider_line = modslotmapool_list[2]
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
    
	name_dict = {}       
	temp_dict = {} 
        for raw_line in modslotmapool_list[3:-1]:
            line = raw_line
            local_dict = {}
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
            start = columnDict[0][0]
            end = columnDict[0][1]+1
            name = line[start:end].strip()
	    if name in name_dict.keys():
		name_dict[name] += 1
		name = name + "_" + str(name_dict[name])
	    else:
		name_dict[name] = 0
            for labels_idx in range(1,len(labels_line)):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
                local_dict[labels_line[labels_idx]] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
            # We store each entry in the temp dictionary
            temp_dict[name] = local_dict
        # We store each temp dictionary to process
        showmodprocmapool_dict[process] = temp_dict

    return showmodprocmapool_dict

def showmoduleprocessmapp(self,slot):

    showmodprocmapp_dict = {}
    debug = False
    # Sample raw input
    """
    Stoke[local]#show module NSM slot 2 ma pp
                                   Elem__________________________________
    Name                           Size     InUse     Allocs    Frees     Blocks
    ------------------------------ -------- --------- --------- --------- ---------
    _global_                              0         0         8         0         0
    HALibHAPP::0                        396         0         0         0         1
    HALibHAGlobCB::0                    204         0         0         0         1
    HALibAsyncCB::0                      60         0         0         0         1
    Stoke[local]#
    # Sample output
  
    'NSM': {   'GlcLSstats:16::0': {   'Allocs': '2',
                                       'Blocks': '1',
                                       'Frees': '0',
                                       'InUse': '2',
                                       'Size': '168'},
               'HALibAsyncCB::0': {   'Allocs': '17',
                                      'Blocks': '0',
                                      'Frees': '17',
                                      'InUse': '0',
                                      'Size': '60'},
               'HALibHAGlobCB::0': {   'Allocs': '2',
                                       'Blocks': '1',
                                       'Frees': '0',
                                       'InUse': '2',
                                       'Size': '204'},
               'HALibHAPP::0': {   'Allocs': '1',
                                   'Blocks': '1',
                                   'Frees': '0',
                                   'InUse': '1',
                                   'Size': '396'},
               '_global_': {   'Allocs': '12',
                               'Blocks': '0',
                               'Frees': '0',
                               'InUse': '0',
                               'Size': '0'}},
 
    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue

        command = "show module %s slot %s ma pp" %(process,slot)
        raw_modslotmapp_list = self.cmd(command)
        modslotmapp_list = raw_modslotmapp_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotmapp_list

        if ('ERROR:' in raw_modslotmapp_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotmapp_list
            showmodprocmapp_dict[process] = {'Error':raw_modslotmapp_list.strip()}
	    continue
	elif raw_modslotmapp_list == "":
	    # no output.  Give out warning and continue on
	    print "Command %s shows no output" %command
	    continue	

        labels_line = modslotmapp_list[2].split()
    	divider_line = modslotmapp_list[3]
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
           
	temp_dict = {} 
        for raw_line in modslotmapp_list[4:]:
            line = raw_line 
            local_dict = {}
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
            start = columnDict[0][0]
            end = columnDict[0][1]+1
            name = line[start:end].strip()
            for labels_idx in range(1,len(labels_line)):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
                local_dict[labels_line[labels_idx]] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
            # We store each entry in the temp dictionary
            temp_dict[name] = local_dict
        # We store each temp dictionary to process
        showmodprocmapp_dict[process] = temp_dict

    return showmodprocmapp_dict

    


def showmoduleprocessma(self,slot):

    showmodprocma_dict = {}
    debug = False

    # Sample raw input
    """
    brazil[local]#show module NSM slot 2 ma
    Type                     Usage         Allocs        Frees
    ------------------------ ------------- ------------- -------------
    Slabs                        2,097,152             2             0
    Pools                          628,020       137,486       136,914
    Default VarPool                107,808           402           302
    VarPool Fixed Pools            732,176        60,522        60,454
    VarPool malloc                       0             0             0
    Shared Pools                         0             0             0
    Persistent Pools                12,288             8             0
    malloc                       7,757,824
    Overhead                        18,192            94             0
    MMap                         2,097,152             2             0
    User MMap                          724             1             0
    brazil[local]#

    Sample output:
    ==============

                                                'NSM': {   'Default VarPool': {   'Allocs': '569',
                                                                                  'Frees': '469',
                                                                                  'Usage': '107,808'},
                                                           'MMap': {   'Allocs': '2',
                                                                       'Frees': '0',
                                                                       'Usage': '2,097,152'},
                                                           'Overhead': {   'Allocs': '94',
                                                                           'Frees': '0',
                                                                           'Usage': '18,192'},
                                                           'Persistent Pools': {   'Allocs': '8',
                                                                                   'Frees': '0',
                                                                                   'Usage': '12,288'},
                                                           'Pools': {   'Allocs': '287,847',
                                                                        'Frees': '287,275',
                                                                        'Usage': '628,020'},
                                                           'Shared Pools': {   'Allocs': '0',
                                                                               'Frees': '0',
                                                                               'Usage': '0'},
                                                           'Slabs': {   'Allocs': '2',
                                                                        'Frees': '0',
                                                                        'Usage': '2,097,152'},
                                                           'User MMap': {   'Allocs': '1',
                                                                            'Frees': '0',
                                                                            'Usage': '724'},
                                                           'VarPool Fixed Pools': {   'Allocs': '127,048',
                                                                                      'Frees': '126,980',
                                                                                      'Usage': '732,176'},
                                                           'VarPool malloc': {   'Allocs': '0',
                                                                                 'Frees': '0',
                                                                                 'Usage': '0'},
                                                           'malloc': {   'Allocs': '',
                                                                         'Frees': '',
                                                                         'Usage': '7,757,824'}}}

    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue

        command = "show module %s slot %s ma" %(process,slot)
        raw_modslotma_list = self.cmd(command)
        modslotma_list = raw_modslotma_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotma_list

        if ('ERROR:' in raw_modslotma_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotma_list
            showmodprocma_dict[process] = {'Error':raw_modslotma_list.strip()}
	    continue
        elif raw_modslotma_list == "":
            # no output.  Give out warning and continue on
            print "Command %s shows no output" %command
            continue


        labels_line = modslotma_list[1].split()
    	divider_line = modslotma_list[2]
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
           
	temp_dict = {} 
        for raw_line in modslotma_list[3:]:
            line = raw_line 
            local_dict = {}
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
            start = columnDict[0][0]
            end = columnDict[0][1]+1
            name = line[start:end].strip()
            for labels_idx in range(1,len(labels_line)):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
                local_dict[labels_line[labels_idx]] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(labels_line[labels_idx],local_dict[labels_line[labels_idx]]))
            # We store each entry in the temp dictionary
            temp_dict[name] = local_dict
        # We store each temp dictionary to process
        showmodprocma_dict[process] = temp_dict

    return showmodprocma_dict
	


def getshowmemcounters(self):
    """
    Call show_mem to get data, but remove the "slot" keyword 
    and remove time stamp entry
    """
    shMemory_dict = show_mem(self.ssx)
    tmpDict = {}
    for slot in shMemory_dict.keys():
       if slot == "time stamp":
            continue
       newSlot = slot[-1:]
       tmpDict[newSlot] = shMemory_dict[slot]
    return tmpDict

def showmoduleprocessmappslab(self,slot):
    # Per Greg comment, treat this data as a slob, meaning calculate a total of how many entries
    # and the sum of "Space In Use" and report as one data point.

    showmodprocmappslab_dict = {}
    debug = False
    # Sample raw input
    """
    {'Count': {   'Space In Use': 8204288,
                 'Total Entry': 8},
    'DHCPdLC': {   'Space In Use': 99328,
                   'Total Entry': 1},
    'Evl': {   'Space In Use': 99328,
               'Total Entry': 1},
    'Evt': {   'Space In Use': 111616,
               'Total Entry': 1},
    'Fpd': {   'Space In Use': 99328,
               'Total Entry': 1},
    'Iked': {   'Space In Use': 8910848,
                'Total Entry': 9},
    'Inspectd': {   'Space In Use': 99328,
                    'Total Entry': 1},
    'IpLc': {   'Space In Use': 99328,
                'Total Entry': 1},
    'NSM': {   'Space In Use': 99328,
               'Total Entry': 1}}
 
    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue
	
        command = "show module %s slot %s ma pp-slab" %(process,slot)
        raw_modslotmappslab_list = self.cmd(command)
        modslotmappslab_list = raw_modslotmappslab_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotmappslab_list

        if ('ERROR:' in raw_modslotmappslab_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotmappslab_list
            showmodprocmappslab_dict[process] = {'Error':raw_modslotmappslab_list.strip()}
            continue
        elif raw_modslotmappslab_list == "":
            # no output.  Give out warning and continue on
            print "Command %s shows no output" %command
            continue


        labels_line1 = modslotmappslab_list[1]
        labels_line2 = modslotmappslab_list[2]
    	divider_line = modslotmappslab_list[3]
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
           
	temp_dict = {} 
        sum = 0
        for raw_line in modslotmappslab_list[4:-1]:
            line = raw_line 
            local_dict = {}
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
            start = columnDict[0][0]
            end = columnDict[0][1]+1
            name = line[start:end].strip()
            for labels_idx in range(1,len(columnDict.keys())):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
	    	label = labels_line1[start:end].strip() + " " + labels_line2[start:end].strip()
	    	label = label.strip() 
                local_dict[label] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(label,local_dict[label]))
		# calculate the sum of inuse by adding size and subtracting free space
		if labels_idx == 1:
		    # add it
		    sum += int(local_dict[label].replace(',',''))
		elif labels_idx == 2:
		    # subtract it
		    sum -= int(local_dict[label].replace(',',''))
            # We store each entry in the temp dictionary
            temp_dict[name] = local_dict
        # We store each temp dictionary to process
        showmodprocmappslab_dict[process] = {'Total Entry':str(len(modslotmappslab_list[4:-1])),'Space In Use':str(sum)}

    return showmodprocmappslab_dict

def showmoduleprocessmaslab(self,slot):
    # Per Greg comment, treat this data as a slob, meaning calculate a total of how many entries
    # and the sum of "Space In Use" and report as one data point.
    showmodprocmaslab_dict = {}
    debug = False
    # Sample raw input
    """
    {'Count': {   'Space In Use': 6480896,
                 'Total Entry': 7},
    'DHCPdLC': {   'Space In Use': 1531904,
                   'Total Entry': 2},
    'Evl': {   'Space In Use': 1525760,
               'Total Entry': 2},
    'Evt': {   'Space In Use': 1561600,
               'Total Entry': 2},
    'Fpd': {   'Space In Use': 1505280,
               'Total Entry': 2},
    'Iked': {   'Space In Use': 36207616,
                'Total Entry': 35},
    'Inspectd': {   'Space In Use': 2042880,
                    'Total Entry': 2},
    'IpLc': {   'Space In Use': 39867392,
                'Total Entry': 39},
    'NSM': {   'Space In Use': 2301952,
               'Total Entry': 3}}

    """

    # call to get a list of processes on this slot
    processMemory_dict = show_process_memory(self,slot)
    #pprint(processMemory_dict,indent=4,width=20,depth=20)
    process_dict = {}
    for process in processMemory_dict.keys():
	if process == "Status":
	    # show_process_memory returns error then skip
	    if processMemory_dict['Status'] == "Error":
		continue
	elif re.search('.*_\d+',process) != None:
	    # probably _<digit> added to differentiate same process name in show_process_memory, then skip it
	    continue

        command = "show module %s slot %s ma slab" %(process,slot)
        raw_modslotmaslab_list = self.cmd(command)
        modslotmaslab_list = raw_modslotmaslab_list.splitlines()
        if debug:
            print 'The raw value returned was:'
            print modslotmaslab_list

        if ('ERROR:' in raw_modslotmaslab_list):
            print 'Detected an error when running: ' + command
            print 'Returned text was:'
            print raw_modslotmaslab_list
            showmodprocmaslab_dict[process] = {'Error':raw_modslotmaslab_list.strip()}
	    continue
        elif raw_modslotmaslab_list == "":
            # no output.  Give out warning and continue on
            print "Command %s shows no output" %command
            continue

        labels_line1 = modslotmaslab_list[1]
        labels_line2 = modslotmaslab_list[2]
    	divider_line = modslotmaslab_list[3]
    	columnDict = parse_divider_line(self,divider_line)
    	if debug: 
            print 'The columnDict is:'
            print columnDict
           
	temp_dict = {} 
	sum = 0
        for raw_line in modslotmaslab_list[4:-1]:
            line = raw_line 
            local_dict = {}
            if debug:
                print '----------------------------------------------'
                print 'The line to be processes is:'
                print line
            start = columnDict[0][0]
            end = columnDict[0][1]+1
            name = line[start:end].strip()
            for labels_idx in range(1,len(columnDict.keys())):
                start = columnDict[labels_idx][0]
                end = columnDict[labels_idx][1]+1
	    	label = labels_line1[start:end].strip() + " " + labels_line2[start:end].strip()
	    	label = label.strip() 
                local_dict[label] = line[start:end].strip()
                if debug: 
                    print("The %s is: %s " %(label,local_dict[label]))
		# calculate the sum of "Space in Use" in column 1
		if labels_idx == 1:
		    sum += int(local_dict[label].replace(',',''))
            # We store each entry in the temp dictionary
            temp_dict[name] = local_dict
        # We store each temp dictionary to process
        #showmodprocmaslab_dict[process] = temp_dict
        showmodprocmaslab_dict[process] = {'Total Entry':str(len(modslotmaslab_list[4:-1])),'Space In Use':str(sum)}

    return showmodprocmaslab_dict

#================================
"""
def uninstall(self,version = ""):
    # Uninstall a package.  If verion is specified, uninstall that version
    # Otherwise, choose an avaialble version to install
    debug = True
    
    if version == "":
        # call to get a list of installed version
        installed_version = show_versions_and_build(self)
        if debug:
            pprint(installed_version,indent=4,width=20,depth=20)
	# try to uninstall one version
	enable_prompt_regex = "[\r\n]*\S+\[\S+\]#"
	yesno_prompt_regex =".*[\r\n.]*\(\[*yes\]*/\[*no\]*\)\s*$"
	for ver in installed_version.keys():
            self.sendline('system uninstall package %s' %ver)
	    done = False
	    while not done:
                retr == self.expect(yesno_prompt_regex,enable_prompt_regex, timeout = 10)
                if retr == 0:
                    self.sendline('system uninstall package %s' %ver)
		
            # This is the password option:
            ses.sendline(password)
	    output = self.cmd("system uninstall package %s" %ver)
"""

#================================

# End section added by Anthony Ton
