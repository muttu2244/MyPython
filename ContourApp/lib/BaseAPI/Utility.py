"""Contour App related APIs"""
import xml.etree.ElementTree as ET
import re
import logging
import ConfigParser
import time
from BaseAPI.ExperitestClient import Client
from BaseAPI import Config


class Utility(object):
    """Utility class for generic methods"""

    def __init__(self):
        """Constructor"""
        # self.logger = logging.getLogger("scriptlevel")
        self.host = None
        self.port = None
        self.client = None

    def set_up(self):
        """Starting a server to connect with device"""
        self.host = "localhost"
        self.port = 8889
        self.client = Client()
        self.client.init(self.host, self.port, True)

    def open_xml(self, file_name):
        """open XML file and return root of file"""
        tree = ET.parse(file_name)
        root = tree.getroot()
        return root

    def open_ini(self, file_name):
        """opens config file and return file pointer"""
        config = ConfigParser.ConfigParser()
        file_pointer = open(file_name)
        config.readfp(file_pointer, file_name)
        return config

    def read_ini(self, config, section, key):
        """get value of key from ini file"""
        return config.get(section, key)

    def get_device_property(self):
        """return device property"""
        pass

    def get_text_from_xml(self, root, element, sub_element="trans-unit", sub_element2="target"):
        """return list of grand child elements under element"""
        sub_element_eng = "english"
        obj_list = list()
        id_list = list()
        eng_list = list()
        for node in root.findall(element):
            for j in node.findall(sub_element):
                obj_list.append(j.find(sub_element2).text.strip())
                # print "Text with string id: ", j.attrib
                id_list.append(j.get("id"))
                # if sub_element2 != "english":
                eng_list.append(j.find(sub_element_eng).text.strip())
        return obj_list, id_list, eng_list

    def read_xpath_list_from_xml(self, root, element, sub_element):
        """returns the list of xpath under element tag"""
        obj_list = list()
        for node in root.findall(element):
            for j in node.findall(sub_element):
                element = dict()
                element['zone'] = j.find('zone').text.strip()
                element['xpath'] = j.find('xpath').text.strip()
                element['index'] = int(j.find('index').text.strip())
                element['comment'] = j.find('comment').text.strip()
                obj_list.append(element)
        return obj_list

    def get_config(self):
        """returns config"""
        pass

    def set_values(self):
        """Sets values"""
        pass

    def timestamp(self):
        """log timestamp"""
        pass

    def log_builder(self):
        """define levels of log"""
        pass

    def reporter(self):
        """Seetest in-built reporter API"""
        pass

    # def text_compare(self, client, common, expected_text, actual_text, logfile):
    def text_compare(self, client, *args):
        """method to compare two text string"""
        common, expected_text, actual_text, string_id, logger_name = args
        logger = logging.getLogger(logger_name)
        # logger.info("String verification: STARTED")
        is_equal = 1
        expected_text_words = expected_text.split()
        actual_text_words = actual_text.split()
        i = 0

        try:
            for i in range(0, max(len(expected_text_words), len(actual_text_words))):
                if expected_text_words[i] != actual_text_words[i]:
                    is_equal = 0
                    break

            if is_equal == 0:
                # logger.error("Actual text from screen: %s != Expected text: %s" % (
                #     actual_text_words[i], expected_text_words[i]))
                # logger.error("RESULT: FAILED")
                Config.results_list.append(string_id)
                Config.results_list.append("Fail")
                logger.error("Actual text from screen: " + actual_text_words[i] + " != " +
                             "Expected text: " +
                             expected_text_words[i])
                logger.error("Result: FAILED")
                # self.logger.error("Expected String %s IS NOT EQUAL TO Actual String %s" % (
                # expected_text_words[i], actual_text_words[i]))
                common.report(client, ' : Failed!!! "' + expected_text_words[i] +
                              '" != "' + actual_text_words[i] + '"', False)
            else:
                # logger.info("Actual text from screen: %s == Expected text: %s" %(actual_text,
                # expected_text))
                # logger.info("RESULT:PASSED")
                Config.results_list.append(string_id)
                Config.results_list.append("Pass")
                logger.info("Actual text from screen: " + actual_text + " == " +
                            "Expected text: " + expected_text)
                logger.info("Result: PASSED")
                # self.logger.info("Expected text %s IS EQUAL TO Actual text %s" % (expected_text,
                # actual_text))
                common.report(client, " : " + '"' + expected_text + '" is Equal to "' +
                              actual_text + '"', True)
        except Exception, msg:
            logger.error("Exception raised: " + str(msg))

    def create_log_file(self, sys_path, script_name, language):
        """creates log file with script name"""
        print "Inside create_log_file"
        path = sys_path + "\\Logs\\"
        print "path=", path
        filename = path + script_name + "_" + language + time.strftime("%b-%d-%Y-%H-%M-%S",
                                                                       time.localtime()) + ".log"
        print "filename=", filename
        try:
            logging.basicConfig(format='%(levelname)s %(message)s', filename=filename,
                                filemode='a', level=logging.INFO)
        except Exception, msg:
            print "Exception raised: ", str(msg)

    def get_app_name(self, device_info_filename, device_name):
        """returns app Name on the basis of OS"""
        tree = ET.parse(device_info_filename)
        root = tree.getroot()
        os_name = ""
        for node in root.findall("device"):
            match = re.match("adb:(.*)", device_name)
            if match:
                if node.get("name") == match.group(1):
                    os_name = node.get("os")

        if os_name == "android":
            app_name = "com.ascensia.contour/.MainActivity"
        else:
            app_name = "com.onyx.r2"  # ios application Name
        return app_name

    def text_compare2(self, common, expected_text, actual_text, string_id, logger_name):
        """method to compare two text string"""
        logger = logging.getLogger(logger_name)
        is_equal = 1
        expected_text.decode('utf-8', 'ignore')
        if actual_text is not None:
            actual_text.decode('utf-8', 'ignore')
        expected_text_words = self.parse_html_tag(expected_text)
        actual_text_words = self.parse_html_tag(actual_text)
        expected_text_words = expected_text_words.split()

        actual_text_words = actual_text_words.split()
        actual_text_words = [x for x in actual_text_words if not x.startswith("\\u")]
        # logger.info("Actual text from screen:" + actual_text + " ----------- " +
        #             "Expected text: " + expected_text)
        try:
            for i in range(0, max(len(expected_text_words), len(actual_text_words))):
                if expected_text_words[i] != actual_text_words[i]:
                    is_equal = 0
                    break

            if is_equal == 0:
                Config.results_list.append(string_id)
                Config.results_list.append("Fail")
                logger.error("Actual text from screen: " + actual_text_words[i] + " != " +
                             "Expected text: " + expected_text_words[i])
                logger.error("Result: FAILED")
                # self.logger.error("Expected String %s IS NOT EQUAL TO Actual String %s" % (
                # expected_text_words[i], actual_text_words[i]))
                common.report(self.client, ' : Failed!!! "' + expected_text_words[i] +
                              '" != "' + actual_text_words[i] + '"', False)
            else:
                Config.results_list.append(string_id)
                Config.results_list.append("Pass")
                logger.info("Actual text from screen: " + actual_text + " == " +
                            "Expected text: " + expected_text)
                logger.info("Result: PASSED")
                # self.logger.info("Expected text %s IS EQUAL TO Actual text %s" % (expected_text,
                # actual_text))
                common.report(self.client, " : " + '"' + expected_text + '" is Equal to "' +
                              actual_text + '"', True)
        except Exception, msg:
            logger.error("Exception raised: " + str(msg))

    def parse_html_tag(self, expected_text_words):
        search_obj = re.search(r'^[0-9][\.]$', expected_text_words[0])
        if search_obj:
            # actualTextWords[0] = re.sub(r'^[0-9].', "", actualTextWords[0])
            expected_text_words.remove(expected_text_words[0])

        # for i in range(0,len(actualTextWords)):
        search_obj = re.search("\\{1,}['][A-Za-z]*[']\\{1,}", expected_text_words)
        if search_obj:
            expected_text_words.strip('\\')
        cleanr = re.compile('<.*?>')
        if cleanr:
            cleaned_text = re.sub(cleanr, '', expected_text_words)
            expected_text_words = cleaned_text

        search_obj = re.search(r'.*\.*', expected_text_words)
        if search_obj:
            expected_text_words = expected_text_words.replace('\\', '')

        search_obj = re.compile(r'^[0-9][\.]\s*')
        if search_obj:
            expected_text_words = re.sub(search_obj, '', expected_text_words)
        return expected_text_words

    def log_project_info(self, device_info_filename, device_name):
        """returns app Name on the basis of OS"""
        logger = logging.getLogger("suitelevel")
        tree = ET.parse(device_info_filename)
        root = tree.getroot()
        os_name = ""
        for node in root.findall("device"):
            match = re.match("adb:(.*)", device_name)
            if match:
                if node.get("name") == match.group(1):
                    os_name = node.get("os")
                    logger.info("OS Type : " + os_name)
            logger.info("Device Catergory : " + node.get("category"))
            logger.info("Model : " + node.get("model"))
            logger.info("Serial Number : " + node.get("serialnumber"))
            logger.info("Android Version : " + node.get("version"))
            logger.info("Application : Contour Diabetes App")
