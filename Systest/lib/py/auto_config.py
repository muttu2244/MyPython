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

"""
This API is designed to dynamically generate the configuration for some/all
devices in your test setup and load that configuration. It has special methods
for determining if the configuration needs to generated from scratch or not
and if it needs to be loaded on the SSX. 

The logic for loading of the configuration can be found here:
http://stoke-central.stoke.com/index.php/Verifying_the_Running_Configuration

This method will also be usable via a command line interface. In that application
it will load and hash configurations. The hashes will be displayed to the screen.
"""

# Verify files exist
import os 
# md5 hashing library
import hashlib
# used for storing and loading md5 hashes
import ConfigParser
# for copying files about
import shutil

# used to auto configure
from topo import *
from config import *
from SSX import SSX

# used to generate the configs
import tunnel

# used to hash the config from the cisco
import CISCO

# used to crash when there is a fault
import sys 

# Global Debug 
debug = False

def hash_running_config(self):
    """
    takes: the SSX object
    returns: the md5 hash of the running config
    
    Logic:
    runs the command "show config" and then calculates the md5 hash of this config.
    After calculation it returns the md5 hash.
    """
    debug = False
    
    if debug:
        print 'now in auto_config.py hash_running_config'
        
    # with python2.5 device.py this may fail with large configurations
    # this is not a bug in the hash_running_config library
    if debug:
        print 'retrieving the running config from the SSX'
    # We need to strip off the first empty line
    # empty first line is left in by device.py (bug)
    if debug:
        print 'removing blank first line'
    running_config = raw_running_config.lstrip()
    # chop it into lines to process
    running_config_lines = running_config.splitlines()
    

        
    
    
    # should probably make sure we got something back here
    # have no idea what the failure of running the above command
    # looks like. 
    
    hash_buffer = hashlib.md5()
    for line in running_config_lines:
        real_line = line + '\n'
        hash_buffer.update(real_line)
    # Instead we will split the raw input 
    # then add the missing \n char on the end
    # then hash it. 
    if debug:
        print 'hashing the running config'
    hash_value = hash_buffer.hexdigest()
    if debug:
        print 'the hashed value is:', hash_value
        
    return hash_value
    
    
    
def hash_running_config_cisco(cisco_ip):
    """
    takes: the cisco IP/hostname
    returns: the md5 hash of the running config
    
    Logic:
    runs the command "show running-config" and then calculates the md5 hash of this config.
    After calculation it returns the md5 hash.
    """

    debug = False
    
    if debug:
        print 'connecting to cisco:', cisco_ip
    cisco = CISCO.CISCO(cisco_ip)
    cisco.console(cisco_ip)

    
    if debug:
        print 'now in auto_config.py hash_running_config_cisco'
        
        
        
        
        
    # with python2.5 device.py this may fail with large configurations
    # this is not a bug in the hash_running_config library
    if debug:
        print 'retrieving the running config from the cisco'
    raw_running_config = cisco.cmd('show running-config')
    running_config = raw_running_config.lstrip()
    running_config_lines = running_config.splitlines()
    if debug:
        print 'we got', len(running_config_lines), 'lines to process'
    # This command returns some extra stuff at the top of the cisco config
    # It should be stripped. 

    if debug:
        line_count = 0
        for line in running_config_lines:
            print line
            line_count = line_count + 1
            if line_count == 10:
                break
                
    discard_line_count = 3
    
    if debug:
        print 'the following lines will be thrown away'
        for line in range(0, discard_line_count):
            print running_config_lines[line]
    
    # should probably make sure we got something back here
    # have no idea what the failure of running the above command
    # looks like. 
    
    hash_buffer = hashlib.md5()
    for line in running_config_lines[discard_line_count:]:
        real_line = line + '\n'
        hash_buffer.update(real_line)
    # Instead we will split the raw input 
    # then add the missing \n char on the end
    # then hash it. 
    if debug:
        print 'hashing the running config'
    hash_value = hash_buffer.hexdigest()
    if debug:
        print 'the hashed value is:', hash_value
        
    return hash_value
    
    
