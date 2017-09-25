"Module containing wrapped common SEETEST method"
import time
import logging
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException


class Common(object):
    """Common APIs wrapper class"""

    def __init__(self):
        """Constructor"""
        # self.logger = logging.getLogger("scriptlevel")
        pass

    def capture(self, client, sys_path, line, file_name):
        """Return image path"""
        save_path = sys_path + "\\Images\\" + file_name + ".png"
        run_path = client.captureLine(line)
        src = open(run_path, "rb")
        des = open(save_path, "wb")
        des.writelines(src.readlines())
        logging.info(str(time.asctime(time.localtime())) + " " + save_path + " Image Saved !!!")
        # self.logger.info("Captured image saved at %s" % save_path)
        return save_path

    def capture_element(self, client, *args):
        """return runtime element object that can be used for selecting the element"""
        name, x_cord, y_cord, width, height, similarity = args
        element = client.captureElement(name, x_cord, y_cord, width, height, similarity)
        logging.info(str(time.asctime(time.localtime())) + " :: Captured Element " + name)
        # self.logger.info("Captured Element is " % name)
        return element

    def element_get_text(self, client, *args):
        """return text of element"""
        zone, element, comment, logger_name, index = args
        logger = logging.getLogger(logger_name)
        text = ""
        try:
            logger.info("Get Text from element: " + comment)
            text = client.elementGetText(zone, element, index)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; " + str(msg))
        return text

    def generate_report(self, client, value=False):
        """Generate's Report"""
        client.generateReport2(value)
        logging.info(str(time.asctime(time.localtime())) + " :: Generating report: " + str(value))
        # self.logger.info("Generating report: %s" % str(value))

    def get_last_command_result_map(self, client):
        """returns the status of last executed command"""
        value = client.getLastCommandResultMap()
        logging.info(str(time.asctime(time.localtime())) + " Last Commands result:  " + str(value))
        # self.logger.info("Result for the last executed command: %s" % str(value))
        return value

    def list_select(self, client, *args):
        """Select element from a list"""
        send_reset, send_navigation, delay, text, color, rounds, send_on_find = args
        try:
            client.listSelect(send_reset, send_navigation, delay, text, color, rounds, send_on_find)
            logging.info(str(time.asctime(time.localtime())) + "List Select-->Passed")
            # self.logger.info("List select --> PASSED")

        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + "List "
                                                                                    "Select-Failed")
            # self.logger.error("An Internal exception raised : %s. List select - FAILED")

        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + "List "
                                                                                    "Select-Failed")
            # self.logger.error("An Internal exception raised : %s. List select - FAILED")

    def press_while_not_found(self, client, zone, element_to_click, element_to_click_index, *args):
        """Press till didn't found a element"""
        element_to_find, element_to_find_index, timeout, delay = args
        result = client.pressWhileNotFound2(zone, element_to_click, element_to_click_index,
                                            element_to_find, element_to_find_index, timeout, delay)
        logging.info(str(time.asctime(time.localtime())) + " :: Press While " +
                     element_to_click + " is not found")
        # self.logger.info("Press while not found : %s "
        # "is not found")
        return result

    def set_show_report(self, client, show_report):
        """Set to show report"""
        result = client.setShowReport(show_report)
        logging.info(str(time.asctime(time.localtime())) + " :: Show Report Set !!!")
        # self.logger.info("Show Report set !!")
        return result

    def set_project_base_directory(self, client, directory, logger_name):
        """Sets project base directory"""
        logger = logging.getLogger(logger_name)
        client.setProjectBaseDirectory(directory)
        logger.info("Project Base Directory set for reporting")  # creating logs
        # logger.info("Project base directory set !!")

    def swipe_while_not_found(self, client, direction, offset, swipe_time, *args):
        """Swipe till didn't find a element"""
        zone, element_to_find, element_to_find_index, delay, rounds, click = args
        result = client.swipeWhileNotFound2(direction, offset, swipe_time, zone, element_to_find,
                                            element_to_find_index, delay, rounds, click)
        logging.info(str(time.asctime(time.localtime())) + " :: Swipe While Not Found")
        # self.logger.info("Swipe the element %s until found with timeout %s" %(element_to_find,
        # delay))
        return result

    def release_client(self, client):
        """Release the client"""
        # logger = logging.getLogger("suitelevel")
        client.releaseClient()
        logging.info(str(time.asctime(time.localtime())) + " :: " + " Client released ")
        # logger.info("Client is released")

    # def set_reporter(self, client, sys_path, script_name, logfile):
    def set_reporter(self, client, sys_path, script_name, logger_name):
        """Sets reporting format"""
        logger = logging.getLogger(logger_name)
        try:
            client.setReporter2("xml", sys_path + "\\Reports\\", script_name)
            # logger.info("Reporter for script: SET")
            logger.info("Reporter for script: SET")
            logger.info("Report available at: "+ sys_path + "\\Reports\\" + script_name)
        except InternalException, msg:
            # logger.error("Set Reporter: FAILED - %s" % msg)
            logger.info("Set Reporter: FAILED " + msg)
            logger.info("Report available at: "+ sys_path + "\\Reports\\" + script_name)
        except RuntimeException, msg:
            # logger.error("Set Reporter: FAILED - %s" % msg)
            logger.info("Set Reporter: FAILED " + msg)
            logger.info("Report available at: "+ sys_path + "\\Reports\\" + script_name)

    def report(self, client, remark, status, path_to_image=""):
        """Add path To Image and remark in report"""
        if path_to_image == "":
            client.report(remark, status)
            logging.info(str(time.asctime(time.localtime())) + " " + remark + " is added in report")
            # self.logger.info("%s added in report" % remark)
        else:
            client.report(path_to_image, remark, status)
            logging.info(str(time.asctime(time.localtime())) + " Image saved at "
                         + path_to_image + remark + " is added in report")
            # self.logger.info("Image saved at %s. %s is added in report" % (path_to_image, remark))
