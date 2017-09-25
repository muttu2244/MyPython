"""module"""
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


# *********************************************************************************
# *********************************************************************************
#                               System Map Name: Meter ERROR code
#                               Script Name : eter ERROR code
#                               Created On: jan 7 , 2017
#                               Created By:Umesha HP (10065170)
# ***********************************************************************************
# ************************************************************************************

class MeterErrorCodes(unittest.TestCase):
    """ Based on python's pyunit (unittest) framework this TestCase verifies Language
    Translations for Meter Error Codes on ContourApp on both Android and IOS Devices"""

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

    def test_meter_error_codes(self):
        """ This is Unit test frame work INI method where the test framework calls other methods"""
        self.to_meter_code()  # This function will take the system from Home screen to meter Help
        self.error_code()
        self.headings()

    def to_meter_code(self):
        """ This Method will take the system from Home screen to Meter Error
        codes screen get Xpath and navigate to Meter Error codes screen.
        # This function will take the system from Home screen to meter error code  it returns
        None """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "toMeterError",
                                                   self.my_object)
        for loop_index in range(len(xpath)):
            if self.my_object == "Iobject":
                self.util.client.sleep(2500)
            self.object.wait_for_element(self.util.client,
                                         xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'], xpath[loop_index]['comment'],
                                         20000, self.logger_name)
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'],
                              xpath[loop_index]['comment'],
                              1, self.logger_name)

    def error_code(self):
        """ This Method navigates and tests all the strings which are clickable strings.
        It gets strings as actual_text and get the screen text as element strings and call the
        function compare. If the actual string is equal to the expected string both string will
        be logged else corresponding words will be logged as result fail.It returns None"""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "TestingErrors", "trans-unit",
                                                                   Config.selected_language.strip())

        xpath_main = self.util.read_xpath_list_from_xml(self.object_repo, "MainScreen",
                                                        self.my_object)
        xpath_screen2 = self.util.read_xpath_list_from_xml(self.object_repo, "Screen2",
                                                           self.my_object)
        xpath_single = self.util.read_xpath_list_from_xml(self.object_repo, "ErrorCodeSingle",
                                                          self.my_object)
        xpath = xpath_single[0]['xpath']  # xpath ita a class x path
        index = xpath_single[0]['index']  # it requires to increemnt the index by one to get the
        # next class x path
        zone = xpath_single[0]['zone']  # this zone is same for all elements that is WEB zone
        comment = xpath_single[0]['comment']
        text_index = 0
        # list_index = [9, 15, 26, 28, 41]  # list index
        for loop_index in range(2):
            # self.util.client.sleep(1000)
            print "index " + str(loop_index)
            if loop_index == 1:
                element_text = self.object.element_get_property(self.util.client,
                                                                xpath_main[loop_index]['zone'],
                                                                xpath_main[loop_index]['xpath'],
                                                                xpath_main[loop_index]['index'],
                                                                "placeholder", self.logger_name)
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                if element_text:
                    self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                            self.logger_name)
                text_index += 1
                continue
            else:
                self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
                text_index += 1
        for loop_index in range(41):
            print " inside error code"
            if index == 7:
                self.dev.swipe(self.util.client, "Down", 850, 500)
            element_text = self.common.element_get_text(self.util.client, zone, xpath, comment,
                                                        self.logger_name, index)
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                    self.logger_name)
            self.object.click(self.util.client, zone, xpath, index, comment, 1, self.logger_name)
            pixel = self.dev.p2cy(self.util.client, 15)
            self.dev.swipe(self.util.client, "Up", pixel, 300)
            index += 1
            text_index += 1
            for j in range(2):
                self.get_text_compare(xpath_screen2, j, text_from_xml, text_index, ids, eng_list)
                text_index += 1
            self.object.click(self.util.client, xpath_screen2[2]['zone'],
                              xpath_screen2[2]['xpath'],
                              xpath_screen2[2]['index'],
                              xpath_screen2[2]['comment'],
                              1, self.logger_name)

    def headings(self):
        """ headings There are heading strings like communication error , software error,
        hardware error etc. it returns None """
        actual_text, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Headings", "trans-unit",
                                                                 Config.selected_language.strip())
        print len(actual_text)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Headings", self.my_object)
        text_index = 0  # index to the actual text
        for loop_index in range(len(xpath)):
            self.get_text_compare(xpath, loop_index, actual_text, text_index, ids, eng_list)
            text_index += 1

    def get_text_compare(self, xpaths, xpath_index, text_from_xml, text_index, ids, eng_list):
        """ This method gets Xpath of the object and  actual text ,
        get the screen text by calling get_element_text() method and passes to compare2() method
        for comparison. If the actual string is equal to the expected string both string will be
        logged else the corresponding words will be logged as result fail. Finally it returns
        None"""
        try:
            element_text = self.common.element_get_text(self.util.client,
                                                        xpaths[xpath_index]['zone'],
                                                        xpaths[xpath_index]['xpath'],
                                                        xpaths[xpath_index]['comment'],
                                                        self.logger_name,
                                                        xpaths[xpath_index]['index'])
            if element_text is None:
                element_text = self.object.element_get_property(self.util.client,
                                                                xpaths[xpath_index]['zone'],
                                                                xpaths[xpath_index]['xpath'],
                                                                xpaths[xpath_index]['index'],
                                                                "text", self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            if element_text:
                self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
        except:
            print " Xpath doesn't found due some hidden text"

    def go_home(self):
        """ go_home"""
        xpath_go_home = self.util.read_xpath_list_from_xml(self.object_repo, "GoHome",
                                                           self.my_object)
        print xpath_go_home
        for loop_index in range(0, len(xpath_go_home)):
            print loop_index
            self.object.click(self.util.client, xpath_go_home[loop_index]['zone'],
                              xpath_go_home[loop_index]['xpath'],
                              xpath_go_home[loop_index]['index'], 1)

    def tearDown(self):
        """Generates a report of the test case.
        For more information - https://docs.experitest.com/display/public/SA/Report+Of+Executed
        +Test"""

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
