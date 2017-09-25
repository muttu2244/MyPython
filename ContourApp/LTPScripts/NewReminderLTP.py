"""this module does LTP of Reminder"""
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


# **********************************************************************************
# **********************************************************************************
#                               System Map Name: New Reminder
#                               Script Name : NewReminderLTP.py
#                               Created On: jan 7 , 2016
#                               Created By:Umesha HP (10065170)
#                               App Version :1.9.44
# **********************************************************************************
# ************************************************************************************

class NewReminder(unittest.TestCase):
    """ tBased on python's pyunit (unittest) framework this TestCase verifies
     Language Translations for New Reminder on ContourApp on both Android and IOS Devices """

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

    def test_new_reminder(self):
        """ test reminder"""
        print "i am in start"
        self.to_reminder()  # This function will take the system from Home screen to meter Help
        self.main_screen()
        self.take_my_medication()
        self.log()
        self.blood_sugar()
        self.others()
        self.delete_reminder()
        # self.go_home()

    def to_reminder(self):
        """ This Method will take the system from Home screen to Meter Error codes screen get
        Xpath and navigate to New Reminder home screen."""
        print "To Reminder"
        # This function will take the system from Home screen to to reminder
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "ToReminder",
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
        """This Method navigates and tests all the strings which are present in the new reminder
        home screen. It gets strings as actual_text and get the screen text as element strings
        and call the function compare."""
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "MainScreen", "trans-unit",
                                                  Config.selected_language.strip())

        xpath_main = self.util.read_xpath_list_from_xml(self.object_repo, "MainScreen",
                                                        self.my_object)
        len_main = len(xpath_main)
        text_index = 0
        for loop_index in range(len_main):
            print loop_index
            # self.util.client.sleep(1000)
            self.get_text_compare(xpath_main, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1

    def take_my_medication(self):
        """ This Method  compare take my medication screen strings .
         It mainly loop through the elements if Xpath in the Object xml is "click" the up
        next object is to be clicked. If Xpath in the Object xml is "text" it sends the text to
        device else it gets the Xpath and calls get_text_compare().
        """
        text_index = 0
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "TakeMyMedication", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TakeMyMedication",
                                                   self.my_object)
        loop_index = 0
        while loop_index <= len(xpath) - 1:
            # self.util.client.sleep(2000)
            print loop_index
            if xpath[loop_index]['xpath'] == 'click':
                self.object.wait_for_element(self.util.client, xpath[loop_index + 1]['zone'],
                                             xpath[loop_index + 1]['xpath'],
                                             xpath[loop_index + 1]['index'],
                                             xpath[loop_index + 1]['comment'],
                                             20000, self.logger_name)
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'placeHolder':  # get nd compare place holder text
                self.object.wait_for_element(self.util.client, xpath[loop_index + 1]['zone'],
                                             xpath[loop_index + 1]['xpath'],
                                             xpath[loop_index + 1]['index'],
                                             xpath[loop_index + 1]['comment'],
                                             20000, self.logger_name)
                element_text = self.object.element_get_property(self.util.client,
                                                                xpath[loop_index + 1]['zone'],
                                                                xpath[loop_index + 1]['xpath'],
                                                                xpath[loop_index + 1]['index'],
                                                                "placeholder",
                                                                self.logger_name)
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                if element_text:
                    self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
                loop_index += 2
                text_index += 1
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'text':
                loop_index += 1
                self.object.element_send_text(self.util.client, xpath[loop_index]['zone'],
                                              xpath[loop_index]['xpath'],
                                              xpath[loop_index]['index'],
                                              "NEW", xpath[loop_index]['comment'],
                                              self.logger_name)
                # self.object.click(self.util.client,xpath[loop_index+1]['zone'],
                # xpath[loop_iidex+1]['xpath'],
                #           xpath[loop_index+1]['index'], 1)
                loop_index += 1
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def log(self):
        """ this method calls based_on() and specific() methods to captures and compares all the
        screen of photo, note, activity, food. Since all the screen navigation and Xpaths are
        same across sub screens so based_on() and specific_time () will cover all the screens.  """
        text_index = 0
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Log", "trans-unit",
                                                  Config.selected_language.strip())
        xpath_main = self.util.read_xpath_list_from_xml(self.object_repo, "LogMain",
                                                        self.my_object)
        xpath_back = self.util.read_xpath_list_from_xml(self.object_repo, "LogBack",
                                                        self.my_object)  # xapth variable to get
        # back the Home
        # xpath_days=self.util.read_xpath_list_from_xml(self.object_repo, "Days",self.my_object)
        loop_index = 0
        while True:
            print "inside logmain "
            if xpath_main[loop_index]['xpath'] == 'click':
                # if xpath value read is click, it clicks the object and
                #  here  increments xpath by 2 to get the next object xpath
                self.object.click(self.util.client, xpath_main[loop_index + 1]['zone'],
                                  xpath_main[loop_index + 1]['xpath'],
                                  xpath_main[loop_index + 1]['index'],
                                  xpath_main[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                continue
            if xpath_main[loop_index]['xpath'] == 'end':
                break
            self.get_text_compare(xpath_main, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1
        xpath_menu = self.util.read_xpath_list_from_xml(self.object_repo, "LogMenu",
                                                        self.my_object)  # there are 4 menus to test
        listlog = ["Photo", 'Note', 'Activity',
                   'Food']  # log menu item to pass it to basedOn() and specific_time()
        for j in range(len(xpath_menu)):
            print " processing menu item " + listlog[j]
            self.object.click(self.util.client, xpath_menu[j]['zone'],
                              xpath_menu[j]['xpath'],
                              xpath_menu[j]['index'],
                              xpath_menu[j]['comment'],
                              1, self.logger_name)
            self.specific_time(listlog[j].strip() + "Specific")
            self.based_on(listlog[j].strip() + "Based")
        self.object.click(self.util.client, xpath_back[0]['zone'],
                          xpath_back[0]['xpath'],
                          xpath_back[0]['index'],
                          xpath_back[0]['comment'],
                          1, self.logger_name)

    def blood_sugar(self):
        """ This Method  compares blood sugar and its inner  screen strings .
        It mainly loop through the elements if Xpath in the Object xml is "click" the up next
        object is to be clicked. If Xpath in the Object xml is "text" it sends the text to device
        else it gets the Xpath and calls get_text_compare() and validates screen strings. """
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "TestMyBlood", "trans-unit",
                                                  Config.selected_language.strip())

        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "TestMyBloodSugar",
                                                   self.my_object)
        xpath_2 = self.util.read_xpath_list_from_xml(self.object_repo, "TestBlood2",
                                                     self.my_object)
        xpath_days = self.util.read_xpath_list_from_xml(self.object_repo, "Days", self.my_object)
        loop_index = 0
        text_index = 0  # index to the actual text
        while loop_index <= len(xpath) - 1:
            # self.util.client.sleep(1000)
            if xpath[loop_index]['xpath'] == 'click':
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                continue
            if xpath[loop_index]['xpath'] == 'days':  # get and compare place holder text
                for j in range(len(xpath_days)):
                    # self.util.client.sleep(2000)
                    self.get_text_compare(xpath_days, j, text_from_xml, text_index, ids, eng_list)
                    text_index += 1
                loop_index += 1
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1
        loop_index = 0
        while True:
            # self.util.client.sleep(2000)
            if xpath_2[loop_index]['xpath'] == 'end':
                break  # stop the loop when you hit end in the xpath value
            if xpath_2[loop_index]['xpath'] == 'click':
                self.object.click(self.util.client, xpath_2[loop_index + 1]['zone'],
                                  xpath_2[loop_index + 1]['xpath'],
                                  xpath_2[loop_index + 1]['index'],
                                  xpath_2[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                continue
            self.get_text_compare(xpath_2, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def specific_time(self, log_item):
        """ This method is common across the screen it avoids duplication of  code.
        It takes sub screen name as an input argument and validate the screen strings which are
        comes under this screen"""
        xpath_days = self.util.read_xpath_list_from_xml(self.object_repo, "Days", self.my_object)
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "SpecificTime",
                                                   self.my_object)
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, log_item, "trans-unit",
                                                  Config.selected_language.strip())
        text_index = 0
        loop_index = 0
        while loop_index <= len(xpath) - 1:
            # self.util.client.sleep(2000)
            print loop_index
            if xpath[loop_index]['xpath'] == 'click':
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            if xpath[loop_index]['xpath'] == 'days':  # get and compare days
                for j in range(len(xpath_days)):
                    # self.util.client.sleep(2000)
                    self.get_text_compare(xpath_days, j, text_from_xml, text_index, ids, eng_list)
                    text_index += 1
                loop_index += 1
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

    def based_on(self, log_item):
        """ This method is common across the screen it avoids duplication of  code.
         It takes sub screen name as an input argument and validate
         the screen strings which are comes under this screen.  """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "BasedOn", self.my_object)
        text_from_xml, ids, eng_list  = self.util.get_text_from_xml(self.string_xml, log_item, "trans-unit",
                                                  Config.selected_language.strip())
        text_index = 0
        loop_index = 0
        print "inside based on my blood sugar level " + str(len(xpath))
        while loop_index <= len(xpath) - 1:
            # self.util.client.sleep(2000)
            print loop_index
            if xpath[loop_index]['xpath'] == 'click':
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                print loop_index
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1  # index to the actual text Index
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
            if element_text:
                self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
        except:
            print " Xpath doesn't found due some hidden text"

    def others(self):
        """ This Method  compare blood sugar and its inner  screen strings .
        It mainly loop through the elements if Xpath in the Object xml is "click" the up next
        object is to be clicked. If Xpath in the Object xml is "text" it sends the text to device
        else it gets the Xpath and calls get_text_compare() and validates screen strings."""
        text_index = 0
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "Others", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "Others", self.my_object)
        # xpath_days=self.util.read_xpath_list_from_xml(self.object_repo, "Days",self.my_object)
        loop_index = 0
        while loop_index < len(xpath):
            if xpath[loop_index]['xpath'] == 'click':
                self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                  xpath[loop_index + 1]['xpath'],
                                  xpath[loop_index + 1]['index'],
                                  xpath[loop_index + 1]['comment'],
                                  1, self.logger_name)
                loop_index += 2
                continue
            if xpath[loop_index]['xpath'] == 'placeholder':
                element_text = self.object.element_get_property(self.util.client,
                                                                xpath[loop_index + 1]['zone'],
                                                                xpath[loop_index + 1]['xpath'],
                                                                xpath[loop_index + 1]['index'],
                                                                "placeholder",
                                                                self.logger_name)
                self.logger.info("Testing StringID == " + str(ids[text_index]))
                self.logger.info("English Text == " + eng_list[text_index])
                if element_text:
                    self.util.text_compare2(self.common, text_from_xml[text_index], element_text, ids[text_index],
                                        self.logger_name)
                loop_index += 2
                text_index += 1
                continue
            if xpath[loop_index]['xpath'] == 'text':
                self.object.element_send_text(self.util.client, xpath[loop_index + 1]['zone'],
                                              xpath[loop_index + 1]['xpath'],
                                              xpath[loop_index + 1]['index'], "NEW",
                                              xpath[loop_index]['comment'], self.logger_name)
                loop_index += 2
                continue
            self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
            text_index += 1
            loop_index += 1

            # self.object.click(self.util.client, xpath[1]['zone'], xpath[1]['xpath'],
            #                           xpath[1]['index'], 1) # this click is required to move to
            #  new screen
            # #self.dev.close_keyboard(self.util.client)
            # self.specific_time("Specific")
            # self.based_on("BasedOn")

    def delete_reminder(self):
        """
         This Method  compare blood sugar and its inner  screen strings .
        It mainly loop through the elements if Xpath in the Object xml is "click" the up next
        object is to be clicked. If Xpath in the Object xml is "text" it sends the text to device
        else it gets the Xpath and calls get_text_compare() and validates screen strings.
        :return:
        """
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "SetReminder", self.my_object)
        for loop_index in range(0, len(xpath)):
            print loop_index
            self.object.click(self.util.client, xpath[loop_index]['zone'],
                              xpath[loop_index]['xpath'],
                              xpath[loop_index]['index'],
                              xpath[loop_index]['comment'],
                              1, self.logger_name)
        text_index = 0
        text_from_xml, ids, eng_list = self.util.get_text_from_xml(self.string_xml, "DeleteReminder", "trans-unit",
                                                  Config.selected_language.strip())
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "DeleteReminder", self.my_object)
        # xpath_days=self.util.read_xpath_list_from_xml(self.object_repo, "Days",self.my_object)
        loop_index = 0
        if self.object.is_element_found(self.util.client,
                                        xpath[1]['zone'],
                                        xpath[1]['xpath'],
                                        xpath[1]['index'],
                                        xpath[1]['comment'],
                                        self.logger_name):
            while loop_index < len(xpath):
                if xpath[loop_index]['xpath'] == 'click':
                    self.object.click(self.util.client, xpath[loop_index + 1]['zone'],
                                      xpath[loop_index + 1]['xpath'],
                                      xpath[loop_index + 1]['index'],
                                      xpath[loop_index + 1]['comment'],
                                      1, self.logger_name)
                    loop_index += 2
                    continue

                if xpath[loop_index]['xpath'] == 'swipe':
                    self.object.element_swipe(self.util.client, xpath[loop_index + 1]['zone'],
                                              xpath[loop_index + 1]['xpath'],
                                              xpath[loop_index + 1]['index'],
                                              xpath[loop_index]['comment'],
                                              "Right", 500, 500, self.logger_name)
                    loop_index += 2
                    continue
                self.get_text_compare(xpath, loop_index, text_from_xml, text_index, ids, eng_list)
                text_index += 1
                loop_index += 1

    def go_home(self):
        """ This method take the system from new reminder to home screen of the App."""
        xpath_go_home = self.util.read_xpath_list_from_xml(self.object_repo, "GoHome",
                                                           self.my_object)
        for loop_index in range(0, len(xpath_go_home)):
            print loop_index
            self.object.click(self.util.client, xpath_go_home[loop_index]['zone'],
                              xpath_go_home[loop_index]['xpath'],
                              xpath_go_home[loop_index]['index'],
                              xpath_go_home[loop_index]['comment'],
                              1, self.logger_name)

    def tearDown(self):
        """ Generates a report of the test case.
        # For more information - https://docs.experitest.com/display/public/
        # SA/Report+Of+Executed+Test"""
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
