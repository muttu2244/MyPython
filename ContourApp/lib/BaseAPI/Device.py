"Wrapped SeeTest Device APIs"
import logging
import time
from BaseAPI.ExperitestClient import RuntimeException
from BaseAPI.ExperitestClient import InternalException
# pylint: disable=R0201

class Device(object):
    """Wrapped Device APIs"""

    def __init__(self):
        #self.logger = logging.getLogger("scriptlevel")
        pass

    def clear_device_log(self, client):
        """clear device logs and return True or False"""
        try:
            client.clearDeviceLog()
            logging.info(str(time.asctime(time.localtime())) + " :: Device Logs Cleared - "
                                                               "Passed!!!")
            #self.logger.info("Device logs cleared - PASSED")
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + " - Failed!!!")
            #self.logger.error("Clear device logs raised exception: %s" % str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + " - Failed!!!")
            #self.logger.error("Clear device logs raised exception: %s" % str(msg))

    def get_connected_devices(self, client):
        """return list of connected devices"""
        device_list = client.getConnectedDevices()
        # to get List split('\n')
        return device_list

    def get_device_log(self, client):
        """return path of xml file"""
        file_path = client.getDeviceLog()
        logging.info(str(time.asctime(time.localtime())) + " Device Logs collected !! " + file_path)
        #self.logger.info("Device logs collected at %s" % file_path)
        return file_path

    def get_text(self, client, zone="NATIVE"):
        """return list of text present on screen"""
        value = ""
        try:
            value = client.getText(zone)			#want to return
            logging.info(str(time.asctime(time.localtime())) +"getText-->Passed")
            #self.logger.info("Text got = %s" % value)
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + "::" + str(msg) + "get Text-Failed")
            #self.logger.error("Get text method raised exception: %s" % str(msg))
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + "::" + str(msg) + "get Text-Failed")
            #self.logger.error("Get text method raised exception: %s" % str(msg))
        return value

    def send_text(self, client, text, logger_name):
        """send text to device"""
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Send Text: " + text)
            client.sendText(text)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))

    def swipe(self, client, direction, offset, sec=500):
        """perform swipe parameters direction and offset"""
        try:
            client.swipe2(direction, offset, sec)
            logging.info(str(time.asctime(time.localtime())) +"swiping" + " swipe-->Passed ")
        except InternalException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + "swipe-Failed")
        except RuntimeException, msg:
            logging.error(str(time.asctime(time.localtime())) + " :: " + str(msg) + "swipe-Failed")

    def get_device_property(self, client, prop):
        """return value of property of device"""
        value = client.getDeviceProperty(prop)
        return value

    def clear_location(self, client):
        """clears location"""
        client.clearLocation()
        return True

    def close_keyboard(self, client):
        """close keyboard"""
        client.closeKeyboard()

    def device_action(self, client, action):
        """perform action on device"""
        client.deviceAction(action)

    def drag_coordinates(self, client, *args):
        """drag from (x1,y1) to (x2, y2)"""
        x_coord1, y_coord1, x_coord2, y_coord2, sec = args
        client.dragCoordinates2(x_coord1, y_coord1, x_coord2, y_coord2, sec)

    def flick(self, client, direction, offset=0):
        """perform flick parameter direction and offset"""
        client.flick(direction, offset)

    def p2cx(self, client, percent):
        """convert screen percent into pixel on X axis"""
        pixel = client.p2cx(percent)
        return pixel

    def p2cy(self, client, percent):
        """convert screen percent into pixel on Y axis"""
        pixel = client.p2cy(percent)
        return pixel

    def pinch(self, client, *args):
        """perform pinch operation"""
        inside, x_coord, y_coord, radius, horizontal = args
        try:
            client.pinch(inside, x_coord, y_coord, radius, horizontal)
            logging.info(str(time.asctime(time.localtime())) + " pinch-Passed ")
        except InternalException, msg:
            logging.info(str(time.asctime(time.localtime())) + " :: " + str(msg) + " pinch-Failed ")
        except RuntimeException, msg:
            logging.info(str(time.asctime(time.localtime())) + " :: " + str(msg) + " pinch-Failed ")

    def reboot(self, client, sec):
        """reboot machine in given time """
        result = client.reboot(sec)
        return result

    def reset_device_bridge(self, client, device_type):
        """reset the device connection"""
        client.resetDeviceBridgeOS(device_type)

    def run(self, client, command, logger_name):
        """Run the command on device"""
        logger = logging.getLogger(logger_name)
        try:
            logger.info("Run the command: " + command)
            var = client.run(command)
            logger.info("Result: PASSED")
        except InternalException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
        except RuntimeException, msg:
            logger.error("RESULT: FAILED; "+ str(msg))
        return var

    def set_location(self, client, latitude, longitude):
        """set the location of device"""
        client.setLocation(latitude, longitude)
        return True

    def set_network_conditions(self, client, profile, duration):
        """set network conditions"""
        try:
            client.setNetworkConditions(profile, duration)
            logging.info(str(time.asctime(time.localtime())) + " Network Condition set-Passed ")
        except InternalException, msg:
            logging.info(str(time.asctime(time.localtime())) + " :: " + str(msg) + \
                         " Network Condition set-Failed ")
        except RuntimeException, msg:
            logging.info(str(time.asctime(time.localtime())) + " :: " + str(msg) + \
                         " Network Condition set-Failed ")

    def set_property(self, client, key, value):
        """set the property name as key with value"""
        client.setProperty(key, value)
        return True

    def shake(self, client):
        """perform shake on device"""
        client.shake()
        return True

    def sync(self, client, silent_time, sensitivity, timeout):
        "Perform sync"
        var = client.sync(silent_time, sensitivity, timeout)
        return var

    def sync_elements(self, client, silent_time, timeout):
        """Sync Element"""
        var = client.syncElements(silent_time, timeout)
        return var

    def simulate_capture(self, client, picture_path):
        """Simulate Capture"""
        client.simulateCapture(picture_path)

    def get_property(self, client):
        """Returns property, not properly defined function"""
        client.getProperty()

    def start_logging_device(self, client, path):
        """start generating logs"""
        client.startLoggingDevice(path)
        logging.info(str(time.asctime(time.localtime())) + " Logging Started !!!")

    def stop_logging_device(self, client):
        """stops logging for device and return file path"""
        path = client.stopLoggingDevice()
        logging.info(str(time.asctime(time.localtime())) + "Log file Location: " + path)

    def set_authentication_reply(self, client, reply, delay):
        """Set Authentication Reply"""
        client.setAuthenticationReply(reply, delay)

    def collect_support_data(self, client):
        """Returns supported data"""
        client.collectSupportData()
