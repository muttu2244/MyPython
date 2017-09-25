"""module"""
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
    Configuration, Config

# *********************************************************************************
# *********************************************************************************
#                               System Map Name: FAQ(Help system Map)
#                               Script Name : FAQ.py
#                               Created On: FEb 24 , 2017
#                               Created By:Umesha HP (10065170)
# ***********************************************************************************
# ************************************************************************************

class FAQ(unittest.TestCase):
    """ FAQ class"""

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

    def test_faq(self):
        """ unitest frame work start method"""
        self.to_faq()  # This function will take the system from Home screen to meter Help
        self.verify_faq()
        self.about()

    def to_faq(self):
        """ FAQ
        This function will take the system from Home screen to App Help FAQ
        """

        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToFAQ",
                                                   self.my_object)
        for loop_index in range(len(xpath)):
            if self.my_object =="Iobject":
                self.util.client.sleep(2500)
            self.object.wait_for_element(self.util.client, xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'], xpath[loop_index]['index'],
                                         xpath[loop_index]['comment'],
                                         100000, self.logger_name)
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                              self.logger_name)

    def verify_faq(self):
        """ This Method compares FAQ screen strings.
        1.	This method starts with clicking all the question index.
        2.	Once all questions are clicked, it makes hidden answer strings visible on the screen.
        3.	Once all strings visible on the screen call the get_text() method this method returns
            all strings which are present in the zone.
        4.	After getting a huge single string split the string by lines and remove empty lines
            using remove_empty_lines() method.
        5.	Now compare master string vs screen string line by line.
        Note: here consider one paragraph as single string or line. finally it returns None """
        actual_text, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "FAQ", "trans-unit",
                                                  Config.selected_language.strip())
        actual_text2 = []
        for str1 in actual_text:
            if "<br>" in str1:
                str_li = str1.split("<br>")
                for i in str_li:
                    actual_text2.append(i)
            else:
                actual_text2.append(str1)
        text_index = 0
        # xpath_place = self.util.read_xpath_list_from_xml(self.object_repo, "SearchFaq",
        # self.my_object)
        # xpath_qes = self.util.read_xpath_list_from_xml(self.object_repo, "FaqQuestions",
        # self.my_object)
        # xpath = xpath_qes[0]['xpath'] #xpath  for staring question object
        # zone = xpath_qes[0]['zone']  #zone of starting  question object
        # index = xpath_qes[0]['index']
        # index of starting question object this is required to get the next question index
        # self.place_holder(xpath_place, 0, actual_text, text_index)
        # text_index += 1
        # for loop_index in range(0, 31):
        #     pixel = self.dev.p2cy(self.util.client, 10)
        #     # if loop_index % 3==0:
        #     #     self.dev.swipe(self.util.client, "Up", pixel, 300)
        #     self.object.swipe_while_not_found(self.util.client, "Down", pixel, 1000, zone,
        # xpath, index, 1000, 10,  True)
        #     # self.object.click(self.util.client, zone, xpath, index, 1)
        #     index += 1 # increment the index by one to get next question xpath
        #     pixel = self.dev.p2cy(self.util.client, 15) #swipe according to device screen
        # resolution
        #     self.dev.swipe(self.util.client, "Down", pixel, 1000)
        # self.object.touch_down(self.util.client, xpath_place[0]['zone'], xpath_place[0]['xpath'],
        #                        xpath_place[0]['index'])
        # self.object.touch_move(self.util.client, xpath_place[0]['zone'], xpath_place[0]['xpath'],
        #                        xpath_place[0]['index'])
        # self.object.touch_up(self.util.client)
        # #these three strings missing
        # self.object.click(self.util.client, zone, xpath, 5, 1)
        # self.object.click(self.util.client, zone, xpath, 6, 1)
        # self.object.click(self.util.client, zone, xpath, 30, 1)
        self.util.client.sleep(5000)
        string_inzone = self.object.get_text(self.util.client,
                                             "WEB")  # this method gets all string in the zone
        string_list = string_inzone.splitlines()
        # split the whole string into multiple lines to matches with the master string
        string_list = self.remove_empty_lines(
            string_list)  # this method removes string with empty lines line from list
        print actual_text2
        for loop_index in range(max(len(actual_text), len(string_list)) - 1):
            print loop_index
            print actual_text2[text_index]
            print string_list[loop_index]
            if actual_text2[text_index] and string_list[loop_index]:
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                self.util.text_compare2(self.common, actual_text2[text_index], string_list[loop_index],
                                ids[text_index],
                                self.logger_name)
            text_index += 1  # increment the string index by one

        #
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "FaqBack", self.my_object)
        self.click(xpath, 0)

    def remove_empty_lines(self, string_list):
        """ The main purpose of this method is to remove the empty lines by splitting whole
        string into multiple lines/paragraph which is exactly same as a string with unique id.
        Sometime empty line come due to the space between one string to another string. So need
        to remove."""
        string_list2 = []
        for strn in string_list:
            if strn:
                line = strn.strip()
                if line == "":
                    continue
                else:
                    string_list2.append(line)
        return string_list2

    def click(self, xpath, i):
        """click the object on the screen..this method is to avoid the duplication of code"""
        self.object.click(self.util.client, xpath[i]['zone'],
                          xpath[i]['xpath'], xpath[i]['index'], xpath[i]['comment'], 1,
                          self.logger_name)

    def place_holder(self, xpath, i, text_from_xml, text_index, ids, eng_list):
        """This method get the place holder text of screen and compares"""
        print "in place Holder"

        try:
            element_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                            xpath[i]['xpath'], xpath[i]['index'],
                                                            "placeholder", self.logger_name)
            if element_text:
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                self.logger_name)
        except:
            print " Value not found"

    def about(self):
        """
        Method to compare the strings in the About screen
        :param: None
        :return: None
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "About", "trans-unit",
                                                    Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "About", self.my_object)
        self.object.click(self.util.client,
                          xpath[0]['zone'],
                          xpath[0]['xpath'],
                          xpath[0]['index'],
                          xpath[0]['comment'],
                          1, self.logger_name)
        text_index = 0
        self.util.client.sleep(1000)
        for loop_index in range(1, len(xpath)):
            element_text = self.common.element_get_text(self.util.client, xpath[loop_index]['zone'],
                                                        xpath[loop_index]['xpath'],
                                                        xpath[loop_index]['comment'],
                                                        self.logger_name,
                                                        xpath[loop_index]['index'])
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                            self.logger_name)
            text_index += 1

    def tearDown(self):
        """ Generates a report of the test case.
        For more information -
         https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test"""
        self.app.application_close(self.util.client, self.app_name)
        if self.my_object == "Iobject":
            self.app.application_close(self.util.client, "com.onyx.-")

        self.common.generate_report(self.util.client, False)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)
