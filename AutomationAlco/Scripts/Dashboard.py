    
from pywinauto.application import Application
#from pywinauto.sysinfo import UIA_support
#from pywinauto import backend
import unittest, os

#print "******************" + pywinauto.__file__

from VersionInfo import getVersionInfo
ver = getVersionInfo()

class aDashboardStartTest(unittest.TestCase):
    print "**************************Test Dashboard**************************"
    def setUp(self):
        pass

    def test_1GatewayStartTest(self):
        script_path = os.path.dirname(__file__)
        print script_path
        script_dir = os.path.split(script_path)[0]
        print script_dir
        #projDir = os.path.join(script_dir, 'V1.16' + '\\' + 'GateWay' + '\\' + 'GatewayCommunication' + '\\')
        projDir = os.path.join(script_dir, 'SRC' + '\\' + ver + '\\' + ver + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'GateWay' + '\\' + 'DashboardApp' + '\\' )
        print projDir

        app = Application().start(projDir + r"DashboardApp.exe")
        app = Application(backend="uia").connect(path = projDir + r"DashboardApp.exe")
        
        print app.Dashboard.PrintControlIdentifiers()
        app.Dashboard.Start.click()


        '''
        app.Dashboard.Configuration.click()
        app.Dashboard.Configuration.PrintControlIdentifiers()
        app.Dashboard.Configuration.Sender.click()
        #app.Dashboard.Configuration.cancel.click()
        '''

    def tearDown(self):
        pass

if __name__ == '__main__':
	unittest.main()










