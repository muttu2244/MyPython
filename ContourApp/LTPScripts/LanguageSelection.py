"""MOdule level import"""
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
# ************************************************************************************
#                               Script Name : LanguageSelection.py
#                               Created On: jan 16 , 2016
#                               Created By:Umesha HP (10065170)
#                               APP version :1.9.44  3551
# *************************************************************************************
# **************************************************************************************

class LanguageSelection(unittest.TestCase):
    """ LanguageSelection"""

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
            self.app.launch(self.util.client, self.app_name, True, False, self.logger_name, self.logger_name)
        print self.my_object
        self.common.set_project_base_directory(self.util.client, os.getcwd(), self.logger_name)
        self.common.set_reporter(self.util.client, SYS_PATH,
                                 os.path.splitext(os.path.basename(__file__))[0], self.logger_name)
        self.config.set_show_pass_image_in_report(self.util.client, False)
        self.current_language = Config.selected_language.strip().decode('utf-8').lower()
        print self.current_language
    def test_country_selection(self):
        """ unitest frame work start method"""
        self.to_cntry_lang()
        # This function will take the system from Home screen to country language Help
        self.read_select_country()


    def to_cntry_lang(self):
        """ This Method will take the system from Home screen to country and language screen. it
        returns Nothing"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToCountry", self.my_object)

        for loop_index in range(len(xpath)):
            if self.my_object is "Iobject":
                self.util.client.sleep(2000)
            if self.object.is_element_found(self.util.client, xpath[loop_index]['zone'],
                                            xpath[loop_index]['xpath'],
                                            xpath[loop_index]['index'],
                                            xpath[loop_index]['comment'], self.logger_name):
                self.object.click(self.util.client, xpath[loop_index]['zone'],
                                  xpath[loop_index]['xpath'],
                                  xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                                  self.logger_name)


    def read_select_country(self):
        """ select language"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, self.current_language, self.my_object)
        xpath_back = self.util.read_xpath_list_from_xml(self.object_repo, "GoBack", self.my_object)
        if self.object.is_element_found(self.util.client, xpath[0]['zone'],
                                            xpath[0]['xpath'],
                                            xpath[0]['index'],
                                            xpath[0]['comment'], self.logger_name):
                # self.common.swipe_while_not_found(self.util.client,"Up",500,1000,
                #                   xpath[0]['zone'],
                #                   xpath[0]['xpath'],
                #                   xpath[0]['index'],
                #                   xpath[0]['comment'], 1000, 5, True, self.logger_name)
                self.object.click(self.util.client, xpath[0]['zone'],
                                  xpath[0]['xpath'],
                                  xpath[0]['index'], xpath[0]['comment'], 1,
                                  self.logger_name)
                self.object.click(self.util.client, xpath_back[0]['zone'],
                                  xpath_back[0]['xpath'],
                                  xpath_back[0]['index'], xpath_back[0]['comment'], 1,
                                  self.logger_name)

        else :
            print " Unable to find the Xpath"



    def tearDown(self):
        """Generates a report of the test case.
        For more information - https://docs.experitest.com/display/public/SA/Report+Of+Executed
        +Test"""
        self.app.application_close(self.util.client, self.app_name)
        self.common.generate_report(self.util.client, False)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)


if __name__ == '__main__':
    unittest.main()
