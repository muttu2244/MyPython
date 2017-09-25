"""Misc SEETEST wrapped APIs"""
import logging
import time

import re
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException


class Misc(object):
    """Wrapped Misc APIs"""

    def __init__(self):
        """Constructor"""
        pass

    def add_device(self, client, serial_number, device_name):
        """Add the device in Seetest device repos"""
        var = client.addDevice(serial_number, device_name)
        return var

    def close_device(self):
        """Closing device"""
        pass

    def comment(self):
        """Comment"""
        pass

    def exit(self, client):
        """Exit SEETEST Method"""
        client.exit()

    def get_current_application_name(self, client):
        """returns name of a application"""
        app_name = client.getCurrentApplicationName()
        logging.info(str(time.asctime(time.localtime()))
                     + " :: Application name: " + app_name + " Passed")

    def get_devices_information(self, client, sys_path, device_name, logger_name):
        """returning value in xml format"""
        logger = logging.getLogger(logger_name)
        sys_path += '\\DeviceInfo\\'
        match_obj = re.match("(.*):(.*)$", device_name)
        if match_obj:
            device_name = match_obj.group(2)
        else:
            device_name = ""

        file_name = sys_path + device_name + ".xml"
        info = open(file_name, "w")          # open(deviceInfoPath + deviceName + ".xml", "w")
        info.writelines(client.getDevicesInformation())
        info.close()
        # deviceInfoPath
        logger.info("Device information saved at: " + file_name)
        return file_name

    def get_installed_applications(self, client):
        """return list of all installed application"""
        var = ""
        try:
            var = client.getInstalledApplications()
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        return var

    def get_visual_dump(self, client, zone):
        """return visual dump"""
        var = ""
        try:
            var = client.getVisualDump(zone)
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        return var

    def open_device(self, client):
        """open the device"""
        client.openDevice()

    def release_device(self, client, *args):
        """release the device"""
        device_name, release_agent, remove_from_device_list, release_from_cloud = args
        client.releaseDevice(device_name, release_agent,
                             remove_from_device_list, release_from_cloud)
        logging.info(str(time.asctime(time.localtime())) + " " + device_name + " is released!!!")

    def set_device(self, client, device_name, logger_name):
        """set the device"""
        logger = logging.getLogger(logger_name)
        try:
            client.setDevice(device_name)
            logger.info(device_name + " is set")
        except InternalException, msg:
            logger.error(str(msg) + " ---> " + device_name + " is not set")
        except RuntimeException, msg:
            logger.error(str(msg) + " ---> " + device_name + " is not set")

    def sleep(self, client, sec):
        """sleep for given time"""
        client.sleep(sec)


    def start_video_record(self, client):
        """starts video recording"""
        client.startVideoRecord()

    def stop_video_record(self, client):
        """stops video recording"""
        client.stopVideoRecord()

    def wait_for_device(self, client, device, timeout=300000):
        """Waits for device"""
        try:
            value = client.waitForDevice(device, timeout)
            if value:
                logging.info(str(time.asctime(time.localtime()))
                             +" Waited for device" + device + " for " + timeout + " Passed")
            else:
                logging.error(str(time.asctime(time.localtime())) + " Timeout !!!")
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))

    def start_audio_play(self, client, audio_file):
        """start audio play"""
        client.startAudioPlay(audio_file)

    def stop_audio_play(self, client):
        """stop audio play"""
        client.stopAudioPlay()

    def wait_for_audio_play_end(self, client, timeout):
        """Wait for audio to play"""
        client.waitForAudioPlayEnd(timeout)

    def start_audio_recording(self, client, audio_file):
        """Starts audio recording"""
        try:
            client.startAudioRecording(audio_file)
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))


    def stop_audio_recording(self, client):
        """Stops audio recording"""
        try:
            client.stopAudioRecording()
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime()))
                          + " :: " + str(msg))

    def get_picker_values(self, client, *args):
        """pick a value from a element(works only on iOS)"""
        zone, picker_element, index, wheel_index = args
        try:
            value = client.getPickerValues(zone, picker_element, index, wheel_index)
            logging.info(str(time.asctime(time.localtime())) +" Get Picker Value")
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + str(msg))
        return value
