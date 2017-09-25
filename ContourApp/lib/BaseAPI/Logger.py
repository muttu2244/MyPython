"""Module for logging"""
import os
import datetime
import logging

class Logger(object):
    """
    Class to generate the logs
    """
    def __init__(self, logger_name):
        """
        Constructor
        :param logger_name: Logger name reference
        """
        if not os.path.exists("..\\Logs"):
            os.makedirs("..\\Logs")
        if logger_name == "suitelevel":
            now = datetime.datetime.now()
            datetime_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            logfilename = "..\\Logs\\ltptest_" + datetime_string + ".log"
        elif logger_name == "scriptlevel":
            now = datetime.datetime.now()
            datetime_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            logfilename = "..\\Logs\\script_" + datetime_string + ".log"
        else:
            now = datetime.datetime.now()
            datetime_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            logfilename = "..\\Logs\\"+ logger_name + datetime_string + ".log"

        self.setup_logger(logger_name, logfilename, logging.DEBUG)
        self.logger = logging.getLogger(logger_name)

    def setup_logger(self, logger_name, log_file, level=logging.INFO):
        """
        Method to set the logger up with specified data
        :param logger_name: Logger name
        :param log_file: Log file name
        :param level: Logging level
        :return: None
        """
        log = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(formatter)
        log.addHandler(self.stream_handler)
        log.setLevel(level)

    def close_file(self):
        """ Close the logs"""
        if self.logger.propagate:
            self.logger.propagate = False
