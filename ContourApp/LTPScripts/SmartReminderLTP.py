"""Base version used 1.9.44"""
# -*- coding: utf-8 -*-
# encoding=utf8

# *********************************************************************
# *********************************************************************
#                               System Map Name: Smart Reminders
#                               Script Name    : SmartReminderLTP.py
#                               Created On     : Jan 25 , 2017
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


class SmartReminderLTP(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Smart Reminders screens on
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
        # self.config.set_show_pass_image_in_report(self.util.client, False)
        Config.results_list = []

    def test_smartreminder(self):
        """
        Main LTP test method to test Smart Reminders screens.For each string element on the
        screen, which is ACTUAL STRING, is compared with target string in the language XML that
        is EXPECTED.
        :param: None
        :return: None
        """
        self.to_testreminderplan()
        self.smartreminderscreen()
        self.try_two_reminders()
        self.gohome()

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
        :param: xml_tag1, xml_tag2 - XML tags from objects.xml file to get the xpath of actual
        text. Same XML tag is used to read the language xml file to fetch the expected string for
        comparision
        :return: None
        """
        if Config.selected_language == "":
            Config.selected_language = "english"
        if xml_tag2 == "":
            xml_tag2 = xml_tag1
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, xml_tag1, "trans-unit",
                                                    Config.selected_language)
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

    def comparereminders(self, *args):
        """
        This is a generic method which has the logic to compare the strings of all the reminder
        plans as against the language xml one after the other.
        :param: arg1 - XML tag for click events
        :param: arg2 - arg3 - XML tags for string compare events
        :param: arg4 - XML tag for tooltip(popup) string comparison
        :param: arg5 - XML tag for generated smart reminder screen
        :param: arg6 -  XML tag for delete popup string comparison
        :return: None
        """
        arg1, arg2, arg3, arg4, arg5, arg6 = args
        pixel = self.dev.p2cy(self.util.client, 80)
        if arg1.strip() == "UpcomingNonInsulin" and self.my_object == "Iobject":
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        self.clickbtn(arg1)  # argument

        if arg1.strip() == "StressClick" or arg1.strip() == "EventClick" or \
                        arg1.strip() == "PointPlanClick" or arg1.strip() == "OvernightLowClick" \
                or arg1.strip() == "UpcomingVisitClick" or arg1.strip() == "DietClick" or \
                        arg1.strip() == "UpcomingNonInsulin":
            if arg1.strip() == "UpcomingVisitClick":
                self.dev.swipe(self.util.client, "Down", pixel, 300)
            if (arg1.strip() == "StressClick" or arg1.strip() == "UpcomingNonInsulin") and \
                            self.my_object == "Iobject":
                self.dev.swipe(self.util.client, "Down", pixel, 300)
            self.compare(arg2)
        elif arg1.strip() == "StartInsulinClick" or arg1.strip() == "ActingInsulinClick":
            self.compare(arg2, "DietCompare")
        else:
            self.compare(arg2, "DislikeCompare")  # compare dislike # argument
        self.util.client.sleep(1000)
        self.clickbtn("Continue")  # click continue

        if arg1.strip() == "EventClick":
            self.clickbtn("EventAppClick")
            self.compare("EventDone")
            self.clickbtn("EventDone")
            self.clickbtn("EventName")
            self.dev.send_text(self.util.client, "testltp", self.logger_name)
            self.dev.close_keyboard(self.util.client)
            self.compare(arg3)
        elif arg1.strip() == "UpcomingVisitClick" or arg1.strip() == "UpcomingNonInsulin":
            self.clickbtn("EventAppClick")
            self.compare("EventDone")
            self.clickbtn("EventDone")
            self.compare(arg3)
        elif arg1.strip() == "OvernightLowClick":
            self.compare(arg3)
        elif arg1.strip() == "StartInsulinClick":
            self.compare(arg3, "OvernightLowCompare2")
        else:
            self.compare(arg3, "DislikeCompare2")  # compare dislike test screen #argument

        self.clickbtn("ClickInfo")  # info click
        self.compare(arg4, "TestReminderPopup1")  # info compare #argument
        self.clickbtn("CloseInfoSave")  # info close
        xpath_reminder = self.util.read_xpath_list_from_xml(self.object_repo, "ReminderOpen",
                                                            self.my_object)
        if self.object.wait_for_element(self.util.client, xpath_reminder[0]['zone'],
                                        xpath_reminder[0]['xpath'],
                                        xpath_reminder[0]['index'], xpath_reminder[0]['comment'],
                                        10000,
                                        self.logger_name):
            print "found"
        self.util.client.sleep(500)
        self.clickbtn("ReminderOpen")
        self.compare(arg5, "DislikeCompare3")  # compare dislike to test #argument
        self.clickbtn("DeletePlan")  # delete plan
        self.compare(arg6, "DelPopupCompare")  # delete popup #argument
        self.clickbtn("ClickDelete")  # delete
        self.util.client.sleep(1000)

    def to_testreminderplan(self):
        """
        This methods navigates to "My Reminders" screen. It then checks if there are any
        existing reminder plans already saved. If so, the existing reminder plan is deleted.
        This is done, as only one reminder plan can be added at once.
        :param: None
        :return: None
        """
        self.clickbtn("ToReminder")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "CheckTestReminder",
                                                   self.my_object)
        testreminder = self.object.is_element_found(self.util.client, xpath[0]['zone'],
                                                    xpath[0]['xpath'], xpath[0]['index'], xpath[0][
                                                        'comment'], self.logger_name)
        if testreminder:
            self.clickbtn("DelExistingReminder")
        self.clickbtn("TestReminder")

    def smartreminderscreen(self):
        """
        This method first compares the strings from Test Reminder plans main screen against
        language xml. Then takes up each of the reminder plans and compares the strings on the
        screen against language xml. If the actual string is equal to the expected string, both
        strings will be logged, else the corresponding failed word will be logged with result
        as fail.
        :param: None
        :return: None
        """
        self.compare("TestReminderPlanScreen")
        self.util.client.sleep(1000)
        pixel = self.dev.p2cy(self.util.client, 60)
        self.dev.swipe(self.util.client, "Up", pixel, 300)   # fix for Note5
        self.util.client.sleep(2000)
        self.comparereminders("DislikeClick", "DislikeCompare", "DislikeCompare2",
                              "TestReminderPopup1", "DislikeCompare3", "DelPopupCompare")
        self.comparereminders("CuriousClick", "CuriousCompare", "CuriousCompare2", "CuriousPopup",
                              "CuriousCompare3", "DelPopupCompare2")
        self.comparereminders("StressClick", "StressCompare", "StressCompare2", "StressPopup",
                              "StressCompare3", "DelPopupCompare3")
        self.comparereminders("EventClick", "EventCompare", "EventCompare2", "EventPopup",
                              "EventCompare3", "DelPopupCompare4")

        self.comparereminders("UpcomingVisitClick", "UpcomingVisitCompare", "UpcomingVisitCompare2",
                              "UpcomingVisitPopup", "UpcomingVisitCompare3", "DelPopupCompare5")
        self.comparereminders("UpcomingNonInsulin", "UpcomingNonInsulinCompare",
                              "UpcomingNonInsulinCompare2", "UpcomingNonInsulinPopup",
                              "UpcomingNonInsulinCompare3", "DelPopupCompare6")

        self.comparereminders("PointPlanClick", "PointPlanCompare", "PointPlanCompare2",
                              "PointPlanPopup", "PointPlanCompare3", "DelPopupCompare7")
        self.comparereminders("ActingInsulinClick", "ActingInsulinCompare", "ActingInsulinCompare2",
                              "ActingInsulinPopup", "ActingInsulinCompare3", "DelPopupCompare8")
        self.comparereminders("OvernightLowClick", "OvernightLowCompare", "OvernightLowCompare2",
                              "OvernightLowPopup", "OvernightLowCompare3", "DelPopupCompare9")
        self.comparereminders("DietClick", "DietCompare", "DietCompare2", "DietPopup",
                              "DietCompare3", "DelPopupCompare10")
        self.comparereminders("StartInsulinClick", "StartInsulinCompare", "StartInsulinCompare2",
                              "StartInsulinPopup", "StartInsulinCompare3", "DelPopupCompare11")

        self.clickbtn("ReminderInfoClick")
        self.compare("ReminderPopup")
        self.clickbtn("CloseReminderPopup")

    def try_two_reminders(self):
        """
        Method to try to add two reminder plans to compare the pop up strings
        :param: None
        :return: None
        """
        self.clickbtn("DislikeAdd")
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "CheckReminder",
                                                   self.my_object)
        testreminder = self.object.is_element_found(self.util.client, xpath[0]['zone'],
                                                    xpath[0]['xpath'], xpath[0]['index'], xpath[0][
                                                        'comment'], self.logger_name)
        if testreminder:
            self.clickbtn("CuriousAdd")
            self.compare("OneSmartReminderPopup")
            self.compare("OKBtn")
            self.clickbtn("OKBtn")
            self.clickbtn("DelExistingReminder")
        else:
            self.logger.error("ERROR: Not able to Add Dislike to test reminder/Reminder not found")

    def gohome(self):
        """
        Method to traverse to Home screen
        :param: None
        :return: None
        """
        self.clickbtn("GoHome")

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
