import sys, os
import unittest,webbrowser, time
from VersionInfo import getVersionInfo
ver = getVersionInfo()

class stopBatTest(unittest.TestCase):
    #mshData = GetMshInputData()
    def setUp(self):
        #webbrowser.open('http://l-442000187/CommunicationService/Service1.svc')
        pass
        

    def test_stopBat(self):
        #time.sleep(5)
        script_path = os.path.dirname(__file__)
        print script_path
        script_dir = os.path.split(script_path)[0]
        print script_dir
        #projDir = os.path.join(script_dir, 'V1.16')
        #projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.20' + '\\' + 'V1.20' + '\\' + 'Alcon' )
        projDir = os.path.join(script_dir, 'SRC' + '\\' + ver + '\\' + ver + '\\' + 'Alcon' )
        print projDir
        os.system(projDir + "\\Stop.bat ")

    def tearDown(self):
        #self.client.generateReport2(False);
        # Releases the client so that other clients can approach the agent in the near future. 
        #self.client.releaseClient();
        pass


if __name__ == '__main__':
	unittest.main()






