#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: Covers CLI related test cases from AAA test plan 
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: AAA-CLI-001
            AAA-CLI-002		
            AAA-CLI-003		
            AAA-CLI-004		
            AAA-CLI-005		
            AAA-CLI-006		
            AAA-CLI-007	

TOPOLOGY DIAGRAM: Single ssx.
	|-----|
	| SSX |  
	|-----| 
DEPENDENCIES: None
How to run: "python2.5 aaa_cli.py"
AUTHOR: Ankit Jain - ankit@primesoftsolutionsinc.com
        Raja rathnam - rathnam@primesoftsolutionsinc.com
	Ramesh - ramesh@primesoftsolutionsinc.com
REVIEWER: 
"""

import sys, os, getopt

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries 
from SSX import SSX 
from log import *
from logging import getLogger
from StokeTest import test_case, test_suite, test_runner  
from helpers import is_healthy

#import configs file
from aaa_config import *
from aaa import *
import topo

testlogdir = ""
if os.environ.has_key('TEST_LOG_DIR'):
    testlogdir = os.environ['TEST_LOG_DIR']

opts, args = getopt.getopt(sys.argv[1:], "d:")
for o, a in opts:
  if o == "-d":
    testlogdir = a

if testlogdir != "":
  os.mkdir(testlogdir)
  os.chdir(testlogdir)




class test_AAA_CLI(test_case):
    """ 
    Description: - AAA CLI test cases. 
    """
    my_log = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx1["ip_addr"])
        self.ssx.telnet()

        # CLear SSX configuration
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()

    def test_AAA_CLI_001(self):
        """
        Test case Id: -  AAA-CLI-001
        Description: - Verify AAA profile configuration mode.
        """

        # Configure SSX from context mode and enter the  AAA profile configuration 
        self.ssx.config_from_string(script_var['aaa_cli_001'])

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("?")

        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        aaa_cmd_array=script_var['list_of_commands'].split('\n')

        # Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in aaa_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_AAA_CLI_002(self):
        """
        Test case Id: -  AAA-CLI-002
        Description: - Verify all AAA profile related CLI commands under a context
        """

        # Enter AAA profile mode from the context mode configure various AAA profile parameters
        self.ssx.config_from_string(script_var['aaa_cli_002'])

        #Verifying the configured AAA profile settings using the "show configuration" for cli with the config_file
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['aaa_cli_002'])
        self.failUnless(output[0] != False ,output[1])

        # Verify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_AAA_CLI_003(self):
        """
        Test case Id: -  AAA-CLI-003
        Description: - Verify all AAA global profile related CLI commands
        """

        # Configure SSX with various AAA global profile parameters
        self.ssx.config_from_string(script_var['aaa_cli_003'])

        #Verifying the configured AAA global profile settings using the "show configuration" for cli with the config_file
        output = generic_verify_config(self.ssx,config_file_loaded=script_var['aaa_cli_003'])
        self.failUnless(output[0] != False ,output[1])

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_AAA_CLI_004(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['aaa_cli_004'])
 	
        # Verify that the output of the 'show debug' command ,
        # With the appropriate configured AAA profile parameters under the appropriate context.
        # Store the show cofnig output in ssx_show_op
        show_output = self.ssx.cmd("show debug")

        #config_file is split based on the new line and stroe
        #the list of commands in list "config_file_command_list"
        aaa_cmd_array = script_var['aaa_cli_004'].split('\n')

        # Verify that the output of the 'show debug' command ,
        # With the appropriate configured AAA profile parameters under the appropriate context.
        for i in range(0,len(aaa_cmd_array)):
            partition_output = aaa_cmd_array[i].partition('aaad')
            self.failUnless(partition_output[2] in show_output,"""Error while matching\n
                                Expected output is ->%s
                                Actual Output is %s""" %(partition_output[2],show_output))
        #configre SSX debug module with 'debug all'.
        self.ssx.cmd("debug module aaad all")
        show_output = self.ssx.cmd("show debug")
        self.failUnless("aaad group all" in show_output,"""Error while matching with show output\n
                                Expected output is aaad group all
                                Actual Output is %s""" %(show_output))


        #Clear the previous configuration on SSX debug module
        self.ssx.configcmd("no debug all")

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_AAA_CLI_005(self):
        """
        Test case Id: -  AAA-CLI-005
        Description: - Verify that appropriate errors are displayed when some parameters are mis-configured.
        """

        # Intentionally mis-configuring some AAA-settings under a context  
        self.ssx.configcmd("context aaaAutomatedTest")
        self.ssx.configcmd("aaa profile")
        cli_output = self.ssx.configcmd("debug circuit-session fffffffff")
        if cli_output:
                m = cli_output
        else:
                print "Test Case Fail"
        	self.failUnless(0 ,"cli command is mis-configured")

        #Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_AAA_CLI_006(self):
        """
        Test case Id: -  AAA-CLI-006
        Description: - Verify the configured AAA settings can be deleted or removed.
        """

        # Configure SSX with requried AAA global profile settings
        self.ssx.config_from_string(script_var['aaa_cli_006_before_no'])

        # Configure SSX within the above profile settings with  'no' command
        self.ssx.config_from_string(script_var['aaa_cli_006_no_profile'])

        #Verifing that the deletion  of configuration using "show configuration " is there are not  output  
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['aaa_cli_006_after_no'])
        self.failUnless(output[0] == False ,"The cli command is not expected in show configuration after using 'no' command")



        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
#    log = buildLogger(filename, debug=True,console=True)
    log = buildLogger(filename, debug=True)

    suite = test_suite()
    suite.addTest(test_AAA_CLI)
    test_runner(stream=sys.stdout).run(suite)

