import sys
import os
import unittest
import config

reload(sys)
sys.setdefaultencoding('utf8')

SYS_PATH = os.path.dirname(os.getcwd())
sys.path.insert(0, SYS_PATH + r"\\lib\\")
from BaseAPI import Utility, Misc, Application, Objects, Common, Device, Navigate


class TestReporter(unittest.TestCase):
    """Class to test the country feature screens"""

    def setUp(self):
        self.util = Utility()
        self.common = Common()
        self.misc = Misc()
        self.dev = Device()
        self.app = Application()
        self.object = Objects()
        self.navigate = Navigate()
        self.util.set_up()


        self.device_name = self.dev.get_connected_devices(self.util.client)
        self.misc.set_device(self.util.client,
                             self.device_name)  # connect only one device with system
        self.device_info_path = self.misc.get_devices_information(self.util.client,
                                                                  SYS_PATH,
                                                                  self.device_name)
        self.app_name = self.util.get_app_name(self.device_info_path, self.device_name)
        self.app.launch(self.util.client, self.app_name, True, True)


        self.common.set_project_base_directory(self.util.client, os.getcwd())
        self.common.set_reporter(self.util.client, SYS_PATH,
                                 os.path.splitext(os.path.basename(__file__))[0])

    def test_reporter(self):
        self.util.client.sleep(3000)
        self.common.capture(self.util.client, SYS_PATH, "Capture", "test")
        self.object.click(self.util.client, "WEB", "xpath=//*[@id='menu3']", 0, 1)



    def tearDown(self):
        # Generates a report of the test case.
        # For more information-https://docs.experitest.com/display/public/SA/Report+Of+Executed+Test
        self.common.generate_report(self.util.client, False)
        # Releases the client so that other clients can approach the agent in the near future.
        self.common.release_client(self.util.client)


if __name__ == '__main__':
    unittest.main()
