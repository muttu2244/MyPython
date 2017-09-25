""" this module does LTP of Meter Settings"""
# -*- coding: utf-8 -*-
# encoding=utf8
import os
import sys
import logging
import unittest

reload(sys)
sys.setdefaultencoding('utf8')
SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
print SYS_PATH

from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Logger, \
    Configuration, Config


# **********************************************************************************
# **********************************************************************************
#                               System Map Name: Meter Settings
#                               Script Name : MeterSettingsLTP.py
#                               Created On: jan 25, 2016
#                               Created By:Umesha HP (10065170)
#                               APP version :1.9.44 3551
# ************************************************************************************
# ***********************************************************************************

class MeterSettings(unittest.TestCase):
    """ Based on python's pyunit (unittest) framework this TestCase verifies Language
    Translations for Meter Settings on both android, iOS Devices."""

    def setUp(self):
        """UnitTest Frame work method """
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

    def test_meter_settings(self):
        """ default test framework method """
        print " i am in start"
        self.to_meter_settings()
        # This function will take the system from Home screen to meter Help
        self.verify()
        # if self.my_object == "Iobject":
        #     self.go_home()

    def to_meter_settings(self):
        """ This Method will take the system from Home screen to Meter settings screen."""
        # This function will take the system from Home screen to App Help
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToMeter", self.my_object)
        for loop_index in range(len(xpath)):
            self.object.wait_for_element(self.util.client,
                                         xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'], xpath[loop_index]['comment'],
                                         20000, self.logger_name)
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                              self.logger_name)

    def verify(self):
        """ This Method navigates and tests all the strings which are present in the screen.
        It gets strings as actual_text and get the screen text as element strings and call the
        function compare. If the actual string is equal to the expected string both string will
        be logged else the corresponding words will be logged as result fail. It returns none. """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MeterSettings", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MeterSettings",
                                                   self.my_object)
        len_main = len(xpath)
        text_index = 0
        loop_index = 0
        j = 0  # index for concat string in object xml
        while loop_index < len_main:
            if xpath[loop_index]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'], xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == "popup":
                self.popup()
                loop_index += 1
                continue
            if xpath[loop_index]['xpath'] == 'concat':
                self.concat(xpath, loop_index, j, text_from_xml, text_index, ids, eng_list)
                j += 1  # index to
                loop_index += 2
                text_index += 1
                print loop_index
                continue
            self.object.wait_for_element(self.util.client, xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'],
                                         xpath[loop_index]['comment'],
                                         100000, self.logger_name)
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def popup(self):
        """(): This Method  is to handle the popup screen at very first time/ sometime this pop up
         screen appears very rarely whenever it appears  this method  handles this screen .
         It gets strings as actual_text and get the screen text as element strings and call the
         method compare. If the actual string is equal to the expected string both string will be
          logged else the corresponding words will be logged as result fail. It returns none."""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "PopUp", self.my_object)
        len_main = len(xpath)
        print len_main
        if self.object.is_element_found(self.util.client, xpath[1]['zone'], xpath[1]['xpath'],
                                        xpath[1]['index'], xpath[1]['comment'],
                                        self.logger_name) and \
                self.object.is_element_found(self.util.client, xpath[2]['zone'],
                                             xpath[2]['xpath'], xpath[1]['index'],
                                             xpath[2]['comment'], self.logger_name):
            self.object.click(self.util.client, xpath[2]['zone'],
                              xpath[2]['xpath'],
                              xpath[2]['index'],
                              xpath[2]['comment'],
                              1, self.logger_name)
            self.util.client.sleep(3000)
            self.object.wait_for_element_to_vanish(self.util.client, xpath[3]['zone'],
                                                   xpath[3]['xpath'], xpath[3]['index'],
                                                   xpath[3]['comment'], 500000, self.logger_name)

    def concat(self, *args):
        """ This method concatenates  the two separate string which are return by the see test
        get_element_text and compare against single string in master string.  It returns none."""
        xpath, loop_index, j, text_from_xml, text_index, ids, eng_list = args
        string1 = self.common.element_get_text(self.util.client,
                                               xpath[loop_index + 1]['zone'],
                                               xpath[loop_index + 1]['xpath'],
                                               xpath[loop_index + 1]['comment'],
                                               self.logger_name,
                                               xpath[loop_index + 1]['index'])
        string2_xpath = self.util.read_xpath_list_from_xml(self.object_repo,
                                                           "Concat",
                                                           self.my_object)
        string2 = self.common.element_get_text(self.util.client,
                                               string2_xpath[j]['zone'],
                                               string2_xpath[j]['xpath'],
                                               xpath[j]['comment'],
                                               self.logger_name,
                                               string2_xpath[j]['index'])
        element_text = string1 + string2
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        if element_text:
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                    self.logger_name)

    def go_home(self):
        """ go home"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "GoHome", self.my_object)
        for loop_index in range(len(xpath)):
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                              self.logger_name)

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
        if element_text:
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                    self.logger_name)

    def tearDown(self):
        """" Generates a report of the test case.
        For more information - https://docs.experitest.com/
        display/public/SA/Report+Of+Executed+Test """
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