def save_running_config(self, directory='cwd', \
                        server = '10.1.1.101', \
                        username = 'regress', \
                        password = 'gleep7'):
    """
    This method is to be run any time you change the running config for any reason.
    If you don't run this method the auto load method will always return the system
    back to the base config. 
    
    takes: 
    self - the SSX object
    directory = 'cwd' - current working directory
    server = '10.1.1.101' - qa-radxpm-1
    username = 'regress' - default QA automation user
    password = 'gleep7' - password for regress
    
    Logic:
    1. saves the configuration to the SSX hd. "save config /hd/running_config.cfg"
    2. copies the file via SFTP to the user regress's home directory:
       copy /hd/running_config.cfg sftp://regress@10.1.1.101:/home/regress/running_config.cfg
    3. opens a linux cmd shell localy and pulls that file to the CWD
       copy /home/regress/running_config.cfg . 
       copy /home/regress/running_config.cfg <directory>
    """
    if debug:
        print 'now in auto_config save_running_config'
    
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




    if debug:
        print 'removing the file /hd/running_config.cfg just in case'
    self.cmd('del /hd/running_config.cfg noconfirm')    
    
    if debug:
        print 'saving config to /hd/running_config.cfg'
    self.cmd('save config /hd/running_config.cfg')
    
    if debug:
        print 'copying configuration off SSX'
    command = 'copy /hd/running_config.cfg' + ' sftp://' + username + '@' + server + ':/home/' + username \
         + '/running_config.cfg'
        
    if debug:
        print 'The command will be:'
        print command
    print 'Copying the running_config.cfg off the system.'

    #self.ftppasswd(command, user_password)
    self.ftppasswd(command, password, 60)
    print 'File copied succesfully'
    
    #######################################################
    ## copy file from regress home directory over to CWD ##
    #######################################################
    current_dir = os.getcwd()
    if debug:
        print 'script is being run from:', current_dir
        
    source_path = '/home/' + username + '/running_config.cfg'
    
    dest_filename = current_dir + '/running_config.cfg'
    
    print '------------------------'
    print 'about to move:', source_path, 'to:', dest_filename
    
    shutil.copyfile(source_path, dest_filename)
    print 'file moved succesfully.'

    return 0


def md5_hash_file(filename):
    """
    takes:
    filename - can be cwd just filename or full path
    returns:
    md5 hash of contents of file
    
    Logic:
    opens a file specified opens it and calculates the md5 hash of the contents. Will fail if
    file does not exist or can not be opened. (raise exception)
    """
    debug = False
    if debug:
        print 'now in auto_config.py md5_hash_file'
    

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


    
    if debug:
        print 'checking for the file:', filename
    if os.path.exists(filename):
        try:
            if debug:
                print 'trying to open the file for reading'
            raw_file = open(filename, 'r')
        except:
            error_message = 'unable to open file: ' + filename 
            raise(error_message)
            
        if debug:
            print 'creating hashlib object'
        hash_buffer = hashlib.md5()
        
        if debug:
            print 'reading the file line by line'
            print '*' * 40
        for line in raw_file:
            if debug:
                print 'processing line:'
                print line
            hash_buffer.update(line)
            
        if debug:
            print '*' * 40
            print 'done reading file. Closing it'
        raw_file.close()
            
        if debug:
            print 'hashing the contents of the file'
        hash_value = hash_buffer.hexdigest()
        
        if debug:
            print 'the calculated hash is:', hash_value
            
        return hash_value
        
    else:
        print 'file:', filename, 'does not exist!'
        raise('file does not exist')
    
    
