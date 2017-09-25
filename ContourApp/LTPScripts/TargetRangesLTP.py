"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Target Ranges
#                               Script Name    : TargetRangesLTP.py
#                               Created On     : Feb 06 , 2017
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


class TargetRangesLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Target Ranges screens on
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

    def test_target_ranges(self):
        """
        Main LTP test method to test Target Ranges screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.goto_mycare()
        self.goto_target_range_screen()
        highvalue = self.critical_high()
        self.set_critical_low()
        initialvalue = self.after_meal_overall_high(highvalue)
        self.before_meal_fasting_high(initialvalue)
        self.low()
        self.critical_low()
        self.summary_view()

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

    def parse_and_compare(self, xml_tag):
        """
        This method joins the list of strings from language xml. The gets the text from screen.
        If the element starts with ")" or ends with "(", append the text to element string (
        initially eppty) along with a space. Compare the parsed string from language xml with the
        element string.
        :param xml_tag - XML tags from objects.xml file to get the xpath of actual text.
        Same XML tag is used to read the language xml file to fetch the expected string for
        comparision
        :return: None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        text_xml_str = "".join(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        element_str = ""
        self.logger.info("String verification: STARTED")
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

    def goto_mycare(self):
        """
        This methods navigates us to My care screen
        :param: None
        :return: None
        """
        self.clickbtn("ClickMenu")
        xpath_mycare = self.util.read_xpath_list_from_xml(self.object_repo, "MyCare",
                                                          self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_mycare[0]['zone'],
                                        xpath_mycare[0]['xpath'],
                                        xpath_mycare[0]['index'], xpath_mycare[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("MyCare")

    def goto_target_range_screen(self):
        """
        This method navigates to Target Ranges screen and verifies the strings for Target ranges
        main screen against the language xml content. If the actual string is equal to the
        expected string, both strings will be logged, else the corresponding failed word will be
        logged with result as fail.
        :param: None
        :return: None
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TargetRange",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                        xpath[0]['index'], xpath[0]['comment'], 10000,
                                        self.logger_name):
            pass
        self.clickbtn("TargetRange")
        self.compare("TargetMainScreen")
        self.clickbtn("ClickInfo")
        self.compare("TargetRangeSpan")
        self.parse_and_compare("TargetRangeSpan1")
        self.parse_and_compare("TargetRangeSpan2")
        self.parse_and_compare("TargetRangeSpan3")
        self.clickbtn("ClickCloseBtn")

    def critical_high(self):
        """
        This method verifies the strings in Critical High screen against the language xml
        content. Calls set_critical_high() method to set a critical high value. If the actual
        string is equal to the expected string, both strings will be logged, else the
        corresponding failed word will be logged with result as fail.
        :param: None
        :return: Critical high value that has been set
        """
        self.clickbtn("ClickCriticalHigh")
        self.compare("CriticalHigh")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        value = self.set_critical_high()
        self.clickbtn("ClickBackBtn")
        return value

    def set_critical_high(self):
        """
        This method sets the Critical High value to 200.
        :param: None
        :return: Critical high value of 200
        """
        set_to = 200
        count = 0
        xpath_setcritical = self.util.read_xpath_list_from_xml(self.object_repo,
                                                               "SetCriticalHigh", self.my_object)
        value = int(self.object.element_get_property(self.util.client, xpath_setcritical[0]['zone'],
                                                     xpath_setcritical[0]['xpath'],
                                                     xpath_setcritical[0]['index'], "text",
                                                     self.logger_name))
        if value == 200:
            return value
        else:
            xpath_slider = self.util.read_xpath_list_from_xml(self.object_repo,
                                                              "SetCriticalHigh", self.my_object)

            if value > set_to:
                while value > set_to:
                    if count == 20:
                        break
                    self.object.drag(self.util.client, xpath_slider[0]['zone'],
                                     xpath_slider[0]['xpath'], xpath_slider[0]['index'],
                                     xpath_slider[0]['comment'], 0, 4, self.logger_name)
                    value = int(
                        self.object.element_get_property(self.util.client,
                                                         xpath_setcritical[0]['zone'],
                                                         xpath_setcritical[0]['xpath'],
                                                         xpath_setcritical[0]['index'], "text",
                                                         self.logger_name))

            else:
                while value < set_to:
                    if count == 20:
                        break
                    self.object.click(self.util.client, xpath_slider[0]['zone'],
                                      xpath_slider[0]['xpath'], xpath_slider[0]['index'],
                                      xpath_slider[0]['comment'], 0, -4, self.logger_name)
                    value = int(
                        self.object.element_get_property(self.util.client,
                                                         xpath_setcritical[0]['zone'],
                                                         xpath_setcritical[0]['xpath'],
                                                         xpath_setcritical[0]['index'], "text",
                                                         self.logger_name))

            self.clickbtn("SliderOK")
            return value

    def set_critical_low(self):
        """
        This method sets the Critical Low value to 20
        :param: None
        :return: None
        """
        set_to = 20
        count = 0
        self.clickbtn("ClickCriticalLow")
        xpath_slider = self.util.read_xpath_list_from_xml(self.object_repo, "SetCriticalLow",
                                                          self.my_object)
        value = int(self.object.element_get_property(self.util.client, xpath_slider[0]['zone'],
                                                     xpath_slider[0]['xpath'],
                                                     xpath_slider[0]['index'],
                                                     "text", self.logger_name))

        if value == 20:
            self.clickbtn("ClickBackBtn")
            return
        while value > set_to:
            if count == 20:
                        break
            self.object.drag(self.util.client, xpath_slider[0]['zone'], xpath_slider[0]['xpath'],
                             xpath_slider[0]['index'], xpath_slider[0]['comment'], 0, 100,
                             self.logger_name)
            value = int(self.object.element_get_property(self.util.client, xpath_slider[0]['zone'],
                                                         xpath_slider[0]['xpath'],
                                                         xpath_slider[0]['index'], "text",
                                                         self.logger_name))

        self.clickbtn("SliderOK")
        self.clickbtn("ClickBackBtn")

    def after_meal_overall_high(self, high_value):
        """
        This method navigates to "After Meal or Overall High" screen, compares the strings
        against language xml. Opens the tooltip and compares the tooltip content against that of
        language xml. Then tries to set the value to 190 mg/dL to capture the popup text and
        verify. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param high_value - Critical high value set before
        :return: Overall High value of 180 mg/dL
        """
        self.clickbtn("ClickOverallHigh")
        self.compare("OverallHigh")

        highest_value = high_value
        index = 0
        xpath_highvalue = self.util.read_xpath_list_from_xml(self.object_repo, "HighValue",
                                                             self.my_object)
        xpath_popup = self.util.read_xpath_list_from_xml(self.object_repo, "AfterMealPopup",
                                                         self.my_object)
        popup_from_xml = self.util.get_text_from_xml(self.string_xml, "AfterMealPopup",
                                                     "trans-unit", Config.selected_language.strip())
        value = int(
            self.object.element_get_property(self.util.client, xpath_highvalue[index]['zone'],
                                             xpath_highvalue[index]['xpath'],
                                             xpath_highvalue[index]['index'], "text",
                                             self.logger_name))
        initial_value = value
        while value < (highest_value - 10):
            self.object.drag(self.util.client, xpath_highvalue[index]['zone'],
                             xpath_highvalue[index]['xpath'], xpath_highvalue[index]['index'],
                             xpath_highvalue[index]['comment'], 0, -240, self.logger_name)
            value = int(
                self.object.element_get_property(self.util.client, xpath_highvalue[index]['zone'],
                                                 xpath_highvalue[index]['xpath'],
                                                 xpath_highvalue[index]['index'], "text",
                                                 self.logger_name))
        if value == (highest_value - 10):
            self.object.drag(self.util.client, xpath_highvalue[index]['zone'],
                             xpath_highvalue[index]['xpath'], xpath_highvalue[index]['index'],
                             xpath_highvalue[index]['comment'], 0, -240, self.logger_name)
        # if self.object.wait_for_element(self.util.client, xpath_popup[0]['zone'],
        #                                 xpath_popup[0]['xpath'], xpath_popup[0]['index'],
        #                                 xpath_popup[0]['comment'], 5000, self.logger_name):
        #     pass
        #
        # element_text = self.object.element_get_property(self.util.client, xpath_popup[0]['zone'],
        #                                                 xpath_popup[0]['xpath'],
        #                                                 xpath_popup[0]['index'], "text",
        #                                                 self.logger_name)
        #
        # self.util.text_compare(self.util.client, self.common, popup_from_xml[0], element_text,
        #                        self.logger_name)

        self.clickbtn("SliderClose")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")
        print "Initialvalue=", initial_value
        return initial_value

    def before_meal_fasting_high(self, initialvalue):
        """
        This method navigates to "Before Meal or Fasting High" screen, compares the strings
        against language xml. Opens the tooltip and compares the tooltip content against that of
        language xml. Then tries to set the value to 20 mg/dL to capture the popup text and verify.
        If the actual string is equal to the expected string, both strings will be logged,
        else the corresponding failed word will be logged with result as fail.
        :param initialvalue - Initial value of 180 mg/dL set in after_meal_overall_high()
        :return: None
        """
        self.clickbtn("ClickBeforeMeal")
        self.compare("BeforeMealHigh")
        index = 0
        xpath_highvalue = self.util.read_xpath_list_from_xml(self.object_repo,
                                                             "BeforeHighValue", self.my_object)
        xpath_popup = self.util.read_xpath_list_from_xml(self.object_repo, "BeforeMealPopup",
                                                         self.my_object)
        popup_from_xml = self.util.get_text_from_xml(self.string_xml, "BeforeMealPopup",
                                                     "trans-unit", Config.selected_language.strip())
        value = int(
            self.object.element_get_property(self.util.client, xpath_highvalue[index]['zone'],
                                             xpath_highvalue[index]['xpath'],
                                             xpath_highvalue[index]['index'], "text",
                                             self.logger_name))

        if value == initialvalue:
            self.object.drag(self.util.client, xpath_highvalue[index]['zone'],
                             xpath_highvalue[index]['xpath'], xpath_highvalue[index]['index'],
                             xpath_highvalue[index]['comment'], 0, -240, self.logger_name)

        while value < initialvalue:
            self.object.drag(self.util.client, xpath_highvalue[index]['zone'],
                             xpath_highvalue[index]['xpath'], xpath_highvalue[index]['index'],
                             xpath_highvalue[index]['comment'], 0, -240, self.logger_name)
            value = int(
                self.object.element_get_property(self.util.client, xpath_highvalue[index]['zone'],
                                                 xpath_highvalue[index]['xpath'],
                                                 xpath_highvalue[index]['index'], "text",
                                                 self.logger_name))

        # if self.object.wait_for_element(self.util.client, xpath_popup[0]['zone'],
        #                                 xpath_popup[0]['xpath'], xpath_popup[0]['index'],
        #                                 xpath_popup[0]['comment'], 5000, self.logger_name):
        #     pass
        # element_text = self.object.element_get_property(self.util.client, xpath_popup[0]['zone'],
        #                                                 xpath_popup[0]['xpath'],
        #                                                 xpath_popup[0]['index'], "text",
        #                                                 self.logger_name)
        # self.util.text_compare(self.util.client, self.common, popup_from_xml[0], element_text,
        #                        self.logger_name)

        self.clickbtn("SliderClose")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

    def low(self):
        """
        This method navigates to "Low" screen, compares the strings against language xml. Opens
        the tooltip and compares the tooltip content against that of language xml. Tries to set
        the value to 30 to capture the popup text and verify. If the actual string is equal to
        the expected string, both strings will be logged, else the corresponding failed word will
        be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickLow")
        self.compare("Low")
        index = 0
        xpath_lowvalue = self.util.read_xpath_list_from_xml(self.object_repo, "LowValue",
                                                            self.my_object)
        xpath_popup = self.util.read_xpath_list_from_xml(self.object_repo, "LowPopup",
                                                         self.my_object)
        popup_from_xml = self.util.get_text_from_xml(self.string_xml, "LowPopup", "trans-unit",
                                                     Config.selected_language.strip())
        value = int(
            self.object.element_get_property(self.util.client, xpath_lowvalue[index]['zone'],
                                             xpath_lowvalue[index]['xpath'],
                                             xpath_lowvalue[index]['index'], "text",
                                             self.logger_name))
        lowvalue = 20
        if value == (lowvalue + 10):
            self.object.drag(self.util.client, xpath_lowvalue[index]['zone'],
                             xpath_lowvalue[index]['xpath'], xpath_lowvalue[index]['index'],
                             xpath_lowvalue[index]['comment'], 0, 200, self.logger_name)

        while value > (lowvalue + 10):
            self.object.drag(self.util.client, xpath_lowvalue[index]['zone'],
                             xpath_lowvalue[index]['xpath'], xpath_lowvalue[index]['index'],
                             xpath_lowvalue[index]['comment'], 0, 200, self.logger_name)
            value = int(
                self.object.element_get_property(self.util.client, xpath_lowvalue[index]['zone'],
                                                 xpath_lowvalue[index]['xpath'],
                                                 xpath_lowvalue[index]['index'], "text",
                                                 self.logger_name))

        # if self.object.wait_for_element(self.util.client, xpath_popup[0]['zone'],
        #                                 xpath_popup[0]['xpath'], xpath_popup[0]['index'],
        #                                 xpath_popup[0]['comment'], 5000, self.logger_name):
        #     pass
        # element_text = self.object.element_get_property(self.util.client, xpath_popup[0]['zone'],
        #                                                 xpath_popup[0]['xpath'],
        #                                                 xpath_popup[0]['index'], "text",
        #                                                 self.logger_name)
        # self.util.text_compare(self.util.client, self.common, popup_from_xml[0], element_text,
        #                        self.logger_name)

        self.clickbtn("SliderClose")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

    def critical_low(self):
        """
        This method navigates to Critical Low screen, compares the strings against language xml.
        It then opens the tooltip and compares the tooltip content against that of language xml.
        If the actual string is equal to the expected string, both strings will be logged,
        else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickCriticalLow")
        self.compare("CriticalLow")
        self.clickbtn("ClickInfo")
        self.compare("CriticalHighInfo")
        self.clickbtn("CriticalHighInfoClose")
        self.clickbtn("ClickBackBtn")

    def summary_view(self):
        """
        This method navigates to Summary View screen, compares the strings against language xml.
        It then opens the tooltip and compares the tooltip content against that of language xml.
        If the actual string is equal to the expected string, both strings will be logged,
        else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("ClickSummaryView")
        self.compare("SummaryView")
        self.clickbtn("ClickInfo")
        self.compare("SummarySpan")
        self.parse_and_compare("SummarySpan1")
        self.parse_and_compare("SummarySpan2")
        self.parse_and_compare("SummarySpan3")
        self.clickbtn("ClickCloseBtn")
        for i in range(0, 2):
            self.clickbtn("ClickBackBtn")

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
