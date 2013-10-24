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

DESCRIPTION: Covers CLI related test cases from CDR test plan 
TEST PLAN: CDR Test Plan
TEST CASES: CDR-CLI-001
            CDR-CLI-002		
            CDR-CLI-003		
            CDR-CLI-004		
            CDR-CLI-005		
            CDR-CLI-006		
            CDR-CLI-007	
            CDR-CLI-008	
            CDR-CLI-009	
            CDR-CLI-010	
            CDR-CLI-011	
            CDR-CLI-012	
            CDR-CLI-013	
            CDR-CLI-014	
            CDR-CLI-015	

TOPOLOGY DIAGRAM: Single ssx.
	|-----|
	| SSX |  
	|-----| 
DEPENDENCIES: None
How to run: "python CDR_cli.py"
AUTHOR: Laxmana Maruthy - laxmana@stoke.com
REVIEWER:Srinivas Nukala - srinivas@stoke.com 
"""

import sys, os, getopt

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from cdr import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *
#import private libraries
from ike import *

from misc import *

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




class test_CDR_CLI(test_case):
    """ 
    Description: - CDR CLI test cases. 
    """
    my_log = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(topo.ssx["ip_addr"])
        self.ssx.telnet()

        # CLear SSX configuration
        self.ssx.clear_config()
        # wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()

    def tearDown(self):
        # Close the telnet session of SSX
        self.ssx.close()

    def test_CDR_CLI_001(self):
        """
        Test case Id: -  CDR-CLI-001
        Description: - Verify CDR related configuration 
        """

        # Configure SSX from context mode and enter the  AAA profile configuration 
        self.ssx.config_from_string(script_var['cdr_cli_001'])

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("?")

        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands1'].split('\n')

        # Verify the list of commands in CDR configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_002(self):
        """
        Test case Id: -  CDR-CLI-002
        Description: - Load the CDR configuration & the verify the same whether they have configured the same without issues
        """

        # Enter AAA profile mode from the context mode configure various AAA profile parameters
        self.ssx.config_from_string(script_var['cdr_cli_002'])

	show_output = self.ssx.cmd("show configuration cdr")


        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands2'].split('\n')


	# Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))



        # Verify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_003(self):

        """
        Test case Id: -  CDR-CLI-003
        Description: - Verify AAA profile configuration mode.
        """

        # Configure SSX from context mode and enter the  AAA profile configuration
        self.ssx.config_from_string(script_var['cdr_cli_003'])

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("?")

        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands3'].split('\n')

        # Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_004(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify AAA profile configuration mode.
        """

        # Configure SSX from context mode and enter the  AAA profile configuration
        self.ssx.config_from_string(script_var['cdr_cli_004'])

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.cmd("show configuration cdr")

	if show_output.strip():
		self.failUnless(0,"Test case failed")
	else:
	        # Vefify that the SSX is still in a healthy state
        	hs = self.ssx.get_health_stats()
	        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_005(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify AAA profile configuration mode.
        """

        # Configure SSX from context mode and enter the  AAA profile configuration
        self.ssx.config_from_string(script_var['cdr_cli_005'])

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.cmd("show configuration cdr")

        if show_output.strip():
                self.failUnless(0,"Test case failed")
        else:
                # Vefify that the SSX is still in a healthy state
                hs = self.ssx.get_health_stats()
                self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_006(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        #self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])
 	

        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("debug ?")


        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands6'].split('\n')

        # Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))


        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



    def test_CDR_CLI_007(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        #self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])


        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("debug module cdrproc ?")


        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands7'].split('\n')

        # Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))


        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_008(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        #self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])


        # Store the '?' command output in 'show_output'
        show_output = self.ssx.configcmd("debug module cdr?")


        # Store the commands configured on SSX in a list 'aaa_cmd_array'
        cdr_cmd_array=script_var['list_of_commands8'].split('\n')

        # Verify the list of commands in AAA profile configuration mode with the list 'list_of_commands'
        for command in cdr_cmd_array:
            self.failUnless(command.strip() in show_output,"""
                CLI Used - " ? "
                Expected in output of  command - %s
                Actual output of < ? >  - %s"""% (command, show_output))


        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")





    def test_CDR_CLI_009(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])

        #configre SSX debug module with 'debug all'.
        self.ssx.cmd("debug module cdrproc all")
        # Verify that the output of the 'show debug' command ,
        show_output = self.ssx.cmd("show debug")
        self.failUnless("cdrproc group all" in show_output,"""Error while matching with show output\n
                                Expected output is cdrproc group all
                                Actual Output is %s""" %(show_output))


        #Clear the previous configuration on SSX debug module
        self.ssx.configcmd("no debug all")

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



    def test_CDR_CLI_010(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])

        #configre SSX debug module with 'debug all'.
        self.ssx.cmd("debug module cdrtest all")
        # Verify that the output of the 'show debug' command ,
        show_output = self.ssx.cmd("show debug")
        self.failUnless("cdrtest group all" in show_output,"""Error while matching with show output\n
                                Expected output is cdrtest group all
                                Actual Output is %s""" %(show_output))


        #Clear the previous configuration on SSX debug module
        self.ssx.configcmd("no debug all")

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")




    def test_CDR_CLI_011(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])

        #configre SSX debug module with 'debug all'.
        self.ssx.cmd("debug module cdrlib all")
        # Verify that the output of the 'show debug' command ,
        show_output = self.ssx.cmd("show debug")
        self.failUnless("cdrlib group all" in show_output,"""Error while matching with show output\n
                                Expected output is cdrlib group all
                                Actual Output is %s""" %(show_output))


        #Clear the previous configuration on SSX debug module
        self.ssx.configcmd("no debug all")

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



    def test_CDR_CLI_012(self):
        """
        Test case Id: -  AAA-CLI-004
        Description: - Verify all the AAA related debug commands.
        """

        #Configure SSX,to enable 'debug' for some aaad modules
        self.ssx.configcmd("no debug all")
        self.ssx.config_from_string(script_var['cdr_cli_006'])

        #configre SSX debug module with 'debug all'.
        self.ssx.cmd("debug process-module cdr")
        # Verify that the output of the 'show debug' command ,
        show_output = self.ssx.cmd("show debug")
        self.failUnless("Process module CDR" in show_output,"""Error while matching with show output\n
                                Expected output is Process module CDR
                                Actual Output is %s""" %(show_output))


        #Clear the previous configuration on SSX debug module
        self.ssx.configcmd("no debug all")

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")




    def test_CDR_CLI_013(self):
        """
        Test case Id: -  AAA-CLI-005
        Description: - Verify that appropriate errors are displayed when some parameters are mis-configured.
        """

        # Intentionally mis-configuring some AAA-settings under a context  
        self.ssx.configcmd("context cdr-1")
        self.ssx.configcmd("cdr")
	#cli_output = self.ssx.config_from_string(script_var['aaa_cli_005A'])
        cli_output = self.ssx.configcmd("disk-commit-interval 0")
	#m = cli_output.search("ERROR")
		#print "Test PASS"
	if cli_output:
                m = cli_output
	else:
		print "Test Case Fail"

	#self.failUnless("""Test Case Failed""")

        #Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_014(self):
        """
        Test case Id: -  AAA-CLI-006
        Description: - Verify the configured AAA settings can be deleted or removed.
        """


        # Intentionally mis-configuring some AAA-settings under a context
        self.ssx.configcmd("context cdr-1")
        self.ssx.configcmd("cdr")
        cli_output = self.ssx.configcmd("disk-commit-interval 1440001")
        #m = cli_output.search("ERROR")
                #print "Test PASS"
        if cli_output:
                m = cli_output
        else:
                print "Test Case Fail"



        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_CDR_CLI_015(self):
        """
        Test case Id: -  AAA-CLI-006
        Description: - Verify the configured AAA settings can be deleted or removed.
        """


        # Intentionally mis-configuring some AAA-settings under a context
        self.ssx.configcmd("context cdr-1")
        self.ssx.configcmd("cdr")
	cli_output = self.ssx.configcmd("debug circuit-session fffffffff")
        if cli_output:
                m = cli_output
        else:
                print "Test Case Fail"



        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



if __name__ == '__main__':


    filename = os.path.split(__file__)[1].replace('.py','.log')
#    log = buildLogger(filename, debug=True,console=True)
    log = buildLogger(filename, debug=True)

    suite = test_suite()
    suite.addTest(test_CDR_CLI)
    test_runner(stream=sys.stdout).run(suite)