class hash_file(object):
    """
    Object that handles the hash file stored in CWD containing key pairs of filename:hash value
    used to store calculated hashes for topo.py and running config
    
    to access the hashes you will use
    myhashes = hash_file
    myhashes.hashes['hash name']
    """
    def __init__(self):
        if debug:
            print 'now in auto_config.py hash_file object method __init__'
            
        self.hash_file_filename = 'hashfile.cfg'
        self.hash_file_exists = False
        
        # this will be the config file handle (actual file)
        self.config_file = None
        
        # this is the config parser handle. This is used most of the time
        self.config = None
        
        # This is the member variable where the key pairs will be stored
        # accessing it will be hash_file.hashes['hash name']
        self.hashes = {}
                

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



        # At this point we need to make sure the file exists
        # If it does not we call the create_hash_file method
        # hopefully it's able to create the file.
        if debug:
            print 'checking for the hashfile:', self.hash_file_filename
            
        if not (os.path.exists(self.hash_file_filename)):
            retr = self.create_hash_file()
            # If anything is returnd it's a failure
            if retr:
                raise("unable to create new hashfile. Please check directory/file permissions")
        else:
            self.hash_file_exists = True
            if debug:
                print 'hashfile found'

    def read_hash_file(self):
        """
        takes:
        filename = 'hashfile.cfg' - file containing md5 hashes of other files
        
        returns:
        python dictionary containing filename:md5 hash pairs
        
        Logic:
        using the python config library it makes a human readable file containing simple
        filename:hash pairs. Can be used for hashing any file. Inteded use is for hashing the config
        files and the topo.py file to detect changes in those files. If the file is not present or can
        not be read this method will raise exception. 
        
        After first successful run of automation there should be the following pairs:
        topo.py 
        generate_config.cfg
        running_config.cfg
        <test_script_name>.py 
        """
        if debug:
            print 'now in read_hash_file'
        
        if self.hash_file_exists:
            
            self.config = ConfigParser.ConfigParser()
            
            """
            # If the file was read previously then the pointer will be at the end
            # of the file. We need to reset the pointer to the beginning so 
            # we can read it a second time (for every read)
            self.config_file.seek(0)
            """

            try:
                self.config.read(self.hash_file_filename)
            except:
                if debug:
                    print 'unable to read the configuration file'
                raise("unable to read the configuration file. It's either corrupt or file permissions")
                
            # At this point instead of reading all the sections it would be much better to only
            # have one section. That makes things much less complex. 
            
            try:
                filenames = self.config.options('hashed files')
                for filename in filenames:
                    self.hashes[filename] = self.config.get('hashed files', filename)
            except:
                if debug:
                    print 'there are no hashed files'
                self.hashes = None
            return self.hashes 

        
    def write_hash_file(self):
        """
        takes the member variable self.hashes and writes it to the file hash_file_filename which
        should be hashfile.cfg but can be overwritten. Raises exception if it fails to write file.
        """
        if debug:
            print '\nnow in auto_config write_hash_file'
            
        if debug:
            print self.hashes 
            
        filenames = self.hashes.keys()
        for file in filenames:
            self.config.set('hashed files', file, self.hashes[file])
        
        self.config_file = open(self.hash_file_filename, 'w')
        self.config.write(self.config_file)
        self.config_file.close()
        
    
    def create_hash_file(self):
        """
        generates an empty hash file. Default filename is hashfile.cfg Calls the method write_hash_file
        to write to disk the first time. If exception is raisied allows for backtrack.
        """
        debug = False
        
        if debug:
            print 'now in create_hash_file'
            # there are two parts. The self.config is the object representing the data structures
            # the othee is the raw file on the disk that's called self.config_file
            
        self.config = ConfigParser.ConfigParser()
        try:
            if debug:
                print 'creating the config file'
            self.config_file = open(self.hash_file_filename, 'w')
        except:
            print 'unable to open the config file:', self.hash_file_filename, 'for writing'
            print 'please check the file permissions in the CWD'
            raise('unable to write to CWD')
        
        if debug:
            print 'adding the section header "hashed files"'
        self.config.add_section('hashed files')
        
        if debug:
            print 'writing changes to disk.'
        self.config.write(self.config_file)
        
        
        self.hash_file_exists = True
        
    
    def __del__(self):
        """
        Automatically called when destroying this object
        """
        if debug:
            print 'now in the __del__ method of the hash file object'
        try:
            self.config_file.close()
        except:
            pass
            
        


