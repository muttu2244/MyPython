"""Module to interact with Seetest object API's"""
import logging
import time
from BaseAPI import Utility
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException
# pylint: disable=R0201

class Objects(object):
    """Wrapper class to interact with Seetest Object methods"""

    def __init__(self):
        self.util = Utility()

    def click(self, client, *args):
        """Click on an element"""
        # zone, element, index, comment, click_count, logfile = args
        zone, element, index, comment, click_count, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            logger.info("CLICK " + comment)
            client.click(zone, element, index, click_count)
            logger.info("RESULT: PASSED")
            # logger.info("Clicked the element: %s" % comment)
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)

    def click_coordinate(self, client, *args):
        """Click in window X,Y coordinates"""
        x_coordinate, y_coordinate, click_count = args
        try:
            client.clickCoordinate(x_coordinate, y_coordinate, click_count)
            logging.info(str(
                time.asctime(
                    time.localtime())) + "Clicked on Coordinates X: " + x_coordinate + " Y: "
                         + y_coordinate + " ---> " + "Passed !!!")
        except Exception, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " +
                str(msg) + " not Click Co-ordinates---->Failed")

    def element_get_property(self, client, *args):
        """Get element property"""
        zone, element, index, properties, logger_name = args
        value = ""
        logger = logging.getLogger(logger_name)
        try:
            value = client.elementGetProperty(zone, element, index, properties)
            logger.info("Got " + properties + " from screen " + " : " +
                value)
            return value
        except Exception, msg:
            logger.error("Unable to get "+ properties + str(msg) + " ")

    def element_send_text(self, client, *args):
        """Send text to an element"""
        zone, element, index, text = args
        try:
            client.elementSendText(zone, element, index, text)
            logging.info(
                str(time.asctime(time.localtime())) + element + " :: Element Send Text --> Passed")
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + " Element Send Text --> Failed")

    def element_swipe(self, client, *args):
        """Swipe the screen in a given direction"""
        zone, element, index, comment, direction, offset, timeout, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Swipe: " + comment)
            client.elementSwipe(zone, element, index, direction, offset, timeout)
            logger.info("RESULT: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)

    def swipe_while_not_found(self, client, *args):
        """Swipe to search for an element or text"""
        direction, offset, swipe_time, zone, element_to_find, \
        element_to_find_index, comment, delay, rounds, click, logger_name = args
        value = ""
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Swipe "+ comment + " until found")
            value = client.swipeWhileNotFound2(direction, offset, swipe_time, zone,
                                               element_to_find,
                                               element_to_find_index,
                                               delay, rounds, click)
            logger.info("RESULT: PASSED")

            return value
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)

    def verify_in(self, client, *args):
        """Search for an element and verify element related to it exist.
        The direction can be UP, DOWN, LEFT and RIGHT."""
        zone, search_element, index, direction, element_find_zone, \
        element_to_find, width, height = args

        try:
            client.verifyIn(zone, search_element, index, direction, element_find_zone,
                            element_to_find,
                            width, height)
            return True, ""
        except Exception, msg:
            return False, msg

    def wait_for_element(self, client, *args):
        """Wait for an element to appear in a specified zone"""
        zone, element, index, comment, timeout, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Wait for: " + comment)
            client.waitForElement(zone, element, index, timeout)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
            # logger.error("Clicking the element: %s failed" % comment)

    def hybrid_clear_cache(self, client, clear_cookies, clear_cache):
        """To Clear browser cookies and/or cache"""
        try:
            client.hybridClearCache(clear_cookies, clear_cache)
            return True, ""
        except Exception, msg:
            return False, msg

    def press_while_not_found(self, client, *args):
        """Press on a certain element (ElementToClick) while another element (ElementToFind)is not
        found"""
        zone, element_to_click, element_to_click_index, element_to_find,\
        element_to_find_index, timeout, delay = args
        try:
            client.pressWhileNotFound2(zone, element_to_click, element_to_click_index,
                                       element_to_find,
                                       element_to_find_index,
                                       timeout, delay)
            logging.info(str(time.asctime(time.localtime())) + "Pressed While Not Found!!-->Passed")
        except Exception, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " + str(
                    msg) + "Not Pressed While Not Found---->Failed")

    def set_show_report(self, client, show_report):
        """"when set to False will not show reports steps"""
        try:
            client.setShowReport(show_report)
            logging.info(str(time.asctime(time.localtime())) + " :: Show Report Set !!!")
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + " Show Report can not set !!!")

    def element_swipe_while_not_found(self, client, *args):
        """Swipe to search for an element or text"""
        zone, search_element, direction, offset,swipe_time, element_find_zone, \
        element_to_find, element_to_find_index, delay, rounds, click = args
        try:
            client.elementSwipeWhileNotFound(zone, search_element, direction, offset,
                                             swipe_time,
                                             element_find_zone,
                                             element_to_find, element_to_find_index,
                                             delay, rounds,
                                             click)
            logging.info(
                str(time.asctime(time.localtime())) + " :: elementSwipeWhileNotFound!!-->Passed")
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + "Element swipe not done while not found---->Failed")

    def get_text_in(self, client, *args):
        """Get a text in a specified area indicate by an element,	direction, width and height.
        The direction can be UP, DOWN, LEFT and RIGHT."""
        zone, element, index, text_zone, direction, width, height = args
        value = ""
        try:
            value = client.getTextIn2(zone, element, index, text_zone, direction, width,
                                      height)  # want to return text
            logging.info(str(time.asctime(time.localtime())) + element + "getTextIn-->Passed")
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg))
            return value

    def verify_element_found(self, client, zone, element, index):
        """To Verify an element is found"""
        try:
            client.verifyElementFound(zone, element, index)
            logging.info(str(time.asctime(time.localtime())) + "verifyElementFound-->Passed")
            return True
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + "Element Not Found-->Failed")
            return False

    def verify_element_not_found(self, client, zone, element, index):
        """To Verify an element is not found"""
        try:
            client.verifyElementNotFound(zone, element, index)
            logging.info(str(time.asctime(time.localtime())) + "verifyElementNotFound-->Passed")
        except Exception, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " + str(msg) + "Element Found-->Failed")

    def click_in(self, client, *args):
        """Search for an element and click on an element near him.
        The direction can be UP, DOWN, LEFT and RIGHT"""
        pass

    def click_offset(self, client, zone, element, index):
        """"Click an element with an offset, This may have been deprecated in the current
        SeeTest Version"""
        try:
            client.clickOffset(zone, element, index)
            logging.info(str(time.asctime(time.localtime())) + "Clicked --> Passed")
        except Exception, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " + str(msg) + "Unable to click")

    def element_get_table_rows_count(self, client, *args):
        """Get table total or visible rows count"""
        pass

    def element_list_visible(self, client, *args):
        """Make the target element visible"""
        pass

    def element_scroll_to_table_row(self, client, *args):
        "Scroll table / list to the given row"
        pass

    def element_set_property(self, client, *args):
        """Set element property"""
        pass

    def flick_coordinate(self, client, x_coordinate, y_coordinate, direction):
        """Flick from a given point in a given direction"""
        pass

    def flick_element(self, client, *args):
        """"Flick the element in a given direction"""
        zone, element, index, comment, direction, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Flick the element: " + comment)
            client.flickElement(zone, element, index, direction)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))

    def get_element_count_in(self, client, *args):
        """Search for an element and count the number of times an element is found near him.
        The direction can be UP, DOWN, LEFT and RIGHT."""
        pass

    def is_element_blank(self, client, *args):
        """Check if a given element found in the specified zone is blank;
        if blank returns TRUE if not found returns FALSE"""
        pass

    def is_found_in(self, client, *args):
        """Search for an element and check if an element related to it exist.
        The direction can be UP, DOWN, LEFT and RIGHT."""
        pass

    def long_click(self, client, *args):
        """Long click on or near to an element (the proximity to the element
        is specified by a X-Y offset)"""
        pass

    def run_native_api_call(self, client, *args):
        """Run native API call on the given element."""
        pass

    def send_while_not_found(self, client, *args):
        """Send a given text while an element is not found"""
        pass

    def wait_for_element_to_vanish(self, client, *args):
        """"Wait for an element to vanish"""
        zone, element, index, comment, timeout, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            print "inside try"
            logger.info("Waiting for "+ comment + " to vanish from screen")
            client.waitForElementToVanish(zone, element, index, timeout)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))

    def get_coordinate_color(self, client, x_coordinate, y_coordinate):
        """Returns an integer representation in the RGB color model for coordinate (x,y)"""
        pass

    def drag_drop(self, client, *args):
        """Drag an element in a specified zone and drop it at a second element"""
        pass

    def force_touch(self, client, *args):
        """Force touch on element and drag for distance."""
        pass

    def touch_down(self, client, zone, element, index, comment, logger_name):
        """Touch down on element"""
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Touch Down the element: " + comment)
            client.touchDown(zone, element, index)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))

    def touch_move(self, client, zone, element, index):
        """TouchMove to element."""
        pass

    def touch_up(self, client, logger_name):
        """Touch Up from last coordinate touched down or moved to."""
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Touch Up")
            client.touchUp()
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))

    def touch_down_coordinate(self, client, x_coordinate, y_coordinate):
        """Touch down at X,Y coordinates"""
        pass

    def touch_move_coordinate(self, client, x_coordinate, y_coordinate):
        """TouchMove to X,Y coordinates"""
        pass

    def get_text(self, client, zone):
        """Get the text from screen"""
        value = ""
        try:
            value = client.getText(zone)  # want to return
            logging.info(str(time.asctime(time.localtime())) + "getText-->Passed")
        except Exception, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " + str(msg) + "getText--->Failed")
        return value

    def drag(self, client, *args):
        """Drag an element in a specified zone."""
        zone, element, index, comment, x_offset, y_offset, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Drag: " + comment)
            client.drag(zone, element, index, x_offset, y_offset)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))

    def element_list_pick(self, client, list_zone_name, list_locator, element_zone_name,
                          element_locator, index=0,
                          click=True):
        """Select an element from the Object Repository in a list"""
        try:
            client.elementListPick(list_zone_name, list_locator, element_zone_name,
                                   element_locator,
                                   index, click)
            logging.info(str(time.asctime(time.localtime())) + "Element List Pick-->Passed")
        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + "Element List Pick-->Failed")

    def is_element_found(self, client, zone, element, index, comment, logger_name):
        """Check if a given element or text is found in the specified zone"""
        value = ""
        logger = logging.getLogger(logger_name)
        try:
            value = client.isElementFound(zone, element, index)
            # logger.info("FOUND: " + comment)

        except Exception, msg:
            logger.info("Exception in is_element_found; " + str(msg))
        if value:
            logger.info("FOUND: " + comment)
        else:
            logger.info("NOT FOUND: " + comment)
        return value

    def get_element_count(self, client, zone, element):
        """Count the number of times an element or text is found"""
        value = ""
        try:
            value = client.getElementCount(zone, element)
            logging.info(str(
                time.asctime(time.localtime())) + element + " count is: " + value + "--> Passed")

        except Exception, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(
                msg) + "Element not found --> Failed")

        return value
