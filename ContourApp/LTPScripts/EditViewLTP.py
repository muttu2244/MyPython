"""
Edit View Script for LTP
"""
import sys
import os
import unittest
import logging
from random import choice

SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
from BaseAPI import Utility, Misc, Application, Objects, Common
from BaseAPI import Device, Navigate, Config, Logger, Configuration


class EditView(unittest.TestCase):
    """
    Class to verify language translations for Contour APP Edit View screens on
    Android devices
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

        if Config.selected_language == "":
            Config.selected_language = "english"
        self.logger_name = os.path.splitext(
            os.path.basename(__file__))[0] + Config.selected_language.strip()
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
        self.misc.set_device(
            self.util.client, self.device_name, self.logger_name)
        self.device_info_path = self.misc.get_devices_information(
            self.util.client, SYS_PATH,
            self.device_name, self.logger_name)
        self.app_name = self.util.get_app_name(self.device_info_path, self.device_name)
        self.app.launch(self.util.client, self.app_name, True, True, self.logger_name)
        print self.device_name
        if self.device_name.find("iPhone") > 0:
            # self.client.waitForDevice("@os='ios'",10000)
            self.app.launch(self.util.client, "com.onyx.-", True, False, self.logger_name)
            self.my_object = "Iobject"
        else:
            self.my_object = "Aobject"
            self.app_name = self.util.get_app_name(self.device_info_path, self.device_name)
            self.app.launch(self.util.client, self.app_name, True, False, self.logger_name)
        print self.my_object
        self.common.set_project_base_directory(self.util.client, os.getcwd(), self.logger_name)
        self.common.set_reporter(self.util.client, SYS_PATH,
                                 os.path.splitext(os.path.basename(__file__))[0], self.logger_name)
        Config.results_list = []
        # self.config.set_show_pass_image_in_report(self.util.client, False)

    def new_entry(self):
        """Method to enter a New Entry"""
        xpath = self.util.read_xpath_list_from_xml(self.object_repo, "new_entry", self.my_object)
        i = 0
        # Adding new Entry
        # Clicking on + sign on main screen
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        if self.my_object == "Aobject":
            # Manual Entries Pop up
            if self.object.is_element_found(
                    self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                    xpath[i]['index'], xpath[i]['comment'], self.logger_name):
                # Start: Block
                # Click on OK Button
                self.object.click(
                    self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                    xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
                # End: Block
        i += 2
        self.misc.sleep(self.util.client, 1000)
        # Swiping only minutes to set time with last 15 minutes
        for ctr in range(0, 3):
            # Start: Loop
            # Swiping minutes
            self.object.element_swipe(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], "Up", 100, 2000, self.logger_name)
            print "Loop Counter: ", ctr
            # End: Loop
        i += 1
        # Clicking "Done" on time select
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Clicking "Reading" on Edit Entry
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        number = choice(range(100, 200))
        self.dev.send_text(self.util.client, str(number), self.logger_name)
        # Closing Keyboard
        self.dev.close_keyboard(self.util.client)
        self.misc.sleep(self.util.client, 4000)
        # Clicking on "After Meal"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Clicking on "Before Meal"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Clicking "Save" on "Meal Marker"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        self.misc.sleep(self.util.client, 1000)
        # Automatic Meal marker
        if self.object.is_element_found(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], self.logger_name):
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 2
        # Click on "Done" on Edit Entry
        self.misc.sleep(self.util.client, 2000)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click "OK" on "Confirm Your Manual Entry"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        self.misc.sleep(self.util.client, 2000)
        self.app.application_close(self.util.client, self.app_name)
        self.app.launch(self.util.client, self.app_name, True, True, self.logger_name)

    def verify_reminder(self):
        """Verifying Reminders"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "reminder", self.my_object)
        i = 0
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "reminder", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        self.misc.sleep(self.util.client, 500)
        # Starting Reminder for cancel
        if self.object.element_get_property(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], "hidden", self.logger_name) == "false":
            i += 1
            # Clicking on "1hr"
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            i += 1
            # Closing Reminder
            # Click on Cross button
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            i += 1
            self.misc.sleep(self.util.client, 1000)
            # (56.0)Text: "Delete this reminder?"
            actual_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                           xpath[i]['xpath'],
                                                           xpath[i]['index'], "text",
                                                           self.logger_name)
            i += 1
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
            text_index += 1
            # Clicking on OK Button
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            i += 1
            # ----------------------------------------------------
            # Starting reminder for 15 min
            # Click on "15 min"
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            i += 1
            self.common.report(self.util.client, "15 min reminder started!!!", True)
            print "15 min reminder started!!!"
            # Wait FOR 15 MIN pop up to occur
            # Reminder complete Pop up
            self.object.wait_for_element(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 960000, self.logger_name)
            i += 1
            # Click on snooze button
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            i += 1
            # -----------------Start:Remind me again in 15 min ------------------
            # (66.0)Text: "Remind me again in 15 min"
            actual_text = self.object.element_get_property(self.util.client, xpath[i]['zone'],
                                                           xpath[i]['xpath'],
                                                           xpath[i]['index'], "text",
                                                           self.logger_name)
            i += 1
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
            # Click on ok button
            self.object.wait_for_element(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            # -----------------End:Remind me again in 15 min ------------------

    def verify_activity(self):
        """Verifying Activity"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "activity", self.my_object)
        i = 0
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "activity", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        # Click on Activity button
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
        self.misc.sleep(self.util.client, 1000)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on Add/edit activity button
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 10000, self.logger_name)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Verify number of element present in list if any
        element_count = self.object.get_element_count(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'])
        i += 1
        # Run below if count is more than 0
        if element_count > 0:
            # Loop on number of element to delete
            for i in range(0, element_count):
                self.object.element_swipe(
                    self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
                    xpath[i]['comment'], "Right", 400, 2000, self.logger_name)
                # Click on Delete button
                self.object.click(
                    self.util.client, xpath[i+1]['zone'], xpath[i+1]['xpath'],
                    xpath[i+1]['index'], xpath[i+1]['comment'], 1, self.logger_name)
            # end for
        # end if
        i += 2
        # (14.0)Text: "You have not logged any activities yet."
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        # Click on "Cancel" button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)

    def verify_meal(self):
        """Verifying Meal"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "meal", self.my_object)
        i = 0
        # reading expected text from xml language
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "meal", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        # Click on "Meal" Button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on Carb "0 g"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Swiping down
        self.object.element_swipe(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
            xpath[i]['comment'], "Down", 200, 2000, self.logger_name)
        i += 1
        # Click on "Done" button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (29.0)Text: "Food/Amount"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on "Add/edit food"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (79.0) Unable to Verify
        # (80.0) Unable to Verify
        # Entering the new food item
        # Sending text to Add Food
        self.object.element_send_text(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
            "Egg Sandwhich", xpath[i]['comment'], self.logger_name)
        i += 1
        # Clicking on Food entry
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (33.0)Text: "Enter the carbs for this meal to set the app
        # to autopopulate the carb amunt for this meal in the future"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Clicking on cancel button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Clicking on first item in food
        if self.object.is_element_found(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], self.logger_name):
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
            # Click on "Edit carbs"
            self.object.click(
                self.util.client, xpath[i+1]['zone'], xpath[i+1]['xpath'],
                xpath[i+1]['index'], xpath[i+1]['comment'], 1, self.logger_name)
            # (37.0)Text: "Edit the carb amount to change future entries;
            #  this change does not affect your previous entries."
            # i+2
            actual_text = self.object.element_get_property(
                self.util.client, xpath[i+2]['zone'], xpath[i+2]['xpath'],
                xpath[i+2]['index'], "text", self.logger_name)
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
        text_index += 1
        i += 3
        # Verify number of element present in list if any
        element_count = self.object.get_element_count(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'])
        i += 1
        # Run below if count is more than 0
        if element_count > 0:
            # Loop on number of element to delete
            for ctr in range(0, element_count):
                print ctr
                # Swiping right
                self.object.element_swipe(
                    self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
                    xpath[i]['comment'], "Right", 0, 2000, self.logger_name)
                # Click on Delete button
                self.object.click(
                    self.util.client, xpath[i+1]['zone'], xpath[i+1]['xpath'],
                    xpath[i+1]['index'], xpath[i+1]['comment'], 1, self.logger_name)
            # end for
        # end if
        i += 2
        # (30.1)Text: "You have not logged any foods yet."
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on "Cancel" button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)

    def verify_meds(self):
        """Verifying Meds"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "meds", self.my_object)
        i = 0
        # reading expected text from xml language
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "meds", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        # Click on medication
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on Add/edit medication
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Verify number of element present in list if any
        element_count = self.object.get_element_count(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'])
        i += 1
        # Run below if count is more than 0
        if element_count == 0:
            # (45.1)Text: "You have not logged any medications yet."
            actual_text = self.object.element_get_property(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], "text", self.logger_name)
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
        text_index += 1
        i += 1
        # Sending text to search bar
        self.object.element_send_text(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
            "Byetta", xpath[i]['comment'], self.logger_name)
        i += 1
        # Click on Byetta
        if self.my_object == "Iobject":
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        # Double click for iOS
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        self.misc.sleep(self.util.client, 2000)
        if self.my_object == "Iobject":
            # Clicking if OS is iOS
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        else:
            # Swiping to set a value
            self.object.element_swipe(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'], xpath[i]['index'],
                xpath[i]['comment'], "Down", 100, 2000, self.logger_name)
        # Click on "Done" button
        i += 1
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on "Done" button on "Add Medication"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (49.0)Text: "Byetta"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Clicking on "Cancel" button on "Edit Entry"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (68.0)Text: "Are you sure you want to discard your changes?"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # (68.0)Text: "Discard Changes"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on "Discard" on "Discard Changes"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)

    def verify_photo(self):
        """Verifying photo"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "photo", self.my_object)
        i = 0
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "photo", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        # Revoking application permission for camera
        # (81.0) Unable to verify "Unable to Access Camera"
        # Click on Photo button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Verify that pic is present or not
        # Start if
        if self.object.is_element_found(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], self.logger_name):
            # Click on cross button
            self.object.wait_for_element(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # end if
        # (7.0)Text: "Take a Photo"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # (7.0)Text: "Add Photo from Library"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on Take a Photo
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
        # Attention:
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on Center button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        self.misc.sleep(self.util.client, 4000)
        # (8.0)Text: "Retake"
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on Use photo
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on cross button
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (60.1)Text: "Delete Photo"
        # Compare Actual & Expected
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # (60.1)Text: "Are you Sure you want to delete this photo?"
        # Compare Actual & Expected
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        text_index += 1
        # Click on OK button on Delete Photo pop up
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        # i += 1
        # i += 1
        # i += 1
        # (69.0) Unable to Verify Photo Error
        # (7.2) Unable to Verify "The Contour App would like permissioen to access photos."

    def verify_automatic_meal_popup(self):
        """Verifying automatic meal pop up"""
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "automatic_meal", self.my_object)
        i = 0
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "automatic_meal_popup", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        # Do you want automatic meal marker prompting to continue?
        if self.object.is_element_found(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], self.logger_name):
            # Start: Block
            # (62.0)Text: "Do you want automatic meal marker prompting to continue?"
            actual_text = self.object.element_get_property(
                self.util.client, xpath[i+1]['zone'], xpath[i+1]['xpath'],
                xpath[i+1]['index'], "text", self.logger_name)
            # Compare Actual & expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
            text_index += 1
            # (62.0)Text: "Yes, continue"
            actual_text = self.object.element_get_property(
                self.util.client, xpath[i+2]['zone'], xpath[i+2]['xpath'],
                xpath[i+2]['index'], "text", self.logger_name)
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
            text_index += 1
            # (62.0)Text: "No, stop prompting"
            actual_text = self.object.element_get_property(
                self.util.client, xpath[i+3]['zone'], xpath[i+3]['xpath'],
                xpath[i+3]['index'], "text", self.logger_name)
            # Compare Actual & Expected
            self.logger.info("Testing StringID == " + str(ids[text_index]))
            self.logger.info("English Text == " + eng_list[text_index])
            self.util.text_compare2(
                self.common, expected_text[text_index],
                actual_text, ids[text_index], self.logger_name)
            # Clicking on "Yes, continue"
            self.object.click(
                self.util.client, xpath[i+4]['zone'], xpath[i+4]['xpath'],
                xpath[i+4]['index'], xpath[i+4]['comment'], 1, self.logger_name)
            # End: Block

    def test_edit_view_ltp(self):
        """Main test method"""
        expected_text, ids, eng_list = self.util.get_text_from_xml(
            self.string_xml, "main", "trans-unit",
            Config.selected_language.strip())
        text_index = 0
        xpath = self.util.read_xpath_list_from_xml(
            self.object_repo, "main", self.my_object)
        i = 0
        # Creating new Entry for reminder
        self.new_entry()
        self.misc.sleep(self.util.client, 2000)
        # Click on reading in List view
        if self.my_object == "Iobject":
            ind = self.object.get_element_count(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'])
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                ind - 1, xpath[i]['comment'], 1, self.logger_name)
        else:
            self.object.wait_for_element(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Start: Reminder
        self.verify_reminder()
        # Clicking on reading
        self.object.wait_for_element(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 30000, self.logger_name)
        # Attention: No inc
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on reading value
        self.dev.close_keyboard(self.util.client)
        # Required for Reminder purpose
        # Clicking on "After Meal"
        self.misc.sleep(self.util.client, 1000)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Clicking on "Before Meal"
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # No Mark
        self.misc.sleep(self.util.client, 2000)
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # (61.0)Text: "By Selecting No Mark, no Meal Markers or Meals will be saved."
        actual_text = self.object.element_get_property(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], "text", self.logger_name)
        i += 1
        # Compare Actual & Expected
        self.logger.info("Testing StringID == " + str(ids[text_index]))
        self.logger.info("English Text == " + eng_list[text_index])
        self.util.text_compare2(
            self.common, expected_text[text_index],
            actual_text, ids[text_index], self.logger_name)
        # Click on "OK" button
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Click on Save Button
        self.dev.close_keyboard(self.util.client)
        if self.object.is_element_found(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], self.logger_name):
            self.object.click(
                self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
                xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        i += 1
        # Verify pop up
        self.verify_automatic_meal_popup()
        self.misc.sleep(self.util.client, 2000)
        # Clicking on Meal
        self.object.click(
            self.util.client, xpath[i]['zone'], xpath[i]['xpath'],
            xpath[i]['index'], xpath[i]['comment'], 1, self.logger_name)
        # Start: Photo
        self.verify_photo()
        # Start: Activity
        self.verify_activity()
        # Start: Meal
        self.verify_meal()
        # Start: Medication
        self.verify_meds()

    def tearDown(self):
        # Close Application
        self.app.application_close(self.util.client, self.app_name)
        # Generates a report of the test case.
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