def copy_config(self, source_filename):
    """
    Takes a configuraiton file from the CWD and copies it onto the
    SSX into /hd/perf
    
    input: 
    - self.ssx
    - source_filename
    """
    debug = True
    
    if debug:
        print 'now in auto_config.py copy_config method'
        
    # get out of the log dir if necessary 
    tunnel.exit_log_dir()

    if debug:
        print 'checking for source file'
        
    if os.path.exists(source_filename):
        
        #############################
        # Create /hd/perf if needed #
        #############################
        
        if debug:
            print 'checking to see if /hd/perf exists on the ssx'
        # make the /hd/perf dir
        retr = self.ssx.cmd('dir /hd | grep perf')
        
        if 'perf/' in retr:
            if debug:
                print '/hd/perf exists'
        else:
            
            print 'creating the /hd/perf directory for the first time'
            self.ssx.cmd('mkdir /hd/perf')
        
        current_dir = os.getcwd()
        if debug:
            print 'cwd is:', current_dir
        
    
        full_filename_path = os.path.join(current_dir, source_filename) 
        if debug:
            print 'the full source path will be:'
            print full_filename_path
        # The IP used here is "sandscript" and should always be available in santa clara
        ftp_command = 'copy sftp://regress@10.1.1.2:' + full_filename_path + ' /hd/perf noconfirm'
        if debug:
            self.myLog.debug("the SFTP command will be:")
            self.myLog.debug(ftp_command)
        retr = self.ssx.ftppasswd(ftp_command)
        if not (retr == 0):
            return 'sftp failed'
    else:
        return 'source file does not exist!'
        
    return 0

