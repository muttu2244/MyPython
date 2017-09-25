"""LTP Test suite"""
import sys
from unittest import TestSuite, TextTestRunner
import os
import platform
import logging

from CountryLTP import CountryLTP
from TargetRangesLTP import TargetRangesLTP
from EmgcyContactsLTP import EmgcyContactsLTP
from TooltipLTP import TooltipLTP
from SmartReminderLTP import SmartReminderLTP
from ExpandedGraphLTP import ExpandedGraphLTP
from DayDividersLTP import DayDividersLTP
from MenuLTP import MenuLTP
from EditEntryLTP import EditEntry
from HCPReportLTP import HCP
from HealthCareLTP import HealthCare
from MeterErrorCodesLTP import MeterErrorCodes
from MeterHelpLTP import MeterHelp
from MeterSettingsLTP import MeterSettings
from NewReminderLTP import NewReminder
from UnpairingLTP import Unpairing
from AppHelpLTP2 import Apphelp
from FAQLTP import FAQ
from EditViewLTP import EditView
from LanguageSelection import LanguageSelection
SYS_PATH = os.path.dirname(os.getcwd())
sys.path.append(SYS_PATH + r"\\lib\\")
from BaseAPI import Utility, Common, Device, Application, Misc, Objects, Logger, Config
# from BaseAPI import Config

class LTPTests(object):
    """
        Class to add testcases to the LTP suite
    """
    def __init__(self):
        self.util = Utility()
        self.common = Common()
        self.misc = Misc()
        self.app = Application()
        # self.obj = Objects()
        self.dev = Device()
        self.app_name = None
        self.util.set_up()
        self.suitelogger = Logger.Logger("suitelevel")
        # pass

    def project_testcase_setup(self):
        """Project level setup"""
        # pass
        self.logger = logging.getLogger("suitelevel")
        self.logger.info("Project Logging started")
        self.logger.info("===================================================")
        self.logger.info("HOST MACHINE INFORMATION")
        self.logger.info("===================================================")
        self.logger.info("Host Name: %s" % platform.node())
        self.logger.info("Host OS: %s" % platform.system())
        self.logger.info("===================================================\n")
        self.logger.info("===================================================")
        self.logger.info("DEVICE AND APP INFORMATION")
        self.logger.info("===================================================")
        self.logger.info("Seetest version: 10.3.71")
        device_name = self.dev.get_connected_devices(self.util.client)
        self.logger.info("Device Name : %s" % device_name)

        # connect only one device with system
        self.misc.set_device(self.util.client, device_name, "suitelevel")
        device_info_path = self.misc.get_devices_information(
            self.util.client, SYS_PATH, device_name, "suitelevel")
        # getting app name depending on OS
        self.app_name = self.util.get_app_name(device_info_path, device_name)
        self.app.launch(self.util.client, self.app_name, True, True, "suitelevel")
        self.util.log_project_info(device_info_path, device_name)
        self.common.set_project_base_directory(self.util.client, os.getcwd(), "suitelevel")
        self.logger.info("Application version : %s"%self.dev.get_device_property(
            self.util.client,  "app.version"))
        # if device_name.find("iPhone") > 0:
        #     self.app.launch(self.util.client, "search:contour", True, True)
        #     self.my_object = "Iobject"
        # else:
        #     self.my_object = "Aobject"
        #     self.app_name = self.util.get_app_name(device_info_path, device_name)
        #     self.app.launch(self.util.client, self.app_name, True, False)

    def add_test(self):
        """
        Method to add tests to the LTP suite
        :return: suite object
        """
        suite = TestSuite()
        # suite.addTest(LanguageSelection("test_country_selection"))
        suite.addTest(CountryLTP("test_country_ltp"))
        suite.addTest(EmgcyContactsLTP("test_emgcycontacts_ltp"))
        suite.addTest(MenuLTP("test_menuscreens"))
        suite.addTest(SmartReminderLTP("test_smartreminder"))
        suite.addTest(DayDividersLTP("test_daydividers"))
        suite.addTest(ExpandedGraphLTP("test_expgraph"))
        suite.addTest(TooltipLTP("test_tooltip"))
        suite.addTest(HCP("test_hcp_reports"))
        suite.addTest(HealthCare("test_healthcare"))
        suite.addTest(MeterSettings("test_meter_settings"))
        suite.addTest(NewReminder("test_new_reminder"))
        suite.addTest(Unpairing("test_unpairing"))
        suite.addTest(MeterHelp("test_meter_help"))
        suite.addTest(Apphelp("test_app_help"))
        suite.addTest(FAQ("test_faq"))
        suite.addTest(TargetRangesLTP("test_target_ranges"))
        suite.addTest(EditView("test_edit_view_ltp"))
        suite.addTest(MeterErrorCodes("test_meter_error_codes"))
        suite.addTest(EditEntry("test_edit_entry"))
        return suite

    def project_testcase_teardown(self):
        """Project level tear down"""
        # pass
        self.suitelogger.close_file()
        #self.scriptlogger.close_file()
        self.common.release_client(self.util.client)

def command_usage():
    """
    Help: Command usage
    :return:
    """
    print "LTP scripts need language as input"

if __name__ == "__main__":

    import ConfigParser
    CONF_PARSE = ConfigParser.ConfigParser()
    CONF_PARSE.read('language.ini')

    LANG = CONF_PARSE.get('Language', 'language')
    LANGLIST = LANG.split(',')

    for language in LANGLIST:
        Config.selected_language = language
        ltptest = LTPTests()
        ltptest.project_testcase_setup()
        ltptest.project_testcase_teardown()
        ltpsuite = ltptest.add_test()
        runner = TextTestRunner(verbosity=2)
        result = runner.run(ltpsuite)
        numberOfTestCases = result.testsRun
        numberOfTestCasesFailed = result.errors.__len__()
        numberOfTestCasesPassed = (ltpsuite.countTestCases() - result.errors.__len__())

        if result.wasSuccessful():
            print 0
        else:
            print -1

