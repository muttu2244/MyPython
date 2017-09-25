"""hcp reports"""
# -*- coding: utf-8 -*-
# encoding=utf8
import os
import sys
import unittest
import logging

reload(sys)
sys.setdefaultencoding('utf8')
SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
print SYS_PATH

from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Logger, \
    Configuration, Config

# ********************************************************************************
#  *******************************************************************************
#                               System Map Name: HCP Report
#                               Script Name : HCPReportLTP.py
#                               Created On: jan 12 , 2016
#                               Updated On: Mar 20 2017
#                               Created By:Umesha HP (10065170)
#                               APP version :1.9.44 3551
# *********************************************************************************
# *********************************************************************************
class HCP(unittest.TestCase):
    """ this class dose HCP reports"""

    def setUp(self):
        self.util = Utility()
        self.common = Common()
        self.misc = Misc()
        self.dev = Device()
        self.app = Application()
        self.object = Objects()
        self.navigate = Navigate()
        self.config = Configuration()
        self.util.set_up()

        if Config.selected_language == "":
            Config.selected_language = "english"
        self.logger_name = os.path.splitext(os.path.basename(__file__))[0] + \
                           Config.selected_language.strip()
        self.logger = Logger.Logger(self.logger_name)
        self.logger = logging.getLogger(self.logger_name)

        self.logger.info("=======================================================")
        self.logger.info("Script name: " + os.path.splitext(os.path.basename(__file__))[0] + ".py")
        self.logger.info("=======================================================")
        self.logger.info("TestCase set-up: STARTED")
        self.string_xml = self.util.open_xml(
            os.path.splitext(os.path.basename(__file__))[0] + ".xml")
        self.object_repo = self.util.open_xml(
            os.path.splitext(os.path.basename(__file__))[0] + "Objects.xml")

        self.device_name = self.dev.get_connected_devices(self.util.client)
        self.misc.set_device(self.util.client,
                             self.device_name,
                             self.logger_name)  # connect only one device with system
        self.device_info_path = self.misc.get_devices_information(self.util.client,
                                                                  SYS_PATH,
                                                                  self.device_name,
                                                                  self.logger_name)
        self.app_name = self.util.get_app_name(self.device_info_path, self.device_name)
        self.app.launch(self.util.client, self.app_name, True, True, self.logger_name)
        print self.device_name

        if self.device_name.find("iPhone") > 0:
            self.app.launch(self.util.client, "search:contour", True, True, self.logger_name)
            self.my_object = "Iobject"
        else:
            self.my_object = "Aobject"
            self.app_name = self.util.get_app_name(self.device_info_path, self.device_name)
            self.app.launch(self.util.client, self.app_name, True, False, self.logger_name)
        print self.my_object
        self.common.set_project_base_directory(self.util.client, os.getcwd(), self.logger_name)
        self.common.set_reporter(self.util.client, SYS_PATH,
                                 os.path.splitext(os.path.basename(__file__))[0], self.logger_name)
        self.config.set_show_pass_image_in_report(self.util.client, False)
        Config.results_list = []

    def test_hcp_reports(self):
        """ test call This function is unitTest Default method from where the execution starts"""
        self.to_hcp()  # This function will take the system from Home screen to meter Help
        self.hcp_report()

    def to_hcp(self):
        """hcp This function will take the system from Home screen to App Help"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToHCPReport", self.my_object)
        for i in range(len(xpath)):
            if self.my_object =="Iobject":
                self.util.client.sleep(2500)
            self.object.wait_for_element(self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                                         xpath[i]['index'], xpath[i]['comment'], 10000,
                                         self.logger_name)
            self.object.click(self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                              xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)

    def hcp_report(self):
        """ hcp reports this Method compares HCP reports text string """
        print "In HCP report"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "HCPReport",
                                                  "trans-unit",
                                                  Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MainScreen", self.my_object)
        len_main = len(xpath)
        text_index = 0  # index to the Actual string
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.object.wait_for_element(self.util.client, xpath[i + 1]['zone'],
                                             xpath[i + 1]['xpath'],
                                             xpath[i + 1]['index'], xpath[i + 1]['comment'], 10000,
                                             self.logger_name)
                if self.object.is_element_found(self.util.client, xpath[i + 1]['zone'],
                                                xpath[i + 1]['xpath'],
                                                xpath[i + 1]['index'], xpath[i + 1]['comment'],
                                                self.logger_name):
                    self.object.click(self.util.client, xpath[i + 1]['zone'], xpath[i + 1]['xpath'],
                                      xpath[i + 1]['index'], xpath[i + 1]['comment'], 1,
                                      self.logger_name)
                i += 2
                continue
            if xpath[i]['xpath'] == 'text':
                self.object.element_send_text(self.util.client, xpath[i + 1]['zone'],
                                              xpath[i + 1]['xpath'], xpath[i + 1]['index'])
                self.util.client.sleep(5000)
                i += 2
                continue
            self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def get_text_compare(self, xpaths, xpath_index, text_from_xml, text_index, ids, eng_list):
        """ This method takes xpath and xxpath inxex and get the
        text from the device using elementGetText method and compare the actual string  against
        device text """
        element_text = self.common.element_get_text(self.util.client, xpaths[xpath_index]['zone'],
                                                    xpaths[xpath_index]['xpath'],
                                                    xpaths[xpath_index]['comment'],
                                                    self.logger_name,
                                                    xpaths[xpath_index]['index'])
        if element_text is None:
            element_text = self.object.element_get_property(self.util.client,
                                                            xpaths[xpath_index]['zone'],
                                                            xpaths[xpath_index]['xpath'],
                                                            xpaths[xpath_index]['index'], "text",
                                                            self.logger_name)
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        if element_text :
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                self.logger_name)

    def tearDown(self):
        """ Generates a report of the test case.
        # For more information-https://docs.experitest.com/display/public/SA/Report+Of+Executed
        +Test """
        self.app.application_close(self.util.client, self.app_name)

        self.common.generate_report(self.util.client, False)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)
        self.common.release_client(self.util.client)
        self.logger.info("==============Results=================")
        self.logger.info("Number of Strings verified: " + str(len(Config.results_list)/2))
        for i in range(0, len(Config.results_list), 2):
            self.logger.info(str(Config.results_list[i]) + "{:>36}".format('=====> ')
                             + str(Config.results_list[i+1]))
        self.logger.info("Testcase tear-down: COMPLETED")


if __name__ == '__main__':
    unittest.main()
