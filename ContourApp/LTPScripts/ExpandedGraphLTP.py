"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Modal Day/Expanded Graph
#                               Script Name    : ExpandedGraphLTP.py
#                               Created On     : Feb 02 , 2017
#                               Created By     : Sharath R (341247)
#                               APP version    : 1.9.44
# **********************************************************************
# **********************************************************************
import sys
import os
import unittest
import logging
import random

reload(sys)
sys.setdefaultencoding('utf8')
SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Logger, \
    Config, Configuration


class ExpandedGraphLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Expanded graph/Modal day screens on
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

    def test_expgraph(self):
        """
        Main LTP test method to test Expanded graph/Modal day screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.rotate_turn_on()
        self.add_reading()
        self.goto_expandedgraph()
        self.graphscreens()

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
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag1,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag2,
                                                   self.my_object)

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
        This method joins the list of strings from language xml and compare with each of the
        string from screen.
        :param xml_tag: XML tag from objects.xml file to get the xpath of actual text. Same XML
        tag is used to read the language xml file to fetch the expected string for comparision
        :return: None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag,
                                                                   "trans-unit",
                                                                   Config.selected_language.strip())
        text_xml = " ".join(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, xml_tag, self.my_object)
        # print "textxml=", text_xml
        element_text = self.object.element_get_property(self.util.client, xpath[0]['zone'],
                                                        xpath[0]['xpath'],
                                                        xpath[0]['index'], "text", self.logger_name)

        self.logger.info("Testing StringID == " + str(ids[0]))
        self.logger.info("English Text == " + eng_list[0])
        self.util.text_compare2(self.common, text_xml, element_text, ids[0], self.logger_name)

    def rotate_turn_on(self):
        """
        This methods enables the landscape mode using adb command(for android) and enables the
        "Expanded Graph Rotate" from "App Preferences" screen.
        :param: None
        :return: None
        """
        if self.my_object == "Aobject":
            self.dev.run(self.util.client,
                         "adb shell content insert --uri content://settings/system --bind "
                         "name:s:accelerometer_rotation --bind value:i:0", self.logger_name)
            self.dev.run(self.util.client,
                         "adb shell content insert --uri content://settings/system --bind "
                         "name:s:accelerometer_rotation --bind value:i:1", self.logger_name)

        self.clickbtn("ClickMenu")
        xpath_settings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "Settings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_settings[0]['zone'],
                                        xpath_settings[0]['xpath'],
                                        xpath_settings[0]['index'], xpath_settings[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("Settings")

        xpath_apppref = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "AppPref",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_apppref[0]['zone'],
                                        xpath_apppref[0]['xpath'],
                                        xpath_apppref[0]['index'], xpath_apppref[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("AppPref")

        pixel = self.dev.p2cy(self.util.client, 80)
        if self.my_object == "Iobject":
            xpath_appscreen = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "AppPrefScreen",
                                                   self.my_object)
            if self.object.wait_for_element(self.util.client, xpath_appscreen[0]['zone'],
                                        xpath_appscreen[0]['xpath'],
                                        xpath_appscreen[0]['index'], xpath_appscreen[0]['comment'],
                                        15000,
                                        self.logger_name):
                print "found"
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TurnOnRotate",
                                                   self.my_object)
        self.object.flick_element(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                                  xpath[0]['index'], xpath[0]['comment'], "Right", self.logger_name)

        self.clickbtn("AppPrefBack")
        self.util.client.sleep(1000)
        xpath_menu = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "SettingsToMenu",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_menu[0]['zone'],
                                        xpath_menu[0]['xpath'],
                                        xpath_menu[0]['index'], xpath_menu[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("SettingsToMenu")

        xpath_readings = self.util.read_xpath_list_from_xml(self.object_repo,
                                                            "MyReadings",
                                                   self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_readings[0]['zone'],
                                        xpath_readings[0]['xpath'],
                                        xpath_readings[0]['index'], xpath_readings[0]['comment'],
                                        15000,
                                        self.logger_name):
            print "found"
        self.clickbtn("MyReadings")

    def add_reading(self):
        """
        This method adds a new manual reading for current date with Meal and Notes.
        :param: None
        :return: None
        """
        self.clickbtn("NewReading1")
        xpathmanentry = self.util.read_xpath_list_from_xml(self.object_repo, "MainPopup",
                                                           self.my_object)
        manualentrypopup = self.object.is_element_found(self.util.client, xpathmanentry[0]['zone'],
                                                        xpathmanentry[0]['xpath'],
                                                        xpathmanentry[0]['index'], xpathmanentry[0][
                                                            'comment'], self.logger_name)
        if manualentrypopup:
            self.clickbtn("MainPopup")
        self.clickbtn("NewReading2")
        self.dev.send_text(self.util.client, "120", self.logger_name)
        self.util.client.sleep(1000)
        self.dev.close_keyboard(self.util.client)
        self.util.client.sleep(1000)
        self.clickbtn("ReadingSave")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MealMarkerPrompt",
                                                   self.my_object)
        mealmarkerprompt = self.object.is_element_found(self.util.client, xpath[0]['zone'],
                                                        xpath[0]['xpath'], xpath[0]['index'],
                                                        xpath[0]['comment'], self.logger_name)
        if mealmarkerprompt:
            self.clickbtn("MealMarkerPrompt")
        self.clickbtn("AddNotes")
        self.dev.send_text(self.util.client, "ltptest", self.logger_name)
        # self.dev.closeKeyboard(self.util.client)
        self.clickbtn("ClickMeal")

        xpath1 = self.util.read_xpath_list_from_xml(self.object_repo, "SelectCarbPopup",
                                                    self.my_object)
        carbpopup = self.object.is_element_found(self.util.client, xpath1[0]['zone'], xpath1[0][
            'xpath'],
                                                 xpath1[0]['index'], xpath1[0]['comment'],
                                                 self.logger_name)
        if carbpopup:
            self.clickbtn("SelectCarbPopup")

        self.clickbtn("AddFood")
        randnum = random.randrange(0, 999)
        self.dev.send_text(self.util.client, "ltptest" + str(randnum), self.logger_name)
        # if self.my_object == "Iobject":
            # xpath_select = self.util.read_xpath_list_from_xml(self.object_repo, "CheckMealSelected",
                                                    # self.my_object)
            # selectmeal = self.object.is_element_found(self.util.client, xpath_select[0]['zone'],
                                                   # xpath_select[0]['xpath'],
                                                   # xpath_select[0]['index'],
                                                   # xpath_select[0]['comment'], self.logger_name)
            # if selectmeal:
                # self.clickbtn("Meal1")
        self.clickbtn("Meal1")

        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo, "ClickContinue",
                                                    self.my_object)
        continuebtn = self.object.is_element_found(self.util.client, xpath2[0]['zone'],
                                                   xpath2[0]['xpath'], xpath2[0]['index'],
                                                   xpath2[0]['comment'], self.logger_name)
        if continuebtn:
            self.clickbtn("ClickContinue")
        self.clickbtn("Meal2")
        self.clickbtn("DoneBtn")
        xpath4 = self.util.read_xpath_list_from_xml(self.object_repo, "ManualEntryConfirm",
                                                    self.my_object)
        manentrypopup = self.object.is_element_found(self.util.client, xpath4[0]['zone'],
                                                     xpath4[0]['xpath'], xpath4[0]['index'],
                                                     xpath4[0]['comment'], self.logger_name)
        if manentrypopup:
            self.clickbtn("ManualEntryConfirm")

        xpath5 = self.util.read_xpath_list_from_xml(self.object_repo, "CriticalValue",
                                                    self.my_object)
        criticalpopup = self.object.is_element_found(self.util.client, xpath5[0]['zone'],
                                                     xpath5[0]['xpath'], xpath5[0]['index'],
                                                     xpath5[0]['comment'], self.logger_name)
        if criticalpopup:
            self.clickbtn("CriticalValue")

        xpath3 = self.util.read_xpath_list_from_xml(self.object_repo, "ReminderPopup",
                                                    self.my_object)
        popup = self.object.is_element_found(self.util.client, xpath3[0]['zone'],
                                             xpath3[0]['xpath'],
                                             xpath3[0]['index'], xpath3[0]['comment'],
                                             self.logger_name)
        if popup:
            self.clickbtn("ReminderPopup")

        xpath6 = self.util.read_xpath_list_from_xml(self.object_repo, "CloseConfirm",
                                                    self.my_object)
        confirmpopup = self.object.is_element_found(self.util.client, xpath6[0]['zone'],
                                                    xpath6[0]['xpath'], xpath6[0]['index'],
                                                    xpath6[0]['comment'], self.logger_name)
        if confirmpopup:
            self.clickbtn("CloseConfirm")
        self.util.client.sleep(1000)

        xpath7 = self.util.read_xpath_list_from_xml(self.object_repo, "RunningHighLow",
                                                    self.my_object)
        runningpopup = self.object.is_element_found(self.util.client, xpath7[0]['zone'],
                                                    xpath7[0]['xpath'], xpath7[0]['index'],
                                                    xpath7[0]['comment'], self.logger_name)
        xpath8 = self.util.read_xpath_list_from_xml(self.object_repo, "RunningHighLow1",
                                                    self.my_object)
        runningpopup1 = self.object.is_element_found(self.util.client, xpath8[0]['zone'],
                                                     xpath8[0]['xpath'], xpath8[0]['index'],
                                                     xpath8[0]['comment'], self.logger_name)
        if runningpopup:
            self.clickbtn("RunningHighLow")
        elif runningpopup1:
            self.clickbtn("RunningHighLow1")
        self.util.client.sleep(1000)

    def goto_expandedgraph(self):
        """
        This method takes us to expanded graph mode, sets the date to today.
        :param: None
        :return: None
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "GotoExpandedGraph",
                                                   self.my_object)
        self.object.touch_down(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                               xpath[0]['index'], xpath[0]['comment'], self.logger_name)
        self.object.touch_up(self.util.client, self.logger_name)

        xpathpopup = self.util.read_xpath_list_from_xml(self.object_repo, "RotatePopup",
                                                        self.my_object)
        rotatepopup = self.object.is_element_found(self.util.client, xpathpopup[0]['zone'],
                                                   xpathpopup[0]['xpath'], xpathpopup[0]['index'],
                                                   xpathpopup[0]['comment'], self.logger_name)
        if rotatepopup:
            self.compare("RotatePopupCompare")
            self.clickbtn("RotatePopup")

        if self.my_object == "Aobject":
            xpath_date = self.util.read_xpath_list_from_xml(self.object_repo, "GetDate",
                                                            self.my_object)
            xpath_day_swipe = self.util.read_xpath_list_from_xml(self.object_repo,
                                                                 "DaySwipe",
                                                                 self.my_object)
            # current_date = time.strftime("%x").split('/')[1]
            if self.object.wait_for_element(self.util.client, xpath_date[0]['zone'],
                                            xpath_date[0]['xpath'],
                                            xpath_date[0]['index'], xpath_date[0]['comment'], 10000,
                                            self.logger_name):
                pass
            date = self.common.element_get_text(self.util.client, xpath_date[0]['zone'],
                                                xpath_date[0]['xpath'], xpath_date[0]['comment'],
                                                self.logger_name, xpath_date[0]['index'])
            # onlyDay = str(date).split()[1]

            # while(onlyDay!=current_date or date.strip()!="Today"):
            count = 0
            while date.strip() != "Today":
                if count == 15:
                    break
                self.object.element_swipe(self.util.client, xpath_day_swipe[0]['zone'],
                                          xpath_day_swipe[0]['xpath'], xpath_day_swipe[0]['index'],
                                          xpath_day_swipe[0]['comment'], "Down", 0, 2000,
                                          self.logger_name)
                date = self.common.element_get_text(self.util.client, xpath_date[0]['zone'],
                                                    xpath_date[0]['xpath'],
                                                    xpath_date[0]['comment'],
                                                    self.logger_name, xpath_date[0]['index'])
                count += 1

                # onlyDay = date.split()[1]

    def graphscreens(self):
        """
        This method compares the strings on screen against the language xml, takes us to
        "Customize your view", compares the strings. Also, compares the tooltip strings against
        the language xml. If the actual string is equal to the expected string, both strings will be
        logged, else the corresponding failed word will be logged with result as fail.
        :param: None
        :return: None
        """
        self.clickbtn("SetView")
        self.compare("GraphScreen1")
        self.clickbtn("SetViewAvg")
        self.compare("GraphScreenAvg")
        self.clickbtn("ClickInfo")
        self.compare("ExpandedPopup")
        self.parse_and_compare("ExpandedPopup2")
        self.parse_and_compare("ExpandedPopup3")
        self.clickbtn("CloseInfo")

        self.clickbtn("ClickStd")
        self.compare("GraphScreen2")

        self.clickbtn("ClickInfo1")
        self.compare("ExpandedPopup")
        self.parse_and_compare("ExpandedPopup2")
        self.parse_and_compare("ExpandedPopup3")
        self.clickbtn("CloseInfo")

        self.clickbtn("ClickDone")
        if self.my_object == "Aobject":
            xpath_noreading = self.util.read_xpath_list_from_xml(self.object_repo, "NoReading",
                                                            self.my_object)
            xpath_day_swipe = self.util.read_xpath_list_from_xml(self.object_repo,
                                                                 "DaySwipe",
                                                                 self.my_object)
            self.object.element_swipe(self.util.client, xpath_day_swipe[0]['zone'],
                                      xpath_day_swipe[0]['xpath'], xpath_day_swipe[0]['index'],
                                      xpath_day_swipe[0]['comment'], "Up", 0, 2000,
                                      self.logger_name)
            no_reading = self.object.is_element_found(self.util.client, xpath_noreading[0]['zone'],
                                                xpath_noreading[0]['xpath'],
                                                xpath_noreading[0]['index'],
                                                xpath_noreading[0]['comment'], self.logger_name)
            if no_reading:
                self.compare("NoReading")
        self.clickbtn("CloseGraph")

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
