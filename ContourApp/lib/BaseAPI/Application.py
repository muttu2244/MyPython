"""This module used for application specific """
import logging
import time
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException


class Application(object):
    """This class used for application specific """

    def __init__(self):
        pass

    def install(self, client, app_path, instrument, keep_data):
        """Install the application in the given path on the devic """
        try:
            client.install2(app_path, instrument, keep_data)
            logging.info(str(time.asctime(time.localtime())) + " Application Installed !!!")

        except InternalException, msg:
            logging.error(
                str(time.asctime(time.localtime())) + " :: " + str(msg) +
                " Unable to install application")
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) +
                          "Unable to install application")

    def launch(self, *args):
        """Launch activity"""
        client, activity, instrument, stopif_running, logger_name = args
        logger = logging.getLogger(logger_name)
        try:
            client.launch(activity, instrument, stopif_running)
            # logging.info(str(time.asctime(time.localtime())) + " Application launched !!!")
            logger.info("Application launched")
        except InternalException, msg:
            # logging.error(str(
            #     time.asctime(time.localtime())) + " :: " + str(msg) + " Unable to launch
            # application")
            logger.error("Unable to launch the application: " + str(msg))
        except RuntimeException, msg:
            # logging.error(
            #     str(time.asctime(time.localtime())) + " :: " + str(msg) +
            #     "Unable to launch application")
            logger.error("Unable to launch the application: " + str(msg))

    def application_clear_data(self, client, app):
        """Clear application data"""
        try:
            client.applicationClearData(app)
            logging.info(str(
                time.asctime(time.localtime())) + " Application " + app +
                         " data is cleared !!!")
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) +
                          " Unable to clear")
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) +
                          "Unable to clear")

    def application_close(self, client, app):
        """Close application"""
        try:
            client.applicationClose(app)
            logging.info(str(time.asctime(time.localtime())) + " :: Application closed")

        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) +
                          "List Select-Failed")
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) +
                          " :: Unable to close application " + app)

    def uninstall(self, client, app):
        '''Uninstall(app)'''
        pass
