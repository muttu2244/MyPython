"""  Base version used 1.9.44 """
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Country and Language
#                               Script Name    : CountryLTP.py
#                               Created On     : Jan 17 , 2017
#                               Created By     : Sharath R (341247)
#                               APP version    : 1.9.44
# **********************************************************************
# **********************************************************************

import sys
import os
import unittest
import logging

reload(sys)
sys.setdefaultencoding('utf8')

SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Logger, \
    Config, Configuration


class CountryLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Country and Language screens on
    Android and iOS devices
    """

    # def __init__(self):
    #     pass

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
        # self.util.create_log_file(SYS_PATH,
        #                           os.path.splitext(os.path.basename(__file__))[
        #                               0], Config.selected_language.strip())  # creating logs file
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
            self.app.launch(self.util.client, self.app_name, True, True, self.logger_name)
        print self.my_object
        self.common.set_project_base_directory(self.util.client, os.getcwd(), self.logger_name)
        self.common.set_reporter(self.util.client, SYS_PATH,
                                 os.path.splitext(os.path.basename(__file__))[0], self.logger_name)
        self.config.set_show_pass_image_in_report(self.util.client, False)
        Config.results_list = []

    def test_country_ltp(self):
        """
        Main LTP test method to test Country and Language screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.goto_country_langscreen()
        self.goto_country_screen()
        self.goto_lang_screen()
        self.goto_home()

    def clickbtn(self, xml_tag):
        """
        Generic method for all click events
        :param: xml_tag - XML tag from objects.xml file to get the xpath to click
        :return: None
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        # self.util.client.sleep(1000)
        count = len(xpath)
        for i in range(0, count):
            self.util.client.sleep(1000)
            self.object.click(self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i][
                'index'], xpath[i]['comment'], 1, self.logger_name)

    def compare(self, xml_tag):
        """
        Generic method to fetch the text from the screen and compare the same with language xml
        :param: xml_tag - XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                              "trans-unit",
                                                    Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        # self.util.client.sleep(1000)
        self.logger.info("String verification: STARTED")
        for i in range(0, len(xpath)):
            # self.util.client.sleep(1000)
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)

            self.logger.info("Testing StringID == " + str(ids[i]))
            self.logger.info("English Text == " + eng_list[i])
            self.util.text_compare(self.util.client, self.common, text_from_xml[i], element_text,
                                   ids[i], self.logger_name)

    def goto_country_langscreen(self):
        """
        Method to navigate to Country and Language main screen
        and compare the strings on that screen against the language xml.If the actual string is
        equal to the expected string, both strings will be logged, else the corresponding failed
        word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("MenutoSettings")
        xpath_settings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickSettings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_settings[0]['zone'],
                                        xpath_settings[0]['xpath'],
                                        xpath_settings[0]['index'], xpath_settings[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickSettings")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ClickCountryLang",
                                                   self.my_object)
        if (self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                         xpath[0]['index'], xpath[0]['comment'], 10000,
                                         self.logger_name)):
            pass
        self.clickbtn("ClickCountryLang")
        self.compare("CountryMainScreen")

    def goto_country_screen(self):
        """
        Method to navigate to Country screen and compares the strings on the screen against
        language xml. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickCountry")
        self.compare("CountryRegionScreen")
        self.clickbtn("ClickRegBackBtn")

    def goto_lang_screen(self):
        """
        Method to navigate to the Language screen and compares the relevant strings on the screen
        against language xml. If the actual string is equal to the expected string, both strings
        will be logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickLang")
        self.compare("LangScreen")
        self.clickbtn("ClickLangBackBtn")
        self.clickbtn("ClickBackBtn")

    def goto_home(self):
        """
        Method to traverse to Home screen
        :param: None
        :return: None
        """
        self.util.client.sleep(1000)
        self.clickbtn("GotoHome")

    def tearDown(self):
        # Generates a report of the test case.
        # For more information-https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test
        self.app.application_close(self.util.client, self.app_name)
        self.common.generate_report(self.util.client, True)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)
        self.logger.info("==============Results=================")
        self.logger.info("Number of Strings verified: " + str(len(Config.results_list)/2))
        for i in range(0, len(Config.results_list), 2):
            self.logger.info(str(Config.results_list[i]) + "{:>36}".format('=====> ')
                             + str(Config.results_list[i+1]))
        self.logger.info("Testcase tear-down: COMPLETED")


if __name__ == '__main__':
    unittest.main()
