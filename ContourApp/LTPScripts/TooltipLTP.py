"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Tooltip
#                               Script Name    : TooltipLTP.py
#                               Created On     : Feb 08 , 2017
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


class TooltipLTP(unittest.TestCase):
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

    def test_tooltip(self):
        """
        Main LTP test method to test Tooltip screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        # if self.device_name.split(":")[1].strip() != "MotoG3-TE":
        self.readings()
        self.reminders()
        self.targetranges()
        self.daydividers()
        self.healthcare()
        self.appointments()
        self.mymeters()

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
                'index'], xpath[i]['comment'],
                              1, self.logger_name)

    def compare(self, xml_tag):
        """
        Generic method to fetch the text from the screen and compare the same with language xml
        :param xml_tag - XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return:  None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        # self.util.client.sleep(1000)
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
        This method joins the list of strings from language xml. The gets the text from screen.
        If the element starts with ")" or ends with "(", append the text to element string (
        initially empty) along with a space. Compare the parsed string from language xml with the
        element string.
        :param: xml_tag - XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        text_xml_str = "".join(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        element_str = ""
        for i in range(0, len(xpath)):
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'],
                                                            xpath[i]['index'], "text",
                                                            self.logger_name)
            self.logger.info("Testing StringID == " + str(ids[0]))
            self.logger.info("English Text == " + eng_list[0])
            if element_text.startswith(")"):
                space = ""
            else:
                space = " "
            element_str = element_str + space + element_text
        self.util.text_compare2(self.common, text_xml_str, element_str, ids[0], self.logger_name)

    def readings(self):
        """
        This method verifies the tooltip content on My Readings(Meal marker) screen against the
        language xml. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_readings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "MenuToReadings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_readings[0]['zone'],
                                        xpath_readings[0]['xpath'],
                                        xpath_readings[0]['index'], xpath_readings[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("MenuToReadings")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ManualPopup",
                                                   self.my_object)
        popup = self.object.is_element_found(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                             xpath[0]['index'], xpath[0]['comment'],
                                             self.logger_name)
        if popup:
            self.clickbtn("ManualPopup")
        self.clickbtn("Readings")
        self.compare("ReadingsTooltip")
        self.clickbtn("CloseReadingTooltip")
        xpath1 = self.util.read_xpath_list_from_xml(self.object_repo, "ManualEntryPopup",
                                                    self.my_object)
        popup1 = self.object.is_element_found(self.util.client, xpath1[0]['zone'],
                                              xpath1[0]['xpath'],
                                              xpath1[0]['index'], xpath1[0]['comment'],
                                              self.logger_name)
        if popup1:
            self.clickbtn("ClickOK")
        self.clickbtn("CancelButton")
        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo, "DiscardPopup",
                                                    self.my_object)
        popup2 = self.object.is_element_found(self.util.client, xpath2[0]['zone'],
                                              xpath2[0]['xpath'],
                                              xpath2[0]['index'], xpath2[0]['comment'],
                                              self.logger_name)
        if popup2:
            self.clickbtn("DiscardButton")

    def reminders(self):
        """
        This method verifies the tooltip content on Test plan reminders screen against the
        language xml. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_reminders = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "ToMyReminders",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_reminders[0]['zone'],
                                        xpath_reminders[0]['xpath'],
                                        xpath_reminders[0]['index'], xpath_reminders[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("ToMyReminders")

        xpath_add_reminder = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "AddReminder",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_add_reminder[0]['zone'],
                                        xpath_add_reminder[0]['xpath'],
                                        xpath_add_reminder[0]['index'],
                                        xpath_add_reminder[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("AddReminder")
        self.compare("ReminderTooltip")
        self.clickbtn("Closetooltip")
        xpath_myreadings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "GotoMyReadings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_myreadings[0]['zone'],
                                        xpath_myreadings[0]['xpath'],
                                        xpath_myreadings[0]['index'], xpath_myreadings[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.clickbtn("GotoMyReadings")

    def targetranges(self):
        """
        This method verifies the tooltip content for Target ranges : Critical High, After Meal
        or Overall High, Before Meal or Fasting high, Low, Critical Low and Summary View against
        the language xml content. If the actual string is equal to the expected string,
        both strings will be logged, else the corresponding failed word will be logged with
        result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_mycare = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "MyCare",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_mycare[0]['zone'],
                                        xpath_mycare[0]['xpath'],
                                        xpath_mycare[0]['index'], xpath_mycare[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("MyCare")

        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TargetRange",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("TargetRange")
        xpath_info = self.util.read_xpath_list_from_xml(self.object_repo, "TargetRangeInfo",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_info[0]['zone'],
                                        xpath_info[0]['xpath'],
                                        xpath_info[0]['index'], xpath_info[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("TargetRangeInfo")
        self.compare("TargetRangeTooltip")
        self.parse_and_compare("TargetRangeTooltip1")
        self.clickbtn("ClickCloseBtn")

        self.clickbtn("ClickCriticalHigh")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

        self.clickbtn("ClickOverallHigh")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

        self.clickbtn("ClickBeforeMeal")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

        self.clickbtn("ClickLow")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

        self.clickbtn("ClickCriticalLow")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

        self.clickbtn("ClickSummaryView")
        self.clickbtn("ClickInfo")
        self.compare("SummarySpan")
        self.parse_and_compare("SummarySpan1")
        self.clickbtn("ClickCloseBtn")
        for i in range(0, 2):
            self.clickbtn("ClickBackBtn")

    def daydividers(self):
        """
        This method verifies the tooltip content for Day Dividers : Breakfast , Lunch, Dinner,
        Overnight against the language xml content. If the actual string is equal to the expected
        string, both strings will be logged, else the corresponding failed word will be logged
        with result as fail.
        :param: None
        :return: None
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "DayDividers",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("DayDividers")

        self.clickbtn("Breakfast")
        self.clickbtn("ClickInfoDayDivider")
        self.compare("DayDividerInfo")
        self.clickbtn("DayDividerClose")
        self.clickbtn("DayDividerBack")

        self.clickbtn("Lunch")
        self.clickbtn("ClickInfoDayDivider")
        self.compare("DayDividerInfo")
        self.clickbtn("DayDividerClose")
        self.clickbtn("DayDividerBack")

        self.clickbtn("Dinner")
        self.clickbtn("ClickInfoDayDivider")
        self.compare("DayDividerInfo")
        self.clickbtn("DayDividerClose")
        self.clickbtn("DayDividerBack")

        self.clickbtn("Overnight")
        self.clickbtn("ClickInfoDayDivider")
        self.compare("DayDividerInfo")
        self.clickbtn("DayDividerClose")
        self.clickbtn("DayDividerBack")
        self.clickbtn("DayDividerClose1")

    def healthcare(self):
        """
        This method compares the strings for Helathcare team : Send blood sugar report screen
        against the language xml. It swipes until the "Send blood sugar report" element is found
        and fetches the tooltip content. If the actual string is equal to the expected string,
        both strings will be logged, else the corresponding failed word will be logged with
        result as fail.
        :param: None
        :return: None
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Healthcare",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("Healthcare")
        pixel = self.dev.p2cy(self.util.client, 40)
        for i in range(0, 3):
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        xpathswipe = self.util.read_xpath_list_from_xml(self.object_repo, "SendSugarReport",
                                                        self.my_object)
        swipe = self.object.swipe_while_not_found(self.util.client, "Down", 200, 2000,
                                                  xpathswipe[0][
                                                      'zone'],
                                                  xpathswipe[0]['xpath'], xpathswipe[0]['index'],
                                                  xpathswipe[0]['comment'], 1000,
                                                  5,
                                                  True, self.logger_name)
        self.util.client.sleep(1000)
        if not swipe:
            self.clickbtn("AddHealthcareTeam")
            xpath = self.util.read_xpath_list_from_xml(self.object_repo, "SendData",
                                                       self.my_object)
            self.util.client.sleep(1000)
            count = len(xpath)
            for index in range(0, count):
                self.object.click(self.util.client, xpath[index]['zone'], xpath[index]['xpath'],
                                  xpath[index]['index'], xpath[index]['comment'], 1,
                                  self.logger_name)
                self.dev.send_text(self.util.client, "ltptest", self.logger_name)
                self.util.client.sleep(1000)
                self.dev.close_keyboard(self.util.client)

            xpath_phone = self.util.read_xpath_list_from_xml(self.object_repo, "SendPhone",
                                                             self.my_object)
            self.object.click(self.util.client, xpath_phone[0]['zone'], xpath_phone[0]['xpath'],
                              xpath_phone[0]['index'], xpath_phone[0]['comment'], 1,
                              self.logger_name)
            self.dev.send_text(self.util.client, "5555", self.logger_name)
            self.dev.close_keyboard(self.util.client)
            self.util.client.sleep(1000)
            self.clickbtn("SaveData")
            self.clickbtn("HealthcareBack")

        pixel = self.dev.p2cy(self.util.client, 40)
        for i in range(0, 3):
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        self.util.client.sleep(1000)
        swipe = self.object.swipe_while_not_found(self.util.client, "Up", 0, 2000, xpathswipe[0][
            'zone'],
                                                  xpathswipe[0]['xpath'], xpathswipe[0]['index'],
                                                  xpathswipe[0]['comment'], 1000,
                                                  5,
                                                  True, self.logger_name)
        if swipe:
            self.clickbtn("SendSugarReport")
            self.compare("SummaryReport")
            self.clickbtn("PopupClose")

    def appointments(self):
        self.clickbtn("Appointments")
        self.dev.send_text(self.util.client, "ltptest", self.logger_name)
        if self.my_object == "Iobject":
            self.clickbtn("DoneBtn")
        self.clickbtn("ClickDate")
        xpathswipe = self.util.read_xpath_list_from_xml(self.object_repo, "SelectDate",
                                                        self.my_object)
        self.object.element_swipe(self.util.client, xpathswipe[0]['zone'],
                                  xpathswipe[0]['xpath'], xpathswipe[0]['index'],
                                  xpathswipe[0]['comment'], "Up", 300, 2000,
                                  self.logger_name)
        self.clickbtn("DoneNSave")
        self.util.client.sleep(1000)
        xpath_info = self.util.read_xpath_list_from_xml(self.object_repo, "AppInfo", self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_info[0]['zone'],
                                        xpath_info[0]['xpath'],
                                        xpath_info[0]['index'], xpath_info[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("AppInfo")
        self.compare("MealMarkerGuide")
        self.clickbtn("AppointmentClose")

    def mymeters(self):
        """
        This method compares all the strings from My Meters against the language xml strings. If
        the actual string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenuForMeters")
        xpath_meters = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "MyMeters",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_meters[0]['zone'],
                                        xpath_meters[0]['xpath'],
                                        xpath_meters[0]['index'], xpath_meters[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("MyMeters")

        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ClickMyMeters",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("ClickMyMeters")

        xpathswipe = self.util.read_xpath_list_from_xml(self.object_repo, "ClickMeter",
                                                        self.my_object)
        self.object.element_swipe(self.util.client, xpathswipe[0]['zone'],
                                  xpathswipe[0]['xpath'], xpathswipe[0]['index'],
                                  xpathswipe[0]['comment'], "Right", 0, 2000,
                                  self.logger_name)
        self.clickbtn("UnpairMeter")
        self.compare("UnpairingTooltip")
        self.clickbtn("CloseUnpairTooltip")

        self.clickbtn("AddMeterIcon")
        self.compare("PairInfo")
        self.clickbtn("PairClose")
        xpath1 = self.util.read_xpath_list_from_xml(self.object_repo, "WaitForVanish",
                                                    self.my_object)
        if self.object.wait_for_element_to_vanish(self.util.client, xpath1[0]['zone'],
                                                  xpath1[0]['xpath'], xpath1[0]['index'],
                                                  xpath1[0]['comment'], 10000, self.logger_name):
            pass

        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo, "SelectMeter",
                                                    self.my_object)
        selectmeter = self.object.is_element_found(self.util.client, xpath2[0]['zone'],
                                                   xpath2[0]['xpath'], xpath2[0]['index'],
                                                   xpath2[0]['comment'], self.logger_name)
        if selectmeter:
            self.clickbtn("ClickMeterInfo")
            self.compare("SelectMeterInfo")
            self.clickbtn("CloseNContinue")

        xpath3 = self.util.read_xpath_list_from_xml(self.object_repo, "NoPair",
                                                    self.my_object)
        if self.object.wait_for_element(self.util.client, xpath3[0]['zone'], xpath3[0]['xpath'],
                                        xpath3[0]['index'], xpath3[0]['comment'], 10000,
                                        self.logger_name):
            pass

        self.clickbtn("NoPair")
        self.compare("NoPairInfo")
        self.clickbtn("PairpopupClose")

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
