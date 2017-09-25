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
#                               System Map Name: unpair system map
#                               Script Name : HCPReportLTP.py
#                               Created On: mar 31 , 2017
#                               Created By:Umesha HP (10065170)
#                               APP version :1.9.44  3551
# *************************************************************************************
# **************************************************************************************

class Unpairing(unittest.TestCase):
    """ Meter Settings"""

    def setUp(self):
        """ UnitTest Frame work method """
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

    def test_unpairing(self):
        """ unitest frame work start method"""
        if self.to_unpair() == 0:
            pass
        # This function will take the system from Home screen to meter Help
        self.verify_unpair()
        # self.about_meter()

    def to_unpair(self):
        """ This Method will take the system from Home screen to Meter settings screen. it
        returns Nothing  """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToUnpair", self.my_object)
        xpath2 = self.util.read_xpath_list_from_xml(self.object_repo, "Unpair2", self.my_object)
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Delete", "trans-unit",
                                                    Config.selected_language.strip())
        for loop_index in range(3):
            if self.my_object == "Iobject":
                self.util.client.sleep(2500)
            self.object.wait_for_element(self.util.client,
                                         xpath[loop_index]['zone'],
                                         xpath[loop_index]['xpath'],
                                         xpath[loop_index]['index'], xpath[loop_index]['comment'],
                                         20000, self.logger_name)
            if self.object.is_element_found(self.util.client, xpath[loop_index]['zone'],
                                            xpath[loop_index]['xpath'],
                                            xpath[loop_index]['index'],
                                            xpath[loop_index]['comment'], self.logger_name):
                self.object.click(self.util.client, xpath[loop_index]['zone'],
                                  xpath[loop_index]['xpath'],
                                  xpath[loop_index]['index'], xpath[loop_index]['comment'], 1,
                                  self.logger_name)
            else:
                return 0
        if self.object.is_element_found(self.util.client, xpath[3]['zone'],
                                            xpath[3]['xpath'],
                                            xpath[3]['index'],
                                            xpath[3]['comment'], self.logger_name):
            self.object.element_swipe(self.util.client, xpath[3]['zone'],
                                              xpath[3]['xpath'],
                                              xpath[3]['index'],
                                              xpath[3]['comment'],
                                              "Right", 500, 500, self.logger_name)
            self.get_text_compare(xpath, 4, text_from_xml, 0, ids, eng_list)
            self.object.click(self.util.client, xpath[4]['zone'],
                                  xpath[4]['xpath'],
                                  xpath[4]['index'], xpath[4]['comment'], 1,
                                  self.logger_name)


                # print xpath2[0]['xpath']
                # if self.object.is_element_found(self.util.client, xpath2[0]['zone'],
                #                                 xpath2[0]['xpath'],
                #                                 xpath2[0]['index'], xpath2[0]['comment'],
                #                                 self.logger_name):
                #     self.object.click(self.util.client, xpath2[0]['zone'], xpath2[0]['xpath'],
                #                       xpath2[0]['index'], xpath2[0]['comment'], 1, self.logger_name)
                # else:
                #     return 0

    def verify_unpair(self):
        """ This Method navigates and tests all the strings which are present in the screen.
         It gets strings as actual_text and get the screen text as element text and call the
         function compare.  """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Unpair", "trans-unit",
                                                    Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Unpair", self.my_object)
        len_main = len(xpath)
        text_index = 0  # index to the actual text
        loop_index = 0
        while loop_index < len_main:
            if xpath[loop_index]['xpath'] == 'click':
                if self.object.is_element_found(self.util.client,
                                                xpath[loop_index + 1]['zone'],
                                                xpath[loop_index + 1]['xpath'],
                                                xpath[loop_index + 1]['index'],
                                                xpath[loop_index]['comment'],
                                                self.logger_name):

                    self.object.click(self.util.client,
                                      xpath[loop_index + 1]['zone'],
                                      xpath[loop_index + 1]['xpath'],
                                      xpath[loop_index + 1]['index'],
                                      xpath[loop_index + 1]['comment'], 1,
                                      self.logger_name)
                    loop_index += 2
                    continue
                else:
                    return 0
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def go_home(self):
        """ go home"""
        pass

    def about_meter(self):
        """ This Method navigates and tests all the strings which are present in the screen.
         It gets strings as actual_text and get the screen text as element text and call the
         function compare.  """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "AboutMeter", "trans-unit",
                                                    Config.selected_language.strip())
        print len(text_from_xml)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "AboutMeter", self.my_object)
        len_main = len(xpath)
        text_index = 0  # index to the actual text
        loop_index = 0
        while loop_index < len_main:
            if xpath[loop_index]['xpath'] == 'click':
                if self.object.is_element_found(self.util.client,
                                                xpath[loop_index + 1]['zone'],
                                                xpath[loop_index + 1]['xpath'],
                                                xpath[loop_index + 1]['index'],
                                                xpath[loop_index]['comment'],
                                                self.logger_name):

                    self.object.click(self.util.client,
                                      xpath[loop_index + 1]['zone'],
                                      xpath[loop_index + 1]['xpath'],
                                      xpath[loop_index + 1]['index'],
                                      xpath[loop_index + 1]['comment'], 1,
                                      self.logger_name)
                    loop_index += 2
                    continue
                else:
                    return 0
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

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