def auto_config(self):
    """
    Method checks running configuration against saved configuration
    If there is any change it generates and loads the configuration
    This method configures all devices in the test setup for x tunnels
    with x being specified in the topo file. 
    
    self must contain the logger
    """

    """
    Section Index:
    - topo.py
    -- verify hash
    
    - Cisco
    -- clear config
    -- load config (configure)
    
    - SSX (tunnel initiator)
    -- check running config hash
    -- clear config (load minimal)
    -- generate config
    -- load config
    
    - SSX (DUT)
    -- check running config hash
    -- clear config (load minimal)
    -- reload config from file
    -- generate config
    -- load config
    
    - IXIA
    -- Get MAC
    -- Convert Mac
    -- Generate config
    -- copy config
    -- load config
    
    - Verfication
    -- check tunnels
    -- start traffic
    -- check traffic
    -- stop traffic
    """
    debug = True
    

    if debug:
        print 'now in auto_config.py method auto_config'
    
    
    # get out of the log dir if necessary 
    tunnel.exit_log_dir()
    
    if debug:
        print 'connecting to SSX DUT:', topo.ssx_resp['ip_addr']
    ## SSX ##
    ssx_dut = SSX(topo.ssx_resp["ip_addr"])
    ssx_dut.telnet()
    
    if debug:
        print 'connecting to SSX Initiator', topo.ssx_ini['ip_addr']
    ssx_ini = SSX(topo.ssx_ini["ip_addr"])
    ssx_ini.telnet() 



    ###############
    ## - topo.py ##
    ###############
    
    # Default values. 
    # these will be rewriten if the running config has not changed
    # please don't change these!
    regenerate_config = True
    reload_config = True
    


    ##################
    # -- verify hash #
    ##################


    ########################
    ## Hash the topo file ##
    ########################
    if os.path.exists('topo.py'):
        self.myLog.info("hashing the topo.py file")
        topo_hash_value = md5_hash_file('topo.py')
        self.myLog.info("The calculated hash for the topo file was: %s" % topo_hash_value)
    else:
        self.myLog.info("unable to find the topo.py file")
        self.myLog.info("automation can not continue")
        sys.exit(1)



    ###############################
    ## Open/create the hash file ##
    ###############################
    
    myhash = hash_file()                                            
    self.myLog.info("reading the hashfile")                                                            
    hashes = myhash.read_hash_file()
    
    if debug:
        self.myLog.debug(hashes)
    
    if len(hashes) > 0:
        filenames = hashes.keys()
        
        if debug:
            self.myLog.debug(filenames)
    
        ###################################
        ## retrieve the hash for topo.py ##
        ###################################
        
        # Check to see if we have a hash value for the topo.py file
        if 'topo.py' in filenames:
            # compare the saved hash to the hash of the topo.py
            # this will allow us to see if it has changed. 
            
            #############################
            ## Compare the stored hash ##
            #############################
            
            self.myLog.info("Comparing the stored value with the current value")
            if hashes['topo.py'] == topo_hash_value:
                self.myLog.info("**********************************************************")
                self.myLog.info("the two hash values are the same. The topo has not changed")
                self.myLog.info("the configuration does not need to be generated")
                self.myLog.info("**********************************************************")
                # so we don't need to regen the config. 
                regenerate_config = False
            else:
                self.myLog.info("the two values are different. The topo file has changed")
                self.myLog.info("the configuration will be generated fresh")
                regenerate_config = True
                            
            
        # else we have never hashed it. So we must generate all
        # configurations from scratch
        else:
            self.myLog.info("*****************************************************************")
            self.myLog.info("topo.py hash not found the configuration will be generated fresh")
            self.myLog.info("*****************************************************************")
            regenerate_config = True
                    
    else:
        self.myLog.info("**********************************************************")
        self.myLog.info("hashes.cfg is empty. Configuraiton will be generated fresh")
        self.myLog.info("**********************************************************")
        regenerate_config = True

    
    #############
    ## - Cisco ##
    #############
    reload_cisco = True
    
    if not regenerate_config:

        cisco_hash_value = hash_running_config_cisco(topo.cisco['ip_addr'])    
        
        # check to see if we have a hash for the Cisco
        if 'cisco' in filenames:
            if hashes['cisco'] == cisco_hash_value:
                self.myLog.info('the cisco configuration has not changed')
                reload_cisco = False
            else:
                self.myLog.info('the cisco configuraiton has changed. It will be reloaded')
                reload_cisco = True
                
    if reload_cisco:
        ###################
        # -- clear config #
        ###################
        
        self.myLog.info("about to connect to cisco: %s" % topo.cisco['ip_addr'])
        self.myLog.info("clearing all ports used in this topology")
        tunnel.clear_cisco_ports(topo.cisco['ip_addr'])
        self.myLog.info("port cleared")
        
        ##############################
        # -- load config (configure) #
        ##############################
        
        self.myLog.info("about to connect to cisco: %s" % topo.cisco['ip_addr'])
        self.myLog.info("configuring ports used in this topology")
        tunnel.set_up_cisco(topo.cisco['ip_addr'])
        self.myLog.info("all ports configured")
        
        #################
        # Save the Hash #
        #################
        
        self.myLog.info("hashing the cisco running configuration")
        cisco_hash_value = hash_running_config_cisco(topo.cisco['ip_addr'])
        self.myLog.info("writing the hash value into our hash dictionary")
        hashes['cisco'] = cisco_hash_value
        self.myLog.info("saving the hash file")
        myhash.write_hash_file()
    
    
    
    ##############################
    ## - SSX (tunnel initiator) ##
    ##############################
    
    
    ################################
    # -- check running config hash #
    ################################
    
    reload_initiator = True
    
    if not regenerate_config:
    
        init_hash_value = auto_config.hash_running_config(self.ssx_ini)
        
        # check to see if we have a hash value for the initiator
        if 'ssx_ini' in filenames:
            if hashes['ssx_ini'] == init_hash_value:
                self.myLog.info("the tunnel initiator configuration has not changed")
                reload_initiator = False
            else:
                self.myLog.info("the tunnel initator configuration has changed. It will be reloaded")
                reload_initiator = True
    
    if reload_initiator:
        
        ##################################
        # -- clear config (load minimal) #
        ##################################
        
        issu.minimal_configuration(self.ssx_ini)


        ######################
        # -- generate config #
        ######################
        
        
        slot = 2
        routeOption = 'N'
        first_file = 'config_card' + str(slot) + '_initiator.cfg'
        self.myLog.info("generating the tunnel configuration for slot%s" % slot)
        self.myLog.info("the config file will be named: %s" % first_file)
        if os.path.exists(first_file):
            self.myLog.info("the output file already exists. It will be overwritten")


        retr = tunnel.generate_tunnel_config_initiator(topo.max_tun_slot2,\
                    haimc_var['Ini_context_name'], \
                    haimc_var['dummy_intf_slot2_startIp'], \
                    haimc_var['tunnel_intf_slot2_startIp'], \
                    haimc_var['ini_cisco_slot2_ip/mask'], \
                    haimc_var['cisco_ini_slot2_ip'], \
                    topo.dummy_ports[0], \
                    haimc_var['port_ini_slot2'], \
                    haimc_var['ini_slot2_route_startIp'], \
                    haimc_var['lpbk_ip'], \
                    slot, \
                    first_file)
                                                       
        self.failIf(retr)

        self.myLog.info("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        self.myLog.info("the file was generated. Now to generate the file for card 3")
        self.myLog.info("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


        slot = 3
        routeOption = 'N'
        second_file = 'config_card' + str(slot) + '_initiator.cfg'
        self.myLog.info("generating the tunnel configuration for slot%s" % slot)
        self.myLog.info("the config file will be named: %s" % second_file)
        if os.path.exists(second_file):
            self.myLog.info("the output file already exists. It will be overwritten")
            
        retr = tunnel.generate_tunnel_config_initiator(topo.max_tun_slot3,\
                    haimc_var['Ini_context_name2'], \
                    haimc_var['dummy_intf_slot3_startIp'], \
                    haimc_var['tunnel_intf_slot3_startIp'], \
                    haimc_var['ini_cisco_slot3_ip/mask'], \
                    haimc_var['cisco_ini_slot3_ip'], \
                    topo.dummy_ports[1], \
                    haimc_var['port_ini_slot3'], \
                    haimc_var['ini_slot3_route_startIp'], \
                    haimc_var['lpbk_ip1'], \
                    slot, \
                    second_file)

    
    
        first_file = 'config_card2_initiator.cfg'
        second_file = 'config_card3_initiator.cfg'
        ssx_ini_config = 'config_initiator.cfg'
        tunnel.join_files(first_file, second_file, ssx_ini_config)
    
    
    
        ##################
        # -- load config #
        ##################
        
        ######################
        # Copy file onto SSX #
        ######################
        

        
    
    
    #################
    ## - SSX (DUT) ##
    #################
    
    ################################
    # -- check running config hash #
    ################################
    
    ##################################
    # -- clear config (load minimal) #
    ##################################
    
    ##############################
    # -- reload config from file #
    ##############################
    
    ######################
    # -- generate config #
    ######################
    
    ##################
    # -- load config #
    ##################
    
    
    
    
    ###########
    ## - IXIA #
    ###########
    
    ##############
    # -- Get MAC #
    ##############
    
    ##################
    # -- Convert Mac #
    ##################
    
    ######################
    # -- Generate config #
    ######################
    
    ##################
    # -- copy config #
    ##################
    
    ##################
    # -- load config #
    ##################
    
    
    
    
    ###################
    ## - Verfication ##
    ###################
    
    ####################
    # -- check tunnels #
    ####################
    
    ####################
    # -- start traffic #
    ####################
    
    ####################
    # -- check traffic #
    ####################
    
    ###################
    # -- stop traffic #
    ###################


    # Close the telnet session of SSX
    ssx_dut.close()
    ssx_ini.close()

        