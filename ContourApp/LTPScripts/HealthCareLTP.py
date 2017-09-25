"""This module does health care LTP"""
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
# **********************************************************************************
#                               System Map Name: Meter ERROR code
#                               Script Name : AppHelp.py
#                               Created On: jan 11 , 2017
#                               Created By:Umesha HP (10065170)
#                               App version :1.9.44
#                               Last modified : 17/4/2017
# ***********************************************************************************
# ***********************************************************************************

class HealthCare(unittest.TestCase):
    """ Health Care"""

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
    def test_healthcare(self):
        """ unitest frame work init method"""
        self.to_healthcare()  # This function will take the system from Home screen to meter Help
        self.verify_healthcare()
        self.verify_edit_health()

    def to_healthcare(self):
        """ This Method will take the system from Home screen to new Health Care team home  screen.
        It returns None"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToHealthCare",
                                                   self.my_object)
        for loop_index in range(len(xpath)):
            self.util.client.sleep(2000)
            print xpath[loop_index]['xpath']
            self.object.wait_for_element(self.util.client,
                                         xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'], xpath[loop_index]['comment'],
                                         20000, self.logger_name)
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                              self.logger_name)

    def verify_healthcare(self):
        """ This Method navigates and tests all the strings which are present in the screen.
         This Method compares Health Care Team and its inner screen strings.
        It mainly loop through the elements if Xpath in the Object xml is "click" the up next
        object is to be clicked. If Xpath in the Object xml is "text" it sends the text to device
        else it gets the Xpath and calls get_text_compare() and validates screen strings.
        If the actual string is equal to the expected string both string will be logged
        else the corresponding words will be logged as result fail.
        It returns None"""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "HealthCare", "trans-unit",
                                                    Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "HealthProfessional",
                                                   self.my_object)
        len_main = len(xpath)
        text_index = 0
        loop_index = 0
        # try:
        while loop_index < len_main:
            if xpath[loop_index]['xpath'] == 'click':
                # self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'], xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)

                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'wait':
                self.object.wait_for_element(self.util.client,
                                             xpath[loop_index + 3]['zone'],
                                             xpath[loop_index + 3]['xpath'],
                                             xpath[loop_index + 3]['index'],
                                             xpath[loop_index + 3]['comment'],
                                             400000, self.logger_name)

                loop_index += 2
                continue

            if xpath[loop_index]['xpath'] == "popup":
                # self.util.client.sleep(2000)
                if self.object.is_element_found(self.util.client,
                                                xpath[loop_index + 1]['zone'],
                                                xpath[loop_index + 1]['xpath'],
                                                xpath[loop_index + 1]['index'],
                                                xpath[loop_index + 1]['comment'],
                                                self.logger_name):
                    self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                      xpath[loop_index + 1]['xpath'],
                                      xpath[loop_index + 1]['index'],
                                      xpath[loop_index + 1]['comment'],
                                      1, self.logger_name)
                loop_index += 2
                continue

            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1  # after each comparison increment actual text index by one
            loop_index += 1
        xpath_add = self.util.read_xpath_list_from_xml(self.object_repo, "AddName",
                                                       self.my_object)
        self.object.click(self.util.client, xpath_add[0]['zone'],
                          xpath_add[0]['xpath'],
                          xpath_add[0]['index'],
                          xpath_add[0]['comment'],
                          1, self.logger_name)
        self.dev.send_text(self.util.client, "New", self.logger_name)
        self.dev.close_keyboard(self.util.client)
        self.object.click(self.util.client, xpath_add[1]['zone'],
                          xpath_add[1]['xpath'],
                          xpath_add[1]['index'],
                          xpath_add[1]['comment'],
                          1, self.logger_name)
        # except:
        #     print " Value error"

    def verify_edit_health(self):
        """
        :return:
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Edit", "trans-unit",
                                                    Config.selected_language.strip())
        text_index = 0
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Edit", self.my_object)
        xpath_edit = self.util.read_xpath_list_from_xml(self.object_repo, "AddName", self.my_object)
        length_xpath = len(xpath)
        if self.object.is_element_found(self.util.client, xpath[1]['zone'],
                                        xpath[1]['xpath'],
                                        xpath[1]['index'],
                                        xpath[1]['comment'], self.logger_name):
            # self.object.click(self.util.client, xpath[1]['zone'],
            #                   xpath[1]['xpath'],
            #                   xpath[1]['index'],
            #                   xpath[1]['comment'],
            #                   1, self.logger_name)
            loop_index = 0
            try :
                while loop_index < length_xpath:
                    print xpath[loop_index]["xpath"]
                    if xpath[loop_index]['xpath'] == 'click':
                        # self.util.client.sleep(2000)
                        self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                          xpath[loop_index + 1]['xpath'],
                                          xpath[loop_index + 1]['index'], xpath[loop_index + 1]['comment'],
                                          1, self.logger_name)
                        loop_index += 2
                        continue
                    if xpath[loop_index]['xpath'] == 'text':  # edit the Health care team
                        self.object.click(self.util.client, xpath_edit[0]['zone'],
                                          xpath_edit[0]['xpath'],
                                          xpath_edit[0]['index'],
                                          xpath_edit[0]['comment'],
                                          1, self.logger_name)
                        self.dev.send_text(self.util.client, "New1", self.logger_name)
                        self.dev.close_keyboard(self.util.client)
                        loop_index += 1
                        continue
                    self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
                    text_index += 1  # after each comparison increment actual text index by one
                    loop_index += 1
            except :print " xpath doesnt found due to some issues with app"
    # def delete(self):

    def get_text_compare(self, xpaths, xpath_index, text_from_xml, text_index, ids, eng_list):
        """ This method takes xpath and xxpath inxex and get the
        text from the device using elementGetText method and compare the actual string  against
        device text """
        element_text = self.common.element_get_text(self.util.client, xpaths[xpath_index]['zone'],
                                                    xpaths[xpath_index]['xpath'],
                                                    xpaths[xpath_index]['comment'],
                                                    self.logger_name,
                                                    xpaths[xpath_index]['index'])
        if element_text is None:
            element_text = self.object.element_get_property(self.util.client,
                                                            xpaths[xpath_index]['zone'],
                                                            xpaths[xpath_index]['xpath'],
                                                            xpaths[xpath_index]['index'], "text",
                                                            self.logger_name)
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        if element_text :
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                self.logger_name)

    def go_home(self):
        """ This method take the system from new Health Care Team to App home screen.Finally it
        returns None """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToHome", self.my_object)
        for loop_index in range(len(xpath)):
            # self.util.client.sleep(2000)
            # print xpath[loop_index]['xpath']
            self.object.wait_for_element(self.util.client, xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'], 20000)
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'], 1)

    def tearDown(self):
        """Generates a report of the test case.
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
