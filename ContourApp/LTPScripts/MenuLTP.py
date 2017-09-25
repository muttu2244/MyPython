"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Menu
#                               Script Name    : MenuLTP.py
#                               Created On     : Jan 24 , 2017
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
from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Config, \
    Logger, Configuration


class MenuLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Menu screens on
    Android and iOS devices
    """

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
            # self.client.waitForDevice("@os='ios'",10000)
            self.app.launch(self.util.client, "com.onyx.-", True, True, self.logger_name)
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

    def test_menuscreens(self):
        """
        Main LTP test method to test Menu screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.mainmenu()
        self.myreadings()
        self.mypatterns()
        self.mycare()
        self.mysettings()
        self.help()
        self.myreminders()
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
            # self.util.client.sleep(1000)
            self.object.click(self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i][
                'index'], xpath[i]['comment'],
                              1, self.logger_name)

    def compare(self, xml_tag1, xml_tag2=""):
        """
        Generic method to fetch the text from the screen and compare the same with language xml
        :param xml_tag1, xml_tag2 - XML tags from objects.xml file to get the xpath of actual text.
        Same XML tag is used to read the language xml file to fetch the expected string for
        comparision
        :return:  None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        if xml_tag2 == "":
            xml_tag2 = xml_tag1
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag1,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag2,
                                                   self.my_object)
        self.logger.info("String verification: STARTED")
        self.util.client.sleep(1000)
        for i in range(0, len(xpath)):
            # self.util.client.sleep(1000)
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[i]))
            self.logger.info("English Text == " + eng_list[i])
            self.util.text_compare2(self.common, text_from_xml[i], element_text, ids[i],
                                    self.logger_name)

    def parse_and_compare(self, xml_tag):
        """
        This method gets the text from screen, splits with "(" and compares with the string from
        language xml. This repeats over a loop.
        :param xml_tag: XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        self.logger.info("String verification: STARTED")
        for i in range(0, len(xpath)):
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[i]))
            self.logger.info("English Text == " + eng_list[i])
            element_text = element_text.split("(")[0]
            self.util.text_compare2(self.common, text_from_xml[i], element_text, ids[i],
                                    self.logger_name)

    def parse_and_compare_for_help(self, xml_tag):
        """
        This method is mainly used for Help screen. It takes the list of words from language xml,
        joins them into a string. Then, gets the text from screen, adds them with the previous
        element to generate a string and then compared against the parsed string from language xml.
        :param xml_tag: XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        text_xml_str = "".join(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        self.logger.info("String verification: STARTED")
        element_str = ""
        for i in range(0, len(xpath)):
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[0]))
            self.logger.info("English Text == " + eng_list[0])
            element_str = element_str + element_text
        self.util.text_compare2(self.common, text_xml_str, element_str, ids[0], self.logger_name)

    def mainmenu(self):
        """
        This methods clicks the Menu icon and compare the items on the screen against language xml.
        If the actual string is equal to the expected string, both strings will be logged,
        else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("MainMenuClick")
        self.util.client.sleep(1000)
        self.compare("MainMenu")

    def myreadings(self):
        """
        This method compares the strings from My Readings screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMyReadings")
        self.util.client.sleep(1000)
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MyReadings",
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MyReadings",
                                                   self.my_object)
        for i in range(0, len(xpath)):
            if self.object.swipe_while_not_found(self.util.client, "Down", 500, 2000,
                                                 xpath[i]['zone'],
                                                 xpath[i]['xpath'],
                                                 xpath[i]['index'], xpath[i]['comment'], 1000, 25,
                                                 False, self.logger_name):
                pass
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)

            self.logger.info("Testing StringID == " + str(ids[i]))
            self.logger.info("English Text == " + eng_list[i])
            self.util.text_compare2(self.common, text_from_xml[i], element_text,
                                    ids[i], self.logger_name)

    def mypatterns(self):
        """
        This method compares the strings from My Patterns screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("MainMenuClick")
        xpath_patterns = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickMyPatterns",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_patterns[0]['zone'],
                                        xpath_patterns[0]['xpath'],
                                        xpath_patterns[0]['index'], xpath_patterns[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickMyPatterns")
        self.util.client.sleep(2000)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MyPatterns",
                                                   self.my_object)
        detected_pattern = self.object.is_element_found(self.util.client, xpath[1]['zone'],
                                                        xpath[1][
                                                            'xpath'],
                                                        xpath[1]['index'], xpath[1]['comment'],
                                                        self.logger_name)

        xpath_about = self.util.read_xpath_list_from_xml(self.object_repo, "CheckAboutPatterns",
                                                         self.my_object)
        about_pattern = self.object.is_element_found(self.util.client, xpath_about[0]['zone'],
                                                     xpath_about[0][
                                                         'xpath'],
                                                     xpath_about[0]['index'], xpath_about[0][
                                                         'comment'],
                                                     self.logger_name)

        if about_pattern:
            self.compare("AboutPatterns")
            self.clickbtn("BackButton")
            self.clickbtn("BackButton")
        elif detected_pattern:
            self.parse_and_compare("MyPatterns")
        else:
            self.compare("NoDetectedPatterns")

    def mycare(self):
        """
        This method compares the strings from My Care screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_mycare = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickMyCare",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_mycare[0]['zone'],
                                        xpath_mycare[0]['xpath'],
                                        xpath_mycare[0]['index'], xpath_mycare[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickMyCare")
        self.compare("MyCare")

    def mysettings(self):
        """
        This method compares the strings from Settings screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenuForSettings")
        xpath_settings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickMySettings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_settings[0]['zone'],
                                        xpath_settings[0]['xpath'],
                                        xpath_settings[0]['index'], xpath_settings[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickMySettings")
        self.compare("MySettings")

    def help(self):
        """
        This method compares the strings from Help screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenuForHelp")
        xpath_help = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickHelp",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_help[0]['zone'],
                                        xpath_help[0]['xpath'],
                                        xpath_help[0]['index'], xpath_help[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickHelp")
        self.compare("Help")
        self.parse_and_compare_for_help("Help1")

    def myreminders(self):
        """
        This method compares the strings from My Reminders screens against language xml. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenuForHelp")
        xpath_reminders = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ClickMyReminders",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_reminders[0]['zone'],
                                        xpath_reminders[0]['xpath'],
                                        xpath_reminders[0]['index'], xpath_reminders[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickMyReminders")
        self.util.client.sleep(1000)
        xpath1 = self.util.read_xpath_list_from_xml(self.object_repo, "MyReminders1",
                                                    self.my_object)
        emptyreminders = self.object.is_element_found(self.util.client, xpath1[1]['zone'],
                                                      xpath1[1]['xpath'], xpath1[1]['index'],
                                                      xpath1[1]['comment'], self.logger_name)
        if emptyreminders:
            self.compare("MyReminders1")

        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo, "MyReminders2",
                                                    self.my_object)
        reminders = self.object.is_element_found(self.util.client, xpath2[1]['zone'], xpath2[1][
            'xpath'],
                                                 xpath2[1]['index'], xpath2[1]['comment'],
                                                 self.logger_name)
        emptytestreminders = self.object.is_element_found(self.util.client, xpath2[3]['zone'],
                                                          xpath2[3]['xpath'], xpath2[3]['index'],
                                                          xpath2[3]['comment'], self.logger_name)
        if reminders and emptytestreminders:
            self.compare("MyReminders2")

        xpath3 = self.util.read_xpath_list_from_xml(self.object_repo, "MyReminders3",
                                                    self.my_object)
        customreminders = self.object.is_element_found(self.util.client, xpath3[2]['zone'],
                                                       xpath3[2]['xpath'], xpath3[2]['index'],
                                                       xpath3[1]['comment'], self.logger_name)
        if customreminders:
            self.compare("MyReminders3")

        xpath4 = self.util.read_xpath_list_from_xml(self.object_repo, "ReminderElements",
                                                    self.my_object)
        custreminders = self.object.is_element_found(self.util.client, xpath4[0]['zone'],
                                                     xpath4[0]['xpath'], xpath4[0]['index'],
                                                     xpath4[1]['comment'], self.logger_name)
        testreminders = self.object.is_element_found(self.util.client, xpath4[1]['zone'],
                                                     xpath4[1]['xpath'], xpath4[1]['index'],
                                                     xpath4[1]['comment'], self.logger_name)
        if custreminders and testreminders:
            self.compare("MyReminders4")

    def goto_home(self):
        """
        Method to traverse to Home screen
        :param: None
        :return: None
        """
        self.clickbtn("GotoHome")

    def tearDown(self):
        self.common.generate_report(self.util.client, False)
        self.common.release_client(self.util.client)
        self.logger.info("==============Results=================")
        self.logger.info("Number of Strings verified: " + str(len(Config.results_list)/2))
        for i in range(0, len(Config.results_list), 2):
            self.logger.info(str(Config.results_list[i]) + "{:>36}".format('=====> ')
                             + str(Config.results_list[i+1]))
        self.logger.info("Testcase tear-down: COMPLETED")

if __name__ == '__main__':
    unittest.main()
