#!/sr/bin/env python
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

DESCRIPTION: Covers CLI related test cases from RADIUS test plan 
TEST PLAN: AAA/RADIUS Test Plan
TEST CASES: RADIUS-CLI-001
            RADIUS-CLI-002		
            RADIUS-CLI-003		
            RADIUS-CLI-004		
            RADIUS-CLI-005		
            RADIUS-CLI-006		
            RADIUS-CLI-007	
            RADIUS-CLI-008	
            RADIUS-CLI-009	
            RADIUS-CLI-010	

TOPOLOGY DIAGRAM: Single ssx.
	|-----|
	| SSX |  
	|-----| 
DEPENDENCIES: None
How to run: "python2.5 radius_cli.py"
AUTHOR: Raja rathnam - rathnam@primesoftsolutionsinc.com
REVIEWER: 
"""

import sys, os

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

class test_RADIUS_CLI(test_case):
    """ 
    Description: - RADIUS CLI test cases. 
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

    def test_RADIUS_CLI_001(self):
        """
        Test case Id: -  RADIUS-CLI-001
        Description: - Verify all RADIUS session authentication profile related CLI commands.
        """

	#From the context mode in CLI, enter the radius session authentication profile & 
	#configure the various parameters available under the profile
        self.ssx.config_from_string(script_var['radius_cli_001'])

	# Verify the configured profile setting using .show configuration. command .
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_001'])
        self.failUnless(output[0] != False ,output[1])

	# Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_RADIUS_CLI_002(self):
        """
        Test case Id: -  RADIUS-CLI-002
        Description: - Verify all RADIUS session accounting profile related CLI commands.
        """
	# From the context mode in CLI, enter the radius session accounting profile 
	# And configure the various parameters available under the profile.
        self.ssx.config_from_string(script_var['radius_cli_002'])

	# Verify the configured profile setting using .show configuration. command.
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_002'])
        self.failUnless(output[0] != False ,output[1])

        # Verify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_RADIUS_CLI_003(self):
        """
        Test case Id: -  RADIUS-CLI-003
        Description: - Verify all RADIUS user authentication profile related CLI commands.
        """

        # From the context mode in CLI, enter the radius user authentication profile .
	# And configure the various parameters available under the profile.
        self.ssx.config_from_string(script_var['radius_cli_003'])

	# Verify the configured profile setting using .show configuration. command.
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_003'])
        self.failUnless(output[0] != False ,output[1])

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

    def test_RADIUS_CLI_004(self):
        """
        Test case Id: -  RADIUS-CLI-004
        Description: -  Verify the configured profile setting using .show configuration. command. 
        """

        # From the context mode in CLI, enter the radius user accounting profile .
	# And configure the various parameters available under the profile.
        self.ssx.config_from_string(script_var['radius_cli_004'])
 	
	# Verify the configured profile setting using .show configuration. command.	
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_004'])
        self.failUnless(output[0] != False ,output[1])

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")


    def test_RADIUS_CLI_005(self):
        """
        Test case Id: -  RADIUS-CLI-005
        Description: - Verify RADIUS attribute configuration from CLI.
        """
	# From the context mode in CLI, configure the radius NAS-IP-ADDRESS attribute .
        self.ssx.config_from_string(script_var['radius_cli_005'])

        # Verify the configured profile setting using .show configuration. command.
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_005'])
        self.failUnless(output[0] != False ,output[1])

        #Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

    def test_RADIUS_CLI_006(self):
        """
        Test case Id: -  RADIUS-CLI-006
        Description: - Verify that the CLI allows configuring multiple radius servers
                                in the same profile for redundancy.
        """

        # From context mode configure the radius session authentication profile with two servers
        # where in the second server is for redundancy
        self.ssx.config_from_string(script_var['radius_cli_006'])

        # Verify the configured profile using the 'show configuration' commands .
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_006'])
        self.failUnless(output[0] != False ,output[1])

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



    def test_RADIUS_CLI_007(self):
        """
        Test case Id: -  RADIUS-CLI-007
        Description: - Verify that appropriate errors are displayed when some parameters are mis-configured.
        """

	# Intentionally mis-configure some RADIUS settings. Like setting the max-outstanding 
	# messages to an unsupported value etc.

        self.ssx.configcmd("context %(context)s"%script_var)
        self.ssx.configcmd("radius session accounting profile")
        invalid_command_array=script_var['radius_cli_007'].split('\n')

        # Verify that that appropriate errors are displayed when some parameters are mis-configured.
        for i in range(1,len(invalid_command_array)):
              cli_output = self.ssx.configcmd(invalid_command_array[i])
              self.failUnless("ERROR" in cli_output,"""No error displayed with invalid input command
                                Cli used is %s
                                Expected is ERROR in cli
                                Actual is %s"""%(invalid_command_array[i],cli_output))

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

    def test_RADIUS_CLI_008(self):
        """
        Test case Id: -  RADIUS-CLI-008
        Description: - Verify the configured RADIUS settings can be deleted or removed.
        """

        # Configure SSX with requried RADIUS global profile settings
        self.ssx.config_from_string(script_var['radius_cli_008_before_no'])

        # Configure SSX within the above profile settings with  'no' command
        self.ssx.config_from_string(script_var['radius_cli_008_no_profile'])

        #Verifing that the deletion  of configuration using "show configuration " is there are not  output
        show_confi_output = self.ssx.cmd("show configuration")
        show_confi_split = show_confi_output.split('\n')
        if show_confi_split[4] == " exit":
                print "Test Case Pass"
        else:
                self.failUnless(0,""" Test Case Failed""")



        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

    def test_RADIUS_CLI_009(self):

        """
        Test case Id: -  RADIUS-CLI-009
        Description: -  Verify all RADIUS related show commands.
        """

        #Configure varioues RADIUS setings using CLI
        self.ssx.config_from_string(script_var['radius_cli_009'])

        #Saving the cofiguration
        self.ssx.save_config(location='/cfint/stoke.cfg')

        # Verify the configuration using the 'show configuration' command
        output = generic_verify_config(self.ssx,config_file_loaded=script_var['radius_cli_009'])
        self.failUnless(output[0] != False ,output[1])

        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")

    def test_RADIUS_CLI_010(self):
        """
        Test case Id: -  RADIUS-CLI-010
        Description: -  Reloading device after RADIUS configuration.
        """

        #Establish a telnet session to the SSX box.
        self.ssx.close()
        self.ssx = SSX(topo.ssx1["name"])
        self.ssx.telnet()

        # Configure various RADIUS settings using CLI .
        self.ssx.config_from_string(script_var['radius_cli_010'])

        #Saving the cofiguration
	self.ssx.cmd("save configuration")
        #self.ssx.save_config(location='/cfint/stoke.cfg')

        # Reload the SSX
        self.ssx.reload_device()

        # After reload verify the previously set RADIUS configuration using the "show configuration" command.
        self.ssx.cmd('terminal length infinite')
        output = generic_verify_config(self.ssx,context="%s" % script_var['context'],config_file_loaded=script_var['radius_cli_010'])
        self.failUnless(output[0] != False ,output[1])

	
        # Vefify that the SSX is still in a healthy state
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy(hs), "Platform is not healthy")



if __name__ == '__main__':

    filename = os.path.split(__file__)[1].replace('.py','.log')
    log = buildLogger(filename, debug=True, console=True)

    suite = test_suite()
    suite.addTest(test_RADIUS_CLI)
    test_runner(stream=sys.stdout).run(suite)

