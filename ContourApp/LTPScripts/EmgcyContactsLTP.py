"""Base version 1.9.44 used"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Emergency Contacts
#                               Script Name    : EmgcyContactsLTP.py
#                               Created On     : Jan 18 , 2017
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
    Configuration, Config


class EmgcyContactsLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Emergency contacts screens on
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

    def test_emgcycontacts_ltp(self):
        """
        Main LTP test method to test Emergency contacts screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.emgcy_contacts()

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
            self.object.click(self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                              xpath[i]['index'],
                              xpath[i]['comment'], 1, self.logger_name)

    def compare(self, xml_tag):
        """
        Generic method to fetch the text from the screen and compare the same with language xml
        :param: xml_tag - XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag, "trans-unit",
                                                    Config.selected_language)
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

    def goto_emgcy_contact_screen(self):
        """
        This methods navigates to "Emergency contacts" main screen and compare the strings on
        that screen against the Language xml. . If the actual string is equal to the expected
        string, both strings will be logged, else the corresponding failed word will be logged
        with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("MenutoMyCare")
        xpath_mycare = self.util.read_xpath_list_from_xml(self.object_repo, "ClickMyCare",
                                                          self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_mycare[0]['zone'],
                                        xpath_mycare[0]['xpath'],
                                        xpath_mycare[0]['index'], xpath_mycare[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ClickMyCare")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "CheckEmgcy",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 15000,
                                        self.logger_name):
            pass
        self.clickbtn("ClickEmgcyContact")
        self.util.client.sleep(1000)
        self.compare("EmgcyMainScreen")

    def goto_local_emgcynum_screen(self):
        """
        This method navigates to "Local Emergency Number" screen and compares the strings on the
        screen against language xml. . If the actual string is equal to the expected string, both
        strings will be logged, else the corresponding failed word will be logged with result
        as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickLocalEmgcyNum")
        self.compare("EmgcyScreen1")
        self.clickbtn("ClickBackBtn")

    def goto_custom_emgcy_screen(self):
        """
        This method navigates to the "Custom emergency number" screen and compares the  relevant
        strings on the screen against language xml. . If the actual string is equal to the
        expected string, both strings will be logged, else the corresponding failed word will be
        logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickCustEmgcyNum")
        self.compare("EmgcyScreen2")
        if self.my_object == "Iobject":
            self.dev.close_keyboard(self.util.client)
            pixel = self.dev.p2cy(self.util.client, 80)
            self.dev.swipe(self.util.client, "Up", pixel, 300)
        self.clickbtn("ClickBackBtn1")

    def goto_choose_contact_screen(self):
        """
        This method navigates to the "Choose an existing contact" screen, waits until the screen
        is visible and compares the  relevant strings on the screen against language xml. Once
        done, navigate back to the previous screen. . If the actual string is equal to the expected
        string, both strings will be logged, else the corresponding failed word will be logged
        with result as fail.
        :param: None
        :return: None
        """
        self.compare("EmgcyScreen3")
        self.clickbtn("ClickExistingContact")
        self.util.client.sleep(2000)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "WaitForContactScreen",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 400000  ,
                                        self.logger_name):
            print "found"

        # self.util.client.sleep(2000)
        self.compare("EmgcyScreen4")
        xpathclickcontact = self.util.read_xpath_list_from_xml(self.object_repo,
                                                               "ClickAContact",
                                                               self.my_object)
        count = len(xpathclickcontact)
        if self.object.is_element_found(self.util.client, xpathclickcontact[0]['zone'],
                                        xpathclickcontact[0]['xpath'],
                                        xpathclickcontact[0]['index'], xpathclickcontact[0][
                                            'comment'], self.logger_name):
            for i in range(0, count):
                self.object.click(self.util.client, xpathclickcontact[i]['zone'],
                                  xpathclickcontact[i]['xpath'], xpathclickcontact[i]['index'],
                                  xpathclickcontact[i]['comment'], 1, self.logger_name)
            self.compare("EmgcyScreen5")
            self.clickbtn("ClickNum")
            self.clickbtn("ClickBackBtn")

        else:
            for i in range(0, 3):
                self.clickbtn("ClickBackBtn")

    def goto_manual_contact_screen(self):
        """
        Method to traverse to manual contact screen
        :param: None
        :return: None
        """
        self.clickbtn("ClickManualContact")
        self.compare("EmgcyScreen2")
        self.clickbtn("ClickBackBtn1")
        for i in range(0, 2):
            self.clickbtn("ClickBackBtn")
            self.clickbtn("ClickBackBtn")

    def emgcy_contacts(self):
        """
        Main method to check all the screens. For each string element on the screen, which is
        ACTUAL STRING, is compared with target string in the language XML that is EXPECTED.
        :param: None
        :return: None
        """
        self.goto_emgcy_contact_screen()
        self.goto_local_emgcynum_screen()
        self.goto_custom_emgcy_screen()
        self.goto_choose_contact_screen()
        # self.goto_manual_contact_screen()
        self.goto_home()

    def goto_home(self):
        """
        Method to traverse to home screen
        :param: None
        :return: None
        """
        self.util.client.sleep(1000)
        self.clickbtn("GotoHome")

    def tearDown(self):
        # Generates a report of the test case.
        # For more information-https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test
        self.common.generate_report(self.util.client, False)
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
