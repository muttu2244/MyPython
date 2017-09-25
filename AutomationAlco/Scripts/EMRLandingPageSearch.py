import unittest, os
#import HTMLTestRunner
from pywinauto.application import Application
from EMRPatientDataFeed import PatientRegistration
from ReadUIInputData import readUIInput

from VersionInfo import getConfig
ver = getConfig()

class bUILandingPageTest(unittest.TestCase):
    print "**************************Test EMRLanding**************************"
    #mshData = GetMshInputData()
    def setUp(self):
        #self.host = "localhost"
        #self.port = 8889
        #self.client = Client()
        #self.client.init(self.host, self.port, True)
        #self.client.setProjectBaseDirectory("C:\\Users\\do299817.WIPRO\\workspace\\project2")
        #self.client.setReporter2("xml", "reports", "Untitled")

        
        #os.system(projDir + "\\EMR\\EMRApp\\EMRApp.exe ")

        pass

    def test_2LandingPage(self):
        
        script_path = os.path.dirname(__file__)
        print script_path
        script_dir = os.path.split(script_path)[0]
        print script_dir
        #projDir = os.path.join(script_dir, 'V1.16' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
        
        #projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.20' + '\\' + 'V1.20' + '\\' + 'Alcon' + '\\' + 'output'  + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
        projDir = os.path.join(script_dir, 'SRC' + '\\' + ver[0] + '\\' + ver[0] + '\\' + 'Alcon' + '\\' + 'output'  + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
        print projDir

        #app = Application().start(r"D:\MedicalDevices\AlconProject\TestAutomation\V1.12\EMR\EMRApp\EMRApp.exe")
        app = Application().start(projDir + r"EMRApp.exe")
        #app = Application().connect(path = r"D:\MedicalDevices\AlconProject\TestAutomation\V1.12\EMR\EMRApp\EMRApp.exe")
        app = Application().connect(path = projDir + r"EMRApp.exe")
        #app = Application(backend="uia").connect(path = projDir + r"EMRApp.exe")
        cabinetwclass = app.EMRApp
        cabinetwclass.Wait('ready',timeout=100)

        print app.EMRApp.PrintControlIdentifiers()
        DataFeederList = readUIInput(script_path + '\\ADTUIInputTestData.xlsx')
        print DataFeederList

        for data in DataFeederList:
            app.EMRApp.Patient.Wait('ready').Click()
            #Calling the patient registration function from EMRPatientDataFeed module
            PatientRegistration(data, app)
            #print app.Landing.PrintControlIdentifiers()

        #app.EMRApp.Close()

        #print app.EMRApp.Menu()
        #app.EMRApp.GetFocus().Close()
        #MenuItms = app.EMRApp.MenuSelect("View->Order/Schedule")
        #app.EMRApp.menuStrip1.ClickInput('#0->#0', app)
        #app.EMRApp.menuStrip1.MenuItem("View->Order/Schedule")


    def tearDown(self):
        #self.client.generateReport2(False);
        # Releases the client so that other clients can approach the agent in the near future. 
        #self.client.releaseClient();
        pass


if __name__ == '__main__':
	unittest.main()
	
