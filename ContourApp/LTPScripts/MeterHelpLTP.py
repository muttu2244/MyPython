"""this module does Meter Help"""

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
print SYS_PATH

from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate, Logger, \
    Configuration, Config

# ***********************************************************************************
# ***********************************************************************************
#                               System Map Name: Meter Help
#                               Script Name : AppHelp.py
#                               Created On: jan 18, 2016
#                               Created By:Umesha HP (10065170)
#                               App Version :1.9.44
# ************************************************************************************
# *************************************************************************************
class MeterHelp(unittest.TestCase):
    """ Based on python's pyunit (unittest) framework this TestCase verifies Language
     Translations for Meter Help on ContourApp on both Android  and  IOS Devices."""

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

    def test_meter_help(self):
        """ test meter is a unittest Framework method from where the execution starts"""
        self.to_meter_help()
        self.main_screen()  # this function tests main screen strings in App Help
        self.meter_settings()
        self.meter_app_connection()
        self.blood_sugar_meal_marker()
        self.icon_glossary()
        # self.go_home()

    def to_meter_help(self):
        """This Method will take the system from Home screen to Meter Help screen get
         Xpath and navigate to Meter Help screen. it returns None"""
        print " meter Help"
        # This function will take the system from Home screen to App Help
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "toMeterHelp",
                                                   self.my_object)
        for loop_index in range(len(xpath)):
            # self.util.client.sleep(2000)
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

    def main_screen(self):
        """ : This Method navigates and tests Meter Help Home screen Strings.
        It gets strings as actual_text and get the screen text as element strings and call the
        function compare. If the actual string is equal to the expected string both string will
        be logged else the corresponding words will be logged as result fail. It returns none."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "mainScreen", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "mainScreen",
                                                        self.my_object)

        text_index = 0
        for loop_index in range(len(xpath)):
            self.util.client.sleep(1000)
            print "index " + str(loop_index)
            if loop_index == 1:
                element_text = self.object.element_get_property(self.util.client,
                                                                xpath[loop_index]['zone'],
                                                                xpath[loop_index]['xpath'],
                                                                xpath[loop_index]['index'],
                                                                "placeholder",
                                                                self.logger_name)
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                if element_text:
                    self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
                    text_index += 1
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            # except:" not found"

    def meter_settings(self):
        """ This Method will navigate and  compare Meter Settings  screen strings.
        It gets strings as actual_text and get the screen text as element strings and call the
        function compare. If the actual string is equal to the expected string both string will
        be logged else the corresponding words will be logged as result fail. If the actual
        string is equal to the expected string both string will be logged else the corresponding
        words will be logged as result fail. It returns none."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "meterSettings", "trans-unit",
                                                  Config.selected_language.strip())
        xapth_meter_setting = self.util.read_xpath_list_from_xml(self.object_repo, "meterSettings",
                                                                 self.my_object)
        xpath_met_quest = self.util.read_xpath_list_from_xml(self.object_repo,
                                                             "meterSettingsQuestions",
                                                             self.my_object)
        xpath_met_ans = self.util.read_xpath_list_from_xml(self.object_repo, "meterSettingsAnswer",
                                                           self.my_object)
        self.object.click(self.util.client, xapth_meter_setting[0]['zone'],
                          xapth_meter_setting[0]['xpath'],
                          xapth_meter_setting[0]['index'],
                          xapth_meter_setting[0]['comment'],
                          1, self.logger_name)
        text_index = 0  # Index to the Actual text
        for loop_index in range(1, len(xapth_meter_setting)-1):
            self.util.client.sleep(1000)
            if loop_index == 2:
                try:
                    self.place_holder(xapth_meter_setting, loop_index , text_from_xml, text_index,  ids, eng_list)
                    text_index += 1
                    continue
                except:
                   print " value error"

            self.get_text_compare(xapth_meter_setting, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
        answ_list = [1, 9, 4, 3]  # number of answers in a equestion
        answer_index = 0
        for loop_index in range(0, len(xpath_met_quest)):
            print "question " + str(loop_index)

            if loop_index == 0:
                self.get_text_compare(xpath_met_quest, loop_index, text_from_xml, text_index, ids, eng_list)
                text_index += 1
                self.object.click(self.util.client, xpath_met_quest[loop_index]['zone'],
                                  xpath_met_quest[loop_index]['xpath'],
                                  xpath_met_quest[loop_index]['index'],
                                  xpath_met_quest[loop_index]['comment'],
                                  1, self.logger_name)
                self.util.client.sleep(1000)
                self.get_text_compare(xpath_met_ans, answer_index, text_from_xml, text_index, ids, eng_list)
                text_index += 1
                answer_index += 1
                self.click(xpath_met_quest, loop_index)
                continue
            if loop_index == 3:
                self.dev.swipe(self.util.client, "Down", 500, 500)

            else:
                self.get_text_compare(xpath_met_quest, loop_index, text_from_xml, text_index, ids, eng_list)
                text_index += 1
                self.click(xpath_met_quest, loop_index)
                for j in range(0, answ_list[loop_index]):
                    # self.util.client.sleep(1000)
                    #print "text :" + actual_text[text_index]
                    self.get_text_compare(xpath_met_ans, answer_index, text_from_xml, text_index, ids, eng_list)
                    text_index += 1
                    answer_index += 1
                self.dev.swipe(self.util.client, "Up", 500, 500)
                self.click(xpath_met_quest, loop_index)

        print xapth_meter_setting[4]['xpath']
        self.click(xapth_meter_setting, 4)
        # click back button to meter help

    def meter_app_connection(self):
        """ This Method will navigate and compare Meter App-Connection screen strings.
        It gets master strings as actual_text and get the screen text as element_text and call
        the function compare. It calls place_holder() method to compare the place holder text in
        the screen. If the actual string is equal to the expected string both string will be
        logged else the corresponding word will be logged as result fail. It returns none."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MeterAppConnection",
                                                  "trans-unit", Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MeterAppConnection",
                                                   self.my_object)
        length = len(xpath)
        print length
        text_index = 0
        loop_index = 0
        while loop_index < length:
            if xpath[loop_index]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.click(xpath, loop_index + 1)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'place':
                self.place_holder(xpath, loop_index + 1, text_from_xml, text_index, ids, eng_list)
                text_index += 1
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def blood_sugar_meal_marker(self):
        """ This Method will navigate and  compare blood sugar readings and meal marker  screen
        strings. It gets master strings as actual_text and get the screen text as element_text and
         then pass these two strings to compare method.
         If the actual string is equal to the expected string both string will be logged else
         the corresponding words will be logged as result fail. It returns none."""
        print " calling self.blood_sugar_meal_marker()"
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "BloodSugar", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "BloodSugar", self.my_object)
        length = len(xpath)
        print length
        text_index = 0  # index to the actual text
        loop_index = 0
        while loop_index < length:
            if xpath[loop_index]['xpath'] == 'click':
                # self.util.client.sleep(2000)
                self.click(xpath, loop_index + 1)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'place':
                self.place_holder(xpath, loop_index + 1, text_from_xml, text_index,  ids, eng_list)
                text_index += 1
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def icon_glossary(self):
        """" This Method will compare navigate and  Icon Glossary  screen strings.
         It gets master strings as actual_text and get the screen text as element_text and
          then pass these two strings to compare method. If the actual string is equal to the
          expected string both string will be logged else the corresponding words will be logged
          as result fail. It returns none."""
        text_from_xml, ids, eng_list= self.util.get_text_from_xml(self.string_xml, "IconGlossary", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "IconGlossary",
                                                        self.my_object)
        text_index = 0
        count = len(xpath)
        for loop_index in range(0, count - 1):
            try:
                if loop_index == 0 or loop_index == count - 1:
                    self.object.click(self.util.client, xpath[loop_index]['zone'],
                                      xpath[loop_index]['xpath'],
                                      xpath[loop_index]['index'],
                                      xpath[loop_index]['comment'],
                                      1, self.logger_name)
                else:

                    self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
                    text_index += 1
            except:
                print " list out of bound "

    def place_holder(self, xpath, loop_index, text_from_xml, text_index, ids, eng_list):
        """This method gets the place holder text of screen and compares.
        If the actual string is equal to the expected string both string will be
        logged else the corresponding words will be logged and reported as result fail. """
        try:
            element_text = self.object.element_get_property(self.util.client,
                                                            xpath[loop_index]['zone'],
                                                            xpath[loop_index]['xpath'],
                                                            xpath[loop_index]['index'],
                                                            "placeholder", self.logger_name)
            if element_text:
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
        except:
            print" Value not found"

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
            if element_text :
                self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                self.logger_name)
        except:
            print " Xpath doesn't found due some hidden text"

    def click(self, xpath, loop_index):
        """ This method will click the object on the screen. It returns none"""
        self.object.click(self.util.client, xpath[loop_index]['zone'],
                          xpath[loop_index]['xpath'],
                          xpath[loop_index]['index'],
                          xpath[loop_index]['comment'],
                          1, self.logger_name)

    def go_home(self):
        """ go home"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "GoHome",
                                                   self.my_object)

        for loop_index in range(0, len(xpath)):
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'],
                              xpath[loop_index]['comment'],
                              1, self.logger_name)

    def tearDown(self):
        """ Generates a report of the test case
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
