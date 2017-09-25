from pywinauto.application import Application
import unittest, os
from VersionInfo import getVersionInfo
ver = getVersionInfo()

class GatewayStartTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_GatewayStartTest(self):
        script_path = os.path.dirname(__file__)
        print script_path
        script_dir = os.path.split(script_path)[0]
        print script_dir
        #projDir = os.path.join(script_dir, 'V1.16' + '\\' + 'GateWay' + '\\' + 'GatewayCommunication' + '\\')
        #projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.18' + '\\' + 'V1.18' + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'GateWay' + '\\' + 'GatewayCommunication' + '\\' )
        projDir = os.path.join(script_dir, 'SRC' + '\\' + ver + '\\' + ver + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'GateWay' + '\\' + 'GatewayCommunication' + '\\' )
        
        print projDir
        
        app = Application().connect(path = projDir + r"GatewayCommunication.exe")
        print app.Gateway.PrintControlIdentifiers()
        app.Gateway.Start.Wait('ready').Click()

    def tearDown(self):
        pass

if __name__ == '__main__':
	unittest.main()










