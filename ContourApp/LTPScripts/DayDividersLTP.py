"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

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


class DayDividersLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Day Dividers screens on
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

    def test_daydividers(self):
        """
        Main LTP test method to test Day Dividers screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.goto_daydividers()
        self.daydivscreens()
        self.brkfastscreen()
        self.lunchscreen()
        self.dinnercreen()
        self.overnightscreen()
        self.util.client.sleep(1000)
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
        if xml_tag2 == "":
            xml_tag2 = xml_tag1
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag1, "trans-unit",
                                                    Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag2,
                                                   self.my_object)
        self.util.client.sleep(1000)
        self.logger.info("String verification: STARTED")
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
        This method first splits the strings from language xml(specially for time) with "-" and
        stores it in a list. Gets the text from screen(for time), splits with ":", convert them
        to 12 hour format if it is not already, adds PM/AM accordingly and compares with the
        parsed string from language xml.
        :param xml_tag: XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag, "trans-unit",
                                                    Config.selected_language.strip())
        text_from_xml = [x.split("-") for x in text_from_xml]
        text_xml = reduce(lambda xx, yy: xx + yy, text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        for i in range(0, len(xpath)):

            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[0]))
            self.logger.info("English Text == " + eng_list[0])
            element_text1 = element_text.split(":")[0]
            element_text2 = element_text.split(":")[1]
            if 2 < len(element_text2) < 5:
                val = element_text2[2] + element_text2[3]
            elif len(element_text2) >= 5:
                val = element_text2[2] + element_text2[3] + element_text2[4] + element_text2[5]
            else:
                val = ""
            if int(element_text1) > 12:
                new = int(element_text1) - 12
                if val == "p.m." or val == "":
                    val = "PM"
                    # elif val == "p.m.":
                    # val = "PM"
                element_text = str(new) + ":" + "00" + val
            elif int(element_text1) == 12:
                val = "PM"
                element_text = str(int(element_text1)) + ":" + "00" + val
            else:
                if val == "a.m." or val == "":
                    val = "AM"
                elif val == "p.m." or val == "":
                    val = "PM"
                element_text = str(int(element_text1)) + ":" + "00" + val

            self.util.text_compare2(self.common, text_xml[i], element_text, ids[0],
                                    self.logger_name)

    def goto_daydividers(self):
        """
        Method to navigate to Day Divider screen
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_mycare = self.util.read_xpath_list_from_xml(self.object_repo, "GotoMyCare",
                                                          self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_mycare[0]['zone'],
                                        xpath_mycare[0]['xpath'],
                                        xpath_mycare[0]['index'], xpath_mycare[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("GotoMyCare")

        xpath_daydiv = self.util.read_xpath_list_from_xml(self.object_repo, "DayDiv",
                                                          self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_daydiv[0]['zone'],
                                        xpath_daydiv[0]['xpath'],
                                        xpath_daydiv[0]['index'], xpath_daydiv[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("DayDiv")

    def daydivscreens(self):
        """
        This method  compares the strings from Day Dividers main screen against language xml.
        Then takes up day dividers time, calls parse_and_compare() to parse and compare them with
        language xml. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.compare("DayDividerScreen")
        self.parse_and_compare("DayDividerScreen1")

    def brkfastscreen(self):
        """
        This method navigates to Breakfast screen, compares the strings against the language xml.
        Changes the time, and then compares the strings, navigates to tooltip, parses them and
        compare against the language xml. If the actual string is equal to the expected string,
        both strings will be logged, else the corresponding failed word will be logged with
        result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickBreakfast")
        self.compare("BrkfastScreen1")
        self.parse_and_compare("BrkfastScreen2")
        xpath1 = self.util.read_xpath_list_from_xml(self.object_repo,
                                                    "BrkfastSwipeUpperLimit",
                                                    self.my_object)
        self.object.element_swipe(self.util.client, xpath1[0]['zone'], xpath1[0]['xpath'],
                                  xpath1[0]['index'], xpath1[0]['comment'], "Right", 0, 2000,
                                  self.logger_name)
        self.compare("BrkfastScreen3")
        self.parse_and_compare("BrkfastScreen4")
        self.object.element_swipe(self.util.client, xpath1[0]['zone'], xpath1[0]['xpath'],
                                  xpath1[0]['index'], xpath1[0]['comment'], "Left", 0, 2000,
                                  self.logger_name)

        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo,
                                                    "BrkfastSwipeLowerLimit",
                                                    self.my_object)
        self.object.element_swipe(self.util.client, xpath2[0]['zone'], xpath2[0]['xpath'],
                                  xpath2[0]['index'], xpath2[0]['comment'], "Down", 50, 2000,
                                  self.logger_name)
        self.compare("BrkfastScreen5")
        self.parse_and_compare("BrkfastScreen6")
        for i in range(0, 3):
            self.object.element_swipe(self.util.client, xpath2[0]['zone'], xpath2[0]['xpath'],
                                      xpath2[0]['index'], xpath2[0]['comment'], "Up", 50, 5000,
                                      self.logger_name)
        xpath3 = self.util.read_xpath_list_from_xml(self.object_repo, "BrkfastSpan",
                                                    self.my_object)
        span = self.object.is_element_found(self.util.client, xpath3[0]['zone'], xpath3[0]['xpath'],
                                            xpath3[0]['index'], xpath3[0]['comment'],
                                            self.logger_name)
        if span:
            self.compare("BrkfastSpan")

        for i in range(0, 2):
            self.object.element_swipe(self.util.client, xpath2[0]['zone'], xpath2[0]['xpath'],
                                      xpath2[0]['index'], xpath2[0]['comment'], "Down", 50, 5000,
                                      self.logger_name)
        self.clickbtn("ClickInfo")
        self.compare("DayDividerPopup")
        self.clickbtn("CloseInfoNBack")

    def lunchscreen(self):
        """
        This method navigates to Lunch screen, compares the strings against the language xml.
        Navigates to the tooltip, parses them and compare against the language xml. If the actual
        string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickLunch")
        self.compare("LunchScreen1")
        self.parse_and_compare("LunchScreen2")
        self.clickbtn("ClickInfo")
        self.compare("DayDividerPopup")
        self.clickbtn("CloseInfoNBack")

    def dinnercreen(self):
        """
        This method navigates to Dinner screen, compares the strings against the language xml.
        Navigates to the tooltip, parses them and compare against the language xml. If the actual
        string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickDinner")
        self.compare("DinnerScreen1")
        self.parse_and_compare("DinnerScreen2")
        self.clickbtn("ClickInfo")
        self.compare("DayDividerPopup")
        self.clickbtn("CloseInfoNBack")

    def overnightscreen(self):
        """
        This method navigates to Overnight screen, compares the strings against the language xml.
        Navigates to the tooltip, parses them and compare against the language xml. If the actual
        string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickOvernight")
        self.compare("OvernightScreen1")
        self.parse_and_compare("OvernightScreen2")
        self.clickbtn("ClickInfo")
        self.compare("DayDividerPopup")
        self.clickbtn("CloseInfoNBack")

    def goto_home(self):
        """
        Method to traverse to Home screen
        :param: None
        :return: None
        """
        self.clickbtn("GotoHome")
        xpath_home = self.util.read_xpath_list_from_xml(self.object_repo, "Home",
                                                          self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_home[0]['zone'],
                                        xpath_home[0]['xpath'],
                                        xpath_home[0]['index'], xpath_home[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("Home")

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
