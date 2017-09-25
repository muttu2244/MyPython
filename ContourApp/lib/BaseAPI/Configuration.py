'''This module used for confuguration '''
import logging
import time
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException


class Configuration(object):
    '''This class used for confuguration '''
    def extract_language_files(self, client, application, directory_path, overwrite=True):
        '''Extract language Files'''
        client.extractLanguageFiles(application, directory_path, overwrite)
        logging.info(
            str(time.asctime(time.localtime())) + " :: Language extracted : " + directory_path)

    def set_default_click_down_time(self):
        '''set_default_click_down_time'''
        pass

    def set_default_timeout(self):
        '''set_default_timeout'''
        pass

    def set_default_web_view(self):
        '''set_default_web_view'''
        pass

    def set_drag_tart_delay(self):
        """ set_drag_tart_delay"""
        pass

    def set_in_key_delay(self):
        """setInKeyDelay"""
        pass

    def set_key_to_key_delay(self):
        """ set_key_to_key_delay"""
        pass

    def set_language(self, client, language):
        """Set the language"""
        client.setLanguage(language)
        logging.info(str(time.asctime(time.localtime())) + "Language set" + language)

    def set_language_properties_file(self):
        """ set_language_properties_file"""
        pass

    def set_show_image_in_report(self, client, value=False):
        """ false will not show report"""
        try:
            client.setShowImageInReport(value)
            logging.info(str(time.asctime(time.localtime())) + " :: Set Show Image In Report ")
        except InternalException, msg:
            logging.error(str(msg) + " :: Unable to Set Show Image In Report")
        except RuntimeException, msg:
            logging.error(str(msg) + " :: Unable to Set Show Image In Report")

    def set_show_pass_image_in_report(self, client, value=False):
        """ setShowPassImageInReport"""
        try:
            client.setShowPassImageInReport(value)
            logging.info("Set Show Pass Image In Report ")
        except InternalException, msg:
            logging.error("Unable to Set Show Pass Image In Report: " + msg)
        except RuntimeException, msg:
            logging.error("Unable to Set Show Pass Image In Report: " + msg)

    def set_show_report(self):
        """ set_show_report"""
        pass

    def set_speed(self):
        """ set_speed"""
        pass

    def set_throw_exception_on_fail(self):
        """set_throw_exception_on_fail """
        pass

    def set_web_auto_scroll(self):
        """" setWebAutoScroll"""
        pass

    def start_steps_group(self):
        """start_steps_group"""
        pass

    def stop_steps_group(self):
        """stop_steps_group"""
        pass

    def text_filter(self):
        """ text_filter"""
        pass

    def start_transaction(self):
        """start_transaction """
        pass

    def end_transaction(self):
        """ end_transaction """
        pass
