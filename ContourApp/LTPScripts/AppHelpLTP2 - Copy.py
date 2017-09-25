"""App Help Module"""
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
    Config, Configuration

# *********************************************************************
# *********************************************************************
#                               System Map Name: App Help
#                               Script Name : AppHelp.py
#                               Created On: feb 28, 2017
#                               Created By:Umesha HP (10065170)
#                               App Version 1.9.44
# **********************************************************************
# ***********************************************************************

class Apphelp(unittest.TestCase):
    """ Based on python's pyunit (unittest) framework this TestCase verifies Language
     Translations for AppHelp feature on ContourApp on both Android and iOS Devices. """

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
        self.logger.info("Script name: " + os.path.basename(
            __file__))
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
            self.app.launch(self.util.client, "search:contour", True, False, self.logger_name)
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

    def test_app_help(self):
        """ main method"""
        self.to_app_help()  # This function will take the system from Home screen to App Help
        # self.main_screen()  # this function tests main screen strings in App Help
        # self.account_set_up()
        # self.navigation()
        # if self.my_object == "Iobject":
        #     print " "
        #     self.blood_sugar_reading_meal_marker_ios()
        # else:
        #     self.blood_sugar_reading_meal_marker()
        self.target_range_critical_values()
        self.reminders_and_patterns()
        # self.reports()
        # if self.my_object == 'Iobject':
        #    self.go_home()

    def to_app_help(self):
        """# This function will take the system from Home screen to App Help"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "toAppHelp",
                                                   self.my_object)
        for loop_index in range(len(xpath)):
            if self.my_object =="Iobject":
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
            # object.click(util.client, element[0]['zone'], xpaths[index - 1]['xpath'],
            # xpaths[index - 1]['index'], 1)

    def main_screen(self):
        """: This Method navigates and tests App Help Home screen Strings.
        It gets strings as actual_text and get the screen text as element strings and call the
        function compare. If the actual string is equal to the expected string both string will
        be logged else the corresponding word will be logged as result fail """
        actual_text = self.util.get_text_from_xml(self.string_xml, "mainScreen", "trans-unit",
                                                  Config.selected_language.strip())
        xpath_main = self.util.read_xpath_list_from_xml(self.object_repo, "mainScreen",
                                                        self.my_object)
        text_index = 0  # index to actual text
        # self.util.client.sleep(2000)
        loop_index = 0
        while loop_index < len(xpath_main):
            print xpath_main[loop_index]
            if loop_index == 1:
                self.place_holder(xpath_main, loop_index, actual_text, text_index)
                text_index += 1
                loop_index += 1
                continue
            self.get_text_compare(xpath_main, loop_index, actual_text, text_index)
            text_index += 1
            loop_index += 1

    def get_text_compare(self, xpaths, xpath_index, text_from_xml, text_index):
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
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text,
                                    self.logger_name)
        except:
            print " Xpath doesn't found"

    def place_holder(self, xpath, loop_index, actual_text, text_index):
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
                self.util.text_compare2(self.common, actual_text[text_index], element_text,
                                        self.logger_name)
        except:
            print" Value not found"

    def account_set_up(self):
        """This Method will navigate and  compare Account set up  screen strings.
        It gets strings as actual_text and get the screen text as element strings and
        call the function compare. If the actual string is equal to the expected string both string
         will be logged else the corresponding words will be logged as result fail."""
        actual_text = self.util.get_text_from_xml(self.string_xml, "AccountsetUp", "trans-unit",
                                                  Config.selected_language.strip())
        print len(actual_text)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "AccountsetUp",
                                                   self.my_object)
        len_main = len(xpath)
        text_index = 0  # index to the actual text
        loop_index = 0
        while loop_index < len_main:
            if xpath[loop_index]['xpath'] == 'click':
                # self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'place':
                self.place_holder(xpath, loop_index + 1, actual_text, text_index)
                text_index += 1
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, actual_text, text_index)
            text_index += 1
            loop_index += 1

    def navigation(self):
        """ This Method will navigate and  compare Navigation  screen strings.
        It gets master strings as actual_text and get the screen text as element_text and
        call the function compare. It calls place_holder() method to compare the place holder
        text in the screen. If the actual string is equal to the expected string both string will
        be logged else the corresponding words will be logged and reported as result fail."""
        actual_text = self.util.get_text_from_xml(self.string_xml, "Navigation", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Navigation", self.my_object)
        lenth = len(xpath)
        text_index = 0
        loop_index = 0
        while loop_index < lenth:
            if xpath[loop_index]['xpath'] == 'click':
                # self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                continue
            if xpath[loop_index]['xpath'] == 'place':
                # self.place_holder(xpath,loop_index+1,actual_text,text_index)
                text_index += 1
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, actual_text, text_index)
            text_index += 1
            loop_index += 1

    def blood_sugar_reading_meal_marker(self):
        """This Method will navigate and  compare blood sugar readings and meal marker  screen
        strings. It gets master strings as actual_text and get the screen text as element_text and
        then pass these two strings to compare method. If the actual string is equal to the expected
        string both string will be logged else the corresponding words will be logged and
        reported as result fail."""
        actual_text = self.util.get_text_from_xml(self.string_xml,
                                                  "BloodSugarReadingAndMealMarkers",
                                                  "trans-unit", Config.selected_language.strip())
        actual_text2 = []
        for str1 in actual_text:
            if "<br>" in str1:
                str_li = str1.split("<br>")
                for i in str_li:
                    actual_text2.append(i)
            else:
                actual_text2.append(str1)
        text_index = 0  # index to
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "BloodSugar", self.my_object)
        self.object.click(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                          xpath[0]['index'],
                          xpath[0]['comment'],
                          1, self.logger_name)
        self.place_holder(xpath, 1, actual_text, text_index)
        text_index += 1

        xpath_questions = self.util.read_xpath_list_from_xml(self.object_repo, "BloodQuestions",
                                                             self.my_object)
        for loop_index in range(len(xpath_questions)):
            # self.object.swipe_while_not_found(self.util.client, "Down", 0, 2000,
            # xpath_questions[loop_index]['zone'],
            # xpath_questions[loop_index]['xpath'], xpath_questions[loop_index]['index'],
            #                                   100, 5, False)

            pixel = self.dev.p2cy(self.util.client, 15)
            if loop_index == 6:
                self.dev.swipe(self.util.client, "Up", pixel, 300)
            self.click(xpath_questions, loop_index)
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        xpath_b2 = self.util.read_xpath_list_from_xml(self.object_repo, "Blood2", self.my_object)
        if self.object.is_element_found(self.util.client, xpath_b2[0]['zone'], xpath_b2[0]['xpath'],
                                        xpath_b2[0]['index'], xpath[0]['comment'],
                                        self.logger_name) is False:
            self.click(xpath_b2, 1)
        string_inzone = self.object.get_text(self.util.client,
                                             "WEB")  # this method gets all string in the zone
        string_list = string_inzone.splitlines()
        string_list = self.remove_empty_lines(
            string_list)  # this method removes string with empty lines line from list

        for loop_index in range(max(len(actual_text), len(string_list)) - 1):
            # try:
            if actual_text2[text_index] and string_list[loop_index]:
                self.util.text_compare2(self.common, actual_text2[text_index],
                                        string_list[loop_index], self.logger_name)
            text_index += 1
            # except:
            #     "value error"

        self.click(xpath, 2)
    def blood_sugar_reading_meal_marker_ios(self):
        """This Method will navigate and  compare blood sugar readings and meal marker  screen
        strings. It gets master strings as actual_text and get the screen text as element_text and
        then pass these two strings to compare method. If the actual string is equal to the expected
        string both string will be logged else the corresponding words will be logged and
        reported as result fail."""
        actual_text = self.util.get_text_from_xml(self.string_xml,
                                                  "BloodSugarReadingAndMealMarkers",
                                                  "trans-unit", Config.selected_language.strip())
        actual_text2 = []
        for str1 in actual_text:
            if "<br>" in str1:
                str_li = str1.split("<br>")
                for i in str_li:
                    actual_text2.append(i)
            else:
                actual_text2.append(str1)
        text_index = 0  # index to
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "BloodSugar", self.my_object)
        self.object.click(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                          xpath[0]['index'],
                          xpath[0]['comment'],
                          1, self.logger_name)
        self.place_holder(xpath, 1, actual_text, text_index)
        text_index += 1

        xpath_questions = self.util.read_xpath_list_from_xml(self.object_repo, "BloodQuestions",
                                                             self.my_object)
        for loop_index in range(len(xpath_questions)):
            # self.object.swipe_while_not_found(self.util.client, "Down", 0, 2000,
            # xpath_questions[loop_index]['zone'],
            # xpath_questions[loop_index]['xpath'], xpath_questions[loop_index]['index'],
            #                                   100, 5, False)

            pixel = self.dev.p2cy(self.util.client, 15)
            if loop_index == 6:
                self.dev.swipe(self.util.client, "Up", pixel, 300)
            self.click(xpath_questions, loop_index)
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        xpath_b2 = self.util.read_xpath_list_from_xml(self.object_repo, "Blood2", self.my_object)
        if self.object.is_element_found(self.util.client, xpath_b2[0]['zone'], xpath_b2[0]['xpath'],
                                        xpath_b2[0]['index'], xpath[0]['comment'],
                                        self.logger_name) is False:
            self.click(xpath_b2, 1)
        string_inzone = self.object.get_text(self.util.client,
                                             "WEB")  # this method gets all string in the zone
        string_list = string_inzone.splitlines()
        string_list = self.remove_empty_lines(
            string_list)  # this method removes string with empty lines line from list

        for loop_index in range(max(len(actual_text), len(string_list)) - 1):
            # try:
            if actual_text2[text_index] and string_list[loop_index]:
                self.util.text_compare2(self.common, actual_text2[text_index],
                                        string_list[loop_index], self.logger_name)
            text_index += 1
            # except:
            #     "value error"

        self.click(xpath, 2)
    def remove_empty_lines(self, string_list):
        """This method removes string with empty lines  from list and it returns list of string
        without empty lines"""
        string_list2 = []
        for strn in string_list:
            if strn:
                line = strn.strip()
                if line == "":
                    continue
                else:
                    string_list2.append(line)
        return string_list2

    def click(self, xpath, loop_index):
        """# click the objects """
        self.object.click(self.util.client,
                          xpath[loop_index]['zone'],
                          xpath[loop_index]['xpath'],
                          xpath[loop_index]['index'],
                          xpath[loop_index]['comment'],
                          1, self.logger_name)

    def target_range_critical_values(self):
        """# (): This Method will navigate and compare target ranges and critical values  screen
        strings. It gets master strings as actual_text and get the screen text as element_text and
        then pass these two strings to compare method. If the actual string is equal to the
        expected string both string will be logged else the corresponding words will be logged and
        reported as result fail. Finally it returns none. Finally it returns none."""
        print "This Method is to comparetarget_range_critical_values help screen  strings"
        actual_text = self.util.get_text_from_xml(self.string_xml, "TargetRangeandCriticalValues",
                                                  "trans-unit", Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TargetRange", self.my_object)
        lenth = len(xpath)
        text_index = 0
        loop_index = 0
        while loop_index < lenth:
            if xpath[loop_index]['xpath'] == 'click':
                # self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'place':
                self.place_holder(xpath, loop_index + 1, actual_text, text_index)
                text_index += 1
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, actual_text, text_index)
            pixel = self.dev.p2cy(self.util.client, 15)
            self.dev.swipe(self.util.client, "Up", pixel, 300)
            text_index += 1
            loop_index += 1

    def reminders_and_patterns(self):
        """(): This Method will navigate and compare Reminders and Patterns screen strings.
        It gets master strings as actual_text and get the screen text as element_text and
        then pass these two strings to compare method. If the actual string is equal to the expected
         string both string will be logged else the corresponding words will be logged and
         reported as result fail. Finally it returns none."""
        actual_text = self.util.get_text_from_xml(self.string_xml, "Reminders",
                                                  "trans-unit", Config.selected_language.strip())
        actual_text2 = []
        for str1 in actual_text:
            if "<br>" in str1:
                str_li = str1.split("<br>")
                for i in str_li:
                    actual_text2.append(i)
            else:
                actual_text2.append(str1)
        text_index = 0
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Reminders", self.my_object)
        self.object.click(self.util.client, xpath[0]['zone'], xpath[0]['xpath'],
                          xpath[0]['index'], xpath[0]['comment'], 1, self.logger_name)
        self.place_holder(xpath, 1, actual_text, text_index)
        text_index += 1

        xpath_questions = self.util.read_xpath_list_from_xml(self.object_repo, "RemQuestions",
                                                             self.my_object)
        for loop_index in range(len(xpath_questions)):
            pixel = self.dev.p2cy(self.util.client, 15)
            if loop_index == 6:
                self.dev.swipe(self.util.client, "Up", pixel, 300)
            self.click(xpath_questions, loop_index)
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        # self.object.touch_down(self.util.client, xpath[1]['zone'],
        #                        xpath[1]['xpath'],
        #                        xpath[1]['index'],
        #                        xpath[1]['comment'],
        #                        self.logger_name)
        # self.object.touch_move(self.util.client, xpath[2]['zone'], xpath[2]['xpath'], xpath[2][
        # 'index'])
        # self.object.touch_up(self.util.client, self.logger_name)
        string_inzone = self.object.get_text(self.util.client,
                                             "WEB")  # this method gets all string in the zone
        string_list = string_inzone.splitlines()
        string_list = self.remove_empty_lines(
            string_list)  # this method removes string with empty lines line from list

        for loop_index in range(max(len(actual_text), len(string_list)) - 1):
            try:
                if actual_text2[text_index] and string_list[loop_index]:
                    self.util.text_compare2(self.common, actual_text2[text_index],
                                            string_list[loop_index], self.logger_name)
                text_index += 1
            except:
                print "value error"
        self.click(xpath, 2)

    def reports(self):
        """This Method will compare navigate and  Reports screen strings.
        It gets master strings as actual_text and get the screen text as element_text and then
         pass these two strings to compare method. If the actual string is equal to the expected
         string both string will be logged else the corresponding words will be logged and
         reported as result fail."""
        actual_text = self.util.get_text_from_xml(self.string_xml, "Reports", "trans-unit",
                                                  Config.selected_language.strip())
        text_index = 0
        actual_text2 = []
        for str1 in actual_text:
            if "<br>" in str1:
                str_li = str1.split("<br>")
                for i in str_li:
                    actual_text2.append(i)
            else:
                actual_text2.append(str1)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Reports", self.my_object)
        self.object.click(self.util.client, xpath[0]['zone'],
                          xpath[0]['xpath'],
                          xpath[0]['index'],
                          xpath[0]['comment'],
                          1, self.logger_name)
        self.place_holder(xpath, 1, actual_text, text_index)
        text_index += 1

        xpath_questions = self.util.read_xpath_list_from_xml(self.object_repo, "ReportsQues",
                                                             self.my_object)
        for loop_index in range(len(xpath_questions)):
            pixel = self.dev.p2cy(self.util.client, 15)
            self.click(xpath_questions, loop_index)
            self.dev.swipe(self.util.client, "Down", pixel, 300)
        # self.object.touch_down(self.util.client, xpath[1]['zone'], xpath[1]['xpath'], xpath[1][
        # 'index'])
        # #self.object.touch_move(self.util.client, xpath[2]['zone'], xpath[2]['xpath'],
        # xpath[2]['index'])
        # self.object.touch_up(self.util.client)
        string_inzone = self.object.get_text(self.util.client,
                                             "WEB")  # this method gets all string in the zone
        string_list = string_inzone.splitlines()
        string_list = self.remove_empty_lines(
            string_list)  # this method removes string with empty lines line from list

        for loop_index in range(max(len(actual_text), len(string_list))):
            try:
                if actual_text2[text_index] and string_list[loop_index]:
                    self.util.text_compare2(self.common, actual_text2[text_index],
                                            string_list[loop_index], self.logger_name)
                text_index += 1
            except:
                print "value error"
        self.click(xpath, 2)

    def go_home(self):
        """go_home """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "GoHome", self.my_object)
        for loop_index in range(0, len(xpath)):
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'],
                              xpath[loop_index]['comment'],
                              1, self.logger_name)

    def tearDown(self):
        """ Generates a report of the test case.
        For more information -
         https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test"""
        # self.app.application_close(self.util.client, self.app_name)

        self.common.generate_report(self.util.client, False)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)


if __name__ == '__main__':
    unittest.main()
