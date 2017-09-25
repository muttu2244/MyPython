''' This module does edit entry LTP'''
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
#                               System Map Name: Edit ENTRY
#                               Script Name : EditEntryLTP.py
#                               Created On: jan 13 , 2016
#                               Created By:Umesha HP (10065170)
#                               APP version :1.9.44
# **********************************************************************
# **********************************************************************
class EditEntry(unittest.TestCase):
    """This class does edit entry LTP"""

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

    def test_edit_entry(self):
        """ unitest frame work start method"""
        self.verify_staring_popups()
        self.to_edit_entry()
        # if self.my_object == "Iobject":
        #     self.menu_item_ios()
        # else:
        self.verify_menu_strings()
        self.medication()

    def verify_staring_popups(self):
        """This Method will take the system from Home screen to Edit Entry screen get Xpath and
        navigate to Edit Entry Home screen. This Method compares edit entry Home screen. First
        give some integer value to get it appear on the device.In this method some un expected
         screens comes to handle these popup() method written.
        It mainly loop through the elements if Xpath in the Object xml is "click"
        the up next object is to be clicked. If Xpath in the Object xml is "text" it sends
        the text to device else it gets the Xpath and calls get_text_compare() for string
        validation.
        :return: none
        """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "StartingPopUps", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "StartingPopUps", self.my_object)
        len_main = len(xpath)
        text_index = 0
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[i + 1]['zone'],
                                  xpath[i + 1]['xpath'],
                                  xpath[i + 1]['index'],
                                  xpath[i + 1]['comment'],
                                  1, self.logger_name)
                i += 2
                continue
            if xpath[i]['xpath'] == 'swipeup':
                self.util.client.sleep(2000)
                self.object.element_swipe(self.util.client, xpath[i + 1]['zone'],
                                          xpath[i + 1]['xpath'],
                                          xpath[i + 1]['index'],
                                          xpath[i + 1]['comment'],
                                          "Up",
                                          300, 500, self.logger_name)
                i += 2
                continue
            if xpath[i]['xpath'] == 'swipedown':
                self.util.client.sleep(2000)
                self.object.element_swipe(self.util.client, xpath[i + 1]['zone'],
                                          xpath[i + 1]['xpath'],
                                          xpath[i + 1]['index'],
                                          xpath[i + 1]['comment'],
                                          "Down",
                                          300, 500, self.logger_name)
                i += 2
                continue

            if xpath[i]['xpath'] == 'text':
                self.dev.send_text(self.util.client, "9", self.logger_name)
                self.util.client.sleep(2000)  # data file for entries (format???)...
                self.dev.close_keyboard(self.util.client)
                i += 1
                continue
            self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def to_edit_entry(self):
        """This Method will take the system from Home screen to Edit Entry screen get Xpath and
        navigate to Edit Entry Home screen. This Method compares edit entry Home screen. First
        give some integer value to get it appear on the device.In this method some un expected
         screens comes to handle these popup() method written.
        It mainly loop through the elements if Xpath in the Object xml is "click"
        the up next object is to be clicked. If Xpath in the Object xml is "text" it sends
        the text to device else it gets the Xpath and calls get_text_compare() for string
        validation. """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MainScreen", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MainScreen", self.my_object)
        len_main = len(xpath)
        text_index = 0
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[i + 1]['zone'],
                                  xpath[i + 1]['xpath'],
                                  xpath[i + 1]['index'],
                                  xpath[i + 1]['comment'],
                                  1, self.logger_name)
                i += 2
                continue
            if xpath[i]['xpath'] == 'text':
                self.dev.send_text(self.util.client, "142", self.logger_name)
                self.util.client.sleep(2000)  # data file for entries (format???)...
                self.dev.close_keyboard(self.util.client)
                i += 1
                continue
            if xpath[i]['xpath'] == "popup":
                self.popup()
                i += 1
                continue
            self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def verify_menu_strings(self):
        """This Method compares Menu screen strings.
        It mainly loop through the elements if Xpath in the Object xml is "click" the up next
        object is to be clicked. If Xpath in the Object xml is 'text' it sends the text to device
        else it gets the Xpath and calls get_text_compare(). Sometime unexpected screen
        It gets strings as actual_text and gets the screen text as element text compares."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MenuItem", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MenuItem", self.my_object)
        len_main = len(xpath)
        text_index = 0
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[i + 1]['zone'],
                                  xpath[i + 1]['xpath'],
                                  xpath[i + 1]['index'],
                                  xpath[i + 1]['comment'],
                                  1, self.logger_name)
                i += 2
                print i
                continue
            if xpath[i]['xpath'] == "popupcarbs":  # first time unit selection popup will come to
                #  handle
                self.popup_carbs()
                i += 1
                continue
            if self.object.is_element_found(self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                                            xpath[i]['index'], xpath[i]['comment'],
                                            self.logger_name):
                self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def menu_item_ios(self):
        """This Method compares Menu screen strings.
        It mainly loop through the elements if Xpath in the Object xml is 'click' the up next
        object is to be clicked. If Xpath in the Object xml is 'text' it sends the text to device
        else it gets the Xpath and calls get_text_compare(). Sometime unexpected screen
        It gets strings as actual_text and gets the screen text as element text compares."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MenuItem", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "MenuItem", self.my_object)
        len_main = len(xpath)
        text_index = 0
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[i + 1]['zone'],
                                  xpath[i + 1]['xpath'],
                                  xpath[i + 1]['index'],
                                  xpath[i + 1]['comment'],
                                  1, self.logger_name)
                i += 2
                print i
                continue
            if xpath[i]['xpath'] == 'text':
                self.dev.send_text(self.util.client, "new", self.logger_name)
                self.util.client.sleep(2000)  # data file for entries (format???)...
                self.dev.close_keyboard(self.util.client)
                i += 1
            self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def medication(self):
        """This Method compares medication screen strings.
        It mainly loop through the elements if Xpath in the Object xml is "click"
        the up next object is to be clicked else it gets the Xpath and calls get_text_compare()
        to validate strings. If the actual string is equal to the expected string both string
        will be logged else the corresponding words will be logged as result fail."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Medication", "trans-unit",
                                                                   Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Medication", self.my_object)
        len_main = len(xpath)
        text_index = 0
        i = 0
        while i < len_main:
            if xpath[i]['xpath'] == 'click':
                self.util.client.sleep(2000)
                self.object.click(self.util.client, xpath[i + 1]['zone'],
                                  xpath[i + 1]['xpath'],
                                  xpath[i + 1]['index'],
                                  xpath[i + 1]['comment'],
                                  1, self.logger_name)
                i += 2
                print i
                continue
            self.get_text_compare(xpath, i, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            i += 1

    def popup(self):
        """ This method is to handle some irregular screen which appears in the device .
        if Xpath is click root method calls this method and verifies  the screen presence ,if it is,
        it compares and then navigates to next screen else it does nothing.  """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "PopUp", self.my_object)
        len_main = len(xpath)
        print len_main
        if self.object.is_element_found(self.util.client, xpath[1]['zone'], xpath[1]['xpath'],
                                        xpath[1]['index'], xpath[1]['comment'],
                                        self.logger_name) and \
                self.object.is_element_found(self.util.client, xpath[2]['zone'],
                                             xpath[2]['xpath'], xpath[1]['index'],
                                             xpath[1]['comment'], self.logger_name):
            self.object.click(self.util.client, xpath[2]['zone'],
                              xpath[2]['xpath'],
                              xpath[2]['index'],
                              xpath[2]['comment'],
                              1, self.logger_name)

    def popup_carbs(self):
        """ This method is to handle some irregular screen which appears in the device .
        if Xpath is click root method calls this method and verifies  the screen presence ,if it is,
        it compares and then navigates to next screen else it does nothing.  """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "PopUpCarbs", self.my_object)
        len_main = len(xpath)
        print len_main
        if self.object.is_element_found(self.util.client, xpath[1]['zone'], xpath[1]['xpath'],
                                        xpath[1]['index'], xpath[1]['comment'],
                                        self.logger_name) and \
                self.object.is_element_found(self.util.client, xpath[2]['zone'],
                                             xpath[2]['xpath'], xpath[1]['index'],
                                             xpath[1]['comment'], self.logger_name):
            self.object.click(self.util.client, xpath[6]['zone'],
                              xpath[6]['xpath'],
                              xpath[6]['index'],
                              xpath[6]['comment'],
                              1, self.logger_name)
            self.object.click(self.util.client, xpath[7]['zone'],
                              xpath[7]['xpath'],
                              xpath[7]['index'],
                              xpath[7]['comment'], 1, self.logger_name)

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
        if element_text:
            self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                    self.logger_name)

    def tearDown(self):
        """ Generates a report of the test case.
        #For more informatsion-https://docs.experitest.com/display/public/SA/Report+Of+Executed
        +Test"""
        self.app.application_close(self.util.client, self.app_name)
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
